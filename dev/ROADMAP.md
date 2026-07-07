# gmnsopt — development roadmap

Goal: an open GMNS-native benchmark ecosystem where **open-source solvers, commercial solvers, ML-for-
optimization, RL/control, and transportation researchers** test algorithms on realistic, dynamic, stochastic,
visually explainable mobility problems. (English only.)

## Model / application families (implement in this order)
| # | family | status | key formulation |
|---|---|---|---|
| A | shortest path / accessibility | ✅ v0.1 | LP / Dijkstra |
| B | traffic assignment & system-optimal | ✅ v0.1 (UE) | convex NLP / Frank-Wolfe → add SO, multiclass, pricing |
| C | **ODME / inverse optimization** (counts, speeds, probes, OD prior) | next | LP/QP/NLP; ties to the lab's bounded + observability ODME |
| D | signal timing & arterial control | planned | MILP (Big-M) / MPC / RL; green split, offset, cycle, queue storage |
| E | network design & capacity planning | planned | MIP; add lane / project selection under budget/equity |
| F | resilience: work-zone / incident / heat / evacuation | planned | stochastic robust, CVaR; capacity[link,time,scenario] |
| G | freight / EV charging / UAM / multimodal logistics | planned | VRP / EVRPTW / pickup-delivery (OR-Tools, cuOpt) |
| H | transit frequency, fleet, accessibility/equity | planned | MIP; frequency, fleet, first/last-mile |

## Benchmark ladder (release both small + large)
- **L0** formulation micro-cases (5–20 nodes, 1 signal) — teach, debug, validate LLM-generated formulations
- **L1** classic research nets as GMNS — Sioux Falls ✅, Anaheim, Chicago Sketch/Regional, Eastern Mass, Winnipeg
- **L2** open-city OSM2GMNS — Tempe, Phoenix subarea, Atlanta, Chicago, LA/SCAG corridor, Bay Area
- **L3** dynamic corridor operations — signals, queues, work zones, incidents, transit priority (DTA/CBI/ODME)
- **L4** stochastic scenarios — normal/rain/heat/incident/event, CAV & UAM & probe uncertainty (robust, CVaR, RL)
- **L5** industrial-scale city — 10⁴–10⁶ vars, multi-mode/period/scenario, solver logs, warm starts, dashboards

## Flagship cases (research IDs)
`GMNS-SP-101` ✅ · `GMNS-DTA-201` (UE done; dynamic+pricing next) · `GMNS-ODME-301` · `GMNS-SIGNAL-401` ·
`GMNS-RESILIENCE-501` · `GMNS-CAV-UAM-601`.

## Solver tiers
`T0` NetworkX/scipy/HiGHS/OR-Tools · `T1` Pyomo + HiGHS/CBC/Ipopt · `T2` Gurobi/CPLEX/COPT/Mosek ·
`T3` GPU/cuOpt/ADMM/RL/neural. Package must run license-free by default.

## ML-for-optimization (benchmark against exact/heuristic baselines; always feasibility-check)
learning-to-warm-start (start here — easy, measurable) → learning-to-branch (labels + B&B logs + MILP feature
graph + train/test **city split**) → learning-to-price/column-generate → surrogate simulation → value-function
/ RL → GNN encoders of GMNS topology → tensor factorization of OD-mode-time-scenario-control → LLM-to-model
(with strict validation).

## Near-term action list
1. **Benchmark spec** (done: `release_github/docs/BENCHMARK_SPEC.md`).
2. **Three seed cases** (done: SP, min-cost flow, Sioux Falls UE). Next seed: signal queue-spillback + ODME.
3. **One neural benchmark** — learning-to-warm-start for signal timing or network design (warm start first).
4. **Scenario generator** (`scenario_generator.py`, fixed seeds) — demand surge, capacity drop, incident,
   work zone, heat day, sensor noise, CAV penetration, UAM weather. See `scenario_generator_spec.md`.
5. **GUI4GMNS as required final report** — every case emits `dashboard.html` (outreach advantage).

## Community deliverables
- solver devs: MPS/LP files, model stats, primal/dual traces, B&B logs, instance families, scaling ladder.
- ML devs: graph/tensor features, train/val/test split, scenario generator, expert demos, branching/warm-start
  labels, feasibility checker, out-of-distribution tests.
- transportation users: GMNS files, dashboards, maps, before/after KPIs, scenario reports, policy interpretation.
