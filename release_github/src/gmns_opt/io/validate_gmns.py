"""Validate a GMNSNetwork against the minimal data contract; report problems instead of crashing."""
from __future__ import annotations


def validate_gmns(net) -> dict:
    """Return a report dict: {ok, errors, warnings, stats}. `ok` is False if any error is found."""
    errors, warnings = [], []
    node_ids = set(net.nodes)

    if not net.links:
        errors.append("no links")
    for lk in net.links:
        if lk.from_node not in node_ids:
            errors.append(f"link {lk.link_id}: from_node {lk.from_node} not in node.csv")
        if lk.to_node not in node_ids:
            errors.append(f"link {lk.link_id}: to_node {lk.to_node} not in node.csv")
        if lk.capacity <= 0:
            warnings.append(f"link {lk.link_id}: non-positive capacity")
        if lk.free_speed <= 0:
            warnings.append(f"link {lk.link_id}: non-positive free_speed")

    zones = set(net.zones)
    for (o, d, v) in net.demand:
        if o not in zones:
            warnings.append(f"demand origin zone {o} has no anchoring node")
        if d not in zones:
            warnings.append(f"demand destination zone {d} has no anchoring node")

    stats = {"nodes": len(net.nodes), "links": len(net.links), "zones": len(zones),
             "od_pairs": len(net.demand), "total_demand": sum(v for *_, v in net.demand)}
    # de-duplicate but keep order
    errors = list(dict.fromkeys(errors)); warnings = list(dict.fromkeys(warnings))[:50]
    return {"ok": not errors, "errors": errors, "warnings": warnings, "stats": stats}
