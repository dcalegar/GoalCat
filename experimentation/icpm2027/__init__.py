"""Replication package for the ICPM 2027 submission — every run behind the paper's reported
results (RQ1's paired intent-guided/open protocol across RTFM, Sepsis, and BPIC 2019, plus the
RTFM goal-model perturbations), as opposed to the illustrative case studies under
experimentation.examples.

Scaffold only: this package fills in as the frozen experimental protocol lands (see
EXPERIMENTATION_PLAN.md in the paper repository). Each dataset's paired guided/open runs should
land in their own subdirectory here (e.g. icpm2027/rtfm/, icpm2027/sepsis/, icpm2027/bpic2019/),
mirroring experimentation.examples' one-subdirectory-per-log convention, plus whatever
cross-dataset analysis (contingency matrices, coverage comparison) the protocol calls for.
"""
