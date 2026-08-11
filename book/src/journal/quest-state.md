# Journal state and tracking

A journal entry definition describes what an entry is. A quest graph decides
when that entry becomes active, inactive, succeeded, or failed. Visited state
and quest tracking are related presentation state, but they are not synonyms
for those lifecycle states.

This chapter applies that distinction to the exact Lab 1 nodes. Read
[Journal trees and typed paths](trees-and-paths.md) first if `realPath`,
`className`, or `fileEntryIndex` is unfamiliar.

## Definition versus runtime state

The Lab 1 journal defines three quest-lifecycle entries beneath its two
container entries:

```text
cqa001                         gameJournalQuest
└── cqa001_01                  gameJournalQuestPhase
    └── cqa001_01_obj_wait     gameJournalQuestObjective
```

Those objects do not carry the current save's active/succeeded state as an
authoring property. The questphase sends operations to their paths at runtime.

Important entry properties are still part of the definition:

| Entry type | Relevant authored properties |
| --- | --- |
| `gameJournalQuest` | `id`, `title.value`, `type`, `districtID`, `recommendedLevelID` |
| `gameJournalQuestPhase` | `id`, `locationPrefabRef` |
| `gameJournalQuestObjective` | `id`, `description.value`, `counter`, `optional`, `districtID`, `itemID`, `locationPrefabRef` |
| `gameJournalQuestDescription` | `id`, `description.value` |

Lab 1 leaves district, item, location, and prefab fields empty or zero. That is
not a hidden automatic setup: the lab has no world target, item counter,
description child, or map pin.

## The journal operation node

The graph node is `questJournalNodeDefinition`. Its `type` property holds a
node-type handle that supplies the target path and presentation options.

Lab 1 uses `questJournalQuestEntry_NodeType` with these properties:

| Property below `type` | Lab 1 value |
| --- | --- |
| `optional` | `0` |
| `sendNotification` | `1` |
| `trackQuest` | `1` |
| `version` | `Initial` |
| `path.editorPath` | empty string |
| `path.fileEntryIndex` | `2` |

Another common payload is `questJournalEntry_NodeType`. It contains `path` and
`sendNotification`, but not the quest-specific tracking, optional, or version
fields.

Do not infer a target entry's class from this payload type alone.
**Observed in vanilla:** some phone-message nodes use
`questJournalQuestEntry_NodeType`, while other working flows use the simpler
`questJournalEntry_NodeType`. Inspect the whole node, its sockets, path, and
surrounding presentation intent.

## The incoming socket selects the operation

The same node type and journal path can request different states. The incoming
socket is decisive:

| Input socket | Requested journal operation |
| --- | --- |
| `Active` | Make the target active |
| `Inactive` | Make the target inactive |
| `Succeeded` | Mark the target succeeded |
| `Failed` | Mark the target failed |

The node then emits `Out`. `CutDestination`, when present, belongs to
interruption routing and is not another journal state.

Not every serialized node retains every unused state socket. Use WolvenKit's
**Show Unused Sockets** command when constructing the graph, and confirm the
specific sockets required by the flow before connecting it.

## Lab 1's exact state sequence

Lab 1 uses four separate nodes so each transition is explicit:

| Node ID | Target | Incoming socket | Result |
| ---: | --- | --- | --- |
| `11` | `quests/minor_quest/cqa001` | `Active` | Activate the quest |
| `12` | `quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait` | `Active` | Activate the objective |
| `14` | same objective path | `Succeeded` | Succeed the objective after the delay |
| `16` | `quests/minor_quest/cqa001` | `Succeeded` | Succeed the quest |

The successful flow is:

```text
activate quest
  -> activate objective
  -> wait ten real-time seconds
  -> succeed objective
  -> set cqa001_completed = 1
  -> succeed quest
  -> terminating output
```

IDs `12` and `14` intentionally share the same payload path. Their different
incoming sockets make them different operations. Editing the objective's
journal definition cannot substitute for the missing `Succeeded` edge.

The completion fact is also separate from journal success. Setting
`cqa001_completed` gives the one-shot guard persistent control state; it does
not automatically mark the quest succeeded. Conversely, succeeding the quest
does not set that authored fact.

See [Configure the journal operations](../start-here/lab-01-authoring.md#ids-11-12-14-and-16-journal-operations)
and [connect every socket](../start-here/lab-01-authoring.md#7-expose-and-connect-every-socket)
for the click-by-click authoring procedure.

## State, visited, and tracked are separate

Treat these as separate questions:

| Dimension | Example question | How it is addressed |
| --- | --- | --- |
| Lifecycle state | Is the objective active or succeeded? | Journal-node state socket or state condition |
| Visited state | Did the player open or select the entry? | `questJournalEntryVisited_ConditionType` |
| Tracking | Is this quest selected for tracker/navigation presentation? | `trackQuest` on a journal operation plus runtime UI state |
| Notification | Was a presentation request sent for this operation? | `sendNotification` on the node payload |

Activating a phone choice group does not prove that one choice was selected.
Activating a message does not prove that the player opened it. Marking an
objective succeeded does not prove that the quest is still tracked.

For a state condition, use:

```text
questJournalCondition
└── type                         questJournalEntryState_ConditionType
    ├── path                     gameJournalPath
    ├── state                    Succeeded
    └── inverted                 0
```

For a visited condition, use:

```text
questJournalCondition
└── type                         questJournalEntryVisited_ConditionType
    ├── path                     gameJournalPath
    └── visited                  1
```

Both condition payloads require the same full typed path discipline described
in the previous chapter. A condition can be used beneath an immediate
condition node or a wait-until node; that surrounding graph node determines
whether the graph samples now or pauses for a later change.

## Presentation flags are requests, not proof

`sendNotification: 1` requests presentation for the journal operation.
`trackQuest: 1` requests tracking behavior where that node/entry combination
supports it. Neither flag proves what the player actually saw.

Presentation depends on more than the two booleans:

- the target entry family and requested state;
- whether its parent entries are available;
- whether localization resolves;
- current tracking and mappin state;
- timing relative to adjacent journal operations;
- state already retained in the save.

Legacy runtime evidence also showed that activating an onscreen entry made it
available in the journal without producing an obvious item-acquisition
notification. Do not generalize one entry family's presentation to another.

For Lab 1, preserve the exact flags in the supplied checkpoint, but keep the
presentation claims synchronized with the acceptance record that captures the
objective text, notification behavior, tracking, and final Completed
presentation.

## Completion is an ordered lifecycle

A robust success path makes every side effect explicit:

```text
finish the player action
  -> succeed the active objective
  -> perform any reward or cleanup
  -> set the authored completion fact
  -> succeed the quest
  -> terminate the phase
```

Lab 1 has no reward or cleanup dependency, so its shorter order is deliberate.
Later chapters add those operations without pretending that quest journal
success grants a reward or cleans world state automatically.

There is no universal placement for every quest's reward, cleanup, or
completion fact. State the invariant for that flow, then test interruption and
reload at the boundaries where partial completion would matter.

**Observed in vanilla:** the following phase contains multiple objective
journal nodes, phone-message presentation, mappin changes, and a separate
reward manager in one larger lifecycle:

`base\open_world\street_stories\watson\kabuki\sts_wat_kab_05\phases\sts_wat_kab_05_openworld.questphase`

Extract it from your own game and inspect focused nodes; do not copy the whole
resource or assume its street-story orchestration belongs in a minimal quest.

## Save-backed behavior

Journal state is stored in the save. Installing a changed `.journal` or
`.questphase` does not rewind an entry that was already activated, visited,
succeeded, failed, or tracked.

Lab 1's acceptance matrix therefore separates:

1. activation from a manual save created before the first install;
2. saving and reloading while the delay and objective are active;
3. reloading after quest success;
4. reinstalling the identical build over the completed save;
5. replaying from the untouched pre-install save.

Record the exact archive hash, loose ArchiveXL-file hash, save identity, and
fresh logs with the observations. A fact reset can help isolate one branch,
but it does not clear journal state and cannot promote a test to clean-save
evidence.

## Failure checks

If a transition does not appear:

1. Confirm the edge enters the intended state socket, especially `Active`
   versus `Succeeded`.
2. Confirm `type.path.realPath`, `className`, and `fileEntryIndex` resolve to
   the supplied journal entry.
3. Confirm the journal resource and its ArchiveXL registration loaded before
   diagnosing graph timing.
4. Check whether the entry was already changed in the test save.
5. If state changes but text is blank, compare the journal localization key
   with the onscreen `secondaryKey`.
6. If text appears but tracking or notification differs, record that outcome
   separately rather than reporting the entire journal operation as failed.
7. Repeat the first-run case from the original pre-install save before changing
   the resource again.

These checks preserve the difference between a missing resource, a bad typed
path, a wrong graph socket, a localization failure, and stale save state.
