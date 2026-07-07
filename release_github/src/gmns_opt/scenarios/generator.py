"""Deterministic scenario generator: perturb a base GMNS case into named scenarios.

Families: normal, capacity_drop, demand_surge, work_zone, weather, cav_penetration, uam_weather_restriction.
Writes `optional_input/scenario.csv` (scenario_id, family, target_type, target_id, param, value) describing
the perturbation, so downstream models (e.g. resilience_scenario) apply it. Fixed seeds -> reproducible.
"""
from __future__ import annotations
import csv
import os
from typing import List, Optional

FAMILIES = ["normal", "capacity_drop", "demand_surge", "work_zone", "weather",
            "cav_penetration", "uam_weather_restriction"]


def generate_scenarios(case_dir: str, scenario_type: str = "capacity_drop",
                       links: Optional[List[int]] = None, drop: float = 0.5,
                       factor: float = 1.3, seed: int = 12345) -> str:
    """Write `optional_input/scenario.csv` for the requested scenario. Returns the path."""
    if scenario_type not in FAMILIES:
        raise ValueError(f"unknown scenario_type '{scenario_type}'. Known: {FAMILIES}")
    out_dir = os.path.join(case_dir, "optional_input")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "scenario.csv")
    rows = []
    sid = f"{scenario_type}_{seed}"
    if scenario_type == "normal":
        rows.append(dict(scenario_id="normal", family="normal", target_type="global",
                         target_id="", param="multiplier", value=1.0))
    elif scenario_type in ("capacity_drop", "work_zone", "weather"):
        p = drop if scenario_type == "capacity_drop" else (0.6 if scenario_type == "work_zone" else 0.2)
        for lid in (links or []):
            rows.append(dict(scenario_id=sid, family=scenario_type, target_type="link",
                             target_id=lid, param="capacity_drop_fraction", value=p))
        if not links:
            rows.append(dict(scenario_id=sid, family=scenario_type, target_type="global",
                             target_id="", param="capacity_drop_fraction", value=p))
    elif scenario_type == "demand_surge":
        rows.append(dict(scenario_id=sid, family="demand_surge", target_type="global",
                         target_id="", param="demand_multiplier", value=factor))
    elif scenario_type == "cav_penetration":
        rows.append(dict(scenario_id=sid, family="cav_penetration", target_type="global",
                         target_id="", param="cav_share", value=min(max(factor - 1.0, 0.0), 1.0) or 0.3))
    elif scenario_type == "uam_weather_restriction":
        rows.append(dict(scenario_id=sid, family="uam_weather_restriction", target_type="air_corridor",
                         target_id="all", param="availability", value=1.0 - drop))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["scenario_id", "family", "target_type", "target_id", "param", "value"])
        w.writeheader(); w.writerows(rows)
    return path
