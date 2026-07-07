# GUI4GMNS integration

Optimization without visualization is hard to understand. `gmns_opt.visualization.export_optimization_layers`
emits GUI4GMNS-ready layers from any model result:
`optimization_links.geojson`, `optimization_nodes.geojson`, `decision_variables.csv`, `constraint_status.csv`,
`objective_trace.csv`, `scenario_summary.csv`.

| optimization output | visualization |
|---|---|
| link flow | link width / 3D height |
| speed / V:C | color |
| queue | red spillback ribbon |
| capacity decision | before/after link highlight |
| signal green | phase clock / green-split chart |
| OD adjustment | desire-line delta |
| pricing | toll marker / shadow-price layer |
| constraint violation | red warning marker |
| objective trace | convergence panel |
| scenario risk | heatmap / before-after dashboard |

Every case should produce `optimization result + simulation check + visual explanation`.
