# Step 8 — High-level description generation report

Run: `20260917_152158` | Log: `rtfm` | Description model: `manual/claude-fable-5-1`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Resolved via timely payment (`timely_payment`)

**Declared (Step 5):** The offender pays the fine before enforcement begins, that is before any Insert Fine Notification or Add Penalty, typically within days of creation and sometimes before or shortly after the fine is dispatched. The case closes at the first OR branch of 'Fine case is resolved' without entering the enforceable path. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** 7 variants, 49969 cases.

**Discovered pattern:** A single dominant path accounts for 93% of this category's cases, out of 7 distinct variants. Waiting times between activities are highly variable across cases -- worth checking whether this masks a hidden sub-behavior.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** Consistent with achieving task 12. One path (pay directly after creation) carries 93% of the 49,969 cases, the model is tightly bounded (fitness 1.00, precision 1.00), and the measured 'Average time to case closure' of 17.4 days converts to +100 across every case. Two points for the reviewer. First, 'Time to fine dispatch' is measurable for only 7% of these cases (3,586), because most timely payers are never sent a fine at all; the +39 for that minority (66.5 days) says the dispatch that did happen was slow, not that the category has a dispatch problem. Second, the high waiting-time variability flagged in the pattern comes from the minority variants in which payment is logged before or long after Send Fine; they still realize the alternative, but a reviewer may want to confirm that a payment recorded before dispatch is a real payment event and not a data-ordering artefact.

## Resolved via delinquent payment after enforcement (`delinquent_payment`)

**Declared (Step 5):** The fine enters enforcement (Insert Fine Notification, Add Penalty) and is then closed by the offender paying, often late and often in several installments, without any appeal. This alternative helps 'Maximize timely fine revenue' (+50), while the mandatory Add Penalty step slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** 21 variants, 16851 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 21 distinct variants accounts for 56% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 0.74).

**Goal alignment:** The behavior realizes task 13: all 16,851 cases are notified, penalised and then closed by payment, with 56% on the single-payment path and the rest in installment variants, and the model stays fairly tight (fitness 1.00, precision 0.74, the slack coming from the variable number and placement of Payment events). Against the parent goal the measurement is poor: 'Average time to case closure' is 356.5 days, converting to -95 on full coverage. 'Time to fine dispatch' sits exactly at the 90-day statutory threshold (91.6 days, +0), so the organization consumed the whole lawful dispatch window before the offender's delinquency even began. The alternative is therefore achieved procedurally while the closure indicator it is judged on is nearly at its worst, and part of that delay is administrative rather than the offender's. Worth reviewer attention as a process-performance finding rather than a categorization problem.

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

**Declared (Step 5):** The offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received and notified to the offender. One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** 129 variants, 4042 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 129 distinct variants accounts for 62% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.55) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** The category does realize task 14 in the sense that 96% of its 4,042 cases have a measurable Prefecture filing, and that filing is timely: 49.0 days converts to +100 against the statutory 60-day limit. But the evidence sits awkwardly against the anchor in three ways the reviewer should weigh. First, the model is loose (precision 0.55) and 129 variants share the category, because the alternative's four AND-decomposed steps occur in many orders and are often incomplete, and because the category as assigned also holds cases that were later closed by payment or credit collection after the appeal. Second, only 23% of cases (942) have a measurable closure at all, and for those 'Average time to case closure' is 481.7 days, -100; the remaining 77% end at an appeal step with no closure logged, so most of these cases are not resolved within the log, which contradicts the anchor task's name 'Resolve via'. Third, 27 cases also carry a Judge filing, at 73.2 days (-100), evidence that the XOR between the two appeal branches is violated in practice. 'Time to fine dispatch' is at the threshold (89.1 days, +1).

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

**Declared (Step 5):** The offender takes the fine to a Judge, logged as Appeal to Judge, usually shortly after notification and before or around the penalty. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** 60 variants, 525 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 60 distinct variants accounts for 26% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Loosely bounded: the model fits the observed cases well (log fitness 1.00) but permits substantially more behavior than was actually observed (precision 0.54) -- consistent with a category that groups together several distinct real paths.

**Goal alignment:** The path evidence supports the anchor only weakly. The category is the most dispersed of the five (60 variants for 525 cases, top variant 26%, precision 0.54), and the measurements undercut the claim that task 19 is achieved lawfully: 'Time to appeal filing, Judge' is 97.1 days against a statutory 30-day limit, converting to -100 on 97% coverage, so judicial appeals in this log are systematically filed out of time. 'Average time to case closure' is 722.6 days, -100, on 91% coverage, the worst closure figure of any category. A further 154 cases (29%) also carry a Prefecture filing (38.8 days, +100), so many of these are escalations after an administrative result rather than pure judicial appeals; the category groups two realities the goal model's XOR says cannot co-occur. 'Time to fine dispatch' is just over the threshold (95.5 days, -2). Reviewer attention warranted: the alternative is exercised, but its declared contribution to due-process rights is not supported by the filing-time measurement.

## Resolved via coercive credit collection (`coercive_credit_collection`)

**Declared (Step 5):** The fine is notified and penalised and, with no payment in full and no successful appeal, the organization hands it to credit collection to enforce it, typically more than a year after the penalty. This alternative helps 'Maximize timely fine revenue' (+50) but hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** 13 variants, 58598 cases.

**Discovered pattern:** A single dominant path accounts for 96% of this category's cases, out of 13 distinct variants. Waiting times between activities show moderate variability across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The path realizes task 20 exactly: 96% of 58,598 cases follow notification, penalty and hand-over with nothing else, and the model is tight (fitness 1.00, precision 1.00; the 13 variants differ only in partial payments before hand-over). The measurement is uniformly poor: 'Average time to case closure' is 688.8 days, -100, on full coverage, and this is the largest category in the log by cases, so it dominates the process-wide closure indicator. 'Time to fine dispatch' is inside the threshold (84.2 days, +9). The alternative is thus achieved as a procedural closure, but the declared +50 contribution to 'Maximize timely fine revenue' is not supported: the hand-over typically follows more than a year of inactivity after the penalty, and whether collection actually recovers revenue is not observable in this log. Reviewer attention warranted on the inactivity gap between penalty and hand-over, which is the organization's own delay.
