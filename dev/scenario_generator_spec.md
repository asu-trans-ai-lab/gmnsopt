# scenario_generator.py — spec (planned)

Generate reproducible scenario sets (fixed random seeds) that perturb a base GMNS case into `scenario.csv`
(+ time-dependent `link_performance.csv`) for Level-4 stochastic/robust cases.

Scenario families: demand surge, capacity drop, incident (link/start/duration/severity), work zone,
heat day, sensor noise / probe penetration, CAV penetration, UAM weather restriction.

Contract:
```
scenario_generator.py --case <dir> --families demand_surge,incident,heat --n 50 --seed 12345
  -> <case>/optional_input/scenario.csv      (scenario_id, family, param, value)
  -> <case>/optional_input/link_performance_s{n}.csv   (link_id, time, capacity, ...)
```
Objectives enabled downstream: expected delay, worst-case delay, CVaR, reliability. Every scenario must be
reproducible from (case, family set, seed).
