# ML for optimization (readiness)

**ML supports solvers and repeated scenarios; it does not replace rigorous optimization.** Always benchmark
learned methods against exact/heuristic baselines and check feasibility + out-of-distribution behavior.

Transportation has repeated structure (same city, many days/scenarios/incidents/signal plans/penetration
rates) — exactly where learning helps. `gmns_opt.ml` provides:

- `extract_features(net)` — node / link / demand / graph-adjacency features (GNN-ready `edge_index`).
- `WarmStarter` — learning-to-warm-start interface (default = free-flow all-or-nothing baseline; subclass with
  a learned model). Start here: warm start is easy, safe, and measurable.
- `BranchRecord` / `write_branching_dataset` — learning-to-branch dataset schema (imitation of strong branching).

Roadmap: neural diving, GNN embeddings, neural surrogate for DTA/simulation, RL control policies, and a
train/validation/test split **by city/scenario** with a feasibility checker. Every learned model is evaluated
against a solver baseline (Tier 0–2) on the same case contract.
