# Condition index

Use this page to find a native condition class, its wrapper, and the chapter
that owns its current evidence boundary. A class name in the retained corpus
proves that a serialized shape exists; it does not prove listener timing,
external-reference resolution, save/load behavior, or suitability as a recipe.

Unless a row says otherwise, inventory counts are **Observed in vanilla** in
the retained 41-questphase corpus described by [Retained vanilla condition
catalog](../gates/condition-catalog.md). That corpus was serialized with
WolvenKit `8.17.4`; current reader inspection targets Cyberpunk 2077 `2.31a`
and WolvenKit `8.19.0`. The exact condition shapes supplied by Labs 1–5 are
**Structurally validated**, while their runtime claims remain controlled by
the lab markers and acceptance records. [Labs at a glance](labs-at-a-glance.md)
identifies the smallest project for each taught family.

## Choose the evaluation schedule first

The same predicate can sit beneath two different graph schedules:

| Graph node | Question answered on entry | Focused ordinary results |
| --- | --- | --- |
| `questConditionNodeDefinition` | “Is this predicate fulfilled now?” | `True` or `False` |
| `questPauseConditionNodeDefinition` | “When this predicate becomes fulfilled, continue this active route.” | `Out` after fulfillment |

An immediate Condition does not wait on its `False` route. A Pause Condition
does not expose an ordinary `False` continuation in the focused shape. See
[Immediate branches and waiting gates](../gates/immediate-and-waiting.md).

## Read the payload layers

Many condition families use two object layers:

```text
Condition or Pause Condition node
└── condition                    domain wrapper
    └── type                     concrete predicate payload
```

For example:

```text
questFactsDBCondition
└── questVarComparison_ConditionType
```

Other wrappers, including `questTriggerCondition`, carry decisive fields
directly. Preserve the actual wrapper/payload pairing; replacing a wrapper
while leaving an incompatible nested handle is not a type conversion.

## Families reduced to practical property contracts

| Family | Wrapper | Concrete payload or direct fields | Decisive values | Book evidence |
| --- | --- | --- | --- | --- |
| Fact comparison | `questFactsDBCondition` | `questVarComparison_ConditionType` | `factName`, signed `value`, `comparisonType` | 259 retained instances are **Observed in vanilla**; exact Lab 1–5 fact predicates are **Structurally validated** |
| Trigger | `questTriggerCondition` | Direct `type`, `triggerAreaRef`, `activatorRef`, `isPlayerActivator` | `IsInside`, `IsOutside`, or another specifically evidenced predicate; exact NodeRef and activator | 214 retained instances are **Observed in vanilla**; exact Lab 3–5 player gates are **Structurally validated** |
| Distance | `questDistanceCondition` | `questDistanceComparison_ConditionType` containing operand handles | `questObjectDistance`, `questValueDistance`, comparator, both object identities | 55 retained instances are **Observed in vanilla**; no Lab 1–5 distance gate |
| Journal lifecycle | `questJournalCondition` | `questJournalEntryState_ConditionType` | Typed path, engine `state`, payload-specific `inverted` | 66 retained instances are **Observed in vanilla** |
| Journal user state | `questJournalCondition` | `questJournalEntry_ConditionType` | Typed path and user-facing `state` | 21 retained instances are **Observed in vanilla** |
| Journal visited | `questJournalCondition` | `questJournalEntryVisited_ConditionType` | Typed path and `visited` | One retained instance is **Observed in vanilla** |
| Realtime delay | `questTimeCondition` | `questRealtimeDelay_ConditionType` | `hours`, `minutes`, `seconds`, native spelling `miliseconds` | 146 retained instances are **Observed in vanilla**; exact Lab 1, 2, and 4 delays are **Structurally validated** |
| Game-time delay | `questTimeCondition` | `questGameTimeDelay_ConditionType` | `days`, `hours`, `minutes`, `seconds` | 19 retained instances are **Observed in vanilla** |
| Character spawned | `questCharacterCondition` | `questCharacterSpawned_ConditionType` | `objectRef`, comparison type/count, `entireCommunity` | 73 retained instances are **Observed in vanilla**; exact Lab 5 `Greater 0` community-scoped wait is **Structurally validated** |

The focused authoring fields and validation steps are in [Condition
payloads](../gates/condition-payloads.md). Community readiness adds the
identity and activation-order requirements in [Activation, readiness, and
acquisition](../communities/activation-readiness-and-acquisition.md).

### Fact comparators

The property guide exposes these native values. The count column keeps the
retained corpus observation separate from enum availability:

| `comparisonType` | Predicate | Retained instances |
| --- | --- | ---: |
| `Equal` | fact equals authored value | 55 |
| `NotEqual` | fact does not equal authored value | 2 |
| `Greater` | fact is greater than authored value | 138 |
| `GreaterOrEqual` | fact is at least authored value | 55 |
| `Less` | fact is less than authored value | 9 |
| `LessOrEqual` | fact is at most authored value | 0 |

The absence of `LessOrEqual` from this focused sample is not evidence that the
enum cannot represent it.

Facts are signed integers. `Equal 1` and `Greater 0` are not interchangeable
when another writer can store `2`.

### Trigger predicates

The retained trigger inventory contains:

| Direct `questTriggerCondition.type` | Retained instances |
| --- | ---: |
| `IsInside` | 153 |
| `IsOutside` | 56 |
| `Entered` | 5 |

These names are search keys, not proof of exact state-versus-edge behavior
through activation, teleportation, streaming, or save/load. The exact Lab 3–5
resources use state-shaped `IsInside` / `IsOutside` forms with the player form
of the activator fields; only their retained acceptance cases can promote a
runtime claim.

### Time payloads

| Concrete payload beneath `questTimeCondition` | Retained instances | Current depth |
| --- | ---: | --- |
| `questRealtimeDelay_ConditionType` | 146 | Property recipe and **Structurally validated** lab examples |
| `questGameTimeDelay_ConditionType` | 19 | Property recipe plus vanilla observations |
| `questTimePeriod_ConditionType` | 2 | Inventory only |
| `questTickDelay_ConditionType` | 1 | Inventory only |

The payload name does not settle pause-menu, time-skip, fast-travel,
loading-screen, process-restart, or save-restoration policy. Those are separate
runtime cases; see [Delays, facts, and persistence
boundaries](../gates/delays-and-persistence.md).

## Logical condition trees

`questLogicalCondition` combines child predicates inside one Condition or
Pause Condition. It is not a graph-level join or race node.

| Direct `operation` | Retained instances | Safe current statement |
| --- | ---: | --- |
| `AND` | 72 | Every represented child predicate is required by the authored tree; exact evaluation order and short-circuit policy are not inferred |
| `OR` | 14 | The tree represents alternatives but does not report which child supplied fulfillment |
| `XOR` | 1 | The four-child serialized shape exists; its multi-true truth policy remains **Experimental** |

The exact nested AND condition in Lab 2 is **Structurally validated**. There is
no generic NOT wrapper in the retained corpus. Use a payload's own negative
form only when that payload owns one—for example `NotEqual`, `IsOutside`, or
the journal-state payload's `inverted` field. See [Boolean condition
trees](../gates/boolean-trees.md).

Do not confuse the table with `questLogicalAndNodeDefinition` or
`questLogicalXorNodeDefinition`. Those graph nodes combine execution signals
and have sockets; `questLogicalCondition` combines predicate objects and has
no listener sockets to cancel.

## Object-condition families

The retained corpus contains 60 `questObjectCondition` wrappers. Their nested
payloads account for all 60 definitions:

| Concrete payload | Retained instances | External owner to identify before authoring |
| --- | ---: | --- |
| `questDevice_ConditionType` | 44 | Placed device identity, template/controller state, and the producer of the observed device state |
| `questInventory_ConditionType` | 11 | Item/record identity, inventory owner, quantity or state, and the operation that changes it |
| `questScan_ConditionType` | 3 | Scannable target identity and scan event/state owner |
| `questDestruction_ConditionType` | 2 | Target identity and destruction-state producer |

All four rows are **Observed in vanilla** inventory, not current property
recipes. The shared wrapper does not imply shared fields or runtime behavior.

## Character, combat, and workspot families

The 250 retained `questCharacterCondition` wrappers contain:

| Concrete payload | Retained instances |
| --- | ---: |
| `questCharacterSpawned_ConditionType` | 73 |
| `questCharacterMount_ConditionType` | 67 |
| `questCharacterKilled_ConditionType` | 37 |
| `questCharacterStatusEffect_CondtionType` | 29 |
| `questCharacterState_ConditionType` | 18 |
| `questCharacterCombat_ConditionType` | 11 |
| `questCharacterHealth_ConditionType` | 4 |
| `questCharacterHit_ConditionType` | 4 |
| `questCharacterWorkspot_ConditionType` | 4 |
| `questCharacterAttack_ConditionType` | 1 |
| `questCharacterGender_CondtionType` | 1 |
| `questCharacterQuickHacked_ConditionType` | 1 |

`Condtion` is the native spelling in the two class names above. Preserve it
when searching. Except for the bounded `CharacterSpawned` contract taught by
Lab 5, these rows remain **Observed in vanilla** discovery entries. Before
authoring one, establish actor/community ownership, reference form,
streaming/readiness, the producer of the state change, and cleanup.

Lab 5's focused spawn wait is:

```text
questCharacterCondition
└── questCharacterSpawned_ConditionType
    ├── objectRef.reference: community NodeRef
    └── comparisonParams
        ├── comparisonType: Greater
        ├── count: 0
        └── entireCommunity: 1
```

Read it literally: the community-scoped spawned count is greater than zero.
It does not prove that every actor in a multi-entry community is ready.

## Scene, content, phone, and system families

| Wrapper | Concrete payload | Retained instances | Boundary |
| --- | --- | ---: | --- |
| `questSceneCondition` | `questSceneNode_ConditionType` | 31 | Scene state consumer; it does not launch the scene |
| `questContentCondition` | `questContentLock_ConditionType` | 10 | Content-lock predicate inventory |
| `questContentCondition` | `questContentToken_ConditionType` | 5 | Content-token predicate inventory |
| `questSystemCondition` | `questPhoneMuted_ConditionType` | 26 | Phone-muted predicate inventory |
| `questSystemCondition` | `questCameraFocus_ConditionType` | 24 | Camera-focus predicate inventory |
| `questSystemCondition` | `questPhone_ConditionType` | 4 | Phone-state predicate inventory |

Every row is **Observed in vanilla**. A condition is a consumer of state; it
does not create the scene, token, phone call, or camera behavior it observes.

## Vehicle and spawning families

| Wrapper | Concrete payload | Retained instances | Boundary |
| --- | --- | ---: | --- |
| `questVehicleCondition` | `questVehicleSpeed_ConditionType` | 3 | Identify the exact vehicle, load/spawn owner, and speed comparison |
| `questVehicleCondition` | `questVehicleTrunk_ConditionType` | 2 | Identify vehicle/trunk state and the producer of that state |
| `questVehicleCondition` | `questVehicleWater_ConditionType` | 1 | Inventory only |
| `questSpawnerCondition` | `questSpawnerReady_ConditionType` | 7 | Identify spawner ownership, activation order, failure route, and cleanup |

These rare families are **Observed in vanilla** and remain poor copy-by-name
recipes. They require reduced mod-owned fixtures before practical publication.

## Distance operands

All 55 retained `questDistanceCondition` wrappers use
`questDistanceComparison_ConditionType`. The focused operand relationship is:

```text
questDistanceComparison_ConditionType
├── distanceDefinition1 -> questObjectDistance
│   ├── entityRef
│   └── nodeRef2
├── distanceDefinition2 -> questValueDistance
│   └── distanceValue
└── comparisonType
```

Call `distanceValue` a numeric threshold. The retained shape does not prove a
universal measurement unit, the reference points used on each entity, or
streaming/teleportation policy.

## Focused vanilla search routes

Extract these resources from your own game and retain only focused notes or
excerpts. Do not redistribute the CR2W files or full serializations.

| Families | Depot path |
| --- | --- |
| Facts, logical trees, triggers, time, journal, content | `base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase` |
| Game-time/realtime, journal, content token, phone | `base\quest\side_quests\sq011\phases\sq011_concert.questphase` |
| Inventory, scan, scene, character, vehicle trunk | `base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase` |
| Device, killed, spawned, workspot, quickhack | `base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase` |
| Destruction, device, combat, vehicle speed | `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase` |
| Spawner ready, distance, character mount | `base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_09\phases\sts_wbr_jpn_09_gameplay.questphase` |

## Before promoting an indexed family

For a condition not yet taught as a practical recipe, retain:

1. the exact immediate or waiting graph node and socket route;
2. the wrapper, nested concrete payload, and every decisive field;
3. ownership and resolution for every external identifier;
4. the system or graph operation that produces the observed state;
5. a mod-owned WolvenKit `8.19.0` round trip with non-null compatible handles;
6. already-true, normal-transition, false/failure, save/load, stream-loss,
   cancellation, completion, and re-entry cases as applicable;
7. exact versions, installed hashes, save provenance, and logs.

Until those checks exist, a corpus row remains **Observed in vanilla** and a
new behavior claim remains **Experimental**.
