# Lab 1: author First Signal

This walkthrough builds the complete **First Signal** checkpoint from the empty
Lab 1 WolvenKit project. You will create three mod-owned CR2W resources, wire
the quest graph, add the ArchiveXL registration, install the project, and run a
save-aware acceptance pass.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Runtime test date | Not yet recorded |

**Lab 1 runtime evidence:** **Experimental** — pending.

**Evidence status:** the supplied checkpoint is **Structurally validated** with
WolvenKit 8.19.0. The dedicated marker above mirrors the canonical acceptance
record. Follow the test procedure using that record; expected behavior is never
an observed result.

Use this exact baseline:

- Cyberpunk 2077 `2.31a`;
- WolvenKit `8.19.0`;
- ArchiveXL `1.27.0`;
- RED4ext `1.30.0`;
- redscript `0.5.31` (ArchiveXL 1.27.0 requires `0.5.31` or newer).

Complete the [pinned toolchain setup](setup.md), review the
[project and resource structure](project-structure.md), and read
[Lab 1's design](lab-01.md) before starting. Keep the
[completed checkpoint](../downloads/cqa-lab-01-completed.zip) extracted in a
separate directory for comparison.

## Editor boundary used in this guide

WolvenKit 8.19.0 exposes these named commands in the tested editor:

- **File > New File** for an empty CR2W or ArchiveXL file;
- **Add Node** on an empty part of a quest graph;
- **Show Unused Sockets** on a graph node;
- **Node Properties** beside the quest graph;
- **Project > Scan for broken file references**, **Scan for broken files**, and
  **Run File Validation on the entire project**;
- **Build > Install**.

The nested CR2W type chooser is contextual: its placement and visible rows
depend on the selected property. Where that makes a click label ambiguous,
this guide gives a **RED property path** instead. At that path, use the plus
control whose tooltip is **Add Handle** for a null handle or **Add New Element**
for an array, then choose the exact RED type named here. This is still an
in-editor workflow. Do not edit the serialized files under `source\raw`.

## 1. Open the start checkpoint

1. Extract the [start checkpoint](../downloads/cqa-lab-01-start.zip) to a
   writable working directory outside the game directory.
2. In WolvenKit, choose **File > Open Project** and open
   `CQA_Lab01_OneShot_Start.cpmodproj`.
3. Save a separate backup of that freshly extracted directory. WolvenKit's
   quest editor has no general undo/redo safety net for this graph workflow.
4. In the Project Explorer, open the `source\archive` directory in Windows
   Explorer and create this directory tree:

   ```text
   mod\cqa\cqa001\
   ├── journal\
   ├── localization\en-us\onscreens\
   └── phases\
   ```

The start checkpoint's project `ModName` ends in `_Start`, so its packed
archive will be named `CQA_Lab01_OneShot_Start.archive`. That external archive
name can differ from the completed checkpoint's archive name; the depot paths
inside it must match exactly.

## 2. Create the three CR2W resources

Create each file through **File > New File**. Choose the **CR2W Files**
category, select the listed root type, replace the proposed name with the
relative path below, and select **Create**.

| Root type shown in New File | Name | Result beneath `source\archive` |
| --- | --- | --- |
| `questQuestPhaseResource` | `mod\cqa\cqa001\phases\cqa001.questphase` | Root questphase |
| `gameJournalResource` | `mod\cqa\cqa001\journal\cqa001.journal` | Journal tree |
| `JsonResource` with the `.json` description | `mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json` | Onscreen localization |

The last file has a `.json` depot extension but is a binary CR2W
`JsonResource`. It is not the plain-text review file whose name ends in
`.json.json` in the completed checkpoint.

Press `Ctrl+S` after creating each file. The empty questphase should already
contain a non-null `questGraphDefinition`; this is the scratch-file behavior
of WolvenKit 8.19.0.

## 3. Author the journal tree

Open `cqa001.journal`. Work in the CR2W property tree and build this handle
chain:

```text
RootChunk                                      gameJournalResource
└── entry                                      gameJournalRootFolderEntry
    └── entries[0]                             gameJournalPrimaryFolderEntry
        └── entries[0]                         gameJournalFolderEntry
            └── entries[0]                     gameJournalQuest
                └── entries[0]                 gameJournalQuestPhase
                    └── entries[0]             gameJournalQuestObjective
```

At `RootChunk.entry`, add a handle of type
`gameJournalRootFolderEntry`. At every following `entries` array, add one
element and select the type shown above. Do not add an extra wrapper folder.

Set these properties. Paths use RED property names and array indexes, not
CR2W-JSON `HandleId` wrappers.

| Property path below `RootChunk` | Value |
| --- | --- |
| `cookingPlatform` | `PLATFORM_PC` |
| `entry.descriptor.DepotPath` | `base\journal\descriptor.journaldesc` |
| `entry.descriptor.Flags` | `Soft` |
| `entry.entries[0].id` | `quests` |
| `entry.entries[0].entries[0].id` | `minor_quest` |
| `entry.entries[0].entries[0].entries[0].id` | `cqa001` |
| `...cqa001.title.unk1` | `0` |
| `...cqa001.title.value` | `cqa_cqa001_title` |
| `...cqa001.type` | `MinorQuest` |
| `...cqa001.entries[0].id` | `cqa001_01` |
| `...cqa001_01.entries[0].id` | `cqa001_01_obj_wait` |
| `...cqa001_01_obj_wait.description.unk1` | `0` |
| `...cqa001_01_obj_wait.description.value` | `cqa_cqa001_objective_wait` |
| `...cqa001_01_obj_wait.counter` | `0` |
| `...cqa001_01_obj_wait.optional` | `0` |

In the abbreviated paths, `...cqa001` means
`entry.entries[0].entries[0].entries[0]`; each later name identifies its one
child entry.

`base\journal\descriptor.journaldesc` is the game-owned journal descriptor
that supplies the standard hierarchy contract. It is a reference only: do not
extract it into, rename it for, or redistribute it with the tutorial project.

Leave every entry's `journalEntryOverrideDataList` empty. Leave the quest's
`districtID` empty and `recommendedLevelID` at zero. Leave the phase's
`locationPrefabRef` at zero. Leave the objective's `districtID` empty and its
`itemID` and `locationPrefabRef` at zero. These values are deliberate: Lab 1
has no district, item, marker, or world reference.

Press `Ctrl+S`, close the tab, and reopen it. Confirm that the six-entry chain
and both localization keys survived serialization.

## 4. Author the onscreen localization

Open the CR2W `cqa001.json` under `source\archive`. At `RootChunk.root`, add a
handle of type `localizationPersistenceOnScreenEntries`. Add two elements to
its `entries` array; both elements are
`localizationPersistenceOnScreenEntry`.

Set the resource and entries exactly:

| Property path below `RootChunk` | Value |
| --- | --- |
| `cookingPlatform` | `PLATFORM_PC` |
| `root.entries[0].primaryKey` | `0` |
| `root.entries[0].secondaryKey` | `cqa_cqa001_title` |
| `root.entries[0].femaleVariant` | `First Signal` |
| `root.entries[0].maleVariant` | empty string |
| `root.entries[1].primaryKey` | `0` |
| `root.entries[1].secondaryKey` | `cqa_cqa001_objective_wait` |
| `root.entries[1].femaleVariant` | `Wait for the signal.` |
| `root.entries[1].maleVariant` | empty string |

This reproduces the structurally validated checkpoint shape. Runtime fallback
and presentation for this new arrangement remain part of the Lab 1
**Experimental** acceptance run.

Save, close, and reopen the resource. Confirm the secondary keys exactly match
the journal's `title.value` and `description.value` strings.

## 5. Add the quest nodes

Open `cqa001.questphase`. Its **Phase Resources** view should show empty
`inplacePhases` and `phasePrefabs` arrays. Leave both empty.

On an empty area of the graph, right-click and choose **Add Node**, then add
the following nodes in order. The menu uses the short editor label; the second
column records the serialized RED type.

| Add Node label | RED type | Target graph ID |
| --- | --- | ---: |
| `Input` | `questInputNodeDefinition` | `0` |
| `Output` | `questOutputNodeDefinition` | `1` |
| `Condition` | `questConditionNodeDefinition` | `10` |
| `Journal` | `questJournalNodeDefinition` | `11` |
| `Journal` | `questJournalNodeDefinition` | `12` |
| `PauseCondition` | `questPauseConditionNodeDefinition` | `13` |
| `Journal` | `questJournalNodeDefinition` | `14` |
| `FactsDBManager` | `questFactsDBManagerNodeDefinition` | `15` |
| `Journal` | `questJournalNodeDefinition` | `16` |

WolvenKit assigns fresh IDs as nodes are created. Select each node and use
**Node Properties** to set its `id` to the target value. If you created all
nine first, change them in the table's order: moving the initial input from
`1` to `0` frees `1` for the output, and the remaining IDs move to the unused
`10`–`16` range.

Set the interface fields:

| Node | Property | Value |
| --- | --- | --- |
| ID `0` | `socketName` | `In1` |
| ID `1` | `socketName` | `Out1` |
| ID `1` | `type` | `Terminating` |

`socketName` is the phase interface. It is different from the input node's
internal `Out` socket and the output node's internal `In` socket.

Press `Ctrl+S`, close the questphase tab, and reopen it now. WolvenKit's canvas
can retain the wrappers' original display IDs after an in-place `id` edit.
Before following the ID-addressed steps below, verify that the graph now shows
exactly `[0]`, `[1]`, and `[10]` through `[16]`. Reopening also rebinds the
connector owners to the serialized IDs.

## 6. Configure the node payloads

### ID 10: one-shot guard

At the node's `condition` property, add a `questFactsDBCondition` handle. At
`condition.type`, add a `questVarComparison_ConditionType` handle, then set:

| Property path | Value |
| --- | --- |
| `condition.type.factName` | `cqa001_completed` |
| `condition.type.comparisonType` | `Equal` |
| `condition.type.value` | `0` |

This node evaluates once on entry. It does not wait for the fact to change.

### IDs 11, 12, 14, and 16: journal operations

For each journal node, add a `questJournalQuestEntry_NodeType` handle at
`type`. Then select `type.path`, choose **Add Handle**, and create a
`gameJournalPath` handle. New journal nodes do not create that nested path for
you. Set the common fields on all four nodes:

| Property path | Value |
| --- | --- |
| `type.optional` | `0` |
| `type.sendNotification` | `1` |
| `type.trackQuest` | `1` |
| `type.version` | `Initial` |
| `type.path.editorPath` | empty string |
| `type.path.fileEntryIndex` | `2` |

Then set each typed path:

| ID | `type.path.className` | `type.path.realPath` |
| ---: | --- | --- |
| `11` | `gameJournalQuest` | `quests/minor_quest/cqa001` |
| `12` | `gameJournalQuestObjective` | `quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait` |
| `14` | `gameJournalQuestObjective` | `quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait` |
| `16` | `gameJournalQuest` | `quests/minor_quest/cqa001` |

IDs `12` and `14` address the same entry. Their incoming sockets will request
different states.

### ID 13: ten-second realtime gate

At `condition`, add a `questTimeCondition` handle. At `condition.type`, add a
`questRealtimeDelay_ConditionType` handle and set:

| Property path | Value |
| --- | ---: |
| `condition.type.hours` | `0` |
| `condition.type.minutes` | `0` |
| `condition.type.seconds` | `10` |
| `condition.type.miliseconds` | `0` |

`miliseconds` is the RED property spelling. This pause condition holds its
path until the realtime delay becomes true.

### ID 15: persistent fact write

WolvenKit initializes a new FactsDBManager node with a
`questSetVar_NodeType`. Verify and set:

| Property path | Value |
| --- | ---: |
| `type.factName` | `cqa001_completed` |
| `type.setExactValue` | `1` |
| `type.value` | `1` |

This writes exactly `1`; it does not increment the existing value.

## 7. Expose and connect every socket

Right-click each node and choose **Show Unused Sockets**. Drag from each source
output to the destination input in this table:

| Source | Destination | Meaning |
| --- | --- | --- |
| `0.Out` | `10.In` | Enter the one-shot guard |
| `10.True` | `11.Active` | First run: activate and track the quest |
| `10.False` | `1.In` | Already complete: terminate immediately |
| `11.Out` | `12.Active` | Activate and track the objective |
| `12.Out` | `13.In` | Begin the realtime wait |
| `13.Out` | `14.Succeeded` | Succeed the objective after the wait |
| `14.Out` | `15.In` | Continue to the completion fact write |
| `15.Out` | `16.Succeeded` | Succeed the quest after the fact write |
| `16.Out` | `1.In` | Terminate the successful route |

Socket inventory matters even when a socket is unused:

| Node IDs | Supplied sockets | Lab 1 use |
| --- | --- | --- |
| `0` | `CutDestination`, `Out` | `Out` is connected; cut is unwired |
| `1` | `CutDestination`, `In` | both normal routes enter `In`; cut is unwired |
| `10` | `CutDestination`, `In`, `False`, `True` | all except cut are connected |
| `11`, `12`, `14`, `16` | `CutDestination`, `Active`, `Inactive`, `Succeeded`, `Failed`, `Out` | the connected state input differs by node; `Out` continues; all other state inputs and cut are unwired |
| `13` | `CutDestination`, `In`, `Out` | normal wait path is connected; cut is unwired |
| `15` | `CutDestination`, `In`, `Out` | normal fact-write path is connected; cut is unwired |

For ID `11`, `Active` is connected. For ID `12`, `Active` is connected. For
IDs `14` and `16`, `Succeeded` is connected. An edge entering a journal node's
ordinary-looking but wrong state socket changes the requested journal state.

The unused `CutDestination` sockets are visible lifecycle obligations, not
missing normal-flow edges. Lab 1 does not claim cut-safe behavior. Do not wire
them to the terminating output as a guess.

Press `Ctrl+S`, close the questphase, and reopen it. Compare the graph against
the [exact generated figure](lab-01.md#exact-questphase). Node placement may
differ; IDs, types, sockets, payloads, and edges must not.

## 8. Register the resources with ArchiveXL

Choose **File > New File**, select the **ArchiveXL** category and
**ArchiveXL file**, name it `CQA_Lab01_OneShot.archive.xl`, and select
**Create**. WolvenKit places it under `source\resources`.

Enter this YAML exactly:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa001\phases\cqa001.questphase
    parent: base\quest\cyberpunk2077.quest

journal:
- mod\cqa\cqa001\journal\cqa001.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json
```

Save the file. The three entries have separate jobs: attach the executable
phase beneath the vanilla quest root, merge the journal, and register the
English onscreen strings. The `parent` path is a reference; do not extract or
add `base\quest\cyberpunk2077.quest` to the project.

Your authored source tree should now contain:

```text
source\
├── archive\mod\cqa\cqa001\
│   ├── journal\cqa001.journal
│   ├── localization\en-us\onscreens\cqa001.json
│   └── phases\cqa001.questphase
└── resources\CQA_Lab01_OneShot.archive.xl
```

## 9. Compare with the completed checkpoint

Open the completed `.cpmodproj` in a second WolvenKit instance, or close the
start project and open the completed project after saving. Compare semantic
structure, not binary bytes or CR2W handle numbers.

Check all of the following:

1. the three depot paths and ArchiveXL filename match;
2. the journal has the six exact types and IDs in one chain;
3. both journal localization keys resolve to the two secondary keys;
4. the questphase has IDs `0`, `1`, and `10`–`16`, with no extra nodes;
5. the nine connections match the socket table above;
6. both outer questphase arrays are empty;
7. the condition, delay, fact-write, journal path, notification, and tracking
   values match the property tables;
8. the ArchiveXL YAML matches by registration meaning and depot path.

If you need a text diff, Project Explorer can export a mod-owned CR2W file to
JSON under the mirrored `source\raw` path. Use that export only as a review
artifact. Do not repair the lab by editing raw JSON, and do not compare
`HandleId` allocation as if it were graph identity.

## 10. Validate, install, and inspect the install

With all tabs saved:

1. run **Project > Scan for broken file references**;
2. run **Project > Scan for broken files**;
3. run **Project > Run File Validation on the entire project**;
4. resolve every validation error owned by this project before continuing;
5. close Cyberpunk 2077;
6. choose **Build > Install** and wait for packing and installation to finish;
7. read WolvenKit's Log panel rather than treating the button press as proof.

Use the normal **Install** command for this ArchiveXL project. Do not choose
**Install as REDmod** or a hot-reload command. The full install, launch, log,
and evidence-recording procedure is collected in
[Install, test, record, reset](install-and-test.md).

The vanilla journal descriptor and root `parent` are deliberate references;
they need not be copied into the project. Treat any other unresolved reference
or validation error as a stop condition, even if it does not spell out one of
the three mod depot paths.

For the start checkpoint, verify these exact installed files beneath the game
directory:

```text
archive\pc\mod\CQA_Lab01_OneShot_Start.archive
archive\pc\mod\CQA_Lab01_OneShot.archive.xl
```

If you install the completed checkpoint instead, the archive is named
`CQA_Lab01_OneShot.archive`. The loose `.archive.xl` must be present beside the
archive in either case. A packed archive alone cannot register the root,
journal, or localization resources.

After launching the game once, inspect:

```text
red4ext\plugins\ArchiveXL\ArchiveXL.log
red4ext\logs\red4ext.log
red4ext\logs\game.log
r6\logs\redscript_rCURRENT.log
```

Search the ArchiveXL log for `CQA_Lab01_OneShot.archive.xl`, `cqa001`, or an
error naming one of the registered depot paths. Confirm that RED4ext loaded
ArchiveXL and that redscript did not report a new dependency/load error.
Registration without errors is evidence about registration, not proof that
the quest route executed.

## 11. Run the acceptance matrix

Use a manual save made before any version of `cqa001` was installed or loaded.
Record the save name, game and framework versions, and the installed archive
and `.archive.xl` hashes before the first run.

Use the packaged `runtime-acceptance.json`, not an unstructured pass/fail note.
The [acceptance-record procedure](install-and-test.md#complete-the-acceptance-record)
maps the first load to `clean-save-activation`, `realtime-delay`, and
`journal-completion`; the later runs map to `mid-flow-reload`,
`completed-save-reload`, `completed-save-reinstall`, and `clean-replay`; fresh
logs supply `registration-and-lookup-logs`.

The archive built from the manual start checkpoint is
`CQA_Lab01_OneShot_Start.archive`; it is your authored comparison candidate,
not the byte-identical completed candidate named by the canonical record. You
may copy and adapt the JSON for personal diagnostics, but that run cannot
promote the book. For contributor evidence, close the game, remove the `_Start`
archive, install the supplied completed checkpoint, verify that only
`CQA_Lab01_OneShot.archive` and its `.archive.xl` are under test, and then fill
the canonical record without changing its candidate paths or expected cases.

### First load

Load the clean save and observe, without using a world trigger. The intended
result is:

1. **First Signal** activates and is tracked;
2. **Wait for the signal.** activates and is tracked;
3. after about ten seconds of elapsed realtime, the objective succeeds;
4. the quest succeeds;
5. the quest does not reactivate on the completed save.

Record what actually happens and the relevant log lines. Until that retained
observation exists, all five statements remain expected **Experimental**
behavior.

The terminating output has no independent on-screen witness in Lab 1. Reaching
it is an inference from the exact terminal topology, successful journal state,
and absence of reactivation—not a directly observed UI event.

### Mid-flow reload

Return to the original clean save. As soon as the objective appears, make a
new manual save before the ten-second gate finishes. Reload that new save and
record whether the active route resumes and completes once. A successful
first-load run does not establish this reload behavior.

### Completed reload and reinstall

After a completed run, make another manual save and reload it. Then close the
game, install the same unchanged build again, and reload the completed save.
The intended one-shot result is that `cqa001_completed == 1` sends ID `10`
through `False` to the terminating output without reactivating the journal.
Record both passes separately.

### Clean replay

Reload the original pre-mod manual save for another first-run test. Do not use
the completed save as the replay baseline.

## 12. Reset and remove safely

There are three different operations:

- **Clean replay:** load the preserved pre-mod save. This is the acceptance
  reset because neither the fact nor the Lab 1 journal history exists there.
- **Fact-only diagnosis:** a fact inspection tool can change
  `cqa001_completed` back to `0`, but that does not clear succeeded journal
  state, a saved quest route, or other save-backed records. Never call this a
  clean replay.
- **Uninstall:** close the game and remove only the installed archive belonging
  to the project plus `archive\pc\mod\CQA_Lab01_OneShot.archive.xl`. Removing
  files does not erase state already written into a save.

When switching between the start and completed checkpoints, remove the other
checkpoint's archive first so two archives do not provide the same three depot
paths. Keep the pre-mod save untouched. If a test behaves differently after a
fact-only reset, repeat it from that pre-mod save before attributing the result
to the graph.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| No quest activation | Installed `.archive.xl`, its `quest.phases` path, ArchiveXL log, and the save's completion fact |
| Quest title or objective text is blank | Journal localization key versus onscreen `secondaryKey` |
| Objective stays active | ID `13.Out` to ID `14.Succeeded`, not `14.Active` |
| Quest finishes but repeats | ID `15` exact fact write and the fact value on the reloaded save |
| First run works; replay looks inconsistent | Journal state and other save-backed data left by the earlier run |
| WolvenKit graph looks different after reopen | Compare IDs, node types, sockets, and edges; ignore layout and handle allocation |

Serialization, validation, packing, ArchiveXL registration, and runtime
behavior are different evidence steps. Keep the **Experimental** label until
the clean-save matrix—not merely the successful build—has been retained.

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Lab 1:
First Signal](lab-01.md) · Next: [Install, test, and reset](install-and-test.md).
