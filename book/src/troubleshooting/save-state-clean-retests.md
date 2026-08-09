# Save state and clean retests

The save is part of the candidate. Replacing an archive does not rewind facts,
journal state, active quest nodes, checkpoints, scenes, communities, or device
persistent state.

## Evidence and version boundary

Use Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31` for current acceptance.

**Structurally validated:** every lab acceptance record defines named starting
save classes, immutable pre-install assertions, installed hashes, and reload
cases. The record schema can validate metadata and retained evidence; it
cannot manufacture an in-game observation.

**Runtime-proven:** retained legacy delivery testing around archive
`1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC`
recorded that installing a rebuilt questphase did not rewind a save which had
already entered the earlier delivery phase. That bounded result justifies
treating saved graph progress as input, but does not prove any current lab
route under the pinned stack.

**Experimental:** a case remains experimental when its starting save is
unknown, was already exposed to another candidate, or differs from the
documented seed lineage.

## Choose the right save class

| Save class | Suitable use | Not suitable for |
| --- | --- | --- |
| Untouched pre-install original | First activation and clean replay | Routine play or destructive diagnosis |
| Closed-game full-slot clone of the original | Independent clean cases | Claiming a mid-flow resume state |
| Named mid-flow seed made under one exact candidate | Reload/stream/interruption cases defined at that point | First-install claims or a different candidate hash |
| Completed seed | Guard/reinstall/removal isolation | Replaying first activation |
| Old or unknown save | Negative diagnosis only | Positive acceptance evidence |

An eligible original is created before any version of the scoped quest was
installed or registered. Preserve it unchanged and run tests on clones.

## Clone a save safely

1. Exit to desktop and wait for the game process to close.
2. Record the source slot-directory name and visible save label.
3. Hash the source slot's canonical save artifact and record any metadata used
   by the lab acceptance form.
4. Copy the complete slot directory, not selected files, to a new unique slot.
5. Hash the clone and verify it matches the source capture before launch.
6. Assign that clone to one execution only.
7. Never refresh a failed case by copying files while the game is running.

Do not publish private save files. Retain hashes, labels, slot names, and
privacy-reviewed metadata or notes sufficient to identify the input.

## Inventory state domains before editing

| Domain | Example symptom after replacement |
| --- | --- |
| Fact database | Completion guard still bypasses the quest |
| Journal | Objective remains active/succeeded or a message stays visited |
| Quest graph/checkpoint | Execution resumes after the edited node instead of entering it |
| Scene | Active/interrupted state restores an older section or actor acquisition |
| Community | Entry remains active, spawned, or already cleaned up |
| Streaming world | Active world-dependent stage restores at a different load boundary |
| Device persistent state | Controller remembers interaction under the same NodeRef identity |

Resetting one fact does not clear the other rows. A save editor or console is
useful for a clearly labelled diagnostic, but its result is not a clean-save
acceptance case.

## Diagnose “works only on an old save”

Run a two-input comparison without changing installed bytes:

1. Hash the exact installed candidate and logs.
2. Load a clone of the untouched pre-install original and follow the shortest
   route to the symptom.
3. Exit fully; preserve observations and fresh logs.
4. Relaunch the same bytes and load the old/unknown save.
5. Compare the first visible divergence in facts, journal, active objective,
   actor/world state, or device state.

| Result | Interpretation |
| --- | --- |
| Clean clone passes, old save fails | Saved lifecycle is the leading boundary; do not rewrite structurally identical resources yet |
| Both fail at the same point | Save contamination is not sufficient to explain the failure |
| Old save passes, clean clone fails | Old state may bypass a broken first-run route |
| Results differ across launches with the same save and bytes | Preserve logs; investigate timing/streaming or duplicate installed resources |

An old completed save can make a broken first-run graph look healthy by taking
the completion guard directly to termination.

## Minimum lifecycle matrix

For a one-shot root, retain independent cases for:

1. **Clean activation:** untouched clone enters the first-run route once.
2. **Mid-flow reload:** a named seed resumes without duplicate activation or
   skipped required work.
3. **Completed reload:** completion state persists and the root guard bypasses
   replay.
4. **Identical reinstall:** reinstalling byte-identical candidate files does
   not erase completion.
5. **Clean replay:** another clone of the original repeats the first-run route.
6. **Removal isolation:** where the lab defines it, remove only the canonical
   candidate with the game closed and load an appropriate clone to prove the
   observed behavior depends on those mounted files.

World, scene, community, device, interruption, and stream-away cases add
separate seeds and oracles. Do not claim them from the five core cases or the
optional removal-isolation control.

## When a fresh NodeRef is also required

A clean save is the primary test for a stateful device. When a revision
deliberately changes the device's persistent identity or invalidates prior
controller state, author a fresh mod-owned NodeRef and test from a clean save.
Record that this is identity migration, not a generic fix for every device
problem.

Reusing the old NodeRef is appropriate when testing compatibility with old
state. Renaming it merely to escape an unexplained failure discards that
compatibility question.

## Keep candidate and save lineage together

Every runtime row should identify:

- archive and loose-file hashes;
- full required/absent mod inventory;
- framework and game versions;
- source capture and execution clone;
- expected and observed result;
- complete relevant log hashes;
- retained privacy-reviewed evidence;
- whether the run passed, failed, or could not be executed.

A seed created under candidate A is not positive evidence for candidate B,
even if their filenames match. If bytes change, regenerate the seed through
the documented route or explicitly test compatibility as a different case.

## Safe reset order

1. Preserve the failing candidate, save metadata, and logs.
2. Close the game.
3. Restore the exact intended installed files and verify hashes.
4. Restore or clone the correct save capture.
5. Launch once and collect a fresh complete log bundle.
6. Run only the assigned case.

Changing frameworks, candidate bytes, unrelated mods, and starting saves
together destroys the comparison.

Previous: [Journal, localization, and audio](journal-localization-audio.md).
Next: [Controlled isolation and evidence](controlled-isolation-evidence.md).
