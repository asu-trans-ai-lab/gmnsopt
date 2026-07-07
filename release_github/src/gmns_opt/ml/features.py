"""Feature extraction from a GMNS network for ML-for-optimization (see docs/ml_for_optimization.md).

Produces node / link / demand / graph-adjacency features usable by GNN encoders, learning-to-warm-start, and
learning-to-branch. This does NOT replace solvers — it supports repeated-scenario workflows.
"""
from __future__ import annotations
from collections import defaultdict
import numpy as np


def extract_features(net, scenario: str = "normal") -> dict:
    """Return numeric feature blocks + adjacency for the network (dependency-light, numpy only)."""
    node_ids = sorted(net.nodes)
    nidx = {n: i for i, n in enumerate(node_ids)}
    indeg = defaultdict(int); outdeg = defaultdict(int)
    link_feat = []
    for lk in net.links:
        outdeg[lk.from_node] += 1; indeg[lk.to_node] += 1
        link_feat.append([lk.length, lk.lanes, lk.free_speed, lk.capacity, lk.fftt_min, lk.alpha, lk.beta])
    node_feat = []
    for n in node_ids:
        a = net.nodes[n]
        node_feat.append([a.get("x", 0.0), a.get("y", 0.0), float(a.get("zone_id") is not None),
                          indeg[n], outdeg[n]])
    prod = defaultdict(float); attr = defaultdict(float)
    for (o, d, v) in net.demand:
        prod[o] += v; attr[d] += v
    demand_feat = {"total": sum(v for *_, v in net.demand), "n_od": len(net.demand),
                   "max_production": max(prod.values()) if prod else 0.0,
                   "max_attraction": max(attr.values()) if attr else 0.0}
    edge_index = [[nidx[lk.from_node], nidx[lk.to_node]] for lk in net.links]
    return {"scenario": scenario,
            "node_features": np.asarray(node_feat, float).tolist(),
            "node_feature_names": ["x", "y", "is_zone", "in_degree", "out_degree"],
            "link_features": np.asarray(link_feat, float).tolist(),
            "link_feature_names": ["length", "lanes", "free_speed", "capacity", "fftt_min", "alpha", "beta"],
            "demand_features": demand_feat,
            "edge_index": edge_index,
            "stats": {"n_nodes": len(node_ids), "n_links": len(net.links)}}
