from __future__ import annotations

import pandas as pd
import pm4py

from ..config import PipelineConfig


def load_event_log(config: PipelineConfig) -> pd.DataFrame:
    return pm4py.read_xes(str(config.log_path))
