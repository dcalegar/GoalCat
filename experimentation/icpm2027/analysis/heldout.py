"""Task C1 — held-out label recovery for BPIC 2019.

The study's one non-partition-divergence check: the log carries an organization-supplied case
attribute (`case:Item Category`) that names, for every case, which matching regime it followed.
`narrative/textualization.py` builds the Step 5a/5b/6 input from a fixed field set that excludes
every `case:` attribute, so this label never reaches the LLM — it is genuinely held out from the
pipeline.

**This is label recovery under an axis-aligned frame, not accuracy against independent ground
truth.** `bpic2019_goal_model.jucm`'s declared OR-alternatives (3-way-after-GR, 3-way-before-GR,
2-way, consignment) and `case:Item Category`'s four values name the same distinction *by
construction* — the goal model was authored knowing this attribute exists. Agreement therefore
measures whether Step 6 places variants on the axis the goal model declares, given narratives that
must convey the goods-receipt / invoice ordering; it is not evidence that either labelling is
correct. Consignment (goal-model task T9, anchor 13) additionally has no distinguishing activity
label in the log, so its agreement figure is not comparable to the other three (README, Task C1).

`per_case` is passed in, not read here: extracting a case attribute means parsing the full XES
(~90 s for BPIC 2019), so `extract_heldout_series()` caches it to parquet and the callers reuse it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

CAVEAT = (
    "Label recovery under an axis-aligned frame (Task C1): the goal model's declared alternatives "
    "and `case:Item Category` name the same distinction by construction, so agreement is not "
    "accuracy and neither labelling is ground truth. The attribute is excluded from the narrative "
    "by construction, so it is held out from Steps 5-6 but not independent of the goal model's "
    "design. Consignment (anchor 13 / task T9) has no distinguishing activity label and its figure "
    "is not comparable to the other three."
)


def extract_heldout_series(
    log_path: str | Path, case_id_key: str, attribute: str, cache_path: str | Path
) -> pd.Series:
    """`case_id -> attribute value`, one row per case (first non-null occurrence). Cached to
    `cache_path` (parquet); the XES parse only runs on a cache miss."""
    cache_path = Path(cache_path)
    if cache_path.exists():
        cached = pd.read_parquet(cache_path)
        return pd.Series(cached["value"].values, index=cached["case_id"].astype(str), name=attribute)

    import pm4py

    df = pm4py.read_xes(str(log_path))
    per_case = (
        df.groupby(case_id_key)[attribute]
        .agg(lambda s: s.dropna().iloc[0] if s.notna().any() else None)
        .rename("value")
    )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    per_case.rename_axis("case_id").reset_index().to_parquet(cache_path)
    return pd.Series(per_case.values, index=per_case.index.astype(str), name=attribute)


@dataclass
class LabelRecoveryResult:
    dataset_id: str
    condition_id: str
    anchor_to_label: dict[str, str]
    #: rows = guided label (or "(residual)"), cols = held-out label. Case- and variant-weighted.
    confusion_cases: pd.DataFrame
    confusion_variants: pd.DataFrame
    n_cases: int
    n_variants: int
    #: agreement among cases/variants that got a guided label (residual excluded), and overall
    #: (residual counted as a miss).
    agree_cases_labelled: float
    agree_cases_overall: float
    agree_variants_labelled: float
    agree_variants_overall: float
    per_label: pd.DataFrame  # label, truth_cases, guided_cases, recall_cases, precision_cases, comparable
    notes: list[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [
            f"# Task C1 — held-out label recovery ({self.dataset_id}, `{self.condition_id}`)",
            "",
            f"_{CAVEAT}_",
            "",
            f"- Cases: {self.n_cases:,} | Variants: {self.n_variants:,}",
            f"- Case-weighted agreement (labelled only / overall incl. residual as miss): "
            f"**{self.agree_cases_labelled:.1%}** / {self.agree_cases_overall:.1%}",
            f"- Variant-weighted agreement (labelled only / overall): "
            f"**{self.agree_variants_labelled:.1%}** / {self.agree_variants_overall:.1%}",
            "",
            "## Per-label recovery (case-weighted)",
            "",
            self.per_label.to_markdown(index=False),
            "",
            "_`recall` = held-out-label cases the guided arm also gave that label; "
            "`precision` = guided-label cases whose held-out label matches. "
            "Rows marked `comparable = False` carry the Consignment caveat above._",
            "",
            "## Confusion matrix — case-weighted (rows = guided label, cols = `case:Item Category`)",
            "",
            self.confusion_cases.to_markdown(),
            "",
            "## Confusion matrix — variant-weighted",
            "",
            self.confusion_variants.to_markdown(),
        ]
        if self.notes:
            lines += ["", "## Notes", ""] + [f"- {n}" for n in self.notes]
        return "\n".join(lines) + "\n"


def compute_label_recovery(
    assignments_df: pd.DataFrame,
    variants_df: pd.DataFrame,
    per_case: pd.Series,
    taxonomy: dict,
    anchor_to_label: dict[str, str],
    dataset_id: str,
    condition_id: str,
    incomparable_labels: tuple[str, ...] = (),
) -> LabelRecoveryResult:
    """Explodes each variant to its member cases, maps its guided category through its first
    `anchor_id` to a held-out label, and tabulates agreement against `per_case`.

    `variants_df` must carry `case_ids` as a list (``goalcat.extraction.variants.load_variants``
    reconstructs it); `taxonomy` is the condition's `taxonomy.json` dict, used only to resolve
    `category_id -> anchor_id`.
    """
    anchor_of = {c["category_id"]: (c.get("anchor_ids") or [None])[0] for c in taxonomy["categories"]}
    cat_of = dict(zip(assignments_df["variant_id"].astype(str), assignments_df["category_id"]))
    truth_of = per_case.to_dict()

    RESID = "(residual)"
    variant_rows: list[tuple[str, str, str, int]] = []  # variant_id, guided_label, ???unused
    case_rows: list[tuple[str, str]] = []  # guided_label, truth_label
    variant_pairs: list[tuple[str, str]] = []  # guided_label, truth_label (majority truth of the variant)

    for _, r in variants_df.iterrows():
        vid = str(r["variant_id"])
        cid = cat_of.get(vid)
        anchor = anchor_of.get(cid) if isinstance(cid, str) else None
        guided_label = anchor_to_label.get(str(anchor), RESID) if anchor is not None else RESID
        case_ids = r["case_ids"] if isinstance(r["case_ids"], list) else str(r["case_ids"]).split(",")
        truths = [truth_of.get(str(c)) for c in case_ids]
        for tr in truths:
            case_rows.append((guided_label, tr if tr is not None else "(unlabelled)"))
        # variant-weighted: the variant's modal held-out label
        s = pd.Series([t for t in truths if t is not None])
        modal = s.mode().iloc[0] if not s.empty else "(unlabelled)"
        variant_pairs.append((guided_label, modal))

    cdf = pd.DataFrame(case_rows, columns=["guided", "truth"])
    vdf = pd.DataFrame(variant_pairs, columns=["guided", "truth"])
    labels = list(anchor_to_label.values())
    col_order = labels + [l for l in cdf["truth"].unique() if l not in labels]
    row_order = labels + [RESID]

    def _confusion(df: pd.DataFrame) -> pd.DataFrame:
        ct = pd.crosstab(df["guided"], df["truth"])
        ct = ct.reindex(index=[r for r in row_order if r in ct.index],
                        columns=[c for c in col_order if c in ct.columns], fill_value=0)
        ct["All"] = ct.sum(axis=1)
        ct.loc["All"] = ct.sum(axis=0)
        return ct

    def _agree(df: pd.DataFrame) -> tuple[float, float]:
        labelled = df[df["guided"] != RESID]
        a_lab = (labelled["guided"] == labelled["truth"]).mean() if len(labelled) else float("nan")
        a_all = (df["guided"] == df["truth"]).mean() if len(df) else float("nan")
        return float(a_lab), float(a_all)

    ac_lab, ac_all = _agree(cdf)
    av_lab, av_all = _agree(vdf)

    per_label_rows = []
    for lbl in labels:
        t = cdf["truth"] == lbl
        g = cdf["guided"] == lbl
        tp = int((t & g).sum())
        per_label_rows.append({
            "label": lbl,
            "truth_cases": int(t.sum()),
            "guided_cases": int(g.sum()),
            "recall_cases": round(tp / t.sum(), 4) if t.sum() else float("nan"),
            "precision_cases": round(tp / g.sum(), 4) if g.sum() else float("nan"),
            "comparable": lbl not in incomparable_labels,
        })

    return LabelRecoveryResult(
        dataset_id=dataset_id,
        condition_id=condition_id,
        anchor_to_label=anchor_to_label,
        confusion_cases=_confusion(cdf),
        confusion_variants=_confusion(vdf),
        n_cases=len(cdf),
        n_variants=len(vdf),
        agree_cases_labelled=ac_lab,
        agree_cases_overall=ac_all,
        agree_variants_labelled=av_lab,
        agree_variants_overall=av_all,
        per_label=pd.DataFrame(per_label_rows),
    )


def main(argv: list[str] | None = None) -> int:
    """`python -m experimentation.icpm2027.analysis.heldout --dataset bpic2019` — runs Task C1 for
    each named condition (default: the two guided E1 replicates) and writes one combined report."""
    import argparse

    from goalcat.config import REPO_ROOT
    from goalcat.extraction.variants import load_variants

    from ..protocol import DatasetSpec

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--dataset", default="bpic2019")
    parser.add_argument(
        "--conditions", default="e1_guided_rep1,e1_guided_rep2",
        help="Comma-separated condition ids under data/output/<log>/icpm2027_<id>/",
    )
    args = parser.parse_args(argv)

    ds = DatasetSpec.load(args.dataset)
    if not ds.heldout_case_attribute or not ds.heldout_label_map:
        raise SystemExit(f"{args.dataset} has no heldout_case_attribute / heldout_label_map — Task C1 is bpic2019-only.")

    out_root = REPO_ROOT / "data" / "output" / ds.log_stem
    per_case = extract_heldout_series(
        ds.log_path, ds.case_id_key, ds.heldout_case_attribute,
        cache_path=out_root / f"heldout_{ds.heldout_case_attribute.replace(':', '_').replace(' ', '_')}.parquet",
    )
    variants_df = load_variants(str(out_root / "icpm2027_base" / "01_variants" / "variants.csv"))

    sections = []
    for cond in [c.strip() for c in args.conditions.split(",") if c.strip()]:
        cdir = out_root / f"icpm2027_{cond}" / "round1"
        assignments = pd.read_csv(cdir / "06_assignment" / "assignments.csv", dtype={"variant_id": str})
        taxonomy = json.loads((cdir / "05_taxonomy" / "taxonomy.json").read_text())
        res = compute_label_recovery(
            assignments, variants_df, per_case, taxonomy, ds.heldout_label_map,
            dataset_id=args.dataset, condition_id=cond,
            incomparable_labels=tuple(ds.heldout_incomparable_labels),
        )
        sections.append(res.to_markdown())
        print(f"{cond}: case-agreement(labelled)={res.agree_cases_labelled:.1%}  "
              f"variant-agreement(labelled)={res.agree_variants_labelled:.1%}")

    report_path = REPO_ROOT / "data" / "output" / "icpm2027_results" / args.dataset / "label_recovery.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n\n---\n\n".join(sections), encoding="utf-8")
    print(f"Wrote {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
