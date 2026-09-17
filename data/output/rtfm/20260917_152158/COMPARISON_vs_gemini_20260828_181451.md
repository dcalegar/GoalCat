# Full RTFM: Claude Fable 5.1 (manual provider, run `20260917_152158`) vs Gemini 3.5 Flash Lite (run `20260828_181451`)

Both runs execute `experimentation/examples/rtfm/example_run.py`'s sequence on the same log
(150,370 cases, 231 variants), the same frozen goal model, the same prompt templates and the same
34-narrative sample, accepting the round-1 taxonomy outright. Only the LLM differs. Read
`PROVENANCE.md` first: the two runs are **not** matched on temperature or on isolation, so the
differences below are descriptive, not an experiment.

## Step 5a: taxonomy

Identical in structure. Both induce five categories mapped 1:1 to the declared alternatives
(anchor ids 12, 13, 14, 19, 20), no subdivision, no merge. Only the slugs differ
(`resolve_timely_payment` vs `timely_payment`, and so on). Both pass the grounding check; the
manual run also passes `check_axis_partition`, which did not yet exist when the Gemini run was
made (it was added in commit `b016cb9` on 2026-08-31, after this Gemini run of 2026-08-28).

## Step 6: assignment

| | Gemini | Manual |
|---|---|---|
| Variants agreeing | 142 of 231 | |
| Cases agreeing | 149,396 of 150,370 (99.35%) | |
| Residual | 10 variants, 20,861 cases | 1 variant, 20,385 cases |

Case-level agreement is high because the four largest variants (85% of the log) are assigned
identically. The 89 disagreeing variants carry 974 cases (0.65%) and fall into three groups.

**1. A rule difference on appeal-then-closure cases (46 variants, 434 cases).** When an appeal
is lodged and the case is later closed by payment or credit collection, Gemini assigned by the
closing activity (`resolve_coercive_credit_collection` for 27 variants, `resolve_delinquent_payment`
for 15); the manual run assigned by the contest (rule 5 in `PROVENANCE.md`). Neither reading
contradicts the goal model, which does not say which alternative "resolves" a case that was both
contested and then enforced. The measured consequence is visible in Step 7b below.

**2. Gemini assignments that contradict its own category descriptions (29 variants, 52 cases).**
Gemini labelled 29 variants `resolve_timely_payment` although every one of them contains
`Insert Fine Notification` and `Add penalty`, and most also an appeal (for example `V0141`:
notification, penalty, Prefecture appeal, ten payments; `V0147`: notification, Appeal to Judge,
penalty, twelve payments). Timely payment is defined in both runs as payment *before*
enforcement. The manual run put 21 of these under the Prefecture appeal, 5 under the Judge and 3
under delinquent payment. These are low-frequency variants (52 cases in total), which is why the
case-level agreement is barely affected, but they inflate Gemini's timely-payment category from
7 to 34 variants and are the reason its precision there is 0.90 instead of 1.00.

**3. Residual handling (9 variants, 480 cases).** Gemini sent to the residual six variants that
run a complete Prefecture appeal cycle ending at `Receive Result` or `Notify Result`
(`V0030`, `V0032`, `V0034`, `V0038`, `V0046`, `V0077`: 108 cases), one early `Appeal to Judge`
(`V0093`), and two variants that pay before the fine is dispatched (`V0012`, 362 cases, and
`V0193`). The manual run assigned all nine; it treats a completed appeal as realizing the appeal
alternative and a pre-dispatch payment as timely payment. Both runs put `V0003`
(Create Fine, Send Fine, nothing else; 20,385 cases) in the residual.

Per-category variant counts:

| Category | Gemini | Manual |
|---|---|---|
| Timely payment | 34 | 7 |
| Delinquent payment | 33 | 21 |
| Administrative appeal (Prefecture) | 64 | 129 |
| Judicial appeal (Judge) | 50 | 60 |
| Coercive credit collection | 40 | 13 |
| Residual | 10 | 1 |

## Step 7: discovery

Fitness is 1.00 for every category in both runs. Precision differs where the assignment rules do:

| Category | Gemini cases / precision | Manual cases / precision |
|---|---|---|
| Timely payment | 49,658 / 0.90 | 49,969 / 1.00 |
| Delinquent payment | 16,875 / 0.38 | 16,851 / 0.74 |
| Administrative appeal | 3,602 / 0.54 | 4,042 / 0.55 |
| Judicial appeal | 380 / 0.56 | 525 / 0.54 |
| Coercive credit collection | 58,996 / 0.53 | 58,598 / 1.00 |

The manual partition yields tightly bounded models for the three non-appeal categories because
no appeal behaviour is mixed into them; Gemini's credit-collection and delinquent-payment models
have to admit appeal steps and so are loose. The two appeal categories are loose in both runs,
for the same reason: the Prefecture alternative's four AND steps occur in many orders and are
often incomplete, and both runs hold cases that mix the two appeal branches.

## Step 7b: measured indicator satisfaction

Deterministic, so every difference below is a consequence of Step 6. The cleanest diagnostic is
which indicators are *applicable* per category:

| Indicator | Gemini: applicable in | Manual: applicable in |
|---|---|---|
| Time to appeal filing, Prefecture | all five categories | the two appeal categories only |
| Time to appeal filing, Judge | all five categories | the two appeal categories only |

In the manual run the three non-appeal categories contain zero appeal filings (the indicator is
`not applicable` for every case), which is what the goal model's decomposition implies. In the
Gemini run they contain 265 Prefecture filings and 146 Judge filings under credit collection, 24
and 1 under delinquent payment, and 33 and 9 under timely payment. Where both runs measure the
same indicator on the same category, the values are close:

| Category, indicator | Gemini | Manual |
|---|---|---|
| Timely payment, closure | 17.8 d (+100) | 17.4 d (+100) |
| Delinquent payment, closure | 356.6 d (-95) | 356.5 d (-95) |
| Delinquent payment, dispatch | 91.6 d (+0) | 91.6 d (+0) |
| Credit collection, closure | 690.5 d (-100) | 688.8 d (-100) |
| Prefecture appeal, filing | 50.0 d (+100) | 49.0 d (+100) |
| Prefecture appeal, closure | 355.4 d (-94, coverage 14%) | 481.7 d (-100, coverage 23%) |
| Judge appeal, filing | 109.9 d (-100) | 97.1 d (-100) |
| Judge appeal, closure | 565.9 d (-100, coverage 89%) | 722.6 d (-100, coverage 91%) |

The appeal categories' closure figures are higher in the manual run because it keeps the
appeal-then-collection cases (closures of 600 to 1,400 days) inside the appeal categories, where
Gemini moved them to credit collection.

## Step 8: goal alignment

Same verdicts in both runs: timely payment supported; delinquent payment procedurally achieved
but failing its closure indicator; Prefecture appeal timely at filing but poor at closure; Judge
appeal systematically filed out of time (-100) with the worst closures; credit collection
consistent but with -100 closure. The manual texts add reviewer-facing points Gemini's do not:
that only 23% of Prefecture-appeal cases have any closure in the log, contradicting the anchor
task's "Resolve via"; that 27 Prefecture-appeal and 154 Judge-appeal cases carry both appeal
branches, violating the goal model's XOR in practice; that dispatch time sits at the statutory
threshold for the enforced categories, so part of the "delinquent" delay is administrative; and
that timely payment's dispatch indicator covers only 7% of its cases because most timely payers
are never sent a fine.

## Cost

Gemini: 7 calls, 35,466 input and 13,801 output tokens, about 227 s, about $0.045. Manual: 7
calls, no token metering, no cost; latency is agent turnaround (see `pipeline_usage_summary.json`).
