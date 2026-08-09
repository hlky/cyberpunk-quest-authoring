# Lab 2 — Signal Race

**Lab 2 runtime evidence:** **Experimental** — pending.

This directory contains two WolvenKit checkpoints for the fact-only gate lab:

- `start`: the registered journal/localization resources and a minimal
  `Input -> Terminating Output` questphase;
- `completed`: the full immediate-branch, pause-gate, logical-AND, monitor, and
  XOR convergence graph for `cqa002`.

Both checkpoints contain only mod-owned resources. The completed project is
**Structurally validated** with WolvenKit 8.19.0. Its default
`cqa002_test_mode = 2` takes the 120-second stable route. Changing only node
`[11]` to set exact value `1`, rebuilding, and loading a separate untouched
pre-Lab-2 save exercises the 30-second failure route.

The graph uses facts and real-time delays, so it does not require world nodes,
communities, devices, or Ghostline tooling.
