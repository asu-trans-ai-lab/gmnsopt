# Solver tiers

Core models run **license-free** by default (Tier 0). Higher tiers are OPTIONAL and never required.

| tier | back ends | used for |
|---|---|---|
| 0 | NetworkX, scipy (linprog/milp = HiGHS), OR-Tools | shortest path, flows, assignment, signal LP, network-design & facility MILP |
| 1 | Pyomo + HiGHS / CBC / Ipopt | larger LP/MILP/NLP modeling |
| 2 | Gurobi / CPLEX / COPT / Mosek | industrial-scale MILP/QP (commercial, optional) |
| 3 | cuOpt / GPU / neural warm-start / RL / custom decomposition | acceleration + learned methods |

Adapters live in `gmns_opt.solvers` (`ScipyHiGHS`, `NetworkXSolver`, `ORToolsAdapter`, `CommercialPlaceholder`,
`NeuralPlaceholder`). Check availability: `gmns-opt solver-status`. No commercial dependency is imposed;
placeholders detect optional back ends if installed.
