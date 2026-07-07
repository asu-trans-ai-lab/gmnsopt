"""Expand a base demand/capacity slice into scenario slices for D[o,d,m,tau,s] / C[link,tau,s].

Simple deterministic scenario families used by benchmark cases and the scenario generator:
  normal, incident, capacity_drop, demand_surge. Each returns a new SparseTensor scenario slice.
"""
from __future__ import annotations
from typing import Dict, List
from .schema import SparseTensor, TensorAxes


def expand_demand_scenarios(D_base: SparseTensor, scenarios: Dict[str, float]) -> SparseTensor:
    """Scale a normal-scenario demand tensor into multiple scenarios.

    `scenarios` maps scenario_name -> multiplier (e.g. {'normal':1.0,'demand_surge':1.3}). The demand tensor
    must have a trailing 's' axis; the base slice is read from scenario label 'normal'.
    """
    axes = D_base.axes
    s_pos = axes.names.index("s")
    out = SparseTensor(name=D_base.name, axes=axes)
    base = {idx: v for idx, v in D_base.data.items() if idx[s_pos] == "normal"}
    for sname, mult in scenarios.items():
        for idx, v in base.items():
            new = list(idx); new[s_pos] = sname
            out.set(tuple(new), v * mult)
    return out


def capacity_scenario(links, drop_link_ids: List[int], drop: float, tau: int = 0,
                      scenario: str = "capacity_drop") -> SparseTensor:
    """Build C[link, tau, s]: capacity per link, with `drop_link_ids` reduced by fraction `drop`."""
    axes = TensorAxes(names=["link", "tau", "s"])
    C = SparseTensor(name="capacity", axes=axes)
    dset = set(drop_link_ids)
    for lk in links:
        cap = lk.capacity * (1.0 - drop) if lk.link_id in dset else lk.capacity
        C.set((lk.link_id, tau, scenario), cap)
    return C
