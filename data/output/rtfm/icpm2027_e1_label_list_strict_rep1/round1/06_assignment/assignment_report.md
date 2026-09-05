# Step 6 — Narrative assignment report

Run: `icpm2027_e1_label_list_strict_rep1` | Log: `rtfm` | Taxonomy mode: `intent_guided` | Assignment model: `gemini/gemini-3.5-flash-lite`

231 variants, 150370 cases total.

## Single-payment settlement (`single_payment_settlement`)

The fine is settled in one payment covering the full amount due at that point in the case, with no installment structure and no formal dispute on record.

**Taxonomy-derivation rationale (Step 5):** Distinguishes cases whose settlement required no payment plan from those that did, independent of whether the amount paid included an added penalty.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 45/231 variants (19.5%) · micro 59918/150370 cases (39.8%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.77, nearest other category `formal_dispute` at mean distance 4.32

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.058, nearest other category `installment_settlement` at mean distance 0.341

## Installment or partial-payment settlement (`installment_settlement`)

The fine is settled through two or more separate payments over time, with no formal dispute on record — a payment-plan pattern rather than a single transaction.

**Taxonomy-derivation rationale (Step 5):** Separates settlement mechanics (how payment was structured) from settlement timing, which the appeal-channel framing does not distinguish on its own.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 74/231 variants (32.0%) · micro 7641/150370 cases (5.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 5.46, nearest other category `single_payment_settlement` at mean distance 5.37

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.109, nearest other category `single_payment_settlement` at mean distance 0.341

## Formal dispute lodged (`formal_dispute`)

The offender contests the fine through any formal channel on record (e.g., a filing with an administrative or judicial authority), regardless of which channel or of the dispute's outcome.

**Taxonomy-derivation rationale (Step 5):** Merges administrative and judicial contestation into one bucket, on the premise that, from a collections-office perspective, what matters operationally is that the case left the standard payment track, not which forum received the challenge.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 60/231 variants (26.0%) · micro 3376/150370 cases (2.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 3.94, nearest other category `unresolved_other` at mean distance 4.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.321, nearest other category `single_payment_settlement` at mean distance 0.367

## Referred to external collections (`referred_to_collections`)

The case is escalated to an external credit-collection process because it was not settled or contested through the standard channels within the observed trace.

**Taxonomy-derivation rationale (Step 5):** A case that reaches enforced collection is operationally distinct regardless of how it got there, so it is kept separate from formal_dispute even where a dispute preceded it.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 44/231 variants (19.0%) · micro 59013/150370 cases (39.2%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.10, nearest other category `formal_dispute` at mean distance 4.72

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.182, nearest other category `single_payment_settlement` at mean distance 0.466

## Unresolved or other (`unresolved_other`)

The observed trace ends without a payment, a dispute filing, or a referral to collections — an open, ambiguous, or otherwise unclassifiable case.

**Taxonomy-derivation rationale (Step 5):** A residual bucket for traces that do not exhibit any of the four settlement/escalation patterns above, kept distinct from the pipeline's own no-match residual.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 8/231 variants (3.5%) · micro 20422/150370 cases (13.6%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 4.04, nearest other category `formal_dispute` at mean distance 4.26

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.417, nearest other category `formal_dispute` at mean distance 0.385

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V0023` / `V0153` (category `installment_settlement`): structural=17, profile=0.106
- `V0048` / `V0153` (category `installment_settlement`): structural=17, profile=0.091
- `V0142` / `V0153` (category `installment_settlement`): structural=17, profile=0.038
- `V0018` / `V0153` (category `installment_settlement`): structural=16, profile=0.057
- `V0024` / `V0153` (category `installment_settlement`): structural=16, profile=0.061
- `V0028` / `V0153` (category `installment_settlement`): structural=16, profile=0.086
- `V0039` / `V0153` (category `installment_settlement`): structural=16, profile=0.359
- `V0041` / `V0153` (category `installment_settlement`): structural=16, profile=0.380
- `V0050` / `V0153` (category `installment_settlement`): structural=16, profile=0.381
- `V0056` / `V0153` (category `installment_settlement`): structural=16, profile=0.339

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`referred_to_collections`) / `V0004` (`single_payment_settlement`): structural=1, profile=0.355
- `V0001` (`referred_to_collections`) / `V0029` (`formal_dispute`): structural=1, profile=0.396
- `V0002` (`single_payment_settlement`) / `V0003` (`unresolved_other`): structural=1, profile=0.492
- `V0002` (`single_payment_settlement`) / `V0048` (`installment_settlement`): structural=1, profile=0.500
- `V0003` (`unresolved_other`) / `V0007` (`single_payment_settlement`): structural=1, profile=0.335
- `V0003` (`unresolved_other`) / `V0012` (`single_payment_settlement`): structural=1, profile=0.030
- `V0003` (`unresolved_other`) / `V0063` (`formal_dispute`): structural=1, profile=0.352
- `V0003` (`unresolved_other`) / `V0093` (`formal_dispute`): structural=1, profile=0.015
- `V0004` (`single_payment_settlement`) / `V0005` (`installment_settlement`): structural=1, profile=0.357
- `V0004` (`single_payment_settlement`) / `V0006` (`installment_settlement`): structural=1, profile=0.367

## Residual

0/231 variants (0.0%), 0/150370 cases (0.0%) unassigned.
