# Completed checkpoint

**Lab 1 runtime evidence:** **Experimental** — pending.

This WolvenKit project contains the completed `cqa001` Lab 1 resource set.

Expected depot paths:

```text
mod\cqa\cqa001\phases\cqa001.questphase
mod\cqa\cqa001\journal\cqa001.journal
mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json
```

`source/raw` contains WolvenKit CR2W-JSON review artifacts for the same
mod-owned resources. They support deterministic diagrams and diffs; readers
are not expected to edit them.

The resources are **Structurally validated** with WolvenKit `8.19.0`.
Follow [Install, test, and reset](../../../book/src/start-here/install-and-test.md)
for the in-game checks.

## Save warning

`cqa001_completed` is persistent. Use a save that has never loaded this mod for
the first run. Reopening the same save should take the guard's `False` path and
terminate without reactivating the journal.

For a true replay, load a save created before the first installation. A console
fact edit is useful for diagnosis but is not equivalent to a a clean run because the journal and root questphase also have save-backed
state.
