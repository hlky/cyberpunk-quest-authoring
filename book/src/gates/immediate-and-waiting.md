# Immediate branches and waiting gates

`questConditionNodeDefinition` and `questPauseConditionNodeDefinition` both own
a `condition` handle. Their surrounding graph contracts are different:

```text
immediate                         waiting

In                               In
 |                                |
 evaluate now                     hold this path
 +-- True  -> route A              |
 `-- False -> route B              `-- Out -> continue when fulfilled
```

Choosing between them is a behavior decision, not an editor-layout choice.

## Vanilla references

These focused base-game resources are useful comparisons. Extract them from
your own installation; they are references, not files to copy into the project.

```text
base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase
```

## Immediate condition: answer on entry

Execution entering `questConditionNodeDefinition` causes its predicate to
select a route. The focused vanilla shape has:

| Part | Role |
| --- | --- |
| `condition` | Handle to the leaf or logical predicate |
| `In` | Ordinary execution entry |
| `True` | Route selected when the predicate is fulfilled |
| `False` | Route selected when the predicate is not fulfilled |
| `CutDestination` | Separate interruption target; not another Boolean result |

The decisive property is the node class. When the predicate is false, the
node follows `False`; it does not remain active hoping that the value will
change.

A startup prerequisite can therefore reject or bypass work immediately:

```text
In
 -> is prerequisite ready?
      True  -> begin activity
      False -> unavailable route or termination
```

If the design instead says "start whenever the prerequisite becomes ready,"
this graph is incomplete. The `False` route needs some explicit retry owner,
or the predicate belongs under a waiting node.

## Pause condition: retain one execution path

`questPauseConditionNodeDefinition` receives an execution signal and delays
that path until its predicate is fulfilled. Its focused observed shape has:

| Part | Role |
| --- | --- |
| `condition` | Handle to the leaf or logical predicate |
| `In` | Starts this wait |
| `Out` | Continues after fulfillment |
| `CutDestination` | Target for an explicitly wired cut path |

There is no ordinary `False` continuation in this shape. A false predicate
means that this execution path has not yet produced `Out`.

That makes the node suitable for state gates such as:

- a fact reaching an authored value;
- the player satisfying a trigger predicate;
- a journal entry reaching a state;
- a real-time or game-time delay completing.

The nested payload defines *fulfilled*. [Condition payloads](condition-payloads.md)
shows the focused property shapes. A [Boolean condition tree](boolean-trees.md)
can combine several payloads beneath either surrounding node.

## The same predicate does not mean the same behavior

Suppose `signal_ready` currently equals `0` and later becomes `1`.

```text
questConditionNodeDefinition(signal_ready == 1)
```

selects `False` when the signal arrives at that moment. It has already made
its decision.

```text
questPauseConditionNodeDefinition(signal_ready == 1)
```

owns a waiting path whose intended release condition is the later fulfilled
comparison. Do not turn that explanation into unsupported scheduling claims:
the retained structure alone does not say how often the engine revisits the
predicate, what happens during a load screen, or whether a terminated phase
cleans up an active waiter.

## Author the node in WolvenKit

Use WolvenKit `8.19.0` and a mod-owned `.questphase`. The following procedure
describes the native resource shape; it does not require a generator or a
published vanilla asset.

1. Decide the behavior in plain language: **branch now** or **wait until**.
2. Add `questConditionNodeDefinition` for the first behavior, or
   `questPauseConditionNodeDefinition` for the second.
3. In the node's `condition` handle, create the wrapper that owns the intended
   state domain. For a fact comparison, that is `questFactsDBCondition` with a
   `questVarComparison_ConditionType` beneath `type`.
4. Set every decisive payload property. Do not leave a default fact name,
   journal path, NodeRef, comparison, or threshold unexplained.
5. Show unused sockets if necessary. Connect `In`, then both `True` and
   `False` for an immediate branch, or connect `In` and `Out` for a waiting
   gate.
6. Leave `CutDestination` unwired unless the activity has a designed and
   tested interruption owner.
7. Save the resource, reopen it, and verify the concrete node class, payload
   handle, socket names, and connected destination IDs.

For a structural record, serialize and round-trip the mod-owned resource, then
compare the focused node and edge set. A successful save is not runtime proof.

## One-shot activation is an immediate branch

A one-shot side effect needs persistent control state and an already-done
route:

```text
In
 -> started == 0?
      True  -> set started = 1 -> perform one-shot side effect
      False -> bypass the side effect
```

Facts are signed integers, even when `0` and `1` are used by convention. The
fact writer is a separate graph operation; the comparison does not change the
fact.

The book's mod-owned First Signal checkpoint uses
`cqa001_completed == 0` in this shape and is **Structurally validated** with
WolvenKit `8.19.0`. Its clean-save runtime evidence remains
**Experimental** — pending.

Place the write according to the invariant you need. If `started` means "do
not send the opening presentation twice," write it before or immediately with
that presentation. If `completed` means "the whole activity finished," write
it only on the completed route. When restart and completion differ, use
separate facts instead of overloading one value.

Writing a start guard early can suppress a retry after interruption; writing
it late can repeat the guarded side effect. That is a lifecycle trade-off to
test, not an ordering rule hidden inside the condition node.

This pattern is useful, but its re-entry safety is **Experimental** until the
exact graph is tested through repeated entry, save/load, and reinstall over a
completed save. An observed or structurally valid guard cannot promote a new
tutorial graph to **Runtime-proven** without those retained runtime cases.

## A waiting monitor is still active work

A graph output can start a normal activity and a pause condition in parallel:

```text
start
  +-> main activity
  `-> wait for failure fact -> fail optional objective
```

This is a monitor-shaped topology. It does not imply that success on the main
path cancels the listener. The vanilla street-story resource cited above
contains a parallel stealth-failure listener and later reads the stored result,
but contains no `CutSource` for that listener. That is **Observed in vanilla**
evidence for the shape, not automatic cleanup.

For every waiting path, name:

- who starts it;
- which predicate releases it;
- what output consumes the release signal;
- whether another route can make it irrelevant;
- how it is explicitly cut, completed, or made harmless;
- which save/reload and re-entry cases must be exercised.

An unwired `CutDestination` does not answer those questions.

## Save-backed facts change the first entry

A fact used by either condition node may already exist in the save. Installing
a new archive does not guarantee its authored comparison begins at zero.

Test at least these distinct cases for a one-shot or waiting fact gate:

1. an untouched save made before the mod was installed;
2. a save while the waiter is active;
3. a save after the releasing fact changed;
4. a completed save after reinstalling the identical build;
5. a replay from the original untouched save.

Record the archive and loose-file hashes with the save identity and logs. A
console fact edit is useful diagnosis, but it does not clear journal state,
active graph state, or other save-backed dependencies and therefore is not a
clean-save result.

## Diagnose the schedule before the payload

When a gate takes the wrong route or never releases:

1. Confirm the concrete node class: immediate Condition versus Pause
   Condition.
2. Trace the edge into `In` and every expected outgoing socket by node ID.
3. Inspect the concrete payload and its comparison instead of relying on the
   node caption.
4. Check the fact, journal path, NodeRef, or timer fields for the test save and
   installed build.
5. Determine whether the path was started once, more than once, or never.
6. Check whether a competing route completed without stopping this waiter.
7. Repeat the first-entry route from the original untouched save before
   changing the resource again.

That order separates a scheduling mistake from a malformed predicate, stale
save state, missing dependency, and unowned cleanup.
