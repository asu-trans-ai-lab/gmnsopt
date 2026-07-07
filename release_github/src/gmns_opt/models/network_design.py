"""Fixed-charge network design MILP (Case family E): which links to build to route demand at min cost.

min  sum_a c_a x_a + sum_a f_a y_a
s.t. node conservation (route Q units source->sink),  x_a <= Q * y_a,  sum_a f_a y_a <= budget,  y in {0,1}.
Existing links have build cost 0 and y fixed to 1; candidate links carry a build cost. Solved with
scipy.optimize.milp (HiGHS) -- no commercial solver required.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from ..io.build_graph import zone_to_node


def network_design(net, source, sink, flow: float, budget: float, by_zone: bool = True,
                   candidate_link_ids=None) -> dict:
    links = net.links
    L = len(links)
    z2n = zone_to_node(net) if by_zone else {}
    s = z2n.get(source, source); t = z2n.get(sink, sink)
    cand = set(candidate_link_ids) if candidate_link_ids is not None else {lk.link_id for lk in links}
    travel = np.array([lk.fftt_min for lk in links])
    build = np.array([(lk.length if lk.link_id in cand else 0.0) for lk in links])   # build cost = length
    is_cand = np.array([lk.link_id in cand for lk in links])

    nodes = sorted(net.nodes)
    nidx = {n: i for i, n in enumerate(nodes)}
    # variables: x (L continuous), y (L binary)
    c = np.concatenate([travel, build])
    A_rows, lb, ub = [], [], []
    # node conservation (equality)  sum_out x - sum_in x = b
    Aeq = np.zeros((len(nodes), 2 * L))
    for a, lk in enumerate(links):
        Aeq[nidx[lk.from_node], a] += 1.0
        Aeq[nidx[lk.to_node], a] -= 1.0
    b = np.zeros(len(nodes)); b[nidx[s]] = flow; b[nidx[t]] = -flow
    cons = [LinearConstraint(Aeq, b, b)]
    # linking  x_a - flow*y_a <= 0
    Alink = np.zeros((L, 2 * L))
    for a in range(L):
        Alink[a, a] = 1.0; Alink[a, L + a] = -flow
    cons.append(LinearConstraint(Alink, -np.inf * np.ones(L), np.zeros(L)))
    # budget  sum f_a y_a <= budget
    Abud = np.zeros((1, 2 * L)); Abud[0, L:] = build
    cons.append(LinearConstraint(Abud, [-np.inf], [budget]))

    lo = np.zeros(2 * L); hi = np.concatenate([flow * np.ones(L), np.ones(L)])
    hi[L:][~is_cand] = 1.0; lo[L:][~is_cand] = 1.0        # existing links: y fixed to 1
    integ = np.concatenate([np.zeros(L), np.ones(L)])     # y integer
    res = milp(c, constraints=cons, integrality=integ, bounds=Bounds(lo, hi))
    if not res.success:
        return {"objective": float("inf"), "solution": [], "constraint_status": [
            {"constraint": "design_feasible", "status": "infeasible", "detail": res.message}],
            "meta": {"feasible": False}}
    x = res.x[:L]; y = res.x[L:]
    built = [{"link_id": links[a].link_id, "from_node": links[a].from_node, "to_node": links[a].to_node,
              "flow": round(float(x[a]), 3), "built": int(round(y[a])),
              "candidate": bool(is_cand[a]), "build_cost": round(float(build[a]), 3)}
             for a in range(L) if x[a] > 1e-6 or (is_cand[a] and y[a] > 0.5)]
    spend = float((build * (np.round(y))).sum())
    return {"objective": round(float(res.fun), 4), "solution": built,
            "objective_trace": [{"iteration": 0, "objective": round(float(res.fun), 4), "gap": 0.0}],
            "constraint_status": [{"constraint": "flow_conservation", "status": "satisfied"},
                                  {"constraint": "budget", "status": f"spend {spend:.2f} <= {budget}"}],
            "meta": {"feasible": True, "budget": budget, "build_spend": round(spend, 3),
                     "n_candidate_built": int(sum(1 for a in range(L) if is_cand[a] and y[a] > 0.5)),
                     "travel_cost": round(float((travel * x).sum()), 3)}}
