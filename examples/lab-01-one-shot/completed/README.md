# Completed checkpoint

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

## Evidence

- Questphase, journal, and localization CR2W-JSON: **Structurally validated**
  after deserialization and round-trip serialization with WolvenKit 8.19.0.
- ArchiveXL registration: **Structurally validated** against the documented
  ArchiveXL shape.
- Expected in-game behavior: **Experimental** until the complete checkpoint is
  exercised on a clean Cyberpunk 2077 2.31a save.

## Save warning

`cqa001_completed` is persistent. Use a save that has never loaded this mod for
the first run. Reopening the same save should take the guard's `False` path and
terminate without reactivating the journal.
