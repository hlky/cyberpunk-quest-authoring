# Conditions and gates

A condition answers a question about game state. A gate decides when that
question is asked and what execution signal leaves afterward. Keeping those
jobs separate is the foundation of reliable quest control flow.

"Continue when the player has arrived" can mean at least three different
things:

- sample the arrival state now and choose `True` or `False`;
- hold this execution path until the arrival state is fulfilled;
- combine arrival with other predicates before either of those graph nodes
  acts.

Those are different native resource shapes. A visually similar graph can
therefore have different runtime behavior.

## Evidence and inspection baseline

| Record | Value |
| --- | --- |
| Section review date | 2026-08-09 |
| Reader inspection target | Cyberpunk 2077 `2.31a` Windows archives |
| Reader inspection tool | WolvenKit `8.19.0` |
| Retained research corpus | 41 vanilla `.questphase` resources |
| Corpus serialization | WolvenKit `8.17.4`; CR2W header game resource version `2310` |

> **Evidence boundary:** the native classes and focused depot-path examples in
> this section are **Observed in vanilla**. They were counted in a retained
> research extraction and should be re-extracted from your own pinned game
> installation before being treated as current. A new mod-owned graph is only
> **Structurally validated** after it survives serialization, round-trip, and
> graph checks. Timing, cancellation, save/load, and re-entry behavior remain
> **Experimental** until a hash-bound runtime acceptance run covers them.

The corpus contains 262 immediate condition nodes and 797 pause condition
nodes. That frequency is useful evidence that both shapes matter; it is not a
claim that every quest uses them in the same lifecycle.

**Lab 2 runtime evidence:** **Experimental** — pending.

The downloadable Signal Race CR2W resources are **Structurally validated**
with pinned WolvenKit `8.19.0`. The dedicated marker above remains
**Experimental** until both candidates and all six required executions have
hash-bound runtime evidence.

## Three layers, three questions

Trace a gate from the outside in:

```text
execution signal
      |
      v
graph node: evaluate now or wait?
      |
      v
condition object: which state is being tested?
      |
      v
leaf payloads and Boolean composition
```

Then trace outward again through named sockets. The three layers answer
different questions:

| Layer | Native examples | Question |
| --- | --- | --- |
| Evaluation schedule | `questConditionNodeDefinition`, `questPauseConditionNodeDefinition` | Is the predicate sampled on entry, or does this path wait? |
| Predicate | `questFactsDBCondition`, `questTriggerCondition`, `questJournalCondition` | What piece of game state counts as fulfilled? |
| Predicate composition | `questLogicalCondition` containing child conditions | Must all, any, or some other combination of child predicates be fulfilled? |

Graph-level logical nodes are a fourth, separate concern: they receive
execution signals through sockets. A `questLogicalCondition` does not merge
graph edges, and a graph-level AND or XOR does not inspect facts by itself.
Using the same English words for both layers is convenient, but the serialized
types reveal which contract actually applies.

## Choose the native shape from the behavior

| Intended behavior | Starting shape | Essential caution |
| --- | --- | --- |
| Decide between two routes using current state | Immediate condition node | `False` is an output route, not a request to wait |
| Continue this route after a predicate is fulfilled | Pause condition node | Do not assume how it polls, saves, cancels, or re-arms |
| Require several state predicates together | Logical condition tree beneath either node | This combines truth values, not execution signals |
| Prevent a one-shot effect from running again | Immediate fact guard plus an explicit persistent fact write | The save may already contain either value |
| Watch for failure while other work continues | A separately activated waiting path | Starting a listener does not define how it is stopped |
| Accept one of several arriving graph signals | Graph topology, not a nested condition tree | Winner, cancellation, and tie behavior require their own evidence |

The table is a design router, not a copy-paste recipe. Every row still needs an
explicit entry edge, exit edge, lifecycle owner, and evidence plan.

## Read this section in order

| Chapter | Question it answers |
| --- | --- |
| [Immediate branches and waiting gates](immediate-and-waiting.md) | When does a condition run, and which sockets continue the graph? |
| [Condition payloads](condition-payloads.md) | How do fact, trigger, distance, journal, and time predicates represent state? |
| [Boolean condition trees](boolean-trees.md) | How are leaf predicates nested under AND or OR, and why is there no generic NOT recipe? |
| [Signal flow](signal-flow.md) | How do graph-level AND, XOR, Hub, and Switch shapes route execution signals? |
| [Delays and persistence](delays-and-persistence.md) | Which clock and save-state questions must a delayed route answer? |
| [Parallel monitors and cancellation](monitors-and-cancellation.md) | How can a side listener remain harmless or be explicitly cut? |
| [Condition-family catalog](condition-catalog.md) | Which additional native condition families were observed, and what still needs research? |
| [Lab 2: Signal Race](lab-02.md) | How do immediate selection, parallel waits, a Boolean AND, and XOR-shaped convergence fit in one project? |
| [Author Signal Race](lab-02-authoring.md) | Which native properties and 22 socket edges reproduce the supplied graph? |
| [Test both routes](lab-02-test.md) | How are two source variants, clean saves, hashes, logs, and outcomes kept distinct? |

Start with the node schedule. A perfectly authored fact comparison still
behaves incorrectly if it sits under the wrong surrounding graph node.

## Inspect evidence without redistributing it

Use a disposable WolvenKit project for vanilla research:

1. In the Asset Browser, locate the exact depot path named by a chapter.
2. Open it without adding it to a distributable project, or add it only to a
   separate local inspection project.
3. Record the graph-local node ID, concrete node class, `condition` payload,
   socket names, and focused connected edges.
4. Record the game version, WolvenKit version, extraction date, and optionally
   a local hash.
5. Keep the extracted `.questphase` and any complete CR2W-JSON serialization
   out of the book and downloadable examples.

The depot path is provenance. It is not a dependency to package, and the
surrounding vanilla quest is not a template whose local facts, NodeRefs, or
journal paths can be copied into a new mod.

## State is not an event sequence

Many predicates describe state: a fact has a value, a journal entry has a
state, or an actor is inside an area. Even when a payload enum contains words
such as `Entered` or `Exited`, the enum name alone does not establish its exact
edge timing, persistence, or replay behavior.

Ordered behavior comes from explicit execution edges:

```text
wait for A
  -> wait for B
  -> perform C
```

Putting A and B in one AND tree asks whether both predicates are fulfilled for
one condition evaluation. It does not record that A happened first. Starting
two waiters in parallel likewise does not establish which will emit first or
whether the losing path will stop.

## Claims this section deliberately does not make

The retained structures do not by themselves prove:

- polling frequency or short-circuit order;
- automatic cleanup when a phase terminates;
- timer behavior through pause menus, loading, time skip, fast travel, or
  save/load;
- deterministic resolution when several signals become ready together;
- reset, exactly-once, or re-arm behavior after interruption;
- a universal Boolean NOT node;
- that a numeric distance threshold is measured in metres.

Those questions are runtime acceptance cases. Keep them **Experimental** until
the exact resource build, installation, save state, route, and observation are
retained together.
