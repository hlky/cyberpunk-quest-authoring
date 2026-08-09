# Inputs and outputs

Questphase inputs and outputs form an interface around a graph. They are
implemented by nodes inside the child resource and matched by sockets on the
parent's `questPhaseNodeDefinition`.

## Two socket layers

The names are easy to conflate:

```text
parent phase node                 child graph boundary
-----------------                --------------------
input socket In1            ->   input socketName In1
                                  ordinary socket Out -> child work

output socket Out1          <-   output socketName Out1
                                  child work -> ordinary socket In
```

`questInputNodeDefinition.socketName` names the entry exposed by the child.
Execution then leaves that node through its ordinary `Out` socket.

`questOutputNodeDefinition.socketName` names the result exposed by the child.
Execution reaches that node through its ordinary `In` socket.

Lab 4's focused terminating-child contract is:

| Resource/node | Graph ID | Interface value | Internal or parent socket |
| --- | ---: | --- | --- |
| Child `questInputNodeDefinition` | `0` | `socketName: In1` | emits internal `Out` |
| Parent `questPhaseNodeDefinition` | `13` | input `In1` | receives parent flow |
| Child `questOutputNodeDefinition` | `1` | `socketName: Out1`, `type: Terminating` | receives internal `In` |
| Parent `questPhaseNodeDefinition` | `13` | output `Out1` | emits returned parent flow |

Those names are `CName` values. They are not graph-local IDs and not CR2W
handle IDs.

## Entry is a contract, not an activation rule

The input node says where execution enters after a phase has been invoked. It
does not decide why or when that invocation happens.

Activation policy belongs outside that boundary:

- ArchiveXL root attachment makes a root reachable;
- parent graph flow reaches the phase node's `In1`;
- the parent node resolves its external child;
- the first child action begins only after the child enters through its
  matching `socketName`.

Lab 4's child `0.Out` activates the reach objective. The location behavior
comes from later `IsInside` and `IsOutside` conditions, not from `In1`.

## Terminating output returns one outcome

With `type: Terminating`, reaching child output node `1.In` ends that child
route. Its `socketName: Out1` maps the result to parent node `13.Out1`.

The parent resumes only through that matching phase-node output:

```text
child 17.Out -> child 1.In
  child exposes Out1
    -> parent 13.Out1 -> parent 14.Active
```

The connection from `13.Out1` to the parent's confirmation objective is
essential. A child output does not automatically select the next parent node.

Termination does not:

- reset facts;
- remove journal history;
- deactivate world dependencies automatically;
- invent an outgoing parent connection;
- prove the root will never be evaluated again.

Those are separate lifecycle decisions.

## `In1` and `Out1` are not universal

Lab 4 deliberately uses the smallest focused interface: one input and one
terminating output. Do not infer that every native phase node has both.

**Observed in vanilla:** extract these files from your own game:

```text
base\open_world\street_stories\watson\northside_industrial_district\
  sts_wat_nid_03\phases\sts_wat_nid_03.questphase

base\open_world\street_stories\watson\northside_industrial_district\
  sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase
```

The inspected root contains an external phase node with `In1`, `Out1`, and
`CutDestination`, and another external phase node with `In1` and
`CutDestination` but no `Out1`. That second shape is enough to reject
“all phase nodes have In1/Out1” as an engine invariant.

Use `In1`/`Out1` here because the parent must wait for one child activity and
then continue. Copy the interface contract appropriate to the lifecycle you
are implementing, not the nearest-looking graph.

## Multiple outcomes require matching evidence

A child can expose several meaningful results only when the complete parent
and child arrangement supports them:

```text
child output "accepted" -> parent phase-node output "accepted" -> continuation
child output "declined" -> parent phase-node output "declined" -> cleanup
```

Every outcome requires:

1. a reachable child output node with the intended `socketName`;
2. a same-named output socket on the invoking phase node;
3. an intentional parent connection or documented terminal policy;
4. runtime evidence for the exact arrangement.

Lab 4 makes no multi-outcome claim. It returns only `Out1`.

## Cut is a separate socket class

Lab 4's input, output, and phase nodes retain structurally valid
`CutDestination` sockets. None is connected. `CutDestination` is not an alias
for `Out1`, and an unwired socket is not a tested interruption policy.

The presence and serialized type are **Structurally validated**. The runtime
behavior of a wired cut, its propagation across the child boundary, and the
required recovery state remain **Experimental**.

## Review checklist

For each interface node, record:

| Question | Why it matters |
| --- | --- |
| What is the `socketName`? | It is the cross-phase interface name |
| Which internal socket is connected? | It proves the internal route reaches the boundary |
| Is the output `Terminating`? | It defines what reaching the boundary does to the child |
| Does the parent expose the same name? | A mismatch breaks the intended handoff |
| Where does the parent output lead? | A returned outcome still needs a continuation |
| Is a cut route wired? | Normal return and interruption are separate routes |

A phase can serialize while an intended outcome remains unreachable. Review
reachability, exact names, and both resources together.

Previous: [Registering a root questphase](root-registration.md). Next:
[Calling child phases](child-phases.md).
