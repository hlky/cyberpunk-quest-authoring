# Questphases

Questphases are executable graphs that coordinate progression, state, journal
presentation, scenes, world objects, and child phases.

This section will cover:

- registering a root phase under `base\quest\cyberpunk2077.quest`;
- input, output, and termination nodes;
- root/child phase handoff;
- named outputs and scene outcomes;
- phase-prefab ownership and inheritance;
- facts, conditions, and journal operations;
- parallel branches, joins, races, and cleanup;
- save-safe one-shot and repeatable flows.

The book will begin with very small graphs and add one subsystem at a time.
