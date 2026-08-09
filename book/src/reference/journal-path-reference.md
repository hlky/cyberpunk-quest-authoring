# Journal path reference

A `gameJournalPath` addresses one typed entry inside the merged journal tree.
It does not address the `.journal` CR2W file, a handle inside that file, or a
localization string. Use this page when filling a quest node's `path` value;
use [Journal trees and typed paths](../journal/trees-and-paths.md) for the full
authoring model.

| Record | Value |
| --- | --- |
| Reference review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Lab 1–5 path resources | **Structurally validated** |
| Exact Lab 1–5 in-game state transitions | Governed by each lab's canonical marker: pending/failed is **Experimental**; passed promotes only its recorded cases to **Runtime-proven** |

Journal activation, visited state, tracking, success, and failure can persist
in a save. Use an untouched save made before the candidate journal was first
installed when changing a tree, path, or entry identity.

## The four fields

| `gameJournalPath` field | RED value kind | What to enter |
| --- | --- | --- |
| `realPath` | String | Slash-separated entry `id` values, excluding the anonymous `gameJournalRootFolderEntry` |
| `className` | `CName` | Exact RED class of the intended target in tutorial-owned trees |
| `fileEntryIndex` | Integer | Zero-based `realPath` component containing the nearest `gameJournalFileEntry` |
| `editorPath` | String | Empty string in Labs 1–5 |

For Lab 1's objective:

```text
realPath: quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait
className: gameJournalQuestObjective
fileEntryIndex: 2
editorPath: ""
```

Do not put a depot path in `realPath`. These three addresses are distinct:

```text
mod\cqa\cqa001\journal\cqa001.journal       cooked depot resource
quests/minor_quest/cqa001/...                 merged journal entry
cqa_cqa001_objective_wait                     localization key
```

## Calculate `fileEntryIndex`

Split `realPath` at `/`, count from zero, and locate the component whose entry
is the nearest containing subtype of `gameJournalFileEntry`.

```text
0  quests
1  minor_quest
2  cqa001             gameJournalQuest; containing file entry
3  cqa001_01
4  cqa001_01_obj_wait
```

The value is therefore `2` for the quest, phase, objectives, and nested quest
mappin in every `quests/minor_quest/cqa00N/...` tutorial tree. It is not the
leaf depth and is not a constant for every journal family.

| Path family | Typical containing file entry | Example index |
| --- | --- | ---: |
| `quests/minor_quest/<quest>/...` | `gameJournalQuest` at component 2 | `2` |
| `contacts/<contact>/...` | `gameJournalContact` at component 1 | `1` |
| `points_of_interest/minor_quests/...` | `gameJournalPointOfInterestGroup` at component 1 | `1` |
| `onscreens/emails/quests/minor_quest/<quest>/files/...` | `gameJournalFileGroup` at component 5 | `5` |
| `onscreens/emails/quests/minor_quest/<quest>/messages/...` | `gameJournalOnscreenGroup` at component 5 | `5` |

Calculate the value from the actual contributed tree. A different folder
layout can move the containing file entry.

## Common target classes

| Target | `className` |
| --- | --- |
| Quest | `gameJournalQuest` |
| Quest phase | `gameJournalQuestPhase` |
| Quest objective | `gameJournalQuestObjective` |
| Objective description | `gameJournalQuestDescription` |
| Quest mappin | `gameJournalQuestMapPin` |
| Contact | `gameJournalContact` |
| Phone message | `gameJournalPhoneMessage` |
| Phone choice group | `gameJournalPhoneChoiceGroup` |
| Phone choice | `gameJournalPhoneChoiceEntry` |

Use the exact target type for mod-owned entries. **Observed in vanilla:** some
older quest nodes carry surprising or less-specific `className` values. When
researching one, resolve `realPath` against the extracted journal tree before
deciding whether the value is intentional. Do not copy a legacy mismatch into
a new resource.

## Lab 1–5 path sheet

Every path below uses `fileEntryIndex: 2` and `editorPath: ""`. The class is
`gameJournalQuest`, `gameJournalQuestPhase`, `gameJournalQuestObjective`, or
`gameJournalQuestMapPin` according to the last component shown.

| Lab | Entry | `realPath` |
| --- | --- | --- |
| First Signal | Quest | `quests/minor_quest/cqa001` |
| First Signal | Phase | `quests/minor_quest/cqa001/cqa001_01` |
| First Signal | Wait objective | `quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait` |
| Signal Race | Quest | `quests/minor_quest/cqa002` |
| Signal Race | Phase | `quests/minor_quest/cqa002/cqa002_01` |
| Signal Race | Wait objective | `quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_wait` |
| Signal Race | Stable objective | `quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_stable` |
| Boundary Check | Quest | `quests/minor_quest/cqa003` |
| Boundary Check | Phase | `quests/minor_quest/cqa003/cqa003_01` |
| Boundary Check | Reach objective | `quests/minor_quest/cqa003/cqa003_01/cqa003_01_obj_reach` |
| Boundary Check | Quest mappin | `quests/minor_quest/cqa003/cqa003_01/cqa003_01_obj_reach/cqa003_01_qmp_checkpoint` |
| Boundary Check | Leave objective | `quests/minor_quest/cqa003/cqa003_01/cqa003_01_obj_leave` |
| Handoff Point | Quest | `quests/minor_quest/cqa004` |
| Handoff Point | Phase | `quests/minor_quest/cqa004/cqa004_01` |
| Handoff Point | Reach objective | `quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_reach` |
| Handoff Point | Quest mappin | `quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_reach/cqa004_01_qmp_handoff` |
| Handoff Point | Leave objective | `quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_leave` |
| Handoff Point | Confirmation objective | `quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_confirm` |
| First Contact | Quest | `quests/minor_quest/cqa005` |
| First Contact | Phase | `quests/minor_quest/cqa005/cqa005_01` |
| First Contact | Meet objective | `quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_meet` |
| First Contact | Quest mappin | `quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_meet/cqa005_01_qmp_contact` |
| First Contact | Leave objective | `quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_leave` |

These values are **Structurally validated** against the supplied mod-owned
journal CR2Ws and questphases. A matching string and successful CR2W round
trip do not prove that a saved journal transition will replay in game.

## Registration and resolution check

The journal contribution must be registered independently of every path that
targets it:

```yaml
journal:
- mod\cqa\cqa001\journal\cqa001.journal
```

Check the chain in this order:

1. The cooked `.journal` exists beneath `source\archive` at the intended depot
   path.
2. The loose `.archive.xl` registers that exact depot path.
3. The journal's entry `id` chain produces `realPath` exactly, including case
   and separators.
4. `className` matches the mod-owned target type.
5. `fileEntryIndex` identifies the nearest containing file entry.
6. The localization key on the target resolves through the separate onscreen
   lookup.
7. The starting save has known journal state.

If the entry changes state but displays blank text, the path resolved. Continue
with the [localization reference](localization-reference.md). If a new state
change behaves like an older build, retest from a pre-install save before
editing the path again.

## Focused vanilla checks

**Observed in vanilla:** extract `base\journal\cooked_journal.journal` from
your own installation and inspect only the needed branch. Useful comparisons
are `contacts/dex/q003_flathead_price` for contact paths and the SQ021 file path
under `onscreens/emails/quests/side_quest/sq021_sick_dreams/...` for a
component-5 file entry. Pair the latter with
`base\quest\side_quests\sq021\phases\sq021_randys_room.questphase`.

Do not publish the extracted journal, its complete serialization, or the
vanilla questphase. Record the depot path, focused entry types, component
indices, and the exact question the comparison answered.
