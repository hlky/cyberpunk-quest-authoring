# Author Signal Race in WolvenKit

This walkthrough expands the supplied Lab 2 start checkpoint into the exact
21-node Signal Race graph. You edit native resources in WolvenKit; the
repository's generator and CR2W-JSON files are documentation-author review
infrastructure, not reader prerequisites.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

Use Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext
`1.30.0`, and redscript `0.5.31`. Other versions may expose different editor
wrappers or runtime behavior.

## 1. Open and isolate the start checkpoint

1. Download and extract [the start ZIP](../downloads/cqa-lab-02-start.zip).
2. Open `CQA_Lab02_SignalRace_Start.cpmodproj` through **File > Open Project**.
3. Make an untouched backup of the extracted directory.
4. Confirm the project contains three cooked resources beneath
   `source\archive`, their three review JSON files beneath `source\raw`, and
   `CQA_Lab02_SignalRace_Start.archive.xl` beneath `source\resources`.
5. Do not install Lab 1, the completed Lab 2 checkpoint, and this start project
   as though they were one candidate. Lab 2's two checkpoints collide on all
   three `cqa002` depot paths.

The phase should contain only `[0] Input` connected to `[1] Output`. Verify
Input `socketName: In1`, Output `socketName: Out1`, and Output
`type: Terminating` before adding nodes.

## 2. Audit the supplied journal and strings

Open `cqa002.journal`. Confirm this exact typed tree:

```text
gameJournalRootFolderEntry
└── quests                         gameJournalPrimaryFolderEntry
    └── minor_quest                gameJournalFolderEntry
        └── cqa002                 gameJournalQuest
            └── cqa002_01          gameJournalQuestPhase
                ├── cqa002_01_obj_wait
                └── cqa002_01_obj_stable
```

The required objective has `optional: 0`; the stable objective has
`optional: 1`. Both have empty district IDs, zero item/location references,
and the quest has no district or recommended-level dependency.

Open the localization resource at
`mod\cqa\cqa002\localization\en-us\onscreens\cqa002.json`. Its
`localizationPersistenceOnScreenEntries.entries` array must join these keys:

| `secondaryKey` | `femaleVariant` |
| --- | --- |
| `cqa_cqa002_title` | `Signal Race` |
| `cqa_cqa002_objective_wait` | `Wait for the signal test to resolve.` |
| `cqa_cqa002_objective_stable` | `Keep the signal stable.` |

Each entry uses primary key `0` and an empty male variant. Save, close, and
reopen both resources. Do not edit their raw JSON review copies.

## 3. Add and number the graph nodes

Open `cqa002.questphase`, right-click an empty graph area, choose **Add Node**,
and add the following nodes in the table's order. The initial Input and Output
already exist.

| Target ID | Add Node label | RED type |
| --- | --- | --- |
| `10` | `Condition` | `questConditionNodeDefinition` |
| `11` | `FactsDBManager` | `questFactsDBManagerNodeDefinition` |
| `12` | `Journal` | `questJournalNodeDefinition` |
| `13` | `Journal` | `questJournalNodeDefinition` |
| `14` | `Journal` | `questJournalNodeDefinition` |
| `15` | `PauseCondition` | `questPauseConditionNodeDefinition` |
| `16` | `PauseCondition` | `questPauseConditionNodeDefinition` |
| `17` | `Condition` | `questConditionNodeDefinition` |
| `18` | `PauseCondition` | `questPauseConditionNodeDefinition` |
| `19` | `FactsDBManager` | `questFactsDBManagerNodeDefinition` |
| `20` | `PauseCondition` | `questPauseConditionNodeDefinition` |
| `21` | `FactsDBManager` | `questFactsDBManagerNodeDefinition` |
| `22` | `Journal` | `questJournalNodeDefinition` |
| `23` | `Journal` | `questJournalNodeDefinition` |
| `24` | `FactsDBManager` | `questFactsDBManagerNodeDefinition` |
| `25` | `LogicalXor` | `questLogicalXorNodeDefinition` |
| `26` | `Journal` | `questJournalNodeDefinition` |
| `27` | `FactsDBManager` | `questFactsDBManagerNodeDefinition` |
| `28` | `Journal` | `questJournalNodeDefinition` |

WolvenKit assigns IDs as nodes are created; a fresh start graph normally uses
`2` through `20`. Those auto IDs overlap the target range. Do not overwrite a
target ID that another node still owns.

After adding all 19 nodes, use the creation order recorded above to renumber in
two passes:

1. move the added nodes to unique temporary IDs `100` through `118`, preserving
   the table order;
2. move those same nodes from the temporary IDs to target IDs `10` through
   `28` from the table.

Save, close, and reopen the phase after both passes so the wrappers and
connector owners rebind to the serialized IDs. Confirm the inventory is
exactly `0`, `1`, and `10` through `28` before following any ID-addressed step.

Leave the root resource's `inplacePhases` and `phasePrefabs` arrays empty. This
lab owns no child phase or world resource. `phaseInstancePrefabs` belongs to a
`questPhaseNodeDefinition`; it is not a root `questQuestPhaseResource`
property.

## 4. Configure the immediate conditions

For IDs `10` and `17`, add a `questFactsDBCondition` handle at `condition`,
then add `questVarComparison_ConditionType` at `condition.type`.

| ID | `factName` | `comparisonType` | `value` |
| ---: | --- | --- | ---: |
| `10` | `cqa002_completed` | `Equal` | `0` |
| `17` | `cqa002_test_mode` | `Equal` | `1` |

These nodes sample their facts when a signal enters `In` and choose `True` or
`False`. Neither waits for a later value change.

## 5. Configure the fact writers

Each FactsDBManager node uses `questSetVar_NodeType`. Set
`type.setExactValue: 1` on all five nodes:

| ID | `type.factName` | `type.value` |
| ---: | --- | ---: |
| `11` | `cqa002_test_mode` | `2` |
| `19` | `cqa002_signal_failed` | `1` |
| `21` | `cqa002_signal_stop` | `1` |
| `24` | `cqa002_signal_succeeded` | `1` |
| `27` | `cqa002_completed` | `1` |

Exact mode value `2` is canonical. Do not change it while building the graph.
Incrementing an old save-backed value would make the test mode depend on prior
runs and invalidate the acceptance design.

## 6. Configure the waiting conditions

### Fact listener at ID 15

Add `questFactsDBCondition`, then `questVarComparison_ConditionType`:

| Property | Value |
| --- | --- |
| `factName` | `cqa002_signal_failed` |
| `comparisonType` | `Greater` |
| `value` | `0` |

### Boolean AND listener at ID 16

Add `questLogicalCondition` at `condition`, set `operation: AND`, and add two
handles to its `conditions` array. Each child is a `questFactsDBCondition`
containing a `questVarComparison_ConditionType`:

| Child | `factName` | `comparisonType` | `value` |
| ---: | --- | --- | ---: |
| `0` | `cqa002_signal_stop` | `Greater` | `0` |
| `1` | `cqa002_test_mode` | `Equal` | `2` |

This is a Boolean tree inside one Pause Condition. Do not replace it with a
graph-level Logical AND node.

### Realtime delays at IDs 18 and 20

At each node, add `questTimeCondition`, then
`questRealtimeDelay_ConditionType`. Set hours, minutes, and `miliseconds` to
zero. Set seconds to `30` on ID `18` and `120` on ID `20`. These deliberately
long human-test windows make the objective state observable after loading and
leave time to create a mid-flow manual save.

`miliseconds` is the native RED spelling. Timer behavior through pause,
loading, and save/reload remains part of the runtime test.

## 7. Configure every journal operation

For each Journal node, add `questJournalQuestEntry_NodeType` at `type`, then a
`gameJournalPath` handle at `type.path`. Set these common properties:

| Property | Value |
| --- | --- |
| `type.optional` | `0` |
| `type.sendNotification` | `1` |
| `type.trackQuest` | `1` |
| `type.version` | `Initial` |
| `type.path.editorPath` | empty string |
| `type.path.fileEntryIndex` | `2` |

Then set paths by target:

| IDs | `className` | `realPath` |
| --- | --- | --- |
| `12`, `28` | `gameJournalQuest` | `quests/minor_quest/cqa002` |
| `13`, `26` | `gameJournalQuestObjective` | `quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_wait` |
| `14`, `22`, `23` | `gameJournalQuestObjective` | `quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_stable` |

The incoming socket chooses state: IDs `12`, `13`, and `14` receive `Active`;
ID `22` receives `Failed`; IDs `23`, `26`, and `28` receive `Succeeded`.
Changing the payload's path does not compensate for wiring the wrong state
socket.

## 8. Configure the XOR-typed convergence

On ID `25`, set:

| Property | Value |
| --- | ---: |
| `inputSocketCount` | `2` |
| `outputSocketCount` | `1` |

After saving and reopening, confirm ordinary sockets `In1`, `In2`, and `Out1`
plus the inherited `CutDestination`. The node's name does not prove automatic
cancellation or exactly-once behavior; those are acceptance questions.

## 9. Expose and wire all sockets

Right-click each node and choose **Show Unused Sockets**. Create these 22
ordinary edges:

| Source | Destination |
| --- | --- |
| `0.Out` | `10.In` |
| `10.False` | `1.In` |
| `10.True` | `11.In` |
| `11.Out` | `12.Active` |
| `12.Out` | `13.Active` |
| `13.Out` | `14.Active` |
| `14.Out` | `15.In` |
| `14.Out` | `16.In` |
| `14.Out` | `17.In` |
| `17.True` | `18.In` |
| `18.Out` | `19.In` |
| `17.False` | `20.In` |
| `20.Out` | `21.In` |
| `15.Out` | `22.Failed` |
| `22.Out` | `25.In1` |
| `16.Out` | `23.Succeeded` |
| `23.Out` | `24.In` |
| `24.Out` | `25.In2` |
| `25.Out1` | `26.Succeeded` |
| `26.Out` | `27.In` |
| `27.Out` | `28.Succeeded` |
| `28.Out` | `1.In` |

The three connections leaving `14.Out` are intentional. Do not insert a Hub.
The two edges entering `1.In` are also valid; they do not require two formal
input sockets.

Leave every `CutDestination` unwired. Lab 2 deliberately avoids claiming cut
behavior. Do not connect cut sockets to ordinary flow as a guessed cleanup.

Save, close, reopen, and compare against the
[exact generated graph](lab-02.md#exact-questphase). Placement and handle IDs
may differ; node IDs, RED types, payloads, socket names, and resolved edges
must match.

## 10. Verify registration and project structure

The start checkpoint already contains ArchiveXL registration. Keep its three
sections unchanged while authoring:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa002\phases\cqa002.questphase
    parent: base\quest\cyberpunk2077.quest

journal:
- mod\cqa\cqa002\journal\cqa002.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa002\localization\en-us\onscreens\cqa002.json
```

`base\quest\cyberpunk2077.quest` is a vanilla reference. Do not include an
extracted copy in the project.

Keep the start project filename, `<Name>`, `<ModName>`, and
`CQA_Lab02_SignalRace_Start.archive.xl` filename during the walkthrough. Its
built archive is a manual comparison candidate, not the byte-identical
canonical candidate named by the acceptance record. For book-promoting
runtime evidence, close that project and open the supplied unmodified
`CQA_Lab02_SignalRace.cpmodproj`; do not try to turn `_Start` into the
canonical project with a partial rename.

## 11. Validate and build

With every tab saved:

1. run **Project > Scan for broken file references**;
2. run **Project > Scan for broken files**;
3. run **Project > Run File Validation on the entire project**;
4. resolve all project-owned errors;
5. close Cyberpunk 2077;
6. choose **Build > Install** and wait for packing and installation;
7. inspect the WolvenKit Log panel and the installed archive plus `.archive.xl`.

Use the normal ArchiveXL project install, not **Install as REDmod**. A packed
archive without the loose registration file cannot attach the root or merge
the journal/localization resources.

The manually authored start project installs
`CQA_Lab02_SignalRace_Start.archive` with its `_Start.archive.xl`. The supplied
canonical completed project installs `CQA_Lab02_SignalRace.archive` with
`CQA_Lab02_SignalRace.archive.xl`. Remove one pair before installing the
other; both pairs register the same three depot paths.

## 12. Create the controlled failure candidate

Do this only after preserving the canonical build and its hash:

1. copy the completed project to a separately named working directory;
2. open node `11`;
3. change only `type.value` from exact `2` to exact `1`;
4. leave `setExactValue: 1` and all other files/properties unchanged;
5. rebuild, hash the edited archive, and label it as the source-edited variant;
6. install it only after removing the canonical archive;
7. load a different untouched save created before any Lab 2 candidate was
   installed.

Do not flip the fact through a console command for acceptance. Together, the
controlled source edit and exact graph establish which producer is wired to
the route and create a reproducible candidate artifact. The runtime run records
the player-visible outcome; it does not directly observe that internal signal.

## Common authoring failures

| Symptom | Check |
| --- | --- |
| Reopening the phase loses or misbinds connectors | Renumber through temporary IDs `100`–`118`, save, close, reopen, and confirm the exact final ID inventory before wiring |
| A condition branches immediately instead of waiting | IDs `15`, `16`, `18`, and `20` must be Pause Condition nodes; IDs `10` and `17` are the only immediate Condition nodes |
| The stable route never releases | Confirm ID `16` contains one logical `AND` tree with both fact children and that ID `21` writes `cqa002_signal_stop` exactly `1` |
| Optional journal state is wrong | Keep the journal entry's `optional: 1` separate from each questphase journal operation's `type.optional: 0`; wire `Failed` and `Succeeded` sockets exactly |
| Build succeeds but the quest is absent | Install both the packed archive and loose `.archive.xl`, then inspect ArchiveXL and RED4ext logs for the three depot paths |
| Canonical hashes no longer match | Restore node `11` to exact value `2` and use the supplied completed project; a manually expanded `_Start` project is only a comparison candidate |

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Lab 2:
Signal Race](lab-02.md) · Next: [Test both Signal Race
routes](lab-02-test.md).
