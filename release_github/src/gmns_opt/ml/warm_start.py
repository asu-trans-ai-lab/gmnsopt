"""Learning-to-warm-start interface (see docs/ml_for_optimization.md).

A warm-starter predicts a good initial solution (paths/flows/green times/tolls) for a repeated case, to be
polished by an exact/heuristic solver. The default is a NON-learned baseline (free-flow all-or-nothing), so
the interface is testable today; learned models (GNN/regression) plug in via `WarmStarter.predict`.
"""
from __future__ import annotations
import networkx as nx
from ..io import build_graph
from ..io.build_graph import zone_to_node


class WarmStarter:
    """Base warm-starter. Subclass and override `predict` with a learned model."""
    name = "free_flow_aon_baseline"

    def predict(self, net) -> dict:
        """Return a baseline initial link-flow warm start (free-flow all-or-nothing)."""
        G = build_graph(net); z2n = zone_to_node(net)
        flow = {lk.link_id: 0.0 for lk in net.links}
        for (o, d, vol) in net.demand:
            try:
                nodes = nx.shortest_path(G, z2n.get(o, o), z2n.get(d, d), weight="weight")
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue
            for u, w in zip(nodes[:-1], nodes[1:]):
                flow[G[u][w]["link_id"]] += vol
        return {"warm_start": "link_flow", "source": self.name,
                "link_flow": [{"link_id": k, "flow": v} for k, v in flow.items() if v > 0]}
# TODO: LearnedWarmStarter(GNN) trained on repeated city/scenario cases; benchmark vs solver-from-scratch.
