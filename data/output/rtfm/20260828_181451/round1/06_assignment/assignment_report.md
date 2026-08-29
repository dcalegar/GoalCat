# Step 6 — Narrative assignment report

Run: `20260828_181451` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`resolve_timely_payment`)

Fines resolved through prompt payment, maximizing timely fine revenue and helping minimize administrative and enforcement cost, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 12, supported by variants such as V0002.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 34/231 variants (14.7%) · micro 49658/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.91, nearest other category `resolve_delinquent_payment` at mean distance 5.02

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.216, nearest other category `resolve_delinquent_payment` at mean distance 0.185

## Resolve via delinquent payment (`resolve_delinquent_payment`)

Enforced cases resolved through delayed payment after notification and penalty additions, helping maximize timely fine revenue, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 13, supported by variants such as V0004 and V0005 where payment occurs after penalties.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 33/231 variants (14.3%) · micro 16875/150370 cases (11.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.02, nearest other category `resolve_administrative_appeal` at mean distance 4.78

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.142, nearest other category `resolve_timely_payment` at mean distance 0.185

## Resolve via administrative appeal to the Prefecture (`resolve_administrative_appeal`)

Contested cases resolved through the administrative appeal process involving the Prefecture, preserving due-process rights while potentially increasing costs and delaying revenue, judged against time to appeal filing, Prefecture.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 14, observed in variants handling prefecture appeals like V0008 and V0057.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 64/231 variants (27.7%) · micro 3602/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.98, nearest other category `resolve_coercive_credit_collection` at mean distance 4.70

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.327, nearest other category `resolve_judicial_appeal` at mean distance 0.404

## Resolve via judicial appeal to the Judge (`resolve_judicial_appeal`)

Contested cases resolved via judicial appeal to a judge, strongly making offender due-process rights while hurting administrative costs, judged against time to appeal filing, Judge.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 19, evidenced in variants containing judicial appeals such as V0103 and V0176.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 50/231 variants (21.6%) · micro 380/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.48, nearest other category `resolve_administrative_appeal` at mean distance 5.11

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.372, nearest other category `resolve_timely_payment` at mean distance 0.374

## Resolve via coercive credit collection (`resolve_coercive_credit_collection`)

Cases resolved via coercive credit collection actions after enforcement steps, helping revenue but hurting administrative costs, judged against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 20, observed in frequent credit collection outcomes such as V0001 and V0009.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 40/231 variants (17.3%) · micro 58996/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.05, nearest other category `resolve_administrative_appeal` at mean distance 4.70

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.144, nearest other category `resolve_judicial_appeal` at mean distance 0.493

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `resolve_judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.716
- `V0120` / `V0153` (category `resolve_judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `resolve_judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `resolve_judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `resolve_judicial_appeal`): structural=16, profile=0.705
- `V0029` / `V0153` (category `resolve_judicial_appeal`): structural=16, profile=0.730
- `V0047` / `V0153` (category `resolve_judicial_appeal`): structural=16, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`resolve_coercive_credit_collection`) / `V0004` (`resolve_delinquent_payment`): structural=1, profile=0.355
- `V0001` (`resolve_coercive_credit_collection`) / `V0029` (`resolve_judicial_appeal`): structural=1, profile=0.396
- `V0004` (`resolve_delinquent_payment`) / `V0009` (`resolve_coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`resolve_delinquent_payment`) / `V0014` (`resolve_judicial_appeal`): structural=1, profile=0.022
- `V0004` (`resolve_delinquent_payment`) / `V0029` (`resolve_judicial_appeal`): structural=1, profile=0.374
- `V0004` (`resolve_delinquent_payment`) / `V0031` (`resolve_judicial_appeal`): structural=1, profile=0.030
- `V0004` (`resolve_delinquent_payment`) / `V0116` (`resolve_timely_payment`): structural=1, profile=0.025
- `V0005` (`resolve_delinquent_payment`) / `V0009` (`resolve_coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`resolve_delinquent_payment`) / `V0031` (`resolve_judicial_appeal`): structural=1, profile=0.387
- `V0005` (`resolve_delinquent_payment`) / `V0037` (`resolve_judicial_appeal`): structural=1, profile=0.062

## Residual

10/231 variants (4.3%), 20859/150370 cases (13.9%) unassigned.

- `V0003`: The case ends with Send Fine and remains unresolved (no payment, appeal, or collection).
- `V0012`: The narrative concludes with Send Fine without reaching a resolution.
- `V0030`: The case ends with notifying the appeal result to the offender, without a final resolution such as payment or closure.
- `V0032`: The case ends at receiving the appeal result from the Prefecture without a final resolution.
- `V0034`: The narrative ends with notifying the result of an administrative appeal without a final resolution.
- `V0038`: The narrative ends with receiving the appeal result from the Prefecture, lacking a resolution.
- `V0046`: The narrative ends with notifying the result of an administrative appeal without a final resolution.
- `V0077`: Incomplete or unusual path ending in Send Fine without resolution.
- `V0093`: Anomalous sequence ending in Send Fine without closure.
- `V0193`: Incomplete lifecycle ending prematurely at Send Fine without resolution or payment.