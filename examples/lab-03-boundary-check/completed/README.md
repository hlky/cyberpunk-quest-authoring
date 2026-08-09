# Completed checkpoint

**Lab 3 runtime evidence:** **Experimental** — pending.

This WolvenKit project contains the completed `cqa003` Boundary Check
resource set. Its graph activates the quest, phase, reach objective, and map
pin; waits on `IsInside` for the 25-metre reach volume; retires the pin and
reach objective; activates the leave objective; then waits on `IsOutside` for
the 110-metre leave volume before completing once.

The completion guard is the only persistent fact:
`cqa003_completed`. The full prefab root is
`$/mod/cqa/cqa003/#cqa003_pr_boundary`; its nested local refs are
`#cqa003_mp_checkpoint`, `#cqa003_tr_reach`, and `#cqa003_tr_leave`.

The marker is centred at `(-1000.02, 1497.2208, 8.3)`. Trigger node-data Z is
`2.3` for the 12-metre-high reach outline and `0.3` for the 16-metre-high
leave outline. `AreaShapeOutline.buffer` is authoritative: if points or height
change, regenerate and verify the buffer too.

Both map-pin manager nodes use `disablePreviousMappins: 0`. This isolated lab
has no deliberate previous route to replace; the nodes' `Active` and
`Inactive` sockets request the two states.

## Evidence boundary

- The six cooked resources and their CR2W-JSON review artifacts are
  **Structurally validated** with WolvenKit 8.19.0.
- The resource shapes and selected location derive from Ghostline research,
  but no extracted vanilla resource is shipped.
- The synchronized marker above and `runtime-acceptance.json` govern ArchiveXL
  mounting, NodeRef resolution, streaming bounds, marker/GPS behavior, trigger
  transitions, and save/reload behavior. Pending or failed evidence is
  **Experimental**; only every required case passing is **Runtime-proven**.

Visible UI can demonstrate objective and pin transitions. It cannot by itself
prove which streaming sector resolved; bind runtime conclusions to candidate
hashes and logs as well.

## Save warning

Start every clean run outside the reach volume on an untouched pre-Lab-3
save. Preserve separate pre-reach, between-boundaries, and completed saves for
reload tests. A console fact reset is diagnostic only and is not clean-save
acceptance evidence.
