# Graph execution

A questphase graph is a set of node definitions connected through named
sockets. Execution enters a node through an input socket, the node performs its
operation or evaluates its condition, and execution continues through one or
more output sockets.

The graph is not executed according to the order in which nodes happen to
appear in serialized JSON or in a WolvenKit list.

## Nodes, sockets, and connections

Every quest node has a graph-local numeric `id` and an array of socket handles.
A socket has:

- a name such as `In`, `Out`, `Active`, `Succeeded`, `True`, or `False`;
- a direction or role such as `Input`, `Output`, or `CutDestination`;
- zero or more graph connections.

A connection joins one source output socket to one destination input socket:

```text
node 12, Out  ──────────>  node 13, In
```

The socket names carry semantics. Sending execution into `Active` on a journal
node activates an entry; sending it into `Succeeded` changes that same entry to
a different state. The node type and path can be identical while the incoming
socket changes the operation.

## Entry and termination

A small child-compatible phase commonly exposes:

```text
questInputNodeDefinition   socketName: In1
    ...
questOutputNodeDefinition  socketName: Out1
                           type: Terminating
```

`In1` and `Out1` are the phase interface. Internal node sockets can still be
named `In` and `Out`.

A terminating output is an explicit lifecycle boundary. Reaching the last
gameplay node is not the same as terminating the phase unless an edge reaches
the output node.

## Evaluate now versus wait

The two most important condition shapes have different control semantics.

### `questConditionNodeDefinition`

This node evaluates when execution reaches it and immediately chooses a named
output such as `True` or `False`.

Lab 1 uses it for:

```text
cqa001_completed == 0
    True  -> activate the quest
    False -> terminate
```

It does not wait for a false condition to become true.

### `questPauseConditionNodeDefinition`

This node holds its execution path until the condition becomes true, then emits
`Out`.

Lab 1 uses a `questRealtimeDelay_ConditionType` for ten seconds. Later chapters
use pause conditions for facts, triggers, actor readiness, inventory, and
other wait-until gates.

Replacing one condition node type with the other changes the quest's behavior
even if their nested comparison data looks identical.

## Fan-out, joins, and ordering

One output can connect to several inputs. That starts several paths; it does not
establish a secret order among them.

```text
arrival
  +-> update objective
  +-> start hostility setup
```

If later work requires both paths, use a node with explicit join semantics. If
only the first signal should win, use a race/XOR shape. Do not use visual
proximity or JSON array order as a substitute for control flow.

An ordered sequence needs edges:

```text
activate community
  -> wait for spawn readiness
  -> start scene
```

Starting all three from one fan-out would permit the scene to begin before its
actor is ready.

## Ordinals are local semantics

Some scene and quest node types attach ordinals to ordered sockets or options.
An ordinal belongs to that node type's local contract; it is not the execution
order of the entire graph.

For example, **Observed in vanilla**, scene choice nodes use option socket
ordinals and additional padded sockets. That rule does not mean every quest
output socket needs an ordinal or that node ID `12` executes before node ID
`13`.

Preserve ordinals when copying a verified node shape. Explain their purpose
before generating or renumbering them.

## Cut and interrupt sockets

Many graph nodes contain a `CutDestination` socket in addition to their normal
inputs and outputs. It belongs to cancellation or interruption routing, not to
ordinary success flow.

The presence of the socket does not mean every tutorial should wire it.
Interruption policy must answer:

- what work is currently active;
- what journal or world state must be cleaned up;
- whether a scene or child phase must receive a cut;
- which output tells the parent that interruption is complete.

Until a guide proves those answers, an unwired cut socket should be described
as a visible lifecycle obligation rather than filled with a guessed edge.

## Reading the Lab 1 graph

Trace [the exact Lab 1 figure](../start-here/lab-01.md#exact-questphase) by
following socket labels:

1. `In1` emits `Out` into the one-shot guard's `In`.
2. `True` enters the quest journal node through `Active`.
3. Each ordinary `Out` advances the first-run sequence.
4. The delay's `Out` enters the objective through `Succeeded`.
5. The final quest journal operation enters through `Succeeded`.
6. Both the guard's `False` route and the successful route reach the same
   terminating output.

That trace explains behavior without relying on how WolvenKit arranged the
boxes.
