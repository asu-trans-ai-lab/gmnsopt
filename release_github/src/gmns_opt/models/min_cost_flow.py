"""Min-cost multi-commodity-free (single-commodity per solve) flow on a GMNS network (Case family A/B).

LP: min sum_a c_a x_a  s.t.  node conservation with supply/demand, 0 <= x_a <= u_a.
Solved with networkx.min_cost_flow (capacity-scaled to integers) for robustness on the bundled cases.
"""
from __future__ import annotations
import networkx as nx
from ..io import build_graph
from ..io.build_graph import zone_to_node


def min_cost_flow(net, supplies: dict, weight: str = "fftt_min", by_zone: bool = True, scale: int = 1) -> dict:
    """Min-cost flow given a node/zone -> net supply map (positive=source, negative=sink; must sum to 0).

    Returns {objective, solution (per-link flow), constraint_status, meta}.
    """
    G = build_graph(net, weight=weight)
    z2n = zone_to_node(net) if by_zone else {}
    H = nx.DiGraph()
    for u, v, a in G.edges(data=True):
        H.add_edge(u, v, weight=int(round(a["weight"] * 1000)),
                   capacity=int(round(a["capacity"] * scale)), link_id=a["link_id"])
    dem = {}
    for k, s in supplies.items():
        n = z2n.get(k, k)
        dem[n] = dem.get(n, 0) - int(round(s * scale))     # networkx: demand = -supply
    for n in H.nodes:
        H.nodes[n]["demand"] = dem.get(n, 0)
    try:
        flow = nx.min_cost_flow(H)
    except (nx.NetworkXUnfeasible, nx.NetworkXError) as e:
        return {"objective": float("inf"), "solution": [], "constraint_status": [
            {"constraint": "flow_conservation", "status": "infeasible", "detail": str(e)}],
            "meta": {"feasible": False}}
    sol = []; obj = 0.0
    for u in flow:
        for v, fv in flow[u].items():
            if fv > 0:
                fval = fv / scale
                sol.append({"link_id": H[u][v]["link_id"], "from_node": u, "to_node": v, "flow": fval})
                obj += (H[u][v]["weight"] / 1000.0) * fval
    return {"objective": obj, "solution": sol,
            "objective_trace": [{"iteration": 0, "objective": obj, "gap": 0.0}],
            "constraint_status": [{"constraint": "flow_conservation", "status": "satisfied"},
                                  {"constraint": "link_capacity", "status": "satisfied"}],
            "meta": {"feasible": True, "weight": weight}}
