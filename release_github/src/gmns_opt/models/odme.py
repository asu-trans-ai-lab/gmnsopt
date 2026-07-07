"""OD matrix estimation as inverse optimization / NNLS (Case family C).

Given base OD d0 and observed link counts y on sensor links, adjust OD to match counts while staying near
the prior:  min ||A d - y||^2 + lambda ||d - d0||^2,  d >= 0,  where A[link, od] is the (free-flow all-or-
nothing) OD->link incidence. Solved with non-negative least squares on the augmented system
[A; sqrt(lambda) I] d ~ [y; sqrt(lambda) d0]. Connects to the observation-operator view: an OD pair with no
sensor on its path is unobservable and stays at d0.
"""
from __future__ import annotations
import os
import csv
import numpy as np
import networkx as nx
from ..io import build_graph
from ..io.build_graph import zone_to_node


def odme(net, case_dir=None, counts=None, reg: float = 0.1, by_zone: bool = True) -> dict:
    G = build_graph(net)
    z2n = zone_to_node(net) if by_zone else {}
    ods = [(o, d, vol) for (o, d, vol) in net.demand if vol > 0]
    d0 = np.array([vol for *_, vol in ods], float)
    # free-flow AON path per OD -> link incidence (by link_id)
    link_ids = [lk.link_id for lk in net.links]
    lid_pos = {}
    for u, v, a in G.edges(data=True):
        lid_pos.setdefault(a["link_id"], len(lid_pos))
    incid = np.zeros((len(lid_pos), len(ods)))
    for k, (o, d, _) in enumerate(ods):
        on, dn = z2n.get(o, o), z2n.get(d, d)
        try:
            nodes = nx.shortest_path(G, on, dn, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
        for u, w in zip(nodes[:-1], nodes[1:]):
            incid[lid_pos[G[u][w]["link_id"]], k] = 1.0

    # observed counts on sensor links
    if counts is None and case_dir:
        cpath = os.path.join(case_dir, "input", "counts.csv")
        if os.path.exists(cpath):
            counts = {int(float(r["link_id"])): float(r["observed_volume"])
                      for r in csv.DictReader(open(cpath, encoding="utf-8-sig"))}
    synthetic = counts is None
    if synthetic:                                   # demo: 'true' OD = 1.2x base -> counts on all AON links
        true_link = incid @ (d0 * 1.2)
        counts = {lid: true_link[pos] for lid, pos in lid_pos.items() if true_link[pos] > 0}

    sensor_pos = [lid_pos[lid] for lid in counts if lid in lid_pos]
    A = incid[sensor_pos, :]
    y = np.array([counts[lid] for lid in counts if lid in lid_pos], float)
    observable = A.sum(axis=0) > 0                  # OD pairs crossing >= 1 sensor

    lam = reg * (np.linalg.norm(A) or 1.0)
    C = np.vstack([A, np.sqrt(lam) * np.eye(len(ods))])
    b = np.concatenate([y, np.sqrt(lam) * d0])
    d, _ = _nnls(C, b)
    d = np.where(observable, d, d0)                 # unobservable OD stay at prior

    before = float(np.sqrt(np.mean((A @ d0 - y) ** 2)))
    after = float(np.sqrt(np.mean((A @ d - y) ** 2)))
    sol = [{"o_zone": ods[k][0], "d_zone": ods[k][1], "base_od": round(float(d0[k]), 3),
            "odme_od": round(float(d[k]), 3),
            "adjustment_ratio": round(float(d[k] / d0[k]) if d0[k] > 0 else 1.0, 4),
            "observable": bool(observable[k])} for k in range(len(ods))]
    return {"objective": round(after, 4), "solution": sol,
            "objective_trace": [{"iteration": 0, "count_rmse": round(before, 3), "gap": 1.0},
                                {"iteration": 1, "count_rmse": round(after, 3), "gap": 0.0}],
            "constraint_status": [{"constraint": "non_negative_demand", "status": "satisfied"},
                                  {"constraint": "observability_gate",
                                   "status": f"{int((~observable).sum())} OD unobservable (kept at prior)"}],
            "meta": {"feasible": True, "sensors": len(y), "synthetic_counts": synthetic,
                     "count_rmse_before": round(before, 3), "count_rmse_after": round(after, 3),
                     "n_observable_od": int(observable.sum()), "n_od": len(ods),
                     "total_base": round(float(d0.sum()), 1), "total_odme": round(float(d.sum()), 1)}}


def _nnls(C, b, iters=200):
    from scipy.optimize import nnls
    try:
        return nnls(C, b, maxiter=iters)
    except Exception:                               # fallback: projected gradient
        x = np.zeros(C.shape[1]); L = np.linalg.norm(C, 2) ** 2 or 1.0
        for _ in range(500):
            x = np.maximum(0.0, x - (C.T @ (C @ x - b)) / L)
        return x, 0.0
