"""Shortest path / least-cost routing on a GMNS network (Case family A).

LP view: min sum_a c_a x_a s.t. node balance (unit flow source->sink), x >= 0. Solved here with Dijkstra
(networkx) on the generalized-cost weight (default: free-flow travel time in minutes).
"""
from __future__ import annotations
import networkx as nx
from ..io import build_graph
from ..io.build_graph import zone_to_node


def shortest_path(net, origin, destination, weight: str = "fftt_min", by_zone: bool = True) -> dict:
    """Least-cost path from origin to destination.

    by_zone=True interprets origin/destination as zone ids (mapped to their anchoring nodes).
    Returns {objective (cost), path (node list), links (link_id list), meta}.
    """
    G = build_graph(net, weight=weight)
    o, d = origin, destination
    if by_zone:
        z2n = zone_to_node(net); o, d = z2n.get(origin, origin), z2n.get(destination, destination)
    try:
        nodes = nx.shortest_path(G, o, d, weight="weight")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return {"objective": float("inf"), "path": [], "links": [], "constraint_status": [],
                "meta": {"feasible": False, "reason": f"no path {o}->{d}"}}
    cost = sum(G[u][v]["weight"] for u, v in zip(nodes[:-1], nodes[1:]))
    links = [G[u][v]["link_id"] for u, v in zip(nodes[:-1], nodes[1:])]
    return {"objective": cost, "path": nodes, "links": links,
            "objective_trace": [{"iteration": 0, "objective": cost, "gap": 0.0}],
            "constraint_status": [{"constraint": "connectivity", "status": "satisfied"}],
            "meta": {"feasible": True, "origin_node": o, "dest_node": d, "weight": weight}}
