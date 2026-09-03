# Aggregated multi-replicate tables (setup and divergence)

Recomputed from the frozen run directories by `experimentation/icpm2027/analysis/aggregate_tables.py`; no LLM call is made. Ranges are min--max over the replicates (or replicate pairs) that executed and are descriptive: within-arm pairs share replicates and are not independent, and a min--max range widens with the number of draws, so ranges over unequal $n$ are not directly comparable.

## Setup — categories and residual, per arm

| Log | Axis | Arm | Variants | Cases | \|T\| | n | Residual (var.) | Residual (cases) |
|---|---|---|---:|---:|---:|---:|---|---|
| RTFM | resolution | `guided` | 231 | 150370 | 5 | 5 | 1.9% [0.4--3.5] | 13.8% [13.6--13.9] |
| RTFM | resolution | `open` | 231 | 150370 | NOT INVARIANT (|T| in RTFM/resolution/open: [4, 5]) | 2 | 2.6% [1.3--3.9] | 13.8% [13.6--14.0] |
| RTFM | resolution | `guided_no_sample` | 231 | 150370 | 5 | 2 | 1.7% | 13.8% |
| Sepsis | admission | `guided` | 846 | 1050 | 2 | 5 | 10.4% | 22.9% |
| Sepsis | admission | `open` | 846 | 1050 | 4 | 2 | 0.9% [0.6--1.3] | 0.8% [0.5--1.0] |
| Sepsis | admission | `guided_no_sample` | 846 | 1050 | 2 | 2 | 10.4% | 22.9% |
| Sepsis | discharge | `guided` | 846 | 1050 | 5 | 5 | 20.4% [18.4--24.9] | 31.3% [29.6--35.2] |
| Sepsis | discharge | `open` | 846 | 1050 | 4 | 2 | 0.9% [0.6--1.3] | 0.8% [0.5--1.0] |
| Sepsis | discharge | `guided_no_sample` | 846 | 1050 | 5 | 2 | 16.7% [13.4--20.0] | 28.2% [25.5--30.9] |
| BPIC 2019 | matching regime | `guided` | 11973 | 251734 | 4 | 2 | 21.8% [21.6--22.0] | 17.1% [17.1--17.2] |
| BPIC 2019 | matching regime | `open` | 11973 | 251734 | 5 | 2 | 9.3% [6.4--12.1] | 4.9% [0.7--9.1] |
| BPIC 2019 | matching regime | `guided_no_sample` | 11973 | 251734 | 4 | 2 | 22.6% [22.6--22.7] | 17.4% [17.2--17.6] |

## Divergence — AMI, residual as its own block

### Variant-weighted

| Log | Axis | guided--guided | open--open | guided vs. open | guided vs. no-sample | no-sample--no-sample |
|---|---|---|---|---|---|---|
| RTFM | resolution | 0.67 [0.50--0.81] (n=10) | 0.50 (n=1) | 0.36 [0.29--0.45] (n=10) | 0.67 [0.55--0.76] (n=10) | 0.72 (n=1) |
| Sepsis | admission | 0.83 [0.77--0.89] (n=10) | 0.55 (n=1) | 0.27 (n=10) | 0.82 [0.76--0.88] (n=10) | 0.78 (n=1) |
| Sepsis | discharge | 0.79 [0.71--0.92] (n=10) | 0.55 (n=1) | 0.21 [0.18--0.23] (n=10) | 0.82 [0.73--0.98] (n=10) | 0.80 (n=1) |
| BPIC 2019 | matching regime | 0.50 (n=1) | 0.46 (n=1) | 0.19 (n=4) | 0.51 [0.50--0.52] (n=4) | 0.50 (n=1) |

### Case-weighted

| Log | Axis | guided--guided | open--open | guided vs. open | guided vs. no-sample | no-sample--no-sample |
|---|---|---|---|---|---|---|
| RTFM | resolution | 0.99 [0.98--1.00] (n=10) | 0.88 (n=1) | 0.92 [0.87--0.98] (n=10) | 0.99 [0.98--1.00] (n=10) | 1.00 (n=1) |
| Sepsis | admission | 0.89 [0.85--0.93] (n=10) | 0.62 (n=1) | 0.40 (n=10) | 0.88 [0.84--0.92] (n=10) | 0.86 (n=1) |
| Sepsis | discharge | 0.81 [0.74--0.93] (n=10) | 0.62 (n=1) | 0.31 [0.27--0.33] (n=10) | 0.84 [0.75--0.98] (n=10) | 0.83 (n=1) |
| BPIC 2019 | matching regime | 0.69 (n=1) | 0.64 (n=1) | 0.45 [0.39--0.50] (n=4) | 0.70 [0.63--0.79] (n=4) | 0.76 (n=1) |

