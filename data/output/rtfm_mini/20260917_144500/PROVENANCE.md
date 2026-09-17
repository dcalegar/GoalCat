# Provenance of run `20260917_144500`

This run was **not** produced by a hosted or local LLM. It was generated from within
[Claude Code](https://claude.com/claude-code) (Anthropic's agentic CLI), with the
**Claude Fable 5.1** model (`claude-fable-5-1`) acting as the LLM for every Step 5a, 6, and 8
call, on 2026-09-17, on a Windows 11 machine with no `GEMINI_API_KEY` and no Ollama install.

## How the LLM calls were made

The run used the `manual/` provider added to `src/goalcat/llm/llm_backend.py` in the same pull
request (model string `manual/claude-fable-5-1`, see `run_config_snapshot.json`). For each call
the adapter wrote the rendered prompt and the pydantic JSON schema to a hand-off directory and
waited for a response file. Claude Code, running the pipeline as a background process, read each
prompt file and wrote the JSON reply by hand. Every reply then went through the pipeline's normal
schema validation, grounding check and axis-partition check, exactly as a model's would.

The prompts are the ones saved by the pipeline itself (`roundN/05_taxonomy/taxonomy_prompt.txt`,
`roundN/06_assignment/assignment_prompts/`, `roundN/08_description/description_prompt.txt`); the
verbatim replies are in the `raw_response` field of each `*_run_metadata.json`. Because nothing was
metered, `input_tokens`/`output_tokens` are null, `estimated_cost_usd` is null, and
`latency_seconds` measures the human/agent turnaround (about 35 to 60 s per call), not model
inference time.

One field of this run's metadata is stale rather than merely unknown: `temperature` reads `0.0`,
copied from the config by the adapter as first merged. No sampling temperature governed these
replies, and the field says nothing about how they were produced. The adapter now records `null`
there for every manual call (commit `ed580ef`), so a fresh manual run will not carry the `0.0`
this one does. The recorded value is left as written rather than edited after the fact.

## One deviation from `example_run.py`, visible in `pipeline.log`

The driver mirrored `experimentation/examples/rtfm_mini/example_run.py`. Its scripted reviewer,
as committed at the time, requested a merge of "the first two induced categories". The round-1
taxonomy listed `timely_payment` (anchor id 12, under Or point 4) first and `delinquent_payment`
(anchor id 13, under Or point 6) second, and Step 5a's `check_axis_partition` rejected the
resulting round-2 taxonomy because the two anchors sit under different decomposition points. That
failed attempt is recorded in `pipeline.log` (the `ValueError` at 14:48:11).

The run was then resumed at round 1 with a reviewer decision the rule permits, merging
`delinquent_payment` and `coercive_credit_collection` (ids 13 and 20, both children of Or
point 6). That is the decision preserved in
`round1/09_review/review_decisions_processed_20260917_184938.yaml`; the original
`timely_payment`+`delinquent_payment` request was overwritten by the resume and is not on disk.
Round 2 then ran Steps 5a to 8 with the merged taxonomy and was accepted. The same pull request
changes `example_run.py` to pick such a pair itself (`_mergeable_pair()`), so a fresh run of the
script no longer needs this manual intervention.

## Comparison with the Gemini reference run `20260831_064805`

Round 1 is identical in everything the pipeline treats as the result: the same five categories
anchored to ids 12, 13, 14, 19, 20, the same evidence variants, the same Step 6 partition with
`V0001` in the residual, fitness 1.00 throughout and precision 1.00 except 0.95 for delinquent
payment. Only the category slugs and the prose of Step 8's goal-alignment assessments differ.
Round 2 differs in which pair was merged: the Gemini run merged ids 12 and 13, which predates the
partition check (commit `b016cb9`, same day) and would be rejected by the current code.
