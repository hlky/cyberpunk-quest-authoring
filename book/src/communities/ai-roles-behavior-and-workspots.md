# AI roles, behavior, and workspots

This chapter composes advanced character behavior without pretending that one
AI node owns the actor. Its practical outcome is an explicit ownership
timeline from community spawn, through gameplay AI and a temporary role or
workspot, into scene or cleanup handoff.

The key distinction is:

```text
character record supplies baseline capabilities and reactions
community supplies the actor instance and ambient phase
Puppet AI Manager selects an active AI tier
AI command assigns a temporary high-level role
world path or workspot supplies a destination/activity
quest conditions observe the required result
scene or cleanup becomes the next lifecycle owner
```

A role is not navigation, a workspot is not a character record, and the output
of a command is not proof that the actor reached the destination.

## Prerequisites and tested baseline

Read [Character records, entities, and appearances](character-records-entities-and-appearances.md),
[Activation, readiness, and acquisition](activation-readiness-and-acquisition.md),
[Cleanup and character safety](cleanup-and-character-safety.md), and [Signal
flow](../gates/signal-flow.md) first.

The practical inspection and authoring boundary uses Cyberpunk 2077 Windows
GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and
redscript `0.5.31`. If baseline character behavior is changed through a new
record, the tested chapter-specific loader is TweakXL `1.11.3`.

Use a clean save made before community activation whenever you change the
actor reference, AI tier, role subtype, path/workspot reference, community
phase, record behavior, or cleanup topology.

## Five behavior owners

| Owner | What it contributes | What it does not prove |
| --- | --- | --- |
| `Character.*` TweakDB record | Reaction preset, faction/attitude, action map, archetype, abilities, equipment, stats, loot, and other gameplay defaults | A spawned instance, a route, or quest ownership |
| Community entry and phase | Actor instance, requested appearance, schedule/quantity, and ambient AI-spot assignment | Gameplay-tier readiness or scene acquisition |
| `questPuppetAIManagerNodeDefinition` | Requested story/AI tier for one or more entity references | That the actor spawned, navigated, or finished a role |
| `questMiscAICommandNode` and typed params | A high-level scripted command such as assigning or clearing a role | Navmesh, path existence, arrival, or safe interruption |
| AI spot, spline, or workspot | Placed activity, route reference, animation/behavior resource, and transform | Actor identity, baseline hostility, or durable quest outcome |

Scene acquisition is a sixth, temporary owner. Do not let a gameplay role,
ambient workspot, and scene performance fight for the same actor. Establish a
named handoff edge and verify the actor's state on both sides.

## Entity references select the runtime actor

The focused quest AI nodes use `gameEntityReference` rather than the character
record's `TweakDBID`:

```text
gameEntityReference
  type: EntityRef
  reference: <community or actor NodeRef>
  names[]: <optional community entry CName values>
  dynamicEntityUniqueName
  sceneActorContextName
  slotName
```

For the vanilla follower comparison, the command target is
`reference: #kab_02_com_chester` plus `names: [chester]`; the follower role's
target is a separate reference, `#player`. The first selects the actor receiving
the role. The second selects whom that actor follows.

The reference and names array form one typed selector. An empty `names` list
can be correct for a direct actor NodeRef, while a community reference can need
the exact entry name. Do not add, remove, or reorder names based on a graph
caption. Compare the full focused node and confirm the intended multiplicity.

## Promote the actor before issuing gameplay commands

The observed `sq031` shape is compact:

```text
questPuppetAIManagerNodeDefinition
  entries[]
    questPuppetAIManagerNodeDefinitionEntry
      entityReference.reference: #rogue
      aiTier: Gameplay
```

The retained escort uses the same family before assigning its follower role.
A safe sequence is:

```text
community Activate
  -> wait CharacterSpawned for the intended entry
  -> Puppet AI Manager: Gameplay
  -> assign the role or workspot command
  -> observe actor position/state with separate conditions
```

`Activate` is a spawn request, `CharacterSpawned` is readiness, the AI manager
requests a tier, and the command requests behavior. Keep all four nodes visible
in review. Do not use a delay as a substitute for actor readiness.

Changing tier can affect presentation, scene ownership, and combat behavior.
The page does not prescribe other `gameStoryTier` values. Extract the exact
vanilla context and test any tier transition independently.

## Assign and clear a follower role

The role assignment is carried by the concrete `params` handle:

```text
questMiscAICommandNode
  entityReference: <target community/entry>
  params -> AIAssignRoleCommandParams
    role -> AIFollowerRole
      followerRef.reference: #player
```

The corresponding clear uses:

```text
questMiscAICommandNode
  entityReference: <same target community/entry>
  params -> AIClearRoleCommandParams
```

In the inspected vanilla follower and patrol nodes,
`questMiscAICommandNode.function` still contains
`AIClearRoleCommandParams` even when the concrete `params` handle is
`AIAssignRoleCommandParams`. The WolvenKit class default has the same function
value. Therefore, inspect both fields and treat the concrete handle graph as
decisive evidence for the serialized role payload; do not rename `function`
to an invented value based on the desired action caption.

For a new node, compose the focused native shape in the CR2W editor and reopen
it after saving. Do not copy a whole vanilla phase. Preserve the exact typed
handle nesting, target reference, role subtype, and sockets while replacing
only the identities the new quest owns.

The follower role does not author catch-up teleport, elevators, doors,
restricted nav areas, companion combat policy, or destination completion.
Use actor-position conditions at explicit route gates and keep the role until
the next owner is ready.

## Patrol roles point at a separate path contract

The inspected `sts_wat_nid_03` nodes use:

```text
AIAssignRoleCommandParams
  role -> AIPatrolRole
    pathParams -> AIPatrolPathParameters
      path: <spline NodeRef>
      movementType: Walk
      continuationPolicy: FromNextControlPoint
      startFromClosestPoint: true
      patrolWithWeapon: false
      isBackAndForth: true
      isInfinite: true
      numberOfLoops: 1
      sortPatrolPoints: true
      patrolAction: PatrolActions.DefaultPatrolAction
```

Those values are **Observed in vanilla** for the six inspected assignments.
They are not recommended defaults for every patrol. In particular, an
infinite role and a loop count can coexist in the serialized object; do not
guess which field wins for a new combination.

The `path` is a `NodeRef` to another world-owned resource. It must resolve in
the mounted prefab/sector context, and the route must be navigable for the
selected actor. The role cannot manufacture navmesh or stream the path's
sector. Test one actor and one path before adding squads, alert variants, or
combat.

For finite movement, author an explicit observation or completion policy.
`questCharacterRoleFinished_ConditionType` exposes an actor `objectRef` and an
`AIFiniteRoleType` selector in the current schema, but this repository has no
retained runtime fixture for its exact already-finished, interruption, or
reload behavior. Using it is **Experimental** until reduced and tested.

## Ambient AI spots and quest-driven workspots are different

A community phase can place an actor at a `worldAISpotNode`:

```text
community phase spotNodeRefs
  -> compiled-area spotNodeIds
  -> worldAISpotNode
       spot -> AIActionSpot
         resource -> .workspot
       nodeData -> world transform
```

That is ambient community ownership. It is the right small surface for a
stationary contact that should already be posed before the player arrives.

A quest can also issue a direct workspot command to an existing actor. The
inspected `sq031` node has this focused shape:

```text
questUseWorkspotNodeDefinition
  entityReference.reference: #sq031_com_longue_male_01
  paramsV1 -> questUseWorkspotParamsV1
    function: UseWorkspot
    workspotNode: #sq031_ws_longue_male_01
    movementType: Walk
    teleport: true
    finishAnimation: true
    changeWorkspot: true
    isWorkspotInfinite: true
    repeatCommandOnInterrupt: true
    continueInCombat: false
  outputs: Work Started, Success
  cut: CutDestination
```

That is **Observed in vanilla** for the cited node. It does not prove that
these flags are appropriate together for another actor or that either output
has the completion semantics a new quest expects. An infinite workspot, an
animation-finishing flag, and both `Work Started`/`Success` sockets must be
tested as a complete contract; do not infer arrival or animation completion
from their names alone.

Choose one owner deliberately:

| Desired behavior | Smaller control surface |
| --- | --- |
| Actor spawns already standing/smoking/guarding | Community phase plus placed `worldAISpotNode` |
| Quest orders a spawned actor into a specific placed activity | `questUseWorkspotNodeDefinition` plus separate state observation |
| Actor follows V through ordinary space | Gameplay tier plus `AIFollowerRole` |
| Actor traverses an authored spline | Gameplay tier plus `AIPatrolRole` and path parameters |
| Actor performs a scene | Release or coordinate AI/workspot ownership, then let the scene acquire the performer |

Do not layer all of them on the actor and hope the latest command wins.

## Commands and conditions have separate jobs

The outgoing edge of an AI manager, role node, or workspot node proves graph
progress according to that node's output contract. It does not prove the world
state the objective needs.

Use a separate condition at each acceptance boundary:

- `CharacterSpawned` before the first gameplay command;
- actor-in-trigger or actor-distance checks for route gates;
- a retained role/workspot completion observer only after its exact semantics
  have been tested;
- scene named outputs for performance completion; and
- an outer trigger/distance plus durable progression before deactivation.

`questCharacterWorkspot_ConditionType` exposes `puppetRef`, `isPlayer`,
`spotRef`, `animationName`, and `waitForAnimEnd` in the current schema. The
condition corpus contains four **Observed in vanilla** instances in
`base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase`,
but this page does not have a hash-bound runtime reduction for their enums,
already-true state, interruption, or reload behavior. Treat new completion
gates using it as **Experimental**.

## Handoff and cleanup are part of the role

Write the owner timeline before connecting the graph:

```text
ambient community spot
  -> gameplay AI + temporary role
  -> route gate(s)
  -> next owner ready
  -> clear or replace role
  -> scene / defend / new community phase
  -> durable outcome
  -> safe outer cleanup boundary
  -> Deactivate
```

At a handoff:

1. observe that the actor reached the required boundary;
2. prepare the next owner, including scene/workspot readiness;
3. write any state needed to resume after reload;
4. clear or replace the old role only when the next owner can take over;
5. keep the community active until every scene, AI, combat, and workspot owner
   has released the actor; and
6. deactivate only on the quest's explicit cleanup branch.

The two retained escort archives show why step 4 matters. Clearing at the
third route gate exposed the original community spot as the actor's remaining
owner, so she walked back. Retaining through the defend activity produced the
intended handoff in the later exact artifact.

## Manual WolvenKit composition order

Author one behavior delta at a time in a mod-owned questphase:

1. In a separate comparison project, extract the smallest cited vanilla
   questphase and inspect only the focused node. Record its exact class,
   handle nesting, entity reference, typed params, sockets, and path/workspot
   references. Do not redistribute the extracted phase.
2. In the mod project, confirm the actor's community activation and
   `CharacterSpawned` gate already work on a clean save.
3. Add a `questPuppetAIManagerNodeDefinition`. Add one entry, point its
   `entityReference` at the exact actor/community entry, and select
   `aiTier: Gameplay` for the reduced case.
4. Add a `questMiscAICommandNode`. For follower or patrol assignment, set its
   concrete `params` handle to `AIAssignRoleCommandParams`, add the intended
   role subtype, and populate only the focused fields. Record the separate
   `function` value rather than inferring it from the subtype.
5. For follower behavior, set `followerRef` to the intended target. For patrol,
   set the exact path NodeRef and explicitly review every path parameter.
6. If the activity is a direct workspot instead, add
   `questUseWorkspotNodeDefinition`, populate `entityReference`, add
   `questUseWorkspotParamsV1`, and review all movement, teleport, infinite,
   interruption, combat, and output choices.
7. Add separate actor-state conditions for route or activity acceptance. Keep
   any unproved role-finished/workspot condition **Experimental**.
8. Add the next-owner handoff and a separate role-clear node using
   `AIClearRoleCommandParams` where the design requires it.
9. Route every cut/interruption edge to a branch that releases ownership or
   deliberately preserves the actor. Never leave `CutDestination` semantics
   implicit.
10. Save, close, reopen, and inspect the exact typed handles and sockets. Pack
    the archive, record its SHA-256, and confirm no extracted vanilla resource
    entered the package.

WolvenKit serialization and archive packing are **Structurally validated**
checks. Only the installed hash and clean-save observations can become
**Runtime-proven**.

## Clean-save acceptance matrix

| Start | Action | Required observation |
| --- | --- | --- |
| Clean pre-activation save | Activate, wait readiness, apply Gameplay tier | One intended actor is ready before the behavior command; no duplicate or early command |
| Same baseline clone | Assign follower role in ordinary walkable space | Actor follows the intended target and actor-position gates, not player-position gates, open in order |
| Same baseline clone | Run the patrol/workspot route | Exact path/spot resolves; movement and animation match every authored parameter |
| Role active | Enter and leave combat or another intended interruption | Authored response occurs; command does not loop, vanish, or deadlock unexpectedly |
| Role active at a supported save point | Save/reload, then continue | One actor and one coherent owner resume; document whether the command must be reissued |
| Actor near a streaming boundary | Stream out and return | Community, path/workspot, tier, and role recover according to the authored policy |
| Final route gate | Transfer to scene, defend, next phase, or cleanup | Old role is retained until the next owner is ready, then cleared exactly once |
| Completed save | Reload and revisit | No stale follower, restarted patrol, duplicate workspot, or reactivated community |

Run every distinct role subtype and every different interruption policy as a
separate evidence case. Record archive hash, starting save, actor record and
entry, reference and names array, AI tier, concrete params/role type, path or
workspot, route, combat state, and the first/last visible behavior.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Command fires but actor does not move | Spawn readiness, Gameplay tier, command target reference/names, concrete params type, navmesh, and streamed path/workspot |
| Wrong member of a community receives the role | `gameEntityReference.reference`, `names[]`, entry spelling, and intended multiplicity |
| Actor follows briefly, then returns to the spawn spot | Role cleared or replaced before the next owner; community ambient spot remained active |
| Patrol starts at an unexpected point | Full path NodeRef, continuation policy, `startFromClosestPoint`, point ordering, and actor spawn position |
| Patrol never completes | `isInfinite`, loop/back-and-forth policy, path validity, and unproved completion observer |
| Actor teleports into or clips through the workspot | `teleport`, movement type, spot transform, workspot resource, clearance, and frame/animation compatibility |
| Actor restarts the activity after combat | `repeatCommandOnInterrupt`, combat policy, durable quest state, and duplicate command path |
| Scene cannot acquire or animate the actor | Active AI role/workspot ownership, scene community reference/entry, actor readiness, and missing handoff |
| Reload produces a different result | Dirty save, saved community/actor state, command reissue policy, stale role, and installed archive hash |
| Node caption says clear while payload assigns | Inspect `params.Data` concrete type and role handle; do not diagnose from `function` or caption alone |

Return to [Communities and characters](index.md).
