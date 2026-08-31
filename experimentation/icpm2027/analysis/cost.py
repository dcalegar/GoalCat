"""`python -m experimentation.icpm2027.analysis.cost` — the single reproducible aggregation of
hosted-LLM spend for the ICPM 2027 study.

Every LLM call the pipeline makes writes a `*_run_metadata.json` next to its output. Two shapes
occur and *both* must be summed or the total is silently ~60x low:

  - single-call steps (5a taxonomy, 8 description) carry a scalar ``estimated_cost_usd``;
  - the batched assignment step (6) carries ``total_estimated_cost_usd`` plus a ``calls`` list.

The run set is defined explicitly here, not by a wildcard, so the reported figure is auditable:

  ICPM  = data/output/{rtfm,sepsis,bpic2019}/icpm2027_*/   (E1, E2, C12 stability)
  CASE  = data/output/rtfm_mini/*/                         (illustrative case study)

Writes ``data/output/icpm2027_results/cost.md``. Figures are indicative, not a benchmark
(pricing basis is stamped in each run's metadata); an abandoned BPIC 2019 batch-size-50 run is
*not* on disk and is not counted here.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT = REPO_ROOT / "data" / "output" / "icpm2027_results" / "cost.md"


def _iter_metadata() -> list[tuple[str, str, Path]]:
    """(dataset, run_id, metadata_path) for every counted run."""
    out: list[tuple[str, str, Path]] = []
    base = REPO_ROOT / "data" / "output"
    for dataset in ("rtfm", "sepsis", "bpic2019"):
        for run_dir in sorted((base / dataset).glob("icpm2027_*")):
            if not run_dir.is_dir():
                continue
            for md in run_dir.glob("round*/*/*run_metadata*.json"):
                out.append((dataset, run_dir.name, md))
    for run_dir in sorted((base / "rtfm_mini").glob("*")):
        if run_dir.is_dir():
            for md in run_dir.glob("round*/*/*run_metadata*.json"):
                out.append(("rtfm_mini", run_dir.name, md))
    return out


def _call(md: Path) -> tuple[float, int, int, int]:
    """(cost_usd, calls, input_tokens, output_tokens) for one metadata file."""
    d = json.loads(md.read_text(encoding="utf-8"))
    cost = (d.get("estimated_cost_usd") or 0.0) + (d.get("total_estimated_cost_usd") or 0.0)
    calls = d.get("calls")
    n = len(calls) if isinstance(calls, list) else int(calls or d.get("n_calls") or 1)
    tin = int(d.get("input_tokens") or d.get("total_input_tokens") or 0)
    tout = int(d.get("output_tokens") or d.get("total_output_tokens") or 0)
    return cost, n, tin, tout


def _bucket(run_id: str) -> str:
    if run_id.startswith("icpm2027_e1_"):
        return "E1"
    if run_id.startswith("icpm2027_c12_"):
        return "C12 stability"
    if run_id.startswith("icpm2027_e2_"):
        return "E2"
    return "case study"


def aggregate() -> dict:
    per_bucket: dict[tuple[str, str], list[float]] = defaultdict(lambda: [0.0, 0, 0, 0])
    grand = [0.0, 0, 0, 0]
    for dataset, run_id, md in _iter_metadata():
        cost, n, tin, tout = _call(md)
        key = (dataset, _bucket(run_id))
        acc = per_bucket[key]
        acc[0] += cost
        acc[1] += n
        acc[2] += tin
        acc[3] += tout
        for i, v in enumerate((cost, n, tin, tout)):
            grand[i] += v
    return {"per_bucket": per_bucket, "grand": grand}


def to_markdown(agg: dict) -> str:
    rows = agg["per_bucket"]
    g = agg["grand"]
    lines = [
        "# Hosted-LLM spend — ICPM 2027 study (Task C15)",
        "",
        "Single reproducible aggregation (`analysis/cost.py`). Sums `estimated_cost_usd` "
        "(single-call steps) **and** `total_estimated_cost_usd` (batched assignment) over the "
        "run set defined in that module. Indicative, not a benchmark.",
        "",
        "| Dataset | Phase | Cost (USD) | Calls | Input tok | Output tok |",
        "|---|---|--:|--:|--:|--:|",
    ]
    for key in sorted(rows):
        c, n, ti, to = rows[key]
        lines.append(f"| {key[0]} | {key[1]} | {c:.2f} | {n} | {ti:,} | {to:,} |")
    lines += [
        f"| **all** | **all** | **{g[0]:.2f}** | **{int(g[1])}** | **{int(g[2]):,}** | **{int(g[3]):,}** |",
        "",
    ]
    e1 = sum(v[0] for k, v in rows.items() if k[1] == "E1")
    e1_calls = sum(v[1] for k, v in rows.items() if k[1] == "E1")
    e1_by_ds = {k[0]: v[0] for k, v in rows.items() if k[1] == "E1"}
    lines += [
        "## Headline",
        "",
        f"- **Whole study: ~{int(g[1])} calls, ~USD {g[0]:.2f}** "
        f"({g[2] / 1e6:.1f} M input + {g[3] / 1e6:.1f} M output tokens).",
        f"- **Experiment 1 (22 conditions): ~USD {e1:.2f}** ({int(e1_calls)} calls) — "
        + ", ".join(f"{ds} USD {c:.2f}" for ds, c in sorted(e1_by_ds.items())) + ".",
        "- BPIC 2019 dominates because its assignment runs at `batch_size = 25` over 11,973 "
        "variants (~480 calls per condition).",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    agg = aggregate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(to_markdown(agg), encoding="utf-8")
    print(to_markdown(agg))
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
