# GMNS-DTA-201 (static) — Sioux Falls user-equilibrium assignment
Classic Sioux Falls (24 nodes, 76 links, 528 OD pairs) converted to GMNS. Static user equilibrium via
Frank-Wolfe with BPR. Run: `gmns-opt run .` → link flows/V:C/times + a real convergence trace
(`objective_trace.csv`, Beckmann + relative gap). Reproduces TSTT ≈ 7.48M veh-min.
Source: Transportation Networks for Research (see ../../../references/README.md).
