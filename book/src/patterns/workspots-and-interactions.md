# Workspots and interactions

“Workspot” is used around several systems, but those systems do not share one
owner. A placed AI spot can reference a `.workspot` activity for a community
actor. A device entity can carry its own interaction components, workspots,
and slots. A scene can acquire an actor whose AI or workspot state was prepared
elsewhere. The quest graph coordinates these assets; it does not manufacture
them.

```text
community actor activity
  community entry/phase/time
    -> spot NodeRef
       -> worldAISpotNode
          -> AIActionSpot.resource (.workspot)

player/device interaction
  worldDeviceNode or worldEntityNode
    -> entityTemplate (.ent)
       -> interaction components / slots / workspots
    -> controller state or emitted fact
       -> quest wait
```

## Evidence and tested boundary

The practical target is Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit
`8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`.
Legacy archives below do not bind that complete environment.

Custom character or device records can add TweakXL. The retained legacy
metadata names TweakXL `1.11.3`; no new record route on this page is promoted
for that dependency, so record the actual version and keep the route
**Experimental** until its own matrix passes.

| Label | Bounded source and claim |
| --- | --- |
| **Observed in vanilla** | `ma_wbr_jpn_013_claws_com.community` joins three community entries to placed spot NodeRefs; the retained `sts_wat_lch_01_combat.questphase` contains a `questCharacterWorkspot_ConditionType`; `drop_point.ent` exposes interaction and navigation slots; and inspected entity templates show that interaction workspots/components belong to the template rather than a quest graph. |
| **Structurally validated** | Lab 5's exact community registry, compiled area, persistent spot identity, `worldAISpotNode`, and workspot resource reference round-trip under WolvenKit `8.19.0`. Legacy generated world fixtures also round-tripped finite and infinite AI-spot shapes. This validates serialization and joins, not animation, navigation, or interaction behavior. |
| **Runtime-proven** | Archive `2C5179349DBD1AFF5A5A01123F83FF1DC76D8D91E45FE946CEA4DCAF0166BF80` spawned its three configured generic actors and kept them passive with the exact cited cigarette-workspot lineage; it did not retain an observation of animation quality or cleanup. Archive `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` completed one community-acquired meeting route. Archive `C3F7608385CDA9E4436AF92E5DA23B866D47504BE889058E0527457470BE71AD` exposed and completed its exact laptop personal-link interaction at the retained placement. |
| **Experimental** | A generic “use a workspot” quest recipe, arbitrary `.workspot` substitution, sequenced movement, workspot-condition semantics, device prompt construction, door interaction, scene interruption, and workspot/facial-animation quality remain unproved on the pinned stack. |

The **Runtime-proven** provenance map binds `2C517934...` to legacy source
commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`, `87956AFF...` to
`68f311c8f2511aeba679b76a68062ef5e446aaa0`, and `C3F76083...` to
`6e959d2149e664432eaff3b7d4905e8b1d342f2f`. The source notes explicitly
withhold generic workspot-animation and interaction conclusions.

Extract focused comparisons from your own installation:

```text
base\open_world\minor_activities\westbrook\japantown\ma_wbr_jpn_13\community\ma_wbr_jpn_013_claws_com.community
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase
base\gameplay\devices\drop_points\drop_point.ent
base\gameplay\devices\masters\computers\laptop_1.ent
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
base\workspots\common\ground\generic__stand_ground_cigarette__smoke__01.workspot
base\workspots\common\ground\generic__stand_ground__guard__02.workspot
base\workspots\patrolling\guard_stand.workspot
```

The three workspot paths represent separate evidence lineages. Do not swap one
for another while keeping the first archive's **Runtime-proven** label. Refer
to the depot path; do not redistribute the vanilla resource.

## Choose the interaction family

| Player-facing design | Primary asset owner | Quest-side responsibility | Current status |
| --- | --- | --- | --- |
| Stationary contact waits at a pose | Community plus one `worldAISpotNode` and `.workspot` | Activate, wait for spawn, acquire in scene, then clean up | Exact legacy meetings are **Runtime-proven**; a new mapping is **Experimental** |
| Guard or civilian follows a finite spot sequence | Community time period plus multiple AI spots and compatible AI behavior | Activate, observe milestones if needed, stop/clean up | Shapes are **Structurally validated**; general movement behavior is **Experimental** |
| Player uses, plugs into, or hacks a device | Device `.ent`, instance package, controller, interaction/workspot/slot | Enable only if required, wait on a controller function or fact | Exact named legacy routes are **Runtime-proven**; arbitrary combinations are **Experimental** |
| Quest waits until an actor is in a workspot | Character condition targeting the actor | Activate the wait only after the producing AI/workspot route | Condition family is **Observed in vanilla**; no generic recipe is promoted |
| Scene needs an actor at a presentation point | Community/AI preparation plus scene marker and actor acquisition | Wait for readiness, start scene, route named exit | One retained meeting is **Runtime-proven**; scene-local animation quality is separate |

This choice prevents a common category error: adding a
`questCharacterWorkspot_ConditionType` cannot place an actor into a workspot,
and adding a device-manager node cannot create the device's prompt.

## AI workspot ownership

### Registry-side route

The retained community shape is:

```text
communityCommunityTemplateData
  entries[]
    communitySpawnEntry
      characterRecordId
      entryName
      phases[]
        communitySpawnPhase
          phaseName
          appearances[]
          timePeriods[]
            communityPhaseTimePeriod
              hour
              isSequence
              quantity
              spotNodeRefs[]
```

| Property | Owner and meaning in the inspected shape |
| --- | --- |
| `characterRecordId` | Community entry; chooses the character TweakDB record, not the world placement |
| `entryName` | Community-local identity used by activation, conditions, and scene acquisition |
| `phaseName` | Community-local mode selected by initial state or Spawn Manager operations |
| `spotNodeRefs` | Full or context-valid references to placed AI spots |
| `isSequence` | Period-level sequence flag in the retained shape; not a complete movement recipe |
| `quantity` | Requested actors for that period; not a readiness or scene-performer count |

`entryActiveOnStart` belongs to registry initial state. For a controlled quest
contact, starting inactive and using an explicit activation edge makes the
lifecycle reviewable. That is a design used by the current lab, not a
universal vanilla requirement.

### Compiled-area mirror

The compiled community area repeats the identity route rather than the
character record:

| Registry value | Compiled-area value |
| --- | --- |
| `communitySpawnEntry.entryName` | `communityCommunityEntrySpotsData.entryName` |
| `communitySpawnPhase.phaseName` | `communityCommunityEntryPhaseSpotsData.entryPhaseName` |
| `communityPhaseTimePeriod.hour` | `communityCommunityEntryPhaseTimePeriodData.periodName` |
| `communityPhaseTimePeriod.isSequence` | `communityCommunityEntryPhaseTimePeriodData.isSequence` |
| `communityPhaseTimePeriod.spotNodeRefs` | `communityCommunityEntryPhaseTimePeriodData.spotNodeIds` |

The registry, compiled area, sector `nodeRefs`, node placement, and persistent
spot data must identify the same route. In the compact lab shape,
`workspotsPersistentData[].globalNodeId` also joins the registry to the placed
spot's world-global identity.

**Structurally validated:** these exact joins are checked for Lab 5. A stale
area mirror can still serialize while leaving the actor unable to acquire the
intended spot; successful joins remain a runtime question.

### The placed AI spot

The world node owns placement and the activity reference:

```text
worldAISpotNode
  isWorkspotInfinite
  isWorkspotStatic
  lookAtTarget
  spot -> AIActionSpot
    resource -> ResourcePath to .workspot
    snapToGround
    useClippingSpace
```

Its matching `nodeData` owns position, orientation, scale, bounds,
`NodeIndex`, and full `QuestPrefabRefHash`. The workspot resource does not
choose the actor or world transform.

| Concern | Correct owner |
| --- | --- |
| Actor selection and appearance | Community entry and character/entity/appearance chain |
| Activity or animation setup | Referenced `.workspot` resource |
| Position and facing | AI spot `nodeData` transform |
| Quest-prefab identity | Full/local NodeRef chain and placement hash |
| Continuing versus finite use | `isWorkspotInfinite` plus the community-period design |
| Ordered route | Multiple unique spots, mirrored order, `isSequence`, compatible AI, and navigable placement |
| Readiness | Spawn Manager request followed by the matching character/spawning condition |

**Runtime-proven:** `2C517934...` establishes that its exact three generic
entries spawned and stayed passive. It does not establish cigarette animation
quality. The later guard-standing and patrol workspot references belong to
different source/runtime lineages and cannot be merged into that hash-bound
claim.

## Device interaction assets

Device interaction does not normally use a community `worldAISpotNode`.
Instead, the placed entity points to a template whose component hierarchy can
own interaction components, personal-link workspots, controllers, scanner
components, and slots:

```text
worldDeviceNode or worldEntityNode
  entityTemplate -> device.ent
  instanceData -> optional RedPackage overrides
  nodeData -> world transform and full identity

device.ent
  components
  workspots / interaction definitions
  attachment and navigation slots
```

**Observed in vanilla:** `drop_point.ent` has different local transforms for
`UI_Interaction`, `poi_mappin`, `roleMappin`, and `main_slot/navQuery`.
Selecting the kiosk root for an icon, interaction, and GPS endpoint therefore
produces different world-space results from selecting the appropriate slot.

**Observed in vanilla:** SQ021's laptop binds node-local persistent controller
data to `laptop_1.ent` through matching component CRUIDs. This establishes the
join, not mismatch behavior or permission to copy SQ021's package. The runtime
behavior of a custom package whose component IDs do not match remains
**Experimental**.

### Placement is part of the interaction

Check the actor/player entry pose, exit pose, facing, clearance, collision,
ground contact, and navigation approach at the final transformed placement.
Rotating an entity can rotate an interaction workspot away from the available
floor even when the visible prop looks acceptable.

The **Runtime-proven** result for the final `C3F76083...` package is limited to
exposing `Steal Data` and completing the personal-link route at its exact
barrel placement. It does not isolate placement from controller/action content
or prove another transform.

## Doors are device contracts

A world door is not an abstract graph gate. The placed door entity, its
controller/persistent-state class, NodeRef, interaction setup, animation and
collision, and surrounding navigation must already agree before a quest node
can operate or observe it.

Keep world doors separate from vehicle doors. A vehicle trunk or seat door can
use `questToggleDoor_NodeType` with vehicle-specific identity and door-slot
fields; that is not the same contract as sending an action to a placed world
device.

**Observed in vanilla:** the cited Q108 phase contains
`questDeviceManager_NodeTypeParams` bound to `DoorControllerPS` and exact door
NodeRefs. Focused operations include `ForceDisabled` for
`#q108_dvc_door_to_soulkiller` and `ForceCloseImmediate` for
`#q108_dvc_door_to_mainframe_interior`. Those names and actions belong to those
doors in that quest. They establish the native manager/controller shape, not a
portable list of actions for every door template.

A bounded quest-driven world-door sequence is:

```text
prove the placed door and controller resolve
  -> optional objective/presentation Active
  -> questInteractiveObjectManagerNodeDefinition
       questDeviceManager_NodeType
       exact objectRef + DoorControllerPS + evidence-matched deviceAction
  -> observe an authoritative controller condition or downstream fact
  -> advance presentation
  -> restore or preserve the intended final door state on every exit
```

Before authoring, answer:

| Boundary | Required decision |
| --- | --- |
| Door asset | Which `.ent`, instance data, components, controller class, and persistent identity own the door? |
| Quest command | Is the quest supposed to force a state, or must the player use an asset-owned prompt? |
| Completion | Which exact controller function, fact, trigger, or later event proves the promised result? |
| Traversal | What happens to collision, navigation, companions, combatants, and the player if the action fails or the door closes? |
| Lifecycle | Should interruption, failure, reload, stream return, and completion restore, preserve, or re-evaluate the state? |

**Experimental:** this book has no retained generic mod-owned door candidate.
Do not infer that `ForceOpen`, `ForceCloseImmediate`, `QuestLockAll`, or another
string works on a newly chosen controller just because the name occurs in a
vanilla phase. Extract an evidence-matched door route, inspect its entity and
controller context, then test wrong-side approach, repeated use, obstruction,
companion traversal, combat, save/load on both sides, interruption, stream
return, completion, and removal isolation with a fresh persistent identity.

## Quest-side coordination

For a passive contact, keep the order explicit:

```text
community Activate
  -> wait CharacterSpawned for the named entry
  -> wait approach or interaction boundary
  -> scene acquires the same community/entry
  -> named exit advances the quest
  -> delay cleanup past every active owner
  -> community Deactivate
```

For a player-driven device interaction:

```text
objective Active
  -> optional quest command that merely enables/configures the device
  -> player uses the asset-owned interaction
  -> wait controller function or explicit fact
  -> objective Succeeded
  -> cleanup / item mutation / completion fact
```

Do not route a quest-issued action that performs the interaction if player
input is the acceptance requirement. See
[Areas, devices, and hacking](areas-devices-and-hacking.md) for the exact
device-manager and condition payloads.

### Workspot conditions are observers

**Observed in vanilla:** the retained condition corpus contains four
`questCharacterWorkspot_ConditionType` payloads beneath
`questCharacterCondition`, including a focused example in
`sts_wat_lch_01_combat.questphase`.

**Experimental:** this page does not prescribe the payload's runtime enums,
actor-reference form, transition behavior, already-true behavior, or reload
semantics. Extract the exact comparison, record every decisive field, identify
the AI or scene that produces the workspot state, and reduce it into a
mod-owned fixture before using it as a completion gate.

## Author a community workspot in WolvenKit

1. Start from a copy of the Lab 5 project. Give the new quest-prefab root,
   community, entry, phase, period, and spot unique mod-owned identities.
2. Select one `.workspot` path from an evidence-matched vanilla comparison.
   Inspect it, but reference the depot asset rather than extracting and
   redistributing it.
3. Add a `worldAISpotNode` to the Quest sector. Set `spot` to an
   `AIActionSpot`, bind its `resource`, and choose finite/infinite and static
   fields deliberately.
4. Add the matching `nodeData` placement and full child NodeRef. Confirm the
   transform leaves clearance and the facing matches the intended player
   approach.
5. Add the spot to the sector's `nodeRefs` and to the compact registry's
   persistent spot data with the same world-global identity.
6. Bind the registry entry's `spotNodeRefs`, then mirror entry, phase, period,
   order, and spot IDs in the compiled community area.
7. Keep the entry inactive until the quest requests it unless a known-good
   comparison requires another lifecycle. Add a `CharacterSpawned` readiness
   wait before a scene or interaction tries to acquire the actor.
8. Save and reopen every CR2W. Serialize and inspect all handles, NodeRefs,
   global IDs, character records, appearance names, period names, and workspot
   resource references.
9. Pack and extract the project, then compare payloads and ArchiveXL
   registrations before entering the game.

## Author a device interaction in WolvenKit

1. Inspect the exact device `.ent`: controller, scanner, interaction
   components, component IDs, workspots, and relevant slots.
2. Place a mod-owned `worldDeviceNode` or evidence-matched entity node with a
   stable full NodeRef and a transform that leaves the interaction path clear.
3. Add the smallest node-local instance package needed for content or state.
   Preserve template-matched component identities; do not paste an unrelated
   RedPackage.
4. Add a sparse `.devices` contribution only when controller lookup evidence
   requires it. Add `.psrep` only when a persistence test establishes that
   requirement.
5. In the questphase, expose or enable the device without prematurely
   performing the player action. Wait on the exact controller function or fact
   the interaction produces.
6. Keep a separate marker at a verified HUD/navigation transform if the entity
   root or interaction slot is not a useful route endpoint.
7. Reopen, serialize, pack, and inspect the complete template/package/NodeRef/
   controller chain before runtime testing.

The Lab 5 download is the executable community/AI-spot reference. It does not
contain a general player-interaction workspot or custom device recipe.

## Clean-save acceptance matrix

| Case | What it distinguishes |
| --- | --- |
| Approach from outside streaming range | Sector, community area, spot, and device availability |
| Activate the community once | Entry/phase/period selection and intended spot acquisition |
| Load before activation | Clean negative control for active-on-start leakage |
| Load after activation but before interaction | Saved community/workspot or device state |
| Approach from several directions | Clearance, facing, navmesh, collision, and prompt range |
| Interrupt before completion | Actor/device recovery and objective non-completion |
| Complete normally | Producer signal, quest wait, presentation, and cleanup order |
| Enter combat during the activity | AI/workspot interruption policy; only include if the design supports combat |
| Stream away and return | Reacquisition without duplicate actor, stuck spot, or missing prompt |
| Reload after the named scene/device exit | Persistent owner release and duplicate prevention |
| Replay from untouched clean save | One-shot state and deterministic placement |
| Reuse an old device identity after changing its package | Demonstrates save contamination; repeat with a fresh identity |

Record the exact archive/resource hashes, workspot path, actor record,
community/entry/phase/period, spot NodeRef and global ID, transform, device
template and component IDs, starting save provenance, interruption state, and
logs. Do not promote animation quality merely because the actor spawned.

## Troubleshooting

| Symptom | Inspect first |
| --- | --- |
| Actor spawns at the wrong spot | Registry `spotNodeRefs`, area `spotNodeIds`, full NodeRef, global ID, and sector placement |
| Actor clips, floats, or faces away | AI spot transform, workspot assumptions, ground contact, clearance, and navmesh |
| Actor activates but never settles | Workspot resource, finite/infinite fields, phase/period, AI role, and navigation |
| Sequence stalls or skips | Unique spot identities, mirrored order, `isSequence`, compatible AI, and interruption state |
| Scene cannot acquire the actor | Community and entry names, readiness wait, active phase, streaming, and scene actor reference |
| Actor disappears during the scene | Cleanup edge, scene named exit, AI/workspot ownership, and deactivation timing |
| Device is visible but prompt is absent | Exact `.ent`, interaction component, slot/workspot, controller binding, instance data, and initial state |
| Prompt appears from the wrong side | Entity transform, slot/workspot local transform, collision, and approach space |
| Quest waits forever after interaction | Controller function/fact producer, NodeRef context, and whether a quest command replaced player input |
| Removed interaction content returns | Save-backed persistent device identity; use a new NodeRef or a pre-stream save |
| Workspot condition never changes | Producing AI/scene lifecycle, actor reference, exact payload fields, activation order, and streaming |

For community structure, continue with
[Entries, phases, and AI spots](../communities/entries-phases-and-ai-spots.md)
and [Cleanup and character safety](../communities/cleanup-and-character-safety.md).
For device ownership, use
[Devices and persistence](../world/devices-and-persistence.md).
