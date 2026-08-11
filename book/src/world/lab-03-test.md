# Test Boundary Check

Lab 3 crosses quest, journal, localization, streaming, marker, trigger, and
save systems. A screenshot of the final journal state cannot isolate those
owners. This protocol binds the exact installed candidate, save provenance,
visible transitions, and fresh logs across eight executions.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

Use the unmodified completed checkpoint for these tests. Record what you
observe for every run; a successful ordinary walk does not establish reload,
stream-return, reinstall, or clean-replay behavior.

## Required environment

| Component | Exact version |
| --- | --- |
| Cyberpunk 2077 for Windows (GOG) | `2.31a` |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Record observed versions on every run. Values printed in the template are
requirements, not proof of the machine that executed it.

## Establish the site and ordinary control route

Do this before installing any Lab 3 candidate. The quest pin and GPS route are
under test, so they cannot be the only way you know how to reach the site.

**Observed in vanilla:** a focused extract from
`base\worlds\03_night_city\_compiled\default\exterior_-17_22_0_0.streamingsector`
places a fast-travel terminal entity at
`(-1064.30457, 1436.18298, 4.95000076)`. Node index `1766` uses record
`FastTravelPoints.wat_kab_dataterm_12`, entity template
`base\gameplay\devices\fast_travel\data_term_1.ent`, and this full NodeRef:

```text
$/03_night_city/c_watson/kabuki/kabuki_data_terminals_prefabW7DFTCQ/#wat_kab_dataterm_12/{kab_data_term_}12_prefabBARKVWA
```

The installed TweakDB maps that record to `LocKey#79217`; English
`base\localization\en-us\onscreens\onscreens.json` maps key `79217` to
`Allen Street`. Its linked destination marker is node `5757` in
`base\worlds\03_night_city\_compiled\default\always_loaded_1.streamingsector`:

```text
$/03_night_city/c_watson/kabuki/kabuki_data_terminals_prefabW7DFTCQ/#wat_kab_dataterm_12/#wat_kab_dataterm_12_tp
(-1065.76489, 1435.83472, 4.94000006)
```

Extract those resources from your own game if you need to reproduce the
lookup; do not redistribute them. The Lab 3 center is the outdoor
recycling-station cabinet row in Watson/Kabuki at
`(-1000.02, 1497.2208, 8.3)`, about 90 m northeast of the linked marker. The
20-sided 110 m outline calculation leaves about 18.8 m of directional margin
at that marker; the terminal and marker Z values lie within the outline's base
`0.3` and height `16`. The next cataloged terminal is about 131 m away and
outside the outline.

Those coordinates and calculations do not prove player access. Treat the
following as **Experimental** until performed on the pinned game build:

1. with no Lab 3 candidate installed, visit and unlock Allen Street;
2. confirm the terminal opens normally and that at least one distant
   destination is already unlocked;
3. from the terminal, walk roughly northeast for about 89 m to the outdoor
   recycling-station cabinet row;
4. recognize the cabinet row independently of any quest marker and confirm an
   ordinary public approach, collision, and practical elevation;
5. walk back to Allen Street and make the untouched outside save there.

If the terminal or cabinet route is inaccessible, record that result and do
not silently replace the route with a console teleport. Revise and hash a new
test candidate or route before continuing.

## Prepare save provenance

Before installing any Lab 3 checkpoint:

1. choose the Allen Street manual save made above, which has never loaded a
   build registering `cqa003`;
2. confirm the player is outside the 25-metre reach volume and can reach the
   cabinet row by the verified ordinary route;
3. copy the entire save-slot directory into private evidence storage;
4. record its label and slot-directory name;
5. hash `sav.dat` and set `created_before_first_install: true` only after
   confirming that history;
6. retain one hash-bound active-before-reach derivation for both Run 2 and Run
   4; restore byte-for-byte working copies from it rather than making a second
   pre-reach state;
7. reserve separate derived copies for between-boundaries and completed
   reloads;
8. reserve a separate between-boundaries derivation for fast travel.

A console reset of `cqa003_completed` does not create a clean save. Removing
the mod after a prior load does not remove serialized journal, graph, marker,
or world state.

## Build and bind the canonical candidate

Use the unmodified completed checkpoint:

```text
candidate id: canonical
project:      CQA_Lab03_BoundaryCheck.cpmodproj
```

1. Close the game.
2. Build and install through WolvenKit.
3. Confirm only this candidate's pair is installed:

   ```text
   archive\pc\mod\CQA_Lab03_BoundaryCheck.archive
   archive\pc\mod\CQA_Lab03_BoundaryCheck.archive.xl
   ```

4. Hash both installed files in `candidates[0].installed_files`.
5. Confirm the record names all six depot resources, including the two
   sectors reached through the registered block.
6. Preserve the installed files until every run needing this candidate is
   complete.

Hash the installed payloads, not the ZIP. Packing and the loose registration
file are part of the runtime candidate.

## Run 1: outside negative control and ordinary walk

Restore the untouched Allen Street save and record the execution as
`clean-walk`. Follow the independently learned route roughly 89 m northeast
from the terminal to the outdoor cabinet row. Do not count the quest GPS route
as proof that the ordinary route is usable.

### Before entering

Observe and retain:

1. Boundary Check, its phase, and the reach objective activate once;
2. the checkpoint pin appears at the intended location;
3. the minimap/world-map presentation and any GPS route are usable;
4. waiting outside the reach boundary does not advance the objective;
5. approaching at different elevations does not trip the volume unexpectedly.

Visible pin placement is evidence about presentation. It does not identify
which sector loaded. Record displaced, inaccessible, missing, flickering, or
route-less behavior exactly rather than smoothing it into a pass.

### Cross the reach boundary

Walk into the inner volume. Confirm the pin retires, the reach objective
succeeds once, and the leave objective activates once. Stay inside the outer
volume long enough to show that leave does not complete merely because the
new objective became active.

### Cross the leave boundary on foot

Walk southwest along the learned route, pass the Allen Street terminal, and
continue at least another 40 m in the same general direction. The structural
calculation puts the linked marker about 18.8 m inside the outline along that
ray, so the terminal
itself is not the expected foot crossing. Record the crossing position/Z,
confirm the leave objective, phase, and quest succeed once, and wait long
enough to detect a delayed duplicate pin or journal notification.

This run supplies `outside-negative-control-and-foot-route` and
`marker-and-navigation`. The exact graph and resources map those visible
events to authored nodes; UI alone does not expose a trigger buffer or sector.

## Run 2: reload before reach

Restore the original untouched save, activate the quest while remaining
outside the reach volume, and make a derived save. Hash it and execute
`pre-reach-reload`:

1. reload without changing the installation;
2. confirm the reach objective and pin return once;
3. enter the reach volume;
4. confirm one pin retirement and one reach success;
5. finish on foot and retain the result.

Keep this exact derived slot immutable after hashing it. Run 4 must restore the
same `sav.dat`, and the two run records must carry the same SHA-256 rather than
two independently recreated active-before-reach saves.

The required result is coherent single progression. Do not infer how the
engine rearmed the state predicate solely from the journal UI.

## Run 3: reload between boundaries

Restore the clean source, reach the checkpoint, and save after the reach
objective succeeds while still inside the 110-metre leave volume. Hash that
save and execute `between-boundaries-reload`:

1. reload in place;
2. confirm leave stays active instead of completing on load;
3. remain inside briefly as a negative control;
4. follow the Allen Street route past the terminal and cross the outer
   boundary on foot;
5. confirm single completion.

If the volume releases immediately, record the player's exact position/Z,
save state, and logs. Do not silently move the boundary or change predicate
mid-candidate.

## Run 4: stream away and return

Restore a byte-for-byte working copy of Run 2's hash-bound
active-before-reach save and execute `stream-away-return`. Confirm its
`sav.dat` SHA-256 matches Run 2 before loading it.

1. remain outside the reach volume and go to the recognizable Allen Street
   terminal by ordinary movement; do not open or use it;
2. follow connected public streets southwest from Allen Street by ordinary
   walking or driving until the map shows at least 500 m of displacement from
   the terminal, then continue another two blocks so the route is well beyond
   the site-centered finite box `(-1300.02..-700.02,
   1197.2208..1797.2208)`;
3. record the farthest map location or player position and whether the active
   objective and pin remain coherent;
4. reverse the same street route, pass the Allen Street terminal again, then
   follow the learned roughly 89 m northeast route to the cabinet row;
5. walk the reach and leave sequence and retain any streaming or NodeRef log
   lines.

Do not use fast travel in this run. If road geometry prevents the stated
route, record the deviation and the farthest position rather than assuming the
test box was left.

This case probes the finite Quest descriptor bounds and return path. It does
not prove a precise unload moment unless independent instrumentation records
one. Describe player-visible continuity and log results without inventing an
invisible streaming event.

## Run 5: characterize fast travel separately

Use the separately retained between-boundaries save for `fast-travel-exit`.

1. after loading, confirm the leave objective is active at the cabinet row;
2. walk the learned ordinary route southwest to the Allen Street terminal;
3. before opening it, record the player position and Z and confirm the leave
   objective has not completed; the structural calculation predicts about
   18.8 m of marker margin, but this observation is the runtime check;
4. open Allen Street and choose any already-unlocked destination that you
   independently confirmed is outside the 110 m leave outline;
5. after arrival, record whether `IsOutside` completes, remains waiting, or
   behaves another way, together with the arrival position/Z and logs.

If leave completes before the terminal opens, mark the required
`fast-travel-characterization` case failed and retain the position evidence;
do not continue that execution as though fast travel caused the exit.

This is a required characterization, not a predetermined claim that fast
travel must simulate `Exited`. Keep it separate from Run 1's ordinary foot
crossing. Allen Street accessibility and the new 110 m behavior remain
**Experimental** until this run is retained.

## Run 6: completed-save reload

From an ordinary clean-walk completion:

1. retain and hash the completed save;
2. reload it without changing installed files as `completed-reload`;
3. confirm no quest/objective reactivation and no checkpoint pin;
4. wait for delayed visible updates;
5. retain fresh logs.

Exact graph evidence maps this bypass to node `10.False`; runtime evidence
records that the completed candidate and save display the expected one-shot
result.

## Run 7: identical reinstall

Close the game, remove the installed candidate pair, and reinstall the
identical hash-bound files. Do not rebuild from merely unchanged-looking
source unless the new installed hashes match exactly.

Load the same completed save as `completed-reinstall`. Confirm the quest stays
complete, the pin stays inactive, and no duplicate activation occurs. The
save SHA-256 must match Run 6.

## Run 8: clean replay

Restore the entire original untouched save-slot directory and leave the
identical canonical candidate installed. Its original `sav.dat` hash must
match the pre-install record.

Execute `clean-replay`, walking the ordinary route again. The same visible
activation, reach, leave, and completion sequence must occur once. Retain a
new log set rather than reusing Run 1's files.

## Retain four logs per execution

After each of the eight executions, close the game and retain fresh copies of:

```text
red4ext\plugins\ArchiveXL\ArchiveXL.log
red4ext\logs\red4ext.log
red4ext\logs\game.log
r6\logs\redscript_rCURRENT.log
```

Hash every file under its run. Search for the registration filename, `cqa003`,
all registered depot paths, the streaming block and sectors, NodeRefs,
journal/localization lookups, and condition errors. Clean logs mean those
systems did not report an error; they do not replace in-game observations.

## Common test failures

| Symptom | Check |
| --- | --- |
| Quest is already active on the first run | Replace the whole slot with one captured before any `cqa003` install; fact resets do not clean journal/world state |
| Pin appears but route cannot reach it | Record the map/minimap/GPS result, site accessibility, marker Z, and exact game build; do not count visible pin alone as navigation success |
| Allen Street is locked or the cabinet row cannot be reached ordinarily | Stop before acceptance, retain the observed route/access result, and establish a separately reviewed route; do not substitute a diagnostic teleport |
| Trigger result is ambiguous | Record position, Z, ordinary movement versus fast travel, visible journal state, candidate hash, and logs; keep state and transition claims distinct |
| Leave completes while walking back to Allen Street | Retain the exact player position/Z and candidate hash as a failed geometry result; do not continue as though the terminal were inside the outline |
| Leave completes on reload | Verify the derived save is actually inside the outer volume and retain its position evidence; do not move geometry inside the canonical candidate |
| Stream-away result is inferred | Report only visible continuity and logs unless instrumentation independently establishes unload/reload |
| Reinstall is not identical | Compare both installed hashes; a new build is a new candidate even when source looks unchanged |
| One screenshot is used for every case | Retain separate run identity, saves, timestamps, observations, and four-log bundles |
| UI is treated as proof of sector ownership | Use exact structural evidence for ownership and runtime evidence only for what the player/logs expose |

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Author
Boundary Check in WolvenKit](lab-03-authoring.md) · Next lab: [Lab 4: Handoff
Point](../questphases/lab-04.md).
