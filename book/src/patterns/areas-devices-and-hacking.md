# Areas, devices, and hacking

This cookbook page assembles three systems that are often mistaken for one:
a world area or device must exist and stream, a questphase must address it
through the correct identity, and the player-facing objective and marker must
be managed separately. The graph never creates the trigger volume, interaction
prompt, controller, hack minigame, or drop-point kiosk that it observes.

```text
world ownership                     quest ownership
streaming block                     questQuestPhaseResource
  -> Quest sector                     -> phasePrefabs root
     -> trigger or device              -> objective / mappin state
     -> nodeData placement              -> action or waiting condition
     -> full child NodeRef              -> local child NodeRef
```

Use this page after [Triggers and areas](../world/triggers-and-areas.md),
[Quest prefabs and NodeRefs](../world/quest-prefabs-and-noderefs.md), and
[Devices and persistence](../world/devices-and-persistence.md). It is a
cookbook, not a replacement for those ownership chapters.

## Evidence and tested boundary

The practical target is Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit
`8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`.
The retained legacy runs below used older authoring provenance and do not prove
the complete pinned stack.

A custom plant or delivery item can add TweakXL to the dependency set. The
legacy surrounding metadata records TweakXL `1.11.3`; no TweakXL version is
promoted into this page's pinned practical baseline, so a new custom-record
route remains **Experimental** and must record its own version.

| Label | Bounded source and claim |
| --- | --- |
| **Observed in vanilla** | `q108_06b_tower_mainframe.questphase` exposes trigger and plant-device shapes; the three `sts_wat_lch_01` phases expose device action, upload, scan, and prefab-scope shapes; `sq021_randys_room.questphase` exposes a computer-read fact; `drop_point.ent` exposes distinct interaction and navigation slots. Exact depot paths appear below. |
| **Structurally validated** | Legacy research commit `24d8dd633e4009380931fd6bcc507929832ef613` retains generated reach, leave, device-action/device-condition, item-consumption, drop-point reservation, and scan shapes with handle validation. The reduced plant template was also round-tripped with WolvenKit `8.17.4`. This is serialization evidence, not a reader dependency or a runtime guarantee. |
| **Runtime-proven** | Archive `82C221619EBA15D39D5F82D53B9CCE86AEEB9107AEC15166718143043284B312` advanced into a security trigger that then waited silently below its rooftop route; `8FF1835A73F93B032FC4E1602FA1CC80234779706B085C385EBB7DFB91CE945B` advanced when V entered the corrected trigger; `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` completed its community-acquired meeting route; `B082D157978347A126DAACB0A5404AF298B88E549731609D81D5A569CBA81FDF` advanced through its native access-point hack; `C3F7608385CDA9E4436AF92E5DA23B866D47504BE889058E0527457470BE71AD` completed the exact personal-link plant route described below; `1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC` completed the retained native drop-point deposit route; and `DE2A28EF7F7D8D20B4FADF3B97BD0B96BB420FED8456AC0D57E9987B00ACFB2A` established surviving-actor cleanup after a leave boundary. Each claim is limited to its named archive. |
| **Experimental** | A newly authored generic reach/leave/meeting, arbitrary controller/action/function combination, custom hackable device, plant interaction, or different drop point remains unproved on the pinned stack until its own retained clean-save matrix passes. |

The **Runtime-proven** provenance map is exact: `82C22161...` and
`8FF1835...` are recorded in legacy source commit
`5f0e0d5558c35b0fe58b9dd732d4039c91e9c2eb`;
`87956AFF...` in `68f311c8f2511aeba679b76a68062ef5e446aaa0`;
`B082D157...` and `C3F76083...` in
`6e959d2149e664432eaff3b7d4905e8b1d342f2f`; and `1C669335...` and
`DE2A28EF...` in `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`.
The archive hash binds the observed package; the commit binds the retained
claim and surrounding test notes.

Extract vanilla references from your own installation; do not copy their full
CR2W resources into a project or redistribute their serializations:

```text
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_phase.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_openworld.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
base\gameplay\devices\drop_points\drop_point.ent
```

## Resource and asset checklist

Before opening the quest graph, inventory every owner. A blank cell is not a
default; it is an unresolved design decision.

| Concern | Required owner | Review evidence |
| --- | --- | --- |
| World namespace | Quest-prefab root plus a Quest streaming descriptor | Local root in `phasePrefabs`; matching full root in the descriptor |
| Area | `worldTriggerAreaNode`, `AreaShapeOutline.buffer`, notifier, and `nodeData` | Full child NodeRef, transform, bounds, decoded points, height, and `questTriggerNotifier_Quest` |
| Objective presentation | Journal objective, description, localization, and optional journal mappin | Full typed paths, correct `fileEntryIndex`, and registered localization |
| World marker | Usually a dedicated `worldStaticMarkerNode` in an AlwaysLoaded sector | Full marker NodeRef and world-space navigation endpoint |
| Device | `worldDeviceNode` or evidence-matched entity placement | Entity template, appearance, node-local `instanceData`, controller, components, slots/workspots, and full NodeRef |
| Quest-side device access | Prefab dependency plus action and/or condition | Exact controller class, action `CName`, condition function `CName`, and local target NodeRef |
| Persisted lookup | Only the evidence-required `.devices` or `.psrep` contribution | Exact NodeRef hash, controller class, merge result, and reload behavior |
| Plant item | TweakDB item record and inventory ownership | Item ID, grant/pickup owner, quantity, consumption rule, and save behavior |
| Drop point | Existing live kiosk plus its controller contract | Exact native NodeRef, walkable approach, reservation item, deposit fact, and separate marker endpoint |

`phasePrefabs` declares a namespace dependency; it does not place the sector.
A sector `nodeRefs` row registers an identity; it does not supply a concrete
trigger or device. A visible entity does not prove that its persistent
controller bound correctly. These are **Observed in vanilla** and
**Structurally validated** ownership distinctions, not runtime shortcuts.

## Reach and leave areas

### Story view

```text
activate reach objective and marker
  -> wait for the intended area relation
  -> succeed reach objective and hide marker
  -> activate leave objective
  -> wait for the outer leave relation
  -> succeed leave objective
  -> optional completion fact or cleanup
```

The reach and leave waits must be ordered. If an outside-state condition is
active before the player enters, it can already be true.

### Exact phase payload

The retained player-targeted trigger condition has this focused property
contract:

| Owner | Property | Meaning in the inspected shape |
| --- | --- | --- |
| `questPauseConditionNodeDefinition` | `condition` | Handle to the condition wrapper |
| `questTriggerCondition` | `triggerAreaRef` | Local NodeRef beneath an available quest-prefab root |
| `questTriggerCondition` | `activatorRef` | Empty entity reference in the inspected player form |
| `questTriggerCondition` | `isPlayerActivator` | `1` in the inspected player form |
| `questTriggerCondition` | `type` | `Entered`, `Exited`, `IsInside`, or `IsOutside` |

**Observed in vanilla:** the cited Q108 phase uses a player-targeted
`questTriggerCondition` with an empty `activatorRef`,
`isPlayerActivator: 1`, local `triggerAreaRef`, and `IsInside`.

**Structurally validated:** the legacy generated reach shape uses `Entered`;
the generated leave shape uses `Exited`. Lab 3 instead uses ordered
`IsInside` and `IsOutside` state waits. Both are valid serialized shapes, but
they ask different questions:

| Condition | Use when the story means | Reload boundary |
| --- | --- | --- |
| `Entered` | Cross from outside to inside after activation | Loading already inside may not create a new edge |
| `Exited` | Cross from inside to outside after activation | Starting outside is not a leave event |
| `IsInside` | Proceed whenever the player is currently inside | Already-inside activation and reload require a retained test |
| `IsOutside` | Proceed whenever the player is currently outside | Must be activated only after the intended inside step |

The world-side area still needs an authoritative outline buffer, a quest
notifier, a placement whose vertical band intersects the route, and a full
NodeRef beneath the same root. That bounded failure is **Runtime-proven** for
archive `82C221619EBA15D39D5F82D53B9CCE86AEEB9107AEC15166718143043284B312`:
after its shard stage advanced, the next trigger waited silently with its
volume below the rooftop route. The **Runtime-proven** result for the later
`8FF183...` archive is limited to corrected trigger entry and downstream
activation. Neither hash makes a ten-metre height or either Z offset universal.

### Marker ownership

Activate and clear the journal mappin on explicit graph edges. Do not assume a
trigger or device NodeRef is also a useful marker anchor. A marker intended to
exist before a Quest sector streams normally needs its own AlwaysLoaded owner.
The retained direct-device mappin failure is documented in
[NodeRefs, streaming, and placement](../troubleshooting/noderefs-streaming-placement.md).

**Experimental:** whether a new native device can serve directly as a journal
mappin target must be tested for that exact cross-world identity. A separate
marker is a controlled design, not a universal engine requirement.

## Meeting areas are a lifecycle, not one radius

A contact meeting normally separates broad setup from the final engagement:

```text
request community activation
  -> wait for CharacterSpawned
  -> V enters the broad setup area
  -> optional checkpoint
  -> start scene at a scene marker
  -> the running scene owns any narrower engage/awareness gate
  -> receive a named scene exit
  -> delay cleanup until no scene or AI owner remains
```

| Boundary | Owner | What it may establish |
| --- | --- | --- |
| Streaming/setup | Quest sector, community area, and broad trigger after readiness | The world and contact have time to become available before scene start |
| Readiness | Spawn Manager action plus `CharacterSpawned` condition | The named community entry exists before scene acquisition |
| Engagement | Narrow trigger or interaction owned by the running scene | The player deliberately reaches the presentation point after scene setup |
| Scene origin | `scnWorldMarker` and scene start node | Scene transform and actor acquisition context |
| Cleanup | Named scene exit, later delay/area, and community deactivation | A reviewable lifetime after presentation ends |

**Runtime-proven:** `87956AFF...` completed one community-readiness and
scene-acquisition meeting route. It does not prove universal trigger sizes,
arbitrary actor states, interruption behavior, or the current Lab 5 package.
Use [Activation, readiness, and acquisition](../communities/activation-readiness-and-acquisition.md)
and [Scene entry, exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md)
for the other owners.

## The native device contract

A quest action and a quest condition are consumers of a device that already
exists:

```text
worldDeviceNode
  -> entityTemplate (.ent)
     -> interaction/controller/scanner/workspot components
  -> node-local instanceData RedPackage, when required
  -> stable full NodeRef

questphase
  -> optional questInteractiveObjectManagerNodeDefinition
  -> questPauseConditionNodeDefinition
     -> questObjectCondition
        -> questDevice_ConditionType
```

The structurally validated focused properties are:

| Node or payload | Decisive properties |
| --- | --- |
| `questInteractiveObjectManagerNodeDefinition` | `type: questDeviceManager_NodeType` |
| `questDeviceManager_NodeTypeParams` | `deviceAction`, `deviceControllerClass`, `objectRef`, `actionProperties`, `slotName` |
| `questPauseConditionNodeDefinition` | `condition: questObjectCondition` |
| `questDevice_ConditionType` | `deviceConditionFunction`, `deviceControllerClass`, `functionParameters`, `objectRef` |

Keep four meanings separate:

- **Observed in vanilla:** the entity template and bound instance package own
  available interaction, controller, scanner, slot, and workspot behavior.
- **Structurally validated:** a device-manager node can send one named action,
  and a pause condition can wait on one named controller function.
- **Runtime-proven:** only the exact action/function/device combinations named
  in the evidence table have retained in-game results.
- **Experimental:** substituting a controller class, action, condition
  function, device template, or NodeRef creates a new runtime claim.

### Player-driven versus quest-driven operation

Use a command node only when the quest itself should send an action. If the
player must select a prompt, the graph should normally expose that interaction
through the device asset and wait on its resulting controller state or fact.
Sending the same action before the wait can complete or retrigger the device
without player input.

**Structurally validated:** the retained generated device shape can omit the
action node and connect presentation directly to the device condition.

**Experimental:** that omission does not prove a particular device exposes a
prompt. Prompt availability still belongs to its template, instance package,
TweakDB interaction record, slots/workspots, controller state, and placement.

## Four bounded device recipes

### Interact with a device

Use this smallest topology when one controller function is the completion
signal:

```text
objective Active
  -> optional description and marker Active
  -> optional device-manager action
  -> wait questDevice_ConditionType
  -> objective Succeeded
  -> marker Inactive
  -> optional success fact
```

**Structurally validated:** this is the exact generated research shape. It
does not synthesize the device, controller, prompt, animation, or the state
transition consumed by `deviceConditionFunction`.

### Hack an access point

An access-point recipe has two additional owners: the access-point entity must
provide the personal-link/minigame behavior, and its placement must leave a
usable entry and exit workspot. The quest may enable the device first, but the
player-driven route should wait for the native result rather than fire the
same operation twice.

**Runtime-proven:** archive `B082D157...` advanced through one native
access-point hack before the escort route and then completed end to end. Its
device, controller/action/condition, world placement, and root-owned prefab
scope form one hash-bound result. It does not prove every access point or hack
function.

**Experimental:** a generic access-point tutorial remains incomplete until a
mod-owned device passes approach, connection, minigame, success, cancel,
disconnect, reload, and replay cases on the pinned stack.

### Plant or upload an item

The reduced plant topology is:

| Order | Native node | Required binding |
| ---: | --- | --- |
| 1 | `questJournalNodeDefinition` | Objective `Active` |
| 2 | `questInteractiveObjectManagerNodeDefinition` | Device, controller class, action |
| 3 | `questPauseConditionNodeDefinition` | Same device/controller plus completion function |
| 4 | `questItemManagerNodeDefinition` | Local-player item removal |
| 5 | `questJournalNodeDefinition` | Objective `Succeeded` |
| 6 | `questFactsDBManagerNodeDefinition` | Exact completion fact |

**Observed in vanilla:** comparable plant-item structures occur in
`sts_std_arr_05_openworld.questphase` and the cited Q108 mainframe phase.

**Structurally validated:** the reduced template uses
`questAddRemoveItem_NodeTypeParams` with `nodeType: RemoveAll`, a concrete
item `TweakDBID`, the local-player universal reference, silent removal, and no
notification. Those exact removal choices are fixture properties, not
universal plant semantics.

**Runtime-proven:** `C3F76083...` exposed a laptop's `Steal Data`
personal-link interaction, waited for the connection, displayed a five-second
install overlay, disconnected automatically, consumed the keylogger, cleaned
up its guards, and completed. That richer route proves its exact package and
graph, not the reduced template with arbitrary bindings.

### Deliver to a drop point

A drop point is a live device and a separate navigation target. The retained
delivery shape first proves the selected item is present, then sends a
`ReserveItemToThisDropPoint` event to the kiosk and waits for the engine-owned
deposit fact.

| Event-manager property | Retained value or binding |
| --- | --- |
| `managerName` | `DropPointManager` |
| `componentName` | `controller` |
| `PSClassName` | `DropPointControllerPS` |
| `objectRef` | Exact native drop-point entity reference |
| `event` | `ReserveItemToThisDropPoint` with the item `TweakDBID` |

The reservation event does not create the kiosk, add the item, choose a safe
location, or place a useful quest marker. Inspect
`base\gameplay\devices\drop_points\drop_point.ent`; its `UI_Interaction`,
`poi_mappin`, `roleMappin`, and `main_slot/navQuery` offsets are distinct in
the retained vanilla template.

**Runtime-proven:** `1C669335...` completed the exact Kabuki
`drop_point_009` reservation/deposit route. The device remained the deposit
target while a separate marker used the transformed walkable navigation
endpoint. This does not certify another kiosk's accessibility.

## Author in WolvenKit

The exact editor layout changes between WolvenKit builds, but the native
resource order is stable enough to review deliberately:

1. Start from a mod-owned project and copy the completed Lab 3 or Lab 5
   checkpoint into a new experiment; never edit an installed lab in place.
2. Add the Quest descriptor and mod-owned sector resources. Declare one
   quest-prefab root and register every full child NodeRef under it.
3. For an area, create the trigger node, placement, notifier, and authoritative
   outline. Reopen and decode the outline after saving.
4. For a custom device, select an evidence-matched `.ent`, then author the
   smallest node-local package or registry contribution required by that
   comparison. Do not copy a whole unrelated RedPackage.
5. In the questphase, add the objective and marker state nodes before adding
   the trigger or device condition. Use an action node only if the quest owns
   that action.
6. Bind every local NodeRef to the root that the phase can actually resolve.
   For an external child, follow the parent/child ownership arrangement proved
   by its selected reference rather than duplicating roots by habit.
7. Add explicit success, marker cleanup, inventory mutation, fact, and
   community cleanup edges. Do not treat an activation node's `Out` as proof
   that the player completed the activity.
8. Save, reopen, serialize, and inspect the concrete node classes, non-null
   handles, socket connections, NodeRefs, item IDs, and controller `CName`
   values.
9. Pack only mod-owned resources and ArchiveXL registrations. Extract the
   archive and compare its payload inventory with the intended project.

The Lab 3 and Lab 5 downloads remain the executable references for world and
meeting ownership. This page does not claim that either download contains a
custom device, plant interaction, or drop-point recipe.

## Clean-save acceptance matrix

Use one untouched save made before the candidate existed, then make separate
named child saves. Do not overwrite the only clean control.

| Case | What it distinguishes |
| --- | --- |
| Start outside the area | Premature state-condition or objective activation |
| Cross the boundary normally | Trigger geometry, notifier, activator, and graph order |
| Load before crossing | Restoration before an edge or state change |
| Load already inside while the wait is active | `Entered` versus `IsInside` behavior for this exact graph |
| Leave through two directions and elevations | Outline, height, bounds, and real site geometry |
| Approach the device before and after its sector streams | Visibility versus controller and interaction readiness |
| Cancel or disconnect mid-hack | Controller recovery and objective non-completion |
| Complete once, then reload | Duplicate action, reward, item mutation, and marker prevention |
| Stream away and return | Device, marker, and community reacquisition |
| Reinstall against an old save | Save-backed fact, journal, trigger, and persistent-device contamination |
| Remove the mod and load a disposable copy | Cleanup/isolation only; never risk the sole clean control |

Record the archive hash, every authored CR2W hash, starting save provenance,
player position and Z, selected interaction, result fact, inventory before and
after, journal states, and ArchiveXL/RED4ext/game logs. Promotion from
**Experimental** to **Runtime-proven** belongs to that exact retained package
and matrix.

## Troubleshooting

| Symptom | Inspect first |
| --- | --- |
| Objective appears but area never completes | Trigger notifier, local/full NodeRef chain, activator fields, condition type, outline buffer, and player Z |
| Leave completes immediately | Graph order and an already-true `IsOutside` condition |
| Meeting starts before the contact exists | Community activation, `CharacterSpawned`, broad setup order, and scene acquisition |
| Marker routes to the wrong place | Dedicated marker transform and navigation endpoint; do not assume the trigger/device root is walkable |
| Device renders but has no expected prompt | Entity template, interaction component, controller binding, workspot/slot, instance-package CRUIDs, and initial state |
| Quest cannot find a visible device | Prefab dependency, local/full NodeRef context, controller class, and evidence-required `.devices` registration |
| Hack completes before player input | A quest action was sent before a player-driven condition wait |
| Plant succeeds but item remains | Item `TweakDBID`, local-player reference, remove mode, quantity, and branch actually reached |
| Drop point has no deposit choice | Reservation event, exact item ownership, native kiosk reference, controller class, and deposit fact |
| Old files, prompts, or device state return | Save-backed device identity; use a fresh NodeRef or a pre-stream clean save |
| A packed candidate loads but behaves incorrectly | Treat serialization and runtime validity separately; inspect the producer of the waited state |

Continue with [Items, shards, files, and scans](items-shards-files-and-scans.md)
for inventory and readable-content ownership, and
[Workspots and interactions](workspots-and-interactions.md) for placement and
interaction assets.
