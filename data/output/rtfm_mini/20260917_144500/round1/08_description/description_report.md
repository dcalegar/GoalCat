# Step 8 — High-level description generation report

Run: `20260917_144500` | Log: `rtfm_mini` | Description model: `manual/claude-fable-5-1`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Resolved via timely payment (`timely_payment`)

**Declared (Step 5):** The offender pays the fine directly after it is created, before any notification or penalty. The case closes at the first OR branch of 'Fine case is resolved' without entering enforcement. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** Consistent with achieving task 12. The single case pays one day after fine creation and never enters enforcement, and the measured 'Average time to case closure' of 1.0 days converts to +100 satisfaction, so the case closes well inside even the statutory dispatch window. The model is tightly bounded (fitness 1.00, precision 1.00), so nothing beyond the declared path is being admitted. One caveat for the reviewer: the evidence is a single case, so this confirms the alternative exists in the log, not how it behaves in general.

## Resolved via delinquent payment after enforcement (`delinquent_payment`)

**Declared (Step 5):** The fine goes through the enforcement path (Insert Fine Notification, Add Penalty) and is then closed by the offender paying, possibly in more than one installment. This alternative helps 'Maximize timely fine revenue' (+50), while the mandatory Add Penalty step it contains slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** 3 variants, 3 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 3 distinct variants accounts for 33% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 0.95).

**Goal alignment:** The discovered behavior does realize task 13: all three cases are notified, penalised, and closed by payment, and the model stays tight (fitness 1.00, precision 0.95, the small slack coming from the repeated Payment and the penalty/payment reordering). But the measurements sit awkwardly against the goal it serves. 'Average time to case closure' is 328.0 days, converting to -79, and 'Time to fine dispatch' is 126.3 days, converting to -13 against a statutory threshold of 90 days. So the alternative is achieved procedurally while the parent goal's own indicator is failed, and the dispatch delay precedes the offender's delinquency and is the organization's own. Worth reviewer attention: the closure delay largely originates upstream of the payment itself, so the category name attributes the slowness to the offender when a share of it is administrative.

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

**Declared (Step 5):** After notification the offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received (and notified to the offender). One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** Consistent with achieving task 14. The single case files its Prefecture appeal 5.0 days after notification (+100 against the statutory 60-day limit), the fine was dispatched in 0.0 days (+100), and the case closes in 78.0 days (+100). All measured indicators are satisfied and the model is tightly bounded (fitness 1.00, precision 1.00). Two points for the reviewer: the case ends at 'Receive Result Appeal from Prefecture' without the declared 'Notify Result Appeal to Offender' step, so the AND-decomposed alternative is realized only partially in the log; and the penalty is added while the appeal is pending, which the goal model does not forbid but which bears on the due-process softgoal this alternative is meant to advance. Single-case evidence.

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

**Declared (Step 5):** After notification and penalty the offender takes the fine to a Judge. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The path matches task 19 (notification, penalty, then Appeal to Judge) and the model is tight (fitness 1.00, precision 1.00), but the measured evidence undercuts the claim that the alternative is achieved lawfully. 'Time to appeal filing, Judge' is 81.0 days against a statutory 30-day limit, converting to -100. The appeal was therefore filed well out of time, so the due-process goal this alternative is supposed to fully advance is not actually met on the one case observed. 'Average time to case closure' is not applicable because the case has no closing activity after the appeal, meaning the case is still open at log end. Both points deserve reviewer attention; the evidence is a single case.

## Resolved via coercive credit collection (`coercive_credit_collection`)

**Declared (Step 5):** The fine is notified and penalised but never paid or appealed, and the organization hands it to credit collection to enforce it. This alternative helps 'Maximize timely fine revenue' (+50) but hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114), against which it performs worst in the sample.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The path realizes task 20 exactly (notification, penalty, then Send for Credit Collection with nothing else) and the model is tightly bounded (fitness 1.00, precision 1.00). Against the goal it serves, however, the measurements are the worst in the taxonomy: 'Average time to case closure' is 971.0 days, converting to -100, and 'Time to fine dispatch' is 132.0 days, converting to -15 against the statutory 90-day threshold. The 745-day gap between the penalty and the hand-over to collection is the dominant contributor. So the alternative is achieved as a procedural closure, but its declared contribution to 'Maximize timely fine revenue' is not supported by the one case observed; the reviewer may want to treat this as a late-enforcement case rather than a revenue-positive one. Single-case evidence.
