# Changelog

## [0.2.0] — broad open-science benchmark scaffold
Preserves the working kernel (I/O, validation, graph, shortest path, min-cost flow, Frank-Wolfe UE, case
runner, CLI, output contract, GeoJSON viz, existing cases/tests) and adds:
- **Application taxonomy** `benchmark/registry.py` + `applications/` — 10 families with formulation classes,
  required/optional files, outputs, solver tier, visualization, maturity (runnable/scaffold/planned).
- **Tensor framework** `tensor/` — sparse x[o,d,m,p,τ,s,a] + companions, GMNS→demand-tensor, scenario
  expansion, CSV/JSON export.
- **Scenario generator** `scenarios/` — normal/capacity_drop/demand_surge/work_zone/weather/cav_penetration/
  uam_weather_restriction (fixed seeds).
- **Solver tiers** `solvers/` — Tier 0–3 adapters (networkx, scipy-HiGHS, OR-Tools, commercial, neural); no
  commercial dependency.
- **ML readiness** `ml/` — GMNS feature extraction, learning-to-warm-start interface, learning-to-branch schema.
- **Visualization** `visualization/export_optimization_layers.py` — GUI4GMNS layer set.
- **Models added**: `system_optimal` (+ pricing), `accessibility`, `max_flow`, `odme` (NNLS), `signal_timing`
  (LP), `network_design` (MILP), `facility_location` (MILP), `resilience_scenario`, `multimodal_skeleton`.
- **Cases**: 13 seed cases (`cases/00..12`) incl. ODME toy, resilience capacity-drop, CAV/UAM skeleton.
- **Case templates** `case_templates/` — one per family.
- **CLI**: `list-families`, `describe-family`, `generate-scenarios`, `solver-status`.
- **Docs**: vision, application_taxonomy, tensor_framework, benchmark_ladder, solver_tiers, ml_for_optimization,
  gui4gmns_integration, open_science_test_cases.
- **Tests**: 18 (kernel + scaffold: registry, taxonomy, tensor conversion, scenarios, ml, CLI, new cases).

## [0.1.0] — reproducible kernel + foundational cases
- GMNS I/O, validation, graph builder, shortest path, min-cost flow, Frank-Wolfe UE, case runner, CLI, docs.
