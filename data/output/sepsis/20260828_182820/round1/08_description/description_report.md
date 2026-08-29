# Step 8 — High-level description generation report

Run: `20260828_182820` | Log: `sepsis` | Description model: `gemini/gemini-3.5-flash-lite`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Admission to Normal Care (`admission_nc`)

**Declared (Step 5):** Patient is admitted to a normal care inpatient ward (Admission NC), advancing treatment goals but subject to normal ward management and discharge pathways.

**Goal-model linkage:** 15 (Task): Admission NC

**Coverage:** 85 variants, 98 cases.

**Discovered pattern:** No single path dominates: the most frequent of 85 distinct variants accounts for only 3% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities are highly variable across cases -- worth checking whether this masks a hidden sub-behavior.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.34) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** The discovered evidence shows high variability across 85 variants with low precision (0.34) and mixed KPI satisfaction (e.g., negative time to antibiotics score of -18, positive lactate score of +100), indicating that the Admission NC task captures a loosely bounded group of paths with variable execution consistency.

## Admission to Intensive Care (`admission_ic`)

**Declared (Step 5):** Patient is admitted to an intensive care inpatient ward (Admission IC). This option incurs some negative impact on minimizing time-to-treatment due to transfer overhead, but is required for critical stabilization.

**Goal-model linkage:** 16 (Task): Admission IC

**Coverage:** 11 variants, 11 cases.

**Discovered pattern:** No single path dominates: the most frequent of 11 distinct variants accounts for only 9% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.17) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** The discovered evidence for Admission IC exhibits low precision (0.17) across 11 variants, but demonstrates strong guideline satisfaction for time to antibiotics (+96) and lactate measurement (+100), supporting its role in critical stabilization despite behavioral dispersion.

## Release Pathway A (`release_a`)

**Declared (Step 5):** Captured discharge representing standard release pathway A, helping to avoid post-discharge deterioration.

**Goal-model linkage:** 17 (Task): Release A

**Coverage:** 487 variants, 525 cases.

**Discovered pattern:** No single path dominates: the most frequent of 487 distinct variants accounts for only 1% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities are highly variable across cases -- worth checking whether this masks a hidden sub-behavior.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.30) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Release A shows extensive behavioral dispersion across 487 variants and low model precision (0.30), coupled with near-neutral time to antibiotics satisfaction (+1) and a negative post-discharge ER return indicator (-34), suggesting potential divergence from optimal avoidance of post-discharge deterioration.

## Release Pathway B (`release_b`)

**Declared (Step 5):** Captured discharge representing release pathway B, helping to avoid post-discharge deterioration.

**Goal-model linkage:** 18 (Task): Release B

**Coverage:** 53 variants, 54 cases.

**Discovered pattern:** No single path dominates: the most frequent of 53 distinct variants accounts for only 4% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities are highly variable across cases -- worth checking whether this masks a hidden sub-behavior.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.28) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Release B exhibits 53 variants with low precision (0.28), but achieves favorable measured satisfaction including strong scores for time to antibiotics (+40), lactate measurement (+100), and a maximum score of +100 for zero post-discharge ER returns, fully supporting the goal of avoiding post-discharge deterioration.

## Release Pathway C (`release_c`)

**Declared (Step 5):** Captured discharge representing release pathway C for specific patient recovery profiles.

**Goal-model linkage:** 19 (Task): Release C

**Coverage:** 23 variants, 23 cases.

**Discovered pattern:** No single path dominates: the most frequent of 23 distinct variants accounts for only 4% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities are highly variable across cases -- worth checking whether this masks a hidden sub-behavior.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.25) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Release C displays high path variability across 23 variants with low precision (0.25). While lactate measurement scores are optimal (+100), the time to antibiotics score is near-neutral (+2) and post-discharge ER returns yield a negative score (-17), showing partial alignment with specific recovery profiles.

## Release Pathway D (`release_d`)

**Declared (Step 5):** Captured discharge representing release pathway D.

**Goal-model linkage:** 20 (Task): Release D

**Coverage:** 23 variants, 23 cases.

**Discovered pattern:** No single path dominates: the most frequent of 23 distinct variants accounts for only 4% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities are highly variable across cases -- worth checking whether this masks a hidden sub-behavior.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.24) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Release D is characterized by 23 variants with low model precision (0.24) and poor time to antibiotics satisfaction (-62), alongside a negative post-discharge ER return indicator (-39), indicating that the observed process behavior sits awkwardly against expected release standards.

## Release Pathway E (`release_e`)

**Declared (Step 5):** Captured discharge representing release pathway E.

**Goal-model linkage:** 21 (Task): Release E

**Coverage:** 6 variants, 6 cases.

**Discovered pattern:** No single path dominates: the most frequent of 6 distinct variants accounts for only 17% of cases -- behavior is spread widely across many distinct paths. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.20) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** Release E covers only 6 cases with low precision (0.20) and features a heavily penalized time to antibiotics score (-100 with only 50 percent coverage), suggesting that the process behavior for this pathway frequently fails to meet guideline thresholds.
