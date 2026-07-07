"""Deterministic scenario generation for stochastic/robust benchmark cases (see docs/benchmark_ladder.md)."""
from .generator import generate_scenarios, FAMILIES
__all__ = ["generate_scenarios", "FAMILIES"]
