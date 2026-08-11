# Retained vanilla condition catalog

This page is a discovery index for condition shapes found in a focused vanilla
research set. It answers, “Which concrete type names should I search for?” It
does **not** answer, “Which fields should I copy into a new quest?”

Every positive inventory claim on this page is **Observed in vanilla**. A type
name and an occurrence count establish that a serialized shape exists; they do
not establish its truth policy, listener timing, external-reference rules,
save/load behavior, or suitability as a reusable recipe.

For the condition families already reduced to focused property descriptions,
start with [Condition payloads](condition-payloads.md). For predicate
composition, see [Boolean condition trees](boolean-trees.md).

## Corpus and counting method

The retained corpus contains 41 `.questphase` serializations. All 41 headers
report:

- game resource version `2310`;
- WolvenKit `8.17.4`;
- WolvenKit JSON version `0.0.9`.

The count was repeated on **2026-08-09** by recursively enumerating concrete
`$type` object definitions in every serialization. Wrapper-to-payload counts
were then checked by reading the concrete `$type` beneath each wrapper's
`type.Data` handle. Direct fields such as `questLogicalCondition.operation`
and `questTriggerCondition.type` were counted separately.

A `HandleRefId` reference does not create another object definition, so it is
not counted again. Conversely, nested predicates are counted even when they
sit beneath one logical tree. These are corpus occurrence counts, not the
number of distinct behaviors, quests, or game-wide uses.

The recursive scan also encounters `scnCheck...InterruptCondition` and
`scnCheck...ReturnCondition` objects in scene-related data. Those belong to
scene interruption/return contracts, not the quest gate wrapper layer, and are
reserved for the scene condition index rather than mixed into the tables here.

The surrounding graph contains 262 `questConditionNodeDefinition` objects and
797 `questPauseConditionNodeDefinition` objects. Those node counts describe
evaluation schedules. They must not be added to the payload counts or treated
as condition-family popularity rankings. The corpus also contains three
`questConditionItem` objects used as switch containers; the container name
alone does not define its case-selection policy.

Reader-facing inspection targets Cyberpunk 2077 `2.31a` and WolvenKit
`8.19.0`. Re-extract each cited depot resource from your own installation when
the game or serializer changes.

## Core state and composition families

| Concrete wrapper | Concrete nested payload or direct field | Retained instances |
| --- | --- | ---: |
| `questFactsDBCondition` | `questVarComparison_ConditionType` | 259 / 259 |
| `questLogicalCondition` | direct `operation` field | 87 |
| `questTimeCondition` | time payload handle | 168 |
| `questJournalCondition` | journal payload handle | 88 |

The 259 retained fact comparisons use these serialized comparator values:
`Greater` 138 times, `Equal` 55, `GreaterOrEqual` 55, `Less` 9, and
`NotEqual` 2. Absence of another enum value from this sample is not evidence
that the engine cannot represent it.

The 87 logical wrappers contain `AND` 72 times, `OR` 14 times, and `XOR` once.
This is a predicate-object inventory, not evidence for short-circuit order or
multi-child XOR truth policy. In particular, the corpus contains no generic
NOT wrapper. Do not invent one from prose shorthand.

The time and journal wrappers resolve to these concrete payloads:

| Wrapper | Concrete payload | Retained instances |
| --- | --- | ---: |
| `questTimeCondition` | `questRealtimeDelay_ConditionType` | 146 |
| `questTimeCondition` | `questGameTimeDelay_ConditionType` | 19 |
| `questTimeCondition` | `questTimePeriod_ConditionType` | 2 |
| `questTimeCondition` | `questTickDelay_ConditionType` | 1 |
| `questJournalCondition` | `questJournalEntryState_ConditionType` | 66 |
| `questJournalCondition` | `questJournalEntry_ConditionType` | 21 |
| `questJournalCondition` | `questJournalEntryVisited_ConditionType` | 1 |

Do not infer clock policy from the four time class names. Do not treat the
single visited payload as a universal “the player read something” signal. Each
shape still needs its decisive fields, owner, and event source inspected in
context.

## Spatial families

| Concrete wrapper | Concrete nested payload or direct field | Retained instances |
| --- | --- | ---: |
| `questTriggerCondition` | direct `type` field | 214 |
| `questDistanceCondition` | `questDistanceComparison_ConditionType` | 55 / 55 |

The retained trigger field values are `IsInside` 153 times, `IsOutside` 56,
and `Entered` 5. These strings are search keys, not proof that one form is
state-recovering and another is edge-triggered across activation, streaming,
teleportation, or save/load.

Every retained distance wrapper uses a
`questDistanceComparison_ConditionType`. Its 55 comparisons are `Greater` 33
times, `LessOrEqual` 11, `GreaterOrEqual` 10, and `Less` once. The corpus also
contains 55 `questObjectDistance` and 55 `questValueDistance` objects, but
that symmetry does not establish the only legal operand pairing or a universal
measurement unit.

## Object, inventory, device, scan, and destruction families

All four payload types below appear beneath `questObjectCondition` in this
corpus. The wrapper occurs 60 times, exactly matching the nested payload total.

| Concrete payload beneath `questObjectCondition` | Retained instances |
| --- | ---: |
| `questDevice_ConditionType` | 44 |
| `questInventory_ConditionType` | 11 |
| `questScan_ConditionType` | 3 |
| `questDestruction_ConditionType` | 2 |

This shared wrapper is a structural relationship, not evidence that the four
payloads share fields or runtime contracts. Before using any one of them,
inspect the referenced object identity, the concrete operation/state values,
who produces the observed change, and whether the condition represents a
state, a transition, or an engine event.

## Character, combat, and workspot families

The corpus contains 250 `questCharacterCondition` wrappers. Their nested
payloads account for all 250 definitions:

| Concrete payload beneath `questCharacterCondition` | Retained instances |
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

`Condtion` in the two class names above is the spelling present in the
serialization; do not silently “correct” native names while searching. The
table does not prove what counts as spawned, killed, mounted, in combat, in a
workspot, or quickhacked. Actor reference form, community ownership,
streaming/readiness, state transitions, and cleanup remain separate evidence
questions.

## Scene, content, phone, and system families

| Concrete wrapper | Concrete payload | Retained instances |
| --- | --- | ---: |
| `questSceneCondition` | `questSceneNode_ConditionType` | 31 / 31 |
| `questContentCondition` | `questContentLock_ConditionType` | 10 of 15 |
| `questContentCondition` | `questContentToken_ConditionType` | 5 of 15 |
| `questSystemCondition` | `questPhoneMuted_ConditionType` | 26 of 54 |
| `questSystemCondition` | `questCameraFocus_ConditionType` | 24 of 54 |
| `questSystemCondition` | `questPhone_ConditionType` | 4 of 54 |

The editorial grouping reflects the concrete wrapper relationships found in
the files. It does not mean that a scene condition owns scene playback, that a
content condition grants a token, or that all system payloads share phone
lifecycle rules. Locate the corresponding producer and manager nodes before
assigning a behavior to any payload.

## Vehicle and spawning families

| Concrete wrapper | Concrete payload | Retained instances |
| --- | --- | ---: |
| `questVehicleCondition` | `questVehicleSpeed_ConditionType` | 3 of 6 |
| `questVehicleCondition` | `questVehicleTrunk_ConditionType` | 2 of 6 |
| `questVehicleCondition` | `questVehicleWater_ConditionType` | 1 of 6 |
| `questSpawnerCondition` | `questSpawnerReady_ConditionType` | 7 / 7 |

These rare families are especially poor candidates for copy-by-name recipes.
A vehicle predicate still depends on how the vehicle is identified, loaded,
spawned, occupied, and cleaned up. A spawner-ready predicate still needs the
spawner owner, activation order, failure path, and save/load behavior made
explicit.

## Representative depot paths

Use these paths to locate focused examples in your own game archives. They are
not templates, and their quest-local facts, NodeRefs, actors, devices, scenes,
and journal paths are not reusable identifiers.

| Families worth inspecting | Vanilla depot path |
| --- | --- |
| Facts, logical trees, triggers, time, journal, content | `base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase` |
| Game-time and real-time payloads, journal, content token, phone system | `base\quest\side_quests\sq011\phases\sq011_concert.questphase` |
| Inventory, scan, scene, character, vehicle trunk | `base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase` |
| Device, killed, spawned, workspot, quickhack | `base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase` |
| Destruction, device, character combat, vehicle speed | `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase` |
| Spawner ready, distance, character mount | `base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_09\phases\sts_wbr_jpn_09_gameplay.questphase` |

Extract a named resource with WolvenKit, serialize it for local inspection,
and preserve only a focused excerpt or your own notes. Do not redistribute the
extracted CR2W or a complete vanilla serialization.

## Before treating a condition as reusable

For a family that this book has not yet reduced to a practical guide, record
all of the following before presenting an authoring contract:

1. The exact immediate or waiting graph node, its socket route, and the
   concrete condition wrapper stored in its handle.
2. The nested payload class and every decisive field, including native enum
   values and exact spellings rather than inferred labels.
3. Ownership and resolution for every external identifier: facts, typed
   journal paths, NodeRefs, entity or community references, TweakDB records,
   scenes, devices, vehicles, spawners, and workspots as applicable.
4. The producer of the observed state or event and the required activation
   order. A consumer condition does not create its source system.
5. A reduced, mod-owned fixture that survives WolvenKit `8.19.0` save/reopen
   and CR2W round-trip checks with non-null handles and stable concrete types.
6. In-game cases for already-true activation, normal transition, false or
   failure state, save/load while waiting, streaming loss and return where
   relevant, cancellation or phase exit, completion, and re-entry/reset.
7. Exact tested Cyberpunk, WolvenKit, RED4ext, ArchiveXL, and dependency
   versions, plus build hashes, logs, clean-save provenance, and the result of
   every acceptance case.

Until those checks are retained, the catalog entry remains **Observed in
vanilla** and any new behavior claim remains **Experimental**. Successful
serialization alone can make a mod-owned shape **Structurally validated**; it
cannot promote the runtime contract.
