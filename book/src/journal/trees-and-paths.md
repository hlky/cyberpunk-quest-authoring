# Journal trees and typed paths

A `.journal` resource defines entries in the game's merged journal tree. A
questphase does not contain those entries. It addresses them through a typed
`gameJournalPath` and asks the journal system to change their runtime state.

This chapter explains the resource and lookup contract behind the journal
portion of [Lab 1](../start-here/lab-01.md#journal-tree). State transitions are
covered in [Journal state and tracking](quest-state.md).

## Evidence and tested boundary

The manual paths in this chapter target this baseline:

| Component | Version |
| --- | --- |
| Cyberpunk 2077 for Windows | `2.31a` (GOG) |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Review date: **2026-08-09**.

**Lab 1 runtime evidence:** **Experimental** — pending.

- **Structurally validated:** the supplied Lab 1 journal has the CR2W root,
  handle tree, descriptor, entry types, IDs, and ArchiveXL registration shown
  here. Its questphase paths resolve against that tree.
- **Runtime evidence:** the dedicated marker above mirrors the canonical Lab 1
  acceptance record. Structural validity alone does not prove that a new
  journal merge and localized presentation work in game.
- **Observed in vanilla:** the focused vanilla trees named below were observed
  in base-game resources. Extract them from your own installation; this book
  does not redistribute them.

The retained vanilla research predates one fully bound version record. Treat
its shapes as inspection evidence, then compare them with resources extracted
from the pinned `2.31a` installation before relying on a version-sensitive
detail.

## The ownership chain

Four different addresses participate in the Lab 1 lookup:

```text
mod\cqa\cqa001\journal\cqa001.journal       depot resource
  -> quests/minor_quest/cqa001               journal path
     -> cqa_cqa001_title                     localization key
        -> First Signal                      localized text
```

The depot path identifies a CR2W file. The journal path identifies an entry
inside the merged journal tree. The localization key identifies text in a
separately registered onscreen resource. None of these identifiers can replace
another.

The questphase owns the operation. The journal owns the target entry. The
onscreen localization resource owns the player-facing text. ArchiveXL registers
the three resources with their respective roots.

## The journal resource root

Create and edit the journal as a CR2W resource in WolvenKit's property tree.
Do not make raw CR2W-JSON editing the authoring workflow.

The Lab 1 resource begins with this native shape:

```text
gameJournalResource
└── entry                                  gameJournalRootFolderEntry
    └── entries[]                         journal entry handles
```

Set these root properties:

| Property below `RootChunk` | Lab 1 value | Purpose |
| --- | --- | --- |
| `cookingPlatform` | `PLATFORM_PC` | Cooking target recorded by the resource |
| `entry` | `gameJournalRootFolderEntry` handle | Root of this contributed tree |
| `entry.id` | default/not serialized in the checkpoint | The root itself is not a named path component |
| `entry.descriptor.DepotPath` | `base\journal\descriptor.journaldesc` | Soft reference to the vanilla journal descriptor |
| `entry.descriptor.Flags` | `Soft` | Reference-loading policy used by the validated resource |
| `entry.journalEntryOverrideDataList` | default/not serialized in the checkpoint | No tutorial overrides on the root |

`base\journal\descriptor.journaldesc` is a vanilla depot reference. Cite or
inspect it; do not add the extracted file to the tutorial project.

## Containers and leaf entries

Journal paths come from the `id` values of nested entries. Container types own
an `entries` array; leaf types hold the data consumed by a particular UI or
quest system.

The exact Lab 1 chain is:

```text
gameJournalRootFolderEntry                 id: omitted/default
└── gameJournalPrimaryFolderEntry          id: quests
    └── gameJournalFolderEntry             id: minor_quest
        └── gameJournalQuest               id: cqa001
            └── gameJournalQuestPhase      id: cqa001_01
                └── gameJournalQuestObjective
                                            id: cqa001_01_obj_wait
```

The resulting leaf path is:

```text
quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait
```

There is no path component for the anonymous root entry. There is also no
extra wrapper folder around `quests`. Adding one changes every path below it.

For the full property table, follow
[Author the journal tree](../start-here/lab-01-authoring.md#3-author-the-journal-tree).
That procedure deliberately leaves district, item, marker, and prefab fields
empty because Lab 1 owns no world content.

## Register the contribution

The file's presence in `source\archive` is not enough. ArchiveXL must merge it
into the game journal:

```yaml
journal:
- mod\cqa\cqa001\journal\cqa001.journal
```

The value is the cooked depot path beneath `source\archive`, not a Windows
filesystem path and not the generated `.journal.json` review artifact beneath
`source\raw`.

Lab 1 keeps this entry beside its root-questphase and onscreen-localization
registrations in `CQA_Lab01_OneShot.archive.xl`. See
[the complete registration block](../start-here/lab-01.md#registration).

**Structurally validated:** Lab 1 uses this ArchiveXL `1.27.0` `journal`
section shape, and repository validation requires the registered depot path to
match the supplied resource. The canonical runtime record remains the
authority for whether the merge was accepted by the pinned game process.

## `gameJournalPath` is a typed lookup

A quest node does not point at a CR2W handle. It carries a
`gameJournalPath` handle with four fields:

| Property | Meaning |
| --- | --- |
| `realPath` | Slash-separated IDs from the merged journal tree |
| `className` | `CName` describing the intended target entry type |
| `fileEntryIndex` | Zero-based component index of the containing `gameJournalFileEntry` |
| `editorPath` | Editor-facing path text; Lab 1 leaves it empty |

Lab 1's objective target is:

| Property | Value |
| --- | --- |
| `realPath` | `quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait` |
| `className` | `gameJournalQuestObjective` |
| `fileEntryIndex` | `2` |
| `editorPath` | empty string |

Use the exact target type in tutorial-owned paths. **Observed in vanilla:**
some vanilla nodes contain legacy or less-specific `className` values, so the
field should not be used to infer the target when inspecting an unfamiliar
resource. Verify the entry at `realPath` instead of copying a surprising
vanilla value into a new mod.

## How to calculate `fileEntryIndex`

Several journal entry families derive from `gameJournalFileEntry`. During
journal-tree traversal, `fileEntryIndex` records the zero-based depth of the
nearest containing file entry. The registered CR2W can begin above it: Lab 1
starts with an anonymous `gameJournalRootFolderEntry`, then reaches the
containing `gameJournalQuest` inside the logical path.

Count from zero:

```text
0: quests
1: minor_quest
2: cqa001        <- gameJournalQuest, the containing file entry
3: cqa001_01
4: cqa001_01_obj_wait
```

Therefore every Lab 1 path at or below `cqa001` uses `2`, including the quest
itself and its objective.

Other common families demonstrate why the value is not always `2`:

| Example path | Containing file-entry type | `fileEntryIndex` |
| --- | --- | ---: |
| `contacts/example_contact/...` | `gameJournalContact` at component 1 | `1` |
| `points_of_interest/minor_quests/...` | `gameJournalPointOfInterestGroup` at component 1 | `1` |
| `onscreens/emails/quests/minor_quest/example/files/...` | `gameJournalFileGroup` at component 5 | `5` |
| `onscreens/emails/quests/minor_quest/example/messages/...` | `gameJournalOnscreenGroup` at component 5 | `5` |

`gameJournalEmailGroup` follows the same containing-file rule as the file and
onscreen groups. The group name and path depth are author choices; calculate
the index from the actual tree rather than memorizing one number.

## Inspect a vanilla tree safely

Use the Asset Browser in a disposable project to extract:

```text
base\journal\cooked_journal.journal
```

This is a large merged vanilla resource. Search for a narrow path instead of
reading or publishing the whole serialization. A useful focused observation
is:

```text
contacts/dex/q003_flathead_price
```

**Observed in vanilla:** that conversation contains a
`gameJournalPhoneMessage`, a `gameJournalPhoneChoiceGroup` with one
`gameJournalPhoneChoiceEntry`, and a following phone message. The containing
`gameJournalContact` is path component `1`, which explains the corresponding
phone-path index.

For a file-backed UI example, inspect the journal path cited by the SQ021
questphase:

```text
onscreens/emails/quests/side_quest/sq021_sick_dreams/
sq021_randy_files/01_cartoon
```

Its containing `gameJournalFileGroup` is component `5`. The related quest
control is in:

```text
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
```

Keep both resources outside the downloadable tutorial. Record their depot
paths and your own observations; do not commit the extracted CR2W files.

## Save-state boundary

The `.journal` resource defines entries, while the save can retain their
runtime state. Repacking the definition does not erase an earlier activation,
success, failure, visit, or tracking decision stored in the save.

Use a manual save created before the journal resource was ever installed when
testing:

- a new entry or changed path;
- first activation and notification behavior;
- objective and quest completion;
- a phone choice or visited-state condition;
- removal and reinstall of the same build.

Resetting a fact is not equivalent to resetting journal state. Follow the
[minimum save test matrix](../foundations/persistent-state.md#minimum-save-test-matrix).

## Failure checks

If a journal lookup fails, check in this order:

1. Confirm the `.journal` CR2W exists at the registered depot path.
2. Confirm the ArchiveXL file contains the `journal` entry at the correct YAML
   nesting.
3. Reopen the journal in WolvenKit and verify the root descriptor and every
   entry `id` survived serialization.
4. Trace `realPath` component by component from the anonymous root.
5. Confirm `className` matches the tutorial-owned target type.
6. Recalculate `fileEntryIndex` from the containing file entry.
7. Distinguish a missing entry from a present entry whose saved state prevents
   the expected transition.

If the entry changes state but its title or description is blank, the journal
lookup succeeded. Continue along the separate localization lookup rather than
rewriting the journal tree.
