# Changelog

## [0.1.0] — reproducible kernel + three foundational cases
- Core: GMNS I/O (`read_gmns`, `validate_gmns`, `build_graph`), case runner (`run_case`) with the
  standard output contract (solution / objective_trace / constraint_status / summary).
- Models: `shortest_path` (Dijkstra), `min_cost_flow` (networkx), `traffic_assignment` (user-equilibrium
  Frank-Wolfe + BPR, with a real convergence trace).
- Cases: `00_shortest_path_toy`, `01_min_cost_flow_toy`, `02_sioux_falls_assignment`.
- CLI `gmns-opt run|validate`; GeoJSON viz export; docs (benchmark spec, data contract, tutorial ladder).
- Roadmap: ODME, signal MILP, network design, resilience, freight/EV/UAM; solver tiers; tensor benchmark.
