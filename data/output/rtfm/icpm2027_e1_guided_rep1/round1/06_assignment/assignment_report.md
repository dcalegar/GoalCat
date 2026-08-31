# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved through prompt payment by the offender, advancing the softgoal 'Maximize timely fine revenue' and helping 'Minimize administrative & enforcement cost', judged against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=12. Supported by frequent narrative variants such as V0002 and V0007 where payment occurs shortly after fine creation.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 6/231 variants (2.6%) · micro 49609/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.73, nearest other category `administrative_appeal` at mean distance 5.24

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.264, nearest other category `delinquent_payment` at mean distance 0.257

## Resolve via delinquent payment (`delinquent_payment`)

Cases where payment occurs after penalties have been added and notifications sent, helping 'Maximize timely fine revenue', judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=13. Supported by variants like V0004, V0005, and V0006 where payments happen subsequent to penalty additions and reminders.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 42/231 variants (18.2%) · micro 16917/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.73, nearest other category `administrative_appeal` at mean distance 4.92

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.168, nearest other category `timely_payment` at mean distance 0.257

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving formal administrative appeals directed to the Prefecture, preserving 'Preserve offender's due-process rights' while impacting 'Minimize administrative & enforcement cost' and 'Maximize timely fine revenue', measured using 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=14. Supported by variants like V0008, V0057, and V00135 containing steps such as 'Insert Date Appeal to Prefecture' and 'Send Appeal to Prefecture'.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 72/231 variants (31.2%) · micro 3682/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.82, nearest other category `coercive_credit_collection` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.355, nearest other category `delinquent_payment` at mean distance 0.393

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving judicial appeals escalated to a Judge, maximizing 'Preserve offender's due-process rights' while hurting 'Minimize administrative & enforcement cost' and 'Maximize timely fine revenue', judged against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=19. Supported by variants like V0103, V0176, and V0140 containing the 'Appeal to Judge' activity.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 64/231 variants (27.7%) · micro 398/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.69, nearest other category `administrative_appeal` at mean distance 5.12

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.400, nearest other category `delinquent_payment` at mean distance 0.386

## Resolve via coercive credit collection (`coercive_credit_collection`)

Cases routed to coercive enforcement and credit collection agencies, helping 'Maximize timely fine revenue' but hurting 'Minimize administrative & enforcement cost', evaluated against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to the declared alternative id=20. Supported by variants like V0001, V0009, and V00134 ending with 'Send for Credit Collection'.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 43/231 variants (18.6%) · micro 59012/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `administrative_appeal` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.185, nearest other category `judicial_appeal` at mean distance 0.498

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

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387
- `V0005` (`delinquent_payment`) / `V0037` (`judicial_appeal`): structural=1, profile=0.062
- `V0005` (`delinquent_payment`) / `V0071` (`coercive_credit_collection`): structural=1, profile=0.379

## Residual

4/231 variants (1.7%), 20752/150370 cases (13.8%) unassigned.

- `V0003`: The case ends with Send Fine and has no final payment, appeal, or credit collection outcome.
- `V0012`: An unusual ordering ending in Send Fine after a payment, fitting none of the standard resolution paths.
- `V0077`: The variant ends prematurely at Send Fine with out-of-order appeal activities and does not cleanly realize any resolution category.
- `V0193`: Case stops at Send Fine without clear resolution or payment/appeal completion.