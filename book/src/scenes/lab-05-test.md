# Test First Contact

Lab 5 is promoted only when the unmodified completed checkpoint passes all
eleven required cases in its schema-version-4 acceptance record. The campaign
binds one installed candidate to exact saves, versions, logs, visible behavior,
and the supplied WEM:

```text
canonical completed checkpoint
  + installed archive and ArchiveXL SHA-256
  + canonical WEM SHA-256
  + untouched and clean-derived save provenance
  + eleven required case results
  + four retained logs for every execution
  = eligible for Runtime-proven promotion
```

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

Use only the canonical completed checkpoint and its packaged
`runtime-acceptance.json` schema version `4`. Do not substitute the start
checkpoint, a project you edited while following the authoring chapter, or
either retained historical archive. Earlier runtime evidence does not prove
the combined `cqa005` mount, world, community, scene, localization, audio,
handoff, reload, and cleanup contract.

## Required environment

| Component | Exact version |
| --- | --- |
| Cyberpunk 2077 for Windows (GOG) | `2.31a` (public patch `2.31`) |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Record those five components as observed on every execution. Wwise Console
`2025.1.7.9143` is production provenance for the already-built WEM, not a
reader runtime requirement; the tester does not need to reconvert it. Preserve
that provenance without claiming Wwise Console ran during gameplay.

Other versions may mount, serialize, stream, acquire, or play the resources
differently and do not satisfy this candidate's promotion contract.

## Freeze a minimal mod loadout

Run Cases 1--10 with only the pinned RED4ext, ArchiveXL, and redscript
frameworks plus the exact canonical Lab 5 pair. Case 11 is the sole candidate
exception: keep the framework and unrelated-mod inventory frozen, but remove
that pair with the game closed exactly as its procedure requires. With the game
and every framework process closed, remove or disable unrelated archives,
ArchiveXL or TweakXL files, RED4ext plug-ins, `.reds` scripts, CET mods,
AI/faction changes, appearance changes, and community/world edits. In
particular, another mod can change the generic Tyger record's hostility,
appearance, workspot behavior, or acquisition without changing any `cqa005`
byte.

Before the first run, retain a sanitized, sorted file-and-SHA-256 inventory of
the load-bearing code and configuration assets in the active mod locations.
Cover at least archives and ArchiveXL/TweakXL configuration under
`archive\pc\mod`; plug-in binaries and static configuration under
`red4ext\plugins` and `bin\x64\plugins`; and source/configuration under
`r6\scripts` and `r6\tweaks`. Exclude logs, caches, crash reports, and other
generated runtime state from this frozen inventory. In particular,
`red4ext\plugins\ArchiveXL\ArchiveXL.log` is a per-run evidence artifact, not a
frozen framework asset.

Keep that framework and unrelated-mod asset inventory unchanged through all
eleven executions, and keep the canonical pair byte-identical and installed for
Cases 1--10. Only Case 11 deliberately omits the pair. Record the frozen asset
inventory as focused `notes` evidence, while retaining the four mutable logs
separately for every run. If an unrelated mod must remain installed, this
campaign is not eligible for promotion; isolate it and begin again instead of
trying to explain away a changed actor or log afterward.

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

Hash the supplied WEM before testing:

```powershell
(Get-FileHash -Algorithm SHA256 `
  .\examples\lab-05-first-contact\completed\source\archive\mod\cqa\cqa005\localization\en-us\vo\contact_i_85c3283507e7ef2f.wem).Hash.ToLowerInvariant()
```

It must equal:

```text
0487ba1116d9c4fa9cfb25e825ad4ec35110195cf3953cb8bc67a16f5cbc657f
```

Preserve that result with the candidate evidence. Wwise conversion is not
claimed to be byte-reproducible, so a newly converted WEM is a different
candidate even when it plays the same source line.

## Prepare save provenance

Create and preserve two manual-save originals before the first Lab 5
installation. Never use an autosave or checkpoint save, and keep both source
slots outside the game's rotating autosave set.

1. Make `CQA005 ORIGINAL OUTSIDE SETUP` outside the setup volume on the
   verified ordinary approach.
2. Make the separate `CQA005 ORIGINAL NEAR SETUP` near but still outside setup
   for the immediate-arrival race. Reach it through ordinary game travel,
   including the verified vanilla fast-travel approach if used; do not
   teleport.
3. Record each complete slot-directory name and `sav.dat` SHA-256 in the
   matching `save_captures` row.
4. Keep `created_before_first_install: true` only after confirming neither save
   has ever loaded any CQA tutorial candidate: no Lab 1–4 start/completed
   project and no Lab 5 start, completed, or older `cqa005` candidate. Labs 3
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

The schema-version-4 `save_captures` inventory is exact:

| Capture ID | Exact label | Source / parent | Frozen observable state | Execution cases |
| --- | --- | --- | --- | --- |
| `original-outside-setup` | `CQA005 ORIGINAL OUTSIDE SETUP` | External original / none | Outside setup on the ordinary route; never loaded any CQA Lab 1–5 candidate | 1, 10 |
| `original-near-setup` | `CQA005 ORIGINAL NEAR SETUP` | Separate external original / none | Near but outside setup; never loaded any CQA Lab 1–5 candidate | 2 |
| `seed-pre-scene-outside-setup` | `CQA005 SEED PRE SCENE OUTSIDE SETUP` | Case 1 / `original-outside-setup` | Meet Active; pin Active; child active; contact spawned and passive; V outside setup; checkpoint `cqa005_first_contact` not executed; scene not started; fact `0` | 3, 4, 7 |
| `seed-post-contact-inside-cleanup` | `CQA005 SEED POST CONTACT INSIDE CLEANUP` | Case 1 / pre-scene seed | `contact_done` returned; Meet Succeeded; pin Inactive; Leave Active; child and contact active; V inside cleanup; fact `0` | 5, 6, 8 |
| `seed-completed` | `CQA005 SEED COMPLETED` | Case 1 / post-contact seed | Leave and quest Succeeded; pin Inactive; contact deactivated; child and root returned; fact `1` | 9, 11 |

Fill each capture's `slot_directory` and `sha256` after making it. The validator
requires five distinct source directories and five distinct source hashes.
Each run uses a byte-identical full-slot clone, records `copy_scope` as
`complete-slot-directory`, and sets `game_closed_before_clone: true` only
after that condition was observed. All eleven execution slot directories must
also be distinct from each other and from every source capture directory.

The packaged run records use these exact states:

| Run ID | `save_state` | `save_provenance` | `capture_id` | `source_run_id` |
| --- | --- | --- | --- | --- |
| `clean-ordinary-passive-spawn` | `untouched-preinstall-outside-setup` | `canonical-original` | `original-outside-setup` | `null` |
| `fast-arrival-race` | `untouched-preinstall-near-setup` | `canonical-original` | `original-near-setup` | `null` |
| `slow-contact-av-once` | `clean-derived-before-setup` | `canonical-clean-derived` | `seed-pre-scene-outside-setup` | `clean-ordinary-passive-spawn` |
| `named-exit-only` | `clean-derived-before-scene` | `canonical-clean-derived` | `seed-pre-scene-outside-setup` | `clean-ordinary-passive-spawn` |
| `no-replay-inside-lifetime` | `clean-derived-after-contact-inside-cleanup` | `canonical-clean-derived` | `seed-post-contact-inside-cleanup` | `clean-ordinary-passive-spawn` |
| `post-scene-reload` | `contact-done-inside-cleanup` | `canonical-clean-derived` | `seed-post-contact-inside-cleanup` | `clean-ordinary-passive-spawn` |
| `stream-away-return` | `child-active-before-setup` | `canonical-clean-derived` | `seed-pre-scene-outside-setup` | `clean-ordinary-passive-spawn` |
| `cleanup-boundary-no-pop` | `contact-done-inside-cleanup` | `canonical-clean-derived` | `seed-post-contact-inside-cleanup` | `clean-ordinary-passive-spawn` |
| `completed-reload` | `completed` | `canonical-completed` | `seed-completed` | `clean-ordinary-passive-spawn` |
| `untouched-replay` | `untouched-preinstall-outside-setup` | `canonical-original` | `original-outside-setup` | `null` |
| `removal-isolation-diagnostic` | `completed-disposable-clone-before-removal` | `canonical-completed-diagnostic-clone` | `seed-completed` | `clean-ordinary-passive-spawn` |

The three pre-scene state names are aliases for byte-identical clones of one
`seed-pre-scene-outside-setup` capture. In particular,
`clean-derived-before-scene` does not mean a save between child checkpoint
node `15` and scene node `16`; those nodes are connected directly. Cases 3,
4, and 7 load the same outside-setup bytes into different execution slots.
Cases 5, 6, and 8 likewise share the post-contact capture; Cases 9 and 11
share the completed capture; and Cases 1 and 10 share the outside original.
Case 2 alone uses the separate near-site original. Do not reset
`cqa005_completed`: journal, scene, community, actor, phase, and streamed-world
state can outlive one fact, so a reset would create an unrelated dirty state.

## Build, install, and bind the canonical candidate

Use the unmodified [completed checkpoint](../downloads/cqa-lab-05-completed.zip):

```text
candidate id: canonical
project:      CQA_Lab05_FirstContact.cpmodproj
manifest:     example.json
```

The checkpoint's definitive WolvenKit `8.19.0` structural preflight is eleven
successful cooks and eleven successful serialize-back checks per checkpoint.
Any missing or failed CR2W stops this campaign. Those checks remain
**Structurally validated** evidence only; they do not pass a runtime case.

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
6. Hash both installed files and place the values in
   `candidates[0].installed_files`.
7. Preserve byte-identical copies of both installed files until the complete
   campaign and log audit finish.

From the game directory:

```powershell
Get-FileHash -Algorithm SHA256 `
  .\archive\pc\mod\CQA_Lab05_FirstContact.archive
Get-FileHash -Algorithm SHA256 `
  .\archive\pc\mod\CQA_Lab05_FirstContact.archive.xl
```

Hash the installed pair, not only the ZIP or project source. The archive binds
the executable resources; the loose ArchiveXL file binds their registration.
If either hash changes, stop and begin a new candidate record rather than
mixing runs.

## Capture every execution consistently

For each run, fill:

- `performed_at` with an ISO 8601 timestamp including its UTC offset;
- `tester`;
- every observed environment version;
- the fixed save label, `capture_id`, `source_run_id`,
  `copy_scope: complete-slot-directory`, distinct execution slot directory,
  `created_before_first_install`, `game_closed_before_clone: true`, and
  `sav.dat` SHA-256;
- all four retained log paths and SHA-256 values;
- the case `status`, a concrete `observed` account, and focused evidence paths.

Every completed run must bind a distinct execution instant, a distinct
four-log SHA-256 bundle, and a distinct normalized execution-slot name. Merely
writing the same instant with another UTC offset, copying one log bundle into
multiple run rows, or renaming a slot only by slash style or letter case does
not create independent evidence. Every execution hash must equal its referenced
source-capture hash, so all five frozen groups remain byte-identical while
their execution directories and run evidence stay independent. A derived run
must occur after its recorded Case-1 source run.

Capture a short continuous video with game audio for timing, replay, visible
spawn, scene, and cleanup claims. Add focused screenshots or notes for journal
and pin states. Record the first and last visible contact behavior, the route,
any combat stimulus, and whether a loading screen occurred. Do not use the
video alone for log or save provenance.

Store focused, sanitized evidence beneath `completed/evidence/` only when it
is suitable for publication. Keep `sav.dat`, private identifiers, extracted
vanilla resources, and large unreviewed captures in private evidence storage.

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

Retain the continuous full-route capture, state screenshots, installed pair
hashes, starting save hash, and four logs. Exit the game before hashing and
cloning the three complete seed directories. Do not invent a save between
checkpoint node `15` and scene node `16`; there is no graph gap there.

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
hash-pinned WEM play once; the contact is acquired, the line does not duplicate,
and lipsync/audio errors are absent from retained logs.

Start from `clean-derived-before-setup`, a distinct execution-slot clone of
`seed-pre-scene-outside-setup`. Confirm its hash matches the capture, keep the
contact in view, enter at a walking pace, and remain until the scene completes.
Capture the exact subtitle, audible line, contact performer, and mouth/facial
response in one continuous recording. Count subtitle display and audible
playback separately; each must be exactly one.

Bind the evidence to RUID `9638591835734011695`, the exact five localization
depot paths above, and WEM SHA-256
`0487ba1116d9c4fa9cfb25e825ad4ec35110195cf3953cb8bc67a16f5cbc657f`.
A subtitle without sound, sound without the exact subtitle, duplicate playback,
or a substituted WEM fails the combined lookup case.

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
clone of `seed-post-contact-inside-cleanup`. Confirm its hash, stay inside the
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
of `seed-pre-scene-outside-setup`, and confirm its matching hash. Do not enter
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

Restore a byte-identical copy of the original
`untouched-preinstall-outside-setup` slot. Confirm its `sav.dat` hash matches
the first clean run, then repeat the complete ordinary route without changing
the candidate. Capture every lifecycle boundary from passive spawn through
root completion and compare it with Case 1 plus the A/V and cleanup evidence.

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

With the game closed, copy the complete `seed-completed` source slot directory
to a distinct disposable execution slot. Record both directory names and
confirm that their `sav.dat` hashes match. Preserve the canonical installed
hashes, then move these two exact files out of the game directory:

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

Label every artifact `removal-isolation-diagnostic`. Restore the hash-bound
candidate pair only after the game and framework processes have fully exited.

## Retain and audit four logs per execution

Before starting another run, copy these logs into that run's private evidence
directory:

```text
red4ext\plugins\ArchiveXL\ArchiveXL.log
red4ext\logs\red4ext.log
red4ext\logs\game.log
r6\logs\redscript_rCURRENT.log
```

Hash every copied log. The packaged record predeclares the same four path
objects for every run; fill their hashes without changing the path set. The
promotion rule requires all four logs for the complete eleven-run campaign.

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
and audio observation. One missing or overwritten log makes that execution
ineligible for promotion until it is rerun.

## Complete the schema-version-4 record

Edit `completed/runtime-acceptance.json` only as an evidence record. Do not
change the five save captures, eleven run IDs, lineage groups, case IDs,
preconditions, expected results, `required` flags, candidate identity, depot
inventory, or promotion rule to fit an unexpected result.

The fixed case set is:

| Case ID | Boundary proved |
| --- | --- |
| `clean-ordinary-passive-spawn` | Clean full route plus exactly three manual seed captures at frozen states |
| `fast-arrival-race` | Spawned readiness before already-fast setup entry |
| `slow-contact-av-once` | Named pre-scene seed load, acquisition, and exactly-once subtitle/hash-pinned WEM |
| `named-exit-only` | Same named pre-scene seed load; `contact_done` handoff with default outputs inert |
| `no-replay-inside-lifetime` | Named post-contact seed load; no scene/A/V replay before outer cleanup |
| `post-scene-reload` | Named post-contact seed load continues cleanup once |
| `stream-away-return` | Named pre-scene seed load followed by finite-sector stream unload/return before setup |
| `cleanup-boundary-no-pop` | Named post-contact seed load; delayed deactivation outside 110 m without an in-volume pop |
| `completed-reload` | Named completed seed load; root completion guard prevents re-entry |
| `untouched-replay` | Complete reproduction from original clean bytes |
| `removal-isolation-diagnostic` | Named completed seed clone; exact-pair removal, no reactivation, fresh-log isolation, and no fixture-owned TweakDB mutation |

For every case, set `status` to `passed` or `failed`, write a concrete
`observed` result, and add at least one focused evidence object with exactly
these fields:

```json
{
  "type": "video",
  "reference": "evidence/slow-contact-av-once/continuous-run.mp4",
  "sha256": "<64 lowercase hexadecimal characters>"
}
```

Allowed `type` values are `screenshot`, `video`, `log`, `save-metadata`, and
`notes`. Every `reference` must be a unique POSIX-style relative path beneath
`completed/evidence/`, name a regular non-linked file, and match that file's
SHA-256. Sanitize focused notes, images, log excerpts, and save metadata before
committing them. Never commit `sav.dat`, private identifiers, extracted
vanilla resources, or large unreviewed captures.

A statement such as “worked” is insufficient. Bind the exact installed
candidate, source capture, closed-game full-slot execution clone, route,
visible outcomes, canonical WEM, and copied logs. When the derived status
becomes `failed` or `passed`, set the top-level `date` to the `YYYY-MM-DD`
calendar date carried by the chronologically latest completed run's
`performed_at` timestamp. Keep it `null` while the campaign remains pending.

Every acceptance or evidence edit changes manifest and package inputs. Refresh
them in this order from the repository root:

```powershell
python -B scripts\build_lab05_diagrams.py
python -B scripts\validate_lab05.py --write-manifest
python -B scripts\validate.py
```

The first command synchronizes SVG evidence labels. The second regenerates the
manifest's complete checkpoint/evidence, shared-file, and diagram hash maps
and derives `evidence.runtime` plus `audio.runtime` from the acceptance record.
The global validator then builds both ZIPs twice in temporary directories and
checks their exact bytes. For a local site preview, build the book before
placing the same packages in its ignored output tree:

```powershell
mdbook build .\book
python -B scripts\package_examples.py
```

A stale hash map, changed case contract, missing candidate hash, incomplete
save provenance, unsafe evidence path, or missing log must fail review.

## Promotion rule

Apply the packaged rule literally: set top-level `status` to `passed` and
`evidence_class` to `runtime-proven` only when all eleven required cases pass
and evidence binds the exact candidate build, both immutable original
captures, all three manual Case-1 seed captures, every closed-game full-slot
execution clone, exact versions, visible observations, canonical WEM hash, and
all four logs for the complete campaign. Structural round trips alone never
promote the combined `cqa005` fixture.

Status derivation is:

- any failed required case makes top-level status `failed` and keeps
  `evidence_class: experimental`;
- a mixture of pending and passed required cases keeps status `pending` and
  class `experimental`;
- only eleven passed required cases permit status `passed` and class
  `runtime-proven`.

The synchronized marker set contains exactly 22 pages. Use this checklist for
every pending, failed, or passed evidence update:

- [ ] `README.md`
- [ ] `HANDOFF.md`
- [ ] `ROADMAP.md`
- [ ] `book/src/introduction.md`
- [ ] `book/src/communities/index.md`
- [ ] `book/src/communities/activation-readiness-and-acquisition.md`
- [ ] `book/src/communities/entries-phases-and-ai-spots.md`
- [ ] `book/src/communities/registries-and-areas.md`
- [ ] `book/src/communities/cleanup-and-character-safety.md`
- [ ] `book/src/scenes/index.md`
- [ ] `book/src/scenes/resource-anatomy.md`
- [ ] `book/src/scenes/actors-and-performers.md`
- [ ] `book/src/scenes/screenplay-sections-and-events.md`
- [ ] `book/src/scenes/one-spoken-line.md`
- [ ] `book/src/scenes/entry-exit-and-quest-handoff.md`
- [ ] `book/src/scenes/cleanup-and-save-state.md`
- [ ] `book/src/scenes/lab-05.md`
- [ ] `book/src/scenes/lab-05-authoring.md`
- [ ] `book/src/scenes/lab-05-test.md`
- [ ] `examples/lab-05-first-contact/README.md`
- [ ] `examples/lab-05-first-contact/start/README.md`
- [ ] `examples/lab-05-first-contact/completed/README.md`

If the full matrix passes, change all 22 markers in the same evidence commit
to:

```text
**Lab 5 runtime evidence:** **Runtime-proven** — passed.
```

If any required case fails, synchronize those markers to:

```text
**Lab 5 runtime evidence:** **Experimental** — failed.
```

For either terminal status, replace `Not yet recorded` in the `Runtime test
date` row of the overview, authoring, and test pages with the exact top-level
acceptance `date`. Keep that row unchanged while the derived status is
`pending`.

The synchronized marker is authoritative for acceptance-gated `cqa005` claims:
pending or failed remains **Experimental**, while eleven passed cases permit
**Runtime-proven**. A failure is retained evidence, not permission to loosen
the case or cite the old archive hashes as proof.

Marker promotion does not cover active-line interruption/return or
`CutDestination`, arbitrary or unlisted pre-scene active-child states,
active-line/interruption reload, or facial/workspot-animation quality. The
exact named pre-scene seed loads in Cases 3, 4, and 7 are covered by the frozen
campaign. The excluded claims remain **Experimental** until separate retained
evidence proves them.

## Failure triage

Preserve the failed run, save hash, candidate pair, video, and all four logs
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
| Completed reload starts the child | Failed completion guard/write order or dirty candidate/save provenance |
| Removal run still mounts Lab 5 | Failed removal isolation; search for duplicate archive pairs and preserve fresh framework logs |
| Packaged project contains a tweak or script mutation | Reject the candidate; Lab 5 may reference the generic record but must not override or mutate it |
| One log or hash is missing | Execution cannot satisfy promotion; rerun from the recorded source state |

Previous: [Author First Contact in WolvenKit](lab-05-authoring.md).
