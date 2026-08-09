# Test Handoff Point

Lab 4 crosses root registration, external child resolution, root-owned prefab
scope, world streaming, journal/mappin state, and two saveable phase owners. A
final quest screenshot cannot identify which boundary worked. This protocol
binds the installed candidate, clean-save lineage, visible handoff, and fresh
logs across eight executions.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

**Lab 4 runtime evidence:** **Experimental** — pending.

Use the packaged `runtime-acceptance.json` schema version `3`. Do not replace
it with an unstructured pass/fail note. Only every required case passing can
promote `cqa004` to **Runtime-proven**. The promotion applies to normal `Out1`
handoff only; `CutDestination` remains unwired and outside the matrix.

## Required environment

| Component | Exact version |
| --- | --- |
| Cyberpunk 2077 for Windows (GOG) | `2.31a` (public patch `2.31`) |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Record observed versions on every run. Values printed in the template are
requirements, not proof of the machine that executed it.

## Establish the site before installation

Lab 4 uses the same Allen Street test site and trigger geometry as Lab 3. Its
center is the outdoor recycling-station cabinet row in Watson/Kabuki at:

```text
(-1000.02, 1497.2208, 8.3)
```

Before installing any Lab 4 candidate, follow Lab 3's
[ordinary control-route procedure](../world/lab-03-test.md#establish-the-site-and-ordinary-control-route).
It cites the vanilla fast-travel entity, linked marker, exact depot resources,
and extraction steps. Do not use Lab 4's own marker as the only way to find a
marker that is under test.

Treat access to the route and the new `cqa004` world resources as
**Experimental** until performed on the pinned game build. If the ordinary
route is inaccessible, record that result. Do not silently substitute a
console teleport.

## Prepare clean-save provenance

Before installing either checkpoint:

1. choose a manual save made at Allen Street with no history of any Lab 4
   candidate;
2. confirm the player is outside the 25-metre reach volume and can approach
   the cabinet row by the verified ordinary route;
3. copy the complete save-slot directory into private evidence storage;
4. record its in-game label and slot-directory name;
5. hash `sav.dat` and set `created_before_first_install: true` only after
   confirming that history;
6. preserve that original byte-for-byte for both `clean-walk` and
   `clean-replay`;
7. derive separate active-child saves before reach and between boundaries;
8. derive a separate parent-active save during the 30-second confirmation;
9. preserve the completed save used by both completed-state cases.

Use a fresh working-copy slot directory for every execution, even when two
runs restore the same preserved source. The `clean-walk`/`clean-replay`,
`pre-reach-reload`/`stream-away-return`, and
`completed-reload`/`completed-reinstall` pairs must each record one shared
`sav.dat` hash. Those three source classes, the between-boundaries save, and
the parent-confirmation save must have distinct hashes from one another.

Do not obtain “clean” evidence by writing `cqa004_completed = 0`, removing the
mod after a prior load, or reusing a slot that saw the start checkpoint.
FactsDB, journal, phase, mappin, and world state can all survive those actions.

## Build and bind the canonical candidate

Use the unmodified completed checkpoint:

```text
candidate id: canonical
project:      CQA_Lab04_HandoffPoint.cpmodproj
```

1. Close the game.
2. Build and install through WolvenKit.
3. Confirm only this candidate's pair is installed:

   ```text
   archive\pc\mod\CQA_Lab04_HandoffPoint.archive
   archive\pc\mod\CQA_Lab04_HandoffPoint.archive.xl
   ```

4. Hash both installed files in `candidates[0].installed_files`.
5. Confirm the record lists all seven depot resources, including the child and
   both sectors reached through the block.
6. Preserve those installed files until all eight executions finish.

From the game directory, PowerShell can produce the two hashes:

```powershell
Get-FileHash -Algorithm SHA256 `
  .\archive\pc\mod\CQA_Lab04_HandoffPoint.archive
Get-FileHash -Algorithm SHA256 `
  .\archive\pc\mod\CQA_Lab04_HandoffPoint.archive.xl
```

Hash the installed files, not the ZIP. Packing and the loose registration file
are both part of the runtime candidate.

## Preflight the ownership boundary

Before Run 1, inspect the installed `.archive.xl` and record:

- exactly one `quest.phases` entry, for `cqa004.questphase`;
- no independent entry for `cqa004_boundary.questphase`;
- the journal, onscreen localization, and streaming block entries;
- no `cqa004` error in a fresh ArchiveXL startup log.

This preflight does not prove the child executes. It proves the candidate under
test has the intended one-root registration shape.

## Run 1: clean walk

Restore a working copy of the original untouched save, keep the canonical
candidate installed, and start a fresh execution.

### Before entering the reach volume

Record all of these visible and state observations:

- Handoff Point, its phase, and `Reach the handoff point.` become active once;
- the handoff map pin becomes active once and points to the marker;
- the leave and confirmation objectives are not active;
- no second root or duplicate child activation appears.

The active reach objective and pin show child-owned work, but do not by
themselves prove the prefab scope is correct. The trigger crossing and logs are
also required.

### Cross the reach boundary

Walk to the cabinet row and cross into the 25-metre reach volume. Confirm:

- the pin becomes inactive;
- the reach objective succeeds once;
- `Clear the handoff area.` becomes active once;
- the quest does not yet show the confirmation objective;
- the quest does not take its completed-save bypass.

Remain inside the 110-metre leave volume long enough to confirm the leave gate
does not immediately complete.

### Cross the leave boundary and observe return

Leave the 110-metre volume by ordinary movement. As soon as the leave objective
succeeds, observe the child-to-parent boundary:

1. `Wait for handoff confirmation.` becomes active once;
2. the reach and leave sequence does not restart;
3. after 30 realtime seconds, confirmation and phase succeed;
4. the completion-fact write is reached before final quest success;
5. the quest succeeds once.

The confirmation objective is the visible evidence that child `Out1` reached
parent node `13.Out1 -> 14.Active`. Preserve a derived save during this window
for Run 4 and the final completed save for Runs 6 and 7.

Copy and hash all four fresh logs before another execution can replace them.

## Run 2: pre-reach reload

Restore the derived save made after the child activated but before reaching
the 25-metre volume.

1. Load without changing the installed candidate.
2. Confirm the reach objective and pin return once.
3. Confirm leave and confirmation are not yet active.
4. Enter reach, remain inside leave, then walk outside.
5. Confirm the child returns once and the parent completes once.
6. Retain the save hash, observations, and four fresh logs.

Pass requires coherent active-child restoration. Restarting the root flow or
duplicating the pin is a failure even if the quest eventually completes.

## Run 3: between-boundaries reload

Restore the derived save made after reach succeeded while the player remained
inside the leave volume.

1. Confirm reach remains succeeded and the handoff pin remains inactive.
2. Confirm leave is active and confirmation is not active.
3. Wait briefly without crossing; the child must not return yet.
4. Walk outside the leave volume.
5. Confirm leave succeeds, confirmation activates once, and completion follows
   once.
6. Retain the save hash, observations, and four fresh logs.

Immediate completion on load is a failure unless the retained position is
actually outside the authoritative leave volume.

## Run 4: post-return reload

Restore the derived save made after the child returned and while the parent's
30-second confirmation delay was active.

1. Confirm the confirmation objective is active.
2. Confirm reach and leave do not reactivate and no pin returns.
3. Observe whether the realtime delay resumes or restarts; record the measured
   result rather than assuming one.
4. Confirm the parent succeeds confirmation, phase, fact, and quest once.
5. Retain the save hash, timing observation, and four fresh logs.

Pass requires a coherent parent-owned continuation. The matrix records timing
semantics; the procedure does not pre-label resume versus restart.

## Run 5: stream away and return while child is active

Restore a working copy of the active-before-reach child save.

1. Travel by ordinary movement beyond the finite Quest descriptor box; do not
   use fast travel for this case.
2. Remain away long enough to collect a clear before/away/return observation.
3. Return by ordinary movement to the site.
4. Confirm the reach objective and pin remain coherent.
5. Cross reach and leave, then confirm one child return and one parent
   completion.
6. Retain route notes, save hash, observations, and four fresh logs.

This case tests active composition across world streaming. It does not test
`CutDestination` and does not generalize to every prefab lifetime.

## Run 6: completed reload

Restore the completed save made by Run 1 with the unchanged canonical
candidate installed.

Confirm:

- Handoff Point remains completed;
- reach, leave, pin, and confirmation do not reactivate;
- the external child is not invoked again;
- fresh logs contain no `cqa004` error.

This is the completed-route bypass, not a second successful playthrough.

## Run 7: completed reinstall

1. Close the game.
2. Remove only the two installed canonical files.
3. Reinstall the identical saved canonical pair and verify their hashes are
   unchanged.
4. Load the same completed save.
5. Confirm the quest remains completed and the child does not restart.
6. Confirm ArchiveXL registers the root without a separate child entry.
7. Retain four fresh logs.

Do not rebuild between removal and reinstall. A changed archive is a new
candidate and invalidates the shared record.

## Run 8: clean replay

Restore a fresh working copy of the original untouched pre-install save while
the canonical candidate remains installed.

Repeat the ordinary walk and record the full sequence:

```text
root first-run route
  -> child reach/pin
  -> child leave
  -> child Out1
  -> parent confirmation
  -> parent completion
```

Every transition must occur once with the same candidate hashes and no
`cqa004` errors. This verifies reproducibility from a second clean derivation;
it does not erase the need for the six boundary-specific runs.

## Retain four logs per execution

After each of the eight runs, copy these files into a run-specific private
evidence directory before starting the next execution:

```text
red4ext\plugins\ArchiveXL\ArchiveXL.log
red4ext\logs\red4ext.log
red4ext\logs\game.log
r6\logs\redscript_rCURRENT.log
```

Hash every copied log and store the paths/hashes in that run's `logs` array.
Search all four for `cqa004`, the child depot path, NodeRef errors, streaming
errors, journal/localization errors, and framework failures. “No visible
crash” is not an adequate log result.

## Complete schema version 3

Edit the packaged `runtime-acceptance.json` only as an evidence record. Do not
change its run IDs, case IDs, expected behavior, or promotion rule to fit an
unexpected result.

For `candidates[0]`, fill both installed SHA-256 values and retain all seven
depot paths. For every run, fill:

- `performed_at` and `tester`;
- every observed environment version;
- save label, slot directory, `created_before_first_install`, and `sav.dat`
  SHA-256;
- the four retained log paths and SHA-256 values.

For every case, set `status` to `passed` or `failed`, describe `observed`, and
list concrete evidence paths. Use ISO 8601 timestamps with a UTC offset. Each
completed case needs focused, hash-bound evidence under
`completed/evidence/`. Sanitize notes, screenshots, log excerpts, or save
metadata before committing. Do not commit `sav.dat`, private identifiers,
extracted vanilla resources, or a large unreviewed capture.

The eight fixed case IDs are:

| Case ID | Boundary proved |
| --- | --- |
| `clean-walk` | Ordinary root -> child -> parent -> completion route |
| `pre-reach-reload` | Child active before first trigger |
| `between-boundaries-reload` | Child active after reach and before leave |
| `post-return-reload` | Parent active after child return |
| `stream-away-return` | Active child across finite-sector streaming |
| `completed-reload` | Completion guard after reload |
| `completed-reinstall` | Completion guard after identical reinstall |
| `clean-replay` | Reproducible second clean run |

Promotion requires all eight cases to pass and evidence to bind the exact
candidate, executions, original and derived saves, versions, observations,
and all four logs per execution. If any required case is pending or failed,
the chapter remains **Experimental**.

Every edit to `completed/runtime-acceptance.json` changes the file hash bound
by `completed/example.json`. From the repository root, recompute it with:

```powershell
(Get-FileHash -Algorithm SHA256 .\examples\lab-04-handoff-point\completed\runtime-acceptance.json).Hash.ToLowerInvariant()
```

Replace `artifacts.files["runtime-acceptance.json"]` in the completed manifest
with that value. After any case is completed, update
`evidence.runtime.status`, `class`, and `date` to match the derived state. The
date is the calendar date of the chronologically latest completed execution;
it remains `null` only while every case is pending.

Status rules are:

- any failed required case makes top-level status `failed` and keeps
  `evidence_class: experimental`;
- a mixture of pending and passed cases keeps status `pending` and class
  `experimental`;
- only all required cases passed permits status `passed` and class
  `runtime-proven`.

Synchronize the first Lab 4 marker on every marked status surface, including
the evidence/version matrix. If the full matrix passes, that marker is exactly:

```text
**Lab 4 runtime evidence:** **Runtime-proven** — passed.
```

A failed matrix uses:

```text
**Lab 4 runtime evidence:** **Experimental** — failed.
```

Record the derived runtime date on all three Lab 4 practical pages for any
completed execution, including a failed result or a partially completed
matrix. As a repository-maintainer step, regenerate the four deterministic
Lab 4 SVGs with `python -B scripts\build_lab04_diagrams.py` so their evidence
footer carries the same status and date, then run
`python -B scripts\validate.py`. Stale record hashes, markers, dates, or
diagrams must fail validation.

`CutDestination` remains **Experimental** even after normal-handoff promotion,
because the candidate contains no cut edge and the promotion rule excludes it.

## Common test failures

| Observation | Classification and next check |
| --- | --- |
| Parent registered, child path error in log | Failed external resolution; verify packed path and soft `phaseResource` |
| Child appears to run twice | Failed lifecycle; verify clean save, one root registration, and no duplicate candidate |
| Trigger refs fail only from child | Failed candidate; inspect root prefab, child/instance empty lists, full world binding, and hashes before changing declarations |
| Leave succeeds but confirmation never activates | Failed handoff; inspect child output and parent `13.Out1 -> 14.Active` |
| Reload before reach restarts journal/pin | Failed active-child recovery, even if later completion succeeds |
| Post-return reload restarts child | Failed owner transition; retain evidence before editing the graph |
| Completed reinstall starts child again | Failed one-shot persistence or candidate identity |
| A cut path is untested | Expected scope boundary; do not mark cut runtime-proven |
| One log is missing | That execution cannot satisfy promotion until rerun with complete evidence |

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Author
Handoff Point in WolvenKit](lab-04-authoring.md) · Next lab: [Lab 5: First
Contact](../scenes/lab-05.md).
