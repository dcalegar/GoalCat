"""Experiment 2's controlled goal-model perturbations (EXPERIMENTATION_PLAN.md §4).

Three perturbations, each producing a **new** frozen `.jucm` file under
`data/goals/perturbed/` plus a provenance record — never an edit to the base model, whose own
freeze policy (every `data/goals/*GM_description.md`'s own §8) requires a new version rather than an
in-place change:

- **A — alternative removal.** One declared alternative `g_x` (a child of an Or/Xor-decomposed
  element) disappears from the model entirely.
- **B — alternative merge.** Two declared alternatives of the same parent collapse into one, to
  test whether the corresponding partition boundary weakens or disappears while unrelated
  categories stay stable.
- **C — artificial plausible distractor.** A new alternative is added under an existing Or/Xor
  goal, to measure uptake.

Built directly on `goalcat.grl.GRLModel` (read via `goalcat.grl.read_jucm()`, the same schema-
validated path Step 5a/6 use) rather than the markdown+mermaid text-rewriting this module's first
version used — manipulating typed objects and writing back through `goalcat.grl.write_jucm()`
(itself schema-validated via pyecore) means a perturbation cannot produce a structurally broken
model the way regex-editing two independently-hand-synced document sections could.

**Where the perturbation is disclosed.** `data/goals/*GM_description.md`'s own §1-§8 prose (purpose,
provenance, freeze status) is *not* part of what any perturbation here touches, by construction —
that document is never read by the pipeline (see `goalcat.grl`'s package docstring) and this
module never edits it. Disclosure instead lives in the generated `.jucm`'s own metadata: `author`
carries a note identifying the perturbation, and a sibling `<output>.provenance.json` records
target elements, the base model's hash, and a human-readable summary — exactly what a reader
auditing `data/goals/perturbed/` needs, without depending on prose the LLM could ever see (Step
5a's prompt is built from `goalcat.grl.render_excerpt()`, which renders `grlspec` content only —
`author` and any `.md` are both outside that render path either way).
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from goalcat.config import REPO_ROOT
from goalcat.grl import (
    ContributionLink,
    DecompositionLink,
    GRLModel,
    IntentionalElement,
    declared_alternatives,
    render_excerpt,
    write_jucm,
)

PERTURBED_DIR = REPO_ROOT / "data" / "goals" / "perturbed"


@dataclass
class PerturbationResult:
    """One generated perturbed goal model, and everything needed to audit where it came from."""

    perturbation_id: str
    kind: str
    targets: tuple[str, ...]
    base_path: Path
    base_sha256: str
    output_path: Path
    output_sha256: str
    model: GRLModel
    notes: list[str] = field(default_factory=list)

    @property
    def goal_model_filename(self) -> str:
        """Relative to `data/goals/` — how `PipelineConfig.goal_model_filename` addresses it
        (`goal_model_path` joins the fixed `data/goals/` prefix, so a subdirectory works)."""
        return str(self.output_path.relative_to(REPO_ROOT / "data" / "goals"))

    def provenance(self) -> dict[str, Any]:
        return {
            "schema": "icpm2027/perturbation/2",
            "perturbation_id": self.perturbation_id,
            "kind": self.kind,
            "targets": list(self.targets),
            "base_model": {"path": str(self.base_path.relative_to(REPO_ROOT)), "sha256": self.base_sha256},
            "output": {"path": str(self.output_path.relative_to(REPO_ROOT)), "sha256": self.output_sha256},
            "goal_model_filename": self.goal_model_filename,
            "generated_on": date.today().isoformat(),
            "notes": self.notes,
        }


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _clone(model: GRLModel) -> GRLModel:
    """A deep, independent copy — every perturbation mutates a clone of the base model, never the
    base itself, so `remove_alternative`/`merge_alternatives`/`add_distractor` can be called
    repeatedly against one loaded base without one perturbation's edits leaking into another's."""
    return copy.deepcopy(model)


def _require_declared_alternative(model: GRLModel, element_id: str) -> str:
    """Returns the parent element id, raising if `element_id` is not a declared Or/Xor
    alternative — Experiment 2 perturbs *declared alternatives*, not arbitrary elements."""
    alternatives = declared_alternatives(model)
    for parent_id, children in alternatives.items():
        if element_id in children:
            return parent_id
    raise ValueError(
        f"{element_id!r} is not a declared alternative in {model.source_path}. Declared "
        f"alternatives (parent -> children): {alternatives}"
    )


def _finalize(
    model: GRLModel,
    *,
    base: GRLModel,
    perturbation_id: str,
    kind: str,
    targets: tuple[str, ...],
    summary: str,
    notes: list[str],
    out_dir: Path,
) -> PerturbationResult:
    """Stamps provenance into the model's own metadata, writes it, and returns the result.

    Validates the model still holds together (every `Decomposition`/`Contribution` link's `src`/
    `dest` resolves to a real element) before writing — the one structural-integrity check that
    matters here, since `GRLModel` construction itself already guarantees every attribute is a
    real GRL literal (no arbitrary regex edit could have introduced an invalid enum value the way
    the text-based predecessor's checks had to guard against).
    """
    base_text = render_excerpt(base)  # deterministic text form of the base, hashed for provenance
    base_sha = _sha256_text(base_text)

    valid_ids = set(model.elements)
    broken = [
        f"{link.id}: {link.src}->{link.dest}"
        for link in list(model.decompositions) + list(model.contributions)
        if link.src not in valid_ids or link.dest not in valid_ids
    ]
    if broken:
        raise ValueError(
            f"Perturbation {perturbation_id!r} left dangling link endpoint(s) referencing removed "
            f"elements: {broken} — refusing to write a structurally broken goal model."
        )

    model.author = (
        f"EXPERIMENTAL CONSTRUCT — {kind}, perturbation_id={perturbation_id}, targets="
        f"{list(targets)}, generated from {base.source_path} (sha256={base_sha[:16]}) by "
        f"experimentation/icpm2027/goalmodel/perturb.py for Experiment 2 "
        f"(EXPERIMENTATION_PLAN.md §4). Not a frozen organizational goal model — {summary}"
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    base_stem = Path(base.source_path).stem
    output_path = out_dir / f"{base_stem}__{perturbation_id}.jucm"
    write_jucm(model, output_path)
    output_sha = _sha256_text(output_path.read_text(encoding="utf-8"))

    result = PerturbationResult(
        perturbation_id=perturbation_id,
        kind=kind,
        targets=targets,
        base_path=Path(base.source_path),
        base_sha256=base_sha,
        output_path=output_path,
        output_sha256=output_sha,
        model=model,
        notes=notes,
    )
    output_path.with_suffix(".provenance.json").write_text(
        json.dumps(result.provenance(), indent=2), encoding="utf-8"
    )
    return result


def remove_alternative(base: GRLModel, target_id: str, out_dir: Path = PERTURBED_DIR) -> PerturbationResult:
    """Perturbation A: remove one declared alternative from the model entirely.

    The measurement this enables is TargetReassignment vs. CollateralReassignment (§4): the share
    of variants originally linked to `target_id` that change category, against the share of every
    other variant that changes. A localized semantic-frame effect implies the first far exceeds
    the second — read against Task C2's replicate noise floor, never on its own.

    Removes the element itself, every Decomposition/Contribution link touching it (as source or
    destination), and drops it from its parent's children. If the parent held only two children
    under an Xor and one is removed, the parent becomes a degenerate one-child decomposition —
    flagged in `notes`, since that is a consequence of the perturbation, not an authoring choice.
    """
    parent_id = _require_declared_alternative(base, target_id)
    model = _clone(base)
    notes: list[str] = []

    removed_element = model.elements.pop(target_id)
    removed_links = [
        link for link in list(model.decompositions) + list(model.contributions)
        if link.src == target_id or link.dest == target_id
    ]
    model.decompositions = [link for link in model.decompositions if link.src != target_id and link.dest != target_id]
    model.contributions = [link for link in model.contributions if link.src != target_id and link.dest != target_id]
    notes.append(
        f"Removed element {target_id} ({removed_element.type}: {removed_element.name!r}) and "
        f"{len(removed_links)} link(s) touching it (decomposition and/or contribution)."
    )

    remaining_children = model.children_of(parent_id)
    parent = model.elements[parent_id]
    notes.append(f"{parent_id}'s children are now {remaining_children} (was including {target_id}).")
    if parent.decomposition_type in ("Or", "Xor") and len(remaining_children) == 1:
        notes.append(
            f"{parent_id} now has a single child under a {parent.decomposition_type} operator — "
            "a degenerate decomposition, a consequence of this perturbation, not an authoring "
            "choice. Report this if it affects the result."
        )

    summary = (
        f"the declared alternative {target_id} ({removed_element.name!r}) has been removed from "
        f"{parent_id}'s decomposition, together with every link touching it."
    )
    return _finalize(
        model,
        base=base,
        perturbation_id=f"pertA_remove_{target_id}",
        kind="A - alternative removal",
        targets=(target_id,),
        summary=summary,
        notes=notes,
        out_dir=out_dir,
    )


def merge_alternatives(
    base: GRLModel,
    target_ids: tuple[str, str],
    merged_name: str,
    out_dir: Path = PERTURBED_DIR,
) -> PerturbationResult:
    """Perturbation B: collapse two declared alternatives of the same parent into one.

    The merged element reuses the first-listed element's id (so anything already referencing it,
    e.g. a prior condition's `anchor_ids`, keeps resolving) with `merged_name` as its new name.
    Contribution links from both originals are unioned by target: where both contribute to the
    same softgoal with **different** qualitative values, the first-listed element's value is kept
    and the conflict is recorded in `notes` — there is no principled automatic way to combine two
    distinct GRL contribution claims (Help vs. Make to the same softgoal are different assertions),
    so the rule is applied uniformly and reported, never resolved silently.
    """
    first_id, second_id = target_ids
    parent_first = _require_declared_alternative(base, first_id)
    parent_second = _require_declared_alternative(base, second_id)
    if parent_first != parent_second:
        raise ValueError(
            f"{first_id!r} and {second_id!r} are alternatives of different parents "
            f"({parent_first} and {parent_second}) — merging them would change the decomposition's "
            "shape, not just its granularity."
        )

    model = _clone(base)
    notes: list[str] = []

    first = model.elements[first_id]
    second = model.elements.pop(second_id)
    original_first_name = first.name
    model.elements[first_id] = dataclasses.replace(first, name=merged_name)
    notes.append(f"Merged {first_id} ({original_first_name!r}) and {second_id} ({second.name!r}) into {first_id} ({merged_name!r}).")

    # Decomposition: drop the second element's own incoming link (from the shared parent);
    # nothing else references it since it was a leaf alternative, not itself decomposed further
    # here — if it had children of its own, they now dangle and _finalize()'s check catches it,
    # surfacing the case (grafting the second's children onto the merged id) as a real error to
    # decide explicitly rather than silently reparenting behavior this function wasn't asked to.
    model.decompositions = [link for link in model.decompositions if link.dest != second_id]

    first_targets = {link.dest for link in model.contributions if link.src == first_id}
    kept_contributions: list[ContributionLink] = []
    dropped_conflicts: list[str] = []
    for link in model.contributions:
        if link.src != second_id:
            kept_contributions.append(link)
            continue
        if link.dest in first_targets:
            existing = next(c for c in model.contributions if c.src == first_id and c.dest == link.dest)
            if existing.contribution != link.contribution:
                dropped_conflicts.append(
                    f"target {link.dest}: kept {first_id}'s {existing.contribution} over "
                    f"{second_id}'s {link.contribution}"
                )
            continue
        kept_contributions.append(dataclasses.replace(link, src=first_id))
    model.contributions = kept_contributions
    if dropped_conflicts:
        notes.append("Contribution conflicts resolved by keeping the first-listed element's value: " + "; ".join(dropped_conflicts))

    summary = f"the declared alternatives {first_id} and {second_id} have been merged into a single alternative {first_id} ({merged_name!r})."
    return _finalize(
        model,
        base=base,
        perturbation_id=f"pertB_merge_{first_id}_{second_id}",
        kind="B - alternative merge",
        targets=(first_id, second_id),
        summary=summary,
        notes=notes,
        out_dir=out_dir,
    )


def add_distractor(
    base: GRLModel,
    parent_id: str,
    distractor_name: str,
    out_dir: Path = PERTURBED_DIR,
) -> PerturbationResult:
    """Perturbation C: add an artificial but plausible alternative under an existing Or/Xor goal.

    The plan makes this optional and conditions it on being "specifiable prospectively and not
    tuned toward a favorable result": the caller supplies the label, and nothing here inspects any
    run output, so the specification is necessarily prospective. What is reported afterwards is
    distractor uptake, the categories variants moved from, collateral reassignment, and the change
    in residual (`analysis/perturbation.py`) — not encoded here.

    The distractor gets a fresh id (`model.new_id()`) and no contribution links: it is added as a
    pure structural alternative, not given a pre-authored stance toward any softgoal, so its
    uptake in Step 5a/6 reflects only its name and position in the decomposition, nothing else.
    """
    model = _clone(base)
    parent = model.element(parent_id)
    if parent.decomposition_type not in ("Or", "Xor"):
        raise ValueError(
            f"{parent_id!r} is decomposed with {parent.decomposition_type!r}, not Or/Xor — its "
            "children are not alternatives to add a distractor among."
        )

    distractor_id = model.new_id()
    model.elements[distractor_id] = IntentionalElement(
        id=distractor_id, name=distractor_name, type="Task", decomposition_type=None
    )
    model.decompositions.append(
        DecompositionLink(id=model.new_id(), src=parent_id, dest=distractor_id)
    )

    summary = f"an artificial alternative {distractor_id} ({distractor_name!r}) has been added under {parent_id}, with no declared organizational intent behind it."
    return _finalize(
        model,
        base=base,
        perturbation_id=f"pertC_distractor_{distractor_id}",
        kind="C - artificial plausible distractor",
        targets=(distractor_id,),
        summary=summary,
        notes=[f"Added {distractor_id} ({distractor_name!r}) as a leaf Task under {parent_id}, with no contribution links."],
        out_dir=out_dir,
    )
