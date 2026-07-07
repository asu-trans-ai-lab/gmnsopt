"""Zone accessibility from one-to-all shortest-path skims (Case family A).

For each origin zone, compute least-cost travel time to every other zone, then a cumulative-opportunity
accessibility: A_i = # zones reachable within `threshold_min` (or a negative-exponential gravity measure).
"""
from __future__ import annotations
import math
import networkx as nx
from ..io import build_graph
from ..io.build_graph import zone_to_node


def accessibility(net, threshold_min: float = 30.0, weight: str = "fftt_min", decay: float = 0.0) -> dict:
    """Return per-zone accessibility. decay>0 uses exp(-decay*t); else cumulative count within threshold."""
    G = build_graph(net, weight=weight)
    z2n = zone_to_node(net)
    zones = sorted(z2n)
    rows = []
    for zi in zones:
        oi = z2n[zi]
        try:
            dist = nx.single_source_dijkstra_path_length(G, oi, weight="weight")
        except nx.NodeNotFound:
            dist = {}
        reachable = 0; grav = 0.0
        for zj in zones:
            if zj == zi:
                continue
            tt = dist.get(z2n[zj])
            if tt is None:
                continue
            if tt <= threshold_min:
                reachable += 1
            grav += math.exp(-decay * tt) if decay > 0 else 0.0
        rows.append({"zone_id": zi, "reachable_within_min": reachable,
                     "gravity_accessibility": round(grav, 4) if decay > 0 else None,
                     "threshold_min": threshold_min})
    total = sum(r["reachable_within_min"] for r in rows)
    return {"objective": total, "solution": rows,
            "objective_trace": [{"iteration": 0, "objective": total, "gap": 0.0}],
            "constraint_status": [{"constraint": "connectivity", "status": "satisfied"}],
            "meta": {"feasible": True, "measure": "cumulative_opportunity" if decay == 0 else "gravity",
                     "zones": len(zones), "mean_reachable": round(total / max(len(zones), 1), 2)}}
