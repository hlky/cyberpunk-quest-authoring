# Completion and interruption

A phase is complete only when execution reaches the intended output and its
owner has performed the required state transitions. The last visible objective
update is not an implicit return.

## Normal child completion

Lab 4's child ends with:

```text
[16] wait until player IsOutside leave volume
  -> [17] leave objective Succeeded
  -> [1] terminating output socketName Out1
```

Reaching output node `1` terminates that child route and exposes outcome
`Out1`. It does not itself finish the root quest.

## Parent continuation is the second half

![Handoff Point parent-child contract](../images/lab-04/cqa004.handoff-contract.svg)

The parent phase node must expose the same name and connect it onward:

```text
child [1] socketName Out1
  -> parent [13].Out1
  -> parent [14] confirmation objective Active
  -> [15] wait 30 realtime seconds
  -> [16] confirmation objective Succeeded
  -> [17] phase Succeeded
  -> [18] set cqa004_completed = 1
  -> [19] quest Succeeded
  -> [1] terminating output
```

The confirmation window exists to make the ownership transition observable
and saveable. If objective `cqa004_01_obj_confirm` becomes active, normal
execution has returned to parent-only work. A reload during that 30-second
window tests a different boundary from a reload while the child is waiting on
a trigger.

Review both resources. A terminating child output with no matching parent
socket cannot convey the intended result. A matching parent socket with no
outgoing connection receives the result and then advances nowhere.

## Termination is not cleanup

Reaching a `questOutputNodeDefinition` does not, by itself:

- inactivate objectives or mappins;
- deactivate a community;
- stop a scene or parallel monitor;
- reset a device's persistent state;
- clear or set a completion fact;
- choose what a parent does next;
- unload every prefab declared by an ancestor.

Lab 4's child performs its local presentation transitions before return: the
checkpoint pin is retired, the reach objective is succeeded, and the leave
objective is succeeded. The parent owns the remaining confirmation and final
quest completion.

Every transient dependency needs an owner and release boundary. Persistent
progress remains only because the re-entry design calls for it.

## Write durable state before terminating

Lab 4 writes `cqa004_completed = 1` after the child has returned and the
confirmation objective and phase have succeeded, but before the quest succeeds
and the root terminates:

```text
phase Succeeded
  -> set completion fact exactly to 1
  -> quest Succeeded
  -> terminate root route
```

Moving the terminating output earlier would make later writes unreachable.
Moving the fact earlier would change which incomplete save boundaries take the
already-completed bypass. The exact order is part of the recovery policy and
must be tested, not inferred from one uninterrupted run.

## Cut sockets are structural interruption surfaces

Many quest nodes expose a `CutDestination` socket. Its presence identifies a
distinct socket class; it does not supply a correct interruption policy.

Lab 4 retains the serialized cut sockets on its relevant nodes and connects
none of them. Its validator rejects any ordinary or cut edge involving
`CutDestination`.

| Claim | Evidence class |
| --- | --- |
| The sockets exist with type `CutDestination` | **Structurally validated** |
| Similar sockets exist in extracted vanilla phases | **Observed in vanilla** |
| An unwired Lab 4 child cleans up correctly when externally interrupted | **Experimental** |
| A wired cut propagates across this parent/child boundary and reaches a particular recovery state | **Experimental** |

Do not draw a cut edge merely to make the graph look complete. Before wiring
one, define:

1. what work may be active when the cut arrives;
2. which child, scene, or monitor receives interruption;
3. which journal entries become inactive, failed, or resumable;
4. which communities, markers, devices, and monitors are released;
5. which durable fact distinguishes cut from normal completion;
6. which child output tells the parent cleanup has finished;
7. which save/reload cases prove the recovery policy.

That requires a separate fixture. Lab 4 teaches normal `Out1` handoff only.

## Re-entry across two active owners

Termination ends an execution route, not the lifetime of all save-backed
state. A composed quest has more than one meaningful reload boundary:

| Save boundary | Expected active owner in Lab 4 |
| --- | --- |
| Before reaching checkpoint | Child, before `IsInside` resolves |
| Between reach and leave volumes | Child, before `IsOutside` resolves |
| After child return, during 30-second confirmation | Parent |
| After final completion | No first-run route; root guard bypasses |

The runtime protocol also streams away and returns while the child is active,
then tests completed reload, identical reinstall, and a second untouched clean
replay.

Use a save created before any Lab 4 candidate was installed. Changing files,
uninstalling, or writing `cqa004_completed = 0` in a console does not erase
save-backed journal, graph, mappin, world, or persistent-state history.

## Review before composition grows

Before adding another child or parallel branch, verify:

- every normal child route reaches an intentional output;
- every parent output has a continuation or deliberate terminal policy;
- all transient dependencies have cleanup owners;
- persistent writes occur before their route becomes unreachable;
- post-return parent work is distinguishable from active-child work;
- cut remains explicitly unsupported or has a tested policy;
- the exact version set, installed hashes, and clean-save provenance are
  recorded.

Previous: [Prefab dependencies](prefab-dependencies.md). Next: [Complex
cleanup, interruption, and
cancellation](cleanup-interruption-and-cancellation.md).
