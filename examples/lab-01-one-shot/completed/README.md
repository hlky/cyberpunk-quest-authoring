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

## Evidence

- Questphase, journal, and localization CR2W-JSON: **Structurally validated**
  after deserialization and round-trip serialization with WolvenKit 8.19.0.
- ArchiveXL registration: **Structurally validated** against the documented
  ArchiveXL shape.
- Runtime evidence: see the dedicated marker above and
  `runtime-acceptance.json`.

`example.json` binds the checked project artifacts to SHA-256 digests.
`runtime-acceptance.json` is the acceptance form for the candidate. Fill its
run provenance and observations from a
real play session, including the observed environment, both installed payload
hashes, the original slot's `sav.dat` hash, and all four log hashes. Then update
the artifact digest in `example.json`. Do not change `evidence_class` merely
because the archive packed or the game launched. Each passed or failed case uses
structured evidence objects that reference a real hash-matched file below an
`evidence/` directory; a note such as “worked” is not an acceptance artifact.

The full contributor promotion procedure is in the book's **Install, test,
and reset** chapter. Evidence files must also be added deliberately to the
checkpoint/package inventories before validation will accept them.

## Save warning

`cqa001_completed` is persistent. Use a save that has never loaded this mod for
the first run. Reopening the same save should take the guard's `False` path and
terminate without reactivating the journal.

For a true replay, load a save created before the first installation. A console
fact edit is useful for diagnosis but is not equivalent to a clean-save
acceptance run because the journal and root questphase also have save-backed
state.
