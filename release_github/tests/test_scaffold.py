"""Tests for the broader scaffold: registry, taxonomy, tensor, scenarios, ml, CLI, and new seed cases.
Existing kernel tests live in test_gmns_opt.py and must keep passing."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
CASES = os.path.join(ROOT, "cases")

from gmns_opt import read_gmns, run_case                       # noqa: E402
from gmns_opt.benchmark.registry import list_families, get_family  # noqa: E402
from gmns_opt.applications import FAMILY_IDS, by_maturity        # noqa: E402
from gmns_opt.tensor import demand_to_tensor, expand_demand_scenarios, validate_tensor  # noqa: E402
from gmns_opt.scenarios import generate_scenarios, FAMILIES as SCEN_FAMILIES  # noqa: E402
from gmns_opt.ml import extract_features, WarmStarter           # noqa: E402
from gmns_opt.solvers import solver_status                      # noqa: E402


def test_registry_has_ten_families():
    fams = list_families()
    assert len(fams) == 10
    assert {f.id for f in fams} == set(FAMILY_IDS)
    assert get_family("signal_queue_control").maturity == "runnable"
    assert set(f.maturity for f in fams) <= {"runnable", "scaffold", "planned"}


def test_by_maturity_partitions():
    total = len(by_maturity("runnable")) + len(by_maturity("scaffold")) + len(by_maturity("planned"))
    assert total == 10


def test_demand_tensor_conversion_and_scenarios():
    net = read_gmns(os.path.join(CASES, "02_sioux_falls_assignment"))
    D = demand_to_tensor(net)
    assert D.nnz == len([1 for *_, v in net.demand if v > 0])
    assert abs(D.total() - sum(v for *_, v in net.demand)) < 1e-6
    assert validate_tensor(D)["ok"]
    Ds = expand_demand_scenarios(D, {"normal": 1.0, "demand_surge": 1.5})
    s_pos = Ds.axes.names.index("s")
    surge = sum(v for idx, v in Ds.data.items() if idx[s_pos] == "demand_surge")
    normal = sum(v for idx, v in Ds.data.items() if idx[s_pos] == "normal")
    assert abs(surge - 1.5 * normal) < 1e-3


def test_scenario_generator(tmp_path):
    import shutil
    dst = tmp_path / "case"
    shutil.copytree(os.path.join(CASES, "00_shortest_path_toy"), dst)
    for fam in ["capacity_drop", "demand_surge", "work_zone", "weather", "cav_penetration"]:
        p = generate_scenarios(str(dst), scenario_type=fam, links=[1, 2], drop=0.4)
        assert os.path.exists(p)
    assert set(["normal", "capacity_drop", "demand_surge"]).issubset(set(SCEN_FAMILIES))


def test_ml_features_and_warm_start():
    net = read_gmns(os.path.join(CASES, "02_sioux_falls_assignment"))
    feat = extract_features(net)
    assert feat["stats"]["n_links"] == 76 and len(feat["edge_index"]) == 76
    assert len(feat["link_feature_names"]) == len(feat["link_features"][0])
    ws = WarmStarter().predict(net)
    assert ws["link_flow"] and all(r["flow"] > 0 for r in ws["link_flow"])


def test_solver_status_tier0_available():
    st = {s["name"]: s for s in solver_status()}
    assert st["networkx"]["available"] and st["scipy_highs"]["available"]  # license-free tier-0 works


def test_new_seed_cases_run():
    for c in ["10_odme_inverse_toy", "11_resilience_capacity_drop_toy", "12_multimodal_cav_uam_skeleton"]:
        r = run_case(os.path.join(CASES, c), write=False)
        assert r["meta"]["feasible"]
    # odme toy actually improves the count fit
    od = run_case(os.path.join(CASES, "10_odme_inverse_toy"), write=False)
    assert od["meta"]["count_rmse_after"] <= od["meta"]["count_rmse_before"]
    # multimodal is a scaffold with a decision-variable schema placeholder
    mm = run_case(os.path.join(CASES, "12_multimodal_cav_uam_skeleton"), write=False)
    assert mm["meta"]["maturity"] == "scaffold" and mm["solution"]


def test_cli_list_families(capsys):
    from gmns_opt.cli import main
    assert main(["list-families"]) == 0
    out = capsys.readouterr().out
    assert "routing_accessibility" in out and "uam_air_ground_coordination" in out
