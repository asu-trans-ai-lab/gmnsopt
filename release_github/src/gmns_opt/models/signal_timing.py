"""Single-intersection green-split LP (Case family D — signal timing).

Given phases (demand q_p, saturation flow s_p), allocate green g_p within a fixed cycle to minimize a
demand-weighted red-time delay proxy:  min sum_p q_p (C - g_p)  <=>  max sum_p q_p g_p
s.t.  sum_p g_p = C - lost_total,  g_min <= g_p <= C - lost_total.  LP via scipy.linprog (HiGHS).
Reports green splits and the resulting degree of saturation X_p = q_p C / (s_p g_p).
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import linprog


def signal_timing(net, phases, cycle: float = 90.0, lost_time_per_phase: float = 4.0,
                  min_green: float = 7.0) -> dict:
    P = len(phases)
    q = np.array([float(p.get("demand", 0.0)) for p in phases])
    s = np.array([float(p.get("saturation", 1800.0)) for p in phases])
    names = [p.get("name", f"phase_{i+1}") for i, p in enumerate(phases)]
    lost_total = lost_time_per_phase * P
    green_avail = cycle - lost_total
    if green_avail < min_green * P:
        return {"objective": float("inf"), "solution": [], "constraint_status": [
            {"constraint": "cycle_feasibility", "status": "infeasible: cycle too short for min greens"}],
            "meta": {"feasible": False}}
    # maximize sum q_p g_p  ->  minimize -q . g
    A_eq = np.ones((1, P)); b_eq = [green_avail]
    res = linprog(-q, A_eq=A_eq, b_eq=b_eq, bounds=[(min_green, green_avail)] * P, method="highs")
    if not res.success:
        return {"objective": float("inf"), "solution": [], "meta": {"feasible": False, "detail": res.message}}
    g = res.x
    X = q * cycle / (s * np.maximum(g, 1e-6))               # degree of saturation
    # Webster uniform delay proxy (informational): d_p = 0.5 C (1 - g/C)^2 / (1 - min(X,0.99) g/C)
    lam = g / cycle
    d = 0.5 * cycle * (1 - lam) ** 2 / np.maximum(1 - np.minimum(X, 0.99) * lam, 1e-3)
    sol = [{"phase": names[i], "green_s": round(float(g[i]), 2), "demand_vph": round(float(q[i]), 1),
            "saturation_vph": round(float(s[i]), 1), "degree_of_saturation": round(float(X[i]), 3),
            "uniform_delay_s": round(float(d[i]), 2)} for i in range(P)]
    return {"objective": round(float((q * d).sum()), 2), "solution": sol,
            "objective_trace": [{"iteration": 0, "objective": round(float((q * d).sum()), 2), "gap": 0.0}],
            "constraint_status": [{"constraint": "cycle_length", "status": f"C={cycle}s, green_avail={green_avail}s"},
                                  {"constraint": "min_green", "status": "satisfied"},
                                  {"constraint": "oversaturation", "status": f"{int((X > 1).sum())} phases X>1"}],
            "meta": {"feasible": True, "cycle_s": cycle, "green_available_s": green_avail,
                     "max_degree_of_saturation": round(float(X.max()), 3),
                     "total_weighted_delay": round(float((q * d).sum()), 2)}}
