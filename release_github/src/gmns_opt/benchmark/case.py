"""Run a benchmark case: read `problem.yml` + GMNS `input/`, dispatch to a model, write `output/`.

Output set (the open-science case contract):
    output/solution.csv           per-link (or per-path) solution
    output/objective_trace.csv    iteration, objective, gap, ...   (convergence)
    output/constraint_status.csv  constraint, status               (feasibility)
    output/summary.md             human-readable headline + KPIs
"""
from __future__ import annotations
import os
import yaml
from ..io import read_gmns, validate_gmns
from ..models import (shortest_path, accessibility, min_cost_flow, max_flow, traffic_assignment,
                      system_optimal, odme, signal_timing, network_design, facility_location)
from .report import write_outputs

# each entry: (net, params, case_dir) -> result dict
DISPATCH = {
    "shortest_path": lambda net, p, cd: shortest_path(net, p["origin"], p["destination"],
                                                      weight=p.get("weight", "fftt_min"),
                                                      by_zone=p.get("by_zone", True)),
    "accessibility": lambda net, p, cd: accessibility(net, threshold_min=p.get("threshold_min", 30.0),
                                                      weight=p.get("weight", "fftt_min"),
                                                      decay=p.get("decay", 0.0)),
    "min_cost_flow": lambda net, p, cd: min_cost_flow(net, p["supplies"], weight=p.get("weight", "fftt_min"),
                                                      by_zone=p.get("by_zone", True), scale=p.get("scale", 1)),
    "max_flow": lambda net, p, cd: max_flow(net, p["source"], p["sink"], by_zone=p.get("by_zone", True)),
    "traffic_assignment": lambda net, p, cd: traffic_assignment(net, max_iter=p.get("max_iter", 60),
                                                                gap_tol=p.get("gap_tol", 1e-4),
                                                                by_zone=p.get("by_zone", True)),
    "system_optimal": lambda net, p, cd: system_optimal(net, max_iter=p.get("max_iter", 80),
                                                        gap_tol=p.get("gap_tol", 1e-4),
                                                        by_zone=p.get("by_zone", True)),
    "odme": lambda net, p, cd: odme(net, case_dir=cd, reg=p.get("reg", 0.1), by_zone=p.get("by_zone", True)),
    "signal_timing": lambda net, p, cd: signal_timing(net, p["phases"], cycle=p.get("cycle", 90.0),
                                                      lost_time_per_phase=p.get("lost_time_per_phase", 4.0),
                                                      min_green=p.get("min_green", 7.0)),
    "network_design": lambda net, p, cd: network_design(net, p["source"], p["sink"], p["flow"], p["budget"],
                                                        by_zone=p.get("by_zone", True),
                                                        candidate_link_ids=p.get("candidate_link_ids")),
    "facility_location": lambda net, p, cd: facility_location(net, p["k"], candidates=p.get("candidates"),
                                                             weight=p.get("weight", "fftt_min")),
}


def run_case(case_dir: str, write: bool = True) -> dict:
    """Run the case in `case_dir`. Returns the result dict; writes output/ when `write` is True."""
    with open(os.path.join(case_dir, "problem.yml"), encoding="utf-8") as f:
        problem = yaml.safe_load(f)
    ptype = problem["problem_type"]
    if ptype not in DISPATCH:
        raise ValueError(f"unknown problem_type '{ptype}'. Available: {sorted(DISPATCH)}")

    net = read_gmns(case_dir)
    report = validate_gmns(net)
    if not report["ok"]:
        raise ValueError(f"GMNS validation failed for {case_dir}: {report['errors'][:5]}")

    result = DISPATCH[ptype](net, problem.get("params", {}) or {}, case_dir)
    result["problem"] = problem
    result["network_stats"] = report["stats"]
    if write:
        out = os.path.join(case_dir, "output")
        write_outputs(out, problem, result, report)
        result["output_dir"] = out
    return result
