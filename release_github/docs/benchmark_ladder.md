# Benchmark ladder (L0–L5)

Release **both** small transparent cases and large realistic cases.

| level | what | purpose | example cases |
|---|---|---|---|
| L0 | formulation micro (5–20 nodes, 1 signal) | teach / debug / validate LLM formulations | 00, 01, 07, 08, 10, 12 |
| L1 | classic research nets as GMNS | connect to literature; algorithm comparison | 02, 03, 04, 05, 06, 09 |
| L2 | open-city OSM2GMNS | GIS/planning + GUI4GMNS outreach | (roadmap: Tempe, Phoenix, Atlanta, LA, Bay) |
| L3 | dynamic corridor operations | signals, queues, work zones, incidents (DTA/CBI/ODME) | (roadmap) |
| L4 | stochastic / robust | demand/capacity/incident/weather/CAV/UAM uncertainty | 11 (capacity drop) |
| L5 | industrial-scale city | 10^4–10^6 vars, multi-mode/period/scenario | 12 (multimodal skeleton) |

Scenarios are generated deterministically (`gmns-opt generate-scenarios`, fixed seeds): normal, capacity_drop,
demand_surge, work_zone, weather, cav_penetration, uam_weather_restriction.
