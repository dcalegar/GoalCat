# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep2` | Log: `rtfm` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Direct Payment (`direct_payment`)

Cases where the fine is created and promptly paid with very short trace lengths and durations, often without involving extensive notification or penalty steps.

**Taxonomy-derivation rationale (Step 5):** High frequency among low-duration and low-length variants (e.g., V0002, V0007), representing straightforward fine settlements.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 2/231 variants (0.9%) · micro 49502/150370 cases (32.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 1.00, nearest other category `delayed_payment` at mean distance 5.09

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.157, nearest other category `delayed_payment` at mean distance 0.325

## Standard Collection / Credit Referral (`standard_collection`)

Cases that progress through standard notifications and penalties over a moderate to long duration, ultimately culminating in credit collection.

**Taxonomy-derivation rationale (Step 5):** Dominates the high-frequency long-duration tail of the log where fines remain unpaid and are escalated (e.g., V0001, V0009).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 30/231 variants (13.0%) · micro 58638/150370 cases (39.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.39, nearest other category `delayed_payment` at mean distance 4.66

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.267, nearest other category `appeals_and_legal` at mean distance 0.426

## Delayed Payment with Penalties (`delayed_payment`)

Cases where payment occurs after significant delays, intermediate notifications, penalties, and frequently exhibits repeated payment transactions.

**Taxonomy-derivation rationale (Step 5):** Represents the cluster of variants featuring standard notifications, added penalties, and multiple recurring payment steps (e.g., V0004, V0005, V0006).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 32/231 variants (13.9%) · micro 9639/150370 cases (6.4%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.90, nearest other category `appeals_and_legal` at mean distance 4.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.220, nearest other category `payment_rework_loops` at mean distance 0.232

## Appeals and Legal Proceedings (`appeals_and_legal`)

Complex cases involving formal appeals to the prefecture or judge, resulting in extended durations, prefecture results, and alternative resolution paths.

**Taxonomy-derivation rationale (Step 5):** Captures variants explicitly containing appeal-related activities such as Send Appeal to Prefecture and Appeal to Judge (e.g., V0008, V0057, V0103).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 115/231 variants (49.8%) · micro 4388/150370 cases (2.9%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.96, nearest other category `delayed_payment` at mean distance 4.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.338, nearest other category `direct_payment` at mean distance 0.389

## Payment Rework Loops (`payment_rework_loops`)

Outlier variants characterized by an exceptionally high trace length driven by repetitive, sequential payment installments or iterative transactional rework.

**Taxonomy-derivation rationale (Step 5):** Identified by extreme length and repetition of payment events over prolonged periods (e.g., V0153, V0151, V0147, V0224).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 50/231 variants (21.6%) · micro 7456/150370 cases (5.0%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.97, nearest other category `delayed_payment` at mean distance 5.83

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.080, nearest other category `delayed_payment` at mean distance 0.232

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.106
- `V0048` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.091
- `V0142` / `V0153` (category `payment_rework_loops`): structural=17, profile=0.038
- `V0153` / `V0193` (category `payment_rework_loops`): structural=17, profile=0.461
- `V0018` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.057
- `V0024` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.061
- `V0060` / `V0153` (category `payment_rework_loops`): structural=16, profile=0.051
- `V0006` / `V0153` (category `payment_rework_loops`): structural=15, profile=0.057
- `V0061` / `V0153` (category `payment_rework_loops`): structural=15, profile=0.030
- `V0067` / `V0153` (category `payment_rework_loops`): structural=15, profile=0.333

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_collection`) / `V0004` (`delayed_payment`): structural=1, profile=0.355
- `V0001` (`standard_collection`) / `V0017` (`appeals_and_legal`): structural=1, profile=0.027
- `V0001` (`standard_collection`) / `V0029` (`appeals_and_legal`): structural=1, profile=0.396
- `V0002` (`direct_payment`) / `V0048` (`payment_rework_loops`): structural=1, profile=0.500
- `V0004` (`delayed_payment`) / `V0005` (`payment_rework_loops`): structural=1, profile=0.357
- `V0004` (`delayed_payment`) / `V0006` (`payment_rework_loops`): structural=1, profile=0.367
- `V0004` (`delayed_payment`) / `V0009` (`standard_collection`): structural=1, profile=0.354
- `V0004` (`delayed_payment`) / `V0014` (`appeals_and_legal`): structural=1, profile=0.022
- `V0004` (`delayed_payment`) / `V0018` (`payment_rework_loops`): structural=1, profile=0.367
- `V0004` (`delayed_payment`) / `V0024` (`payment_rework_loops`): structural=1, profile=0.371

## Residual

2/231 variants (0.9%), 20747/150370 cases (13.8%) unassigned.

- `V0003`: Ends in Send Fine without payment or further collection steps, which does not fit any of the payment, collection, or appeal process outcomes.
- `V0012`: An unusual sequence involving prompt payment followed by sending the fine later, not matching any standard category.