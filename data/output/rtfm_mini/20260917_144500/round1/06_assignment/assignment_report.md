# Step 6 — Narrative assignment report

Run: `20260917_144500` | Log: `rtfm_mini` | Taxonomy mode: `intent_guided` | Assignment model: `manual/claude-fable-5-1`

8 variants, 8 cases total.

## Resolved via timely payment (`timely_payment`)

The offender pays the fine directly after it is created, before any notification or penalty. The case closes at the first OR branch of 'Fine case is resolved' without entering enforcement. This alternative fully advances 'Maximize timely fine revenue' (Make +100) and helps 'Minimize administrative & enforcement cost' (+50); its performance is judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=12. The sample realizes it in exactly one way (V0004: Create Fine, Payment after 1 day, no Send Fine or enforcement steps), so there is no evidence for subdivision and no co-occurrence with any other alternative that would license a merge.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 3.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `delinquent_payment` at mean distance 0.498

## Resolved via delinquent payment after enforcement (`delinquent_payment`)

The fine goes through the enforcement path (Insert Fine Notification, Add Penalty) and is then closed by the offender paying, possibly in more than one installment. This alternative helps 'Maximize timely fine revenue' (+50), while the mandatory Add Penalty step it contains slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=13 (child of the OR at id=6). Three sampled variants realize it (V0003, V0007, V0008). V0007 and V0008 differ from V0003 only by a repeated Payment activity (rework) and, in V0008, by the penalty being added between two payments; these are variations in how the payment is collected, not meaningfully different realizations of the alternative, so one category is kept rather than splitting on rework.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 3/8 variants (37.5%) · micro 3/8 cases (37.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.33, nearest other category `coercive_credit_collection` at mean distance 1.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.253, nearest other category `timely_payment` at mean distance 0.498

## Resolved via administrative appeal to the Prefecture (`administrative_appeal_prefecture`)

After notification the offender contests the fine administratively: the appeal date is inserted, the appeal is sent to the Prefecture, and the Prefecture's result is received (and notified to the offender). One of the two mutually exclusive branches of 'Contested appeal is resolved'. It helps 'Preserve offender's due-process rights' (+50) but slightly harms both 'Minimize administrative & enforcement cost' (-25) and 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Prefecture' (id 113) and 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=14. anchor_ids names only the alternative itself, not its AND-decomposed steps (15-18). V0006 realizes it (Insert Date Appeal to Prefecture, Send Appeal to Prefecture, Receive Result Appeal from Prefecture). It is XOR with the judicial appeal (id=19) and so must not be combined with it.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 3.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.360

## Resolved via judicial appeal to the Judge (`judicial_appeal_judge`)

After notification and penalty the offender takes the fine to a Judge. The other, mutually exclusive branch of 'Contested appeal is resolved'. It fully advances 'Preserve offender's due-process rights' (Make +100) while hurting 'Minimize administrative & enforcement cost' (-50) and slightly harming 'Maximize timely fine revenue' (-25). Judged against 'Time to appeal filing, Judge' (id 175) and 'Average time to case closure' (id 114).

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=19. V0005 realizes it (Appeal to Judge as the closing activity, 21 days after the penalty). XOR with id=14, so kept separate from the Prefecture appeal.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `coercive_credit_collection` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `administrative_appeal_prefecture` at mean distance 0.360

## Resolved via coercive credit collection (`coercive_credit_collection`)

The fine is notified and penalised but never paid or appealed, and the organization hands it to credit collection to enforce it. This alternative helps 'Maximize timely fine revenue' (+50) but hurts 'Minimize administrative & enforcement cost' (-50) and slightly harms 'Preserve offender's due-process rights' (-25). Judged against 'Average time to case closure' (id 114), against which it performs worst in the sample.

**Taxonomy-derivation rationale (Step 5):** Default 1:1 mapping to declared alternative id=20. V0002 realizes it (Send for Credit Collection 745 days after the penalty, 971-day median duration). A single realization in the sample gives no basis for subdivision.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 1/8 variants (12.5%) · micro 1/8 cases (12.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 1.00

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance n/a (singleton category), nearest other category `judicial_appeal_judge` at mean distance 0.429

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0007` / `V0008` (category `delinquent_payment`): structural=2, profile=0.004
- `V0003` / `V0007` (category `delinquent_payment`): structural=1, profile=0.377
- `V0003` / `V0008` (category `delinquent_payment`): structural=1, profile=0.380

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0002` (`coercive_credit_collection`) / `V0003` (`delinquent_payment`): structural=1, profile=0.361
- `V0002` (`coercive_credit_collection`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.429
- `V0003` (`delinquent_payment`) / `V0005` (`judicial_appeal_judge`): structural=1, profile=0.401
- `V0002` (`coercive_credit_collection`) / `V0007` (`delinquent_payment`): structural=2, profile=0.738
- `V0002` (`coercive_credit_collection`) / `V0008` (`delinquent_payment`): structural=2, profile=0.741
- `V0005` (`judicial_appeal_judge`) / `V0007` (`delinquent_payment`): structural=2, profile=0.691
- `V0005` (`judicial_appeal_judge`) / `V0008` (`delinquent_payment`): structural=2, profile=0.687
- `V0002` (`coercive_credit_collection`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.456
- `V0003` (`delinquent_payment`) / `V0004` (`timely_payment`): structural=3, profile=0.306
- `V0003` (`delinquent_payment`) / `V0006` (`administrative_appeal_prefecture`): structural=3, profile=0.428

## Residual

1/8 variants (12.5%), 1/8 cases (12.5%) unassigned.

- `V0001`: The case only reaches Create Fine and Send Fine (the mandatory issuance goal) and then stops after 134 days with no payment, notification, penalty, appeal, or credit collection. It has not entered any branch of 'Fine case is resolved', so it realizes none of the five resolution alternatives; it is a still-open case and belongs in the residual.