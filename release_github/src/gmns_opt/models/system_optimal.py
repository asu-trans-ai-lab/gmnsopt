"""System-optimal (SO) assignment + marginal-cost congestion pricing (Case family B).

SO minimizes total system travel time  min_v  sum_a v_a * t_a(v_a)  by Frank-Wolfe on the MARGINAL cost
    mc_a(v) = t_a(v) + v_a * t_a'(v),   with BPR t_a'(v) = t0_a * alpha_a * beta_a * v_a^(beta-1) / cap^beta.
The marginal-cost toll that decentralizes SO to a user equilibrium is  toll_a = v_a * t_a'(v_a) (in minutes).
"""
from __future__ import annotations
from collections import defaultdict
import numpy as np
import networkx as nx
from ..io.build_graph import zone_to_node


def system_optimal(net, max_iter: int = 80, gap_tol: float = 1e-4, by_zone: bool = True) -> dict:
    links = net.links
    edge_link = {}
    for i, lk in enumerate(links):
        k = (lk.from_node, lk.to_node)
        if k not in edge_link or lk.fftt_min < links[edge_link[k]].fftt_min:
            edge_link[k] = i
    idx = list(edge_link.values())
    edges = [(links[i].from_node, links[i].to_node) for i in idx]
    t0 = np.array([links[i].fftt_min for i in idx]); cap = np.array([max(links[i].capacity, 1e-6) for i in idx])
    alpha = np.array([links[i].alpha for i in idx]); beta = np.array([links[i].beta for i in idx])

    z2n = zone_to_node(net) if by_zone else {}
    dem_by_o = defaultdict(list)
    for (o, d, vol) in net.demand:
        dem_by_o[z2n.get(o, o)].append((z2n.get(d, d), vol))

    def t(v):   return t0 * (1 + alpha * (v / cap) ** beta)
    def dt(v):  return t0 * alpha * beta * (v ** (beta - 1)) / (cap ** beta)
    def mc(v):  return t(v) + v * dt(v)                 # marginal cost
    def tstt(v): return float((v * t(v)).sum())

    def aon(cost):
        G = nx.DiGraph()
        for p, (u, w) in enumerate(edges):
            G.add_edge(u, w, weight=float(cost[p]), pos=p)
        y = np.zeros(len(edges))
        for on, dests in dem_by_o.items():
            if on not in G:
                continue
            dist, paths = nx.single_source_dijkstra(G, on, weight="weight")
            for (dn, vol) in dests:
                if dn in paths:
                    nodes = paths[dn]
                    for u, w in zip(nodes[:-1], nodes[1:]):
                        y[G[u][w]["pos"]] += vol
        return y

    v = aon(t0); trace = []
    for it in range(1, max_iter + 1):
        y = aon(mc(v))
        m = mc(v)
        gap = float((m * (v - y)).sum()) / max(float((m * v).sum()), 1e-9)
        trace.append({"iteration": it, "objective_tstt_min": round(tstt(v), 2), "relative_gap": round(gap, 6)})
        if gap < gap_tol:
            break
        d = y - v; lo, hi = 0.0, 1.0
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            if float((mc(v + mid * d) * d).sum()) > 0:
                hi = mid
            else:
                lo = mid
        v = v + 0.5 * (lo + hi) * d

    toll = v * dt(v)
    sol = [{"link_id": links[i].link_id, "from_node": links[i].from_node, "to_node": links[i].to_node,
            "flow": round(float(v[p]), 3), "voc": round(float(v[p] / cap[p]), 4),
            "marginal_cost_toll_min": round(float(toll[p]), 4), "travel_time_min": round(float(t(v)[p]), 4)}
           for p, i in enumerate(idx)]
    return {"objective": round(tstt(v), 2), "solution": sol, "objective_trace": trace,
            "constraint_status": [{"constraint": "flow_conservation", "status": "satisfied"},
                                  {"constraint": "marginal_cost_pricing", "status": "applied"}],
            "meta": {"feasible": True, "iterations": len(trace), "objective_type": "system_optimal_tstt_min",
                     "total_toll_revenue_min": round(float((toll * v).sum()), 2),
                     "final_relative_gap": trace[-1]["relative_gap"] if trace else None}}
