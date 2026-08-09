# Lifecycle, cleanup, and evidence

Quest authoring is lifecycle design. The happy path is only one transition
through a system that can be saved, reloaded, interrupted, re-entered, or
installed over older state.

## A complete activity lifecycle

A focused activity usually has these responsibilities:

```text
activation
  -> dependency readiness
  -> player-facing work
  -> outcome capture
  -> presentation completion
  -> cleanup
  -> handoff or termination
```

The owner of an activated dependency should also define when it is released.
Examples include:

- deactivate a community after the player leaves a safe boundary;
- hide or inactivate a mappin when its objective ends;
- stop a parallel failure monitor after success;
- return a named scene outcome before terminating its child phase;
- leave persistent facts intact when they are the intended re-entry guard.

Cleanup is not synonymous with resetting everything. Completion facts and
journal history may intentionally persist while transient actors, markers, and
monitors stop.

## Completion ordering

Ordering is observable:

```text
succeed objective
  -> set completion fact
  -> succeed quest
  -> terminate
```

Moving the fact earlier may prevent recovery from a partial run. Moving it
after termination may make it unreachable. Setting the quest succeeded before
its objective can produce confusing presentation.

There is no universal ordering for every quest. State the intended invariant,
then test interruption at the boundaries that matter.

## Re-entry policy

Every root or repeatable activity needs an explicit policy:

| Policy | Required control |
| --- | --- |
| One-shot | Persistent completion guard and a terminating already-done route |
| Resume | Save-safe stage state and a route back into the correct activity |
| Retry after failure | Failure cleanup plus a deliberate reset boundary |
| Repeatable | State reset, cooldown or activation gate, and protection from overlapping runs |

“The graph starts at its input” does not answer what should happen when saved
state says some of its work is already active.

## Cut and interruption

A cut path is a different outcome, not a shortcut to the normal final node.
Before wiring it, decide:

- which scenes or child phases receive interruption;
- which objectives fail, become inactive, or remain resumable;
- which communities, devices, or markers remain valid;
- which facts distinguish interruption from success;
- whether the parent terminates, retries, or chooses another branch.

Complex interruption is introduced only after the normal lifecycle is
runtime-proven. A guessed cleanup route can be more destructive than leaving
an experimental socket unwired.

## The validation ladder

Each check proves a different claim:

| Check | What it proves | What it does not prove |
| --- | --- | --- |
| WolvenKit save or CR2W deserialization | The editor/converter accepted the serialized structure | Runtime references and behavior |
| CR2W round trip | Important structure survives binary serialization | That the game can execute it |
| Handle and graph validation | References, nodes, sockets, and edges are internally consistent | External resource existence |
| Archive packing and path listing | Intended CR2W payloads entered the archive at known depot paths | Loose framework files were installed |
| ArchiveXL log registration | The framework saw and registered configured resources | Player-facing behavior |
| Focused runtime route | The tested behavior occurred in one environment and save state | Reload, interruption, or replay safety |
| Clean-save acceptance matrix | The documented lifecycle cases pass from controlled state | Compatibility with untested versions |

“WolvenKit saved it” and “the archive packed” are therefore intermediate
evidence, not completion.

## Evidence labels

Use the narrowest label supported:

- **Runtime-proven:** exercised successfully in the game in the documented
  arrangement.
- **Structurally validated:** serialized, round-tripped, and inspected, but not
  yet proven in game in that arrangement.
- **Observed in vanilla:** present in one or more cited vanilla resources.
- **Experimental:** investigation or runtime acceptance is incomplete.

A page can contain several labels. For example, a node shape may be observed in
vanilla, its mod-owned copy structurally validated, and its new lifecycle still
experimental.

## Test record

A reproducible runtime claim should record:

- Cyberpunk, WolvenKit, ArchiveXL, RED4ext, and other relevant versions;
- archive and loose-resource hashes;
- the exact installed depot paths;
- the starting save and why it is clean for this test;
- the expected route and observed result;
- relevant ArchiveXL, redscript, and game logs;
- whether normal completion, reload, interruption, and replay were tested;
- hypotheses rejected during isolation.

Changing several resources and declaring the last edit causal is not controlled
evidence. Reduce the candidate, preserve known-good baselines, and change one
boundary at a time.

## Foundation checkpoint

Before proceeding to a lab, be able to explain:

1. which resource owns every referenced object or string;
2. how execution enters and leaves every node;
3. the type and domain of every identifier;
4. which state can already exist in the save;
5. who owns cleanup and termination;
6. which validation step supports each claim.

If one answer is “the template handles it,” the resource has not yet been
explained.
