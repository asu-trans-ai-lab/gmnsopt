"""p-median facility location MILP (Case family G — e.g. EV charging / hub siting).

Open K facilities at candidate zones to minimize total demand-weighted access time:
  min  sum_i sum_j w_i d_ij x_ij   s.t.  sum_j x_ij = 1 (each demand assigned),  x_ij <= y_j,
       sum_j y_j = K,  y in {0,1}, x >= 0.
d_ij = shortest-path travel time (min) zone i -> candidate zone j. Solved with scipy.optimize.milp (HiGHS).
"""
from __future__ import annotations
import numpy as np
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds
from ..io import build_graph
from ..io.build_graph import zone_to_node


def facility_location(net, k: int, candidates=None, weight: str = "fftt_min") -> dict:
    G = build_graph(net, weight=weight)
    z2n = zone_to_node(net)
    demand_zones = sorted(z2n)
    cand_zones = sorted(candidates) if candidates is not None else demand_zones
    w = {z: 0.0 for z in demand_zones}
    for (o, d, vol) in net.demand:
        w[o] = w.get(o, 0.0) + vol
    if sum(w.values()) == 0:
        w = {z: 1.0 for z in demand_zones}
    # skim d_ij
    D = np.zeros((len(demand_zones), len(cand_zones)))
    for ii, zi in enumerate(demand_zones):
        try:
            dist = nx.single_source_dijkstra_path_length(G, z2n[zi], weight="weight")
        except nx.NodeNotFound:
            dist = {}
        for jj, zj in enumerate(cand_zones):
            D[ii, jj] = dist.get(z2n[zj], 1e6)
    nI, nJ = len(demand_zones), len(cand_zones)
    # variables: x (nI*nJ) then y (nJ)
    wi = np.array([w[z] for z in demand_zones])
    c = np.concatenate([(wi[:, None] * D).ravel(), np.zeros(nJ)])
    cons = []
    # assignment: sum_j x_ij = 1
    Aassign = np.zeros((nI, nI * nJ + nJ))
    for i in range(nI):
        for j in range(nJ):
            Aassign[i, i * nJ + j] = 1.0
    cons.append(LinearConstraint(Aassign, np.ones(nI), np.ones(nI)))
    # linking x_ij <= y_j
    Alink = np.zeros((nI * nJ, nI * nJ + nJ)); r = 0
    for i in range(nI):
        for j in range(nJ):
            Alink[r, i * nJ + j] = 1.0; Alink[r, nI * nJ + j] = -1.0; r += 1
    cons.append(LinearConstraint(Alink, -np.inf * np.ones(nI * nJ), np.zeros(nI * nJ)))
    # count: sum_j y_j = K
    Acount = np.zeros((1, nI * nJ + nJ)); Acount[0, nI * nJ:] = 1.0
    cons.append(LinearConstraint(Acount, [k], [k]))
    lo = np.zeros(nI * nJ + nJ); hi = np.ones(nI * nJ + nJ)
    integ = np.concatenate([np.zeros(nI * nJ), np.ones(nJ)])
    res = milp(c, constraints=cons, integrality=integ, bounds=Bounds(lo, hi))
    if not res.success:
        return {"objective": float("inf"), "solution": [], "meta": {"feasible": False, "detail": res.message}}
    y = res.x[nI * nJ:]
    opened = [cand_zones[j] for j in range(nJ) if y[j] > 0.5]
    x = res.x[:nI * nJ].reshape(nI, nJ)
    assign = [{"demand_zone": demand_zones[i], "assigned_facility_zone": cand_zones[int(np.argmax(x[i]))],
               "access_time_min": round(float(D[i, int(np.argmax(x[i]))]), 3),
               "demand_weight": round(float(wi[i]), 2)} for i in range(nI)]
    return {"objective": round(float(res.fun), 4), "solution": assign,
            "objective_trace": [{"iteration": 0, "objective": round(float(res.fun), 4), "gap": 0.0}],
            "constraint_status": [{"constraint": "assign_all_demand", "status": "satisfied"},
                                  {"constraint": "open_exactly_K", "status": f"opened {len(opened)}"}],
            "meta": {"feasible": True, "k": k, "opened_facility_zones": opened,
                     "total_weighted_access_min": round(float(res.fun), 2),
                     "mean_access_min": round(float((wi * D[np.arange(nI), x.argmax(1)]).sum() /
                                                     max(wi.sum(), 1e-9)), 3)}}
