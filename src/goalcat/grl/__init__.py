"""Reading, rendering, and writing GRL goal models in jUCMNav's `.jucm` (URN/GRL XMI) format.

`.jucm` is the project's sole goal-model artifact (`data/goals/<log>_goal_model.jucm`) — every
`<log>GM_description.md` alongside it is documentation *about* how the `.jucm` was authored, never a
pipeline input. `goalcat.config.PipelineConfig.goal_model_path`/`goal_model_filename` point at the
`.jucm` file; `goal_model_path.read_text()` therefore yields XMI text, and everything in this
package that used to slice a markdown document instead parses that XMI directly.

`model.py` defines the in-memory GRL structure this project actually uses (intentional elements,
actors, decomposition/contribution links, KPI indicators) against the real `grl.ecore`/
`urncore.ecore` metamodel, fetched from jUCMNavPlus
(https://github.com/JUCMNAV/jUCMNavPlus/tree/master/seg.jUCMNav/src/seg/jUCMNav/emf) rather than
guessed — the same source the goal models' own provenance notes cite. `jucm_io.py` reads and
writes the `.jucm` XMI. `evaluation.py` holds the satisfaction arithmetic — KPI conversion and quantitative
propagation, behaviourally equivalent to jUCMNav's own; `measures.py` binds an `Indicator` to the
event log through URN `Metadata`, which is what lets Step 7b (`goalcat.indicators`) measure a goal
model against a real log at all. `prompt.py` renders a parsed model into the text Step 5a/6 send an LLM,
and resolves/validates `anchor_ids` — the GRL-native replacement for what
`goalcat.llm.taxonomy._extract_sections()`/`_extract_declared_ids()`/`_resolve_anchor_labels()`
used to do against a markdown §1-§7 structure.

Deliberately *not* built on `pm4py_ucm` (installed as a dependency for the ICPM 2027 UCM-side
work, see `experimentation/icpm2027`): verified against its 0.7.10 source, its `.jucm` importer
explicitly skips `grlspec` ("GRL spec contents ... [are] not modeled") and its exporter writes an
empty `<grlspec/>` — it has no GRL read or write path to extend. This package is new code, not a
vendored/modified copy of anything, so it lives under `src/goalcat/` rather than `third_party/`.
"""

from .evaluation import PropagationResult, indicator_evaluation, is_one_sided, propagate
from .measures import MeasureOutcome, MeasureSpec, measure_specs, measure_sublog
from .model import (
    ActorDef,
    ContributionLink,
    DecompositionLink,
    GRLModel,
    IntentionalElement,
    KPIIndicator,
)
from .jucm_io import parse_jucm, read_jucm, write_jucm
from .prompt import (
    declared_alternatives,
    declared_ids,
    grounding_problems,
    render_excerpt,
    resolve_anchor_labels,
)

__all__ = [
    "ActorDef",
    "ContributionLink",
    "DecompositionLink",
    "GRLModel",
    "IntentionalElement",
    "KPIIndicator",
    "MeasureOutcome",
    "MeasureSpec",
    "PropagationResult",
    "declared_alternatives",
    "declared_ids",
    "grounding_problems",
    "indicator_evaluation",
    "is_one_sided",
    "measure_specs",
    "measure_sublog",
    "parse_jucm",
    "propagate",
    "read_jucm",
    "render_excerpt",
    "resolve_anchor_labels",
    "write_jucm",
]
