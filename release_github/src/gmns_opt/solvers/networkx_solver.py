"""Tier-0 network algorithms via networkx (shortest path, min-cost flow, max-flow)."""
from __future__ import annotations
from .base import SolverAdapter


class NetworkXSolver(SolverAdapter):
    name = "networkx"; tier = 0; classes = ["LP", "network_flow"]
    def available(self) -> bool:
        try:
            import networkx  # noqa: F401
            return True
        except Exception:
            return False
