# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep4` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Represents resolution of the fine case through early or timely payment without requiring enforcement actions. It directly advances the softgoal 'Maximize timely fine revenue' and helps 'Minimize administrative & enforcement cost', evaluated against indicator 'Time to fine dispatch (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12. Supported by frequent variants like V0002 where payment occurs shortly after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 8/231 variants (3.5%) · micro 49588/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.71, nearest other category `administrative_appeal` at mean distance 5.01

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.263, nearest other category `delinquent_payment` at mean distance 0.232

## Resolve via delinquent payment (`delinquent_payment`)

Represents resolution of the fine case through payment occurring after penalties or enforcement steps have been initiated. It helps 'Maximize timely fine revenue' and is judged against the indicator 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13. Supported by variants where payment is observed subsequent to penalty additions or notifications, such as V0004, V0005, and V0006.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 52/231 variants (22.5%) · micro 17037/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.59, nearest other category `administrative_appeal` at mean distance 4.78

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.183, nearest other category `timely_payment` at mean distance 0.232

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Represents cases where the offender pursues an administrative appeal to the Prefecture. It helps preserve due process rights while negatively impacting collection costs and timeliness, measured via 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14. Supported by variants involving insertion of appeal dates and sending appeals to the Prefecture, such as V0008 and V0057.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 70/231 variants (30.3%) · micro 3659/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.82, nearest other category `coercive_credit_collection` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.359, nearest other category `judicial_appeal` at mean distance 0.404

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Represents cases where the offender contests the fine via a judicial appeal to the Judge. It strongly advances offender due process rights while hurting administrative cost and revenue metrics, judged by 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19. Supported by variants containing judicial appeal activities, such as V0103, V0176, and V0140.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 52/231 variants (22.5%) · micro 318/150370 cases (0.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.93, nearest other category `administrative_appeal` at mean distance 5.33

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.392, nearest other category `delinquent_payment` at mean distance 0.371

## Resolve via coercive credit collection (`coercive_credit_collection`)

Represents resolution through coercive credit collection procedures for unresolved or defaulted fines. It helps revenue generation but hurts enforcement cost and due process, measured by 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20. Supported by variants ending with credit collection dispatch, such as V0001 and V0134.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 44/231 variants (19.0%) · micro 59013/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.182, nearest other category `administrative_appeal` at mean distance 0.497

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705
- `V0029` / `V0153` (category `judicial_appeal`): structural=16, profile=0.730
- `V0047` / `V0153` (category `judicial_appeal`): structural=16, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379
- `V0005` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.382
- `V0005` (`delinquent_payment`) / `V0184` (`judicial_appeal`): structural=1, profile=0.060

## Residual

5/231 variants (2.2%), 20755/150370 cases (13.8%) unassigned.

- `V0003`: The case simply sends the fine and remains unresolved without payment, appeal, or credit collection within this trace.
- `V0012`: The sequence shows payment occurring before sending the fine, which is an anomalous order that does not fit standard taxonomy definitions.
- `V0077`: The sequence is incomplete or disordered (ending with Send Fine after appeals), fitting none of the resolution categories.
- `V0093`: The sequence is abnormal (starting with a judicial appeal before sending the fine), fitting none of the categories.
- `V0193`: Case terminates prematurely at Send Fine without resolution or payment.