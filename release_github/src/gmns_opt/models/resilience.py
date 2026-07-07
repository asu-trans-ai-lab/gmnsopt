"""Resilience / work-zone / incident scenario comparison (Case family F).

Apply a capacity-drop scenario to target links, re-run user-equilibrium assignment, and compare the base vs
scenario system travel time. Reports the affected links and the delay increase — the core resilience KPI.
Reads target links/drop from params or from optional_input/scenario.csv (capacity_drop_fraction).
"""
from __future__ import annotations
import copy
import csv
import os
from .traffic_assignment import traffic_assignment


def resilience_scenario(net, drop_link_ids=None, drop: float = 0.5, case_dir=None,
                        max_iter: int = 60, gap_tol: float = 1e-4, by_zone: bool = True) -> dict:
    # scenario from file if present
    if drop_link_ids is None and case_dir:
        sp = os.path.join(case_dir, "optional_input", "scenario.csv")
        if os.path.exists(sp):
            drop_link_ids = []
            for r in csv.DictReader(open(sp, encoding="utf-8-sig")):
                if r.get("param") == "capacity_drop_fraction":
                    drop = float(r.get("value") or drop)
                    if r.get("target_type") == "link" and r.get("target_id"):
                        drop_link_ids.append(int(float(r["target_id"])))
    drop_link_ids = drop_link_ids or []

    base = traffic_assignment(net, max_iter=max_iter, gap_tol=gap_tol, by_zone=by_zone)
    base_tstt = base["meta"]["vmt_min_weighted"]

    scen = copy.deepcopy(net)
    dset = set(drop_link_ids)
    for lk in scen.links:
        if lk.link_id in dset:
            lk.capacity = max(lk.capacity * (1.0 - drop), 1e-6)
    scn = traffic_assignment(scen, max_iter=max_iter, gap_tol=gap_tol, by_zone=by_zone)
    scen_tstt = scn["meta"]["vmt_min_weighted"]

    base_by = {s["link_id"]: s for s in base["solution"]}
    affected = []
    for s in scn["solution"]:
        b = base_by.get(s["link_id"])
        if b and (s["link_id"] in dset or abs(s["flow"] - b["flow"]) > 1.0):
            affected.append({"link_id": s["link_id"], "base_flow": b["flow"], "scenario_flow": s["flow"],
                             "base_voc": b["voc"], "scenario_voc": s["voc"],
                             "dropped": s["link_id"] in dset})
    delta = scen_tstt - base_tstt
    summary = [{"scenario": "base", "tstt_min": round(base_tstt, 1)},
               {"scenario": "capacity_drop", "tstt_min": round(scen_tstt, 1),
                "delta_min": round(delta, 1), "pct_increase": round(100 * delta / max(base_tstt, 1e-9), 2),
                "dropped_links": ";".join(map(str, drop_link_ids)), "drop_fraction": drop}]
    return {"objective": round(scen_tstt, 1), "solution": affected, "scenario_summary": summary,
            "objective_trace": [{"iteration": 0, "objective": round(base_tstt, 1), "gap": 1.0},
                                {"iteration": 1, "objective": round(scen_tstt, 1), "gap": 0.0}],
            "constraint_status": [{"constraint": "flow_conservation", "status": "satisfied"},
                                  {"constraint": "capacity_drop_applied",
                                   "status": f"{len(dset)} links -{int(drop*100)}%"}],
            "meta": {"feasible": True, "base_tstt_min": round(base_tstt, 1),
                     "scenario_tstt_min": round(scen_tstt, 1), "delay_increase_min": round(delta, 1),
                     "pct_increase": round(100 * delta / max(base_tstt, 1e-9), 2),
                     "n_dropped_links": len(dset), "n_affected_links": len(affected)}}
