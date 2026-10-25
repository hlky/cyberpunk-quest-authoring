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

The six resources are **Structurally validated** with WolvenKit `8.19.0`.
Follow [Test Boundary Check](../../../book/src/world/lab-03-test.md) for
streaming, trigger, marker, and reload checks.

## Save warning

Start every clean run outside the reach volume on an untouched pre-Lab-3
save. Preserve separate pre-reach, between-boundaries, and completed saves for
reload tests. A console fact reset is diagnostic only and is not a clean test.
