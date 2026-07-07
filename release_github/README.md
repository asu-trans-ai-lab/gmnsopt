# gmnsopt

[![CI](https://github.com/asu-trans-ai-lab/gmnsopt/actions/workflows/ci.yml/badge.svg)](https://github.com/asu-trans-ai-lab/gmnsopt/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/gmnsopt.svg)](https://pypi.org/project/gmnsopt/)
[![Python](https://img.shields.io/pypi/pyversions/gmnsopt.svg)](https://pypi.org/project/gmnsopt/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**A GMNS-native transportation optimization testbed** — reproducible, visual, data-grounded, and
progressively harder. It turns standardized [GMNS](https://github.com/zephyr-data-specs/GMNS) networks +
demand + operations data into mathematical-programming and network-optimization cases:

```
GMNS network + demand + operations data
  → optimization model template
  → solver / algorithm
  → (dynamic simulation check)
  → GUI4GMNS visualization
  → reproducible benchmark report
```

> **gmnsopt turns GMNS from a network data standard into a transportation optimization testbed
> for planning, operations, control, pricing, resilience, and multimodal decision-making** — where
> open-source solvers, commercial solvers, ML-for-optimization, and RL/control methods can all be tested on
> realistic, dynamic, stochastic, visually explainable mobility problems.

## What ships in v0.1 (working, dependency-light)
Core kernel + **ten runnable cases** across the model families and formulation classes (LP / MILP / convex-NLP
/ inverse), on the common **case contract** (`problem.yml` + GMNS `input/` → `output/solution.csv`,
`objective_trace.csv`, `constraint_status.csv`, `summary.md`):

| model | family | class | case | solver |
|---|---|---|---|---|
| `shortest_path` | A routing | LP | `cases/00_shortest_path_toy` | networkx Dijkstra |
| `min_cost_flow` | flow | LP | `cases/01_min_cost_flow_toy` | networkx |
| `traffic_assignment` (UE) | B assignment | convex-NLP | `cases/02_sioux_falls_assignment` | Frank-Wolfe + BPR |
| `system_optimal` (+ pricing) | B assignment | convex-NLP | `cases/03_system_optimal_pricing` | Frank-Wolfe (marginal cost) |
| `accessibility` | A routing | LP | `cases/04_accessibility` | networkx skims |
| `max_flow` (min-cut) | F resilience | LP | `cases/05_max_flow_evacuation` | networkx max-flow |
| `odme` (inverse) | C ODME | QP/NNLS | `cases/06_odme_sioux_falls` | scipy NNLS |
| `signal_timing` | D operations | LP | `cases/07_signal_timing_intersection` | scipy linprog (HiGHS) |
| `network_design` | E design | **MILP** | `cases/08_network_design_toy` | **scipy milp (HiGHS)** |
| `facility_location` (EV charging) | G siting | **MILP** | `cases/09_facility_location_charging` | **scipy milp (HiGHS)** |

Verified invariants: system-optimal total travel time **<** user-equilibrium; ODME count-RMSE 2720 → 185;
MILP network design respects the budget; p-median opens exactly K hubs. Only `numpy`, `scipy`, `networkx`,
`PyYAML` are required (MILP/LP use scipy's HiGHS backend — **no commercial solver needed**). Optional extras
add Pyomo/HiGHS bindings, pandas/matplotlib.

## Install
```bash
pip install -e .            # core
pip install -e ".[viz,solvers,dev]"   # + pandas/matplotlib, Pyomo/HiGHS, pytest/ruff
```

## Quick start
```bash
gmns-opt run      cases/02_sioux_falls_assignment      # -> output/ (solution, trace, summary)
gmns-opt validate cases/02_sioux_falls_assignment
gmns-opt list-families                                 # the 10-family taxonomy (maturity + classes)
gmns-opt describe-family signal_queue_control
gmns-opt solver-status                                 # available solver tiers
gmns-opt generate-scenarios --case cases/11_resilience_capacity_drop_toy --type capacity_drop --links 1,2,3 --drop 0.5
```

## Broader benchmark scaffold
Beyond the runnable models, the package is an open-science **ecosystem scaffold**:
- **Application taxonomy** — 10 families (`gmns_opt.applications` / `benchmark.registry`), each with formulation
  classes, required/optional GMNS files, outputs, solver tier, visualization, and **maturity**
  (runnable / scaffold / planned). See [docs/application_taxonomy.md](docs/application_taxonomy.md).
- **Tensor framework** — `gmns_opt.tensor`: sparse `x[o,d,m,p,τ,s,a]` + companion tensors (D/F/Q/U/C/R/V),
  GMNS→demand-tensor conversion, scenario expansion, CSV/JSON export. See [docs/tensor_framework.md](docs/tensor_framework.md).
- **Scenario generator** — `gmns_opt.scenarios`: deterministic normal / capacity_drop / demand_surge / work_zone
  / weather / cav_penetration / uam_weather_restriction (fixed seeds).
- **Solver tiers** — `gmns_opt.solvers`: Tier 0 (networkx/scipy-HiGHS) → 1 (Pyomo) → 2 (commercial, optional) →
  3 (GPU/neural/RL). No commercial dependency. See [docs/solver_tiers.md](docs/solver_tiers.md).
- **ML-for-optimization readiness** — `gmns_opt.ml`: GMNS feature extraction (GNN-ready), learning-to-warm-start
  interface, learning-to-branch dataset schema. See [docs/ml_for_optimization.md](docs/ml_for_optimization.md).
- **GUI4GMNS visualization** — `gmns_opt.visualization.export_optimization_layers` → GeoJSON + decision/constraint/
  trace/scenario CSVs. See [docs/gui4gmns_integration.md](docs/gui4gmns_integration.md).
- **Case templates** — `case_templates/` (one per family) and 13 runnable/scaffold seed cases (`cases/00..12`).
```python
from gmns_opt import run_case
res = run_case("cases/02_sioux_falls_assignment")
print(res["objective"], res["meta"]["final_relative_gap"])   # UE Beckmann + FW gap
```

## The benchmark ladder (design)
Not one benchmark — a **ladder** from transparent teaching cases to industrial-scale city cases:

| level | what | purpose |
|---|---|---|
| 0 | formulation micro-cases (5–20 nodes, 1 signal) | teach variables/constraints; debug solvers; validate LLM-generated models |
| 1 | classic research nets **as GMNS** (Sioux Falls, Anaheim, Chicago) | connect to the literature; algorithm comparison |
| 2 | open-city OSM2GMNS (Tempe, Phoenix, Atlanta, LA, Bay Area) | geographically meaningful; GIS/planning + GUI4GMNS outreach |
| 3 | dynamic corridor operations (signals, queues, work zones, incidents) | planning → operations (DTA/CBI/ODME) |
| 4 | stochastic / robust (demand, capacity, incident, weather, CAV/UAM uncertainty) | research-grade OR/AI |
| 5 | industrial-scale city (10⁴–10⁶ vars, multi-mode/period/scenario) | stress solvers + neural acceleration |

## Model families (implemented → planned)
A. shortest path / accessibility ✅ · B. traffic assignment & system-optimal ✅ (UE) · C. **ODME / inverse
optimization** · D. signal timing & arterial control (MILP/MPC) · E. network design & capacity planning ·
F. resilience / work-zone / incident / extreme-heat · G. freight / EV charging / UAM / multimodal logistics ·
H. transit frequency & accessibility. See [docs/BENCHMARK_SPEC.md](docs/BENCHMARK_SPEC.md).

## Solver tiers
`Tier 0` NetworkX / scipy / HiGHS / OR-Tools · `Tier 1` Pyomo + HiGHS/CBC/Ipopt · `Tier 2` Gurobi / CPLEX /
COPT / Mosek · `Tier 3` GPU / cuOpt / ADMM / RL / neural heuristics. Start license-free; scale up when needed.

## Docs
[vision](docs/vision.md) · [application taxonomy](docs/application_taxonomy.md) ·
[tensor framework](docs/tensor_framework.md) · [benchmark ladder](docs/benchmark_ladder.md) ·
[solver tiers](docs/solver_tiers.md) · [ML for optimization](docs/ml_for_optimization.md) ·
[GUI4GMNS integration](docs/gui4gmns_integration.md) · [open-science test cases](docs/open_science_test_cases.md) ·
[benchmark spec](docs/BENCHMARK_SPEC.md) · [data contract](docs/data_contract.md) ·
[roadmap](../dev/ROADMAP.md) · [references](../references/README.md)

## License
MIT — see [LICENSE](LICENSE). Bundled benchmark networks keep their own upstream licenses
(see [references](../references/README.md)); Sioux Falls is from the public Transportation Networks repo.
