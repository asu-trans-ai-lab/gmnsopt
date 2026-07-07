"""Benchmark category registry — the machine-readable taxonomy of transportation optimization families.

Each `ProblemFamily` records its formulation classes, required/optional GMNS files, required outputs, default
solver tier, visualization type, and maturity (runnable | scaffold | planned) plus the implemented model
templates (`problem_type` ids usable in a case `problem.yml`). This is the single source of truth surfaced by
`gmns-opt list-families` / `describe-family` and by `gmns_opt.applications`.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class ProblemFamily:
    id: str
    name: str
    formulation_classes: List[str]
    required_files: List[str]
    optional_files: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=lambda: ["solution.csv", "objective_trace.csv",
                                                        "constraint_status.csv", "summary.md"])
    default_solver_tier: int = 0
    visualization: str = "link_flow"
    maturity: str = "planned"                       # runnable | scaffold | planned
    runnable_models: List[str] = field(default_factory=list)   # registered problem_type ids
    subtypes: List[str] = field(default_factory=list)


FAMILIES: List[ProblemFamily] = [
    ProblemFamily(
        id="routing_accessibility", name="Routing & Accessibility",
        formulation_classes=["LP", "network_flow"],
        required_files=["node.csv", "link.csv"], optional_files=["zone.csv", "demand.csv", "transit_route.csv"],
        default_solver_tier=0, visualization="path_highlight", maturity="runnable",
        runnable_models=["shortest_path", "accessibility", "min_cost_flow"],
        subtypes=["shortest_path", "multimodal_path", "accessibility", "equity_aware_access"]),
    ProblemFamily(
        id="traffic_assignment_pricing", name="Traffic Assignment & Pricing",
        formulation_classes=["convex_NLP", "MIP", "dynamic", "stochastic"],
        required_files=["node.csv", "link.csv", "demand.csv"], optional_files=["toll.csv", "scenario.csv"],
        default_solver_tier=0, visualization="flow_height_speed_color", maturity="runnable",
        runnable_models=["traffic_assignment", "system_optimal"],
        subtypes=["user_equilibrium", "system_optimal", "dynamic_assignment", "congestion_pricing",
                  "managed_lane_control"]),
    ProblemFamily(
        id="odme_inverse_optimization", name="ODME & Inverse Optimization",
        formulation_classes=["LP", "QP", "NLP", "stochastic", "inverse"],
        required_files=["node.csv", "link.csv", "demand.csv"],
        optional_files=["counts.csv", "detector.csv", "trajectory.csv", "scenario.csv"],
        default_solver_tier=0, visualization="desire_line_delta", maturity="runnable",
        runnable_models=["odme"],
        subtypes=["od_matrix_estimation", "path_flow_correction", "sensor_residual_min", "demand_tensor_calibration"]),
    ProblemFamily(
        id="signal_queue_control", name="Signal & Queue Spillback Control",
        formulation_classes=["MIP", "dynamic", "stochastic", "RL_ready"],
        required_files=["node.csv", "link.csv", "demand.csv"],
        optional_files=["movement.csv", "signal_timing.csv", "detector.csv", "scenario.csv"],
        outputs=["solution_signal.csv", "queue_profile.csv", "constraint_status.csv", "objective_trace.csv"],
        default_solver_tier=0, visualization="phase_clock_queue_ribbon", maturity="runnable",
        runnable_models=["signal_timing"],
        subtypes=["signal_timing", "green_split_offset_phase", "queue_spillback", "corridor_mpc_milp_rl"]),
    ProblemFamily(
        id="resilience_workzone_incident", name="Resilience, Work-Zone & Incident",
        formulation_classes=["MIP", "stochastic", "dynamic", "robust"],
        required_files=["node.csv", "link.csv", "demand.csv"], optional_files=["scenario.csv", "resource.csv"],
        outputs=["scenario_summary.csv", "solution.csv", "constraint_status.csv", "objective_trace.csv"],
        default_solver_tier=0, visualization="warning_layer_before_after", maturity="runnable",
        runnable_models=["resilience_scenario", "max_flow"],
        subtypes=["incident_response", "work_zone_scheduling", "extreme_heat_weather_flood",
                  "evacuation_recovery"]),
    ProblemFamily(
        id="cav_control", name="CAV Mixed-Traffic Control",
        formulation_classes=["MIP", "QP", "NLP", "stochastic", "dynamic", "RL"],
        required_files=["node.csv", "link.csv", "demand.csv"],
        optional_files=["scenario.csv", "penetration.csv", "control_zone.csv"],
        outputs=["decision_variable.csv", "constraint_status.csv", "objective_trace.csv", "summary.md"],
        default_solver_tier=2, visualization="control_zone_speed", maturity="scaffold",
        runnable_models=["multimodal_skeleton"],
        subtypes=["mixed_traffic", "speed_advisory", "platooning", "lane_use_control", "ramp_metering",
                  "communication_failure"]),
    ProblemFamily(
        id="uam_air_ground_coordination", name="UAM Air–Ground Coordination",
        formulation_classes=["MIP", "stochastic", "dynamic", "RL"],
        required_files=["node.csv", "link.csv", "demand.csv"],
        optional_files=["vertiport.csv", "air_link.csv", "weather_scenario.csv", "charging_station.csv"],
        outputs=["decision_variable.csv", "constraint_status.csv", "objective_trace.csv", "summary.md"],
        default_solver_tier=2, visualization="vertiport_queue_3d", maturity="scaffold",
        runnable_models=["multimodal_skeleton"],
        subtypes=["vertiport_capacity", "dispatch_repositioning", "weather_uncertainty", "battery_charging",
                  "ground_access_integration"]),
    ProblemFamily(
        id="freight_ev_logistics", name="Freight, EV & Logistics Routing",
        formulation_classes=["MIP", "stochastic", "dynamic"],
        required_files=["node.csv", "link.csv"],
        optional_files=["vehicle.csv", "charging_station.csv", "delivery_demand.csv", "scenario.csv"],
        default_solver_tier=1, visualization="route_energy", maturity="scaffold",
        runnable_models=["facility_location"],
        subtypes=["vrp", "ev_routing_charging", "time_windows", "curb_depot_fleet", "truck_drone_uam"]),
    ProblemFamily(
        id="transit_frequency_accessibility", name="Transit Frequency & Accessibility",
        formulation_classes=["MIP", "LP", "stochastic"],
        required_files=["node.csv", "link.csv", "demand.csv"],
        optional_files=["transit_route.csv", "fleet.csv", "scenario.csv"],
        default_solver_tier=1, visualization="frequency_accessibility", maturity="planned",
        runnable_models=[],
        subtypes=["bus_frequency", "fleet_allocation", "first_last_mile", "transfer_coordination",
                  "equity_service"]),
    ProblemFamily(
        id="solver_learning_and_neural_optimization", name="Solver Learning & Neural Optimization",
        formulation_classes=["ML", "RL", "surrogate"],
        required_files=["node.csv", "link.csv", "demand.csv"], optional_files=["scenario.csv"],
        outputs=["features.json", "warm_start.csv", "objective_trace.csv", "summary.md"],
        default_solver_tier=3, visualization="convergence_panel", maturity="scaffold",
        runnable_models=["ml_features"],
        subtypes=["learning_to_warm_start", "learning_to_branch", "graph_neural_features", "neural_surrogate",
                  "rl_policy_interface", "train_val_test_city_split"]),
]

_BY_ID = {f.id: f for f in FAMILIES}


def list_families() -> List[ProblemFamily]:
    return list(FAMILIES)


def get_family(family_id: str) -> ProblemFamily:
    if family_id not in _BY_ID:
        raise KeyError(f"unknown family '{family_id}'. Known: {sorted(_BY_ID)}")
    return _BY_ID[family_id]
