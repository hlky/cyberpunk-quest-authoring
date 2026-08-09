# Cleanup and save state

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

Scene termination is not quest completion, and quest completion is not world
cleanup. First Contact makes every boundary visible so one successful spoken
line cannot hide a leaked actor, stale marker, or save-backed old graph.

## Five different completion boundaries

| Boundary | Native owner | What it establishes | What it does not establish |
| --- | --- | --- | --- |
| Section normal output | `.scene` graph | The timed line section reached its normal socket | A public named outcome or quest transition |
| End node `3` | `.scene` graph | The scene reached a terminating graph node | Community deactivation or a persistent completion fact |
| Exit `contact_done` | `.scene` + `questSceneNodeDefinition` interface | The child phase can continue through the matching output | Cleanup has occurred |
| Child phase output | Child `.questphase` | Meet/leave objectives and community teardown completed | The root completion guard/fact has been updated |
| Fact `cqa005_completed` | Root `.questphase` and save | Later starts can take the already-completed route | Journal, scene, or community state was automatically erased |

Do not collapse these into a generic “end.” In particular, there is no
quest-scene-node output called `end`; the public success name is
`contact_done`.

## Exact completed lifecycle

The completed child phase orders actor readiness, scene handoff, and teardown:

```text
child Input
  -> meet objective Active
  -> contact mappin Active
  -> community Activate
  -> CharacterSpawned
  -> setup trigger IsInside
  -> checkpoint
  -> scene start
  -> scene contact_done
  -> meet objective Succeeded
  -> contact mappin Inactive
  -> leave objective Active
  -> cleanup trigger IsOutside
  -> community Deactivate
  -> leave objective Succeeded
  -> child Output
```

After the child returns, the root succeeds the quest journal state, writes
`cqa005_completed`, and exits. On a later activation, its completion guard can
bypass the child rather than spawning the contact again.

The order is intentional:

- `CharacterSpawned` prevents the scene racing a community entry that has not
  materialized;
- `contact_done` is consumed before the meet objective and pin change;
- the leave objective makes delayed cleanup visible to the player;
- `IsOutside` avoids deactivating the contact at speaking distance;
- deactivation completes before the leave objective and child output;
- the durable completion fact is written only after the child returns.

A failed or interrupted scene must not accidentally reach the same success
chain. The frozen Lab 5 matrix gates the exact ordinary `cqa005` completion
through `contact_done`, which follows the synchronized marker above.
Active-line interruption, `CutDestination`, and interrupted recovery remain
**Experimental** and need a separate retained runtime record.

## Scene interruption is not cleanup

The scene's Default interruption scenario reacts when speaker distance rises
above `6` and permits return after it falls below `5`. With
`playInterruptLine: 1` and `talkOnReturn: 1`, it describes how the conversation
may interrupt and resume.

That policy is separate from all of these:

- `scnEndNode` `3` and named exit `contact_done`;
- the quest scene node's unconnected `Default INT` and `Default RET` outputs;
- its empty `interruptionOperations`;
- its unconnected `CutDestination`;
- the wider `IsOutside` cleanup condition;
- community `Deactivate`;
- the persistent completion fact.

Do not route a six-unit conversational interruption directly to world cleanup.
The player may return within five units and continue. Conversely, reaching End
does not remove the community; the questphase retains it until the leave
boundary is crossed.

`notAllowedToBeFrozen: 0`,
`reapplyInterruptionOperationsAfterGameLoad: 0`, and `syncToMusic: 0` are exact
scene-node values in the fixture. They are not proof of save/reload or cut
semantics. Those behaviors require runtime observation.

## State that can outlive an archive edit

Treat these as separate save variables while diagnosing the lab:

| Save-backed or persistent area | First Contact example |
| --- | --- |
| Facts | `cqa005_completed` and any prior probe values |
| Journal | Quest/objective state, visited state, tracked entry, and mappin state |
| Quest graph | Active root/child nodes and checkpoint progress |
| Scene | Active or interrupted scene state and its return path |
| Community | Activation, spawned entries, phase/workspot state, and deactivation progress |
| Devices | Controller persistent state if a later lab adds a device; no device is required by this one-line scene |

Replacing a `.scene`, `.questphase`, or archive does not clear these domains.
Resetting only `cqa005_completed` is also insufficient: a save can still retain
an active child, journal state, checkpoint, scene, or community from an older
payload. See [Facts, journals, and
saves](../foundations/persistent-state.md).

## Practical cleanup matrix

Run this matrix on Cyberpunk 2077 Windows GOG `2.31a` with WolvenKit `8.19.0`,
ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`. Record the packed
payload hashes, exact save provenance, installed framework versions, and result
for every row.

The [frozen eleven-case Lab 5 campaign](lab-05-test.md) is the only promotion
contract for the supplied checkpoint. This broader design matrix includes
active-scene reload and interruption probes as explicitly supplemental work;
those rows cannot promote the checked candidate and need their own retained
runtime record.

> The frozen campaign begins from two untouched manual-save originals, then
> Case 1 creates the three named manual seeds under the unchanged candidate.
> Cases 3/4/7, 5/6/8, and 9/11 load distinct full-slot clones from their
> respective seed. Close the game before cloning. Never use an autosave,
> checkpoint save, or a save carried forward from a failed or differently
> hashed candidate as positive evidence.

| Case | Save point and action | Required observations |
| --- | --- | --- |
| Normal route | Clean save; approach, hear the line, leave the outer cleanup area | Contact is ready before launch; line occurs once; `contact_done` advances; pin changes; community deactivates after leaving; objectives and fact finish once |
| Named pre-scene loads (Cases 3/4/7) | Load a distinct byte-identical clone of `seed-pre-scene-outside-setup`, then follow the exact case route | No duplicate contact or objective transition; actor reacquires; Cases 3/4 start once and Case 7 survives its stream-away/return |
| Arbitrary pre-scene save/load | Save at any unlisted active-child point, then load | Supplemental only: exact behavior is recorded without promotion |
| Active-scene reload | Where saving is permitted, save during the line or interruption and reload; otherwise record the nearest game-provided checkpoint | No crash, stale speaker, duplicate line, false success, or leaked Cinematic AI state; exact behavior is recorded rather than inferred |
| Interrupt and return | Cross above 6 units during the line, then return below 5 | Default interruption/return behavior is coherent and does not trigger cleanup or completion accidentally |
| Named post-contact loads (Cases 5/6/8) | Load distinct clones of `seed-post-contact-inside-cleanup`, then follow the exact case route | Meet and pin state remain correct; replay is suppressed; cleanup/deactivation occurs once |
| Named completed loads (Cases 9/11) | Load distinct clones of `seed-completed` under each case's installation condition | Root guard or removal isolation behaves as frozen; final journal state does not reactivate the quest |
| Case 7 stream away and return | Load its `seed-pre-scene-outside-setup` clone, leave the finite Quest descriptor by ordinary movement, return, and finish | NodeRefs reacquire, active stage remains coherent, and no duplicate community/scene launch occurs |

If a case cannot be executed because the game forbids saving at that moment,
record that limitation. Do not convert an untested save point into a passing
claim.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Contact vanishes during the line | Cleanup branch reached too early, wrong trigger state/NodeRef, or an interruption route was conflated with deactivation |
| Contact remains after leaving | `IsOutside` condition, community target/scope, `Deactivate` operation, or active save state from an older graph |
| Meet succeeds but leave objective never appears | Connection order after `contact_done`, journal socket names, and pin-inactive node |
| Quest finishes but contact remains | Root fact/journal completion bypassed child cleanup, or deactivation occurred after rather than before child output |
| Quest restarts after completion | Completion fact write, root guard comparison/branch, or test save provenance |
| Behavior changes only after reload | Active quest checkpoint, scene interruption state, community phase, journal state, and candidate hash |
| Start checkpoint completes the meeting | Root or child start graph invokes the inert Start `1` -> End `3` scene shell; remove that invocation from the start project |

## Evidence boundary

The separation of scene exit, quest handoff, durable state, and community
cleanup is supported by **Observed in vanilla** resource patterns. Retained
legacy candidates make community activation, spawn readiness, delayed
deactivation, and a community-acquired scene route **Runtime-proven** within
their recorded payloads. The exact First Contact ordering and resources are
**Structurally validated**. Exact ordinary `cqa005` behavior, including the
named pre-scene seed loads in Cases 3/4/7 and the post-`contact_done` and
completed reload cases, follows the synchronized marker above. Active-line
interruption and return, `CutDestination`, arbitrary/unlisted pre-scene states,
and active-line/interruption reload remain outside the frozen Lab 5 campaign
and **Experimental** unless separate acceptance records prove them.

Previous: [Author one spoken line](one-spoken-line.md). Back to:
[Scenes](index.md).
