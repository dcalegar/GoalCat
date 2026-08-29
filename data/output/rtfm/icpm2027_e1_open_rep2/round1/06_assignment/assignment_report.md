# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep2` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases that proceed directly from creation to payment with minimal activity steps and low duration, representing straightforward and timely settlements.

**Taxonomy-derivation rationale (Step 5):** Grouped because these variants share a short trace length, fast resolution, and a direct payment outcome without complex notifications or escalation.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 2/231 variants (0.9%) · micro 49502/150370 cases (32.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.00, nearest other category `standard_collection_or_payment` at mean distance 5.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.157, nearest other category `prefecture_appeal` at mean distance 0.384

## Standard Notification and Resolution (`standard_collection_or_payment`)

Cases involving standard administrative steps such as fine notification and penalty addition, eventually leading either to delayed payment or escalation to credit collection.

**Taxonomy-derivation rationale (Step 5):** Represents the most frequent business paths where standard fines are issued, notified, penalized, and resolved either by payment or credit collection over moderate to long durations.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 38/231 variants (16.5%) · micro 68165/150370 cases (45.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.47, nearest other category `prefecture_appeal` at mean distance 4.60

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.314, nearest other category `prefecture_appeal` at mean distance 0.367

## Rework-Heavy Payment (`rework_heavy_payment`)

Cases characterized by extensive repetition of payment activities over long trace lengths, indicating installment-like behavior or payment processing loops.

**Taxonomy-derivation rationale (Step 5):** Clearly distinguished by high trace lengths containing numerous repeated payment steps despite standard initial fine creation and notification paths.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 68/231 variants (29.4%) · micro 7529/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.55, nearest other category `standard_collection_or_payment` at mean distance 5.94

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.105, nearest other category `direct_payment` at mean distance 0.515

## Prefecture Appeal and Legal Escalation (`prefecture_appeal`)

Complex cases involving appeals to the prefecture or judge, result notifications, and extended legal or administrative reviews before final resolution.

**Taxonomy-derivation rationale (Step 5):** Grouped by the presence of appeal-related activities (e.g., Send Appeal to Prefecture, Appeal to Judge) reflecting lengthy dispute resolution paths.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 121/231 variants (52.4%) · micro 4427/150370 cases (2.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.95, nearest other category `standard_collection_or_payment` at mean distance 4.60

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `standard_collection_or_payment` at mean distance 0.367

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `rework_heavy_payment`): structural=17, profile=0.106
- `V0048` / `V0153` (category `rework_heavy_payment`): structural=17, profile=0.091
- `V0142` / `V0153` (category `rework_heavy_payment`): structural=17, profile=0.038
- `V0153` / `V0193` (category `rework_heavy_payment`): structural=17, profile=0.461
- `V0018` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.057
- `V0024` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.061
- `V0028` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.086
- `V0060` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.051
- `V0131` / `V0153` (category `rework_heavy_payment`): structural=16, profile=0.360
- `V0153` / `V0174` (category `rework_heavy_payment`): structural=16, profile=0.009

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_collection_or_payment`) / `V0017` (`prefecture_appeal`): structural=1, profile=0.027
- `V0001` (`standard_collection_or_payment`) / `V0029` (`prefecture_appeal`): structural=1, profile=0.396
- `V0001` (`standard_collection_or_payment`) / `V0040` (`prefecture_appeal`): structural=1, profile=0.027
- `V0002` (`direct_payment`) / `V0048` (`rework_heavy_payment`): structural=1, profile=0.500
- `V0004` (`standard_collection_or_payment`) / `V0005` (`rework_heavy_payment`): structural=1, profile=0.357
- `V0004` (`standard_collection_or_payment`) / `V0006` (`rework_heavy_payment`): structural=1, profile=0.367
- `V0004` (`standard_collection_or_payment`) / `V0014` (`prefecture_appeal`): structural=1, profile=0.022
- `V0004` (`standard_collection_or_payment`) / `V0018` (`rework_heavy_payment`): structural=1, profile=0.367
- `V0004` (`standard_collection_or_payment`) / `V0024` (`rework_heavy_payment`): structural=1, profile=0.371
- `V0004` (`standard_collection_or_payment`) / `V0029` (`prefecture_appeal`): structural=1, profile=0.374

## Residual

2/231 variants (0.9%), 20747/150370 cases (13.8%) unassigned.

- `V0003`: Only creates and sends fine without leading to payment, collection, or appeal, falling outside the defined categories.
- `V0012`: Unusual ordering of early payment followed by sending the fine later, not fitting standard categories.