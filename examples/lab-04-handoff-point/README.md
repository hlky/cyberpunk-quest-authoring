# Lab 4 — Handoff Point

**Lab 4 runtime evidence:** **Experimental** — pending.

This directory contains two incremental WolvenKit checkpoints that split one
small world-integrated quest across a registered root questphase and an
archive-resolved external child questphase:

- `start`: seven complete mod-owned resources with a three-node parent and a
  two-node terminating child;
- `completed`: the same resources with the one-shot lifecycle and thirty-second
  confirmation in the parent, while the reach/leave sequence lives wholly in
  the child.

ArchiveXL registers the root phase, journal, localization, and streaming block.
It deliberately does not register `cqa004_boundary.questphase`: the parent
phase node resolves that archived child through its soft `phaseResource`.

The root owns `#cqa004_pr_handoff`. The child has no `phasePrefabs` entries and
the parent phase node has no `phaseInstancePrefabs`; the child nevertheless
uses the root-owned trigger NodeRefs. That exact scope arrangement is the
subject of the lab.

The cooked resources are **Structurally validated** with WolvenKit 8.19.0.
All `cqa004` mounting, external-child execution, world interaction, continuation,
streaming, and save behavior remains **Experimental** until
`runtime-acceptance.json` is completed.

Do not install both checkpoints together. They register the same depot paths.
