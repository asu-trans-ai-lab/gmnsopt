"""Build a routable networkx DiGraph from a GMNSNetwork (free-flow travel time as default weight)."""
from __future__ import annotations
import networkx as nx


def build_graph(net, weight: str = "fftt_min"):
    """Return a networkx.DiGraph. Each edge carries link attributes + `weight` (default free-flow minutes).

    Parallel links (same from/to) are collapsed to the lowest-cost link for simple-graph algorithms; the
    full link list is preserved on the graph as `graph['links']` for flow models that need every link.
    """
    G = nx.DiGraph()
    for nid, a in net.nodes.items():
        G.add_node(nid, **a)
    best = {}
    for lk in net.links:
        key = (lk.from_node, lk.to_node)
        w = getattr(lk, weight) if hasattr(lk, weight) else lk.fftt_min
        if key not in best or w < best[key][0]:
            best[key] = (w, lk)
    for (u, v), (w, lk) in best.items():
        G.add_edge(u, v, weight=w, link_id=lk.link_id, capacity=lk.capacity,
                   fftt_min=lk.fftt_min, length=lk.length, alpha=lk.alpha, beta=lk.beta)
    G.graph["links"] = net.links
    G.graph["nodes"] = net.nodes
    return G


def zone_to_node(net):
    """Map zone_id -> node_id (a zone is anchored at the node that declares it)."""
    z2n = {}
    for nid, a in net.nodes.items():
        z = a.get("zone_id")
        if z is not None and z not in z2n:
            z2n[z] = nid
    return z2n
