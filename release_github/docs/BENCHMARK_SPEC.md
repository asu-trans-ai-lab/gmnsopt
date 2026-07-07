# gmns4optimization — open-science benchmark spec

Every case is **both a mathematical optimization problem and a visual transportation scenario**. The spec
borrows MIPLIB-style discipline (solver-readable, standardized, benchmarkable) and adds transportation
semantics (OD, modes, paths, time, queues, signals, incidents, scenarios, equity).

## Case folder standard
```
case_name/
  problem.yml            # machine-readable case definition (type, params, objective, solver, viz)
  README.md              # human-readable problem statement
  formulation.md         # the exact mathematical formulation
  input/                 # GMNS data contract (required)
    node.csv  link.csv  demand.csv  [settings.yml]
  optional_input/        # movement, signal_timing, detector, transit_route, vehicle,
                         # charging_station, vertiport, scenario, project, constraint  (as needed)
  models/                # solver-ready model files (model.lp / model.mps / model.py) [optional]
  baselines/             # per-solver baseline solutions (highs/ ortools/ gurobi/ copt/ neural/) [optional]
  output/                # produced by `gmns-opt run`
    solution.csv  objective_trace.csv  constraint_status.csv  summary.md  [gui4gmns_dashboard.html]
```

### The five output files that make it multi-community
| file | columns | who uses it |
|---|---|---|
| `solution.csv` / `decision_variable.csv` | link/path/decision values | transportation + viz |
| `objective_trace.csv` | `iteration, objective, gap, [tstt, runtime]` | solver + ML (convergence) |
| `constraint_status.csv` | `constraint, status, [slack, dual, binding]` | feasibility / diagnosis |
| `solver_log.txt` | raw solver output | solver developers |
| `simulation_check.csv` | re-simulated KPIs vs optimized | transportation validation |

## `problem.yml` schema (minimum)
```yaml
problem_name: corridor_signal_control
problem_type: traffic_assignment        # one of the registered model templates
network_format: gmns
level: 3                                 # 0..5 ladder level
formulation_class: [MILP, dynamic]       # LP | MIP | QP | NLP | stochastic | dynamic | RL
params: { max_iter: 80, gap_tol: 0.0001, by_zone: true }
objective: { primary: minimize_total_delay, secondary: minimize_queue_spillback }
constraints: [flow_conservation, link_capacity, signal_min_green, queue_storage]
solver: { default: frank_wolfe, optional: [gurobi, copt, ortools] }
visualization: { gui4gmns: true, export_3d: true }
```

## Benchmark ladder (levels 0–5)
0 formulation micro · 1 classic-as-GMNS · 2 open-city OSM2GMNS · 3 dynamic corridor operations ·
4 stochastic/robust · 5 industrial-scale city. Release **both** small transparent cases **and** large
realistic cases.

## Formulation-class matrix (tag every case)
| case | LP | MIP | QP | NLP | Stoch | Dyn | RL | NN/solver-learning |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|---|
| shortest path | ✓ | | | | | | | warm start |
| min-cost flow | ✓ | | | | | | | decomposition |
| traffic assignment | | | ✓ | ✓ | ✓ | ✓ | | surrogate |
| signal control | | ✓ | | | ✓ | ✓ | ✓ | learn-to-branch |
| ODME (inverse) | ✓ | | ✓ | ✓ | ✓ | ✓ | | tensor learning |
| pricing | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | policy learning |
| work zone / resilience | | ✓ | | | ✓ | ✓ | ✓ | branching/warm start |
| CAV control | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | value function |
| UAM dispatch | | ✓ | | | ✓ | ✓ | ✓ | neural dispatch |
| EV freight routing | | ✓ | | | ✓ | ✓ | ✓ | neural routing |

## Flagship cases (roadmap IDs)
- `GMNS-SP-101` shortest path & accessibility — **implemented** (`00_shortest_path_toy`)
- `GMNS-DTA-201` dynamic assignment & pricing — UE implemented (`02_sioux_falls_assignment`); dynamic/pricing next
- `GMNS-ODME-301` inverse demand estimation (sensor/probe fusion)
- `GMNS-SIGNAL-401` signal & queue-spillback control (MILP/MPC/RL)
- `GMNS-RESILIENCE-501` incident / heat / work-zone response (stochastic robust, CVaR)
- `GMNS-CAV-UAM-601` multimodal autonomous mobility control (RL + optimization, 3D viz)

## The tensor view (intellectual center)
Do not flatten to `min cᵀx`. Preserve the transportation decision tensor
`x[o, d, m, p, τ, s, a]` (origin, destination, mode, path/policy, time-stage, scenario, action) with
companion tensors `D` (demand), `F` (flow), `Q` (queue), `U` (control), `C` (capacity), `R` (reward),
`V` (value). This connects dynamic programming, stochastic/robust programming, RL, tensor compression, and
learning-to-branch on one shared data contract.
