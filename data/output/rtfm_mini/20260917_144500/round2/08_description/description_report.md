# Step 8 — High-level description generation report

Run: `20260917_144500` | Log: `rtfm_mini` | Description model: `manual/claude-fable-5-1`

Full conformance metrics and model files are in [`discovery_report.md`](../07_discovery/discovery_report.md) (Step 7) -- not duplicated here.

## Resolved via timely payment (`timely_payment`)

**Declared (Step 5):** The offender pays the fine directly after it is created, before any notification or penalty. The case closes at the first OR branch of 'Fine case is resolved' without entering enforcement. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** Consistent with achieving task 12. The single case pays one day after fine creation and never enters enforcement, and the measured 'Average time to case closure' of 1.0 days converts to +100 satisfaction. The model is tightly bounded (fitness 1.00, precision 1.00), so nothing beyond the declared path is admitted. Caveat for the reviewer: single-case evidence confirms the alternative occurs, not how it behaves in general.

## Enforced case closed without appeal (delinquent payment or credit collection) (`uncontested_enforcement_closure`)

**Declared (Step 5):** The fine goes through the enforcement path (Insert Fine Notification, Add Penalty) and is then closed without any appeal, either by the offender eventually paying, possibly in more than one installment, or by the organization handing the unpaid fine to coercive credit collection. Both routes help 'Maximize timely fine revenue' (+50); credit collection additionally hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25), as does the mandatory Add Penalty step on either route (-25). Judged against 'Average time to case closure' (id 114).

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment; 20 (Task): Resolve via coercive credit collection

**Coverage:** 4 variants, 4 cases.

**Discovered pattern:** Moderate concentration: the most frequent of 4 distinct variants accounts for 25% of cases. Waiting times between activities show moderate variability across cases.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 0.91).

**Goal alignment:** The discovered behavior realizes the two anchored tasks, 13 and 20: all four cases are notified and penalised and then closed without appeal, three by payment and one by hand-over to credit collection, and the model remains reasonably tight (fitness 1.00, precision 0.91; the extra slack comes from now admitting two distinct closing activities plus the repeated Payment). Against the goal these tasks serve the measurements are poor: 'Average time to case closure' is 488.7 days, converting to -100, and 'Time to fine dispatch' is 127.7 days, converting to -13 against the statutory 90-day threshold. The closure figure is dominated by the single credit-collection case (971 days) sitting alongside payments closing in roughly 200 to 550 days; merging the two routes therefore hides a large performance difference between them, and the aggregate -100 should not be read as describing the delinquent-payment cases on their own. The reviewer may want to keep the merge only if the intended question is 'was the enforced fine closed without contest', not 'how well does each closure route perform'. The dispatch delay precedes the offender's delinquency and is administrative.

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

**Declared (Step 5):** After notification the offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received (and notified to the offender). One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** Consistent with achieving task 14. The single case files its Prefecture appeal 5.0 days after notification (+100 against the statutory 60-day limit), the fine was dispatched in 0.0 days (+100), and the case closes in 78.0 days (+100). The model is tightly bounded (fitness 1.00, precision 1.00). Two points for the reviewer: the case ends at 'Receive Result Appeal from Prefecture' without the declared 'Notify Result Appeal to Offender' step, so the AND-decomposed alternative is realized only partially in the log; and the penalty is added while the appeal is pending, which bears on the due-process softgoal this alternative is meant to advance. Single-case evidence.

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

**Declared (Step 5):** After notification and penalty the offender takes the fine to a Judge. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** 1 variants, 1 cases.

**Discovered pattern:** This category has a single variant, so all 1 cases follow the exact same path. Only one case in this category -- no cross-case waiting-time variability to characterize.

**Model looseness:** Tightly bounded: the model fits the observed cases well (log fitness 1.00) and permits little behavior beyond what was actually seen (precision 1.00).

**Goal alignment:** The path matches task 19 (notification, penalty, then Appeal to Judge) and the model is tight (fitness 1.00, precision 1.00), but the measured evidence undercuts the claim that the alternative is achieved lawfully. 'Time to appeal filing, Judge' is 81.0 days against a statutory 30-day limit, converting to -100, so the appeal was filed well out of time and the due-process goal this alternative is supposed to fully advance is not met on the one case observed. 'Average time to case closure' is not applicable because no closing activity follows the appeal, meaning the case is still open at log end. Both points deserve reviewer attention; single-case evidence.
