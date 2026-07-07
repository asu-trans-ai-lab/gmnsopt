# gmnsopt

Workspace for **gmnsopt** — a GMNS-native transportation optimization testbed.

```
gmnsopt/
  release_github/   ← the shippable, pip-installable package (open source, English)
  dev/              ← development roadmap, design, teaching-backbone mapping (English)
  references/       ← sources, BibTeX, and the teaching textbook (zip)
```

- **Ship it:** everything in [`release_github/`](release_github/) is the public package (`pip install -e .`,
  `gmns-opt run cases/02_sioux_falls_assignment`). See [`release_github/README.md`](release_github/README.md).
- **Plan it:** [`dev/ROADMAP.md`](dev/ROADMAP.md) (model families, benchmark ladder L0–L5, flagship cases,
  solver tiers, ML plan) and [`dev/DESIGN.md`](dev/DESIGN.md).
- **Cite it:** [`references/README.md`](references/README.md).

v0.1 ships a working kernel + three cases (shortest path, min-cost flow, Sioux Falls user-equilibrium
assignment) on a common case contract, with the roadmap toward ODME, signal control, resilience, freight/EV/UAM,
and stochastic/robust benchmarks for solvers, ML-for-optimization, and RL/control.
