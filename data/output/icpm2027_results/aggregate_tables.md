# Aggregated multi-replicate tables (setup and divergence)

Recomputed from the frozen run directories by `experimentation/icpm2027/analysis/aggregate_tables.py`; no LLM call is made. Ranges are min--max over the replicates (or replicate pairs) that executed and are descriptive: within-arm pairs share replicates and are not independent, and a min--max range widens with the number of draws, so ranges over unequal $n$ are not directly comparable.

## Setup — categories and residual, per arm

| Log | Axis | Arm | Variants | Cases | \|T\| | n | Residual (var.) | Residual (cases) |
|---|---|---|---:|---:|---:|---:|---|---|
| RTFM | resolution | `guided` | 231 | 150370 | 5 | 5 | 2.8% [0.9--7.4] | 13.8% |
| RTFM | resolution | `open` | 231 | 150370 | NOT INVARIANT (|T| in RTFM/resolution/open: [4, 5]) | 5 | 1.6% [0.9--2.6] | 13.8% |
| RTFM | resolution | `guided_no_sample` | 231 | 150370 | 5 | 2 | 3.7% [2.2--5.2] | 13.8% |
| RTFM | resolution | `label_list` | 231 | 150370 | 5 | 2 | 1.3% [0.0--2.6] | 0.0% |
| RTFM | resolution | `label_list_strict` | 231 | 150370 | 5 | 2 | 0.2% [0.0--0.4] | 0.0% |
| Sepsis | admission | `guided` | 846 | 1050 | 2 | 5 | 10.4% | 22.9% |
| Sepsis | admission | `open` | 846 | 1050 | 4 | 5 | 1.1% [0.2--2.1] | 0.9% [0.2--1.7] |
| Sepsis | admission | `guided_no_sample` | 846 | 1050 | 2 | 2 | 10.4% | 22.9% |
| Sepsis | admission | `label_list` | 846 | 1050 | 5 | 2 | 7.4% [7.3--7.6] | 20.4% [20.2--20.6] |
| Sepsis | admission | `label_list_strict` | 846 | 1050 | 5 | 2 | 7.0% [6.6--7.3] | 19.8% [19.7--19.9] |
| Sepsis | discharge | `guided` | 846 | 1050 | 5 | 5 | 18.2% [17.1--21.0] | 29.6% [28.6--32.1] |
| Sepsis | discharge | `open` | 846 | 1050 | 4 | 5 | 1.1% [0.2--2.1] | 0.9% [0.2--1.7] |
| Sepsis | discharge | `guided_no_sample` | 846 | 1050 | 5 | 2 | 18.4% [16.5--20.3] | 29.6% [28.1--31.1] |
| Sepsis | discharge | `label_list` | 846 | 1050 | 5 | 2 | 7.4% [7.3--7.6] | 20.4% [20.2--20.6] |
| Sepsis | discharge | `label_list_strict` | 846 | 1050 | 5 | 2 | 7.0% [6.6--7.3] | 19.8% [19.7--19.9] |
| BPIC 2019 | matching regime | `guided` | 11973 | 251734 | 4 | 3 | 20.7% [19.3--21.6] | 16.3% [16.0--16.8] |
| BPIC 2019 | matching regime | `open` | 11973 | 251734 | 5 | 3 | 23.6% [2.3--57.8] | 9.1% [1.1--23.0] |
| BPIC 2019 | matching regime | `guided_no_sample` | 11973 | 251734 | 4 | 2 | 22.6% [22.6--22.7] | 17.4% [17.2--17.6] |
| BPIC 2019 | matching regime | `label_list` | 11973 | 251734 | 4 | 2 | 17.9% [17.8--18.0] | 18.6% [17.7--19.6] |
| BPIC 2019 | matching regime | `label_list_strict` | 11973 | 251734 | 4 | 2 | 18.0% [17.6--18.4] | 18.9% [18.1--19.8] |

## Divergence — AMI, residual as its own block

### Variant-weighted

| Log | Axis | guided--guided | open--open | guided vs. open | guided vs. no-sample | no-sample--no-sample | guided vs. label-list | label-list--label-list | label-list vs. open | guided vs. label-list-strict | label-list-strict--label-list-strict | label-list vs. label-list-strict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RTFM | resolution | 0.58 [0.49--0.69] (n=10) | 0.50 [0.42--0.65] (n=10) | 0.26 [0.15--0.46] (n=25) | 0.50 [0.38--0.65] (n=10) | 0.61 (n=1) | 0.39 [0.28--0.43] (n=10) | 0.91 (n=1) | 0.37 [0.29--0.49] (n=10) | 0.40 [0.29--0.46] (n=10) | 0.73 (n=1) | 0.78 [0.76--0.81] (n=4) |
| Sepsis | admission | 0.88 [0.84--0.92] (n=10) | 0.51 [0.43--0.56] (n=10) | 0.30 [0.27--0.32] (n=25) | 0.87 [0.84--0.91] (n=10) | 0.88 (n=1) | 0.35 [0.33--0.38] (n=10) | 0.65 (n=1) | 0.39 [0.33--0.50] (n=10) | 0.39 [0.38--0.41] (n=10) | 0.68 (n=1) | 0.61 [0.54--0.64] (n=4) |
| Sepsis | discharge | 0.76 [0.68--0.86] (n=10) | 0.51 [0.43--0.56] (n=10) | 0.25 [0.21--0.32] (n=25) | 0.79 [0.64--0.93] (n=10) | 0.80 (n=1) | 0.22 [0.20--0.23] (n=10) | 0.65 (n=1) | 0.39 [0.33--0.50] (n=10) | 0.24 [0.21--0.26] (n=10) | 0.68 (n=1) | 0.61 [0.54--0.64] (n=4) |
| BPIC 2019 | matching regime | 0.51 [0.48--0.54] (n=3) | 0.40 [0.36--0.43] (n=3) | 0.17 [0.17--0.18] (n=9) | 0.51 [0.48--0.55] (n=6) | 0.50 (n=1) | 0.16 [0.15--0.17] (n=6) | 0.48 (n=1) | 0.15 [0.14--0.16] (n=6) | 0.17 [0.16--0.18] (n=6) | 0.49 (n=1) | 0.43 [0.43--0.45] (n=4) |

### Case-weighted

| Log | Axis | guided--guided | open--open | guided vs. open | guided vs. no-sample | no-sample--no-sample | guided vs. label-list | label-list--label-list | label-list vs. open | guided vs. label-list-strict | label-list-strict--label-list-strict | label-list vs. label-list-strict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RTFM | resolution | 0.99 [0.98--1.00] (n=10) | 0.93 [0.87--1.00] (n=10) | 0.91 [0.87--0.96] (n=25) | 0.99 [0.98--0.99] (n=10) | 0.99 (n=1) | 0.88 [0.87--0.89] (n=10) | 1.00 (n=1) | 0.87 [0.83--0.91] (n=10) | 0.88 [0.86--0.88] (n=10) | 0.98 (n=1) | 0.99 [0.98--1.00] (n=4) |
| Sepsis | admission | 0.92 [0.89--0.94] (n=10) | 0.61 [0.55--0.66] (n=10) | 0.44 [0.40--0.46] (n=25) | 0.92 [0.90--0.94] (n=10) | 0.92 (n=1) | 0.44 [0.43--0.46] (n=10) | 0.70 (n=1) | 0.44 [0.39--0.54] (n=10) | 0.50 [0.49--0.51] (n=10) | 0.71 (n=1) | 0.64 [0.58--0.68] (n=4) |
| Sepsis | discharge | 0.79 [0.72--0.88] (n=10) | 0.61 [0.55--0.66] (n=10) | 0.36 [0.30--0.43] (n=25) | 0.82 [0.69--0.93] (n=10) | 0.83 (n=1) | 0.31 [0.29--0.33] (n=10) | 0.70 (n=1) | 0.44 [0.39--0.54] (n=10) | 0.35 [0.32--0.37] (n=10) | 0.71 (n=1) | 0.64 [0.58--0.68] (n=4) |
| BPIC 2019 | matching regime | 0.69 [0.61--0.83] (n=3) | 0.54 [0.45--0.70] (n=3) | 0.40 [0.27--0.49] (n=9) | 0.72 [0.60--0.82] (n=6) | 0.76 (n=1) | 0.31 [0.28--0.33] (n=6) | 0.84 (n=1) | 0.30 [0.25--0.36] (n=6) | 0.30 [0.28--0.33] (n=6) | 0.84 (n=1) | 0.82 [0.80--0.84] (n=4) |

