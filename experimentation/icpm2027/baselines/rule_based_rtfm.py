"""Task C4 — a deterministic, domain-rule baseline for RTFM.

Task C3's structural-clustering baseline answers "can activity-vector similarity alone reproduce
the guided partition?"; it produces ~unlabelled clusters. This baseline answers the sharper
Related-Work question: **can a handful of hand-written activity rules — the kind a analyst writes
in an afternoon, no LLM — reproduce the goal model's five declared alternatives?** If they can,
the guided arm's value on a log this legible is small and should be reported as such (Task C4,
mirrored in the paper's Threats to Validity).

The rules key on activity *presence* and the `Payment` / `Add penalty` order, applied in a fixed
priority (an escalated fine is classified by its escalation even if a payment follows). They are
authored from the RTFM process description, not tuned against the guided assignment.

Fed into the same `analysis.contingency` machinery as Task C3, so the RTFM report can put
rule-baseline-vs-guided beside structural-vs-guided.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

#: category_id -> the goal-model anchor it stands for (same ids the guided taxonomy uses, so the
#: contingency matrix lines up by label).
RULE_CATEGORIES: dict[str, str] = {
    "timely_payment": "12",
    "delinquent_payment": "13",
    "administrative_appeal": "14",
    "judicial_appeal": "19",
    "coercive_credit_collection": "20",
}

_JUDGE = "Appeal to Judge"
_PREFECTURE = "Send Appeal to Prefecture"
_COLLECTION = "Send for Credit Collection"
_PAYMENT = "Payment"
_PENALTY = "Add penalty"


def classify_variant(activity_sequence: list[str]) -> str | None:
    """The rule. Returns a `RULE_CATEGORIES` key, or `None` for "no declared resolution"
    (the residual), matching how the guided arm leaves unresolved variants unassigned."""
    acts = list(activity_sequence)
    present = set(acts)

    if _JUDGE in present:
        return "judicial_appeal"
    if _PREFECTURE in present:
        return "administrative_appeal"
    if _COLLECTION in present:
        return "coercive_credit_collection"
    if _PAYMENT in present:
        if _PENALTY in present and acts.index(_PENALTY) < acts.index(_PAYMENT):
            return "delinquent_payment"
        return "timely_payment"
    return None


@dataclass
class RuleBaselineResult:
    assignments: pd.DataFrame  # variant_id, category_id (nullable)
    category_ids: tuple[str, ...]

    def as_assignments_df(self) -> pd.DataFrame:
        return self.assignments


def run_rule_baseline(variants_df: pd.DataFrame) -> RuleBaselineResult:
    """`variants_df` needs `variant_id` and `activity_sequence` (either a `>`-joined string or a
    list). No LLM, no fit — pure function of each variant's activities."""
    rows = []
    for _, r in variants_df.iterrows():
        seq = r["activity_sequence"]
        seq = seq.split(">") if isinstance(seq, str) else list(seq)
        seq = [a.strip() for a in seq]
        rows.append({"variant_id": str(r["variant_id"]), "category_id": classify_variant(seq)})
    return RuleBaselineResult(
        assignments=pd.DataFrame(rows),
        category_ids=tuple(RULE_CATEGORIES),
    )
