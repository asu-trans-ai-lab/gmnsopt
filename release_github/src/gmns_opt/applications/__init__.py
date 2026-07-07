"""Application taxonomy — the ten transportation optimization families.

Thin, registry-backed surface: the authoritative metadata lives in `gmns_opt.benchmark.registry`; this package
exposes it for discovery and groups families by maturity. See docs/application_taxonomy.md.
"""
from __future__ import annotations
from ..benchmark.registry import FAMILIES, list_families, get_family, ProblemFamily

BY_ID = {f.id: f for f in FAMILIES}
FAMILY_IDS = [f.id for f in FAMILIES]


def by_maturity(maturity: str):
    """Families at a given maturity: 'runnable' | 'scaffold' | 'planned'."""
    return [f for f in FAMILIES if f.maturity == maturity]


def runnable_models():
    """All registered runnable problem_type ids across families."""
    out = []
    for f in FAMILIES:
        out.extend(f.runnable_models)
    return sorted(set(out))


__all__ = ["FAMILIES", "FAMILY_IDS", "BY_ID", "list_families", "get_family", "ProblemFamily",
           "by_maturity", "runnable_models"]
