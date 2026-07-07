"""Tier-3 neural / GPU / RL placeholder (cuOpt, learned warm-start/branching, RL policies).
Optional; never required. TODO: wire gmns_opt.ml warm-start + RL policy interfaces here."""
from __future__ import annotations
from .base import SolverAdapter


class NeuralPlaceholder(SolverAdapter):
    name = "neural"; tier = 3; classes = ["warm_start", "branching", "RL", "surrogate"]
    def available(self) -> bool:
        for mod in ("torch", "cuopt"):
            try:
                __import__(mod); return True
            except Exception:
                continue
        return False
