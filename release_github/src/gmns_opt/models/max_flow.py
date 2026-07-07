"""Maximum flow / min cut between a source and sink zone (Case family F — evacuation throughput).

max sum flow  s.t.  0 <= x_a <= cap_a, node conservation (except source/sink). Max-flow min-cut theorem gives
the bottleneck cut. Useful as an evacuation / resilience throughput bound on a GMNS network.
"""
from __future__ import annotations
import networkx as nx
from ..io import build_graph
from ..io.build_graph import zone_to_node


def max_flow(net, source, sink, by_zone: bool = True) -> dict:
    G = build_graph(net)
    if by_zone:
        z2n = zone_to_node(net); s, t = z2n.get(source, source), z2n.get(sink, sink)
    else:
        s, t = source, sink
    H = nx.DiGraph()
    for u, v, a in G.edges(data=True):
        H.add_edge(u, v, capacity=float(a["capacity"]), link_id=a["link_id"])
    try:
        flow_val, flow_dict = nx.maximum_flow(H, s, t)
        cut_val, (reach, nonreach) = nx.minimum_cut(H, s, t)
    except (nx.NetworkXError, nx.NetworkXUnbounded) as e:
        return {"objective": 0.0, "solution": [], "meta": {"feasible": False, "reason": str(e)}}
    sol = [{"link_id": H[u][v]["link_id"], "from_node": u, "to_node": v, "flow": fv,
            "capacity": H[u][v]["capacity"]}
           for u in flow_dict for v, fv in flow_dict[u].items() if fv > 0]
    cut_links = [{"from_node": u, "to_node": v, "capacity": H[u][v]["capacity"]}
                 for u in reach for v in H.successors(u) if v in nonreach]
    return {"objective": flow_val, "solution": sol,
            "objective_trace": [{"iteration": 0, "objective": flow_val, "gap": 0.0}],
            "constraint_status": [{"constraint": "capacity", "status": "satisfied"},
                                  {"constraint": "min_cut", "status": f"{len(cut_links)} bottleneck links"}],
            "meta": {"feasible": True, "max_flow": flow_val, "min_cut_capacity": cut_val,
                     "source_node": s, "sink_node": t, "bottleneck_links": cut_links[:20]}}
