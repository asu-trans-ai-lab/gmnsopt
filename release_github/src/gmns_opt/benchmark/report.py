"""Write the standard case output set (solution / objective_trace / constraint_status / summary.md)."""
from __future__ import annotations
import os
import csv


def _write_rows(path, rows):
    if not rows:
        open(path, "w").close(); return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def write_outputs(out_dir, problem, result, validation):
    os.makedirs(out_dir, exist_ok=True)
    _write_rows(os.path.join(out_dir, "solution.csv"), result.get("solution") or
                ([{"path_node": n} for n in result.get("path", [])]))
    _write_rows(os.path.join(out_dir, "objective_trace.csv"), result.get("objective_trace", []))
    _write_rows(os.path.join(out_dir, "constraint_status.csv"), result.get("constraint_status", []))
    if result.get("scenario_summary"):
        _write_rows(os.path.join(out_dir, "scenario_summary.csv"), result["scenario_summary"])
    if result.get("solution") and isinstance(result["solution"], list) and result["solution"] \
            and isinstance(result["solution"][0], dict) and "variable" in result["solution"][0]:
        _write_rows(os.path.join(out_dir, "decision_variable.csv"), result["solution"])

    st = result.get("network_stats", {}); meta = result.get("meta", {})
    lines = [f"# {problem.get('problem_name', 'case')} — result summary\n",
             f"- **problem_type:** `{problem.get('problem_type')}`",
             f"- **objective:** {result.get('objective')}",
             f"- **network:** {st.get('nodes')} nodes, {st.get('links')} links, {st.get('zones')} zones, "
             f"{st.get('od_pairs')} OD pairs (demand {st.get('total_demand')})"]
    for k, v in meta.items():
        lines.append(f"- **{k}:** {v}")
    if result.get("objective_trace"):
        last = result["objective_trace"][-1]
        lines.append(f"- **converged trace (last):** {last}")
    if validation.get("warnings"):
        lines.append(f"\n> validation warnings: {len(validation['warnings'])} "
                     f"(e.g. {validation['warnings'][0]})")
    lines.append("\n*Outputs:* `solution.csv`, `objective_trace.csv`, `constraint_status.csv`. "
                 "Visualize with `gmns_opt.viz` / GUI4GMNS.")
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
