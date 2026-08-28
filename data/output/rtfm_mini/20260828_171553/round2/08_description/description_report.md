# Step 8 — High-level description generation report

Run: `20260828_171553` | Log: `rtfm_mini` | Description model: `gemini/gemini-3.5-flash-lite`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Resolve via payment (`payment_resolution`)

**Declared (Step 5):** Resolution of the fine case through offender payment, either timely or after penalties have been applied, helping maximize timely fine revenue and minimize administrative and enforcement costs, evaluated against average time to case closure.

**Goal-model linkage:** 12 (Task): Resolve via timely payment; 13 (Task): Resolve via delinquent payment

**Coverage:** 2 variants, 2 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 2 distinct variants accounts for 50% of cases. Waiting times between activities are consistent and predictable across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The discovered evidence shows moderate concentration with consistent waiting times, and the tightly bounded model (fitness 1.00, precision 1.00) supports the execution of timely and delinquent payment tasks. However, the measured satisfaction for average time to case closure is -51 (external-by-analogy, 2/2 cases) and time to fine dispatch is -14 (statutory, coverage 50%), indicating that while the process successfully resolves through payment, it performs poorly against the timeliness goals anchored to tasks 12 and 13.

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

**Declared (Step 5):** Resolution via an administrative appeal submitted to the Prefecture, preserving due-process rights while impacting administrative cost and fine revenue, measured against 'Time to appeal filing, Prefecture'.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The single case in this category follows a deterministic path with a tightly bounded model (fitness 1.00, precision 1.00), perfectly aligning with task 14's goal of resolving via administrative appeal to the Prefecture. This is reinforced by maximum measured satisfaction scores of +100 for time to fine dispatch, time to appeal filing to the Prefecture, and average time to case closure.

## Resolve via judicial appeal to the Judge (`judicial_appeal_judge`)

**Declared (Step 5):** Resolution via a judicial appeal brought before a judge, strongly preserving offender due-process rights while hurting administrative cost, measured against 'Time to appeal filing, Judge'.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The process behavior is captured by a single variant and a tightly bounded model (fitness 1.00, precision 1.00), supporting task 19's goal of resolving via judicial appeal to the Judge. The measured satisfaction shows a positive score of +73 for time to fine dispatch, but a failing score of -100 for time to appeal filing to the judge (statutory, 1/1 cases), reflecting significant delay in the appeal filing step despite successful structural execution.

## Resolve via coercive credit collection (`coercive_credit_collection`)

**Declared (Step 5):** Resolution of the fine case through coercive credit collection steps after penalties are added, helping fine revenue and hurting administrative costs.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The single case follows a predictable, strictly modeled path (fitness 1.00, precision 1.00) supporting task 20's goal of coercive credit collection. However, the measured satisfaction for average time to case closure is -100 (external-by-analogy, 1/1 cases) and time to fine dispatch is -15 (statutory, 1/1 cases), showing that the process executes the collection steps correctly but performs very poorly against timeliness goals.
