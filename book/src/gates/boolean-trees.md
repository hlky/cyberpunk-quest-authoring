# Boolean condition trees

`questLogicalCondition` combines child condition objects into one predicate.
It is embedded beneath an immediate or waiting graph node; it is not itself a
graph node and has no execution sockets.

```text
questPauseConditionNodeDefinition
└── condition                    questLogicalCondition
    ├── operation                AND
    └── conditions
        ├── questTriggerCondition
        └── questLogicalCondition
            ├── operation        OR
            └── conditions       ...
```

The surrounding node still decides the schedule:

- beneath `questConditionNodeDefinition`, the combined predicate chooses an
  immediate `True` or `False` route;
- beneath `questPauseConditionNodeDefinition`, the combined predicate defines
  when the waiting path may continue through `Out`.

Review [Immediate branches and waiting gates](immediate-and-waiting.md) and
[Condition payloads](condition-payloads.md) before constructing a nested tree.

## Evidence boundary

The retained 41-phase corpus contains 87 `questLogicalCondition` objects. Its
copies report game resource version `2310` and were serialized with WolvenKit
`8.17.4`. Reader inspection targets Cyberpunk 2077 `2.31a` and WolvenKit
`8.19.0`; review date: **2026-08-09**.

| Operation | Retained instances | Supported claim |
| --- | ---: | --- |
| `AND` | 72 | **Observed in vanilla** as a child-predicate composition |
| `OR` | 14 | **Observed in vanilla** as a child-predicate composition |
| `XOR` | 1 | **Observed in vanilla** as one rare four-child shape; runtime policy not established here |
| `NAND` | 0 | Present in the WolvenKit enum; no retained vanilla instance or runtime proof |
| `NOR` | 0 | Present in the WolvenKit enum; no retained vanilla instance or runtime proof |
| `NXOR` | 0 | Present in the WolvenKit enum; no retained vanilla instance or runtime proof |
| generic `NOT` | not an enum value | No generic NOT recipe is supported |

Enum availability is structural information, not a runtime acceptance result.
Treat the zero-instance operations and the rare XOR behavior as
**Experimental** until a focused mod-owned fixture establishes their truth,
timing, reload, and re-entry contracts.

## Condition tree versus signal-flow topology

Two native layers use similar names:

| Predicate layer | Execution-signal layer |
| --- | --- |
| `questLogicalCondition` | graph nodes such as `questLogicalAndNodeDefinition` |
| Owns an `operation` and child `conditions` | Owns graph sockets and receives edges |
| Combines truth values | Combines or routes arriving execution signals |
| Nested in one node's `condition` handle | Listed as a graph node with a numeric `id` |

This distinction prevents a common category error. A predicate AND can ask
whether the player is inside an area *and* a fact is set. It cannot wait for
two independent execution branches to arrive. Conversely, a graph-level join
does not read those state predicates merely because its type name contains
`And`.

When inspecting CR2W-JSON, ask where the object lives. An object under
`condition.Data.conditions` is predicate composition. An object in the
graph's `nodes` collection with sockets and an `id` is signal topology.

## A nested vanilla tree

Pause node `28` in this resource provides a compact **Observed in vanilla**
example:

```text
base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase
```

Its focused predicate is:

```text
AND(
  player IsInside #ma_wat_nid_15_tr_area_vision,
  OR(
    signpost_start > 0,
    signpost_combat > 0,
    signpost_ended > 0
  )
)
```

The outer AND owns two child handles: one trigger condition and one nested
logical condition. The inner OR owns three fact conditions. Parentheses are
therefore resource ownership, not visual decoration:

```text
inside AND (start OR combat OR ended)
```

is not the same tree as:

```text
(inside AND start) OR combat OR ended
```

Record nesting explicitly whenever prose uses both AND and OR.

## AND: every child predicate

Use an AND tree when the authored predicate requires every child state
together:

```text
AND(
  prerequisite_fact > 0,
  player IsInside #activity_area
)
```

The surrounding graph node decides whether that combined truth is sampled now
or waited upon. AND does not establish the order in which the two states became
true. If the quest requires "first set the prerequisite, then enter the area,"
encode that sequence with graph edges and separate gates.

The q108 tower-mainframe phase contains another **Observed in vanilla** AND
tree requiring the player and three named actors inside a trigger:

```text
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
```

That structure shows heterogeneous activator references beneath one logical
tree. It does not prove which child is inspected first, whether inspection
short-circuits, or how actor streaming affects a new mod-owned version.

## OR: any represented alternative

Use an OR tree to represent alternative leaf predicates within one condition:

```text
OR(
  quest_stage == 2,
  quest_stage == 3,
  quest_completed > 0
)
```

OR does not report which child was responsible. The surrounding condition
node produces only its own result socket. If downstream work needs to know the
winning reason, preserve that information in separate immediate branches or
in authored state rather than expecting the OR payload to emit a named case.

Do not rely on child-array order for priority. The retained structures support
membership and nesting; they do not establish short-circuit order or side
effects during evaluation.

## XOR is a bounded observation, not a general recipe

The only retained logical-condition XOR is a four-child tree beneath Pause
node `127` in:

```text
base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase
```

Its children are two scan predicates, one journal-visited predicate, and one
fact predicate. This is **Observed in vanilla** evidence that the serialized
four-child shape exists.
It is not enough to claim whether multi-child XOR means exactly one fulfilled
child, parity, a first-changing child, or another runtime policy. It also says
nothing about cancellation because a condition tree owns no graph listener
sockets to cancel.

For a new quest, keep XOR **Experimental** until a focused truth-table test
covers every relevant child combination, including more than one child
fulfilled together and state restored from a save.

## There is no generic NOT condition

The logical-operation enum in the inspected WolvenKit classes contains AND,
OR, XOR, NAND, NOR, and NXOR. It does not contain NOT, and the retained corpus
contains no standalone generic negation node.

Express negation only through a payload that owns a verified negative form:

| Domain | Focused negative form | Boundary |
| --- | --- | --- |
| Fact comparison | `comparisonType: NotEqual` | Negates that integer equality, not an arbitrary subtree |
| Trigger state | `type: IsOutside` | Describes that trigger predicate; exact transition timing still needs tests |
| Journal lifecycle state | `questJournalEntryState_ConditionType.inverted: 1` | Belongs to this concrete journal payload only |

For example:

```text
AND(
  alarm_state != 1,
  player IsOutside #restricted_area
)
```

uses two independently supported leaf forms. It does not prove a hypothetical
`NOT(AND(...))` resource shape.

NAND, NOR, and NXOR should not be offered as substitutes merely because their
enum values exist. With no retained vanilla instance and no focused runtime
acceptance, their precise multi-child behavior remains **Experimental**.

## Author a nested tree in WolvenKit

Use a mod-owned `.questphase` in WolvenKit `8.19.0`:

1. Choose the surrounding immediate or pause node from the intended schedule.
2. Set that node's `condition` handle to `questLogicalCondition`.
3. Set `operation` to the supported operation required by the design; begin
   with AND or OR.
4. Add one handle per child to `conditions`. Each child must contain a concrete
   condition wrapper such as `questFactsDBCondition` or
   `questTriggerCondition`.
5. To nest another group, store another `questLogicalCondition` as that child
   handle's concrete object, set its operation, and populate its own
   `conditions` array.
6. Inspect every leaf's decisive properties and every nested handle before
   leaving the property editor.
7. Save, reopen, and verify the tree shape independently of the graph layout.

For the observed MA_WAT_NID_15 shape, the review record should be small and
deterministic:

| Depth | Object | Decisive value |
| ---: | --- | --- |
| 0 | `questLogicalCondition` | `operation: AND`, two child handles |
| 1 | `questTriggerCondition` | player `IsInside` the named trigger NodeRef |
| 1 | `questLogicalCondition` | `operation: OR`, three child handles |
| 2 | three `questFactsDBCondition` objects | named facts, each `Greater 0` |

Do not paste the complete vanilla resource into notes or a chapter. This
focused tree plus the depot path is enough to reproduce the inspection.

## Structural checks

A Boolean tree is **Structurally validated** only after the mod-owned resource
passes checks such as:

- the surrounding node's `condition` handle resolves;
- every item in `conditions` is a non-null handle with the intended concrete
  class;
- nested group boundaries and child counts survive CR2W round-trip;
- every fact name, comparison, typed journal path, and NodeRef is exact;
- the graph node retains the expected `In` and result sockets;
- no graph-level logical node was substituted for an embedded condition tree.

Structural validation still does not prove runtime timing. For a waiting tree,
exercise child states becoming true in different orders, states already true
on activation, save/load during the wait, and exit while it is active. For an
immediate tree, exercise each result route and combinations where several
children are true together. Until those cases are retained against the exact
build, the behavior beyond the observed resource shape is **Experimental**.

Return to the [Conditions and gates overview](index.md) when deciding whether
the next requirement belongs to predicate composition or execution-signal
topology.
