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
`2` before returning to the completed project.

Only the selected writer branch starts in either mode. The other writer is not
left running after the XOR convergence, which makes the example safe without
depending on cancellation of a losing timer.

The resources are **Structurally validated** with WolvenKit `8.19.0`.
Follow [Test both Signal Race routes](../../../book/src/gates/lab-02-test.md)
for the in-game checks.

## Save warning

All five `cqa002_*` facts and the quest/journal lifecycle are save-backed. Use
separate untouched pre-Lab-2 saves for the canonical mode-2 run and the edited
mode-1 run. A console fact reset is useful for diagnosis but is not a clean test.
