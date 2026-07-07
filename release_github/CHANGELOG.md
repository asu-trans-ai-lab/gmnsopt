# Changelog

## [0.1.0] — reproducible kernel + ten cases across the model families
- Core: GMNS I/O (`read_gmns`, `validate_gmns`, `build_graph`), case runner (`run_case`) with the standard
  output contract (solution / objective_trace / constraint_status / summary), CLI `gmns-opt`, GeoJSON viz.
- Models (working, dependency-light; MILP/LP via scipy HiGHS, no commercial solver):
  - A routing/access: `shortest_path`, `accessibility`
  - B assignment: `traffic_assignment` (UE Frank-Wolfe + BPR), `system_optimal` (+ marginal-cost pricing)
  - flow: `min_cost_flow`, `max_flow` (min-cut / evacuation)
  - C inverse: `odme` (NNLS OD estimation, observability gate)
  - D operations: `signal_timing` (green-split LP)
  - E design: `network_design` (fixed-charge MILP)
  - G siting: `facility_location` (p-median MILP; EV charging / hub siting)
- Ten cases (`cases/00..09`) with problem.yml + README + formulation + GMNS input.
- Verified: SO travel time < UE; ODME count-RMSE 2720→185; MILP budget respected; p-median opens K. 10 tests.
- Roadmap toward dynamic assignment, resilience/robust, freight/EV/UAM, transit, CAV; solver tiers; tensor benchmark.
