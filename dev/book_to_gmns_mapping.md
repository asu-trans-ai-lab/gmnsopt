# Teaching backbone: optimization book -> GMNS-native cases

The reference textbook (references/) provides the teaching structure:
optimization foundations -> modeling tricks -> practical cases -> solver implementation -> debugging/IIS/tuning.
gmns4optimization reuses that structure but replaces generic cases with GMNS-native transportation cases.

| book foundation | gmns4optimization translation |
|---|---|
| LP / MIP / QP / SOCP | shortest path, min-cost flow, traffic assignment, capacity design |
| Big-M logic | signal control, lane-use control, work-zone scheduling, if-then restrictions |
| linearization | BPR/QVDF approximation, queue constraints, flow×binary products |
| McCormick envelope | bilinear pricing, capacity-flow interaction, demand-control interaction |
| complexity theory | why network design, VRP, signal coordination, dynamic assignment are hard |
| VRP / VRPTW / EVRPTW | freight, delivery, transit, EV charging, UAM/logistics |
| pickup-delivery | paratransit, school bus, ride-hailing, drayage |
| drone-truck delivery | UAM + ground logistics, emergency/medical delivery |
| IIS / infeasibility | broken demand, disconnected network, impossible timing diagnosis |
| solver tuning / callbacks | large-scale network optimization, column generation, lazy constraints |

Start from clean mathematical-programming foundations, then move to dynamic, stochastic, real-world cases.
