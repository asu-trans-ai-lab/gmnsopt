"""Export optimization results as GUI4GMNS-ready layers.

Emits: optimization_links.geojson, optimization_nodes.geojson, decision_variables.csv, constraint_status.csv,
objective_trace.csv, scenario_summary.csv. GUI4GMNS mapping (width=flow, color=speed/voc, queue ribbon,
phase clock, desire-line delta) is documented in docs/gui4gmns_integration.md."""
from __future__ import annotations
import os
import csv
import json


def _rows(path, rows):
    if not rows:
        open(path, "w").close(); return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def export_optimization_layers(net, result, out_dir: str, scenario_summary=None) -> dict:
    """Write the GUI4GMNS layer set from a model `result` dict. Returns the paths written."""
    os.makedirs(out_dir, exist_ok=True)
    sol = result.get("solution") or []
    by_id = {s.get("link_id"): s for s in sol if isinstance(s, dict) and "link_id" in s}
    # link layer (LineString per link with solution properties)
    feats = []
    for lk in net.links:
        s = by_id.get(lk.link_id)
        if s is None:
            continue
        fn, tn = net.nodes.get(lk.from_node, {}), net.nodes.get(lk.to_node, {})
        feats.append({"type": "Feature",
                      "geometry": {"type": "LineString",
                                   "coordinates": [[fn.get("x", 0.0), fn.get("y", 0.0)],
                                                   [tn.get("x", 0.0), tn.get("y", 0.0)]]},
                      "properties": {"link_id": lk.link_id, "flow": s.get("flow"), "voc": s.get("voc"),
                                     "travel_time_min": s.get("travel_time_min"),
                                     "toll_min": s.get("marginal_cost_toll_min")}})
    with open(os.path.join(out_dir, "optimization_links.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f)
    # node layer
    nfeats = [{"type": "Feature",
               "geometry": {"type": "Point", "coordinates": [a.get("x", 0.0), a.get("y", 0.0)]},
               "properties": {"node_id": nid, "zone_id": a.get("zone_id")}}
              for nid, a in net.nodes.items()]
    with open(os.path.join(out_dir, "optimization_nodes.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": nfeats}, f)
    _rows(os.path.join(out_dir, "decision_variables.csv"), sol if isinstance(sol, list) else [])
    _rows(os.path.join(out_dir, "constraint_status.csv"), result.get("constraint_status", []))
    _rows(os.path.join(out_dir, "objective_trace.csv"), result.get("objective_trace", []))
    if scenario_summary:
        _rows(os.path.join(out_dir, "scenario_summary.csv"), scenario_summary)
    return {"out_dir": out_dir, "layers": ["optimization_links.geojson", "optimization_nodes.geojson",
            "decision_variables.csv", "constraint_status.csv", "objective_trace.csv"]}
