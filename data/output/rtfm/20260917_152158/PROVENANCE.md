# Provenance of run `20260917_152158` (full RTFM log)

This run was **not** produced by a hosted or local LLM. It was generated from within
[Claude Code](https://claude.com/claude-code) (Anthropic's agentic CLI), with the
**Claude Fable 5.1** model (`claude-fable-5-1`) acting as the LLM for every Step 5a, 6, and 8
call, on 2026-09-17, on a Windows 11 machine with no `GEMINI_API_KEY` and no Ollama install.
It mirrors `experimentation/examples/rtfm/example_run.py` (Steps 1-9, accepted outright on
round 1) with the `manual/` provider substituted for `gemini/gemini-3.5-flash-lite`
(`run_config_snapshot.json`, `concurrency: 1`, `assignment_batch_size: 50`).

The reference run it is compared against is `data/output/rtfm/20260828_181451` (Gemini
3.5 Flash Lite, temperature 0). See `COMPARISON_vs_gemini_20260828_181451.md`.

## How the LLM calls were made

Seven calls: one Step 5a taxonomy induction over the 34-narrative sample, five Step 6 assignment
batches (50, 50, 50, 50, 31 narratives), one Step 8 goal-alignment batch over five categories.
For each call the `manual/` adapter wrote the rendered prompt and the pydantic JSON schema to a
hand-off directory and waited for a response file, which Claude Code wrote. Every reply then went
through the pipeline's normal schema validation, grounding check and axis-partition check.

The prompts are the ones saved by the pipeline itself (`round1/05_taxonomy/taxonomy_prompt.txt`,
`round1/06_assignment/assignment_prompts/`, `round1/08_description/description_prompt.txt`); the
verbatim replies are in the `raw_response` field of each `*_run_metadata.json`.

## Conditions that differ from the Gemini reference run, stated plainly

**Temperature.** `run_config_snapshot.json` and every `RunMetadata` record `temperature: 0`
because that value is copied from the config. It describes nothing about how the replies were
produced: the model acting as the LLM had no temperature control and no access to its sampling
parameters, and a rerun of the same prompts would very likely differ in wording and could differ
on borderline variants. This run is **not** a matched-temperature counterpart of the Gemini run
and should not be read as a determinism or stability measurement.

**Isolation.** Gemini saw only each prompt. The model acting as the LLM here had additional
context before answering: the repository source (including `check_axis_partition` and the prompt
templates), the README and goal-model documentation, the completed `rtfm_mini` runs, and, before
Step 5a and Step 6 ran, the Gemini RTFM run's category names, per-category variant counts and
precision figures. It did **not** read Gemini's per-variant assignments until all 231 of its own
were written, and it fixed its assignment rules (below) before the first Step 6 batch. Before
Step 8 it had additionally read Gemini's Step 8 texts and indicator table; its Step 8 replies
cite only numbers present in its own prompt. None of this is an isolation guarantee, only a
record of what was and was not in context.

**Cost and latency.** Nothing was metered: `input_tokens`/`output_tokens` are null and
`estimated_cost_usd` is null. `latency_seconds` measures the agent's read-and-write turnaround
per call, not model inference.

## Assignment rules applied in Step 6

Fixed before batch 1 and applied to all 231 variants:

1. A case ending at `Send Fine` with no payment, appeal or collection activity is still open and
   goes to the residual (only `V0003`, 20,385 cases, 13.6% of the log).
2. Payment before any `Insert Fine Notification` / `Add penalty`, with no appeal, is
   `timely_payment`, including when a `Send Fine` is logged after the payment.
3. Payment after enforcement began, with no appeal, is `delinquent_payment`, whatever the number
   or placement of `Payment` events.
4. `Send for Credit Collection` as the closure, with no appeal, is `coercive_credit_collection`,
   even after partial payments.
5. Any appeal activity (`Insert Date Appeal to Prefecture`, `Send Appeal to Prefecture`,
   `Appeal to Judge`, or a Prefecture result) makes the case a contested one and it is assigned
   to the appeal branch, **regardless of whether payment or credit collection follows**; the
   later closure is read as the enforcement of the appeal's outcome.
6. When both appeal branches appear in one case (which the goal model's XOR forbids), the case
   is assigned to the branch **last lodged** (`Appeal to Judge` after a Prefecture result is an
   escalation to the Judge; a Prefecture filing after an early `Appeal to Judge` goes to the
   Prefecture). Every such rationale says the mixed appeals merit reviewer attention.

Rule 5 is the main systematic difference from the Gemini run, which assigned appeal-then-closure
cases by the closing activity. Both readings are defensible against the goal model; the
comparison document quantifies the consequence.
