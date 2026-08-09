# Rewards and completion

A reward, a completion fact, successful journal presentation, and phase
termination are four independent graph effects. A complete quest connects all
the effects it needs in an intentional order; none is implied by another.

| Record | Value |
| --- | --- |
| Chapter review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Lab 1 completion path | **Structurally validated**; runtime status is shown by the dedicated marker below |
| Native reward reference | **Observed in vanilla** |
| Reward-to-completion sequence | **Runtime-proven** in a retained legacy fixture, not in one fully bound pinned-book run |

**Lab 1 runtime evidence:** **Experimental** — pending.

> **Evidence boundary:** the native reward node shape below is a focused
> vanilla observation. The complete ordering was exercised successfully by a
> retained quest fixture, but that run does not promote this book's pinned
> baseline or Lab 1 to runtime-proven. Custom TweakDB reward-record authoring is
> outside this chapter and remains deferred.

## Four effects, four owners

| Intended effect | Native graph shape | What it does not do |
| --- | --- | --- |
| Grant payout | `questRewardManagerNodeDefinition` containing `questGiveReward_NodeType` | Does not set a completion fact, update the journal, or end execution |
| Persist one-shot completion | `questFactsDBManagerNodeDefinition` containing `questSetVar_NodeType` | Does not pay the player or change visible quest state |
| Show the quest as succeeded | `questJournalNodeDefinition` containing `questJournalQuestEntry_NodeType`, entered through `Succeeded` | Does not guarantee a reward or prevent root re-entry |
| End this phase route | `questOutputNodeDefinition` with `type: Terminating` | Does not mutate the fact, journal, or inventory |

An objective's `Succeeded` state is separate from the containing quest's
`Succeeded` state as well. Use socket connections to establish execution order;
screen position in WolvenKit is not evidence of flow. See
[Graph execution](../foundations/graph-execution.md).

## Exact native reward shape

The reward manager's `type` handle contains the operation, and the operation's
`rewards[]` array contains `TweakDBID` values:

```text
questRewardManagerNodeDefinition
├── sockets: In, Out, CutDestination
└── type
    └── questGiveReward_NodeType
        └── rewards[]
            └── TweakDBID: QuestRewards.my_quest_completion
```

A focused CR2W-JSON property excerpt looks like this. Handles and sockets are
omitted only to keep the ownership visible:

```json
{
  "$type": "questRewardManagerNodeDefinition",
  "type": {
    "Data": {
      "$type": "questGiveReward_NodeType",
      "rewards": [
        {
          "$type": "TweakDBID",
          "$storage": "string",
          "$value": "QuestRewards.my_quest_completion"
        }
      ]
    }
  }
}
```

The node resolves a record that must already exist in TweakDB. A structurally
correct node with a misspelled or absent record can still fail to produce the
intended payout. Defining the `QuestRewards.*` record, its money, experience,
items, and notification behavior is a separate TweakDB authoring task and is
not taught here.

### Reproduce the vanilla observation

Extract this exact depot path from your own installed archives into a
disposable WolvenKit inspection project:

```text
base\open_world\street_stories\watson\kabuki\sts_wat_kab_05\phases\sts_wat_kab_05_openworld.questphase
```

In the focused retained extraction, reward node ID `4` is a
`questRewardManagerNodeDefinition`; its nested type is
`questGiveReward_NodeType`, and `rewards[]` contains the string-backed
`TweakDBID` `QuestRewards.sts_wat_kab_05_completion`. That shape is
**Observed in vanilla**, not a claim that node ID `4` or that reward record is
appropriate for another quest.

The retained reference reported game resource version `2310` and was
serialized for inspection with WolvenKit 8.17.4. Re-extract from the pinned
Cyberpunk 2077 `2.31a` installation and inspect it with WolvenKit 8.19.0 before
depending on the current shape. Follow [Inspect a vanilla questphase](../start-here/inspecting-vanilla.md),
retain only focused notes and hashes, and do not ship the cooked phase or a
complete JSON serialization.

## A known-good completion order

The retained full quest fixture uses this sequence:

```text
wait until the final phone message is visited
  -> grant QuestRewards.<quest>_completion
  -> set <quest>_completed exactly to 1
  -> enter the quest journal node through Succeeded
  -> enter a Terminating output
```

Its concrete operation families are:

| Step | Node and decisive property |
| ---: | --- |
| 1 | `questPauseConditionNodeDefinition` → `questJournalCondition` → `questJournalEntryVisited_ConditionType`, with the final message's `gameJournalPath` and `visited: 1` |
| 2 | `questRewardManagerNodeDefinition` → `questGiveReward_NodeType.rewards[]` |
| 3 | `questFactsDBManagerNodeDefinition` → `questSetVar_NodeType`, with the completion fact, `setExactValue: 1`, and `value: 1` |
| 4 | `questJournalNodeDefinition` → `questJournalQuestEntry_NodeType`, connected to the `Succeeded` input socket for the quest path |
| 5 | `questOutputNodeDefinition`, `type: Terminating` |

This ordering is **Runtime-proven** for the retained legacy fixture. It is a
strong completion pattern, not a universal requirement that every quest end
with a phone message. Replace the first gate with the final player-facing event
your quest actually requires, but do not let an asynchronous scene, message,
or interaction continue after you have declared the route complete unless
that behavior is intentional and tested.

### Why this order is not atomic

The chain is a sequence of graph operations, not one transaction:

- granting the reward before writing the completion fact avoids a state where
  the one-shot guard suppresses a payout that has not happened yet;
- a save or interruption after the reward but before the fact can instead
  expose a duplicate-payout window on re-entry;
- writing the fact before quest journal success prevents a later root
  evaluation from replaying the normal route, but an interruption can leave
  the visible journal in an intermediate state;
- termination ends the current path only after the persistent and visible
  effects have been requested.

There is no universally safe order without considering re-entry, checkpoints,
and whether the reward operation is idempotent. Treat the sequence above as a
known-good starting point and run interruption tests at every boundary that
can be saved. If the quest can enter completion twice through parallel routes,
join or guard those routes before the reward node rather than hoping the final
fact write will deduplicate them.

## Reconcile Lab 1

[Lab 1: First Signal](../start-here/lab-01.md) intentionally has no reward
record and no reward manager. Its ending is:

```text
succeed the objective
  -> set cqa001_completed exactly to 1
  -> succeed quests/minor_quest/cqa001
  -> terminate
```

That is not an incomplete reward example; it is a smaller lifecycle example
whose promised outcome contains no payout. Its fact write, quest success, and
termination remain separate for the same reason described above. The Lab 1
graph is **Structurally validated**, while its clean-save, mid-flow reload, and
completed-reload behavior are governed by the pinned acceptance record.

To add a payout in a later lab, first create and validate a quest-owned
`QuestRewards.*` record through the future TweakDB procedure. Then insert the
reward manager before the completion fact and repeat the entire save matrix.
Do not point Lab 1 at the named vanilla record or copy the vanilla phase.

## Failure checks by owner

| Symptom | Inspect first |
| --- | --- |
| Reward node runs but no payout appears | Exact `TweakDBID`, existence and contents of the reward record, node `In`/`Out` connections, and runtime logs |
| Payout appears but the quest stays active | Quest journal path, `className`, `fileEntryIndex`, and connection to the quest node's `Succeeded` socket |
| Quest succeeds but restarts on a later load | Completion fact name/value, root one-shot condition, and whether the fact write is reachable before termination |
| Quest stops changing before the payout | Final wait condition, especially visited versus merely active journal state |
| Payout occurs twice | Parallel completion routes, reward-to-fact interruption window, checkpoint resume point, and save provenance |
| Journal succeeds but the graph remains active | Connection from the journal node's `Out` socket to a `Terminating` output |
| Objective succeeds but quest does not | Confirm there are distinct objective and quest journal nodes and that both receive the intended state |

Do not diagnose a missing TweakDB record by changing journal state, and do not
diagnose a bad journal path by duplicating the reward node. Each test should
isolate one owner.

## Verification and save boundary

For a payout-bearing completion route:

1. structurally inspect the reward node, its nested operation, every reward
   `TweakDBID`, and the connected socket pair;
2. verify the completion fact has one meaning and the root guard reads that
   same fact;
3. verify objective success, quest success, and termination are distinct
   connected operations;
4. start from a pre-install save and record inventory, money, experience, fact,
   journal state, and logs before and after completion;
5. test a save before the final presentation gate, after the reward if the game
   permits it, after the fact write, and after termination;
6. reload the completed save and prove the quest neither reactivates nor pays
   again;
7. return to the original clean save for the next first-run test.

Facts, journal states, visited flags, graph checkpoints, scenes, communities,
and device persistent state can all survive in a save. A console fact reset is
not a clean replay and cannot establish one-shot correctness. Use
[Facts, journals, and saves](../foundations/persistent-state.md) and
[Install, test, and reset](../start-here/install-and-test.md), and bind the
archive hashes, exact versions, save provenance, and retained logs to the test
record before changing an **Experimental** claim to **Runtime-proven**.
