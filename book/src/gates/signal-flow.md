# Signal flow: joins, races, hubs, and switches

Graph-level logical nodes combine **execution signals**. They are not the
Boolean condition trees stored inside a Condition or Pause Condition node.
Keeping those layers separate prevents one of the easiest questphase mistakes:
treating a socket arrival as though it were a `true` value.

Use [Boolean condition trees](boolean-trees.md) when several observations must
be evaluated as one predicate. Use the nodes in this chapter when several
already-running graph routes must meet, compete, or choose an output.

## Evidence boundary

The examples below come from a retained corpus of 41 vanilla questphases
exported with WolvenKit 8.17.4 and game-resource version 2310. They are
**Observed in vanilla**, not universal engine contracts. Extract the named
depot paths from your own installation and compare them with the version you
ship against.

WolvenKit's generated RED types establish the available properties. The
book-owned Lab 2 resource makes its exact two-input/one-output XOR and ordinary
fan-in/fan-out shapes **Structurally validated**. The wider AND, XOR, Hub, and
Switch arities listed below remain **Observed in vanilla** inventory. Arrival
order, reset/re-arm behavior, simultaneous signals, save/load persistence, and
cancellation remain **Experimental** unless a retained runtime test says
otherwise.

## A connection is an edge

A graph node owns `sockets`. Each socket has a `name`, a socket `type`, and a
`connections` array. A connection points weakly to its source and destination
sockets.

CR2W-JSON often exposes the same connection handle from both endpoints. That
does not create two edges. Count the connection object once, then resolve both
socket handles.

The native socket kinds relevant here are:

| Socket type | Role |
| --- | --- |
| `Input` | Accepts an ordinary execution signal |
| `Output` | Emits an ordinary execution signal |
| `CutSource` | Connects a cut-control route to a target |
| `CutDestination` | Receives an explicit cut connection |

Socket arity and connection count are different. One `Out` socket can hold
several outgoing connections, and one `In` socket can be the destination of
several edges. An ordinary node output can therefore fan out without a Hub.

## What vanilla actually contains

The retained corpus has these graph-level nodes:

| Node type | Count | Serialized ordinary-socket shapes |
| --- | ---: | --- |
| `questLogicalAndNodeDefinition` | 47 | 2–11 inputs, one output |
| `questLogicalXorNodeDefinition` | 51 | 2–4 inputs, one output |
| `questLogicalHubNodeDefinition` | 95 | 1→1/2/3 and 2/3→1 |
| `questSwitchNodeDefinition` | 1 | one `In`, three cases, one `Otherwise` |

For all 193 retained AND, XOR, and Hub nodes, `inputSocketCount` and
`outputSocketCount` match the serialized ordinary socket arity. Each also owns
one `CutDestination` socket. The separate Switch is the table's 194th node and
is not included in that 193-node statement.

That inventory supports property and topology claims. It does not, by itself,
prove what happens after the first output, after a save/reload, or when inputs
arrive on the same frame.

## AND: join-shaped convergence

`questLogicalAndNodeDefinition` carries:

| Property | Meaning established by structure |
| --- | --- |
| `inputSocketCount` | Number of ordinary input sockets |
| `outputSocketCount` | Number of ordinary output sockets |
| `sockets` | The actual named sockets and their connections |

**Observed in vanilla:** root node 38 in
`base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase`
has four inputs and one output. A Pause Condition and three Move Puppet routes
converge on its four inputs, and `Out1` continues to another Pause Condition.

This is safely described as a **four-way, join-shaped topology**. Raw structure
alone does not prove that the node remembers every earlier arrival, fires only
once, resets, or restores partial arrivals after loading a save. If your design
depends on those details, make each one an explicit acceptance case.

## XOR: race-shaped convergence

**Observed in vanilla:** root XOR node 17 in
`base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_gameplay.questphase`
receives three independent wait routes:

- security system is in combat;
- an enemy attacks the player;
- the security system is alerted.

Its single output continues to a fact setter. This is a strong example of
**race-shaped convergence**.

It is not evidence that XOR cancels the two losing listeners. Those waits have
no `CutSource` wiring in this phase. It also does not prove deterministic
resolution for simultaneous arrivals or that a later arrival cannot emit
again. Treat all three claims as **Experimental**.

Lab 2 uses a two-input XOR-shaped convergence because that exact resource can
be structurally inspected and given a focused runtime matrix. See
[Lab 2: Signal Race](lab-02.md).

## Hub: a structural routing node

Do not teach Hub as “the fan-out node.” Vanilla uses it in several shapes:

- **Observed in vanilla:** root Hub 70 in the Q108 phase above has one input and
  three outputs.
- **Observed in vanilla:** root Hub 302 in
  `base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase`
  has two inputs and one output. Its `Out1` itself has two outgoing edges.
- In the same phase, Hub 195 is formally one-input/one-output, while two edges
  target that single `In1` socket.

These resources prove split- and merge-shaped wiring. They do not establish
whether each input is passed through independently, whether a multi-input Hub
waits, whether one arrival broadcasts to all outputs, or which edge runs first.
Use a Hub only after the behavior you need has its own runtime test. For a
simple split, an ordinary output with several connections is the smaller
structure.

## Switch: conditions mapped to case sockets

`questSwitchNodeDefinition` owns a `behaviour` and a list of
`questConditionItem` values. Each item combines a condition handle with a
numeric `socketId`. The corresponding output is named `Case<socketId>`.

The sole Switch in the retained corpus is nested beneath phase node 252 in:

```text
base\open_world\minor_activities\watson\northside\
ma_wat_nid_15\ma_wat_nid_15_phase.questphase
```

**Observed in vanilla:** it uses `First_Fulfilled`, three fact conditions, one
case output for each recorded socket ID, and an unconnected `Otherwise`
socket.

| Serialized part | Observed relationship |
| --- | --- |
| `conditions[n].socketId` | Numeric identity for that condition's case |
| `Case<socketId>` | Output socket associated with the item |
| `In` | Ordinary input that reaches the switch |
| `Otherwise` | Additional output present in the retained shape |

The retained file does not establish evaluation order, short-circuiting,
continuous monitoring, exact `Otherwise` behavior, or the meaning of
`All_Fulfilled`. Those behaviors remain **Experimental**.

## Author safely in WolvenKit

1. Decide whether you are combining predicates or execution routes. If they
   are predicates, return to [Boolean condition trees](boolean-trees.md).
2. Add the graph node with the smallest required arity.
3. Set `inputSocketCount` and `outputSocketCount` before wiring it.
4. Confirm that the visible ordinary sockets match those counts.
5. Connect each producer to the intended named input and the continuation to
   the intended output.
6. Save, reopen, and inspect both endpoints of every edge. Do not count
   reciprocal handle references as separate connections.
7. Export a focused review JSON and verify node IDs, socket names, arity, and
   resolved endpoints.
8. Test every arrival order, then repeat the relevant cases across save/load
   and clean-save replay.

Node IDs are local to a phase graph. A nested phase graph can reuse an ID from
its parent, so record the graph scope whenever you cite or audit a node.

## Design checklist

Before shipping a join, race, Hub, or Switch, answer these questions with
evidence rather than names:

- Which route starts each input producer?
- Can two producers finish together?
- What records the winner or completed prerequisites durably?
- Can a losing listener still write journal state later?
- What stops, cuts, or makes that late write harmless?
- What happens when saving with only some inputs satisfied?
- Can the containing phase be entered again?
- Does the completed-save route bypass every one-shot side effect?

If any answer depends on undocumented timing, label it **Experimental** and add
it to the runtime acceptance record.
