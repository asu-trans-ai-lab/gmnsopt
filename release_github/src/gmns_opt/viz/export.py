"""Export a link-level solution to GeoJSON (LineString per link) for GUI4GMNS / kepler.gl / Leaflet.

Attributes carried per feature: link_id, flow, voc, travel_time_min — so the front end can map width to
flow, color to V/C, and highlight congested links. No external dependencies.
"""
from __future__ import annotations
import json


def export_geojson(net, solution, path: str) -> str:
    """Write a GeoJSON FeatureCollection of the solved links. `solution` is the model's per-link list."""
    by_id = {s["link_id"]: s for s in solution}
    feats = []
    for lk in net.links:
        s = by_id.get(lk.link_id)
        if s is None:
            continue
        fn, tn = net.nodes.get(lk.from_node, {}), net.nodes.get(lk.to_node, {})
        coords = [[fn.get("x", 0.0), fn.get("y", 0.0)], [tn.get("x", 0.0), tn.get("y", 0.0)]]
        feats.append({"type": "Feature",
                      "geometry": {"type": "LineString", "coordinates": coords},
                      "properties": {"link_id": lk.link_id, "flow": s.get("flow"),
                                     "voc": s.get("voc"), "travel_time_min": s.get("travel_time_min")}})
    fc = {"type": "FeatureCollection", "features": feats}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fc, f)
    return path
