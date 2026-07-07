# Application taxonomy

Ten families (authoritative metadata in `gmns_opt.benchmark.registry`; browse with `gmns-opt list-families`
and `gmns-opt describe-family <id>`). Maturity: **runnable** (works today), **scaffold** (schema + placeholder),
**planned**.

| id | name | classes | maturity | runnable models |
|---|---|---|---|---|
| routing_accessibility | Routing & Accessibility | LP | runnable | shortest_path, accessibility, min_cost_flow |
| traffic_assignment_pricing | Traffic Assignment & Pricing | convex-NLP/MIP/dynamic | runnable | traffic_assignment, system_optimal |
| odme_inverse_optimization | ODME & Inverse Optimization | LP/QP/NLP | runnable | odme |
| signal_queue_control | Signal & Queue Control | MIP/dynamic/RL-ready | runnable | signal_timing |
| resilience_workzone_incident | Resilience/Work-Zone/Incident | MIP/stochastic/robust | runnable | resilience_scenario, max_flow |
| cav_control | CAV Mixed-Traffic Control | MIP/QP/NLP/RL | scaffold | multimodal_skeleton |
| uam_air_ground_coordination | UAM Air–Ground Coordination | MIP/stochastic/RL | scaffold | multimodal_skeleton |
| freight_ev_logistics | Freight/EV/Logistics | MIP/stochastic | scaffold | facility_location |
| transit_frequency_accessibility | Transit Frequency & Access | MIP/LP | planned | — |
| solver_learning_and_neural_optimization | Solver Learning & Neural Opt | ML/RL/surrogate | scaffold | ml_features |

Each family maps to `case_templates/<id>/` (copy → fill `input/` → edit `problem.yml` → `gmns-opt run`).
