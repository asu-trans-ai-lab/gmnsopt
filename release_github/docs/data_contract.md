# GMNS data contract

Every case's `input/` uses the minimal routable GMNS subset. Extra GMNS columns are ignored (forward-compatible).

## Required
**node.csv** — `node_id` [, `zone_id`, `x_coord`, `y_coord`]
**link.csv** — `link_id, from_node_id, to_node_id` [, `length`, `lanes`, `free_speed`, `capacity`,
`vdf_alpha`, `vdf_beta`]
**demand.csv** — `o_zone_id, d_zone_id, volume`

Defaults when a column is absent: `length=1`, `lanes=1`, `free_speed=30`, `capacity=1000`,
`vdf_alpha=0.15`, `vdf_beta=4`. Free-flow travel time = `length / free_speed` (bundled cases: miles/mph → minutes).
A zone is anchored at the node that declares its `zone_id`.

## Optional (operations & scenarios) — used by higher-level model families
`movement.csv`, `signal_timing.csv`, `detector.csv`, `link_performance.csv` (time-dependent),
`transit_route.csv`, `vehicle.csv`, `charging_station.csv`, `vertiport.csv`, `scenario.csv`,
`project.csv`, `constraint.csv`.

## Output contract
`output/solution.csv`, `objective_trace.csv`, `constraint_status.csv`, `summary.md`
(+ optional `decision_variable.csv`, `solver_log.txt`, `simulation_check.csv`, `gui4gmns_dashboard.html`).
See BENCHMARK_SPEC.md for column definitions.
