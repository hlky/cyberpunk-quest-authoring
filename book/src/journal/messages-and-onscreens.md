# Messages, files, emails, and onscreens

Phone threads and journal-backed computer documents are journal content. A
questphase can activate entries and wait for their state, while a device can
expose a journal file or email through its persistent controller. A controller
can also own inline document content with no journal path. Neither consumer
creates the other resource automatically.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Authoring target | [Pinned first-release versions](../reference/tested-versions.md) |
| Native hierarchies and property shapes | **Observed in vanilla** |
| New custom phone/device arrangement | **Experimental** until its own hash-bound clean-save acceptance run passes |

This chapter teaches the journal-side contracts. Building a computer's world
node, instance package, persistent controller, and component CRUID bindings is
deferred to [World integration](../world/index.md). A reader does not need a
generator, manifest compiler, console mod, or extracted vanilla asset to use
the model below.

## Three consumers, three responsibilities

```text
questphase
  -> journal state nodes
     -> contact / conversation / message / choice entries

computer persistent controller
  -> filesStructure or mailsStructure
     -> journalPath
        -> gameJournalFile or gameJournalEmail

optional readable item record
  -> secondary action journalEntry
     -> gameJournalOnscreen
```

The shared journal resource owns entry identity and localized fields.
Questphases own ordering. Devices own menus, content slots, and read events.
Optional item records own inventory presentation. Onscreen localization owns
the final UI strings.

Do not infer one chain from another. Activating a `gameJournalFile` does not
populate an empty device controller, and putting a journal path in a controller
does not make a questphase wait for the resulting fact.

## Phone thread hierarchy

The journal tree for a text exchange is:

```text
gameJournalContact
└── gameJournalPhoneConversation
    ├── gameJournalPhoneMessage
    └── gameJournalPhoneChoiceGroup
        └── gameJournalPhoneChoiceEntry
```

The containing contact is the `gameJournalFileEntry` for phone paths. For a
path such as `contacts/cqa_contact/cqa004_offer/...`, use
`fileEntryIndex: 1`: component `1` is `cqa_contact`. It is not the index of a
message in the conversation.

### Contact and conversation properties

| Type | Exact properties used by this model |
| --- | --- |
| `gameJournalContact` | `id`, `avatarID`, `name.value`, `type`, `isCallableDefault`, `useFlatMessageLayout`, `entries` |
| `gameJournalPhoneConversation` | `id`, `title.value`, `entries` |

`avatarID` is a `TweakDBID`; `name.value` and `title.value` are localization
lookups. A text-only contact observed in the retained resources uses
`type: Texter` and `useFlatMessageLayout: 1`. Those values describe that shape,
not a rule that every callable or holocall contact must use them.

### Message and choice properties

| Type | Property | Meaning |
| --- | --- | --- |
| `gameJournalPhoneMessage` | `id` | Entry ID used in the full journal path |
|  | `sender` | Sender role, for example `NPC` in the cited thread |
|  | `text.value` | Onscreen localization key or vanilla localization reference |
|  | `delay` | Presentation delay setting for the message |
|  | `attachment` | Optional attachment; `null` in the simple cited messages |
|  | `imageId` | Optional image `TweakDBID`; `0` in the simple cited messages |
|  | `isQuestImportant` | Quest-importance presentation flag |
| `gameJournalPhoneChoiceGroup` | `id`, `entries` | Container activated when the player should receive response options |
| `gameJournalPhoneChoiceEntry` | `id`, `text.value` | One player response and its label |
|  | `isQuestImportant` | Quest-importance presentation flag |
|  | `questCondition` | Optional condition controlling availability; `null` in the simple cited choice |

Do not reuse a vanilla `LocKey#...` as mod-owned text. Create globally unique
onscreen localization keys and register the mod-owned localization resource.

## Activate content, then wait for the correct state

A retained simple phone flow uses `questJournalNodeDefinition` with a
`questJournalEntry_NodeType` payload.

| Field | Message example | Choice-group example |
| --- | --- | --- |
| `type.path.className` | `gameJournalPhoneMessage` | `gameJournalPhoneChoiceGroup` |
| `type.path.realPath` | Full path to one message | Full path to one group |
| `type.path.fileEntryIndex` | `1` for a contact path | `1` for a contact path |
| `type.sendNotification` | Whether this activation should notify | Whether this activation should notify |

That payload shape exposes `CutDestination`, `Active`, `Inactive`, and `Out`.
Enter through `Active` to make the entry available. `Out` continues the graph
after the state request; it does not mean that the player read a message or
selected a reply. Some vanilla phone nodes instead use
`questJournalQuestEntry_NodeType` and retain additional state sockets; inspect
the actual payload and socket inventory before reproducing a flow.

A two-way exchange therefore has two distinct kinds of wait:

```text
activate opening message(s)
  -> activate choice group
  -> wait for choice A state Succeeded ----> activate reply A --+
  -> wait for choice B state Succeeded ----> activate reply B --+-> final message
                                                            -> wait final message visited
```

For choice selection, place `questJournalEntryState_ConditionType` beneath a
`questJournalCondition` in a `questPauseConditionNodeDefinition`:

| Property | Value |
| --- | --- |
| `path.className` | `gameJournalPhoneChoiceEntry` |
| `path.realPath` | Full path to the individual choice, not the group |
| `path.fileEntryIndex` | `1` for the containing contact |
| `state` | `Succeeded` |
| `inverted` | `0` for the direct condition |

For acknowledgement of the final message, use
`questJournalEntryVisited_ConditionType` with the final
`gameJournalPhoneMessage` path and `visited: 1`. Both pause-condition nodes use
the normal `CutDestination`, `In`, and `Out` sockets.

These state dimensions are not synonyms:

- `Active` means the entry was made available;
- a choice entry's `Succeeded` state means that choice won;
- a message's `visited` value records that the player visited/read it.

Waiting only for activation can pay a reward or finish a quest before the
player sees the response. Conversely, waiting for `visited` on an entry the UI
never exposes can stall the phase permanently.

## A small vanilla phone reference

**Observed in vanilla:** extract your own copy of
`base\journal\cooked_journal.journal` and inspect:

```text
contacts/dex/q003_flathead_price
```

The conversation contains, in order:

```text
gameJournalPhoneMessage       q003_01_msg_flathead_price
gameJournalPhoneChoiceGroup   q003_02_ch_understood
└── gameJournalPhoneChoiceEntry q003_02a_understood
gameJournalPhoneMessage       q003_03_msg_good_luck
```

It is a compact proof of the hierarchy and fields: the first message has
`sender`, `text`, `delay`, `attachment`, `imageId`, and
`isQuestImportant`; the choice carries `text`, `isQuestImportant`, and a null
`questCondition`; the following message has its own delay. It does not by
itself prove the questphase that activates a new custom thread.

## Onscreen, file, and email families

The `onscreens` primary journal branch contains several leaf families:

| Group | Leaf | Player-facing fields on the leaf |
| --- | --- | --- |
| `gameJournalOnscreenGroup` | `gameJournalOnscreen` | `title.value`, `description.value`, `tag`, `iconID` |
| `gameJournalFileGroup` | `gameJournalFile` | `title.value`, `content.value`, `pictureTweak`, `videoResource` |
| `gameJournalEmailGroup` | `gameJournalEmail` | `sender.value`, `addressee.value`, `title.value`, `content.value`, `pictureTweak`, `videoResource` |

`tag` is a `CName`; `iconID` and `pictureTweak` are `TweakDBID` values; and
`videoResource` is a resource reference. Leave optional media values empty
when the design does not use them. Do not copy a vanilla movie, image record,
or localized text into a mod-owned resource.

For a path shaped like:

```text
onscreens/emails/quests/minor_quest/cqa004/files/diagnostic
```

the containing `gameJournalFileGroup` is `files`, component `5`, so the
`gameJournalPath.fileEntryIndex` is `5`. The same rule applies to an email or
onscreen group at that position. Count the component contributed as the
containing file entry; do not count handles or the leaf.

## The SQ021 computer boundary

SQ021 is the useful vanilla reference because its journal content, device
controller, world instance, and quest reaction can be separated precisely.

Extract these resources yourself in a disposable WolvenKit project:

```text
base\journal\cooked_journal.journal
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
base\worlds\03_night_city\_compiled\default\exterior_19_-8_0_0.streamingsector
base\gameplay\devices\masters\computers\laptop_1.ent
```

The active journal-backed file is **Observed in vanilla** at:

```text
onscreens/emails/quests/side_quest/sq021_sick_dreams/
sq021_randy_files/01_cartoon
```

It is a `gameJournalFile`. The sibling email group is:

```text
onscreens/emails/quests/side_quest/sq021_sick_dreams/sq021_randy
```

The laptop controller consumes those entries. The decisive property chains
are:

```text
computerSetup.filesStructure[].content[].journalPath
computerSetup.mailsStructure[].content[].journalPath
gamedeviceDataElement.questInfo.factName
```

Opening the `01_cartoon` device element sets
`sq021_randy_pc_file_cartoon`. A nested branch in
`sq021_randys_room.questphase` waits for that fact, temporarily sends
`ToggleUIInteractivity(false)` to `ComputerManager`, runs the corresponding
scene input, clears the fact, and restores interaction. The quest reacts to
the click; it does not create the Files tab or inject the journal entry.

Likewise, `filesMenu: 1` does not produce a Files tab when `filesStructure` is
empty. The SQ021 controller holds actual file content. Its retained shape has
an inline representation and a journal-backed representation in separate
controller chunks. Treat that as an **Observed in vanilla** device shape, not
as permission to copy SQ021's controller package.

## Why device construction is deferred

The SQ021 sector binds node-local persistent controller data to
`laptop_1.ent` through component CRUIDs. A computer can render, animate, and
offer `Use` while silently falling back to the entity template's empty
controller when those IDs do not match.

That is a world/device ownership problem. This chapter establishes only the
journal-facing requirements:

1. the journal entry exists and is registered;
2. the controller has non-empty content;
3. its `journalPath` resolves to the expected leaf type;
4. the device element owns the intended `questInfo.factName`;
5. the quest waits for that fact separately.

A global `.devices` or `.psrep` entry was not required for the cited SQ021
Files UI. A custom registry entry may still be needed when a quest addresses a
device through device-manager operations. Neither observation is a universal
device-construction recipe.

## Readable onscreens and the optional item layer

Activating a `gameJournalOnscreen` can make it available in the Journal, but a
retained legacy probe did not produce an obvious pickup presentation from that
activation alone.

An optional readable item can point its secondary `Read` action's
`journalEntry` at the onscreen path. That gives inventory acquisition and a
route into the same journal content, but it introduces TweakXL and item-record
authoring. TweakXL is not required for phone threads or computer files, and it
is not a hidden prerequisite of this chapter. Defer that layer to a dedicated
readable-item guide rather than presenting a copied record as magic.

## Save-backed state

Phone entry state, message `visited` state, journal content, questphase waits,
and device persistent state can all be stored in a save. Removing the mod or
resetting one completion fact does not restore a clean phone thread or device.

For first-run acceptance, use a save created before the custom journal and
device identity were installed. Keep it untouched. Make separate saves before
a choice, after a chosen reply, and after the final message. When materially
changing a persistent device package, use a new `NodeRef` or a save that has
never streamed the old identity; an older save can restore copied controller
content that no longer exists in the source.

## Verification and failure routing

Test one ownership boundary at a time:

| Symptom | First boundary to inspect |
| --- | --- |
| Contact or thread never appears | ArchiveXL journal registration, contact ID, full path, `className`, and `fileEntryIndex` |
| Opening message appears but choices do not | Choice-group activation through `Active`, then its exact journal path |
| Both replies appear | Separate `Succeeded` conditions and branch-to-reply wiring |
| Quest advances before the player reads the final message | `Active` was treated as `visited`, or the final visited wait is absent |
| Phone text is blank | Journal `text.value` versus registered onscreen localization keys |
| Computer has no Files tab | Empty `filesStructure`, wrong persistent controller, or component CRUID mismatch; `filesMenu` alone is insufficient |
| File opens but the quest does not advance | `gamedeviceDataElement.questInfo.factName`, then the quest's fact condition |
| Journal-backed file is blank | Leaf type/path mismatch, `fileEntryIndex`, journal registration, or localization lookup |
| Removed emails or files return on one save | Save-backed device persistent state; retry with a fresh identity or pre-stream save |
| Readable entry exists but no pickup appears | Direct journal activation was mistaken for inventory-item presentation |

For phone tests, retain which choice succeeded and whether the final message
became visited. For device tests, retain the exact world identity, journal
path, read fact, installed resource hashes, framework logs, and starting save.
Repeat after reload and from a clean replay save before assigning causality to
an edit.
