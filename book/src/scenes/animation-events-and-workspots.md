# Animation events and workspots

A scene can schedule skeletal animation directly, change an actor's idle or
look-at state, or ask a scene-local quest node to place an actor in a workspot.
Those mechanisms overlap visually, but they have different resource owners,
completion signals, placement rules, and cleanup obligations.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Focused `mq007` and `mq010` shapes | **Observed in vanilla** |
| Lab 5 empty animation collections and scene-local PuppetAI branch | **Structurally validated** |
| New cinematic animation, camera, look-at, or scene-workspot route | **Experimental** |

> **Clean-save requirement:** active scene state, actor AI tier, workspot use,
> transforms, quest checkpoints, and community ownership may survive a rebuild
> or reload. Test from an untouched save made before actor activation and scene
> start. Give changed scene/workspot identities a new candidate namespace when
> an older save could retain them.

This page teaches native scene composition and inspection. It does not teach
animation creation, rigging, retargeting, or Wwise/lipsync production, and it
does not require a project-specific scene generator.

## Pick the correct owner

| Desired behavior | Native mechanism | Primary completion/lifetime owner |
| --- | --- | --- |
| Play a timed body clip inside a section | `scnPlaySkAnimEvent` | Event timing plus the owning section |
| Transition facial or idle state | `scnChangeIdleAnimEvent` | Event timing and subsequent reset/transition events |
| Aim eyes/head/body at a target | `scnLookAtEvent` | Start/stop request data and later scene events |
| Override player-camera parameters | `scneventsCameraParamsEvent` or a compatible camera event family | Event duration, reset flags, and scene interruption/exit |
| Put an actor into a scene-local workspot | `scnQuestNode` wrapping `questUseWorkspotNodeDefinition` | Workspot node outputs, actor AI, instance placement, and cleanup |
| Keep a community NPC at a world AI spot outside the scene | Community plus `worldAISpotNode` and `.workspot` | Community activation/phase and world streaming |

A direct animation event does not create a workspot or navigate an actor to
one. A workspot node does not schedule an arbitrary `scnPlaySkAnimEvent` in a
section. A world AI spot is not the same object as a scene-local
`scnWorkspotInstance`.

## The cinematic animation join

The smallest useful engine view is a three-way join:

```text
resouresReferences
  cinematicAnimSets[slot] -> soft .anims depot path
  cinematicAnimNames[slot] -> names available in that set
                ^
                |
actor.bodyCinematicAnimSets[] -> slot
                ^
                |
section.events[]
  scnPlaySkAnimEvent.performer -> actor
  scnPlaySkAnimEvent.animName  -> a compatible available name
```

### Focused `mq007` observation

Inspect the installed resource:

`base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene`

Its root contains cinematic animation slot `0` with this soft asset:

`base\animations\quest\minor_quests\mq007\anim\body\mq007__talking_gun__male_fpp.anims`

The corresponding `cinematicAnimNames[0]` row lists three names. V's
`bodyCinematicAnimSets` contains `scnCinematicAnimSetSRRefId(0)`. One focused
event then uses:

| `scnPlaySkAnimEvent` property | Observed value |
| --- | --- |
| Performer | `scnPerformerId(257)` |
| Component | `body` |
| Animation name | `stand__equip__skippy__01` |
| Event ID | unsigned `2159138510383108096` |
| Start/duration | `0` / `2600` ms |
| Body-part mask | `spine_upper_body` |
| Root motion enabled | `0` |
| Blend-in / blend-out | `0.5` / `0` |

This exact table is **Observed in vanilla**. The row proves how that scene
connects an asset, an actor-visible slot, and a timed event. It does not prove
that the animation is compatible with another rig, perspective, body type,
component, mask, root-motion mode, or scene marker.

### Event time is not graph completion

An animation event lives inside a section and has `startTime` and `duration`.
The section separately has its own duration and output sockets. Therefore:

- an event ending does not emit a questphase signal;
- a section that ends too early can clip an event;
- a section staying open longer can preserve blend-out or following events;
- an event ID is not an animation-set slot or graph-node ID;
- reaching the next scene node does not by itself reset AI, camera, look-at,
  or workspot state.

When events overlap, calculate the latest required event end and account for
tested transition/reset time. Do not copy Lab 5's 400 ms spoken-line tail as a
universal animation constant.

## Direct animation, idle, look-at, and camera boundaries

The `mq010` scene contains several event families in the same sections:

`base\quest\minor_quests\mq010\scenes\mq010_02_barry_talk.scene`

**Observed in vanilla:** focused inspection finds `scnPlaySkAnimEvent`,
`scnChangeIdleAnimEvent`, `scnLookAtEvent`, and
`scneventsCameraParamsEvent` rows. Their decisive responsibilities differ:

| Event family | Fields to audit first | Common missing boundary |
| --- | --- | --- |
| Play skeletal animation | performer, component, anim name, set visibility, start/duration, blend, root motion, mask | Rig/asset compatibility and exit pose |
| Change idle/facial state | performer, facial keys, transition, duration, enabled state | Explicit transition/reset on every exit |
| Look at target | source performer, target performer/actor/prop, target slot, start/stop request, transition and limits | Clearing or replacing the request after branch/interruption |
| Camera parameters | player-camera flag, camera ref, FOV/DOF overrides, duration, reset flags | Restoring camera state on interrupt, return, and named exit |

Copying one event without its partner reset, target, animation-set row, or
section timing creates a different contract. A visually acceptable normal run
does not prove interruption or reload cleanup.

## The scene-workspot identity chain

A scene-local workspot has more identities than the `.workspot` path:

```text
workspots[]
  scnWorkspotData_ExternalWorkspotResource
    dataId ------------------------------+
    workspotResource -> .workspot        |
                                          v
workspotInstances[]                       dataId
  workspotInstanceId <--------------------+
  localTransform + originMarker
           ^
           |
scnQuestNode / questUseWorkspotNodeDefinition
  entityReference -> actor
  paramsV1.workspotInstanceId
  Work Started / Success outputs
```

### Focused `mq010` observation

One inspected route in `mq010_02_barry_talk.scene` joins:

| Layer | Exact observed value |
| --- | --- |
| External workspot resource | `base\workspots\common\wall\generic__stand_wall_lean_left__stand_around__01.workspot` |
| `scnSceneWorkspotDataId` | `4010771317` |
| `scnSceneWorkspotInstanceId` | `241` |
| Wrapper scene node | `scnQuestNode` `241` |
| Inner native node | `questUseWorkspotNodeDefinition`, ID `241` |
| Actor target | entity reference `#mq010_com_barry`, name `barry` |
| Params type | `scnUseSceneWorkspotParamsV1` |
| Workspot outputs | `Work Started`, `Success` |
| Debug symbol | workspot instance `241` mapped to scene node `241` |

The repeated value `241` is the arrangement in this one route; it does not
collapse the typed ID domains. Its data ID remains a distinct value, and other
vanilla resources may choose different node/instance relationships.

The instance also owns a local transform and an `originMarker`. That placement
is interpreted in the scene's location context. A valid `.workspot` path does
not supply the correct actor, transform, scene marker, navigation, or
interruption behavior.

The observed params include fields such as `changeWorkspot`, `entryId`,
`instant`, `isPlayer`, `isWorkspotInfinite`, `jumpToEntry`, `movementType`,
`teleport`, and player camera settings. Do not copy those values as a generic
recipe. Extract a route whose player/NPC role, movement, camera, entry, and
lifetime match the intended beat, then preserve and test its complete
contract.

For persistent world AI spots and device-owned interaction workspots, use
[Workspots and interactions](../patterns/workspots-and-interactions.md). The
scene-local rows described here do not replace community or device ownership.

## Manual WolvenKit authoring procedure

No downloadable cinematic-animation or scene-workspot checkpoint is claimed
by this page. Lab 5 supplies a **Structurally validated** v5 scene with typed
empty
collections; every added event, asset slot, or workspot route is a new
**Experimental** candidate.

### Add one direct animation event

1. Extract an evidence-matched vanilla scene and the referenced `.anims`
   metadata from your own installation for inspection. Cite the asset; do not
   redistribute it.
2. Confirm the target actor's rig, perspective, component, body type, and
   acquisition route match the comparison closely enough to justify a test.
3. In the mod-owned scene root, add one
   `scnCinematicAnimSetSRRef` to `cinematicAnimSets` with the exact soft depot
   path and deliberate override/priority values.
4. At the matching collection slot, add `scnAnimSetAnimNames` containing only
   the animation names expected from that set. Add the slot's
   `scnCinematicAnimSetSRRefId` to the intended actor's
   `bodyCinematicAnimSets`.
5. Add one `scnPlaySkAnimEvent` to a section. Assign a unique full unsigned
   `scnSceneEventId`, the correct performer, component, animation name,
   start/duration, blend, mask, and root-motion settings.
6. Size the section and subsequent transition deliberately. Add required
   reset/idle/look-at/camera events rather than assuming End cleans them up.
7. Save and reopen the scene in WolvenKit `8.19.0`. Convert a focused copy to
   JSON and verify collection indices, actor visibility, event name,
   performer, timing, and all typed IDs.

### Add one scene-local workspot route

1. Add a `scnWorkspotData_ExternalWorkspotResource` row with a unique
   `scnSceneWorkspotDataId` and evidence-matched `.workspot` depot path.
2. Add one `scnWorkspotInstance` whose `dataId` selects that row. Allocate a
   unique typed instance ID, then set its origin marker and local transform.
3. Add/update the corresponding `scnWorkspotSymbol` debug row if the chosen
   vanilla-compatible shape uses it.
4. Add an `scnQuestNode` wrapper around
   `questUseWorkspotNodeDefinition`. Target the acquired actor exactly and use
   `scnUseSceneWorkspotParamsV1.workspotInstanceId` to select the instance.
5. Copy the complete params/socket shape from a compatible player or NPC case;
   do not infer `teleport`, `instant`, infinite use, entry IDs, or camera
   behavior from their names alone.
6. Route `Work Started`, `Success`, interruption, and cut behavior according to
   the narrative requirement. Decide which output is allowed to advance the
   scene and which owner releases the actor.
7. Inspect data/instance/node/debug joins after a WolvenKit round trip. Pack and
   list the archive before entering the game.

A successful save, CR2W conversion, and pack promote the exact serialization
only to **Structurally validated**. They do not prove animation playback,
navigation, camera quality, workspot success, or cleanup.

## Acceptance and lifecycle matrix

| Case | Required observation |
| --- | --- |
| Normal approach from untouched save | Actor reaches expected start state; event/workspot starts once |
| Animation start and end frames | No T-pose, snap, clipping, wrong body component, or truncated blend |
| Root-motion route | Final transform and facing match the design without collision/navmesh escape |
| Workspot entry from several directions | Navigation/teleport policy, local transform, facing, and clearance are coherent |
| Branch bypasses the event | No animation, look-at, camera, or workspot state leaks from an unentered branch |
| Interrupt during event/workspot | Actor, AI tier, camera, look-at, and graph route recover deliberately |
| Return after interruption | Beat resumes or restarts exactly as specified; no duplicate side effect |
| Save/reload during the beat, if permitted | No stuck pose, missing actor, duplicate event, or false Success |
| Stream away and return | Community actor and scene workspot reacquire without duplicate ownership |
| Named scene exit | Camera/look-at/AI/workspot state is released before the quest cleans up the actor |
| Completed-save reload and mod removal | No replay or retained actor ownership; removal is tested only on a disposable save |

If the game forbids saving during a cinematic state, record that limitation
and test the nearest checkpoint. New animation playback, root motion,
workspot entry, camera behavior, interruption, return, reload, and cleanup
remain **Experimental** until the exact route passes.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Event runs but actor does not move | Performer mapping, actor-visible set slot, animation name, component/mask, and asset compatibility |
| T-pose or severe deformation | Rig/body/perspective mismatch, wrong animation set, missing linked channels |
| Animation is clipped | Event start/duration, section duration, blend-out, and following transition |
| Actor snaps or ends in the wrong place | Root-motion enabled/mode, origin marker, offset, scene marker, and collision |
| Look-at persists after the line | Missing stop/replacement request or untested interruption/exit cleanup |
| Camera remains constrained | Reset flags/events, player-camera ownership, named exit, and interruption path |
| Actor never enters workspot | Actor target, data-to-instance join, instance transform, entry params, navigation, streaming |
| `Work Started` fires but scene stalls | Wrong output consumed, Success semantics, infinite/finite params, or missing wrapper mapping |
| Workspot works once but fails after reload | Saved scene/community/workspot state, retained actor role, stale instance identity |
| Actor disappears at scene exit | Community cleanup/deactivation raced animation/workspot release |

## Evidence boundary and depot anchors

**Observed in vanilla:** the focused fields and paths in this guide were
inspected in installed Cyberpunk `2.31a` resources:

- `base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene`
- `base\animations\quest\minor_quests\mq007\anim\body\mq007__talking_gun__male_fpp.anims`
- `base\quest\minor_quests\mq010\scenes\mq010_02_barry_talk.scene`
- `base\workspots\common\wall\generic__stand_wall_lean_left__stand_around__01.workspot`

These are citations. Extract focused references from your own installation;
do not publish the vanilla CR2W resources or full serialized exports.

**Structurally validated:** Lab 5 verifies that the v5 scene retains typed
empty animation/workspot collections and its scene-local PuppetAI wrapper
through WolvenKit `8.19.0`. It contains no custom cinematic animation or
scene-local workspot route.

**Runtime-proven:** no evidence record in this book proves a new mod-owned
cinematic animation or scene-local workspot under the pinned stack. The legacy
meeting hashes prove scene acquisition and one diagnostic lipsync route, not
animation quality.

**Experimental:** every new animation asset assignment, event combination,
root-motion route, scene-local workspot, camera/look-at sequence,
interruption/return policy, reload, and cleanup behavior is experimental until
its own hash-bound acceptance record passes.

Previous: [External VO, WEM, and
lipsync](external-vo-wem-and-lipsync.md). Back to: [Scenes](index.md).
