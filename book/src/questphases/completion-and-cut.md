# Completion and interruption

A phase is complete only when execution reaches the intended output and its
owner has performed the required cleanup. The last visible objective update is
not an implicit return.

## Normal completion

Lab 1's normal route is:

```text
succeed objective
  -> set cqa001_completed = 1
  -> succeed quest
  -> terminating output Out1
```

Each edge matters. If termination moved before the fact write, the write would
be unreachable. If the completion fact were omitted, later root evaluation
would have no durable one-shot guard.

The exact best ordering depends on the intended recovery policy. It must be
tested at save boundaries rather than inferred from a successful uninterrupted
run.

## Child completion is a two-sided contract

For a child:

```text
child route -> child output "Out1"
                       |
                       v
parent phase node emits "Out1" -> parent continuation
```

Review both resources. A terminating child output with no matching parent
socket cannot convey the intended result. A matching socket with no outgoing
parent connection conveys the result and then goes nowhere.

With several outcomes, cleanup can differ by route:

| Outcome | Example responsibility before return |
| --- | --- |
| `accepted` | Close meeting UI, preserve acceptance fact, release temporary setup |
| `declined` | Inactivate meeting objective and marker, preserve decline policy |
| `failed` | Stop success monitor, apply failure presentation, release encounter |
| `cut` | Stop active work and leave save state in an intentional recovery state |

Outcome names here illustrate a design contract; use names proven for the
specific node/resource arrangement you author.

## Termination is not cleanup

Reaching a `questOutputNodeDefinition` does not, by itself:

- inactivate objectives or mappins;
- deactivate a community;
- stop a scene or parallel monitor;
- reset a device's persistent state;
- clear a completion fact;
- choose what a parent does next.

Every acquired transient dependency needs an owner and release boundary.
Persistent progression should remain only because the re-entry design calls
for it.

## Cut sockets

Many quest nodes expose a `CutDestination` socket. Its presence identifies an
interruption surface; it does not supply a correct interruption policy.

Before wiring a cut route, answer:

1. What work may be active when the cut arrives?
2. Which child phase or scene must receive interruption?
3. Which journal entries become inactive, failed, or resumable?
4. Which communities, markers, devices, and monitors must be released?
5. Which durable fact distinguishes cut from normal completion?
6. Which output tells the parent cleanup is finished?

The Lab 1 structure contains unwired `CutDestination` sockets.
**Experimental:** this book does not claim cut-safe behavior for Lab 1 until an
interruption fixture and expected recovery state are defined.

## Re-entry after termination

Termination ends an execution route, not the lifetime of all save-backed
state. When a root is evaluated again, its policy must choose among:

| Policy | Required evidence |
| --- | --- |
| One-shot | Completed route runs once; later entry takes the already-done route |
| Resume | Saves taken at supported boundaries return to the intended stage |
| Retry | Failure/cut cleanup restores exactly the state needed for another attempt |
| Repeat | Reset or cooldown prevents overlap and restores repeatable inputs |

For Lab 1, test at minimum:

1. first run from a clean save;
2. save/reload while the delay is active;
3. reload after completion;
4. reinstall over a save where `cqa001_completed == 1`;
5. removal/reinstallation behavior only if the guide intends to support it.

Record journal state and the fact value for each case. Visual success alone
does not prove that the one-shot invariant survived the save.

## Review before composition grows

Before adding another child or parallel branch, verify:

- every normal route reaches an intentional output;
- every parent output has a continuation or deliberate terminal policy;
- all transient dependencies have cleanup owners;
- persistent writes occur before their route becomes unreachable;
- cut remains explicitly unsupported or has a tested policy;
- the tested version set and clean-save conditions are recorded.

This keeps phase composition reviewable when later chapters add gates, world
references, scenes, and parallel failure monitors.
