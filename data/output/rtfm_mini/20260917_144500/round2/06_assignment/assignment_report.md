# Step 6 — Narrative assignment report

Run: `20260917_144500` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `manual/claude-fable-5-1`

8 variants, 8 cases total.

## Resolved via timely payment (`timely_payment`)

The offender pays the fine directly after it is created, before any notification or penalty. The case closes at the first OR branch of 'Fine case is resolved' without entering enforcement. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=12. The sample realizes it in exactly one way (V0004: Create Fine, Payment after 1 day, no Send Fine or enforcement steps), so there is no evidence for subdivision and no co-occurrence with any other alternative that would license a merge.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `uncontested_enforcement_closure` at mean distance 3.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `uncontested_enforcement_closure` at mean distance 0.540

## Enforced case closed without appeal (delinquent payment or credit collection) (`uncontested_enforcement_closure`)

The fine goes through the enforcement path (Insert Fine Notification, Add Penalty) and is then closed without any appeal, either by the offender eventually paying, possibly in more than one installment, or by the organization handing the unpaid fine to coercive credit collection. Both routes help 'Maximize timely fine revenue' (+50); credit collection additionally hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25), as does the mandatory Add Penalty step on either route (-25). Judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Merged from the prior categories delinquent_payment (id=13) and coercive_credit_collection (id=20) at the reviewer's explicit request. The combination is structurally permitted: both are direct children of the same OR point, 'Enforced case is closed' (id=6), and neither is under an XOR, so the goal model does not declare them mutually exclusive. The sample contains no case realizing both routes together, so absent the reviewer's request the default 1:1 mapping would have been kept; the merge is recorded as a reviewer decision. Evidence: V0003, V0007, V0008 (payment after enforcement) and V0002 (credit collection).

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment; 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 4/8 variants (50.0%) · micro 4/8 cases (50.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.50, nearest other category `judicial_appeal_judge` at mean distance 1.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.433, nearest other category `timely_payment` at mean distance 0.540

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

After notification the offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received (and notified to the offender). One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=14. anchor_ids names only the alternative itself, not its AND-decomposed steps (15-18). V0006 realizes it (Insert Date Appeal to Prefecture, Send Appeal to Prefecture, Receive Result Appeal from Prefecture). It is XOR with the judicial appeal (id=19) and so must not be combined with it.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.360

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

After notification and penalty the offender takes the fine to a Judge. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=19. V0005 realizes it (Appeal to Judge as the closing activity, 21 days after the penalty). XOR with id=14, so kept separate from the Prefecture appeal.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `uncontested_enforcement_closure` at mean distance 1.50

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal_prefecture` at mean distance 0.360

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0002` / `V0007` (category `uncontested_enforcement_closure`): structural=2, profile=0.738
- `V0002` / `V0008` (category `uncontested_enforcement_closure`): structural=2, profile=0.741
- `V0007` / `V0008` (category `uncontested_enforcement_closure`): structural=2, profile=0.004
- `V0002` / `V0003` (category `uncontested_enforcement_closure`): structural=1, profile=0.361
- `V0003` / `V0007` (category `uncontested_enforcement_closure`): structural=1, profile=0.377
- `V0003` / `V0008` (category `uncontested_enforcement_closure`): structural=1, profile=0.380

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`uncontested_enforcement_closure`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.429
- `V0003` (`uncontested_enforcement_closure`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.401
- `V0005` (`judicial_appeal_judge`) / `V0007` (`uncontested_enforcement_closure`): structural=2, profile=0.691
- `V0005` (`judicial_appeal_judge`) / `V0008` (`uncontested_enforcement_closure`): structural=2, profile=0.687
- `V0002` (`uncontested_enforcement_closure`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.456
- `V0003` (`uncontested_enforcement_closure`) / `V0004` (`timely_payment`): structural=3, profile=0.306
- `V0003` (`uncontested_enforcement_closure`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.428
- `V0005` (`judicial_appeal_judge`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.360
- `V0006` (`administrative_appeal_prefecture`) / `V0008` (`uncontested_enforcement_closure`): structural=3, profile=0.714
- `V0002` (`uncontested_enforcement_closure`) / `V0004` (`timely_payment`): structural=4, profile=0.667

## Residual

1/8 variants (12.5%), 1/8 cases (12.5%) unassigned.

- `V0001`: The case only reaches Create Fine and Send Fine (the mandatory issuance goal) and then stops after 134 days with no payment, notification, penalty, appeal, or credit collection. It has not entered any branch of 'Fine case is resolved', so it realizes none of the four categories; it is a still-open case and belongs in the residual.