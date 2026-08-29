# Step 8 — High-level description generation report

Run: `20260828_181451` | Log: `rtfm` | Description model: `gemini/gemini-3.5-flash-lite`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Resolve via timely payment (`resolve_timely_payment`)

**Declared (Step 5):** Fines resolved through prompt payment, maximizing timely fine revenue and helping minimize administrative and enforcement cost, judged against average time to case closure.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** 34 variants, 49658 cases.

**Discovered pattern:** A single dominant path accounts for 93% of this category's cases, out of 34 distinct variants. Waiting times between activities show moderate variability across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 0.90).

**Goal alignment:** The discovered pattern shows strong path concentration with 93% of cases following a single dominant path and high model precision (0.90). This aligns well with the goal of resolving via timely payment and minimizing costs. Measured satisfaction supports this with an optimal score of +100 for average time to case closure (external-by-analogy, 100% coverage), despite mixed statutory indicators on specific delay sub-metrics.

## Resolve via delinquent payment (`resolve_delinquent_payment`)

**Declared (Step 5):** Enforced cases resolved through delayed payment after notification and penalty additions, helping maximize timely fine revenue, judged against average time to case closure.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** 33 variants, 16875 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 33 distinct variants accounts for 56% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.38) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Moderate path concentration (56% on the top variant) and lower model precision (0.38) indicate a grouping of several distinct real paths, which matches the delinquent nature of these cases. Measured satisfaction for average time to case closure is heavily negative (-95, external-by-analogy, 100% coverage), reflecting the inherent delay and administrative cost penalties associated with delinquent resolution.

## Resolve via administrative appeal to the Prefecture (`resolve_administrative_appeal`)

**Declared (Step 5):** Contested cases resolved through the administrative appeal process involving the Prefecture, preserving due-process rights while potentially increasing costs and delaying revenue, judged against time to appeal filing, Prefecture.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** 64 variants, 3602 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 64 distinct variants accounts for 69% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.54) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Moderate path concentration (69% on the primary variant) and lower model precision (0.54) reflect a variety of administrative appeal trajectories. Measured satisfaction shows a very strong score of +100 for time to appeal filing to the Prefecture (statutory, 96% coverage), but a severely negative score of -94 for average time to case closure (external-by-analogy, 14% coverage), supporting the trade-off of preserved due-process rights against delayed revenue and closure.

## Resolve via judicial appeal to the Judge (`resolve_judicial_appeal`)

**Declared (Step 5):** Contested cases resolved via judicial appeal to a judge, strongly making offender due-process rights while hurting administrative costs, judged against time to appeal filing, Judge.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** 50 variants, 380 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 50 distinct variants accounts for 36% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.56) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Dispersion is high, with the top variant accounting for only 36% of cases and a model precision of 0.56. Measured satisfaction reveals extreme negative scores for judicial appeal filings (-100, statutory, 97% coverage) and average time to case closure (-100, external-by-analogy, 89% coverage), highlighting the heavy cost to timeliness and administrative efficiency inherent in judicial appeals.

## Resolve via coercive credit collection (`resolve_coercive_credit_collection`)

**Declared (Step 5):** Cases resolved via coercive credit collection actions after enforcement steps, helping revenue but hurting administrative costs, judged against average time to case closure.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** 40 variants, 58996 cases.

**Discovered pattern:** A single dominant path accounts for 96% of this category's cases, out of 40 distinct variants. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.53) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** The discovered pattern exhibits exceptionally high concentration, with a single dominant path accounting for 96% of cases. Despite this behavioral consistency, the model precision is loose (0.53). Measured satisfaction reflects a severely negative score of -100 for average time to case closure (external-by-analogy, 100% coverage), which aligns directly with the goal's premise that coercive collection actions help revenue but heavily impact administrative time and costs.
