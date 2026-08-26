"""Subprocess control for the GUI's pipeline runs.

Each pipeline run/round is executed by `python -m gui.worker` in a fresh subprocess, not
in-process and not in a background thread of the Streamlit process itself. Two reasons:

1. `goalcat.run_logging.get_logger()` caches the "goalcat" logger (and its file handler) at
   process scope — the first run in a long-lived process claims pipeline.log for good, and every
   later run in that same process would silently keep writing into it. A long-lived Streamlit
   process launching many runs over a session needs one fresh process per run to get one fresh
   logger per run.
2. A background thread inside the Streamlit process would need to call `st.*` from that thread,
   which Streamlit does not support safely. A subprocess sidesteps this entirely: it never touches
   Streamlit, it only writes plain files (pipeline.log, gui_status.json) that the main Streamlit
   process polls.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from goalcat.config import REPO_ROOT

#: Keys are step numbers, except Step 7b — hence `int | str` rather than `int`. 7b sits between 7
#: and 8 sequentially but does not take a number of its own: the pipeline's architectural claim is
#: nine steps and 7b is an optional enrichment of them, absent entirely on a goal model that does
#: not bind its indicators to the log. Unrelated to the "5a/5b" letters used elsewhere for the two
#: mutually exclusive taxonomy-induction *modes* — Step 5 appears here once, undifferentiated,
#: because exactly one of those modes ever runs.
STEP_NAMES: dict[int | str, str] = {
    1: "Variant extraction",
    2: "Multi-view profiling",
    3: "Textualization",
    4: "Narrative sampling",
    5: "Taxonomy induction",
    6: "Narrative assignment",
    7: "Per-category discovery",
    "7b": "Indicator satisfaction",
    8: "High-level description",
    9: "Business review",
}

STATUS_FILENAME = "gui_status.json"
WORKER_LOG_FILENAME = "gui_worker_stdout.log"


def launch_worker(
    config_path: Path, run_id: str, steps: str, round_: int | None, status_dir: Path
) -> subprocess.Popen:
    """Launches `python -m gui.worker` as a fresh subprocess. steps: "1-8" or "9".

    status_dir is where the worker writes gui_status.json (run_output_dir for "1-8", the round's
    own directory for "9") — this function also writes the subprocess's own stdout/stderr there,
    as gui_worker_stdout.log, for the rare case a failure happens before the worker's own
    exception handling can write to gui_status.json (e.g. an import error).
    """
    status_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "gui.worker",
        "--config", str(config_path),
        "--run-id", run_id,
        "--steps", steps,
    ]
    if round_ is not None:
        cmd += ["--round", str(round_)]

    worker_log_path = status_dir / WORKER_LOG_FILENAME
    with open(worker_log_path, "w", encoding="utf-8") as log_file:
        popen = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT, cwd=str(REPO_ROOT))
    return popen


def read_status(status_path: Path) -> dict | None:
    if not status_path.exists():
        return None
    try:
        return json.loads(status_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        # gui/worker.py writes atomically (temp file + os.replace), so this should be rare —
        # treat it as "not ready yet" rather than an error; the next poll will see the real file.
        return None


def tail_lines(path: Path, n: int = 200) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-n:]
