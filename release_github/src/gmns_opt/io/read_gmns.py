"""Read a GMNS case directory (node.csv, link.csv, demand.csv) into plain Python structures.

GMNS reference: https://github.com/zephyr-data-specs/GMNS . We use the minimal routable subset:
  node.csv : node_id [, zone_id, x_coord, y_coord]
  link.csv : link_id, from_node_id, to_node_id [, length, lanes, free_speed, capacity, vdf_alpha, vdf_beta]
  demand.csv: o_zone_id, d_zone_id, volume
Free-flow travel time is derived as length / free_speed when not given (consistent units are the caller's
responsibility; the bundled cases use miles and mph -> hours, reported in minutes).
"""
from __future__ import annotations
import csv
import os
from dataclasses import dataclass, field


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


@dataclass
class Link:
    link_id: int
    from_node: int
    to_node: int
    length: float = 1.0
    lanes: float = 1.0
    free_speed: float = 30.0
    capacity: float = 1000.0      # per the link (already lane-aggregated in the bundled cases)
    alpha: float = 0.15           # BPR alpha
    beta: float = 4.0             # BPR beta

    @property
    def fftt_min(self) -> float:
        """free-flow travel time in minutes (length[mi] / speed[mph] * 60)."""
        return (self.length / max(self.free_speed, 1e-6)) * 60.0


@dataclass
class GMNSNetwork:
    nodes: dict = field(default_factory=dict)      # node_id -> {zone_id, x, y}
    links: list = field(default_factory=list)      # list[Link]
    demand: list = field(default_factory=list)     # list[(o_zone, d_zone, volume)]

    @property
    def zones(self):
        z = {n["zone_id"] for n in self.nodes.values() if n.get("zone_id")}
        return sorted(z)


def read_gmns(case_dir: str) -> GMNSNetwork:
    """Read node.csv / link.csv / demand.csv from `case_dir` (or `case_dir/input`)."""
    base = case_dir
    if os.path.isdir(os.path.join(case_dir, "input")):
        base = os.path.join(case_dir, "input")
    net = GMNSNetwork()

    with open(os.path.join(base, "node.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            nid = int(_num(r.get("node_id")))
            z = r.get("zone_id")
            net.nodes[nid] = {"zone_id": (int(_num(z)) if z not in (None, "", "0") else None),
                              "x": _num(r.get("x_coord")), "y": _num(r.get("y_coord"))}

    with open(os.path.join(base, "link.csv"), encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            net.links.append(Link(
                link_id=int(_num(r.get("link_id"))),
                from_node=int(_num(r.get("from_node_id"))),
                to_node=int(_num(r.get("to_node_id"))),
                length=_num(r.get("length"), 1.0) or 1.0,
                lanes=_num(r.get("lanes"), 1.0) or 1.0,
                free_speed=_num(r.get("free_speed"), 30.0) or 30.0,
                capacity=_num(r.get("capacity"), 1000.0) or 1000.0,
                alpha=_num(r.get("vdf_alpha"), 0.15) or 0.15,
                beta=_num(r.get("vdf_beta"), 4.0) or 4.0))

    dpath = os.path.join(base, "demand.csv")
    if os.path.exists(dpath):
        with open(dpath, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                vol = _num(r.get("volume"))
                if vol > 0:
                    net.demand.append((int(_num(r.get("o_zone_id"))),
                                       int(_num(r.get("d_zone_id"))), vol))
    return net
