"""Zero-LLM-cost baselines the paired guided/open comparison is measured against.

- `structural_clustering.py` (Task C3): the boolean activity-vector + HDBSCAN representation
  Amling et al. (2025) uses — "the one baseline the Related Work section argues against but the
  current design never runs" (EXPERIMENTATION_PLAN.md §2.3). No LLM call; runs directly against a
  dataset's shared Steps 1-4 base (`experimentation/icpm2027/inputs.py`).
- `rule_based_rtfm.py` (Task C4): a terminal-activity rule reproducing RTFM's five declared
  categories {TP, TA, TB, TC, TD} without any model, the plan's secondary RTFM-only comparison.
"""
