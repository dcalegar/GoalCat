# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Cases resolved directly through payment without enforcement steps, advancing 'Maximize timely fine revenue' and 'Minimize administrative & enforcement cost', judged against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 12 as supported by frequent variants such as V0002 and V0007.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 9/231 variants (3.9%) · micro 49612/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.36, nearest other category `delinquent_payment` at mean distance 5.39

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.330, nearest other category `delinquent_payment` at mean distance 0.271

## Resolve via delinquent payment (`delinquent_payment`)

Cases resolved via payment after enforcement actions (penalties or notifications) have been applied, supporting 'Maximize timely fine revenue', judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 13 as evidenced by variants like V0004, V0005, and V0006 where payment occurs after penalties/notifications.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 47/231 variants (20.3%) · micro 16977/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.54, nearest other category `administrative_appeal` at mean distance 4.82

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.185, nearest other category `timely_payment` at mean distance 0.271

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Cases involving administrative appeals submitted to the Prefecture, preserving offender's due-process rights while potentially impacting enforcement costs and revenue, judged against 'Time to appeal filing, Prefecture (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 14, evidenced by workflow sequences containing date entry, sending, and results from the Prefecture (e.g., V0008, V0057).

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 75/231 variants (32.5%) · micro 3842/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.07, nearest other category `coercive_credit_collection` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.386, nearest other category `judicial_appeal` at mean distance 0.419

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Cases involving judicial appeals escalated to a Judge, maximizing due process rights while hurting cost and revenue metrics, judged against 'Time to appeal filing, Judge (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 19, supported by variants explicitly showing 'Appeal to Judge' activities (e.g., V0103, V0176).

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 59/231 variants (25.5%) · micro 494/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.74, nearest other category `administrative_appeal` at mean distance 5.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.392, nearest other category `delinquent_payment` at mean distance 0.364

## Resolve via coercive credit collection (`coercive_credit_collection`)

Unresolved cases pushed to coercive credit collection, helping fine revenue but hurting enforcement costs, judged against 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Mapped 1:1 to declared alternative 20, evidenced by variants terminating with credit collection activities (e.g., V0001, V0009).

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 34/231 variants (14.7%) · micro 58681/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.20, nearest other category `administrative_appeal` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.188, nearest other category `administrative_appeal` at mean distance 0.479

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0097` / `V0153` (category `judicial_appeal`): structural=17, profile=0.762
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0134` / `V0153` (category `judicial_appeal`): structural=17, profile=0.706
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706
- `V0027` / `V0153` (category `judicial_appeal`): structural=16, profile=0.705

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`coercive_credit_collection`) / `V0004` (`delinquent_payment`): structural=1, profile=0.355
- `V0001` (`coercive_credit_collection`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`coercive_credit_collection`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0004` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.354
- `V0004` (`delinquent_payment`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`delinquent_payment`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`delinquent_payment`) / `V0116` (`administrative_appeal`): structural=1, profile=0.025
- `V0005` (`delinquent_payment`) / `V0009` (`coercive_credit_collection`): structural=1, profile=0.711
- `V0005` (`delinquent_payment`) / `V0031` (`judicial_appeal`): structural=1, profile=0.387

## Residual

7/231 variants (3.0%), 20764/150370 cases (13.8%) unassigned.

- `V0003`: The case ends with Send Fine and is not resolved by payment, appeal, or credit collection, so it falls into the residual.
- `V0012`: The case involves a payment followed by sending the fine, which does not fit standard lifecycle categories well, placing it in the residual.
- `V0077`: The narrative contains administrative appeal activities but terminates prematurely at Send Fine without resolution via payment, appeal outcome, or collection.
- `V0083`: The process includes an intermediate payment followed by administrative appeal steps, but the outcome is just sending an appeal rather than final resolution.
- `V0086`: The sequence contains mixed steps including payment and an administrative appeal, but terminates with sending an appeal rather than a clear final outcome.
- `V0090`: The process includes administrative appeal activities and a direct payment without enforcement penalties, not cleanly fitting timely or delinquent payment categories.
- `V0093`: The narrative features a judicial appeal followed by sending the fine, but lacks a definitive final resolution like payment or collection.