# Identifier-domain reference

Values that look alike in WolvenKit are not interchangeable. Use this page to
name the type, owner, and scope of an identifier before comparing, copying, or
regenerating it.

The exact Lab 1–5 joins cited here are **Structurally validated**. The broader
world and scene relationships inherit the evidence labels of their linked
chapters. This page adds no runtime claim.

## Quick domain map

| Domain | Native type or serialized shape | Scope / owner | Example | Never substitute |
| --- | --- | --- | --- | --- |
| Depot address | `ResourcePath` or a registration path value | Game virtual depot | `mod\cqa\cqa005\scenes\cqa005_first_contact.scene` | Windows path, NodeRef, journal path |
| CR2W object identity | `HandleId` / `HandleRefId` | One serialized CR2W object graph | `"HandleId": "15"` | Graph node ID, scene ID, world identity |
| Quest graph node | integer node `id` | One `questGraphDefinition` | Lab 1 FactsDB node `15` | `HandleId`, scene node ID |
| Quest socket/interface name | `CName` | One node or parent/child interface | `In`, `Out`, `In1`, `Out1`, `contact_done` | Numeric node ID or ordinal |
| Scene graph node | `scnNodeId` | One `scnSceneGraph` | First Contact Section `2` | Quest node ID or performer ID |
| Scene socket stamp | name plus ordinal | One scene-node socket mapping | output `0/0`, input `0/1` | Quest `questSocketDefinition` |
| World reference | `NodeRef` | Registered world / quest-prefab hierarchy | `#cqa005_com_contact` | CR2W handle, ResourcePath, TweakDBID |
| Gameplay record | `TweakDBID` | TweakDB | `Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa` | `.ent` path, NodeRef |
| Name token | `CName` | Field-specific RED name domain | community entry `contact` | Fact, localization key, ResourcePath |
| Fact | `factName` string with signed integer value | Facts database and save | `cqa005_completed` | CName, journal ID, Boolean field |
| Journal lookup | `gameJournalPath` | Merged journal tree | `quests/minor_quest/cqa005/...` | Depot path, localization key |
| Journal component | entry `id` | Parent entry's child collection | `cqa005_01_obj_meet` | `fileEntryIndex`, graph ID |
| UI localization | textual secondary key | Merged onscreen localization table | `cqa_cqa001_title` | Spoken-line RUID |
| Spoken/choice localization | `scnlocLocstringId.ruid` | Scene localization lookup | `9638591835734011695` | Screenplay item ID, event ID |
| Scene actor | `scnActorId` | One scene | contact `0`, V `1` | Performer ID, community ID |
| Scene performer symbol | `scnPerformerId` | Scene debug-symbol mapping | contact `1`, V `257` | Actor ID |
| Screenplay item | `scnscreenplayItemId` | One screenplay store | First Contact line `1` | Locstring or event ID |
| Timed scene event | `scnSceneEventId` | One scene event collection | `8646165628675208917` | Locstring or screenplay item ID |
| Lipsync resource slot | `scnLipsyncAnimSetSRRefId` | Index into one scene's lipsync array | slot `0` | Actor or performer ID |

## Resource addresses

### Filesystem paths and depot paths

These addresses can point toward the same source file while belonging to
different domains:

```text
H:\MyProject\source\archive\mod\myquest\phase.questphase
                                  filesystem path

mod\myquest\phase.questphase      depot path / ResourcePath value
```

Only the second form belongs in CR2W resource references and ArchiveXL path
values. Preserve the backslashes and spelling shown by WolvenKit. A file below
`source\raw` can end in `.questphase.json`; that conversion filename is not the
runtime depot path.

### Registration path versus soft reference

The same depot path can be consumed by different owners:

| Use | Owner | Meaning |
| --- | --- | --- |
| Root `quest.phases[].path` | ArchiveXL | Attach a mod-owned root beneath the game quest root |
| `phaseResource.DepotPath` | `questPhaseNodeDefinition` | Resolve an archived external child |
| `sceneFile.DepotPath` | `questSceneNodeDefinition` | Resolve an archived scene |
| Descriptor `data.DepotPath` | `worldStreamingSectorDescriptor` | Resolve a streaming sector |

A soft `ResourcePath` still requires the target file. It does not perform
ArchiveXL root registration.

## Serialized object and graph identity

### CR2W handles

```json
{
  "HandleId": "15",
  "Data": {
    "$type": "questFactsDBManagerNodeDefinition",
    "id": 15
  }
}
```

`HandleId` identifies the handled object in this serialization. The node's
integer `id` identifies it in the quest graph. They happen to match in the
example and are not required to match.

Rules:

- every `HandleRefId` must resolve to one compatible handled object;
- handle identity is local to one CR2W object graph;
- WolvenKit can normalize handle allocation during a semantic round trip;
- never repair a graph by forcing handle numbers to equal node numbers.

### Graph-local IDs

A node citation is incomplete without its graph scope:

```text
cqa005.questphase, quest node 12
cqa005_contact.questphase, quest node 12
cqa005_first_contact.scene, scene node 2
```

The repeated number does not join those nodes. Quest nodes use integer `id`;
scene graph nodes use typed `scnNodeId`. Parent graphs, child graphs, and scene
graphs can all reuse a number.

### Socket names and ordinals

Quest socket names are normally CNames such as `Active`, `True`, `Out1`, or
`contact_done`. Scene socket stamps use a name/ordinal pair. Neither is a graph
node ID.

An ordinal is local to the node type. First Contact's Start output `0/0`
targets both Section input `0/0` and PuppetAI-wrapper input `0/1`; that does
not mean the wrapper runs “second” in the whole scene.

## World and quest-prefab identity

### Local and full NodeRefs

The quest side can use a local child beneath a declared prefab root:

```text
#cqa005_tr_setup
```

The world side registers the full child:

```text
$/mod/cqa/cqa005/#cqa005_pr_first_contact/#cqa005_tr_setup
```

The root likewise appears in local form in a questphase `phasePrefabs` entry
and full form on the Quest-sector descriptor. Compare each representation in
its owning field; the prefix difference is expected.

The field named `QuestPrefabRefHash` is exposed as a NodeRef string in the
retained WolvenKit JSON. Do not replace it with a numeric hash merely because
its property name contains “Hash.”

### NodeRef is not ResourcePath

| Value | Type | Resolves |
| --- | --- | --- |
| `#cqa005_com_contact` | `NodeRef` | A world object beneath an available prefab root |
| `mod\cqa\cqa005\scenes\cqa005_first_contact.scene` | `ResourcePath` | A CR2W resource in the depot |
| `Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa` | `TweakDBID` | A gameplay record |

All three can be printed as text. Their lookup systems are independent.

### Community/source, registry, and AI-spot IDs

The compact Lab 5 community places several unsigned 64-bit world identities
beside one another:

| Domain | Canonical Lab 5 value | Derived from |
| --- | ---: | --- |
| Community/source identity | `5948510988927765319` | Full community NodeRef |
| Registry-node identity | `6908684691797323855` | Full community NodeRef with `_registry` appended to the final community name |
| AI-spot global identity | `15950783814303760596` | Full AI-spot NodeRef |

The source identity intentionally joins:

```text
worldCompiledCommunityAreaNode_Streamable.sourceObjectId.hash
  == worldCommunityRegistryItem.communityId.entityId.hash
```

The registry-node identity and every AI-spot identity must remain separate.
The spot identity then joins the registry persistent row and the compiled
area's `spotNodeIds` entry.

These numbers use RED4's alias-aware NodeRef operation. The `#` marker is
hierarchy/alias syntax, not an ordinary byte to pass through a generic text
hash. Do not derive these IDs with plain FNV over a debug label or printed
path. Retain the canonical full NodeRef beside every numeric value and reject
zero or unintended collisions. See [Registries and compiled
areas](../communities/registries-and-areas.md).

### Community entry and phase names

`contact` and `default` in Lab 5 are community-local CNames:

```text
entryName: contact
phaseName: default
```

They must match across registry template, compiled-area mirror, activation
action, readiness/acquisition references, and scene actor parameters where
applicable. They are not actor display names, TweakDB records, NodeRefs, or
world-global IDs. `None` in a community action is an authored CName token, not
JSON `null` or an omitted field.

## Journal, facts, and localization

### Fact name and value

A fact consists of a name plus a signed integer value:

```text
cqa005_completed = 1
```

The suffix `_completed` is an author convention. The engine learns its meaning
only from graph reads and writes. A fact is not automatically reset when a
questphase terminates or an archive changes.

### Journal path fields

`gameJournalPath` has four distinct fields:

| Field | Domain |
| --- | --- |
| `realPath` | Slash-separated journal-entry IDs |
| `className` | CName for the intended leaf entry type |
| `fileEntryIndex` | Zero-based component position of the containing `gameJournalFileEntry` |
| `editorPath` | Editor-facing text; the tutorial-owned paths leave it empty |

For this path:

```text
quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait
```

the containing `gameJournalQuest` is component `2`, so `fileEntryIndex` is
`2`. The value is not the objective's child index, graph node ID, or CR2W
handle. See [Journal trees and typed paths](../journal/trees-and-paths.md).

### Three localization domains

| Content | Identifier | Owner |
| --- | --- | --- |
| Journal/UI text | Textual `LocalizationString.value` matching onscreen `secondaryKey` | Registered onscreen localization resource |
| Spoken scene line | Unsigned `scnlocLocstringId.ruid` matching subtitle and VO `stringId` | External subtitle-map/entries and VO-map/WEM branches |
| Scene choice | Unsigned locstring RUID reached through a screenplay option | Scene's embedded `scnlocLocStoreEmbedded` |

A spoken line's RUID cannot be replaced with its screenplay item ID. A scene
choice cannot be repaired by adding its ID to the onscreen localization table.
See [Localization paths](../journal/localization-paths.md).

## Scene identifier domains

First Contact deliberately places several small and large numbers beside one
another:

| Typed domain | Values | Identifies |
| --- | --- | --- |
| `scnActorId` | `0`, `1` | Contact and V actor definitions |
| `scnPerformerId` | `1`, `257` | Debug performer-symbol rows |
| `scnNodeId` | `1`, `2`, `3`, `4` | Start, Section, End, and PuppetAI wrapper |
| `scnscreenplayItemId` | `1` | The screenplay line and the event-to-line join |
| `scnSceneEventId` | `8646165628675208917` | The timed line event instance |
| `scnlocLocstringId` | `9638591835734011695` | External subtitle and voice lookup |
| `scnLipsyncAnimSetSRRefId` | `0` | Slot in `resouresReferences.lipsyncAnimSets` |
| `scnInterruptionScenarioId` | `0` | The scene's Default interruption scenario |

Repeated `0` or `1` values do not create a cross-domain join.

### Actor versus performer

The exact debug-symbol rows are:

| Role | Actor ID | Performer ID |
| --- | ---: | ---: |
| Contact | `0` | `1` |
| V | `1` | `257` |

This fixture preserves the observed `actor ID * 256 + 1` performer-symbol
relationship. That does not authorize using performer `257` in a screenplay
field that expects `scnActorId(1)`.

### Screenplay item, event, and locstring

The join is directional:

```text
scnDialogLineEvent.screenplayLineId = screenplay item 1
  -> scnscreenplayDialogLine.itemId = screenplay item 1
       -> scnscreenplayDialogLine.locstringId = 9638591835734011695
```

Event ID `8646165628675208917` identifies the scheduled event itself. Do not
derive it from the locstring, reuse the item ID, or truncate either unsigned
value to 32 bits.

### Lipsync slot

Both Lab 5 actors refer to `scnLipsyncAnimSetSRRefId(0)`, and the scene owns
one addressable row at array slot `0`. The ID is an array index, not an actor
or performer identity. Actor `1` referring to slot `1` would be out of range
in that exact resource.

### Embedded choice variants

For later choice scenes, keep these domains distinct:

| Field | Role |
| --- | --- |
| `scnChoiceNodeOption.screenplayOptionId` | Join from graph option to screenplay option |
| `scnscreenplayChoiceOption.itemId` | Screenplay option identity |
| `scnscreenplayChoiceOption.locstringId` | Choice-text lookup identity |
| Descriptor `variantId.ruid` | Join to the matching payload variant |
| Descriptor `vpeIndex` | Zero-based position in `vpEntries[]` |

Moving a payload does not update `vpeIndex` by magic. Preserve descriptor,
variant, and payload identity together.

## Unsigned numeric handling

Scene RUIDs and several world identities exceed signed 32-bit range. Preserve
them as unsigned 64-bit values and print them as exact decimal strings when a
tool's number model cannot represent all 64 bits safely.

Do not:

- truncate to 32 bits;
- round through a floating-point number;
- sort decimal spellings lexicographically when numeric order matters;
- reuse an ID because it is small and currently unused in another domain;
- hash a NodeRef with a generic text algorithm when RED4 alias semantics are
  required.

## Domain-audit checklist

For every identifier in a practical resource:

1. Record the native type and full property path.
2. Record the owner and scope: CR2W graph, quest graph, scene, journal tree,
   world hierarchy, TweakDB, localization table, or save.
3. Record the canonical source string for derived world IDs.
4. Verify every join on both sides in the mod-owned resources.
5. Reject null handles, zero values where identity is required, out-of-range
   indices, and unintended collisions.
6. Reopen and round-trip the resources before comparing semantics.
7. Test external resolution and save behavior separately from structural
   validity.
