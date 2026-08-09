# Completed checkpoint

**Lab 2 runtime evidence:** **Experimental** — pending.

This WolvenKit project contains the completed `cqa002` Signal Race resource
set. It teaches the difference between an immediate condition and a pause
condition, a Boolean `AND` condition tree, ordinary-socket fan-out, parallel
monitoring, and race-shaped convergence through a logical XOR node.

Expected depot paths:

```text
mod\cqa\cqa002\phases\cqa002.questphase
mod\cqa\cqa002\journal\cqa002.journal
mod\cqa\cqa002\localization\en-us\onscreens\cqa002.json
```

The canonical project sets `cqa002_test_mode` exactly to `2`. Its selector
takes the 120-second stable branch, the `AND` pause gate observes both
`cqa002_signal_stop > 0` and `cqa002_test_mode == 2`, and the optional objective
succeeds. To exercise the failure branch, change only FactsDBManager node
`[11]` from exact value `2` to `1`, recook and repack, and use a different save
created before Lab 2 was first installed. The immediate selector then starts
the 30-second failure writer and the optional objective fails. Restore value
`2` before comparing the project with the canonical artifact hashes.

Only the selected writer branch starts in either mode. The other writer is not
left running after the XOR convergence, which makes the example safe without
depending on cancellation of a losing timer.

## Evidence

- All six checkpoint CR2W resources: **Structurally validated** by creating
  cooked resources and serializing them back to CR2W-JSON with WolvenKit
  8.19.0, then comparing decisive semantic `Data`.
- ArchiveXL registration: **Structurally validated** against the same
  questphase, journal, and onscreen registration shape used by Lab 1.
- Runtime behavior: **Experimental** until every required case in
  `runtime-acceptance.json` has hash-bound evidence from the pinned game stack.

`source/raw` contains review artifacts for the same mod-owned resources.
Readers author the nodes in WolvenKit and do not need the repository generator.

## Save warning

All five `cqa002_*` facts and the quest/journal lifecycle are save-backed. Use
separate untouched pre-Lab-2 saves for the canonical mode-2 run and the edited
mode-1 run. A console fact reset is useful for diagnosis but is not clean-save
acceptance evidence.
