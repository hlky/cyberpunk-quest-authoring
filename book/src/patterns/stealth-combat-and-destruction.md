# Stealth, combat, and destruction

Stealth, combat, planting, and destruction are not four names for one
objective node. They are separate producers observed by quest logic:

- a stealth monitor records whether an optional rule was broken while the
  main activity continues;
- an encounter owns community activation, readiness, hostility, resolution,
  and cleanup;
- a plant interaction owns a real device action and completion signal before
  inventory is consumed;
- a destruction condition observes damage on an object that is already
  authored to be destructible.

Keep those producers separate and converge only their durable results.

```text
start required activity
  |-> arm optional stealth monitor -> stop and resolve outcome --\
  `-> activate owner -> interact/fight/plant/destroy              +
                      -> write required completion ---------------/
  -> advance journal/reward state
  -> delayed world cleanup
```

## Prerequisites

Inventory every owner before editing the quest graph:

| System | Required authoring |
| --- | --- |
| Community | Registry, compiled area, named entries/phases, AI spots, character records, appearances, factions/attitudes, and activation policy |
| World | Quest prefab, combat-safe navigation, activation and cleanup volumes, device or destructible placement, bounds, and NodeRefs |
| Quest | Required and optional objectives, outcome facts, branch policy, reward/completion owner, and one-shot guard |
| Device/target | Controller class, supported action and condition function, persistent-state identity, interaction workspot, item record if consumed, and actual destruction capability if damage is required |
| Lifecycle | Spawn readiness, hostility target, nonlethal policy, wave end condition, late monitor signals, stream return, save/load, and cleanup |

Start with [Communities and characters](../communities/index.md), [Triggers and
areas](../world/triggers-and-areas.md), [Devices and persistent
state](../world/devices-and-persistence.md), and [Parallel monitors and
cancellation](../gates/monitors-and-cancellation.md).

## Vanilla references

These focused base-game resources are useful comparisons. Extract them from
your own installation; they are references, not files to copy into the project.

```text
base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase
base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_combat.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase
base\open_world\street_stories\santo_domingo\arroyo\sts_std_arr_05\phases\sts_std_arr_05_openworld.questphase
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase
base\open_world\phases\cyberpsychos\open_world_cyberpsychos.questphase
```

## Optional stealth is a parallel monitor

An entry-time condition cannot represent “remain undetected while the player
does something else.” Arm the optional objective, its failure wait, and its
stop wait together:

```text
activate optional objective
  Out -> wait failure_fact > 0 -> objective Failed ------> race input 1
      -> wait stop_fact > 0    -> objective Succeeded
                               -> set success_fact = 1 ---> race input 2

race output -> monitor child Out1
```

The reduced native graph uses these types:

| Role | Node/payload | Decisive properties |
| --- | --- | --- |
| Start presentation | `questJournalNodeDefinition` | Objective path through `gameJournalQuestObjective`; enter through `Active` |
| Failure listener | `questPauseConditionNodeDefinition` → `questFactsDBCondition` → `questVarComparison_ConditionType` | `failure_fact Greater 0` |
| Stop listener | Same types | `stop_fact Greater 0` |
| Failure write | `questJournalNodeDefinition` | Same objective; enter through `Failed` |
| Quiet write | `questJournalNodeDefinition` | Same objective; enter through `Succeeded` |
| Durable quiet result | `questFactsDBManagerNodeDefinition` → `questSetVar_NodeType` | `success_fact`, `setExactValue: 1`, `value: 1` |
| Convergence | `questLogicalXorNodeDefinition` | Two inputs, one output in the retained reduced shape |

The activity owner—not the monitor—produces `stop_fact`. Set it only after the
last gameplay action that is allowed to fail stealth. The security, sight,
combat, alarm, or script owner produces `failure_fact`.

### XOR does not prove cancellation

An XOR-shaped convergence says where two routes meet. The focused vanilla
graphs and reduced resource do not prove that the losing Pause Condition is
destroyed, that simultaneous arrivals have stable priority, or that a late
failure cannot emit.

Make the result safe even if the listener survives:

1. Treat one outcome fact as authoritative.
2. Gate every journal writer so only an unresolved monitor may write.
3. Make late signals bypass all state mutation.
4. If explicit cut topology is required, connect and test the exact
   `CutSource`/`CutDestination` targets rather than assuming a phase exit cuts
   them.
5. Save with both waits armed, reload, and exercise both arrival orders.

The hash-bound quiet-install result proves its two tested routes. It does not
promote the general rules above to a runtime cancellation contract.

## Produce stealth failure from a real system

Choose a producer that corresponds to the player-facing rule. Examples
include a security system entering combat, a dedicated detection fact, an
alarm device state, or a named actor's combat/senses condition. Do not set a
failure fact merely because V entered the objective area.

The retained quiet-install harness used a dangerous security area linked to
the encounter community and observed
`SecuritySystemControllerPS.IsSystemInCombat`. That specific controller,
world link, and route are covered by its runtime record. It is not evidence
that every community automatically informs every security system.

For each producer, document:

| Question | Required answer |
| --- | --- |
| What arms it? | Community/device activation and stream boundary |
| What exact event or state fails stealth? | Controller function, fact writer, or character condition |
| Is it state-shaped or edge-shaped? | Determines activation and reload tests |
| When is it disarmed? | Stop fact, tested cut, or harmless late-signal policy |
| Who persists the result? | Dedicated fact and optional journal state |

## Own the encounter lifecycle

A bounded community encounter follows this order:

```text
activation trigger
  -> activate objective/description/mappin
  -> Spawn Manager Activate
  -> wait required entries spawned
  -> inject explicit hostile target per entry
  -> wait for the authored resolution policy
  -> succeed objective and set outcome
  -> wait for safe cleanup boundary
  -> Spawn Manager Deactivate
```

### Activation and readiness

Whole-community `Activate None/None` is useful only when the encounter owns
every entry. Its `Out` socket does not prove every guard exists. An aggregate
`CharacterSpawned Greater 0` with `entireCommunity: 1` proves at least the
comparison's community-scoped result, not every named entry.

When completion depends on a fixed roster, wait for each named entry or prove
the exact whole-community comparison against a matching vanilla resource and
runtime matrix. Start combat only after every required target has resolved.

### Explicit hostility

The retained three-entry generated shape chains one combat command per actor:

```text
questCombatNodeDefinition
  entityReference
    reference: <community NodeRef>
    names: [<entry CName>]
  function: questCombatNodeParams_ShootAt
  params -> AIInjectCombatThreatCommandParams
    dontForceHostileAttitude: 0
    targetPuppetRef.reference: #player
    duration: <authored value>
    isPersistent: <authored value>
```

An attitude group, faction record, threat injection, and combat target are
related but not interchangeable. A historical null-target pulse left visible
guards passive; a later explicit target worked in its own candidate. Always
name the actor receiving the command and the intended target, then test
ordinary awareness, direct attack, player stealth, disengagement, and reload.

### Completion is an outcome policy

`questCharacterKilled_ConditionType` is misleadingly broad. Its payload can
observe `killed`, `defeated`, and `unconscious` independently. A nonlethal-safe
encounter normally enables every outcome the objective accepts.

One retained reduced whole-community payload is:

| Property | Retained value | Boundary |
| --- | --- | --- |
| Wrapper | `questCharacterCondition` | Character-condition schedule |
| Concrete type | `questCharacterKilled_ConditionType` | Name does not imply lethal-only behavior |
| `objectRef.reference` | Encounter community NodeRef | No entry names in the whole-community shape |
| `comparisonParams.comparisonType` | `GreaterOrEqual` | Coupled to the exact condition implementation |
| `comparisonParams.count` | `0` | Do not reinterpret as generic arithmetic outside the source-matched shape |
| `comparisonParams.entireCommunity` | `1` | Community-scoped result |
| `killed` / `defeated` / `unconscious` | `1` / `1` / `1` | Accepts the three represented resolution states |

This is **Structurally validated** historical evidence, not a universal copy
recipe. Inspect a vanilla encounter with the same roster and resolution rule,
then prove that early deaths, initially absent entries, nonlethal takedowns,
streaming, and save/load cannot satisfy or deadlock the gate incorrectly.

## Compose waves as owned sub-lifecycles

Treat every wave as a complete sub-lifecycle rather than another Spawn Manager
node appended to a shared condition:

```text
wave 1: activate -> all required spawned -> hostility -> resolution -> cleanup
  -> inter-wave fact/checkpoint/presentation
wave 2: activate -> all required spawned -> hostility -> resolution -> cleanup
  -> encounter completion
```

Prefer separate communities or explicit named phases when later entries must
not count toward the current wave. If several waves share one community,
prove exactly how inactive, dead, despawned, or future entries affect every
community-scoped comparison.

The single three-attacker survival wave in a
[retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
is **Runtime-proven** only for its recorded activation, engagement, successful
20-second route, and escort/defend handoff. General sequential waves remain
**Experimental**.

Do not spawn the next wave before the previous wave's surviving actors have a
defined owner. Decide whether survivors despawn, retreat, transfer into the
next phase, or remain as harmless world state. A journal success edge alone
does not clean them up.

## Cyberpsycho encounters are a separate contract

Do not turn an ordinary three-guard graph into a cyberpsycho by renaming the
objective. Focused vanilla investigation shows this broader lifecycle:

```text
activate journal and area mappin
  -> enter outer trigger
  -> activate boss community and wait for named boss
  -> keep boss protected until reveal/arena policy is satisfied
  -> reveal from scan, sight, attack, hit, clue, or scripted event
  -> enable gameplay AI, mortality, hostile target, and combat
  -> wait broad resolution
  -> split lethal and spared outcomes
  -> evidence/report/reward
  -> distance or exit cleanup
```

The minimum resource boundary includes a named boss community entry, combat
space, reveal and cleanup triggers, journal category/mappin, character record,
scanner/name data, and cleanup. The large boss health bar is driven by a
proper character record with `rarity: NPCRarity.Boss` plus hostile target
tracking; it is not a quest-node overlay toggle.

For resolution, use separate named-entry conditions:

| Outcome | `killed` | `defeated` | `unconscious` |
| --- | ---: | ---: | ---: |
| Lethal | `1` | `0` | `0` |
| Spared/nonlethal | `0` | `1` | `1` |

Converge only after writing different outcome facts. The global
`open_world_cyberpsychos.questphase` owns umbrella progress; an individual
sighting still owns its own spawn, fight, report, reward, and cleanup.

These relationships are **Observed in vanilla**. A current generic custom
cyberpsycho recipe is **Experimental** because no retained runtime record in
this book proves reveal races, boss HUD behavior, lethal/nonlethal resolution,
reload, reporting, and cleanup for one new hash-bound candidate.

## Plant through a real device interaction

First decide whether the player or the quest initiates the operation. Those
topologies are not interchangeable.

### Player-driven runtime route

The retained quiet-install candidate used the device asset to expose a
player-selected `Steal Data` personal-link interaction. Its quest graph did
not send that initiating action. It waited for the resulting controller state,
then owned presentation and cleanup:

```text
objective Active
  -> device/template exposes the player prompt
  -> PauseCondition: ScriptableDeviceComponentPS.IsPersonalLinkConnected
  -> five-second install progress presentation
  -> questInteractiveObjectManagerNodeDefinition
       questDeviceManager_NodeType: QuestForceDisconnectPersonalLink
  -> questItemManagerNodeDefinition: RemoveAll exact keylogger
  -> objective Succeeded
  -> completion fact
```

The decisive ownership is:

| Role | Owner or binding |
| --- | --- |
| Expose the initiating prompt | Device template, instance/controller package, interaction record, slot/workspot, and current persistent state |
| Observe connection | `questPauseConditionNodeDefinition` carrying `questObjectCondition` / `questDevice_ConditionType`, the exact device NodeRef and controller class, and `IsPersonalLinkConnected` |
| End the interaction | `questDeviceManager_NodeTypeParams` bound to the same device/controller and `QuestForceDisconnectPersonalLink`, after the wait and presentation |
| Consume item | `questAddRemoveItem_NodeTypeParams`, exact item `TweakDBID`, player reference, quantity/removal policy, and notification policy |
| Persist result | Dedicated fact set only after disconnection and inventory mutation succeed |

That ordering is **Runtime-proven** only for the
[retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence).
Sending the
disconnect action before the player connects would be a different and
unsupported route.

### Quest-driven structural template

A separate reduced template serializes this order:

```text
objective Active
  -> quest sends the intended device action
  -> wait for that action's authoritative controller condition
  -> remove the exact item
  -> objective Succeeded
  -> completion fact
```

This command-before-condition template is **Structurally validated**, not
runtime proof of the quiet-install route. Use it only when the quest itself is
supposed to initiate the operation. If the player must select a prompt, expose
the interaction through the device and begin the graph-side sequence at the
resulting condition. A proximity trigger is not proof that either interaction
occurred.

Device state is save-backed. Give a materially revised device a fresh identity
during isolation, or a used save can preserve the preceding controller state.
Test cancel, disconnect, repeated interaction, missing item, save during the
interaction, completed reload, and candidate removal.

## Observe destruction; do not synthesize it

The inspected `sts_wat_nid_03_openworld.questphase` contains this focused
condition twice:

```text
questPauseConditionNodeDefinition
  condition -> questObjectCondition
    type -> questDestruction_ConditionType
      objectRef.reference: #nid_03_ws_hwango_car_spawn_001
      threshold: 100
```

That exact shape is **Observed in vanilla**. It proves a NodeRef-backed object
and a serialized threshold can be observed. It does not prove:

- the units or scaling of `threshold` for every object class;
- that an arbitrary mesh, entity, or device has destructible components;
- which damage sources count;
- whether repair, stream return, or reload restores the target;
- whether two conditions on one target emit once or repeatedly.

First author or select a target whose entity/device contract already supports
the intended damage and destruction. Then add the condition as an observer,
not as the mechanism that makes the target destructible. A generic custom
destructible-target tutorial remains **Experimental** until the target asset,
condition, cleanup, and save matrix are retained together.

## Manual WolvenKit composition order

1. Build and inspect the community, security/device, and target resources
   before adding completion gates.
2. Author activation and cleanup areas with correct notifier and outline
   buffers.
3. Add objective and mappin activation, then community activation.
4. Wait for every actor whose readiness matters; do not infer a fixed roster
   from aggregate `> 0`.
5. Add one explicit hostility command per intended actor and target.
6. Add the exact lethal/nonlethal or protected-target resolution policy.
7. If stealth is optional, split the failure and stop listeners from the same
   start edge and make late signals harmless.
8. If planting is player-driven, expose the device prompt, wait for its
   controller state, then perform presentation, cleanup action, inventory
   mutation, and the completion fact. If it is quest-driven, send an initiating
   action only when that behavior is explicitly intended and separately tested.
9. If destruction is required, verify the target's destructible behavior
   independently before trusting the quest condition.
10. Advance journal/reward state before delayed cleanup. Do not let an
    encounter cleanup edge erase a scene actor or escorted target owned by the
    next phase.
11. Serialize and reopen every CR2W with WolvenKit `8.19.0`, inspect handles
    and NodeRefs, pack, extract-verify, and freeze exact candidate hashes.

## Controlled acceptance matrix

| Case | Required observation |
| --- | --- |
| Quiet stealth route | Optional objective succeeds once; required activity remains completable |
| Detection route | Correct producer fails stealth once; required activity still follows its authored policy |
| Late failure after stop | No second journal write or contradictory fact |
| Save with monitor armed | Reload preserves one valid outcome route without duplicate listeners |
| Encounter approach | No actors before activation; every required actor spawns once on safe navigation |
| Lethal completion | Accepted lethal states complete exactly once |
| Nonlethal completion | Accepted incapacitated states complete exactly once; rejected states do not |
| Partial roster | One unresolved or unstreamed entry cannot falsely complete the encounter |
| Wave transition | Previous wave ownership ends before the next wave becomes authoritative |
| Plant cancel/retry | Cancel does not consume the item or write completion; retry can succeed |
| Destruction thresholds | Below/at/above boundary behave exactly as the design relies on |
| Stream away/return | Actors, device, target, and armed waits restore without duplicates |
| Completed reload | No objective, hostility pulse, reward, or cleanup repeats |
| Clean replay | Both stealth outcomes and every required combat outcome work from separate untouched saves |

For cyberpsycho work, add approach, reveal, arena, hostile acquisition, boss
HUD, lethal, spared, evidence, report, reward, cleanup, and saves at each hold
point. Structure alone cannot promote any of them.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Optional stealth resolves immediately | Stop/failure facts inherited from the save, entry-time test used instead of a monitor, or wrong comparator |
| Both stealth outcomes write | Losing listener still active, no authoritative outcome fact, or simultaneous signal policy untested |
| Guards spawn but remain passive | Missing explicit target, wrong named entry, faction/attitude mismatch, threat command before readiness |
| Encounter completes early | Aggregate readiness/resolution scope, future/inactive entries, count/comparator payload, stale facts |
| Encounter never completes nonlethally | `defeated`/`unconscious` flags, actor identity, protected/invulnerable state, or wrong target roster |
| Second wave never appears | Previous community not cleaned/transferred, next sector not streamed, reused phase state, or shared comparison counting the wrong entries |
| Plant objective completes on approach | Proximity used as completion instead of device condition |
| Plant action works only once across builds | Save-backed device state or reused NodeRef/controller persistence |
| Damage never advances objective | Target is not destructible, wrong object NodeRef, wrong threshold semantics, or damage source not supported |
| Actor disappears during cleanup | Deactivation occurs before journal/scene/escort ownership transfers |

Use [Serialization success versus runtime
validity](../troubleshooting/serialization-vs-runtime.md) when a round-tripped
resource still fails in game, and [Controlled isolation and
evidence](../troubleshooting/controlled-isolation-evidence.md) before changing
several lifecycle surfaces at once.
