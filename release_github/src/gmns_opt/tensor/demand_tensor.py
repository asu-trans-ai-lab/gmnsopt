"""Convert a simple GMNS demand table into a demand tensor D[o, d, m, tau, s]."""
from __future__ import annotations
import csv
import json
import os
from .schema import SparseTensor, TensorAxes


def demand_to_tensor(net, mode: str = "auto", tau: int = 0, scenario: str = "normal") -> SparseTensor:
    """GMNSNetwork.demand [(o,d,vol)] -> D[o,d,m,tau,s]. Single mode/time/scenario slice by default."""
    axes = TensorAxes(names=["o", "d", "m", "tau", "s"])
    D = SparseTensor(name="demand", axes=axes)
    for (o, d, vol) in net.demand:
        D.set((o, d, mode, tau, scenario), vol)
    return D


def read_demand_table(path: str, mode: str = "auto", tau: int = 0, scenario: str = "normal") -> SparseTensor:
    """Read a demand.csv (o_zone_id,d_zone_id,volume[,mode,tau,scenario]) into D[o,d,m,tau,s]."""
    axes = TensorAxes(names=["o", "d", "m", "tau", "s"])
    D = SparseTensor(name="demand", axes=axes)
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            vol = float(r.get("volume") or 0)
            if vol <= 0:
                continue
            D.set((int(float(r["o_zone_id"])), int(float(r["d_zone_id"])),
                   r.get("mode", mode) or mode, int(float(r.get("tau", tau) or tau)),
                   r.get("scenario", scenario) or scenario), vol)
    return D


def export_tensor(t: SparseTensor, path: str) -> str:
    """Export a sparse tensor to CSV (one row per non-zero) or JSON (by extension)."""
    rows = t.to_rows()
    if path.lower().endswith(".json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"name": t.name, "axes": t.axes.names, "data": rows}, f)
    else:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        cols = t.axes.names + ["value"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    return path
