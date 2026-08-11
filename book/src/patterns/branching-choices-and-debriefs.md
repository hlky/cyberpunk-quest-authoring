# Branching, choices, and debriefs

A choice is made in one state domain and consumed in another. Phone entries,
scene options, fact comparisons, switch cases, and graph joins are not aliases
for one generic “branch” node.

Tested with Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`,
RED4ext `1.30.0`, and redscript `0.5.31`. See [Tested
versions](../reference/tested-versions.md).

The practical rule is simple: observe the player's choice through the system
that owns it, write one durable outcome, and make downstream phases branch on
that outcome. Do not make a debrief rediscover a choice from presentation
state.

## Identify the branch domain

| Source of the decision | Observe it with | Persist it with | Do not substitute |
| --- | --- | --- | --- |
| Phone reply | Journal condition on the individual `gameJournalPhoneChoiceEntry` | `questSetVar_NodeType` on the winning route | Choice-group `Active` state |
| Scene option | Scene graph option/section routing, then a named questphase output or fact handoff | Fact writer immediately after the named result | Choice caption or embedded locstring ID |
| Current world/fact state | `questConditionNodeDefinition` for a snapshot, or a deliberate wait for later state | A result fact if later phases need the answer | A Pause Condition when an immediate false route is required |
| First satisfied asynchronous route | Parallel waits followed by a tested convergence node | Winner fact before convergence | The name “XOR” as proof that losing listeners are cancelled |
| N-way state selection | `questSwitchNodeDefinition` with case-bound conditions | Case-specific fact or phase | A chain of undocumented fall-through assumptions |

Read [Immediate branches and waiting gates](../gates/immediate-and-waiting.md)
before choosing Condition versus Pause Condition, and
[Signal flow](../gates/signal-flow.md) before adding AND, XOR, Hub, or Switch
nodes.

## State prerequisites

Define the outcome vocabulary before editing the graph:

- give each fact one stable meaning, such as `route_destroy_selected`;
- decide whether exactly one outcome, at least one outcome, or every outcome
  may be true;
- define the value domain—boolean `0/1`, an integer enum, or separate facts;
- reserve an explicit fallback for corrupt, missing, or legacy save state;
- decide where the choice becomes durable and where it becomes immutable;
- list every journal, scene, device, or world asset used only by one branch.

Separate boolean facts are easy to inspect but permit impossible combinations.
An integer outcome fact avoids that combination but requires conditions for
each supported value. Neither representation is safe without a clean-save and
reload matrix.

## Recipe: two mutually exclusive fact branches

The retained GQ002 choice gate normalizes two phone-choice facts into two
durable quest-outcome facts:

```text
In1
  +-> wait source_choice_a > 0 -> set outcome_a = 1 -> XOR In1 --+
  `-> wait source_choice_b > 0 -> set outcome_b = 1 -> XOR In2 --+
                                                        |
                                                   XOR Out1
                                                        |
                                                     Out1
```

| Node | Decisive properties |
| --- | --- |
| Each wait | `questPauseConditionNodeDefinition` → `questFactsDBCondition` → `questVarComparison_ConditionType` |
| Comparison | `comparisonType: Greater`, branch-specific `factName`, `value: 0` |
| Each write | `questFactsDBManagerNodeDefinition` → `questSetVar_NodeType`, branch-specific fact, `setExactValue: 1`, `value: 1` |
| Convergence | `questLogicalXorNodeDefinition`, `inputSocketCount: 2`, `outputSocketCount: 1`, sockets `In1`, `In2`, `Out1` |

Start both waits from the same input only when the source facts are guaranteed
to be mutually exclusive. In GQ002, the upstream phone group owned the choice
and wrote exactly one source fact. The gate then wrote a stable outcome fact
for later activity and debrief phases.

**Structurally validated:** the exact GQ002 phase and matching final-polish
build are kept in the
[provenance record](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence).
Its runtime section is
an active checklist; it does not record the two results. Both outcome routes,
XOR cancellation, simultaneous facts, and behavior under the pinned versions
remain **Experimental**. The serialized source reports WolvenKit `8.17.4`, not
a pinned `8.19.0` round trip. Add an acceptance case that deliberately seeds
both source facts; the graph should reject, guard, or route that impossible
state intentionally.

## Recipe: evaluate one optional outcome at a boundary

An optional condition often means “record success or failure when the main
activity reaches this boundary,” not “monitor continuously from activity
start.” One retained reduced fixture has this exact shape:

```text
In1
 -> objective Active
    +-> wait condition_fact > 0  -> set optional_success = 1 -> XOR In1 --+
    `-> wait condition_fact == 0 -> set optional_failure = 1 -> XOR In2 --+
                                                                     |
                                                                XOR Out1
                                                                     |
                                                     objective Succeeded
                                                                     |
                                                                  Out1
```

| Property | Exact retained value or boundary |
| --- | --- |
| Positive route | `questVarComparison_ConditionType`, `Greater`, value `0` |
| Zero route | `questVarComparison_ConditionType`, `Equal`, value `0` |
| Result writes | Separate exact-value fact setters |
| Convergence | Two-input, one-output logical XOR |
| Presentation | The fixture activates and later succeeds a journal objective; its serialized `optional` field is `0` |

The last point matters: the fixture's name does not prove an optional journal
presentation flag. If the objective should render as optional, author and test
that journal property separately.

**Structurally validated:** the reduced mod-owned phase passed handle
validation and a WolvenKit `8.17.4` deserialize/serialize round trip. It has no
retained in-game result and is not validation under WolvenKit `8.19.0`.

This shape also has a bounded value domain: a negative fact satisfies neither
wait and stalls. If negative values are possible, use an immediate
`questConditionNodeDefinition` with explicit `True` and `False` routes, or add
a deliberately tested third route. The immediate node form is **Observed in
vanilla** in
`base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase`;
the same retained phase also shows the contrasting wait form.

Do not use this boundary recipe for a live stealth bonus. A continuous monitor
must start beside the main activity and must have a stop/cut owner. See
[Monitors and cancellation](../gates/monitors-and-cancellation.md).

## Recipe: select one of N cases

`questSwitchNodeDefinition` binds condition items to numbered case sockets:

```text
In
 -> Switch First_Fulfilled
      Case101 -> persist outcome 101 -> case activity
      Case202 -> persist outcome 202 -> case activity
      Case303 -> persist outcome 303 -> case activity
      Otherwise -> explicit fallback
```

| Serialized part | Required relationship |
| --- | --- |
| `behaviour` | The retained vanilla switch uses `First_Fulfilled` |
| `conditions[]` | Each `questConditionItem` owns one condition handle and numeric `socketId` |
| `Case<socketId>` | Output socket paired with that condition item |
| `Otherwise` | Explicit additional output; connect it if missing state must not stall silently |
| `In` | The execution signal that asks the switch to evaluate |

**Observed in vanilla:** the switch with local ID `5`, nested beneath phase node
`252`, in
`base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase`
uses `First_Fulfilled`, three fact conditions, their case sockets, and an
unconnected `Otherwise` socket.

That file proves the shape, not evaluation order, short-circuit rules,
`All_Fulfilled`, save restoration, or what happens when several conditions are
true. Those behaviors are **Experimental**. For authoring:

1. make conditions exclusive whenever the narrative promises one outcome;
2. give each case a durable result write before branch-specific side effects;
3. connect `Otherwise` to a logged/recoverable fallback or explicit
   termination;
4. do not mutate conditions inside one case and expect undocumented
   fall-through;
5. test every case, no case, and multiple-true cases from named saves.

## Converge only after branch-owned effects

Convergence is where branch identity is most often lost too early. Keep this
order:

```text
choice owner
 -> observe winner
 -> persist winner
 -> perform branch-only journal/world/inventory effects
 -> converge
 -> perform exactly-once shared continuation
```

If both branches grant the same reward, converge before one common reward
node. If rewards differ, grant inside each branch, write a payout/result fact,
then converge after both branches' required effects. Never fan both routes
directly into two copies of the same common payout.

A graph-level AND is appropriate only when execution must wait for several
independent routes. When the requirement is “several predicates are true,” a
single Pause Condition with a Boolean AND tree is easier to reason about and
does not depend on partial signal-memory behavior. Vanilla AND, XOR, and Hub
topologies are **Observed in vanilla**; general arrival memory, cancellation,
and reload behavior remain **Experimental** unless the exact route has its own
runtime evidence.

## Carry a scene choice into the quest

Scene options belong to the scene's screenplay and embedded localization
store. Do not branch a questphase on the option's caption or locstring ID.
Instead:

1. route the option inside the `.scene`;
2. end each meaningful route through a named scene output, or write a
   scene-owned fact at a deliberate handoff;
3. expose matching sockets on the `questSceneNodeDefinition`;
4. write the durable quest outcome immediately after the named output;
5. converge only after branch-specific scene/quest effects are complete.

The single named-exit handoff taught by Lab 5 is **Structurally validated**.
The complete retained GQ000 route displayed five scene-choice labels and
continued through its acceptance route in a
[retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence);
that bounded
result is **Runtime-proven**. A generalized multi-exit custom scene remains
**Experimental** and belongs to the later advanced-scene campaign.

## Authoring procedure

1. Draw the player-facing alternatives and mark the system that owns each
   choice.
2. Allocate source-state and durable-outcome facts separately.
3. Add the smallest native condition or switch shape that represents the
   required timing.
4. Set every comparison, path, `socketId`, and socket count before connecting
   edges.
5. Write each outcome before any later phase can consume it.
6. Complete branch-owned journal, inventory, scene, device, or world effects.
7. Connect the convergence and exactly-once shared continuation.
8. Save, reopen, and inspect resolved source/destination sockets from both
   endpoints.
9. Round-trip a focused mod-owned resource with WolvenKit `8.19.0`; label that
   result **Structurally validated**, not **Runtime-proven**.

## Save and runtime matrix

Facts, phone choice state, scene state, journal entries, and active graph waits
can survive in a save. Test at least:

| Case | Required observation |
| --- | --- |
| Outcome A | Only A state/effects occur; shared continuation occurs once |
| Outcome B | Only B state/effects occur; shared continuation occurs once |
| Every additional switch case | Correct case socket, durable fact, and branch assets |
| No case true | `Otherwise` or documented fallback occurs |
| Multiple cases true | Deliberately specified result; no accidental duplicate continuation |
| Save before choice | Reload still presents a valid choice once |
| Save after source choice, before durable write | No lost or duplicated outcome |
| Save after durable write, before convergence | Correct branch resumes and shared effects occur once |
| Completed-save re-entry | No branch side effect or reward repeats |
| Replay from untouched save | First-run behavior remains reproducible |

Use a separate copy of the same untouched baseline for each route. A console
fact edit is useful for fault injection, but it is not clean-save evidence.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Wrong phone branch | Individual choice path, `Succeeded` state, and source fact write |
| Gate never leaves one branch | Fact name, comparison and value, whether the wait was started |
| Both branch effects occur | Mutual-exclusion invariant, stale save facts, losing listener, duplicate edges |
| Switch selects an unexpected case | Condition order, `socketId` to `Case<id>` mapping, multiple-true inputs |
| Switch stalls | Missing true condition and unconnected `Otherwise` |
| Optional result is never recorded | Negative/out-of-domain value, boundary never entered, or wrong result fact |
| Shared continuation runs twice | Convergence semantics, late listener, multiple incoming signals, absent one-shot guard |
| Correct choice but wrong debrief | Outcome was inferred again downstream instead of consuming the durable fact |

The evidence labels apply to exact scopes: the GQ002 two-route resource and
the older reduced optional fixture are **Structurally validated**, their
intended runtime behavior remains **Experimental**, and the cited switch and
condition shapes are **Observed in vanilla**. New branch combinations remain
**Experimental** until their own hash-bound runtime matrix passes.
