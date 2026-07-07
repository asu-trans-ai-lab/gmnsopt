# Contributing (dev)

- Language: **English only** in code, docs, and dev materials.
- Keep the core dependency-light (numpy/scipy/networkx/pyyaml); put heavy solvers/ML in optional extras.
- Every new model template returns `{objective, solution, objective_trace, constraint_status, meta}` and
  ships with a case folder (problem.yml + README + formulation + input/) and a test.
- Run `pytest -q` and `ruff check` before a PR. New cases must `gmns-opt run` cleanly and emit the standard
  output set.
- Bundled networks must carry upstream attribution/license (see references/).
