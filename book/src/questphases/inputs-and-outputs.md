# Inputs and outputs

Questphase inputs and outputs form an interface around the graph. They are
implemented by nodes inside the resource and matched by sockets on the parent
phase node.

## Two socket layers

The names are easy to conflate:

```text
external phase interface        internal graph flow
------------------------        -------------------
input socketName: In1     ->    input node socket: Out
output socketName: Out1   <-    output node socket: In
```

`questInputNodeDefinition.socketName` names the entry exposed by the phase.
Execution then leaves that node through its ordinary `Out` socket.

`questOutputNodeDefinition.socketName` names the result exposed by the phase.
Execution reaches that node through its ordinary `In` socket.

The completed Lab 1 resource uses:

| Node | Graph ID | Interface property | Internal flow socket |
| --- | ---: | --- | --- |
| `questInputNodeDefinition` | `0` | `socketName: In1` | `Out` |
| `questOutputNodeDefinition` | `1` | `socketName: Out1`, `type: Terminating` | `In` |

Those names are values, not graph-local IDs and not CR2W handle IDs.

## Entry

The input node is a boundary, not a trigger condition. It says where execution
enters after the phase has been invoked or evaluated.

Any actual activation policy belongs outside that boundary:

- root attachment makes a root phase reachable;
- a parent `questPhaseNodeDefinition` invokes a child;
- the first internal gate decides whether work should proceed;
- a location condition introduces geographic activation only if authored.

Lab 1's `In1` flows directly to a fact condition. That is why it is
location-independent, not because `In1` itself means “always active.”

## Terminating output

The output node closes the active phase route. With `type: Terminating`,
reaching its internal `In` ends that phase execution.

For a root phase, termination ends the current route; persistent facts and
journal state written before it remain governed by their own save behavior.
For a child, the matching parent output is the handoff point.

Termination does not:

- reset facts;
- remove journal history;
- deactivate world dependencies automatically;
- invent an outgoing parent connection;
- prove the root will never be evaluated again.

Those are separate lifecycle decisions.

## Multiple outcomes

A phase interface can describe more than one meaningful result when the
invoking node exposes matching outputs. Use outcome names to preserve meaning,
not merely to avoid drawing a condition in the parent:

```text
child accepted route -> output "accepted"
child declined route -> output "declined"

parent phase node:
  accepted -> continue job
  declined -> clean up and terminate
```

Every outcome contract requires all three parts:

1. a reachable child output node with the intended `socketName`;
2. a same-named output socket on the invoking phase node;
3. an intentional outgoing connection or explicit terminal policy in the
   parent.

Do not assume an arbitrary name is supported by a particular node type merely
because it is a `CName`. Copy a proven resource shape, inspect the serialized
node, and test the complete handoff.

## Review checklist

For each interface node, record:

| Question | Why it matters |
| --- | --- |
| What is the `socketName`? | It is the cross-phase interface name |
| Which internal socket is connected? | It proves the internal route reaches the boundary |
| Is the output `Terminating`? | It defines what reaching the boundary does to the child |
| Does the parent expose the same name? | A mismatch breaks handoff |
| Where does the parent output lead? | A returned outcome still needs a continuation |
| What happens on cut? | Success output and interruption are separate routes |

The phase can serialize while an intended outcome remains unreachable. Review
reachability and names together.
