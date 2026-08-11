# NPC interaction and meetings

A reliable meeting is a handoff between four owners: the quest requests an
actor, the community materializes it, the world supplies a safe approach and
performance location, and the scene acquires the actor for a bounded
performance. A visible NPC is not yet a scene performer, and a completed spawn
command is not proof that the NPC is ready.

This pattern produces the following native route:

```text
activate objective and contact pin
  -> activate community entry or phase
  -> wait for the required actor to spawn
  -> wait for V to enter a broad setup area
  -> launch the scene at its world marker
  -> consume one named scene exit
  -> advance journal and branch state
  -> wait until V leaves the cleanup area
  -> deactivate or transfer the community lifecycle
```

Use [Lab 5: First Contact](../scenes/lab-05.md) as the downloadable,
**Structurally validated** example. This page generalizes its ownership
decisions; it does not turn the example into a universal template.

## Prerequisites

Before opening the questphase in WolvenKit, prepare these explicit resources:

| Owner | Required material |
| --- | --- |
| Quest | Registered root, child phase, objective, description if used, map pin, one-shot state, and every intended scene outcome |
| World | Root-owned quest prefab, community registry node, compiled community area, AI spot, setup and cleanup triggers, scene marker, and map marker |
| Community | One entry/phase join, character record, appearance, quantity, activation policy, and workspot mapping |
| Scene | `scnSceneResource`, community-acquired actor, public entry, named exits, screenplay, events, and localization/audio dependencies |
| Lifecycle | Interruption policy, combat policy, delayed cleanup, completed-save behavior, and removal isolation |

Read [Registries and areas](../communities/registries-and-areas.md),
[Entries, phases, and AI spots](../communities/entries-phases-and-ai-spots.md),
and [Scene resource anatomy](../scenes/resource-anatomy.md) before composing the
route. If any local NodeRef is still ambiguous, resolve the prefab scope first
with [Quest prefabs and NodeRefs](../world/quest-prefabs-and-noderefs.md).

## Vanilla references

These three resources show the activation, readiness, and scene-acquisition
handoffs used by a small vanilla meeting. Extract them into a separate research
project:

```text
base\quest\minor_quests\mq003\mq003_orbitals.questphase
base\quest\minor_quests\mq003\phases\mq003_homeless.questphase
base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene
```

## Four ownership handoffs

```text
questphase requests activation
  -> community resolves entry and phase
  -> world streams area and AI spot
  -> quest waits for named readiness
  -> scene acquires community actor
  -> scene publishes named outcome
  -> quest persists progression
  -> quest releases or transfers actor
```

The arrows are contracts, not implicit engine conversions:

- a Spawn Manager action does not wait for streaming or entity construction;
- `CharacterSpawned` does not prove a scene can resolve a misspelled entry;
- a scene actor definition does not activate its community;
- a scene End node does not create a questphase output with the same meaning;
- a named scene exit does not update journal state or clean up the actor;
- community deactivation does not prove immediate, safe disappearance.

## Activate at the intended scope

The questphase action uses this focused native shape:

```text
questSpawnManagerNodeDefinition
  actions[]
    questSpawnManagerNodeActionEntry
      type -> questCommunityTemplate_NodeType
        action: Activate
        spawnerReference: <community NodeRef>
        communityEntryName: <entry CName or None>
        communityEntryPhaseName: <phase CName or None>
```

Choose one scope deliberately:

| Scope | Entry/phase values | Appropriate use |
| --- | --- | --- |
| Whole community | `None` / `None` | The quest owns every configured entry and intends to bring the complete community online |
| Named phase | Exact entry and phase `CName` values | One actor or one authored community phase must change without activating unrelated entries |

`None` is an authored `CName` token in the observed serialized shape. It is
not `null`, an omitted property, or an empty string. The Spawn Manager's `Out`
socket means only that the action was issued.

For a reusable contact, start inactive. An active-on-start entry can hide an
ordering bug by making the actor happen to exist before the quest asks for it.
It also makes clean-save and removal behavior harder to distinguish.

## Wait for the actor you actually need

A one-entry whole-community readiness check can use:

```text
questPauseConditionNodeDefinition
  condition -> questCharacterCondition
    type -> questCharacterSpawned_ConditionType
      objectRef.reference: <community NodeRef>
      comparisonParams
        comparisonType: Greater
        count: 0
        entireCommunity: 1
```

That observed payload asks whether the community-scoped spawned count passes
the comparison. It does not mean every configured actor is ready. For a
meeting with several required performers, narrow the `gameEntityReference`
with exact entry names and wait for each performer before converging through
an explicit all-of join.

Do not substitute another identity domain for `objectRef.reference`:

| Wrong value | Why it is wrong |
| --- | --- |
| Registry node's numeric world identity | Placement identity is not the community NodeRef used by the quest condition |
| Compiled area's `sourceObjectId` | It joins compiled area to template; it is not a text NodeRef |
| AI spot global ID | It identifies the placed spot, not the community source |
| Entry name alone | It narrows an entity reference only when paired with the correct community reference |
| Character `TweakDBID` | It selects character data; it does not identify this spawned community instance |

See [Activation, readiness, and
acquisition](../communities/activation-readiness-and-acquisition.md) for the
complete identity join.

## Give streaming an approach boundary

Actor readiness and world readiness are related but different. Place a broad
setup trigger around the meeting site and wait for the player with:

```text
questPauseConditionNodeDefinition
  condition -> questTriggerCondition
    triggerAreaRef: <setup trigger NodeRef>
    type: IsInside
    isPlayerActivator: 1
    activatorRef: <empty/default entity reference>
```

Use a `worldTriggerAreaNode` whose notifier includes the quest consumer. The
outline buffer, sector placement, bounds, and prefab path all need independent
review; see [Triggers and areas](../world/triggers-and-areas.md).

The setup radius is an authoring decision, not a universal number. It should
be large enough to cover fast travel, vehicle approach, and streaming latency,
but not so large that the scene begins before its intended presentation space
is loaded. Test slow walking, sprinting, a fast vehicle, teleport-based debug
arrival, and stream-away/return.

## Let the scene acquire; do not ask it to spawn

The scene's community-backed performer uses:

```text
scnActorDef
  acquisitionPlan: community
  actorId: <scene-local scnActorId>
  actorName: <debug/authoring name>
  communityParams -> scnCommunityParams
    reference: <same community NodeRef>
    entryName: <same entry CName>
```

The decisive joins are exact:

| Field | Must agree with |
| --- | --- |
| `communityParams.reference` | Spawn action, readiness condition, prefab scope, and mounted community source |
| `communityParams.entryName` | Registry template entry and compiled-area entry mirror |
| `actorId` | Screenplay sections, events, performer mappings, and actor-facing scene nodes |
| `actorName` | Scene debug symbols; it is not the community entry join key |

If the actor is visible but the scene cannot acquire it, compare these joins
before moving the actor or adding delays. More delay cannot repair an identity
mismatch.

## Publish a named quest/scene contract

The questphase launches the archived scene with
`questSceneNodeDefinition`. Its key properties are:

| Property | Contract |
| --- | --- |
| `sceneFile` | Soft depot path to the packed `.scene` resource |
| `sceneLocation` | `scnWorldMarker` whose `nodeRef` resolves beneath the active prefab scope |
| Input socket | Exact public scene entry, such as `start` |
| Output sockets | Exact public scene End names, such as `contact_done`, `accepted`, or `refused` |
| `interruptionOperations` | Explicit interruption policy; an empty array is a bounded design choice, not a default guarantee |
| `CutDestination` | Cut target only after its behavior has its own runtime evidence |

Inside the scene, publish the same names with the Start and End nodes. Do not
invent a generic questphase output called `end`. A scene End node named
`contact_done` must be consumed through a questphase output named
`contact_done`.

For choices, expose one named output per durable story result:

```text
scene: accepted -> questphase: accepted -> set accepted fact -> advance journal
scene: refused  -> questphase: refused  -> set refused fact  -> alternate route
scene: Default INT / Default RET        -> explicit interruption policy
```

Persist the branch result after the scene releases its performer and before
cleanup can erase the world actor. Keep the scene's screenplay choice state,
quest facts, and journal outcome as separate systems; see [Entry, exit, and
quest handoff](../scenes/entry-exit-and-quest-handoff.md).

## Manual WolvenKit authoring order

Work from a copy of a known-good project, with the game closed:

1. Mount the registry, compiled area, AI spot, triggers, and markers under one
   verified quest-prefab scope.
2. Confirm the registry entry and compiled-area mirror use the same entry and
   phase names, and that their world identity joins are correct.
3. Set the contact inactive on start unless the surrounding quest deliberately
   owns an earlier activation.
4. In the child questphase, add objective and mappin activation before the
   Spawn Manager action.
5. Add the named or whole-community `Activate` payload.
6. Add actor-specific readiness waits. Use an explicit all-of join when more
   than one performer is mandatory.
7. Add the broad player `IsInside` setup wait. Add a checkpoint only when the
   save/retry policy has been designed and tested.
8. Add `questSceneNodeDefinition`, its soft scene path, world marker, public
   entry, every named success/refusal output, and interruption outputs.
9. Route each named output through its own durable fact/journal writes before
   convergence.
10. Inactivate the meeting pin, activate any leave objective, and wait for the
    player to be outside a generous cleanup area.
11. Deactivate the community, or explicitly transfer ownership to the next
    escort, combat, or scene phase. Do not do both.
12. Serialize every changed CR2W with WolvenKit `8.19.0`, reopen it, verify
    handles and sockets, pack, extract the archive, and compare the intended
    depot paths before launching the game.

The reader path ends in native resources and WolvenKit. Documentation-author
research inputs are not build or runtime dependencies.

## Transfer ownership instead of cleaning up

Some meetings lead directly into following, combat, or another scene. In that
case, preserve the community and hand off through a durable fact or named
questphase output:

```text
meeting named exit
  -> persist outcome
  -> scene releases actor
  -> next phase assigns gameplay AI or follower role
  -> later owner performs cleanup
```

Do not deactivate and immediately reactivate the same actor between adjacent
activities. That introduces a streaming/materialization race and can restore
the actor at its original AI spot. The next owner must state when it clears a
follower role, restores an AI phase, or deactivates the community.

Unique story characters add another boundary. Do not borrow a story-managed
actor merely because its record has a suitable appearance or voice. Prefer a
quest-owned generic record unless you have proved the borrowed character's
global lifecycle, save compatibility, and other-quest interactions. See
[Cleanup and character safety](../communities/cleanup-and-character-safety.md).

## Save, interruption, and cleanup matrix

Use separate untouched save descendants for stateful cases. Do not repeatedly
overwrite one slot and call the runs independent.

| Case | Required observation |
| --- | --- |
| Slow ordinary approach | One activation, one actor, one scene start, correct named return |
| Fast arrival | Setup wait does not outrun actor or scene-marker streaming |
| Stream away before setup | Return restores one actor and one armed meeting route |
| Save after activation, before readiness | Reload reaches readiness without duplication or deadlock |
| Save after readiness, before scene | Reload either resumes the documented pre-scene state or is explicitly unsupported |
| Every named scene exit | Exactly one durable branch result and correct journal/mappin state |
| Leave during approach | Meeting remains recoverable or follows an authored cancellation result |
| Combat or police intrusion | Actor behavior, scene interruption, and cleanup follow the stated policy |
| Post-scene cleanup | Actor remains until the scene is released and V crosses the cleanup boundary |
| Completed-save reload | Meeting, marker, scene, and community do not reactivate |
| Clean replay | The same installed hash completes from a separate untouched save |
| Removal isolation | Removing the candidate does not leave a save-dependent claim disguised as a clean resource result |

Active-line save/load, scene interruption, and cut behavior need their own
matrix. An ordinary named-exit pass does not promote those claims.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Actor never appears | Registry active-on-start policy, activation scope, entry/phase spelling, area/template identity join, AI spot, sector bounds |
| Spawn action exits but wait never resolves | `objectRef.reference`, entry narrowing, comparison scope, stream coverage |
| Actor is visible but scene stalls | Scene `communityParams.reference` and `entryName`, performer mapping, scene marker, public entry |
| Scene runs but quest does not continue | Scene End name versus questphase output socket and connected edge |
| Actor disappears during dialogue | Premature `Deactivate`, competing phase change, stream bounds, or another owner clearing the actor |
| Actor walks back after dialogue | Follower/gameplay role cleared before the next lifecycle owner takes over |
| Reload uses an older route | Save provenance, active questphase/checkpoint, scene state, installed archive hash, and duplicate archives |
| New archive crashes at scene launch | Scene IDs, actor/lipsync slot mapping, handle topology, scene path, and retained crash evidence before changing world geometry |

For symptom-led isolation, use [Actors, scenes, and
lipsync](../troubleshooting/actors-scenes-lipsync.md) and [Save state and clean
retests](../troubleshooting/save-state-clean-retests.md).
