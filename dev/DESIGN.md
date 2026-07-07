# Design notes (dev)

## Architecture
```
gmns_opt/
  io/         read_gmns, validate_gmns, build_graph        (GMNS -> structures/graph)
  models/     shortest_path, min_cost_flow, traffic_assignment, ... (model templates)
  solvers/    tiered registry (networkx/scipy -> Pyomo/HiGHS -> Gurobi/COPT -> GPU/RL)
  benchmark/  run_case (problem.yml dispatch), report (standard output set)
  viz/        GeoJSON export -> GUI4GMNS / kepler.gl / Leaflet
  cli         gmns-opt run|validate
```
Design rules: (1) every case obeys the same **data contract** (GMNS in, standard out); (2) core stays
dependency-light (numpy/scipy/networkx/pyyaml) so it runs license-free; (3) heavier solvers/ML are optional
extras; (4) every model emits `objective_trace` + `constraint_status` so solver, ML, and transportation users
can each read the same case.

## The tensor benchmark (intellectual center)
Preserve `x[o,d,m,p,τ,s,a]` instead of flattening to `min cᵀx`. Companion tensors: `D` demand, `F` flow,
`Q` queue, `U` control, `C` capacity, `R` reward, `V` value. This connects DP, stochastic/robust programming,
RL, tensor compression/low-rank, learning-to-branch, and simulation-based optimization on one contract.

## Adding a model template
1. `models/<name>.py` returning `{objective, solution, objective_trace, constraint_status, meta}`.
2. Register in `models/__init__.py` and `benchmark/case.py:DISPATCH`.
3. Add a case folder with `problem.yml` (`problem_type: <name>`), `README.md`, `formulation.md`, `input/`.
4. Add a test in `tests/`.

## MIPLIB discipline, transportation semantics
Borrow MIPLIB's standardization (solver-readable, benchmarkable) but keep OD/mode/path/time/queue/signal/
scenario/equity meaning. Each instance is simultaneously a math program and a visual transportation scenario.
