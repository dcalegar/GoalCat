# Step 6 — Narrative assignment report

Run: `20260917_152158` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `manual/claude-fable-5-1`

231 variants, 150370 cases total.

## Resolved via timely payment (`timely_payment`)

The offender pays the fine before enforcement begins, that is before any Insert Fine Notification or Add Penalty, typically within days of creation and sometimes before or shortly after the fine is dispatched. The case closes at the first OR branch of 'Fine case is resolved' without entering the enforceable path. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=12. The sample realizes it as Create Fine then Payment (V0002, 30.8% of all cases, 5-day median), as Payment after Send Fine but before notification (V0007), and as Payment recorded before Send Fine (V0012, V0193) or in two installments (V0048). These differ only in whether and when the dispatch event is logged and in payment rework, not in how the goal is achieved, so one category is kept rather than splitting.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49969/150370 cases (33.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.43, nearest other category `coercive_credit_collection` at mean distance 4.82

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.408, nearest other category `delinquent_payment` at mean distance 0.332

## Resolved via delinquent payment after enforcement (`delinquent_payment`)

The fine enters enforcement (Insert Fine Notification, Add Penalty) and is then closed by the offender paying, often late and often in several installments, without any appeal. This alternative helps 'Maximize timely fine revenue' (+50), while the mandatory Add Penalty step slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=13 (child of the OR at id=6). Realized by V0004 (6.3% of cases, single payment 231 days after the penalty), V0005 and V0006 (two payments, with the penalty either before or between them), and by long installment chains such as V0141. Installment count and penalty/payment ordering are rework and ordering variation within the same alternative, not evidence of distinct realizations, so no subdivision.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 21/231 variants (9.1%) · micro 16851/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.90, nearest other category `coercive_credit_collection` at mean distance 4.41

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.066, nearest other category `timely_payment` at mean distance 0.332

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

The offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received and notified to the offender. One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=14; anchor_ids names the alternative only, not its AND-decomposed steps (15-18). V0008 (1.7% of cases) ends at Send Appeal to Prefecture, V0137 runs through to Notify Result Appeal to Offender, and V0136 receives and notifies a result without a logged filing. The sample also shows appeals that are later followed by payment or credit collection (V0132, V0138); those are mixed cases for Step 6 to weigh, not a reason to subdivide. XOR with id=19, so never combined with the judicial appeal.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 129/231 variants (55.8%) · micro 4042/150370 cases (2.7%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.33, nearest other category `coercive_credit_collection` at mean distance 5.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.381, nearest other category `judicial_appeal_judge` at mean distance 0.414

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

The offender takes the fine to a Judge, logged as Appeal to Judge, usually shortly after notification and before or around the penalty. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=19. The sample contains no variant that ends at Appeal to Judge alone; Appeal to Judge appears in V0144, V0176 and V0103 alongside a Prefecture filing, and in V0147, V0151 and V0153 followed by long payment installment chains. These show the alternative is exercised in the log, and the mixing with other closures is for Step 6 to resolve per narrative. XOR with id=14, so kept separate from the Prefecture appeal.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 60/231 variants (26.0%) · micro 525/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.66, nearest other category `administrative_appeal_prefecture` at mean distance 5.35

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.405, nearest other category `administrative_appeal_prefecture` at mean distance 0.414

## Resolved via coercive credit collection (`coercive_credit_collection`)

The fine is notified and penalised and, with no payment in full and no successful appeal, the organization hands it to credit collection to enforce it, typically more than a year after the penalty. This alternative helps 'Maximize timely fine revenue' (+50) but hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=20. V0001 is the single most frequent variant in the log (37.6% of cases, 638-day median) and realizes it exactly; V0009 and V0010 reach credit collection after a partial payment. A partial payment before hand-over does not change the closure, so no subdivision.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 13/231 variants (5.6%) · micro 58598/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.42, nearest other category `delinquent_payment` at mean distance 4.41

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.182, nearest other category `judicial_appeal_judge` at mean distance 0.493

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal_judge`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.698
- `V0120` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal_judge`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal_judge`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal_judge`): structural=17, profile=0.716

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal_judge`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.396
- `V0001` (`coercive_credit_collection`) / `V0040` (`judicial_appeal_judge`): structural=1, profile=0.027
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal_judge`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal_judge`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal_judge`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0054` (`administrative_appeal_prefecture`): structural=1, profile=0.011
- `V0004` (`delinquent_payment`) / `V0085` (`administrative_appeal_prefecture`): structural=1, profile=0.006

## Residual

1/231 variants (0.4%), 20385/150370 cases (13.6%) unassigned.

- `V0003`: Create Fine and Send Fine only, then nothing for 101 days: the mandatory issuance goal is met but no resolution alternative (payment, appeal, credit collection) has been entered. Still-open case; residual.