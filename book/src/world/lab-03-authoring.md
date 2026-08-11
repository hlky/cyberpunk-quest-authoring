# Author Boundary Check in WolvenKit

This walkthrough expands the supplied Lab 3 start checkpoint into the exact
16-node Boundary Check graph. The start project already contains every world,
journal, localization, and registration resource so you can inspect native
ownership before adding behavior.

You edit resources in WolvenKit. The repository's Python generators and
CR2W-JSON copies are documentation-author review infrastructure, not reader
prerequisites.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Structural validation date | 2026-08-09 |
| Runtime test date | Not yet recorded |

Use Cyberpunk 2077 `2.31a` for Windows (GOG), WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`. Other versions may expose
different editor wrappers or runtime behavior.

## 1. Open and isolate the checkpoint

1. Download and extract [the start ZIP](../downloads/cqa-lab-03-start.zip).
2. Open `CQA_Lab03_BoundaryCheck_Start.cpmodproj` with **File > Open
   Project**.
3. Make an untouched backup of the extracted directory.
4. Confirm that `source\archive` and `source\raw` each contain the same six
   depot resources listed in [the lab overview](lab-03.md#resource-ownership).
5. Confirm `CQA_Lab03_BoundaryCheck_Start.archive.xl` is under
   `source\resources`.
6. Do not install the start and completed checkpoints together.

The phase should contain only `[0] Input` connected to `[1] Output`. Confirm
Input `socketName: In1`, Output `socketName: Out1`, and Output
`type: Terminating`.

## 2. Audit registration before graph work

Open the ArchiveXL file and retain all four sections:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa003\phases\cqa003.questphase
    parent: base\quest\cyberpunk2077.quest

journal:
- mod\cqa\cqa003\journal\cqa003.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa003\localization\en-us\onscreens\cqa003.json

streaming:
  blocks:
  - mod\cqa\cqa003\world\cqa003_boundary.streamingblock
```

The block owns the two sector dependencies. Do not add the sectors to a
guessed top-level registration list. `base\quest\cyberpunk2077.quest` is a
vanilla reference; do not include an extracted copy.

## 3. Audit the journal, strings, and map pin

Open `cqa003.journal` and confirm this typed tree:

```text
gameJournalRootFolderEntry
└── quests                         gameJournalPrimaryFolderEntry
    └── minor_quest                gameJournalFolderEntry
        └── cqa003                 gameJournalQuest
            └── cqa003_01          gameJournalQuestPhase
                ├── cqa003_01_obj_reach
                │   └── cqa003_01_qmp_checkpoint
                └── cqa003_01_obj_leave
```

The map-pin entry is `gameJournalQuestMapPin`. Confirm:

| Property | Value |
| --- | --- |
| `enableGPS` | `1` |
| `reference.reference` | `#cqa003_mp_checkpoint` |
| `offset` | `(0, 0, 0.5)` |
| `mappinData.active` | `0` |
| `mappinData.mappinType` | `Mappins.QuestStaticMappinDefinition` |
| `mappinData.variant` | `DefaultQuestVariant` |
| `mappinData.visibleThroughWalls` | `1` |
| localized/debug caption | `cqa_cqa003_mappin_checkpoint` |

Open the onscreen localization resource and confirm four entries with primary
key `0`, empty male variants, and these exact joins:

| `secondaryKey` | `femaleVariant` |
| --- | --- |
| `cqa_cqa003_title` | `Boundary Check` |
| `cqa_cqa003_objective_reach` | `Reach the marked checkpoint.` |
| `cqa_cqa003_objective_leave` | `Leave the checkpoint area.` |
| `cqa_cqa003_mappin_checkpoint` | `Boundary Check checkpoint` |

Save, close, and reopen both resources. Do not edit the raw JSON review copies.

## 4. Audit the root prefab declaration

Open `cqa003.questphase` in the resource editor. Its root
`questQuestPhaseResource` has:

```text
phasePrefabs[0].prefabNodeRef = #cqa003_pr_boundary
inplacePhases = []
```

Keep exactly one declaration. `phasePrefabs` is a root-resource collection;
`phaseInstancePrefabs` belongs to a Phase node. This lab has no child phase
node and needs no duplicate declaration.

The full world root is
`$/mod/cqa/cqa003/#cqa003_pr_boundary`. Local graph conditions refer to child
refs under that declared root.

## 5. Audit the streaming block

Open `cqa003_boundary.streamingblock`. It has two
`worldStreamingSectorDescriptor` records:

| Property | Quest descriptor | AlwaysLoaded descriptor |
| --- | --- | --- |
| `category` | `Quest` | `AlwaysLoaded` |
| `level` | `0` | `1` |
| `data` | `...\cqa003_boundary.streamingsector` | `...\cqa003_always_loaded.streamingsector` |
| `questPrefabNodeRef` | `$/mod/cqa/cqa003/#cqa003_pr_boundary` | zero/unset |
| `numNodeRanges` | `1` | `1` |
| `variants` | empty | empty |

The Quest descriptor's finite box is:

```text
Min (-1300.02, 1197.2208, -291.7)
Max ( -700.02, 1797.2208,  308.3)
```

The AlwaysLoaded descriptor uses the supplied broad `-99999..99999` box.
Descriptor and sector levels are separate properties: the Quest descriptor is
level `0`, while the Quest sector root below is level `255`. Do not normalize
them to the same number.

The chosen bounds are **Experimental**. Keep them unchanged for canonical
comparison; tune bounds only as a separately hashed candidate.

## 6. Audit the Quest sector and placements

Open `cqa003_boundary.streamingsector`. Confirm root category `Quest`, level
`255`, two nodes, two `nodeData.Data` records, and two full `nodeRefs`.

| `NodeIndex` | Local node | Full `QuestPrefabRefHash` | Position |
| ---: | --- | --- | --- |
| `0` | reach `worldTriggerAreaNode` | `$/mod/cqa/cqa003/#cqa003_pr_boundary/#cqa003_tr_reach` | `(-1000.02, 1497.2208, 2.3)` |
| `1` | leave `worldTriggerAreaNode` | `$/mod/cqa/cqa003/#cqa003_pr_boundary/#cqa003_tr_leave` | `(-1000.02, 1497.2208, 0.3)` |

Both placements use yaw `88.6°`, unit scale, zero/unset cooked prefab data,
and these distance-shaped fields:

| Child | `MaxStreamingDistance` | `UkFloat1` |
| --- | ---: | ---: |
| reach | `320` | `280` |
| leave | `360` | `320` |

Treat `UkFloat1` as opaque. Similar numerical ordering does not establish its
meaning.

For these compact supplied sectors, `NodeIndex` selects a local node. Do not
turn that into a universal rule: some vanilla sectors register refs or use
indices outside a local `nodes` array.

## 7. Audit each trigger and its authoritative outline

Each node is a `worldTriggerAreaNode` with one
`questTriggerNotifier_Quest`, `includeChannels: TC_Default`, and
`isEnabled: 1`.

| Child ref | Outline points | Radius | Height |
| --- | ---: | ---: | ---: |
| `#cqa003_tr_reach` | `16` | `25` | `12` |
| `#cqa003_tr_leave` | `20` | `110` | `16` |

Open the `AreaShapeOutline` and inspect the serialized resource, not only the
canvas preview. Its binary `buffer` begins with a little-endian point count,
then stores each point as four floats `(x, y, z, 1.0)`, then the height float.
The supplied resources were verified by decoding those bytes.

Do not manually edit only `points` or `height`. If you intentionally change an
outline, use a WolvenKit operation that rebuilds the buffer, save and reopen,
then serialize the cooked result for an independent buffer check. The
canonical walkthrough keeps the supplied geometry unchanged.

## 8. Audit the marker sector

Open `cqa003_always_loaded.streamingsector`. Confirm category
`AlwaysLoaded`, level `1`, and one `worldStaticMarkerNode` selected by
`NodeIndex: 0`.

| Property | Value |
| --- | --- |
| Full placement ref | `$/mod/cqa/cqa003/#cqa003_pr_boundary/#cqa003_mp_checkpoint` |
| Position | `(-1000.02, 1497.2208, 8.3)` |
| Yaw | `88.6°` |
| `MaxStreamingDistance` | `360` |
| `UkFloat1` | `320` (opaque) |

The marker is an anchor. It is not the journal map pin, and it does not change
journal state. Keep the three-owner chain intact: sector marker, journal map
pin, graph Mappin Manager.

## 9. Add and number graph nodes

In the questphase graph, add these nodes in order. Input `0` and Output `1`
already exist.

| Target ID | Add Node label | RED type |
| ---: | --- | --- |
| `10` | `Condition` | `questConditionNodeDefinition` |
| `11` | `Journal` | `questJournalNodeDefinition` |
| `12` | `Journal` | `questJournalNodeDefinition` |
| `13` | `Journal` | `questJournalNodeDefinition` |
| `14` | `MappinManager` | `questMappinManagerNodeDefinition` |
| `15` | `PauseCondition` | `questPauseConditionNodeDefinition` |
| `16` | `MappinManager` | `questMappinManagerNodeDefinition` |
| `17` | `Journal` | `questJournalNodeDefinition` |
| `18` | `Journal` | `questJournalNodeDefinition` |
| `19` | `PauseCondition` | `questPauseConditionNodeDefinition` |
| `20` | `Journal` | `questJournalNodeDefinition` |
| `21` | `Journal` | `questJournalNodeDefinition` |
| `22` | `FactsDBManager` | `questFactsDBManagerNodeDefinition` |
| `23` | `Journal` | `questJournalNodeDefinition` |

WolvenKit normally assigns lower automatic IDs. Renumber safely in two passes:
move the new nodes to temporary IDs `100`–`113`, then to target IDs `10`–`23`.
Never overwrite an ID still owned by another node. Save, close, reopen, and
confirm the exact inventory before wiring.

## 10. Configure the completion guard and fact writer

At ID `10`, add a `questFactsDBCondition`, then
`questVarComparison_ConditionType`:

| Property | Value |
| --- | --- |
| `factName` | `cqa003_completed` |
| `comparisonType` | `Equal` |
| `value` | `0` |

At ID `22`, choose `questSetVar_NodeType` and set:

| Property | Value |
| --- | --- |
| `factName` | `cqa003_completed` |
| `setExactValue` | `1` |
| `value` | `1` |

Exact assignment makes the one-shot result independent of an old numeric
value. Do not use a console write in the canonical runtime run.

## 11. Configure journal operations

For Journal IDs, add `questJournalQuestEntry_NodeType` and a typed
`gameJournalPath`. Keep these common values:

| Property | Value |
| --- | --- |
| `type.optional` | `0` |
| `type.sendNotification` | `1` |
| `type.trackQuest` | `1` |
| `type.version` | `Initial` |
| `type.path.editorPath` | empty |
| `type.path.fileEntryIndex` | `2` |

| IDs | `className` | `realPath` |
| --- | --- | --- |
| `11`, `23` | `gameJournalQuest` | `quests/minor_quest/cqa003` |
| `12`, `21` | `gameJournalQuestPhase` | `quests/minor_quest/cqa003/cqa003_01` |
| `13`, `17` | `gameJournalQuestObjective` | `quests/minor_quest/cqa003/cqa003_01/cqa003_01_obj_reach` |
| `18`, `20` | `gameJournalQuestObjective` | `quests/minor_quest/cqa003/cqa003_01/cqa003_01_obj_leave` |

Incoming sockets choose state. IDs `11`, `12`, `13`, and `18` receive
`Active`; IDs `17`, `20`, `21`, and `23` receive `Succeeded`.

## 12. Configure map-pin operations

Both Mappin Manager nodes use this typed path:

| Property | Value |
| --- | --- |
| `path.className` | `gameJournalQuestMapPin` |
| `path.realPath` | `quests/minor_quest/cqa003/cqa003_01/cqa003_01_obj_reach/cqa003_01_qmp_checkpoint` |
| `path.fileEntryIndex` | `2` |
| `path.editorPath` | empty |

Set both ID `14` and ID `16` to `disablePreviousMappins: 0`. ID `14` receives
the `Active` socket and ID `16` receives the `Inactive` socket; both paths point
to the same journal entry. This isolated lab has no deliberate prior route to
replace. Use `1` only for a separately tested transition that intentionally
clears previous routing.

## 13. Configure trigger Pause Conditions

At each Pause Condition, add a `questTriggerCondition` at `condition`:

| ID | `condition.type` | `triggerAreaRef` |
| ---: | --- | --- |
| `15` | `IsInside` | `#cqa003_tr_reach` |
| `19` | `IsOutside` | `#cqa003_tr_leave` |

Set `isPlayerActivator: 1`. Leave `activatorRef` as the ordinary empty
`gameEntityReference`; do not substitute a guessed entity path. These are
state-shaped waiting nodes. Do not change them to `Entered`/`Exited` while
comparing with the canonical checkpoint.

## 14. Wire the exact graph

Use **Show Unused Sockets**, then create these 16 ordinary edges:

| Source | Destination |
| --- | --- |
| `0.Out` | `10.In` |
| `10.False` | `1.In` |
| `10.True` | `11.Active` |
| `11.Out` | `12.Active` |
| `12.Out` | `13.Active` |
| `13.Out` | `14.Active` |
| `14.Out` | `15.In` |
| `15.Out` | `16.Inactive` |
| `16.Out` | `17.Succeeded` |
| `17.Out` | `18.Active` |
| `18.Out` | `19.In` |
| `19.Out` | `20.Succeeded` |
| `20.Out` | `21.Succeeded` |
| `21.Out` | `22.In` |
| `22.Out` | `23.Succeeded` |
| `23.Out` | `1.In` |

Leave every `CutDestination` unwired. Save, close, reopen, then compare IDs,
types, payloads, sockets, and edges with the
[exact generated graph](lab-03.md#exact-questphase). Canvas position and
handle IDs are not behavior.

## 15. Validate, build, and install

With every tab saved:

1. run **Project > Scan for broken file references**;
2. run **Project > Scan for broken files**;
3. run **Project > Run File Validation on the entire project**;
4. resolve all project-owned errors;
5. close Cyberpunk 2077;
6. choose **Build > Install** and wait for packing and installation;
7. inspect WolvenKit's Log panel and both installed files.

Use the normal ArchiveXL project install, not **Install as REDmod**. A packed
archive without its loose `.archive.xl` cannot attach the phase, merge the
journal/localization, or register the block.

The manually expanded start project installs `_Start`-named files and is a
comparison candidate. Evidence that promotes the book must use the supplied,
unmodified `CQA_Lab03_BoundaryCheck.cpmodproj`, bind its installed hashes, and
follow the acceptance record.

## Common authoring failures

| Symptom | Check |
| --- | --- |
| Graph sockets move or disappear after reopen | Renumber through `100`–`113`, save, close, reopen, then wire only after final IDs are unique |
| Trigger wait never releases | Confirm Pause Condition, `questTriggerCondition`, player activator, exact local ref, matching full sector child ref, notifier, and decoded outline |
| Leave completes as soon as it activates | Confirm outer volume and Z coverage, `IsOutside`, and that the test save is actually inside the outer volume at reach success |
| Pin cannot resolve | Keep marker full ref, journal local ref, `gameJournalQuestMapPin` path, and active/inactive Mappin Manager operations aligned |
| Block exists but sectors do not appear | Keep both descriptor `data` paths, Quest root ref, category/level pairs, finite Quest bounds, and ArchiveXL block registration |
| Editing points changes nothing | The `AreaShapeOutline.buffer` is authoritative; update and revalidate the complete outline serialization |
| Build succeeds but nothing starts | Confirm installed archive plus loose registration file and inspect logs for all four registered top-level resources |
| Canonical hashes no longer match | Use the supplied completed checkpoint; a manually expanded `_Start` project is not byte-identical evidence |

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Lab 3:
Boundary Check](lab-03.md) · Next: [Test Boundary Check](lab-03-test.md).
