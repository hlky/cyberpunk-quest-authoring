# Clue layers, cleanup, and acceptance

Layered clues are not decorations on recorded animation. Each clue has a
timeline window, an analysis layer, a target entity, discovery behavior, and a
quest-state handoff. Normal exit, interruption, and replay must agree about
which of those results persist.

| Record | Value |
| --- | --- |
| Research review | 2026-08-09 |
| Game / inspection | Cyberpunk 2077 Windows GOG `2.31a`; WolvenKit `8.19.0` |
| Practical framework baseline | ArchiveXL `1.27.0`; RED4ext `1.30.0`; redscript `0.5.31` |
| Custom runtime evidence | **Experimental** — all eight required cases pending |

> **Research note:** layered clue events, BD visibility events, scene-side
> discovery nodes, layer/perspective conditions, and support props are
> **Observed in vanilla** in the cited SQ012/Q004 resources. The retained
> mod-owned scene serializes these shapes and is **Structurally validated**.
> No custom package has a retained eight-case pass, so layer switching,
> discovery, cleanup, interruption, and replay remain **Experimental**.

## The clue ownership chain

```text
rewindable timeline interval
  -> scneventsClueEvent(layer, clueName, entity, time range)
       -> placed/acquired clue entity
       -> BD layer/perspective conditions
       -> questDiscoverBraindanceClue_NodeType or focused clue operation
       -> dedicated discovery fact
       -> questphase fact wait/join
       -> journal objective and terminal outcome
```

Do not skip from “the highlight was visible” to “the quest recorded the clue.”
Those observations sit at different points in the chain.

## What a clue event owns

The focused SQ012 `scneventsClueEvent` entries expose these properties:

| Property | Responsibility |
| --- | --- |
| `clueName` (`CName`) | Scene-local semantic name for the clue |
| `layer` | Analysis layer such as `Visual` or `Audio` |
| `startTime` / `duration` | Interval during which the clue belongs on the recording timeline |
| `clueEntity` (`gameEntityReference`) | Target actor/community entry or standalone world `NodeRef` |
| `markedOnTimeline` | Whether the event contributes a timeline marker |
| `factName` / `overrideFact` | Optional event-owned fact behavior; do not assume every vanilla clue uses it |
| `type`, `executionTagFlags`, `scalingData` | Additional event behavior that must be preserved/understood rather than dropped |

One inspected visual clue addresses actor name `holt` through community
`#sq012_com_braindance`; an audio clue addresses standalone NodeRef
`#sq012_ent_rqr_audio_clue`. These are **Observed in vanilla** examples of two
entity-reference shapes. They are not reusable identifiers.

The same SQ012 rewindable section contains six clue events: visual and audio
examples, each with its own interval. The larger Q004 Yorinobu scene contains
visual/audio/thermal analysis logic, 23 clue-toggle events, 27
`questDiscoverBraindanceClue_NodeType` nodes, and 112
`scnBraindanceLayer_ConditionType` values in the focused current extraction.
Those counts describe that exact main-quest scene; they are not minimums.

## Layer state and discovery state are different

Keep at least four state questions separate:

1. Which analysis layer is currently selected?
2. Is the playhead inside this clue's time interval?
3. Is the clue entity available and focusable?
4. Has the clue's discovery result already been committed?

A Boolean design should usually require the applicable layer and interval
before enabling focus/discovery. A discovery fact may intentionally remain
true after the playhead rewinds or the player switches layers. That persistence
must be an explicit quest design decision.

Use one dedicated fact per independently required clue. Joining three clue
facts with a logical AND makes completion readable and testable:

```text
visual_clue_found > 0 ---\
audio_clue_found > 0 ----- AND -> update objective -> enable finish/exit
thermal_clue_found > 0 ---/
```

This graph records discovery; it does not enforce simultaneous layer state.
See [Boolean trees](../gates/boolean-trees.md) and [Signal
flow](../gates/signal-flow.md).

## Inspect and author clues in WolvenKit

Start in a disposable inspection project with
`base\quest\side_quests\sq012\scenes\sq012_02a_braindance.scene` and
`base\quest\main_quests\prologue\q004\scenes\q004_05_bd_yorinobu.scene`.
For one clue in each resource, record the event type, layer, clue name,
start/duration, entity-reference shape, timeline-marker policy, discovery
operation, fact, and downstream journal/finish route. Do not add either
vanilla scene to a distributable project.

For a mod-owned candidate, compose one layer at a time:

1. Place or acquire one mod-owned clue entity and give it a fresh full
   `NodeRef` or actor/community reference.
2. Add one `scneventsClueEvent` to the rewindable section with an interval
   entirely inside the section duration.
3. Set the exact analysis layer and decide whether the clue is marked on the
   timeline.
4. Add the layer/interval/focus path and one discovery operation.
5. Write one dedicated fact and wait for that exact fact in the owning
   questphase before changing journal state.
6. Add the clue's temporary focus/highlight state to both normal and
   interrupted cleanup ledgers.
7. Serialize the `.scene` to CR2W, reopen or serialize it back to JSON, and
   verify that event identity, layer, interval, entity reference, and fact
   survived.
8. Repeat for audio and thermal only after the visual clue passes structural
   inspection; do not duplicate scene-local IDs or facts.

WolvenKit round trips and a visible property graph support **Structurally
validated**. They do not prove that the runtime switches layer, discovers the
entity, writes the fact, or reconstructs the clue after a seek.

## Support props are lifecycle resources

BD view, fog, and setup are separate scene props in the inspected SQ012 scene.
Their `scnPropDef` entries use a `Props.*` `TweakDBID`, a spawn/despawn
acquisition plan, a unique dynamic entity name, and a global support-marker
`NodeRef`.

The corresponding focused vanilla entity resources are:

```text
base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdview.ent
base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdfog.ent
base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdsetup.ent
```

The view/fog entities are mesh-bearing `entEntityTemplate` resources. The
setup entity includes `entRenderToTextureCameraComponent`. Their scene
definitions, TweakDB records, entity paths, spawn marker, visibility events,
and cleanup policy must agree.

The camera is another prop/world entity and another RID binding. Do not use
the BD setup prop as evidence that the recorded-perspective camera exists or
that the gameplay camera was restored.

## Separate temporary and durable state

Classify every mutation before building the exit routes.

| State | Typical owner | Normal-exit policy | Interrupted-exit policy | Replay policy |
| --- | --- | --- | --- | --- |
| Selected layer / playback speed | BD scene/runtime UI | Reset | Reset | Start from documented default |
| Gameplay camera and render-to-texture state | Scene events/support entities | Restore | Restore | Reacquire from clean state |
| Input/UI/action masks | Quest/scene managers | Restore | Restore | Reapply only on entry |
| Player hold/return placement | Questphase/world anchors | Return safely | Return safely | Re-enter through entry gate |
| Spawned view/fog/setup/camera props | Scene acquisition | Despawn/release | Despawn/release | Fresh acquisition |
| Temporary clue focus/highlight | Scene/clue system | Clear | Clear | Reconstruct from playhead/layer |
| Discovery fact | Facts database | Preserve or reset by explicit design | Same explicit policy | Must match documented replay design |
| Journal objective state | Journal resource/save | Commit only at defined handoff | Do not accidentally commit | Resume or remain complete by explicit design |
| Active scene/phase state | Scene and questphase/save | Reach named exit/terminal output | Reach interruption cleanup/output | Must not retain a stuck active owner |

If normal and interrupted cleanup disagree on temporary state, the second run
is not a valid replay test.

## Normal exit contract

A conservative quest-side route is:

```text
prepare world and acquire performers
  -> place/hold player and set required UI/input state
  -> start rewindable scene at named input and origin
  -> receive named normal outcome
  -> restore camera/render/UI/input state
  -> return player to safe anchor
  -> release support props and transient owners
  -> commit discovery/journal outcome once
  -> complete child phase
```

The exact manager nodes depend on the candidate. Explain every changed state
and its inverse. Delay only when the target system has an asynchronous
lifecycle that requires it; a magic sleep is not a cleanup proof.

## Interrupted exit contract

Interruption may arrive while an actor, camera, clue, or support effect is
active. It therefore needs a first-class route, not a connection directly to
the normal terminal node:

```text
interruption / CutDestination / abort signal
  -> stop or cut scene ownership
  -> disable discovery interaction
  -> restore camera/render/UI/input state
  -> return player if relocation occurred
  -> release props, actors, and transient world operations
  -> preserve or roll back durable facts according to policy
  -> leave through a named, testable phase output
```

The inspected SQ012 scene includes one enabled distance-based
`scnInterruptionScenario` with different interrupt and return thresholds.
That is **Observed in vanilla** scene structure. It does not prove that an
arbitrary custom questphase's `CutDestination` or cleanup path is correct.

See [Complex cleanup, interruption, and
cancellation](../questphases/cleanup-interruption-and-cancellation.md) for the
cross-system ownership ledger.

## Save and replay boundary

Facts, journal state, quest checkpoints, active scene state, spawned
communities, and some device/world state can survive archive replacement.
Every runtime case must record the exact starting save and package hash.

Prepare at least these save seeds:

- `seed-before-install`: created before any version of the candidate was
  installed;
- `seed-before-entry`: candidate installed, quest available, BD child not yet
  active;
- `seed-in-playback-early`: optional diagnostic only; never substitute it for
  the clean normal-entry case;
- `seed-after-normal-cleanup`: produced by the exact package under test and
  used only for the replay case.

Do not load a mid-scene save captured from an older archive to test a rebuilt
RID or event table. The save may retain an active scene/checkpoint layout that
no longer matches the package.

## Mandatory eight-case runtime matrix

All eight rows are required for the same packaged candidate. A pass in one row
cannot promote another.

| Case | Start and action | Required observations | Failure boundary |
| --- | --- | --- | --- |
| Case 1 — forward seek | Clean `seed-before-entry`; enter normally, then seek from an early time to a later time crossing actor, camera, and clue intervals | Correct reconstructed actor/camera/prop state at destination time; no duplicated durable side effect; controls remain responsive | Ordinary linear playback is not a forward-seek pass |
| Case 2 — backward rewind | Separate clean clone; play to a later interval, rewind across camera/body/clue boundaries, then resume | Earlier pose/camera/visibility/focus state is reconstructed; no stuck later effect; resume remains coherent | Moving the playhead without reconstructing state fails |
| Case 3 — visual layer | Separate clean clone; select visual layer during a visual clue interval and discover it | Only intended visual clue is available; timeline/entity/focus agree; exact visual fact changes once; journal does only the documented work | Seeing a highlight without fact/journal proof fails |
| Case 4 — audio layer | Separate clean clone; select audio layer during an audio clue interval and discover it | Intended audio clue and playback/focus behavior appear; exact audio fact changes once; other facts remain unchanged | Hearing scene audio is not an audio-clue pass |
| Case 5 — thermal layer | Separate clean clone; select thermal layer during a thermal clue interval and discover it | Intended thermal clue is available only under the documented conditions; exact thermal fact changes once | A visual/VFX approximation is not a thermal-layer pass |
| Case 6 — normal cleanup | Separate clean clone; discover required clues and leave by the normal scene outcome | Camera, render state, UI/input, player placement, performers, support props, highlights, quest child, facts, and journal match the ownership ledger; save/reload remains stable | Reaching the next objective while leaking temporary state fails |
| Case 7 — interrupted cleanup | Separate clean clone; interrupt at the most stateful documented point (active RID camera plus clue/support effects) | Cut route runs once; player/camera/UI/input/world owners are safe; durable-state policy is honored; reload is stable | Testing interruption before playback acquires anything is insufficient |
| Case 8 — replay after cleanup | Load `seed-after-normal-cleanup` made by this exact candidate; invoke the documented replay/resume route | Replay eligibility matches policy; scene starts from a coherent state; preserved discoveries and reset temporary state behave exactly as documented; second cleanup succeeds | Restarting from a pre-entry clean save is not replay-after-cleanup |

For every row, retain:

- case ID and pass/fail;
- exact archive/package SHA-256 plus every external asset hash;
- game, WolvenKit, ArchiveXL, RED4ext, redscript, and relevant audio/animation
  tool versions;
- starting-save identity and provenance;
- expected and observed facts/journal states before and after;
- expected and observed actor, prop, camera, UI/input, player-placement, and
  scene/phase ownership;
- timestamps or screenshots/log excerpts sufficient to audit the observation;
- unexpected behavior and whether the case was rerun from a fresh clone.

Only a retained record with all eight cases passed may support a bounded
**Runtime-proven** claim for that exact package. Rebuilding any `.questphase`,
`.scene`, `.scenerid`, entity, world resource, TweakDB registration, audio, or
animation asset invalidates the package binding and requires the affected
matrix to be rerun.

## Promotion language

Use exact language:

- **Structurally validated:** “The mod-owned questphase, scene, and RID
  serialize and their typed reference inventory is internally consistent.”
- **Experimental:** “The candidate has not completed the eight-case runtime
  matrix.”
- **Runtime-proven:** only after all eight retained rows pass, and only for
  the exact package/version/save boundary named by the record.

Never use “working pipeline,” “game-ready,” or “validated in game” as a
substitute for the case table and hashes.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Correct layer, no focusable clue | Event interval, `layer`, clue entity reference, entity streaming/acquisition, and focus toggle |
| Clue highlights but fact remains zero | Discovery node/event path, exact fact name, `overrideFact`, signal ordering, and save provenance |
| Fact changes but objective does not | Questphase fact condition, logical join, journal path/state, and one-shot guard |
| Rewind leaves highlight/VFX behind | Event interval reconstruction, layer condition, clue/VFX end state, and side effects crossed by reverse playback |
| Normal exit leaves BD presentation active | View/fog/setup prop cleanup, camera/render restoration, UI/input masks, and named outcome route |
| Interrupted exit strands the player | Cut route, scene ownership termination, player return anchor, and cleanup ordering |
| Replay skips or instantly completes | Preserved discovery facts, journal state, completion fact, active scene state, and explicit replay gate/reset |
| Old and new builds behave differently on the same save | The save is contaminated evidence; return to a documented clean seed before changing resources |

This is the final braindance page. Return to [Braindance and specialized
scenes](index.md) or continue to [Troubleshooting](../troubleshooting/index.md).
