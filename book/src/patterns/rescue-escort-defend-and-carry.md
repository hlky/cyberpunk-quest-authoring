# Rescue, escort, defend, and carry

Extraction objectives are lifecycle chains, not one “follow NPC” node. A
quest may release a target, transfer it into gameplay AI, observe ordered
movement, preserve it through combat, wait for a carry or trunk state, and
only then clean up. Each transition changes which system owns the actor.

```text
community owns inactive or restrained target
  -> quest/device releases target
  -> quest proves named target readiness
  -> gameplay AI or follower role owns movement
  -> ordered destination gates prove progress
  -> defend/carry/trunk activity owns the next state
  -> durable quest outcome is written
  -> AI role, community, device, marker, and actor cleanup complete
```

Do not deactivate and respawn the actor at every stage boundary. Preserve one
identity and transfer ownership deliberately.

## Prerequisites

Prepare these resources before editing the child phases:

| Owner | Required material |
| --- | --- |
| Target community | Registry, compiled area, named target entry/phase, character record, appearance, AI spot, activation/readiness policy, and long enough streaming bounds |
| Release device | Placed device, controller class, exact action and completion function, device registry entry, interaction/workspot, and fresh persistent identity for materially changed tests |
| Route | Walkable navigation, three or more deliberate destination volumes, route/final markers, bounds, and recovery policy |
| Defend encounter | Protected-target identity, attacker community/waves, hostility targets, survival or completion producer, failure policy, and cleanup |
| Carry/trunk | Carry-capable target state, destination volume, vehicle identity if used, trunk interaction owner, and post-placement cleanup |
| Quest | Objectives, descriptions, mappins, outcome facts, checkpoint/retry policy, one-shot guard, and terminal success/failure state |

Read [Activation, readiness, and
acquisition](../communities/activation-readiness-and-acquisition.md), [Cleanup
and character safety](../communities/cleanup-and-character-safety.md), and
[Immediate branches and waiting gates](../gates/immediate-and-waiting.md)
first. Route volumes use the world contract in [Triggers and
areas](../world/triggers-and-areas.md).

## Evidence and version boundary

The practical target is Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit
`8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`.
The retained building-block research predates this exact tool baseline, so its
runtime claims remain bounded to their source commit and archive.

| Label | Bounded claim |
| --- | --- |
| **Observed in vanilla** | Focused base-game phases contain device release/readiness, gameplay-AI/follower, ordered NPC trigger, defend, character-mount, vehicle-trunk, and workspot condition shapes. A cited node is not a self-contained extraction system. |
| **Structurally validated** | Research commit `29066f7b76ad4b7435b3fa2a7c0b20ecea464b5e` retains the focused vanilla corpus and reduced advanced shapes. Commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f` retains release, ordered escort, defend, and carry resources that passed handle checks and WolvenKit `8.17.4` round trips. |
| **Runtime-proven** | At source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f`, archive SHA-256 `B082D157978347A126DAACB0A5404AF298B88E549731609D81D5A569CBA81FDF` completed its exact device release, three ordered escort gates, follower-retaining handoff, three-attacker 20-second defend success, surviving-attacker cleanup, and follower-role clear after success. This does not prove its unrecorded failure/retry route, generic movement, carry, trunk placement, or a different target. |
| **Experimental** | A newly assembled extraction; automatic pathing or teleport recovery; defend failure/retry semantics; arbitrary attacker waves; carry, drop, or trunk placement; workspot arrival; interruption; and every untested save/cleanup route remain unproven until their exact candidate passes. |

Useful comparison paths include:

```text
base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_gameplay.questphase
base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_09\phases\sts_wbr_jpn_09_gameplay.questphase
base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase
base\quest\side_quests\sq004\phases\sq004_03_raffen_shiv_camp.questphase
base\open_world\street_stories\watson\kabuki\sts_wat_kab_02\phases\sts_wat_kab_02_openworld.questphase
```

Extract them yourself and inspect only the focused fields. The repository
does not redistribute vanilla CR2Ws.

## Plan the actor ownership timeline

```text
inactive community
  -> restrained target (activate and spawn)
  -> released target (authoritative action confirmed)
     |-> following -> final hold -> defended -> cleaned
     |                         `-> lost -> retry or terminal failure
     `-> carried -> delivered by destination/trunk state -> cleaned
```

Write down the owner at every state. A scene, follower role, workspot, combat
command, carry interaction, and vehicle trunk can all hold references to the
same actor. Cleanup is safe only after the current owner has released it and
the quest has persisted the outcome.

## Release or rescue a named target

A bounded native release child can use this ordered graph:

```text
objective Active
  -> send release/unlock device action
  -> wait matching device controller function
  -> wait named target CharacterSpawned
  -> objective Succeeded
  -> set released fact
  -> Out1
```

The decisive types and joins are:

| Role | Native shape | Required identity |
| --- | --- | --- |
| Send action | `questInteractiveObjectManagerNodeDefinition` → `questDeviceManager_NodeType` | `objectRef`, `deviceControllerClass`, `deviceAction`, and action properties all match the placed device |
| Confirm action | `questPauseConditionNodeDefinition` → `questObjectCondition` → `questDevice_ConditionType` | Same device NodeRef/controller plus exact `deviceConditionFunction` and parameters |
| Confirm target | `questPauseConditionNodeDefinition` → `questCharacterCondition` → `questCharacterSpawned_ConditionType` | Community NodeRef plus exact target entry name, `entireCommunity: 0`, and the intended comparison |
| Persist release | `questFactsDBManagerNodeDefinition` → `questSetVar_NodeType` | Quest-local released fact written exactly once |

This child does not create or activate the target community. An earlier owner
must activate it and prove the target exists. It also does not assign follower
AI. A successful device condition should hand off to readiness, and readiness
should hand off to the movement owner.

For a non-device rescue, replace only the producer: a scene exit, combat
resolution, door state, or scripted fact may authorize release. Keep the same
requirements—one authoritative completion signal, named target readiness, a
durable result, and explicit lifecycle transfer.

Device state persists in saves. A save that saw an earlier controller or
NodeRef may make a corrected action appear already complete. Use an untouched
save lineage and a fresh identity when isolating a materially changed device.

## Assign gameplay AI before observing movement

The reduced escort shape first promotes the target to gameplay AI:

```text
questPuppetAIManagerNodeDefinition
  entries[]
    aiTier: Gameplay
    entityReference
      reference: <target community NodeRef>
      names: [<target entry CName>]
```

It then assigns a player-following role through a
`questMiscAICommandNode` whose typed params contain:

```text
AIAssignRoleCommandParams
  role -> AIFollowerRole
    followerRef.reference: #player
```

The actor reference on the command must select the same community/entry. The
role makes the target a follower; it does not author navmesh, a patrol spline,
doors, elevators, combat recovery, teleport catch-up, or route markers.

Test the follower before adding route gates:

1. target begins in the intended released state;
2. gameplay AI and follower role apply once;
3. target follows through ordinary walkable space;
4. target responds to combat as intended;
5. stream-away/return and save/load preserve one valid role;
6. role clear returns the target to an intentional phase or cleanup state.

## Observe the NPC, not the player, at route gates

An escort gate uses the named actor as the trigger activator:

```text
questPauseConditionNodeDefinition
  condition -> questTriggerCondition
    triggerAreaRef: <destination NodeRef>
    type: IsInside
    isPlayerActivator: 0
    activatorRef
      reference: <target community NodeRef>
      names: [<target entry CName>]
```

`isPlayerActivator: 0` is decisive. Waiting for the player would allow V to
finish the escort while the target remained behind.

A clear three-stage route is:

```text
activate route pin 1 -> wait target in gate 1 -> clear pin 1
activate route pin 2 -> wait target in gate 2 -> clear pin 2
activate route pin 3 -> wait target in gate 3 -> clear pin 3
```

Keep every trigger and its current marker streamable before it becomes the
active gate. Historical testing found a route where only the final marker kept
the final trigger relevant while the graph was waiting on the first gate. The
fixed candidate gave all three gates adequate world coverage and advanced in
order.

Trigger placement is three-dimensional. Center the volume around the actor's
walkable plane; do not place its base exactly at ground height and assume the
actor will count as inside. Inspect the authoritative outline buffer, node
transform, height, bounds, and notifier.

## Transfer the follower role at the final gate

The final gate is an ownership boundary, not automatically the end of the
actor's lifecycle. Choose one explicit result:

| Next activity | Final-gate action |
| --- | --- |
| Quest ends and actor should leave | Clear follower role, move to a safe community phase if needed, then delay deactivation |
| Defend target | Retain follower/gameplay ownership through the hold; clear only after success or terminal failure cleanup |
| Scene | Move to the required scene/workspot state, wait readiness, let the scene acquire, and clear only after its named exit |
| Continue escort | Preserve role and transfer to the next route phase without deactivation |

The preceding sequential-route candidate, archive SHA-256
`3EB9FCB4DBD1CA8BA6730C02CDF81B8A89B855C75372FFF8927DC66F0423D597`,
advanced through all three gates but cleared the role at gate 3; the persistent
actor then walked back toward her original AI spot as the hold began. That
bounded failure is **Runtime-proven** for its own hash. The later `B082D157...`
candidate retained the role through the hold and cleared it only after
successful defense. That corrected handoff is **Runtime-proven** for the later
archive; it remains a design decision for another actor.

## Defend with an explicit success/failure race

A defend objective needs two independent producers:

- success: timer elapsed, attackers resolved, scripted work completed, or a
  dedicated encounter fact;
- failure: protected target killed, defeated, unconscious, below a health
  threshold, or otherwise in the exact prohibited state.

A compact fact-backed shape is:

```text
objective Active
  Out -> wait completion_fact > 0 -> objective Succeeded -> race input 1
      -> wait protected target lost -> objective Failed
                                      -> set failure_fact -> race input 2
race output -> Out1
```

The target-loss listener uses a named entity reference:

```text
questCharacterKilled_ConditionType
  objectRef.reference: <protected community NodeRef>
  objectRef.names: [<protected entry CName>]
  comparisonParams.entireCommunity: 0
  killed / defeated / unconscious: <failure policy>
```

Set the three outcome flags deliberately. A protected target that may be
incapacitated without failing needs a different payload from one where any
defeat is terminal.

### Spawn the attack before starting survival time

The retained successful hold followed this sequence:

```text
activate attacker community
  -> wait attackers spawned
  -> inject two threats against protected actor and one against V
  -> arm target-loss listener and 20-second timer
  -> timer sets completion fact
  -> success deactivates surviving attackers
  -> clear follower role
  -> persist terminal success
```

Starting the timer before attackers are ready measures streaming latency, not
survival. For a kill-all defense, replace the timer producer with the exact
accepted attacker-resolution policy. For multiple waves, make each wave an
owned activation/readiness/combat/resolution/cleanup sub-lifecycle; see
[Stealth, combat, and destruction](stealth-combat-and-destruction.md).

### Retry is a separate policy

A researched structural variant deliberately does not connect its failure
branch to `Out1`. It is intended to sit after a parent checkpoint whose
`questCheckpointNodeDefinition` uses the chosen retry policy. This makes
failure block normal progression instead of converging with success.

That topology is **Structurally validated**, but generic checkpoint reload,
fact rollback, attacker restoration, target restoration, journal reset, and
repeat reward behavior are **Experimental**. Do not label “retry-safe” until
the exact candidate passes:

1. failure before and after attackers engage;
2. manual reload of the pre-defense checkpoint;
3. automatic retry behavior if the design relies on it;
4. clean restoration of target health/state and follower role;
5. no duplicated attackers, timers, facts, notifications, or rewards;
6. repeated failure followed by success;
7. completed-save reload.

An XOR-shaped join also does not prove cancellation of the losing timer or
target-loss listener. Make late signals harmless or test explicit cut
topology.

## Carry requires two simultaneous truths

The reduced carry child first waits until the named target is mounted to the
player:

```text
questPauseConditionNodeDefinition
  condition -> questCharacterCondition
    type -> questCharacterMount_ConditionType
      condition: OnMount
      childRef.reference: <target community NodeRef>
      childRef.names: [<target entry CName>]
      childIsPlayer: 0
      parentIsPlayer: 1
      anyChild: 0
      anyParent: 0
```

It then waits on a logical `AND` containing:

1. the same target-still-mounted condition; and
2. a player `IsInside` condition for the delivery trigger.

```text
target mounted to V
  -> wait (target still mounted to V AND V inside destination)
  -> objective Succeeded
```

This shape prevents a prior mount event from completing after the body has
been dropped elsewhere. It is **Structurally validated** and comparable to
the character-mount shapes **Observed in vanilla** in
`sts_hey_rey_09_openworld.questphase`. Custom carry behavior remains
**Experimental**.

The graph does not create the incapacitated state, pickup prompt, carry
animation, player locomotion restrictions, drop action, destination
presentation, or actor cleanup. Those are prerequisites and separate
acceptance surfaces.

## Trunk placement is not the carry destination condition

The same inspected vanilla phase contains a
`questVehicleTrunk_ConditionType` with a more specific identity join:

```text
questVehicleTrunk_ConditionType
  isInside: 1
  inverted: 0
  anyObject: 0
  anyVehicle: 0
  playerVehicle: 0
  objectRef
    reference: <target community NodeRef>
    names: [<target entry CName>]
  vehicleRef
    reference: <vehicle community NodeRef>
    names: [<vehicle entry CName>]
```

That shape is **Observed in vanilla**. It proves the condition can name both
the object and vehicle. It does not author the trunk interaction, accept an
arbitrary car, make an actor carryable, or clean up either entity.

A trunk-delivery route should therefore be:

```text
carry target to vehicle
  -> vehicle/trunk interaction owns placement
  -> wait exact object-inside-exact-vehicle condition
  -> persist delivery
  -> release carry/trunk interaction ownership
  -> delayed actor and vehicle cleanup
```

If the design permits any player vehicle, research and test that variant
instead of changing `playerVehicle`/`anyVehicle` by intuition. Generic trunk
placement remains **Experimental**.

## Workspot arrival is another distinct state

An escort often ends at a workspot rather than a trigger. The focused vanilla
corpus contains:

```text
questCharacterWorkspot_ConditionType
  puppetRef.reference: <community NodeRef>
  puppetRef.names: [<entry CName>]
  spotRef: <AI spot NodeRef>
  animationName: None
  waitForAnimEnd: 0
  isPlayer: 0
```

This is **Observed in vanilla** only. The condition observes a puppet/spot
relationship; it does not move the actor into the spot, prove workspot
compatibility, or guarantee animation quality. The community phase, AI
command, scene, or other movement owner must send the actor there first.

Use a workspot gate only when the story requires that state. A broad final
trigger is more tolerant of navmesh and animation differences; a workspot
condition is more precise but adds asset, role, and animation dependencies.

## Manual WolvenKit composition order

1. Build the target community and release device. Prove activation, named
   spawn, action, and completion function independently.
2. Add release objective/action/condition/readiness/fact in one ordered child.
3. Set gameplay AI for the same named entity, then assign the intended
   follower role.
4. Place route volumes on verified navigation, give each current gate adequate
   streaming coverage, and add NPC-activator `IsInside` waits in order.
5. Activate and clear route mappins around their matching waits.
6. At the final gate, transfer the follower role to the defend, scene, carry,
   or cleanup owner instead of clearing it by habit.
7. For defense, activate and wait for attackers before arming the timer or
   completion producer; add a separate named target-loss listener.
8. Persist success/failure before community or role cleanup. Keep reward and
   terminal quest completion on a one-shot route.
9. For carry, wait target-on-player first, then wait the logical AND of
   target-still-mounted and player-inside-destination.
10. For trunk or workspot completion, use the focused condition only after the
    interaction/movement owner has been authored and tested.
11. Serialize and reopen every CR2W with WolvenKit `8.19.0`, verify handles,
    actor references, paths, and sockets, pack, extract-verify, and freeze the
    installed hashes.

## Clean-save and lifecycle matrix

Use independent descendants of an untouched pre-quest save. Record the exact
archive, framework files, versions, and slot provenance for every case.

| Case | Required observation |
| --- | --- |
| Before activation | Target and attackers follow their authored inactive policy |
| Release cancel/failure | No released fact, no premature objective success, retry remains possible |
| Release success | Device state, named readiness, objective, and fact advance once |
| Escort ordinary route | Target—not V—crosses every gate in order; pins follow the current gate |
| Player outruns target | Later gate cannot complete early; target recovers or follows documented failure policy |
| Combat during escort | Follower role, target survival, and return to route are correct |
| Save between every gate | Reload restores one target, one current pin, and the correct next gate |
| Defend success | Attackers spawn before timing, success wins once, survivors and role clean up safely |
| Defend failure | Target outcome, journal state, failure fact, attacker cleanup, and retry/terminal policy are exact |
| Near-simultaneous defend signals | Only the intended result mutates state; late losing signal is harmless |
| Carry pickup/drop/re-pickup | Mount condition follows the actual target state and cannot complete from history alone |
| Carry destination | Target remains mounted while V is inside; completion and cleanup occur once |
| Trunk placement/removal | Exact object/vehicle pair toggles the observed state; wrong vehicle cannot satisfy it |
| Workspot arrival/exit | Condition follows the intended actor and spot; interruption does not deadlock cleanup |
| Stream away/return | Target, current role, route gate, attackers/device, and objective restore without duplicates |
| Completed reload | No release action, follower assignment, wave, timer, reward, marker, or cleanup replays |
| Removal isolation | Removing the exact candidate does not masquerade save-backed state as current behavior |

Carry, trunk, workspot, and generic failure/retry claims keep the
**Experimental** label until their own rows pass. The historical GQT003
success cannot promote them.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Release action fires but actor stays restrained | Controller action/function pair, same device NodeRef, target community phase, readiness identity |
| Actor appears but does not follow | Gameplay AI tier, assign-role params, target community/entry, follower ref, navmesh |
| Gate advances when V arrives alone | `isPlayerActivator`, empty/named `activatorRef`, wrong trigger consumer |
| First gate never advances | Volume vertical placement, notifier, target identity, streaming bounds, target on valid navigation |
| Actor walks back at final gate | Follower role cleared before the next owner, persistent community AI returning to its spot |
| Defense timer completes before combat begins | Timer armed before attacker readiness and threat injection |
| Defense succeeds and then fails | Losing listener still active, no authoritative outcome, untested XOR/cut semantics |
| Retry duplicates attackers or rewards | Checkpoint boundary, persistent facts/journal, active listeners, cleanup, one-shot guard |
| Carry completion survives dropping the target | Historical mount event used without a current mount-and-destination AND gate |
| Trunk condition accepts wrong vehicle | `anyVehicle`, `playerVehicle`, or vehicle entity reference too broad |
| Workspot wait never resolves | Movement owner never assigned the spot, wrong spot NodeRef, incompatible actor/workspot, interrupted AI role |
| Cleanup visibly pops the target | Deactivation before scene/AI/carry/trunk owner releases it or cleanup area too small |

When a corrected resource still behaves like an older route, audit [Save state
and clean retests](../troubleshooting/save-state-clean-retests.md). When an
actor exists but an identity join fails, use [Actors, scenes, and
lipsync](../troubleshooting/actors-scenes-lipsync.md) together with the
[Identifier-domain reference](../reference/identifier-domain-reference.md).
