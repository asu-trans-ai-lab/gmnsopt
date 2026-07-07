"""Multimodal CAV / UAM air-ground coordination SKELETON (Case families cav_control, uam_air_ground).

This is a *scaffold*, not a solved model: it validates a GMNS-compatible multimodal schema (ground links, air
links, vertiport nodes, CAV/UAM modes, scenarios) and emits a decision-variable *schema* placeholder so the
case is dashboard-ready and clearly marks what a full solver must produce. TODO: implement the dynamic,
stochastic, multi-agent control model (MILP/RL) on the decision tensor x[o,d,m,p,tau,s,a].
"""
from __future__ import annotations


def multimodal_skeleton(net, modes=None, time_stages: int = 4, scenarios=None) -> dict:
    modes = modes or ["auto", "cav", "uam"]
    scenarios = scenarios or ["normal", "weather"]
    # classify links (air links flagged by free_speed high / a 'mode' tag would be in a full schema)
    air_links = [lk.link_id for lk in net.links if lk.free_speed >= 120]      # heuristic placeholder
    ground_links = [lk.link_id for lk in net.links if lk.link_id not in set(air_links)]
    vertiports = [nid for nid, a in net.nodes.items() if a.get("zone_id") is None][:5]  # placeholder

    # decision-variable SCHEMA placeholder over the tensor x[o,d,m,p,tau,s,a]
    decision_schema = [
        {"variable": "x_od_mode_path_time_scenario", "tensor_axes": "o,d,m,p,tau,s", "type": "continuous",
         "meaning": "passenger/vehicle flow by OD, mode, path, time stage, scenario", "value": "TODO"},
        {"variable": "dispatch_uam", "tensor_axes": "vertiport,tau,s", "type": "integer",
         "meaning": "UAM dispatch/reposition decisions", "value": "TODO"},
        {"variable": "control_cav", "tensor_axes": "control_zone,tau,s", "type": "continuous",
         "meaning": "CAV speed advisory / lane-use / ramp metering", "value": "TODO"},
        {"variable": "charge", "tensor_axes": "vehicle,tau,s", "type": "continuous",
         "meaning": "battery charging decisions", "value": "TODO"}]
    return {"objective": None, "solution": decision_schema,
            "objective_trace": [{"iteration": 0, "objective": None, "note": "scaffold: not solved"}],
            "constraint_status": [
                {"constraint": "vertiport_capacity", "status": "TODO"},
                {"constraint": "air_corridor_capacity", "status": "TODO"},
                {"constraint": "battery_reserve", "status": "TODO"},
                {"constraint": "mixed_traffic_safety_headway", "status": "TODO"},
                {"constraint": "ground_access_transfer_time", "status": "TODO"}],
            "meta": {"feasible": True, "maturity": "scaffold", "modes": modes, "time_stages": time_stages,
                     "scenarios": scenarios, "n_ground_links": len(ground_links),
                     "n_air_links_placeholder": len(air_links), "n_vertiports_placeholder": len(vertiports),
                     "note": "schema + decision-variable placeholder; full MILP/RL model is a roadmap item"}}
