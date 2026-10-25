# Completed checkpoint

**Lab 4 runtime evidence:** **Experimental** — pending.

This WolvenKit project contains the completed `cqa004` Handoff Point resource
set. The twelve-node root graph owns the one-shot guard, quest and phase state,
external-child invocation, a thirty-second realtime confirmation objective,
the sole `cqa004_completed` fact write, and quest completion. The key return
edge is `13.Out1 -> 14.Active`.

The ten-node child graph owns the reach objective, map-pin lifecycle,
`IsInside` reach wait, leave objective, and `IsOutside` leave wait before its
terminating `Out1` returns to the parent. Its `phasePrefabs` array is empty;
the root owns `#cqa004_pr_handoff`. The parent phase node's
`phaseInstancePrefabs` array is also empty.

The full prefab root is `$/mod/cqa/cqa004/#cqa004_pr_handoff`; its child refs
are `#cqa004_mp_handoff`, `#cqa004_tr_reach`, and `#cqa004_tr_leave`. The world
geometry intentionally matches Lab 3 so this lab changes phase ownership, not
location or trigger shape.

The seven resources are **Structurally validated** with WolvenKit `8.19.0`.
ArchiveXL registers the root, journal, localization, and streaming block;
the parent resolves the child from the archive. Follow
[Test Handoff Point](../../../book/src/questphases/lab-04-test.md) for the
in-game checks. `CutDestination` is unwired in this example.

## Save warning

Start every clean run outside the reach volume on an untouched pre-Lab-4 save.
Preserve distinct pre-reach, between-boundaries, post-return-confirmation, and
completed saves. A console fact reset is diagnostic only and is not a clean test.
