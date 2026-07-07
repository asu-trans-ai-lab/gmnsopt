# Vision

GMNS4Optimization is an **open-science benchmark and modeling ecosystem** that turns GMNS networks into
**dynamic, stochastic, multimodal, high-dimensional** transportation optimization test cases for classical
solvers, commercial solvers, neural optimization, RL/control, CAV, UAM, logistics, resilience, and
planning/operations applications.

Unlike generic solver benchmarks (e.g. MIPLIB), transportation semantics are preserved rather than flattened
into anonymous MIPs: origins, destinations, modes, paths, time stages, scenarios, queues, signals, incidents,
CAV penetration, UAM operations, accessibility, emissions, equity, and real-world constraints. Every case is
**both a mathematical program and a visual transportation scenario** with a common data + output contract.

Three audiences, one contract: **students** learn optimization foundations; **researchers** compare exact /
heuristic / neural / RL methods; **agencies** see how optimization decisions affect traffic, queues,
accessibility, reliability, emissions, and equity. See `application_taxonomy.md`, `tensor_framework.md`,
`benchmark_ladder.md`.
