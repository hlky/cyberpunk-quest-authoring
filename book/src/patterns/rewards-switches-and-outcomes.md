# Rewards, switches, and outcomes

An outcome, its debrief, its payout, journal success, and phase termination are
independent effects. Compose them in an explicit order and preserve the
outcome before presentation begins.

Tested with Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`,
RED4ext `1.30.0`, and redscript `0.5.31`. See [Tested
versions](../reference/tested-versions.md).

Use [Rewards and completion](../journal/rewards-and-completion.md) for the
reward node's full property shape and
[Branching, choices, and debriefs](branching-choices-and-debriefs.md) for
two-way and n-way branch construction. This page covers their composition.

## Resource prerequisites

An outcome-dependent ending can cross several resource systems:

| Resource | Required content |
| --- | --- |
| Questphase | Outcome conditions, branch-specific effects, convergence, reward manager, completion fact, journal success, terminating output |
| Journal | Debrief contact/thread/messages or a debrief objective, plus the quest and objective entries being completed |
| Onscreen localization | Every debrief message, reply, objective, and completion-facing string |
| Reward record | A valid `QuestRewards.*` TweakDB record authored and tested separately |
| Optional scene/audio | `.scene`, actor/context binding, subtitles, VO map, WEMs, lipsync, and named outputs for a voiced debrief |
| World/community/device state | Explicit cleanup or stable completed state before the ending claims completion |

The reward node references a TweakDB record; it does not define the payout.
Do not copy a vanilla reward record or assume a correctly spelled ID exists.
If the quest needs a custom record, use a separately documented TweakDB
authoring path and record that tool's exact tested version. Custom reward-record
creation is outside this page and remains **Experimental** for this book's
pinned release.

## Persist outcome before the debrief

Write the durable result at the event that owns it:

```text
player choice / combat result / device result
 -> set durable outcome
 -> finish branch-owned world and journal effects
 -> clean or stabilize active gameplay systems
 -> start debrief
```

The debrief consumes state; it should not invent it. A phone choice's visited
flag, a scene caption, an NPC's current hostility, or the presence of one
message is fragile presentation/runtime state. A named fact gives later phases
one explicit contract and survives a resource boundary.

When several facts represent exclusive outcomes, validate that exactly one is
positive before the debrief. When an integer fact represents an enum, connect
an explicit unknown-value fallback. Old saves and interrupted writes can
otherwise route the wrong presentation or stall forever.

## Recipe: grant one standalone reward

The native operation is deliberately small:

```text
In
 -> questRewardManagerNodeDefinition
      -> questGiveReward_NodeType
           -> rewards[] = QuestRewards.my_quest_completion
 -> Out
```

| Property | Contract |
| --- | --- |
| `type` | Populated handle containing `questGiveReward_NodeType` |
| `type.rewards[]` | One or more string-backed reward `TweakDBID` values |
| sockets | `In`, `Out`, and the separate `CutDestination` |
| external dependency | Every named reward record already exists and has the intended contents |

**Observed in vanilla:** extract
`base\open_world\street_stories\watson\kabuki\sts_wat_kab_05\phases\sts_wat_kab_05_openworld.questphase`
from your own installation. In the retained focused reference, top-level phase
node `5` owns an embedded `phaseGraph`; local node `4` inside that graph is the
reward manager whose nested operation names
`QuestRewards.sts_wat_kab_05_completion`. This proves that resource shape, not
permission to reuse its record or either graph-local node ID.

A standalone payout still needs a one-shot owner:

```text
reward_claimed == 0?
  False -> already-paid continuation
  True  -> grant reward
         -> set reward_claimed = 1
         -> continuation
```

This ordering has an interruption window between grant and fact write. Writing
the fact first creates the opposite window, in which re-entry can suppress an
ungranted payout. There is no automatic transaction. The new arrangement is
**Experimental** until saves on both sides of the boundary, completed-save
reload, and repeated entry are tested.

## Recipe: outcome-dependent text debrief

The retained GQ002 ending uses common context, one outcome-specific opening,
then a shared response group and completion chain:

```text
debrief objective Active
 -> 1-second realtime pacing delay
 -> common message 1 Active
 -> common message 2 Active
    +-> wait outcome_destroy > 0 -> destroy message Active --+
    `-> wait outcome_spoof   > 0 -> spoof message Active   --+
                                                             |
                                                    XOR convergence
                                                             |
                                                  response group Active
                       +-> wait reply A Succeeded -> reply A --+
                       `-> wait reply B Succeeded -> reply B --+
                                                             |
                                                    XOR convergence
                                                             |
                                                   final message Active
                                             -> 1-second pacing delay
                                             -> objective Succeeded
                                             -> reward
                                             -> set quest_completed = 1
                                             -> quest Succeeded
                                             -> Out1
```

| Stage | Native owner |
| --- | --- |
| Outcome selection | Two `questPauseConditionNodeDefinition` fact waits and a two-input `questLogicalXorNodeDefinition` |
| Message presentation | `questJournalNodeDefinition` → `questJournalEntry_NodeType`, entered through `Active` |
| Player response | One `questJournalEntryState_ConditionType` per individual choice, `state: Succeeded` |
| Objective/quest presentation | Separate `questJournalQuestEntry_NodeType` nodes and state sockets |
| Payout | `questRewardManagerNodeDefinition` → `questGiveReward_NodeType` |
| Durable completion | `questSetVar_NodeType`, exact value `1` |

**Structurally validated:** the exact GQ002 debrief phase and matching
final-polish build are kept in the
[provenance record](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence).
Its runtime section is
the active next-test checklist and lists the expected branch, reply,
completion, payout, and cleanup results. It does not retain those results.
Both outcome-specific openings, both final response routes, payout, and
no-lingering-state behavior remain **Experimental** for that candidate. Its
serialized source reports WolvenKit `8.17.4`; this is not a pinned `8.19.0`
round-trip result.

The exact retained phase uses a one-second realtime delay after activating its
final message. That is a presentation-pacing choice, not proof that the player
read the message. If acknowledgement is a design requirement, replace that
boundary with the visited-state recipe below and test the changed graph. Do not
silently relabel the GQ002 candidate as an acknowledged-message result.

## Recipe: require acknowledgement before payout

The retained GQ000 completion route places a visited gate before its common
ending:

```text
wait final debrief message visited
 -> grant QuestRewards.<quest>_completion
 -> set <quest>_completed exactly to 1
 -> enter quest journal node through Succeeded
 -> Terminating output
```

| Step | Exact node family |
| ---: | --- |
| 1 | `questPauseConditionNodeDefinition` → `questJournalCondition` → `questJournalEntryVisited_ConditionType`, final `gameJournalPhoneMessage` path, `visited: 1` |
| 2 | `questRewardManagerNodeDefinition` → `questGiveReward_NodeType.rewards[]` |
| 3 | `questFactsDBManagerNodeDefinition` → `questSetVar_NodeType`, `setExactValue: 1`, `value: 1` |
| 4 | `questJournalNodeDefinition` → `questJournalQuestEntry_NodeType`, entered through `Succeeded` |
| 5 | `questOutputNodeDefinition`, `type: Terminating` |

**Runtime-proven:** a
[retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
completed the GQ000 route with phone choices, completion presentation,
and the expected reward after its final-message gate.

That legacy result and the GQ002 outcome-specific debrief are separate
artifacts. Combining GQ002-style outcome openings with GQ000-style visited
completion is a strong design, but the combined graph is **Experimental**
until one exact archive and save matrix prove it.

## Same reward versus branch-specific rewards

When every outcome earns the same payout, converge first and keep exactly one
reward node:

```text
case A effects --+
case B effects --+-> convergence -> common reward -> completion
case C effects --+
```

When outcomes earn different payouts, keep the payout inside each branch and
converge afterward:

```text
Case101 -> reward A -> set payout_a_done = 1 --+
Case202 -> reward B -> set payout_b_done = 1 --+-> common journal success
Otherwise -> no-payout/fallback result --------+
```

Each case must still persist its narrative outcome before reward delivery.
Keep payout facts separate if interrupted saves must distinguish “outcome was
selected” from “reward was granted.” Never connect several case outputs to
duplicated copies of an identical common reward merely to simplify layout.

The native reward node is **Observed in vanilla**, and a three-case switch is
**Observed in vanilla** in
`base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase`.
The branch-specific reward composition above has no retained custom runtime
campaign and remains **Experimental**.

## Text debrief versus voiced debrief

Use a journal phone conversation when the ending is text. Use a `.scene` when
the debrief is performed dialogue. A voiced phone call also needs explicit
phone start/end state; see
[Messages, calls, and conversations](messages-calls-and-conversations.md).

For a scene debrief, replace the final-message gate with the exact named scene
result that means the dialogue completed normally:

```text
questSceneNodeDefinition named normal result
 -> reward
 -> completion fact
 -> journal success
 -> terminate
```

Do not pay on scene start, `Holocall INT`, a nonterminal section output, or an
interruption route unless that is the authored outcome. Map rejection,
interruption, and reload to explicit non-paying or recovery paths. The book's
Lab 5 has one **Structurally validated** named scene handoff, but it has no
reward and does not prove this debrief composition. A new voiced payout route
is **Experimental**.

## Cleanup before declaring completion

Completion presentation should match the remaining runtime state. Before the
debrief or final success, decide who owns:

- community deactivation and surviving actor cleanup;
- device disablement or completed persistent state;
- active mappin and objective removal;
- scene normal/interrupted cleanup;
- temporary inventory removal;
- still-running waits, monitors, and losing choice routes.

The GQ002 retained checklist requires no lingering objective, marker, actor, or
interaction at completion. It is an acceptance target, not a result; that
behavior remains **Experimental** for the named archive. Its graph assigns
cleanup to earlier phases rather than implying quest success cleans those
systems automatically.

## Manual authoring order

1. Write the outcome table: source event, durable fact/value, debrief content,
   payout, cleanup, and fallback.
2. Author and register all journal/localization content, then verify its full
   typed paths.
3. Validate each `QuestRewards.*` record independently from the quest graph.
4. Add outcome conditions or a switch and persist the selected result before
   presentation.
5. Wire branch-specific debrief messages/scenes and side effects.
6. Converge at the latest common point; put a shared reward after convergence
   or distinct rewards before it.
7. Add the required final gate: visited message, named normal scene output, or
   another explicitly player-facing completion signal.
8. Connect reward, completion fact, objective/quest success, cleanup, and
   termination as distinct nodes in the intended order.
9. Reopen the resource and inspect every handle, socket, journal path,
   condition, fact, and reward ID.
10. Round-trip the mod-owned phase with WolvenKit `8.19.0`, then run every
    outcome from separate copies of one untouched save.

## Acceptance matrix

| Case | Required evidence |
| --- | --- |
| Every narrative outcome | Correct debrief content and no content from another branch |
| Every final response | Correct reply, one continuation, intended acknowledgement behavior |
| No/unknown outcome | Explicit fallback; no indefinite hidden wait |
| Before debrief save | Correct outcome presentation after reload |
| After branch message/scene start | No wrong branch, duplicate content, or lost phone/scene state |
| Before reward | Reload pays exactly once when completion continues |
| Immediately after reward | Reload does not duplicate payout or suppress required completion state |
| Completed save | No debrief, reward, objective, marker, actor, device action, or root route repeats |
| Clean replay | Same archive reproduces first-run behavior from the original untouched save |

Capture the exact archive, loose ArchiveXL files, TweakDB inputs, framework
versions, save IDs, before/after money-XP-inventory state, relevant facts,
journal states, and fresh logs. A fact-only reset cannot clear phone, scene,
journal, community, or device persistence.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Correct outcome but wrong debrief | Durable outcome write, mutually exclusive values, switch/case mapping |
| Both outcome messages appear | Losing wait, impossible dual facts, stale save, convergence wiring |
| Final message appears but completion stalls | Visited path/class/index, named scene output, or deliberate pacing gate |
| Reward node runs with no payout | Reward record existence/content, exact `TweakDBID`, framework logs |
| Reward repeats | Multiple completion routes, interruption window, missing payout/completion guard |
| Quest succeeds before dialogue finishes | Activation or pacing signal was mistaken for acknowledgement/normal scene completion |
| Quest completes with actors or marker present | Cleanup owner is absent or ordered after termination |
| One old save routes differently | Saved outcome, journal, scene, community, or device state; return to the untouched baseline |

Use the evidence labels literally: the exact GQ000 completion candidate is
**Runtime-proven** for its bounded recorded result, the GQ002 debrief candidate
is **Structurally validated** while its intended behavior remains
**Experimental**, and the cited base-game node shapes are **Observed in
vanilla**. New reward/debrief combinations remain **Experimental** until their
exact acceptance records pass.
