# Condition payloads

The surrounding graph node decides *when* a condition matters. Its condition
object decides *what* counts as fulfilled. In serialized form, many predicates
have two payload layers:

```text
quest condition node
└── condition                    domain wrapper
    └── type                     concrete comparison or event payload
```

For example, `questFactsDBCondition` owns a
`questVarComparison_ConditionType`, while `questTimeCondition` owns a
real-time or game-time delay type. Do not replace one wrapper while leaving an
incompatible nested `type` handle behind.

Read [Immediate branches and waiting gates](immediate-and-waiting.md) before
this chapter. Both graph-node classes carry the same base-condition handle,
but a concrete payload still needs evidence for its intended use. The retained
fact comparison appears beneath both schedules; the delay recipes below appear
beneath Pause nodes.

## Fact comparison

The focused shape is:

```text
questFactsDBCondition
└── type                         questVarComparison_ConditionType
    ├── factName                 string (`CString` in WolvenKit's RED type)
    ├── value                    signed integer
    └── comparisonType           comparison enum
```

The comparison enum provides:

| `comparisonType` | Predicate |
| --- | --- |
| `Equal` | fact value equals authored value |
| `NotEqual` | fact value does not equal authored value |
| `Greater` | fact value is greater than authored value |
| `GreaterOrEqual` | fact value is at least authored value |
| `Less` | fact value is less than authored value |
| `LessOrEqual` | fact value is at most authored value |

Facts are integers. Authors often use `0` and `1` as a Boolean convention, but
the resource does not turn the fact into a Boolean type. These predicates can
express counters and stage values as well:

```text
signal_ready == 1
guards_remaining <= 0
quest_stage >= 3
```

Choose the comparator that states the invariant. `Equal 1` and `Greater 0`
are not interchangeable when another system can write `2`.

The same vanilla street-story phase uses
`jpn_03_stealth_fail == 1` beneath both a Pause node and an immediate
Condition node:

```text
base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase
```

That is **Observed in vanilla** evidence that the fact payload is reusable
under both schedules. It is not evidence that a fact is automatically reset
when either node completes.

### Author a fact predicate

In a mod-owned node's `condition` property:

1. Create a `questFactsDBCondition` handle.
2. Create `questVarComparison_ConditionType` beneath its `type` property.
3. Set the exact `factName`, signed integer `value`, and `comparisonType`.
4. Reopen the resource and verify both handles are non-null and retain their
   concrete classes.
5. Test from a save whose prior fact state is known.

`NotEqual` is payload-specific negation. It does not prove that a generic NOT
condition exists. [Boolean condition trees](boolean-trees.md) develops that
boundary.

## Trigger condition

`questTriggerCondition` carries its decisive fields directly:

| Property | Role |
| --- | --- |
| `type` | Trigger predicate such as `IsInside` or `IsOutside` |
| `triggerAreaRef` | NodeRef of the authored trigger area |
| `activatorRef` | Entity reference used when an explicit activator is required |
| `isPlayerActivator` | Selects the player as activator in the observed player form |

An **Observed in vanilla** player gate appears at root Pause node `20` in:

```text
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
```

It uses `type: IsInside`, the `#q108_tr_mainframe` `triggerAreaRef`, and
`isPlayerActivator: 1`. The same phase also contains a nested AND tree that
names several non-player activators and requires them inside a trigger.

This predicate crosses into world ownership. `#q108_tr_mainframe` resolves
because that quest's streamed resources provide it. Reusing the text in a new
quest does not create a trigger. A mod-owned condition needs a NodeRef that
resolves to its own loaded trigger area at the time the gate is active.

Enum names such as `Entered`, `Exited`, `IsInside`, and `IsOutside` must not be
used as proof of exact temporal behavior. The retained serialization does not
establish whether a form is edge-triggered or state-recovering through load,
streaming changes, teleportation, or activation while the player is already
inside. Treat those cases as **Experimental** until tested.

### Author a trigger predicate

1. Establish ownership of the mod's trigger and its NodeRef before editing the
   questphase.
2. Create `questTriggerCondition` beneath the graph node's `condition` handle.
3. Set `triggerAreaRef` and the intended `type` explicitly.
4. For the player form, set `isPlayerActivator` deliberately and inspect the
   resulting `activatorRef`; for another actor, begin from a separately
   verified actor-reference shape.
5. Test activation from outside, inside, after streaming transition, and after
   save/load before claiming state or event semantics.

`IsOutside` is another payload-specific way to express a negative predicate.
It is not a universal logical NOT wrapper.

## Distance comparison

A distance predicate separates the comparison from its two operands:

```text
questDistanceCondition
└── type                         questDistanceComparison_ConditionType
    ├── distanceDefinition1      questObjectDistance handle
    ├── distanceDefinition2      questValueDistance handle
    └── comparisonType           comparison enum
```

Two focused operand types are:

| Type | Decisive properties |
| --- | --- |
| `questObjectDistance` | `entityRef`, `nodeRef2` |
| `questValueDistance` | `distanceValue` |

Root Pause node `251` provides an **Observed in vanilla** object-versus-value
example in:

```text
base\quest\side_quests\sq031\phases\sq031_rogue.questphase
```

Its first operand resolves the local player and `#emmerick`; its second operand
is `distanceValue: 4`; its comparison is `LessOrEqual`.

Call `4` a numeric distance threshold. The retained resource does not prove
that the authored unit is exactly one metre, which reference points on the two
entities are measured, or how streaming and teleportation affect evaluation.

Before authoring a new distance gate, state both operands in plain language:

```text
distance(local player, contact NodeRef) <= threshold
```

Then verify the nested concrete types after saving. A null operand handle,
wrong NodeRef, wrong local-player selector, or unintended numeric value changes
the predicate even when the graph caption still says "distance."

## Journal predicates

Three similarly named nested payloads represent different questions:

| Concrete `type` beneath `questJournalCondition` | Decisive fields | Question |
| --- | --- | --- |
| `questJournalEntryState_ConditionType` | `path`, engine `state`, `inverted` | Is the entry in an authored lifecycle state, optionally inverted? |
| `questJournalEntry_ConditionType` | `path`, user `state` | Is the entry in an authored user-facing state? |
| `questJournalEntryVisited_ConditionType` | `path`, `visited` | Does the entry have the authored visited flag? |

Every `path` is a typed `gameJournalPath`, not only a slash-separated string.
Its `realPath`, `className`, and `fileEntryIndex` must identify the supplied
journal entry together.

An immediate state example is Condition node `195` in:

```text
base\quest\side_quests\sq011\phases\sq011_concert.questphase
```

It checks whether a phone choice group is `Active` with
`questJournalEntryState_ConditionType`. The typed path records the exact leaf
class and file-entry index.

The retained corpus's single visited payload appears beneath Pause node `127`
in:

```text
base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase
```

It addresses phone message
`contacts/8ug8ear/sts_hey_rey_09/warning4` with
`questJournalEntryVisited_ConditionType` and `visited: 1`.

That one example does not make "journal visited" a generic signal for reading
an inventory shard, computer page, email, or unrelated UI item. Use the entry
family and event source that actually own the interaction.

### Author a journal predicate

1. Identify the exact journal entry and the state dimension being tested:
   lifecycle, user state, or visited.
2. Create `questJournalCondition`, then choose the matching concrete nested
   type.
3. Populate the full typed path. Verify `className` against the leaf resource,
   not against the surrounding quest or folder.
4. Set `state`, `visited`, or `inverted` only where that concrete type owns the
   property.
5. Test from separate untouched, active, visited, and completed saves as the
   design requires.

The `inverted` field belongs to the entry-state payload. It is not a generic
property available on every condition family.

## Time conditions

`questTimeCondition` wraps a concrete time payload. Two common retained forms
are:

| Concrete `type` | Fields | Retained count |
| --- | --- | ---: |
| `questRealtimeDelay_ConditionType` | `hours`, `minutes`, `seconds`, `miliseconds` | 146 |
| `questGameTimeDelay_ConditionType` | `days`, `hours`, `minutes`, `seconds` | 19 |

The native real-time property is spelled `miliseconds`. Preserve that exact
property name when reviewing serialized data; "correcting" it creates a
different, unknown field rather than configuring the resource.

Focused **Observed in vanilla** examples include:

- a two-second real-time delay at nested Pause node `71` in
  `base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase`;
- a 23-hour game-time delay at node `146` in
  `base\quest\side_quests\sq011\phases\sq011_concert.questphase`;
- a three-day delay at node `61` and a five-hour delay at node `87` in
  `base\quest\side_quests\sq011\phases\sq011_follow_up.questphase`.

The corpus also has one tick-delay payload and two time-period payloads. Their
presence is **Observed in vanilla**, but this chapter does not promote those
rare shapes to authoring recipes.

A delay owns only its gate. The downstream graph owns the call, message,
journal update, or other presentation that follows. A 23-hour condition in a
vanilla contact flow does not mean the delay itself schedules phone UI.

### Author and test a delay

1. For the delay recipes covered here, put `questTimeCondition` beneath
   `questPauseConditionNodeDefinition`. The retained immediate time condition
   uses a different `questTimePeriod_ConditionType` inside an AND tree; that
   snapshot time-window shape is outside this recipe.
2. Create `questTimeCondition` and the intended real-time or game-time nested
   type.
3. Set every time component explicitly, including zero-valued components.
4. Verify the exact concrete type and native property spelling after save and
   round-trip.
5. Record normal-play elapsed behavior separately from pause menu, time skip,
   fast travel, save/load, restart, and loading-screen cases.

The cited files establish resource shapes, not clock policy. Every behavior in
step 5 is **Experimental** until the exact mod-owned build is exercised and the
observation is retained.

## Validate the payload before runtime

For any condition family, record this focused resource view:

| Check | What to capture |
| --- | --- |
| Surrounding node | Concrete immediate or pause node class and graph-local ID |
| Wrapper | Concrete class stored by the node's `condition` handle |
| Nested payload | Concrete `type` class, if that wrapper owns one |
| Decisive properties | Comparison, value, path, NodeRef, activator, or time fields |
| Socket route | Entry socket and every connected result socket |
| External owner | Fact writer, journal resource, streamed NodeRef, actor, or clock assumption |

A non-null handle and successful WolvenKit save are necessary structural
checks. They do not prove that an external reference resolves, that save state
starts clean, or that the runtime schedule matches the design.
