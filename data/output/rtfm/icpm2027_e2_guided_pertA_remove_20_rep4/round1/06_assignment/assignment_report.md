# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertA_remove_20_rep4` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Resolution of the fine case through prompt payment by the offender. This pathway advances the softgoal 'Maximize timely fine revenue' (via Make contribution) and helps 'Minimize administrative & enforcement cost' (via Help contribution). Performance is judged against the indicator 'Time to fine dispatch' and 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12. Supported by frequent narrative samples such as V0002 and V0007 where payment occurs directly.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49696/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.95, nearest other category `delinquent_payment` at mean distance 5.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.321, nearest other category `delinquent_payment` at mean distance 0.355

## Resolve via delinquent payment (`delinquent_payment`)

Resolution of the fine case through payment after notifications and penalties have been applied. This pathway helps 'Maximize timely fine revenue'. Performance is judged against 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13. Supported by narrative samples such as V0004, V0005, and V0006 where payments follow penalty and notification tasks.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 40/231 variants (17.3%) · micro 16846/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.21, nearest other category `timely_payment` at mean distance 5.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.313, nearest other category `timely_payment` at mean distance 0.355

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Resolution of the fine case through an administrative appeal lodged with the Prefecture. This pathway helps 'Preserve offender's due-process rights' while incurring some negative effects on administrative cost and timely revenue. Performance is evaluated against 'Time to appeal filing, Prefecture' and 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14. Supported by variants like V0008, V0057, and V0135 containing administrative appeal steps.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 105/231 variants (45.5%) · micro 3976/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.31, nearest other category `delinquent_payment` at mean distance 5.14

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.390, nearest other category `judicial_appeal` at mean distance 0.411

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Resolution of the fine case through a judicial appeal to a judge. This pathway strongly advances 'Preserve offender's due-process rights' (Make contribution) but hurts 'Minimize administrative & enforcement cost' and 'Maximize timely fine revenue'. Judged against 'Time to appeal filing, Judge' and 'Average time to case closure'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19. Supported by variants such as V0103, V0176, and V0140 demonstrating judicial appeals.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 72/231 variants (31.2%) · micro 537/150370 cases (0.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.60, nearest other category `administrative_appeal` at mean distance 5.22

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.416, nearest other category `administrative_appeal` at mean distance 0.411

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0093` / `V0153` (category `judicial_appeal`): structural=18, profile=0.750
- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0018` (`timely_payment`): structural=1, profile=0.367
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.382
- `V0005` (`delinquent_payment`) / `V0130` (`administrative_appeal`): structural=1, profile=0.019
- `V0005` (`delinquent_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060

## Residual

7/231 variants (3.0%), 79315/150370 cases (52.7%) unassigned.

- `V0001`: The case ends with Send for Credit Collection after notifications and penalties, representing uncollected debt rather than a resolution through payment or appeal.
- `V0003`: The case ends with Send Fine and remains open or unresolved without payment or appeal recorded.
- `V0009`: Although a payment is made, the case ultimately proceeds to credit collection, meaning it was not fully resolved by payment alone.
- `V0010`: The case includes an intermediate payment followed by penalties and ends in credit collection.
- `V0012`: The case involves a payment before sending the fine, but ends with Send Fine without a final resolution status.
- `V0026`: The case ends with Send for Credit Collection after a penalty, which does not fit timely payment, delinquent payment, administrative appeal, or judicial appeal.
- `V0077`: The narrative contains appeal scheduling steps followed by a 'Send Fine' activity without reaching a clear resolution or final payment/appeal outcome.