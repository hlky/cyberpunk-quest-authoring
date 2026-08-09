# Test both Signal Race routes

Lab 2 has two reproducible source states and therefore needs two separately
identified runtime candidates. This protocol prevents a mode-1 failure run from
being mistaken for evidence about the canonical mode-2 archive.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

**Lab 2 runtime evidence:** **Experimental** — pending.

Use the packaged `runtime-acceptance.json` schema version 3. Do not replace it
with screenshots or an unstructured pass/fail note. Evidence can promote the
book only when every required case, both candidates, all six executions, both
untouched saves, the derived mid-flow/completed saves, installed payloads,
exact versions, and every execution's log set are hash-bound.

## Required environment

| Component | Exact version |
| --- | --- |
| Cyberpunk 2077 for Windows (GOG) | `2.31a` |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Record the observed values separately in each run. A required version printed
in the template is not evidence that the machine actually used it.

## Prepare two untouched saves

Before installing any Lab 2 checkpoint:

1. choose two manual saves that have never loaded a build registering
   `cqa002`;
2. copy each whole save-slot directory to retained evidence storage;
3. label one for `canonical-clean` and the other for
   `source-edit-failure`;
4. hash each slot's `sav.dat` and record the slot-directory name;
5. set `created_before_first_install: true` only after confirming that history.

A console reset of `cqa002_*` facts does not create a clean save. Neither does
removing the archive after an earlier load: journal, fact, and active-node state
may already be serialized.

## Build and bind the canonical candidate

Use the unmodified completed checkpoint:

```text
candidate id:       canonical-mode-2
node:               11
fact:               cqa002_test_mode
set exact value:    2
canonical:          true
```

1. Close the game.
2. Build and install the completed project with WolvenKit.
3. Verify that only these candidate files are installed:

   ```text
   archive\pc\mod\CQA_Lab02_SignalRace.archive
   archive\pc\mod\CQA_Lab02_SignalRace.archive.xl
   ```

4. Hash both installed files and enter the values under the
   `canonical-mode-2` candidate.
5. Confirm that all three registered depot paths in the record match the
   project.

Do not hash the source ZIP in place of the installed files. Packing is part of
the candidate.

## Run the canonical cases

Load only the save assigned to `canonical-clean`.

### Stable first run

Observe and record:

1. Signal Race activates once;
2. both objectives activate once;
3. the optional objective remains active before the roughly 120-second result;
4. it succeeds after roughly 120 seconds of unpaused observation;
5. the required objective and quest then succeed once;
6. waiting at least 30 additional seconds creates no second journal
   notification or visible reactivation.

This execution supplies `clean-save-stable-route`,
`immediate-selector-versus-pause`, and `logical-and-fulfilment`. The canonical
source configures the positive case in which both AND comparisons can be
fulfilled; the run records only its corresponding visible outcome. It does not
hold `signal_stop > 0` while mode is not `2`, so it cannot prove a one-child
negative control. Time observations should be measured and described; do not
infer the selector/monitor distinction only from the final journal screen.

### Mid-flow reload

Restore the untouched canonical save, start a separate execution, and save
after both objectives activate but while the optional objective is still
active before its roughly 120-second outcome. Reload that derived save. Record
this as `canonical-mid-flow-reload`: hash the mid-flow `sav.dat`, set
`save_state: mid-flow`, and retain fresh logs for this execution. Record
whether the remaining delay resumes, restarts, or behaves another way.

The required correctness result is eventual single completion without a
duplicate journal activation. The timing result is an observation, not a
preselected expectation.

### Completed reload and reinstall

Use another execution from the original canonical save. After completion:

1. make and retain a completed save;
2. hash it and use it for `canonical-completed-reload`;
3. reload it without changing the installed files and confirm there is no
   quest/objective reactivation or delayed visible journal update;
4. retain this execution's fresh logs;
5. close the game, remove and reinstall the **identical hash-bound** candidate;
6. use the same completed save for a new `canonical-reinstall` execution;
7. confirm there is still no reactivation and retain a new log set.

These are distinct cases. Rebuilding from unchanged-looking source is not an
identical reinstall unless the installed hashes match. The completed-save SHA
must match between the two execution records.

### Clean replay

Restore the original untouched canonical save directory, leave the identical
candidate installed, and repeat the stable route as `canonical-clean-replay`.
Its `sav.dat` hash must equal `canonical-clean`'s original pre-install hash.
Retain another fresh log set. The same player-facing result must occur once.

## Build and bind the source-edited candidate

Now close the game and remove the canonical archive and registration file.
Create the controlled edit described in the authoring chapter:

```text
candidate id:       source-edit-mode-1
node:               11
fact:               cqa002_test_mode
set exact value:    1
canonical:          false
```

Change no other property or resource. Build/install, hash the resulting archive
and `.archive.xl`, and enter them under `source-edit-mode-1`. The registration
file may hash identically to the canonical version; record the actual digest
rather than assuming it does.

Load only the second untouched save assigned to
`source-edit-failure`. Give it a distinct save label and retained slot
directory from the canonical original; its bytes may legitimately be identical
if both slots were copied from the same clean baseline. Confirm:

1. both objectives activate once;
2. the optional objective remains active before the 30-second result;
3. the optional objective then fails once;
4. the required objective and quest still succeed once;
5. waiting at least 30 additional seconds produces no unexpected duplicate
   completion in this controlled variant.

This supplies `source-edit-failure-route` and, together with the canonical
run, `xor-route-convergence`. The exact graph maps the two authored routes to
`In1` and `In2`; the player-visible runs show that both outcomes reach the
common completion sequence. They do not deliver both inputs during one
execution, so they do not prove winner, cancellation, repeat-emission, or
simultaneous-arrival policy.

## Retain logs per run

For each of the six executions, close the game after the required observations
and retain fresh copies of:

```text
red4ext\plugins\ArchiveXL\ArchiveXL.log
red4ext\logs\red4ext.log
red4ext\logs\game.log
r6\logs\redscript_rCURRENT.log
```

Hash all four files under that run. Search for the candidate registration file,
`cqa002`, and errors naming any registered depot path, journal lookup,
localization lookup, or condition resource. Clean logs establish that those
systems did not report an error; they do not replace the in-game route
observations.

## Complete schema version 3

The record has four provenance layers:

| Object | Required identity |
| --- | --- |
| `candidates[]` | Source mode plus installed archive/registration hashes |
| `runs[]` | Candidate ID, immutable save state/provenance, timestamp, tester, observed environment, exact save, four logs |
| `cases[]` | Required outcome, linked execution IDs, observation, hash-bound evidence objects |
| top-level status | Derived from every required case |

The six fixed execution IDs are `canonical-clean`,
`canonical-mid-flow-reload`, `canonical-completed-reload`,
`canonical-reinstall`, `canonical-clean-replay`, and
`source-edit-failure`. Do not reuse one timestamp/log bundle for several
executions.

Use ISO 8601 timestamps with a UTC offset. Each completed case needs an
`observed` note and at least one evidence object with `type`, a `reference`
beneath the completed checkpoint's `evidence/` directory, and a SHA-256. Keep
evidence focused and redistributable—sanitized notes, screenshots, log
excerpts, or save metadata—not `sav.dat`, private identifiers, or an
unreviewed large capture. The save itself is represented by its slot label and
hash in the execution record; it is not committed.

Every referenced evidence file is part of the completed checkpoint and its
download ZIP. Packaging admits only safe `evidence/` paths named by the
acceptance record and rejects unreferenced extras, so sanitize and review each
artifact before committing it.

Status rules:

- any required failed case makes top-level status `failed` and evidence class
  `experimental`;
- a mix of pending/passed cases keeps top-level status `pending` and evidence
  class `experimental`;
- only all required cases passed permits top-level status `passed` and evidence
  class `runtime-proven`.

Whenever any case is completed, derive the top-level state and synchronize the
manifest date, practical-guide runtime-test dates, and every reader-facing Lab
2 marker in the same commit. A failed required case uses exactly
`**Lab 2 runtime evidence:** **Experimental** — failed.`; only a complete pass
uses `**Lab 2 runtime evidence:** **Runtime-proven** — passed.`. Repository
validation rejects a status or date split.

## Restore canonical source

After the edited run:

1. close the game and remove the mode-1 installed files;
2. restore node `11` to exact value `2` or discard the edited working copy;
3. compare the canonical completed checkpoint against its recorded artifact
   hashes;
4. restore either no Lab 2 installation or the hash-bound canonical candidate;
5. keep both candidates and all six execution/evidence bundles labelled
   separately.

The downloadable completed checkpoint always remains mode `2`. The mode-1
archive is a test artifact, not a second shipped example.

## Common test failures

| Symptom | Check |
| --- | --- |
| Quest is already active or complete on the first run | Stop and replace the save with a whole slot captured before any `cqa002` candidate was installed; fact resets do not clean journal or active-node state |
| Optional objective changes too early to observe | Confirm the installed candidate hashes and raw node `18 = 30` seconds / node `20 = 120` seconds; remove stale archives before reinstalling |
| Canonical and edited results cannot be attributed | Keep candidate hashes, untouched-save labels, slot-directory identities, executions, and logs separate; identical clean-save bytes are allowed |
| Reload result is ambiguous | Record whether the timer resumed or restarted, but require only eventual single completion without duplicate activation |
| One evidence note is reused for every execution | Retain a fresh four-log set per run and reference focused, hash-bound evidence beneath `completed/evidence/` for each completed case |
| Internal node or socket behavior is claimed from the journal UI | Record only visible states and timing; use the exact graph for structural route mapping and leave winner/cancellation/tie policy **Experimental** |

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Author
Signal Race in WolvenKit](lab-02-authoring.md) · Next lab: [Lab 3: Boundary
Check](../world/lab-03.md).
