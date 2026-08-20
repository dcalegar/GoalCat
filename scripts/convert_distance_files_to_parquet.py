"""One-off migration: converts existing structural_distances.csv/profile_distances.csv files
(written by the pre-Parquet Step 6) to structural_distances.parquet/profile_distances.parquet in
place, under every data/output/<dataset>/<run_id>/round*/06_assignment/ directory.

review.py's rerender_reports_after_rename() and _prune_pairwise_distances() now look only for the
.parquet filenames (see README's Resource usage section) — any run directory produced before that
change still has the old .csv files on disk and needs this migration once, offline, without
re-running Steps 1-8. Not needed for new runs: Step 6 (llm/assignment.py's
save_assignment_outputs()) writes .parquet directly going forward.

Verifies each conversion by reading the new .parquet back and comparing it row-for-row against the
original .csv before deleting the .csv, so a conversion never trades a readable file for a corrupt
one. Idempotent: re-running after a .csv has already been deleted for a given file just skips it.

Usage: python scripts/convert_distance_files_to_parquet.py [data_output_root]
(defaults to data/output relative to the repository root)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from goalcat.atomic_io import atomic_write_parquet  # noqa: E402

_DISTANCE_ID_COLUMNS = {"variant_id_a": str, "variant_id_b": str}


def _convert_one(csv_path: Path) -> tuple[int, int]:
    """Returns (csv_bytes, parquet_bytes). Raises if the round-tripped Parquet doesn't match the
    source CSV exactly, leaving the .csv in place for inspection rather than deleting it."""
    parquet_path = csv_path.with_suffix(".parquet")
    csv_df = pd.read_csv(csv_path, dtype=_DISTANCE_ID_COLUMNS)
    atomic_write_parquet(csv_df, parquet_path, index=False)

    reread = pd.read_parquet(parquet_path).astype(_DISTANCE_ID_COLUMNS)
    pd.testing.assert_frame_equal(csv_df, reread, check_dtype=False)

    csv_bytes = csv_path.stat().st_size
    parquet_bytes = parquet_path.stat().st_size
    csv_path.unlink()
    return csv_bytes, parquet_bytes


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "data" / "output"
    total_csv = 0
    total_parquet = 0
    converted = 0

    for filename in ("structural_distances.csv", "profile_distances.csv"):
        for csv_path in sorted(root.glob(f"*/*/round*/06_assignment/{filename}")):
            csv_bytes, parquet_bytes = _convert_one(csv_path)
            total_csv += csv_bytes
            total_parquet += parquet_bytes
            converted += 1
            print(
                f"{csv_path.relative_to(root)}: "
                f"{csv_bytes / 1e6:.1f} MB -> {parquet_bytes / 1e6:.1f} MB "
                f"({parquet_bytes / csv_bytes * 100:.1f}%)"
            )

    if converted == 0:
        print("Nothing to convert (no matching .csv files found).")
        return

    print(
        f"\nConverted {converted} file(s): "
        f"{total_csv / 1e9:.2f} GB -> {total_parquet / 1e9:.2f} GB "
        f"({total_parquet / total_csv * 100:.1f}%, {(total_csv - total_parquet) / 1e9:.2f} GB freed)"
    )


if __name__ == "__main__":
    main()
