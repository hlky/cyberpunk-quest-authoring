# Parallel monitors and cancellation

A monitor is a graph route that begins alongside the main route and waits for
an event that may or may not occur. Typical uses include optional-objective
failure, combat escalation, leaving an area, a device state change, or a timer
expiring.

The pattern is powerful because questphase outputs can have several
connections. It is also dangerous: the route you stop caring about may still
be alive unless the resource explicitly makes a later signal harmless or cuts
the target.

## Start independent routes

An ordinary `Out` socket can connect to more than one destination:

```text
Activate optional objective
  Out -> wait for failure fact
      -> wait for stop condition
      -> continue main route
```

The three connections represent three independent downstream routes. A Hub is
not required merely to express the split.

**Observed in vanilla:** a nested graph in
`base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase`
starts a main trigger wait and a stealth-objective branch from a shared journal
output. The objective branch starts a Pause Condition for
`jpn_03_stealth_fail == 1`; later, an immediate Condition reads the same stored
fact. The phase contains no `CutSource` wiring.

That proves a parallel-listener topology. It does not prove automatic cleanup
when the objective succeeds, cleanup on phase exit, save/load restoration, or
one-shot emission.

## Store the outcome before converging

When two branches can decide one objective, keep their journal writes mutually
exclusive and record the result explicitly:

```text
failure listener -> optional Failed -----------------> race input 1
stop listener    -> optional Succeeded -> success fact -> race input 2
```

Do not let both branches write success and failure facts after they converge.
The convergence node is a routing boundary, not proof that the losing producer
has been destroyed.

Lab 2 follows this rule. Each branch owns one optional-objective outcome, and
the main completion route begins only after their XOR-shaped convergence. Its
default and source-edited variants exercise different producers without
installing two competing test writers in the same graph.

## XOR is not a cancellation instruction

Vanilla contains race-shaped XOR convergence, including three independent
alert/combat waits in:

```text
base\open_world\street_stories\watson\northside_industrial_district\
sts_wat_nid_03\phases\sts_wat_nid_03_gameplay.questphase
```

**Observed in vanilla:** all three waits enter one
`questLogicalXorNodeDefinition`, then its single output reaches a fact setter.
There are no cut edges from that XOR to the waits.

Therefore the safe statement is “these routes converge through an XOR-typed
node.” The following claims remain **Experimental**:

- first arrival is always the only emitted result;
- losing listeners are cancelled;
- simultaneous arrivals have deterministic priority;
- a later signal cannot retrigger the output;
- race state survives or resets predictably across save/load.

If correctness depends on any of those claims, test it directly and retain the
evidence.

## Explicit cut topology

`questCutControlNodeDefinition` owns ordinary `In`/`Out` sockets plus a
`CutSource`. Selected targets expose `CutDestination`. Vanilla resources wire
the cut source directly to those destinations.

**Observed in vanilla:** the retained corpus contains 50 Cut Control nodes and
75 `CutSource`→`CutDestination` edges; 45 target Pause Condition nodes.

A compact example appears in:

```text
base\open_world\minor_activities\watson\northside\
ma_wat_nid_15\ma_wat_nid_15_phase.questphase
```

Pause node 225 is a character-killed listener. Cut Control node 236 has a cut
edge to that listener's `CutDestination`.

A larger cross-targeted bank appears in:

```text
base\open_world\street_stories\watson\northside_industrial_district\
sts_wat_nid_02\phases\sts_wat_nid_02_ow.questphase
```

There, four Cut Controls cross-target four active Pause Conditions.

These shapes establish **explicit target wiring**, not the complete runtime
contract. Raw data and generated class definitions do not prove whether a cut
rolls back state, emits the target's ordinary output, propagates downstream,
persists in a save, permits later re-entry, or how `permanent` changes the
operation. Treat those effects as **Experimental**.

## Two safe strategies

### Make a late signal harmless

Prefer this when the listener can remain active without cost:

1. Store the authoritative outcome in a fact.
2. Gate every journal or world-state writer on that outcome.
3. Make repeated or losing signals bypass the writer.
4. Terminate the containing route cleanly.
5. Test the late-signal case explicitly.

This strategy does not assert cancellation. It makes correctness independent
of cancellation.

### Cut a named target deliberately

Use this only when runtime acceptance has established the required cut
behavior:

1. Identify the exact listener nodes whose lifecycle must end.
2. Connect a Cut Control's `CutSource` to each target's `CutDestination`.
3. Decide and record the intended `permanent` setting.
4. Test both outcomes, both arrival orders, and simultaneous completion.
5. Save with every target active, then reload and repeat.
6. Re-enter the containing phase and verify whether the target can arm again.

Do not copy a large vanilla cut bank as a template. Extract the relevant phase,
trace the focused socket edges, and recreate only the topology your own test
can defend.

## Phase exit is not evidence of cleanup

A terminating output proves that a route reaches the phase interface. It does
not, by itself, prove that every independent listener, delay, scene, or world
operation started earlier has been cancelled.

Before allowing a phase to terminate, inventory its outstanding work:

| Work that may still be active | Required decision |
| --- | --- |
| Pause Condition | Remain harmless, satisfy, or explicitly cut |
| Realtime/game-time delay | Ignore late output, gate it, or cut after testing |
| Scene | Map every exit and interruption outcome |
| Community/world spawn | Despawn or transfer ownership deliberately |
| Device persistent-state write | Define restoration and clean-save behavior |

Later chapters add the resource-specific lifecycle rules. At the graph level,
the principle is already fixed: every parallel route needs an owner and an end
condition.

## Monitor acceptance matrix

For each monitor/race pair, retain at least:

| Case | Required observation |
| --- | --- |
| Main route wins | Optional outcome and final quest state are correct |
| Monitor wins | Failure/escalation outcome and final quest state are correct |
| Near-simultaneous signals | Exactly the behavior the design relies on |
| Late losing signal | No second or contradictory journal/world write |
| Save with both armed | Reload completes or restores without duplication |
| Completed-save reload | No listener reactivation |
| Clean replay | Both variants still work from separate untouched saves |

Bind the record to exact installed files, versions, saves, and logs before
promoting a claim to **Runtime-proven**.
