# References (English index)

Background and sources for gmnsopt. Full BibTeX in [`references.bib`](references.bib).

## Data standard & benchmark networks
- **GMNS** — General Modeling Network Specification. https://github.com/zephyr-data-specs/GMNS ·
  docs: https://zephyr-data-specs.github.io/GMNS/
- **Transportation Networks for Research** (Sioux Falls, Anaheim, Chicago Sketch/Regional, Winnipeg, …).
  https://github.com/bstabler/TransportationNetworks
- Sioux Falls — LeBlanc, Morlok & Pierskalla (1975), *Transportation Research* 9(5).
- "Rethinking the Sioux Falls Network" (benchmark fidelity) — arXiv:2508.06234.

## Solver benchmark discipline
- **MIPLIB 2017** — Mixed Integer Programming Library (1,065 instances; 240 benchmark set). https://miplib.zib.de/
- Industrial-scale / natural-language-to-optimization modeling benchmark (MIPLIB-NL) — arXiv:2602.10450.

## Open-source & GPU solvers (Tier 0–3)
- **COIN-OR** https://www.coin-or.org/ · **HiGHS** https://highs.dev/ · **OR-Tools**
  https://developers.google.com/optimization/ · **Ipopt** https://www.coin-or.org/projects/ ·
  **NVIDIA cuOpt** https://www.nvidia.com/en-us/ai-data-science/products/cuopt/

## ML-for-optimization
- ML-augmented branch-and-bound for MILP (survey) — *Mathematical Programming* (2024),
  https://link.springer.com/article/10.1007/s10107-024-02130-y
- Learning to Branch in Mixed Integer Programming — AAAI,
  https://cdn.aaai.org/ojs/10080/10080-13-13608-1-2-20201228.pdf

## Teaching backbone (bundled)
- **`建模与规划教材.zip`** — a mathematical-modeling and mathematical-programming textbook (TeX/PDF), used as
  the teaching backbone (foundations → modeling tricks → practical cases → solver implementation → debugging /
  IIS / tuning / callbacks). See [`../dev/book_to_gmns_mapping.md`](../dev/book_to_gmns_mapping.md) for how its
  chapters map onto GMNS-native transportation cases.

> Bundled benchmark networks keep their upstream licenses/terms; cite the original sources above when using them.
