# Open-science test cases

Every case obeys the MIPLIB-style discipline **plus** transportation semantics. A complete case has:
problem statement (`README.md`), GMNS `input/`, mathematical `formulation.md`, `problem.yml` (machine-readable),
solver-ready model (optional `models/`), baseline solutions (optional `baselines/`), and `output/`
(`solution.csv`, `objective_trace.csv`, `constraint_status.csv`, `summary.md`, optional `decision_variable.csv`,
`scenario_summary.csv`, GUI4GMNS layers).

The five outputs that serve three communities at once:
- `objective_trace.csv` (solver + ML: convergence), `constraint_status.csv` (feasibility/diagnosis),
  `solution.csv`/`decision_variable.csv` (transportation + viz), `solver_log.txt` (solver devs),
  `simulation_check.csv` (transportation validation).

Bundled runnable cases: 00–12 (see README). Templates for all ten families: `case_templates/`. Add a case by
copying a template, filling `input/`, and registering a `problem_type` in `gmns_opt.benchmark.case:DISPATCH`.
Do not commit copyrighted data; keep everything English-only; add TODO markers for planned advanced models.
