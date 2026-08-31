# Step 6 — Narrative assignment report

Run: `icpm2027_e2_guided_pertB_merge_13_20_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Resolve via timely payment (`timely_payment`)

Fine is settled promptly through payment, maximizing timely fine revenue and helping minimize administrative and enforcement costs, measured against average time to case closure and time to fine dispatch.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task id 12 as observed in frequent variants such as V0002 and V0004.

**Goal-model linkage:** 12 (Task): Resolve via timely payment

**Coverage:** macro 59/231 variants (25.5%) · micro 53524/150370 cases (35.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.30, nearest other category `administrative_appeal` at mean distance 5.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.213, nearest other category `judicial_appeal` at mean distance 0.421

## Fine becomes enforceable and is resolved (`enforceable_resolution`)

Fine proceeds through notification and penalty addition, balancing revenue maximization against due-process preservation, measured against average time to case closure.

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative goal id 5 representing cases requiring notifications and penalties before ultimate resolution or credit collection, as seen in variants like V0001.

**Goal-model linkage:** 5 (Goal): Fine becomes enforceable and is resolved

**Coverage:** macro 27/231 variants (11.7%) · micro 72009/150370 cases (47.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.51, nearest other category `administrative_appeal` at mean distance 4.89

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.352, nearest other category `judicial_appeal` at mean distance 0.458

## Resolve via administrative appeal to the Prefecture (`administrative_appeal`)

Fine resolution is pursued via an administrative appeal submitted to the Prefecture, preserving offender due-process rights while potentially increasing administrative costs and impacting revenue timing, measured against time to appeal filing (Prefecture).

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task id 14, instantiated in variants where administrative appeal procedures are carried out.

**Goal-model linkage:** 14 (Task): Resolve via administrative appeal to the Prefecture

**Coverage:** macro 75/231 variants (32.5%) · micro 3919/150370 cases (2.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.95, nearest other category `enforceable_resolution` at mean distance 4.89

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.374, nearest other category `judicial_appeal` at mean distance 0.416

## Resolve via judicial appeal to the Judge (`judicial_appeal`)

Fine resolution is pursued via judicial appeal to a judge, strongly making for the preservation of offender's due-process rights while hurting administrative cost minimization and fine revenue, measured against time to appeal filing (Judge).

**Taxonomy-derivation rationale (Step 5):** Maps 1:1 to declared alternative task id 19, observed in variants involving direct judicial challenges.

**Goal-model linkage:** 19 (Task): Resolve via judicial appeal to the Judge

**Coverage:** macro 61/231 variants (26.4%) · micro 520/150370 cases (0.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.29, nearest other category `administrative_appeal` at mean distance 4.96

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.407, nearest other category `administrative_appeal` at mean distance 0.416

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0096` / `V0153` (category `judicial_appeal`): structural=18, profile=0.770
- `V0035` / `V0153` (category `judicial_appeal`): structural=17, profile=0.710
- `V0063` / `V0153` (category `judicial_appeal`): structural=17, profile=0.746
- `V0069` / `V0153` (category `judicial_appeal`): structural=17, profile=0.716
- `V0082` / `V0153` (category `judicial_appeal`): structural=17, profile=0.698
- `V0120` / `V0153` (category `judicial_appeal`): structural=17, profile=0.729
- `V0153` / `V0154` (category `judicial_appeal`): structural=17, profile=0.358
- `V0153` / `V0167` (category `judicial_appeal`): structural=17, profile=0.716
- `V0153` / `V0206` (category `judicial_appeal`): structural=17, profile=0.718
- `V0153` / `V0212` (category `judicial_appeal`): structural=17, profile=0.706

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`enforceable_resolution`) / `V0017` (`judicial_appeal`): structural=1, profile=0.027
- `V0001` (`enforceable_resolution`) / `V0029` (`judicial_appeal`): structural=1, profile=0.396
- `V0001` (`enforceable_resolution`) / `V0040` (`judicial_appeal`): structural=1, profile=0.027
- `V0004` (`enforceable_resolution`) / `V0006` (`timely_payment`): structural=1, profile=0.367
- `V0004` (`enforceable_resolution`) / `V0014` (`judicial_appeal`): structural=1, profile=0.022
- `V0004` (`enforceable_resolution`) / `V0018` (`timely_payment`): structural=1, profile=0.367
- `V0004` (`enforceable_resolution`) / `V0029` (`judicial_appeal`): structural=1, profile=0.374
- `V0004` (`enforceable_resolution`) / `V0031` (`judicial_appeal`): structural=1, profile=0.030
- `V0004` (`enforceable_resolution`) / `V0054` (`timely_payment`): structural=1, profile=0.011
- `V0004` (`enforceable_resolution`) / `V0085` (`timely_payment`): structural=1, profile=0.006

## Residual

9/231 variants (3.9%), 20398/150370 cases (13.6%) unassigned.

- `V0003`: The case ends in sending the fine without resolution or further progression, leaving it outside final resolution categories.
- `V0077`: The narrative is incomplete or anomalous, ending prematurely with Send Fine after appeal steps.
- `V0093`: The sequence is unusual, starting with a judicial appeal before sending the fine.
- `V0160`: Ends in credit collection rather than timely payment, enforcement, or appeals.
- `V0161`: Ends in credit collection despite mixed appeal actions.
- `V0163`: Ends in credit collection after prefecture appeal steps.
- `V0169`: Ends in credit collection after repeated payments failed to close the case in time.
- `V0173`: Ends in credit collection after uncoordinated payments.
- `V0182`: Involves prefecture appeal steps but ultimately ends in credit collection.