"""Experiment 2's controlled goal-model perturbations (EXPERIMENTATION_PLAN.md §4).

Built on `goalcat.grl` (the project's sole `.jucm`-reading/writing module — see its own package
docstring): loading a base model, applying a perturbation, and validating the result are all
`GRLModel` operations, not text/markdown editing. `data/goals/*GM_description.md` documents are never
read or written by anything in this package, matching every other consumer in the project.
"""

from goalcat.grl import GRLModel, declared_alternatives, read_jucm

from .perturb import (
    PERTURBED_DIR,
    PerturbationResult,
    add_distractor,
    merge_alternatives,
    remove_alternative,
)

__all__ = [
    "PERTURBED_DIR",
    "GRLModel",
    "PerturbationResult",
    "add_distractor",
    "declared_alternatives",
    "merge_alternatives",
    "read_jucm",
    "remove_alternative",
]
