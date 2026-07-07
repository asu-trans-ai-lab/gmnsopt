"""Tests: the three foundational cases run end-to-end and produce correct, feasible results."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
CASES = os.path.join(ROOT, "cases")

from gmns_opt import read_gmns, validate_gmns, run_case   # noqa: E402


def test_io_and_validation():
    net = read_gmns(os.path.join(CASES, "00_shortest_path_toy"))
    rep = validate_gmns(net)
    assert rep["ok"]
    assert rep["stats"]["nodes"] == 5 and rep["stats"]["links"] == 5
    assert rep["stats"]["od_pairs"] == 1


def test_shortest_path_toy():
    r = run_case(os.path.join(CASES, "00_shortest_path_toy"), write=False)
    assert r["meta"]["feasible"]
    assert r["path"] == [1, 2, 4, 5]        # shorter branch via node 2
    assert abs(r["objective"] - 6.0) < 1e-6  # (1+1+1) mi / 30 mph * 60 = 6 min


def test_min_cost_flow_toy():
    r = run_case(os.path.join(CASES, "01_min_cost_flow_toy"), write=False)
    assert r["meta"]["feasible"]
    assert abs(r["objective"] - 3600.0) < 1.0   # 600 units * 6 min
    assert sum(s["flow"] for s in r["solution"] if s["from_node"] == 1) == 600


def test_sioux_falls_ue_converges():
    r = run_case(os.path.join(CASES, "02_sioux_falls_assignment"), write=False)
    assert r["meta"]["feasible"]
    assert r["network_stats"]["links"] == 76 and r["network_stats"]["od_pairs"] == 528
    assert r["meta"]["final_relative_gap"] < 0.01        # Frank-Wolfe converged
    # Beckmann objective is finite and monotone-ish over the trace
    trace = r["objective_trace"]
    assert trace[-1]["relative_gap"] <= trace[0]["relative_gap"]
    assert all(s["voc"] >= 0 for s in r["solution"])


def test_outputs_written(tmp_path):
    import shutil
    dst = tmp_path / "case"
    shutil.copytree(os.path.join(CASES, "00_shortest_path_toy"), dst)
    run_case(str(dst), write=True)
    for fn in ("solution.csv", "objective_trace.csv", "constraint_status.csv", "summary.md"):
        assert (dst / "output" / fn).exists()
