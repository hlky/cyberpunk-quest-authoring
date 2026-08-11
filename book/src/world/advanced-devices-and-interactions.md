# Advanced devices, interactions, and persistent state

A quest-controlled device is a collaboration among a placed world entity, an
entity template, bound controller data, quest logic, and save state. No single
resource owns the whole interaction. This chapter turns that split into an
authoring and test contract for computers, access points, doors, drop points,
and other controller-backed world objects.

The outcome is an inspectable, mod-owned device experiment in which you can
name:

- the resource that places the device;
- the component and controller data that make the interaction available;
- the NodeRef and controller class used by quest logic;
- the signal that proves success, failure, or cancellation;
- the final state expected after completion, reload, and removal.

This is an advanced research workflow, not a universal device template. The
current labs do not supply a custom device checkpoint, and a new device remains
**Experimental** until its own clean-save matrix passes.

## Vanilla references

These focused base-game resources are useful comparisons. Extract them from
your own installation; they are references, not files to copy into the project.

```text
base\worlds\03_night_city\_compiled\default\exterior_19_-8_0_0.streamingsector
base\worlds\03_night_city\_compiled\default\4fd0915183681e53.streamingsector_inplace
base\gameplay\devices\masters\computers\laptop_1.ent
base\worlds\03_night_city\_compiled\default\03_night_city.devices
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
```

## The ownership chain

Treat the device as a chain of owners rather than one object:

```text
streaming block and sector
  -> worldEntityNode or worldDeviceNode
     -> full NodeRef + placement
     -> entityTemplate (.ent)
        -> controller / scanner / interaction components
        -> slots and workspots
     -> optional node-local entEntityInstanceData
        -> RedPackage controller/component chunks

questphase
  -> prefab dependency and local/absolute NodeRef context
  -> optional quest-issued controller action
  -> player-driven interaction or engine event
  -> controller condition, fact, or journal signal
  -> explicit outcome and owner-specific final state

save
  -> facts, journal, active graph, and device persistent state
```

| Owner | What it decides | What it cannot prove alone |
| --- | --- | --- |
| Streaming sector | Concrete node, transform, registered NodeRef, and node-local instance data | That the interaction is reachable or the quest can resolve it |
| Entity template | Components, controller identities, appearances, slots, and workspots available to the entity | That copied instance data binds or that a particular action string is accepted |
| Node-local `RedPackage` | Instance-specific controller/component state in observed devices | That global registry or save behavior is unnecessary elsewhere |
| `.devices` / `.psrep` family | Context-dependent lookup and persistence data | A universal prerequisite for every Files UI or quest operation |
| Questphase | When to issue a command, what signal to observe, and how to advance | Creation of the entity, prompt, animation, or persistent controller implementation |
| Journal/facts | Player-facing and durable quest outcomes | Automatic device reset or removal |
| Save | Previously materialized graph and persistent state | That the currently installed archive still matches the saved topology |

The owner table is also a failure-isolation map. A visible prop with an empty
Files tab points toward component/package binding. A functioning prompt that
never advances the quest points toward the observation signal. Behavior that
changes only on an old save points toward persistent identity.

## Three joins must agree

### World identity join

The sector registers the concrete full NodeRef. A phase may address a local
child only when its quest-prefab dependencies establish the surrounding
namespace. Copying the final `#name` without the owner chain does not recreate
the identity.

The retained SQ021 laptop uses the full path:

```text
$/03_night_city/se1/#loc_sq021_trailer_park/loc_sq021_trailer_park_gameplay_prefabV4S2BNI/#loc_sq021_trailer_park_devices/#sq021_randy_pc
```

Its phase can use a shorter local device reference because another resource
establishes that context. This is **Observed in vanilla**, not a string
shortening rule for a mod-owned prefab.

### Component-binding join

The SQ021 placement contains node-local controller data with CRUIDs that match
components in `laptop_1.ent`. In the retained comparison, the active computer
controller uses `1131680419258347532` and the scanning component uses
`1131680419258347552`.

The [retained laptop candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
used the template-matched binding and exposed its exact authored file; that
passing result is **Runtime-proven** for the archived
package. An earlier development comparison reported a visible laptop with
empty authored content after those IDs were replaced, but the current ledger
does not bind that negative control to a separate retained archive. Treat the
causal mismatch interpretation as **Experimental**, and prove it with paired
candidates before relying on it. Do not copy SQ021's IDs into a different
template and call it a reusable recipe.

Keep the separate inplace link separate as well. The laptop placement's
`CookedPrefabData` points at the cited `.streamingsector_inplace`, while its
controller chunks live in node-local `instanceData`. Extracting one does not
substitute for inspecting the other.

### Quest/controller join

The quest payload must agree with the controller actually bound to the placed
entity. Two native shapes cover the common command/observation split:

| Purpose | Native shape | Decisive fields |
| --- | --- | --- |
| Issue a quest-owned command | `questInteractiveObjectManagerNodeDefinition` -> `questDeviceManager_NodeType` -> `questDeviceManager_NodeTypeParams` | `objectRef`, `slotName`, `entityRef`, `deviceControllerClass`, `deviceAction`, `actionProperties` |
| Observe controller state | `questPauseConditionNodeDefinition` -> `questObjectCondition` -> `questDevice_ConditionType` | `objectRef`, `deviceControllerClass`, `deviceConditionFunction`, `functionParameters` |

WolvenKit's generated types and focused serialized resources establish those
field names as **Structurally validated**. They do not establish a public list
of portable action or function strings.

## Commands and observations are different edges

Use a manager node only when the quest owns the command. If the requirement is
"the player uses the device," let the asset expose its prompt and wait on the
resulting controller state, fact, or journal signal.

```text
quest-driven route
  configure or force exact controller action
  -> observe authoritative resulting state
  -> record outcome

player-driven route
  make asset eligible, if required
  -> player selects asset-owned prompt
  -> observe authoritative result
  -> record outcome
```

Sending the completion action immediately before waiting for it can satisfy
the graph without player input. Conversely, waiting on a plausible function
name does not create an interaction the template never exposed.

**Observed in vanilla:** the cited Q108 phase sends `ForceDisabled` to
`#q108_dvc_door_to_soulkiller` and `ForceCloseImmediate` to
`#q108_dvc_door_to_mainframe_interior`, both with `DoorControllerPS`. The same
resource establishes only those exact bindings in that quest context. A
generic `ForceOpen`, lock, restore, or obstruction policy remains
**Experimental** for a newly chosen door.

Another focused vanilla comparison in
`base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase`
waits on `DoorControllerPS.IsOpen` for `#nid_03_dvc_hwangbo_room_door`. This
is **Observed in vanilla** evidence for an action/condition separation, not a
promise that every door reports that function identically across reload,
obstruction, or streaming.

## Interaction result ownership

Choose a completion signal produced by the interaction itself:

| Interaction family | Candidate authoritative signal | Boundary |
| --- | --- | --- |
| Journal-backed computer file | The exact `gameJournalFile.questInfo.factName` written when that file opens | Proves that configured file signal only, not that the player read every line or visited another tab |
| Personal-link action | Evidence-matched controller function such as the tested `ScriptableDeviceComponentPS.IsPersonalLinkConnected`, followed by the authored operation and disconnect | The tested route proves its exact package; success, cancel, and disconnect are separate states |
| Quest-forced door state | Evidence-matched controller condition or a downstream traversal fact/trigger | Issuing the manager command is not proof that collision, navigation, or companions traversed safely |
| Drop point | Engine-owned deposit fact after the exact reservation event and item handoff | A reservation request is not proof of item removal or kiosk accessibility |
| Generic prompt | Controller state, explicit quest fact, journal signal, or later world condition bound to that prompt | Prompt visibility or animation start is not completion |

The SQ021 file route demonstrates the first row. Its controller supplies the
Files content; the file owns `sq021_randy_pc_file_cartoon`; the phase waits for
that fact, coordinates its UI/scene response, then clears the transient signal.
The scene does not create the file. The quest does not infer a click from the
laptop being open.

## Model cancellation explicitly

"Cancel the interaction" can describe several unrelated events:

| Event | Possible owner | Required design decision |
| --- | --- | --- |
| Player closes a device UI | Device/UI controller | Is the operation retriable, and which state proves the UI actually closed? |
| Player breaks a personal-link interaction | Device/workspot/controller | Is a disconnect action required, and are items or facts unchanged? |
| Quest branch becomes irrelevant | Quest graph | Is the waiting signal made harmless, or does a separately tested cut target it? |
| Scene using the same entity interrupts | Scene plus quest wrapper | Which named interruption/return outcome retains or releases the device? |
| Device streams out | World streaming plus persistent controller | Does the interaction resume, fail, or require the player to approach again? |
| Quest completes or is removed | Root lifecycle and save | Should the controller preserve its final state, restore a baseline, or be left to its native owner? |

There is no generic device-cancel node established by the current evidence.
Do not treat a phase output, logical XOR, UI close, or `CutDestination` as an
automatic controller rollback. Record the cancellation discriminator before
any irreversible inventory or journal write, then route retry and terminal
failure separately.

The exact [retained route](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
waited for a personal-link connection, performed
its timed presentation, sent `QuestForceDisconnectPersonalLink`, consumed its
item, and completed. That **Runtime-proven** route does not establish what an
early disconnect, interrupted workspot, reload during connection, or a
different controller should do.

## Persistent state is part of the public identity

A device NodeRef can key state that survives archive replacement. A retained
development investigation reported that a save which had already streamed an
earlier laptop package continued to expose old content after the authored
arrays changed. That observation is **Runtime-proven** only for that saved
identity/package history; it is not hash-bound evidence for the new experiment.
Repacking under the same identity was not a clean comparison.

Treat these as independent saved surfaces:

- the active questphase node and checkpoint;
- facts written by device content or quest logic;
- journal file/message state and visited state;
- device controller persistent state;
- active UI, scene, or workspot state where the game permits saving;
- the world identity that associates the save with the placed device.

Use a new mod-owned NodeRef when materially changing the controller/package
shape during research, or load a save that never streamed the old identity.
Do not combine old and new identities in one positive acceptance run. Resetting
one fact does not clear the other surfaces.

Do not add a `.devices` or `.psrep` contribution by superstition. The SQ021
laptop's searched identity was absent from the cited global `.devices`
resource, yet its Files UI came from node-local instance data. Other
quest-manager lookups can have different requirements. Begin from a focused
native comparison for the same controller and operation, then add the smallest
resource whose absence your experiment actually demonstrates.

## Author the experiment in WolvenKit

Use a new mod-owned identity and keep the first candidate deliberately small:

1. Create or copy a mod-owned WolvenKit project; do not edit an installed lab
   or a base-game resource in place.
2. Extract the exact vanilla comparison from your own game and record its
   sector, node type, entity-template path, full NodeRef, transform, and
   `instanceData` presence.
3. Inspect the entity template's controller, scanner, interaction, slot, and
   workspot components. Record their names and CRUIDs before editing the
   placement package.
4. Add the mod-owned sector node, placement, and full NodeRef. Verify that the
   quest-prefab root and every local child reference resolve to that identity.
5. Author only the controller/component chunks required by the comparison.
   Preserve deliberate template bindings; remove copied quest content and
   scanner clues that your experiment does not own.
6. Add `.devices` or other persistence resources only when the exact native
   comparison or a controlled missing-resource test requires them.
7. In the questphase, activate presentation first. Add a manager action only
   if the quest owns the command; otherwise proceed directly to the player
   interaction and observation gate.
8. Build the condition with the concrete `questDevice_ConditionType`, exact
   controller class, exact NodeRef context, function, and parameters. A fact or
   journal signal can replace the controller condition when it is the native
   content's authoritative result.
9. Route success, retryable cancellation, and terminal failure before adding
   item removal, journal completion, or a durable completion fact.
10. Define the final controller state for normal completion, interruption,
    failure, reload, stream return, and archive removal. Do not invent a
    restore action merely to make the graph symmetrical.
11. Save, close, reopen, and serialize the resources. Inspect concrete types,
    non-null handles, component IDs, NodeRefs, controller `CName` values,
    function/action arrays, sockets, and all world registration paths.
12. Cook and pack only mod-owned files. Extract the finished archive and
    compare its payload inventory and hashes with the candidate you intend to
    test.

The supplied labs remain useful ownership references, but none is a custom
device download. The manual experiment above remains **Experimental** until
the complete matrix below is retained for its exact archive.

## Clean-save and lifecycle matrix

Start the identity/topology campaign from a save created before the device was
ever installed or streamed. Record the archive SHA-256, project commit, exact
save, versions, route, controller state, quest/journal state, and logs for every
case.

| Case | Required observation |
| --- | --- |
| Fresh approach | Entity appears once; prompt, workspot, slots, and navigation are usable at the final transform |
| Normal success | Player-driven input is required when promised; authoritative signal occurs once; inventory/journal/facts advance in the authored order |
| Cancel before commitment | No success fact, item consumption, or objective success; UI/workspot/controller releases; retry remains possible |
| Interrupt during operation | The authored failure, return, or retry policy occurs without duplicate effects or a stuck player/actor |
| Reload before interaction | Prompt and objective restore without auto-completing |
| Reload during a supported interaction state | Controller, UI/workspot, and quest state recover according to the recorded policy; if saving is unavailable, record that limitation |
| Reload after success | Final state and progression remain coherent; the action does not replay |
| Stream away and return | Device resolves once and preserves or re-evaluates exactly the state the design claims |
| Repeated use | One-shot content cannot duplicate a reward or item mutation; repeatable content follows its explicit reset policy |
| Old-save negative control | Previously streamed identity is kept out of positive evidence or is documented as intentionally migrated |
| Removal isolation | Removing the archive from a copied save does not support claims about reset; record lingering save-backed state separately |
| Second untouched save | The exact candidate and route reproduce without inherited controller, fact, journal, or graph history |

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Device appears but authored content is absent | Entity-template component names/CRUIDs and node-local `RedPackage` binding |
| Prompt is absent | Interaction component/TweakDB setup, workspot and slot ownership, controller eligibility, placement clearance |
| Quest command does nothing | `objectRef` context, controller class, action name/properties, prefab dependency, and evidence for registry lookup |
| Player can interact but objective never advances | Whether the condition/fact belongs to that exact interaction result and whether the signal was already true |
| Objective advances without input | A quest-issued action performed the promised player operation or an old save retained the completion state |
| Cancel consumes the item or writes success | Commitment writes occur before the authoritative result or cancel and success converge too early |
| Door moves but traversal fails | Collision, navigation, obstruction, companions, and the concrete final controller state |
| Old content returns after repacking | Reused NodeRef and save-backed controller state; use an untouched save or fresh experimental identity |
| Added `.devices`/`.psrep` changes nothing | The failed behavior may not consume that resource; return to the exact native owner chain |

Previous: [Devices and persistence](devices-and-persistence.md). Next:
[Location research](location-research.md).
