"""Replication package for the ICPM 2027 submission — every run behind the paper's reported
results (RQ1's paired intent-guided/open protocol across RTFM, Sepsis, and BPIC 2019, plus the
RTFM goal-model perturbations), as opposed to the illustrative case studies under
experimentation.examples.

The frozen protocol's machinery is implemented — see this package's own README.md for the
module-by-module inventory (protocol/condition execution, manifests, freeze verification, Task C3's
structural-clustering baseline, Experiment 2's GRL perturbations, coverage/contingency analysis)
and for what is still open (a single per-dataset run driver, Task C4's rule-based baseline, Task
C1's BPIC 2019 held-out validation, and chaining Experiment 2's TargetReassignment/
CollateralReassignment measurement end to end). Nothing here has executed a real frozen run yet —
`configs/preregistration.yaml`'s open decisions (Task C7, C10, C5, C6, D6) must be resolved first.
"""
