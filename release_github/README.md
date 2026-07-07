# gmns4optimization

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

> **gmns4optimization turns GMNS from a network data standard into a transportation optimization testbed
> for planning, operations, control, pricing, resilience, and multimodal decision-making** — where
> open-source solvers, commercial solvers, ML-for-optimization, and RL/control methods can all be tested on
> realistic, dynamic, stochastic, visually explainable mobility problems.

## What ships in v0.1 (working, dependency-light)
Core kernel + three runnable cases on the common **case contract** (`problem.yml` + GMNS `input/` →
`output/solution.csv`, `objective_trace.csv`, `constraint_status.csv`, `summary.md`):

| model | case | solver |
|---|---|---|
| `shortest_path` | `cases/00_shortest_path_toy` | networkx Dijkstra |
| `min_cost_flow` | `cases/01_min_cost_flow_toy` | networkx min-cost-flow |
| `traffic_assignment` (UE, Frank-Wolfe + BPR) | `cases/02_sioux_falls_assignment` | Frank-Wolfe (built-in) |

Only `numpy`, `scipy`, `networkx`, `PyYAML` are required. Optional extras add Pyomo/HiGHS, pandas/matplotlib.

## Install
```bash
pip install -e .            # core
pip install -e ".[viz,solvers,dev]"   # + pandas/matplotlib, Pyomo/HiGHS, pytest/ruff
```

## Quick start
```bash
gmns-opt validate cases/02_sioux_falls_assignment
gmns-opt run      cases/02_sioux_falls_assignment      # -> output/ (solution, trace, summary)
```
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
[benchmark spec](docs/BENCHMARK_SPEC.md) · [data contract](docs/data_contract.md) ·
[tutorial ladder](docs/tutorial_ladder.md) · [positioning](docs/positioning.md) ·
[roadmap](../dev/ROADMAP.md) · [references](../references/README.md)

## License
MIT — see [LICENSE](LICENSE). Bundled benchmark networks keep their own upstream licenses
(see [references](../references/README.md)); Sioux Falls is from the public Transportation Networks repo.
