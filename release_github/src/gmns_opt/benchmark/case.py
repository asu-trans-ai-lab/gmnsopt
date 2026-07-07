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
from ..models import shortest_path, min_cost_flow, traffic_assignment
from .report import write_outputs

DISPATCH = {
    "shortest_path": lambda net, p: shortest_path(net, p["origin"], p["destination"],
                                                  weight=p.get("weight", "fftt_min"),
                                                  by_zone=p.get("by_zone", True)),
    "min_cost_flow": lambda net, p: min_cost_flow(net, p["supplies"], weight=p.get("weight", "fftt_min"),
                                                  by_zone=p.get("by_zone", True), scale=p.get("scale", 1)),
    "traffic_assignment": lambda net, p: traffic_assignment(net, max_iter=p.get("max_iter", 60),
                                                            gap_tol=p.get("gap_tol", 1e-4),
                                                            by_zone=p.get("by_zone", True)),
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

    result = DISPATCH[ptype](net, problem.get("params", {}) or {})
    result["problem"] = problem
    result["network_stats"] = report["stats"]
    if write:
        out = os.path.join(case_dir, "output")
        write_outputs(out, problem, result, report)
        result["output_dir"] = out
    return result
