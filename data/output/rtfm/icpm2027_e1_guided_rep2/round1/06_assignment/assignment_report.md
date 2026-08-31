# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through early or timely payment before coercive enforcement or appeals. Advances 'Maximize timely fine revenue' (Make +100) and 'Minimize administrative & enforcement cost' (Help +50). Evaluated against Indicator id=114 (Average time to case closure) and Indicator id=112 (Time to fine dispatch).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12. Realized in the narrative sample by variants such as V0002, V0003, V0007, where payment occurs directly after fine creation or sending without entering penalty or appeal paths.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49617/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 2.57, nearest other category `delinquent_payment` at mean distance 5.15

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.226, nearest other category `delinquent_payment` at mean distance 0.211

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment occurring after penalties or notifications have been applied, but prior to full coercive credit collection. Helps 'Maximize timely fine revenue' (Help +50). Evaluated against Indicator id=114 (Average time to case closure).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13. Realized in the narrative sample by variants such as V0004, V0005, V0006, and V0009, where payment happens after 'Insert Fine Notification' and 'Add penalty'.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 35/231 variants (15.2%) · micro 16889/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.56, nearest other category `administrative_appeal` at mean distance 5.04

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.160, nearest other category `timely_payment` at mean distance 0.211

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution through an administrative appeal process directed to the Prefecture. Preserves offender's due-process rights (Help +50) while incurring administrative costs and delaying revenue (SomeNegative -25). Evaluated against Indicator id=113 (Time to appeal filing, Prefecture) and Indicator id=114.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14. Realized in the narrative sample by variants like V0008, V0057, and V0137, featuring activities such as 'Insert Date Appeal to Prefecture' and 'Send Appeal to Prefecture'.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 71/231 variants (30.7%) · micro 3596/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.98, nearest other category `coercive_credit_collection` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.349, nearest other category `delinquent_payment` at mean distance 0.373

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution through a judicial appeal brought before a Judge. Fully supports offender's due-process rights (Make +100) but hurts administrative and enforcement costs (Hurt -50) and fine revenue (SomeNegative -25). Evaluated against Indicator id=175 (Time to appeal filing, Judge) and Indicator id=114.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19. Realized in the narrative sample by variants such as V0103, V0140, V0176, and V0224, which explicitly include the 'Appeal to Judge' activity.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 67/231 variants (29.0%) · micro 404/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.60, nearest other category `administrative_appeal` at mean distance 5.13

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.394, nearest other category `administrative_appeal` at mean distance 0.387

## Resolve via coercive credit collection (`coercive_credit_collection`)

Resolution of the case through coercive credit collection measures after standard resolution pathways have failed or expired. Helps timely revenue (Help +50) but hurts administrative costs (Hurt -50) and due-process rights (SomeNegative -25). Evaluated against Indicator id=114 (Average time to case closure).

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20. Realized in the narrative sample by variants such as V0001, V0009, and V0134, where the final outcome activity is 'Send for Credit Collection'.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 43/231 variants (18.6%) · micro 59012/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.75

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.185, nearest other category `judicial_appeal` at mean distance 0.496

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062

## Residual

8/231 variants (3.5%), 20852/150370 cases (13.9%) unassigned.

- `V0003`: The case ends at Send Fine without payment, appeal, or credit collection, leaving the resolution incomplete.
- `V0012`: Payment happens before sending the fine, making it an unusual sequence that does not cleanly fit standard paths.
- `V0030`: The case stops at notifying the result of the appeal to the offender without resolution or payment.
- `V0032`: The case terminates upon receiving the result of the administrative appeal without final resolution like payment or collection.
- `V0034`: The case ends at notifying the appeal result to the offender without final resolution.
- `V0038`: The case stops at receiving the result of the appeal to the Prefecture without a final payment or collection.
- `V0046`: The case terminates at notifying the result of the administrative appeal to the offender without a closing payment or collection.
- `V0193`: The variant ends prematurely at Send Fine without resolution/payment or appeal.