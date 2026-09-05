# Step 6 — Narrative assignment report

Run: `icpm2027_e1_guided_rep2` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Represents resolution of the fine case through prompt payment. Advances softgoals such as 'Maximize timely fine revenue' and helps 'Minimize administrative & enforcement cost', evaluated against indicator 'Time to fine dispatch (days)' and 'Average time to case closure (days)'.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 12 as observed in frequent variants such as V0002 and V0007.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 7/231 variants (3.0%) · micro 49608/150370 cases (33.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.05, nearest other category `delinquent_payment` at mean distance 5.21

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.221, nearest other category `delinquent_payment` at mean distance 0.229

## Resolve via delinquent payment (`delinquent_payment`)

Represents resolution of the fine case through delayed or subsequent payment after penalties or enforcement steps. Helps maximize timely fine revenue.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 13 as observed in variants like V0004, V0005, and V0006 where payments happen after notifications and penalties.

**Goal-model linkage:** 13 (Task): Resolve via delinquent payment

**Coverage:** macro 52/231 variants (22.5%) · micro 16950/150370 cases (11.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.28, nearest other category `administrative_appeal` at mean distance 4.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.184, nearest other category `timely_payment` at mean distance 0.229

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Represents resolution through administrative appeal processes addressed to the Prefecture. Preserves offender due-process rights while potentially impacting enforcement costs and revenue.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 14, evidenced by traces containing date inserts and appeals directed to the Prefecture such as V0008.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 71/231 variants (30.7%) · micro 3666/150370 cases (2.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.26, nearest other category `delinquent_payment` at mean distance 4.67

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.361, nearest other category `judicial_appeal` at mean distance 0.407

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Represents resolution through judicial appeals directed to a judge, strongly advancing offender due-process rights while increasing costs.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 19, supported by variants demonstrating judicial appeals like V0140 and V0176.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 56/231 variants (24.2%) · micro 387/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.88, nearest other category `administrative_appeal` at mean distance 5.39

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.397, nearest other category `delinquent_payment` at mean distance 0.383

## Resolve via coercive credit collection (`coercive_credit_collection`)

Represents resolution through coercive credit collection steps when other paths fail. Helps fine revenue but incurs enforcement costs.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative 20, widely observed in frequent variants ending in credit collection such as V0001 and V0009.

**Goal-model linkage:** 20 (Task): Resolve via coercive credit collection

**Coverage:** macro 42/231 variants (18.2%) · micro 59011/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.09, nearest other category `administrative_appeal` at mean distance 4.87

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.187, nearest other category `judicial_appeal` at mean distance 0.492

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
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706

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

3/231 variants (1.3%), 20748/150370 cases (13.8%) unassigned.

- `V0003`: The case only reaches 'Send Fine' without payment, appeal, or collection, leaving it unresolved within the taxonomy.
- `V0012`: The case features early payment followed by sending the fine, which does not fit standard lifecycle paths.
- `V0193`: The case shows early payment before fine dispatch, which does not fit any standard resolution category cleanly.