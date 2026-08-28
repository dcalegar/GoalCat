"""litellm-backed LLM adapter for Steps 5a/5b, 6, 8.

API keys (GEMINI_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY) are read by litellm straight from
the environment — this module never touches them directly. Project convention: export them from
the user's shell profile (e.g. ~/.bash_profile), never store one in a file inside this repository.
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from ..config import LLMConfig

T = TypeVar("T", bound=BaseModel)


class LLMGenerationError(RuntimeError):
    """Raised when an LLM call fails after exhausting retries (transport or validation)."""


class RunMetadata(BaseModel):
    """Audit record for one LLM call — provider, exact model, params, prompt hash (not the
    full prompt; callers that need the rendered prompt itself save it separately, per the
    pipeline's versioned-prompts requirement), token usage, latency, and the raw response
    behind whatever was parsed/validated from it."""

    provider: str
    model: str
    backend: str
    temperature: float
    prompt_hash: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    prompt_chars: int
    response_chars: int
    raw_response: str


# litellm provider prefixes that route to a locally-hosted model rather than a hosted API —
# checked against the model string's provider segment to fill RunMetadata.backend.
_LOCAL_PROVIDERS = {"ollama", "ollama_chat"}


def estimate_cost_usd(
    metadata: RunMetadata, pricing_usd_per_million_tokens: dict[str, dict[str, float]]
) -> float | None:
    """Estimates a call's cost from RunMetadata's token counts and config.yaml's
    llm.pricing_usd_per_million_tokens (keyed by the same litellm model string as
    taxonomy_model/assignment_model/description_model). Returns None rather than guessing when
    the model has no pricing entry or the provider didn't return token counts (e.g. a local
    Ollama model, which is free) — an unpriced call must read as "unknown", not "$0.00"."""
    rate = pricing_usd_per_million_tokens.get(metadata.model)
    if rate is None or metadata.input_tokens is None or metadata.output_tokens is None:
        return None
    return (metadata.input_tokens * rate["input"] + metadata.output_tokens * rate["output"]) / 1_000_000


class LLMBackend:
    """Thin adapter over litellm — the rest of the pipeline never imports litellm directly,
    the same isolation idiom this project already uses for the vendored LUPIN module
    (`third_party/lupin/`, called only via `subprocess`). One `LLMBackend` is bound to one
    model at construction, matching the per-role model config in `config.yaml`
    (`taxonomy_model`/`assignment_model`/`description_model`) — Steps 5a/5b, 6, and 8 each
    construct their own instance rather than sharing one with a per-call model override.

    No fallback model list is configured on any call: for reproducibility,
    a silent model substitution mid-experiment would change the experimental
    condition without recording that it happened.
    """

    def __init__(self, model: str, config: LLMConfig, logger: logging.Logger | None = None) -> None:
        self._model = model
        self._config = config
        self._logger = logger or logging.getLogger("goalcat")

    async def generate_structured(self, prompt: str, output_schema: type[T]) -> tuple[T, RunMetadata]:
        """Calls the model and validates its response against `output_schema`.

        Retries only on validation failure (the model's response didn't parse against the
        schema) — transient transport errors (timeouts, 5xx, rate limits) are retried
        separately by litellm's own `num_retries`, since the two failure modes call for
        different handling: a validation failure means asking again with the same input,
        a transport failure means the same request didn't arrive or return.
        """
        import litellm

        prompt_hash = _hash_prompt(prompt)
        last_error: Exception | None = None

        for attempt in range(1, self._config.max_retries + 1):
            start = time.monotonic()
            response = await litellm.acompletion(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                response_format=output_schema,
                temperature=self._config.temperature,
                timeout=self._config.timeout_seconds,
                num_retries=self._config.max_retries,
            )
            latency = time.monotonic() - start
            raw_content = response.choices[0].message.content

            try:
                parsed = output_schema.model_validate_json(raw_content)
            except ValidationError as exc:
                last_error = exc
                self._logger.warning(
                    "LLM structured-output validation failed (attempt %d/%d, model=%s, "
                    "prompt_hash=%s): %s",
                    attempt,
                    self._config.max_retries,
                    self._model,
                    prompt_hash,
                    exc,
                )
                continue

            metadata = self._run_metadata(prompt_hash, len(prompt), latency, raw_content, response)
            self._logger.info(
                "LLM structured call ok (backend=%s, model=%s, prompt_hash=%s, latency=%.2fs)",
                metadata.backend,
                self._model,
                prompt_hash,
                latency,
            )
            return parsed, metadata

        raise LLMGenerationError(
            f"LLM structured output did not validate after {self._config.max_retries} "
            f"attempts (model={self._model}, prompt_hash={prompt_hash}): {last_error}"
        )

    async def generate_text(self, prompt: str) -> tuple[str, RunMetadata]:
        """Calls the model for free-form prose. General-purpose method on the adapter -- every
        pipeline step currently uses generate_structured() instead (Step 8's goal_alignment is a
        batched list response, so it needs a schema to map judgments back to category_ids)."""
        import litellm

        prompt_hash = _hash_prompt(prompt)
        start = time.monotonic()
        response = await litellm.acompletion(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self._config.temperature,
            timeout=self._config.timeout_seconds,
            num_retries=self._config.max_retries,
        )
        latency = time.monotonic() - start
        text = response.choices[0].message.content

        metadata = self._run_metadata(prompt_hash, len(prompt), latency, text, response)
        self._logger.info(
            "LLM text call ok (backend=%s, model=%s, prompt_hash=%s, latency=%.2fs)",
            metadata.backend,
            self._model,
            prompt_hash,
            latency,
        )
        return text, metadata

    def _run_metadata(
        self, prompt_hash: str, prompt_chars: int, latency: float, raw_content: str, response
    ) -> RunMetadata:
        usage = getattr(response, "usage", None)
        provider = self._model.split("/", 1)[0]
        return RunMetadata(
            provider=provider,
            model=self._model,
            backend="local" if provider in _LOCAL_PROVIDERS else "remote",
            temperature=self._config.temperature,
            prompt_hash=prompt_hash,
            latency_seconds=latency,
            input_tokens=getattr(usage, "prompt_tokens", None),
            output_tokens=getattr(usage, "completion_tokens", None),
            prompt_chars=prompt_chars,
            response_chars=len(raw_content),
            raw_response=raw_content,
        )


def _hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
