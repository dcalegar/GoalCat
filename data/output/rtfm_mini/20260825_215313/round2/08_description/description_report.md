# Step 8 — High-level description generation report

Run: `20260825_215313` | Log: `rtfm_mini` | Description model: `gemini/gemini-3.5-flash-lite`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Resolve via payment (`payment_resolution`)

**Declared (Step 5):** Resolution of the fine case through payment, encompassing both early payment before penalties and delinquent payment after notification and penalty have been applied. Advances Maximize timely fine revenue and Minimize administrative & enforcement cost.

**Goal-model linkage:** 12 (Task): Resolve via timely payment; 13 (Task): Resolve via delinquent payment

**Coverage:** 2 variants, 2 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 2 distinct variants accounts for 50% of cases. Waiting times between activities are consistent and predictable across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The discovered pattern and model looseness (perfect fitness and precision) confirm standard payment paths, but measured satisfaction indicates significant delays with an average time to case closure score of -51 (external-by-analogy) and a time to fine dispatch score of -14 (statutory, 50% coverage), showing friction in achieving timely payment.

## Resolve via administrative appeal to the Prefecture (`administrative_appeal_to_prefecture`)

**Declared (Step 5):** Contested appeal resolved through administrative process via the Prefecture. Preserves offender's due-process rights while impacting costs and revenue.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The single-case variant is tightly bounded with perfect fitness and precision, and the measured satisfaction scores all reach the maximum +100 (statutory and external-by-analogy), demonstrating strong alignment with resolving via administrative appeal to the Prefecture.

## Resolve via judicial appeal to the Judge (`judicial_appeal_to_the_judge`)

**Declared (Step 5):** Contested appeal resolved through the judicial system. Makes a strong positive contribution to preserving offender's due-process rights while hurting administrative costs.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** Although the process model is tightly bounded and time to fine dispatch scores moderately at +73 (statutory), the time to appeal filing to the Judge scores -100 (statutory, one-sided scale), indicating severe delays in filing that challenge the successful realization of a timely judicial appeal.

## Resolve via coercive credit collection (`coercive_credit_collection`)

**Declared (Step 5):** Resolution of the fine case through coercive credit collection procedures after notifications and penalties. Helps timely revenue while hurting enforcement costs.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The process model is tightly bounded with perfect fitness and precision, but measured satisfaction shows poor performance with a time to fine dispatch score of -15 (statutory) and an average time to case closure score of -100 (external-by-analogy), reflecting extreme delays in concluding coercive collection.
