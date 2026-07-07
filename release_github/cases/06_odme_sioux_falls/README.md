# GMNS-ODME-301 (static) — Sioux Falls OD estimation (inverse optimization)
Adjust the OD matrix to match observed link counts while staying near the prior (NNLS). Observed counts are
read from input/counts.csv if present, else synthesized (true OD = 1.2x base). OD pairs whose free-flow path
crosses no sensor are unobservable and kept at the prior (observability gate).
