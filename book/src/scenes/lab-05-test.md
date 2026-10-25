# Test First Contact

This guide tests the complete **First Contact** checkpoint across ordinary
play, reload, streaming, cleanup, replay, and removal. The eleven cases are
deliberately separate: a scene working once does not show that its actor,
journal state, audio, or cleanup will survive every other lifecycle boundary.

```text
completed checkpoint
  + known starting saves
  + one controlled route per case
  + visible results and fresh logs
  = a result you can diagnose and reproduce
```

| Record | Value |
| --- | --- |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

Use the unmodified completed checkpoint. A project edited while following the
authoring chapter is useful for personal testing, but it is a different build
and may fail for different reasons.

## Required environment

| Component | Exact version |
| --- | --- |
| Cyberpunk 2077 for Windows (GOG) | `2.31a` (public patch `2.31`) |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Record the versions you actually use. The WEM is already built; testing the lab
does not require Wwise Console or audio conversion.

## Freeze a minimal mod loadout

Run Cases 1–10 with the required frameworks and the completed Lab 5 pair.
Disable unrelated quest, world, community, AI, appearance, and framework mods
where practical. In particular, another mod can change the generic Tyger
record's hostility, appearance, workspot behavior, or acquisition without
changing any `cqa005` file.

Keep the loadout unchanged between cases. Case 11 is the exception: close the
game and remove the Lab 5 pair so you can verify that the completed save does
not depend on the mod remaining mounted.

## Establish the site before installation

The shared center is the outdoor recycling-station cabinet row at Allen Street
in Watson/Kabuki:

```text
(-1000.02, 1497.2208, 8.3)
```

Before any Lab 5 candidate is installed, follow Lab 3's [ordinary control-route
procedure](../world/lab-03-test.md#establish-the-site-and-ordinary-control-route).
Confirm the route using the vanilla landmark rather than the Lab 5 pin that is
under test. Do not replace an inaccessible route with a console teleport.

The two boundaries relevant to this campaign are:

| Boundary | Candidate geometry | Test role |
| --- | --- | --- |
| Setup | 25 m circumradius, 16 points, 12 m high | Scene may advance only after spawned readiness and player entry |
| Cleanup | 110 m circumradius, 20 points, 16 m high | Community remains active until V is outside |

The radii describe the supplied polygonal prisms, not universal safe values.
Record the actual route and first/last visible behavior instead of inferring a
crossing from the numbers alone.

## Verify the frozen spoken-line lookup

Before building, inspect the completed checkpoint and verify this exact lookup
chain:

```text
scene locstring RUID 9638591835734011695
  -> registered subtitles\cqa005_subtitles_map.json
       -> indirect subtitles\cqa005_subtitles.json
            femaleVariant = maleVariant = "All clear. Keep moving."
  -> registered vo\cqa005_vo.json
       femaleResPath = maleResPath
         -> vo\contact_i_85c3283507e7ef2f.wem
```

The complete depot paths are:

```text
mod\cqa\cqa005\localization\en-us\onscreens\cqa005_onscreens.json
mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json
mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles.json
mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json
mod\cqa\cqa005\localization\en-us\vo\contact_i_85c3283507e7ef2f.wem
```

The subtitle map and VO map are registration roots. The subtitle entries and
WEM are archived indirect dependencies. Renaming one file or registering the
entries directly changes the candidate.

Use the supplied WEM unchanged for these tests.

## Prepare test saves

Create and preserve two manual-save originals before the first Lab 5
installation. Never use an autosave or checkpoint save, and keep both source
slots outside the game's rotating autosave set.

1. Make `CQA005 ORIGINAL OUTSIDE SETUP` outside the setup volume on the
   verified ordinary approach.
2. Make the separate `CQA005 ORIGINAL NEAR SETUP` near but still outside setup
   for the immediate-arrival race. Reach it through ordinary game travel,
   including the verified vanilla fast-travel approach if used; do not
   teleport.
3. Record each complete slot-directory name in your
   test notes.
4. Confirm neither save has ever loaded any CQA tutorial candidate: no Lab 1–4
   start/completed project and no Lab 5 start, completed, or older `cqa005` candidate. Labs 3
   and 4 share this site, and removing their archives does not erase saved
   quest, journal, trigger, or world state. If you already followed those labs,
   restore a separately preserved pre-tutorial save or create a genuinely new
   clean lineage; a disclosed prior-lab history is not sufficient.
5. Exit the game completely before cloning either complete source slot into a
   run-specific directory. Never execute a case from the immutable source
   directory itself.
6. Case 1 must continue one unbroken ordinary route through completion and
   create exactly three additional manual-save captures at the frozen moments
   below. A checkpoint or autosave does not satisfy a capture row.
7. After Case 1, exit the game completely before cloning any complete seed
   slot for Cases 3–9 or 11. Never edit a clone, reset a fact, or copy only
   `sav.dat` without the rest of its slot directory.

The test uses five named save captures:

| Capture ID | Exact label | Source / parent | Frozen observable state | Execution cases |
| --- | --- | --- | --- | --- |
| `original-outside-setup` | `CQA005 ORIGINAL OUTSIDE SETUP` | External original / none | Outside setup on the ordinary route; never loaded any CQA Lab 1–5 candidate | 1, 10 |
| `original-near-setup` | `CQA005 ORIGINAL NEAR SETUP` | Separate external original / none | Near but outside setup; never loaded any CQA Lab 1–5 candidate | 2 |
| `seed-pre-scene-outside-setup` | `CQA005 SEED PRE SCENE OUTSIDE SETUP` | Case 1 / `original-outside-setup` | Meet Active; pin Active; child active; contact spawned and passive; V outside setup; checkpoint `cqa005_first_contact` not executed; scene not started; fact `0` | 3, 4, 7 |
| `seed-post-contact-inside-cleanup` | `CQA005 SEED POST CONTACT INSIDE CLEANUP` | Case 1 / pre-scene seed | `contact_done` returned; Meet Succeeded; pin Inactive; Leave Active; child and contact active; V inside cleanup; fact `0` | 5, 6, 8 |
| `seed-completed` | `CQA005 SEED COMPLETED` | Case 1 / post-contact seed | Leave and quest Succeeded; pin Inactive; contact deactivated; child and root returned; fact `1` | 9, 11 |

Keep all five source slots unchanged. With the game closed, copy the entire
appropriate slot into a separate working directory for each case, including its
metadata files. Check that its `sav.dat` matches the source copy. Never run a
case directly from the preserved source slot.

Cases 3, 4, and 7 use copies of the same pre-scene capture outside setup.
There is no save window between child checkpoint node `15` and scene node
`16`: they are connected directly. Cases 5, 6, and 8 share the post-contact
capture; Cases 9 and 11 share the completed capture; Cases 1 and 10 share the
outside original. Case 2 alone uses the separate near-site original.

Do not reset `cqa005_completed` to prepare a case. Journal, scene, community,
actor, phase, and streamed-world state can outlive that fact.

## Build, install, and bind the canonical candidate

Use the unmodified [completed checkpoint](../downloads/cqa-lab-05-completed.zip):

```text
project: CQA_Lab05_FirstContact.cpmodproj
```

Open all eleven CR2W resources in WolvenKit before testing. Resolve missing
files or conversion errors before installing the project.

1. Close the game.
2. Open the completed project in WolvenKit and use its normal build/package
   and install workflow.
3. Confirm the start checkpoint, every older `cqa005` archive, and every Lab
   1–4 tutorial candidate are absent. Labs 3 and 4 deliberately reuse this
   Allen Street test area; leaving them installed can add overlapping markers,
   triggers, objectives, and log traffic even though their depot namespaces
   differ.
4. From the game directory, run:

   ```powershell
   Get-ChildItem .\archive\pc\mod\CQA_Lab0*.archive* |
     Select-Object -ExpandProperty Name
   ```

   The complete output must be exactly these two names, with no Start variant
   and no `CQA_Lab01_*` through `CQA_Lab04_*` pair:

   ```text
   CQA_Lab05_FirstContact.archive
   CQA_Lab05_FirstContact.archive.xl
   ```

5. Confirm the candidate contains the twelve depot paths listed in [the
   resource inventory](lab-05.md#twelve-runtime-artifacts), including the
   indirectly reached child, scene, subtitle entries, WEM, and both sectors.
6. Preserve byte-identical copies of both installed files until the complete
   campaign and log audit finish.

Keep the installed pair unchanged between cases. If you rebuild it, repeat
the affected tests from their starting saves.

## Capture every execution consistently

For each run, keep a dated note containing your game/framework versions,
installed filenames, starting save label and slot directory, the source save
it was copied from, and what you observed. Mark cases you did not run as
pending. Keep a fresh copy of all four logs listed below before the next launch
can overwrite them.

Use a separate working slot and log folder for every case. Reusing one run's
logs or observations cannot establish the result of another run.

Capture a short continuous video with game audio for timing, replay, visible
spawn, scene, and cleanup claims. Add focused screenshots or notes for journal
and pin states. Record the first and last visible contact behavior, the route,
any combat stimulus, and whether a loading screen occurred. Do not use the
video alone for log or save history.

Keep saves, logs, and captures in your own test folder. If you contribute a
result to the book, follow the repository contribution guide for sanitizing and
submitting evidence. Do not publish private saves or extracted vanilla resources.

## Case 1: `clean-ordinary-passive-spawn`

**Acceptance precondition:** Install the canonical candidate, load a
closed-game full-slot clone of the untouched outside-setup original, approach
by ordinary movement, and continue the same unbroken route through ordinary
completion while making the three named manual seed saves.

**Required result:** The root and child activate once, the passive community
contact appears through the community/AI-spot mapping, and the meet objective
and pin appear once without a spawn or NodeRef error. The ordinary route
completes once, and exactly the pre-scene, post-contact, and completed seed
captures are made at their frozen observable states.

Walk the verified route without fast travel, teleporting, combat, or waiting at
the boundary to manipulate streaming. Begin capture before the first Lab 5
objective. Record the meet objective and pin appearing once, the contact at the
authored spot, and the absence of hostile/combat behavior when unprovoked.

Continue this same run and make exactly these three manual saves, never a
checkpoint or autosave:

1. `CQA005 SEED PRE SCENE OUTSIDE SETUP`, after the contact is spawned and
   passive but while V remains outside setup. Meet and pin are Active, the
   child is active, checkpoint `cqa005_first_contact` has not executed, the
   scene has not started, and `cqa005_completed` is `0`.
2. `CQA005 SEED POST CONTACT INSIDE CLEANUP`, after `contact_done` returns but
   before leaving cleanup. Meet is Succeeded, pin Inactive, Leave Active,
   child/contact active, and the fact remains `0`.
3. `CQA005 SEED COMPLETED`, after cleanup and root return. Leave and quest are
   Succeeded, pin Inactive, contact deactivated, child/root returned, and the
   fact is `1`.

Keep the route capture, state screenshots, and fresh logs. Exit the game
before copying the three complete seed directories. There is no save window
between checkpoint node `15` and scene node `16`.

## Case 2: `fast-arrival-race`

**Acceptance precondition:** Load a closed-game full-slot clone of the separate
untouched near-setup original and enter immediately before waiting for
streaming or spawn.

**Required result:** The spawned-character wait resolves before the setup wait
advances; the scene begins once only after the contact exists, with no missed
trigger or deadlock.

This is the fast-travel/immediate-sprint setup-race case. Use the independently
preserved near-site save, load it, and sprint into the 25 m setup volume as soon
as player control returns. Do not pause nearby to let the actor appear first.
If fast travel was used to prepare the pre-install route, record that fact and
the vanilla destination; never replace it with a console teleport.

Capture from the loading screen through contact appearance and scene start.
The decisive ordering is actor visible/available before the scene performs,
one scene start, and eventual forward progress. A scene that never starts, a
scene that starts without its contact, or a missed already-true setup condition
fails the case even if a slower retry works.

## Case 3: `slow-contact-av-once`

**Acceptance precondition:** Load a byte-identical full-slot clone of the named
pre-scene outside-setup seed, approach slowly, remain in range for the full
scene, and do not skip or interrupt it.

**Required result:** The exact subtitle `All clear. Keep moving.` and the
supplied WEM play once; the contact is acquired, the line does not duplicate,
and lipsync/audio errors are absent from retained logs.

Start from `clean-derived-before-setup`, a distinct execution-slot clone of
`seed-pre-scene-outside-setup`. Keep the
contact in view, enter at a walking pace, and remain until the scene completes.
Capture the exact subtitle, audible line, contact performer, and mouth/facial
response in one continuous recording. Count subtitle display and audible
playback separately; each must be exactly one.

Check the line with RUID `9638591835734011695`. A subtitle without sound,
sound without the exact subtitle, or duplicate playback fails this test.

## Case 4: `named-exit-only`

**Acceptance precondition:** Load a byte-identical full-slot clone of the same
named pre-scene outside-setup seed used by Cases 3 and 7, then observe ordinary
completion. This is not a save between checkpoint node `15` and scene node
`16`.

**Required result:** Only named exit `contact_done` advances the child to meet
Succeeded; Default INT/RET remain unwired and no fallback continuation is
observed.

Start from `clean-derived-before-scene`, another distinct execution-slot clone
of `seed-pre-scene-outside-setup`, not a new capture. Record the meet objective
before crossing setup, the scene's ordinary terminating end, and the
transition to meet Succeeded/leave Active. Do not invoke an interrupt or cut
path in this case.

Pair the runtime capture with the canonical scene/questphase structural record
showing `contact_done` wired to child node `17.Succeeded` and `Default INT` /
`Default RET` unwired. Runtime evidence must show no fallback or double
continuation; graph inspection alone cannot pass the case.

## Case 5: `no-replay-inside-lifetime`

**Acceptance precondition:** Load a byte-identical full-slot clone of the named
post-contact inside-cleanup seed, then cross the setup boundary or revisit the
contact point before leaving cleanup.

**Required result:** The scene, subtitle, and WEM do not replay during the same
child lifetime; the leave objective remains the only active progression state.

Use `clean-derived-after-contact-inside-cleanup`, a distinct execution-slot
clone of `seed-post-contact-inside-cleanup`. Stay inside the
110 m cleanup volume, and walk out of and back into the 25 m setup area or
revisit the contact point without crossing cleanup. Remain long enough that a
duplicate line would be obvious.

Capture the complete revisit and the journal state. The contact may remain as
part of delayed cleanup, but the scene, subtitle, and WEM must not restart and
the meet objective/pin must not reactivate.

## Case 6: `post-scene-reload`

**Acceptance precondition:** Without changing the installation, load a
byte-identical full-slot clone of the named post-contact inside-cleanup seed.

**Required result:** Meet stays succeeded, the pin stays inactive, leave stays
active, the contact line does not replay, and crossing cleanup continues once.

Hash and load the `contact-done-inside-cleanup` execution clone, verifying it
matches `seed-post-contact-inside-cleanup`, with the exact installed pair
unchanged. Capture journal and pin state immediately after load and after
walking continuously outside cleanup. Record that the line does not replay
and that leave/child progression occurs once.

A run that repairs itself only after re-entering setup is a failure: the saved
post-scene owner state must resume directly.

## Case 7: `stream-away-return`

**Acceptance precondition:** Load a byte-identical full-slot clone of the named
pre-scene outside-setup seed, travel by ordinary movement beyond the finite
Quest descriptor box before entering setup, return, and finish.

**Required result:** The community and child remain coherent across streaming;
returning resolves the same NodeRefs and advances the scene exactly once
without duplicate contact entries.

Start from `child-active-before-setup`, a third distinct execution-slot clone
of `seed-pre-scene-outside-setup`. Do not enter
the setup volume. Travel by ordinary movement beyond the Quest descriptor's
finite box, whose supplied X/Y range is `-1300.02..-700.02` by
`1197.2208..1797.2208`, then return by the same recorded route. Do not use fast
travel for this case.

Capture departure, return, contact materialization, scene, and objective
progression. Retain logs from both streaming transitions. Two contacts, a
stale spot, unresolved NodeRefs, lost child state, or a second scene execution
fails the case.

## Case 8: `cleanup-boundary-no-pop`

**Acceptance precondition:** Load a byte-identical full-slot clone of the named
post-contact inside-cleanup seed, then walk outward continuously through the
cleanup boundary more than 110 metres from the shared center.

**Required result:** IsOutside resolves once, whole-community deactivation
occurs only at cleanup, no visible contact pop occurs inside the cleanup
volume, leave succeeds, and child Out1 returns once.

Load a third distinct `contact-done-inside-cleanup` execution clone and confirm
it matches `seed-post-contact-inside-cleanup`. Walk outward continuously; do
not fast travel, teleport, reload again, or double back. Keep the meeting point
in view when the route permits and record distance/route landmarks, the last
visible contact state, the leave-objective transition, and quest completion.

The actor must not visibly disappear while V is still inside the authored
cleanup prism. The expected deactivation command and return are proved by the
ordered progression and absence of errors, not by claiming that Spawn Manager
guarantees same-frame visual removal.

## Case 9: `completed-reload`

**Acceptance precondition:** With the same exact candidate installed, load a
byte-identical full-slot clone of the named completed seed.

**Required result:** cqa005_completed bypasses the child; objectives, pin,
community, scene, subtitle, and WEM do not reactivate or replay.

Load the `completed` execution clone, confirm it matches `seed-completed`, and
remain near or revisit the site long enough to observe the one-shot guard.
Record the absence of all six reactivation surfaces named in the required
result. A silent scene with a reactivated objective or actor still fails the
case.

## Case 10: `untouched-replay`

**Acceptance precondition:** With the canonical candidate still installed,
load a byte-identical full-slot clone of the same untouched outside-setup
original used by Case 1 and repeat the ordinary route.

**Required result:** Spawn, acquisition, line, named exit, cleanup, child
return, and root completion reproduce once with the same visible and logged
behavior.

Load a working copy of the original `untouched-preinstall-outside-setup` slot
and repeat the complete route with the same build. Compare spawning, dialogue,
cleanup, and completion with Case 1.

This is clean reproducibility. Resetting `cqa005_completed` on the completed
save would test a different, dirty state and cannot pass this case.

## Case 11: `removal-isolation-diagnostic`

**Acceptance precondition:** With the game closed, clone the named completed
seed into the disposable execution slot, remove both exact candidate files
before launching and loading that clone, and revisit the site without resetting
any fact.

**Required result:** No mod-owned resource remains mounted, no Lab 5 objective
or pin reactivates, no `cqa005` contact appears, fresh logs show no `cqa005`
registration, and the packaged fixture contains no TweakDB mutation or
override.

With the game closed, copy the complete `seed-completed` source slot to a
separate disposable slot. Preserve the installed pair, then move these two
files out of the game directory:

```text
archive\pc\mod\CQA_Lab05_FirstContact.archive
archive\pc\mod\CQA_Lab05_FirstContact.archive.xl
```

Confirm there is no second Lab 5 archive or ArchiveXL file under another name.
Do not edit the clone, reset `cqa005_completed`, or use a save editor or console.
Archive the prior four logs, launch the disposable clone, revisit the site, and
then retain the fresh four-log bundle.

Confirm that the fresh ArchiveXL log contains no registration for
`mod\cqa\cqa005`, no Lab 5 objective or pin reactivates, and no mod-owned
contact appears. Completed journal history already stored in the save is not a
mount or reactivation and is not grounds for failure by itself.

The exact packaged inventory contains no `r6\tweaks`, YAML tweak, script, or
other TweakDB mutation source. Its
`Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa` value is a read-only
`characterRecordId` reference. That source-level absence is structurally
validated; this diagnostic deliberately does not claim to prove every vanilla
field or exclude unrelated installed mods. Disable unrelated mods rather than
trying to edit or compare the generic record.

Label every artifact `removal-isolation-diagnostic`. Restore the unchanged
candidate pair only after the game and framework processes have fully exited.

## Retain and audit four logs per execution

Before starting another run, copy these logs into that run's test folder:

```text
red4ext\plugins\ArchiveXL\ArchiveXL.log
red4ext\logs\red4ext.log
red4ext\logs\game.log
r6\logs\redscript_rCURRENT.log
```

Copy the logs before the next launch overwrites them. Keep them in a separate
folder for each run.

Search all four logs for:

- `cqa005`, all twelve depot paths, and the installed project name;
- `#cqa005_pr_first_contact`, the community, spot, scene marker, and trigger
  NodeRefs;
- RUID `9638591835734011695` and
  `contact_i_85c3283507e7ef2f.wem` where the subsystem logs expose them;
- ArchiveXL registration, missing resource, NodeRef, streaming, scene,
  community, localization, audio, RED4ext, and redscript errors.

Record both relevant matches and the absence of expected failures. Do not
claim that silence proves A/V playback: Case 3 still requires direct subtitle
and audio observation.

## Failure triage

Preserve the failed run, save name, candidate pair, video, and all four logs
before editing anything.

| Observation | Classification and first checks |
| --- | --- |
| Quest never appears | Failed registration/root activation; inspect exact pair, ArchiveXL log, root depot path, and untouched-save history |
| Meet/pin appears but no contact | Failed streaming/community join; inspect finite sector, source/registry/spot IDs, entry/phase, workspot, and NodeRef logs |
| Contact is hostile without provocation | Failed passive-contact case; retain surrounding stimuli and inspect the generic record/AI policy before changing the matrix |
| Immediate sprint deadlocks or scene starts without contact | Failed readiness/setup ordering; inspect child nodes `13 -> 14 -> 15 -> 16` and the fast run's streaming logs |
| Exact subtitle appears without sound | Failed VO path/WEM lookup; inspect RUID, `cqa005_vo.json`, WEM depot path/hash, archive inventory, and audio logs |
| Sound plays without the exact subtitle | Failed subtitle-map chain; inspect registered map, indirect entries path, both variants, RUID, and localization logs |
| Line/subtitle plays twice | Failed exactly-once scene lifecycle; inspect duplicate registration, scene start, saved state, and setup replay |
| Scene ends but meet does not succeed | Failed named handoff; inspect `contact_done`, End `3`, child output socket, and inert defaults |
| Reload replays the scene or pin | Failed save-backed owner transition; retain the derived save before inspecting scene/journal state |
| Return after streaming creates a second contact | Failed registry/area lifecycle or duplicate mount; inspect identities, descriptor ownership, and installed candidates |
| Contact disappears while V is inside cleanup | Failed cleanup timing/geometry; inspect trigger polarity, route, node `20`, and deactivation order |
| Completed reload starts the child | Failed completion guard/write order or dirty candidate/save history |
| Removal run still mounts Lab 5 | Failed removal isolation; search for duplicate archive pairs and preserve fresh framework logs |
| Packaged project contains a tweak or script mutation | Reject the candidate; Lab 5 may reference the generic record but must not override or mutate it |
| A useful log was overwritten | Repeat the case from the same starting save and copy the fresh logs before another launch |

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Author
First Contact in WolvenKit](lab-05-authoring.md) · Next: [Troubleshooting](../troubleshooting/index.md).
