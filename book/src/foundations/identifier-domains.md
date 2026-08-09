# Identifier domains

Cyberpunk resources place many identifier types beside one another. Similar
text or numbers do not make them interchangeable.

## Domain map

| Domain | Typical serialized shape | Identifies |
| --- | --- | --- |
| Depot path | `ResourcePath` | A resource in the virtual depot |
| CR2W handle | `HandleId` / `HandleRefId` | An object inside one serialized CR2W object graph |
| Quest graph node | numeric node `id` | A node inside one questphase graph |
| World reference | `NodeRef` | A registered world or quest-prefab object |
| Name token | `CName` | A REDengine name value such as a socket or entry-point name |
| Gameplay record | `TweakDBID` | A record in TweakDB |
| Fact | string `factName` | A signed integer state slot in the facts database |
| Journal path | `gameJournalPath.realPath` | An entry in the merged journal tree |
| Localization key | secondary key or numeric locstring ID | Text in one of several localization lookup systems |
| Scene-local IDs | actor, performer, node, event, screenplay, locstring, and variant IDs | Distinct objects inside scene systems |

Never derive one domain from another merely because the values can both be
printed as strings or integers.

## CR2W handles

A CR2W handle gives one serialized object an identity:

```json
{
  "HandleId": "15",
  "Data": {
    "$type": "questFactsDBManagerNodeDefinition",
    "id": 15
  }
}
```

Another field can refer to that object:

```json
{ "HandleRefId": "15" }
```

The graph node `id` and `HandleId` happen to both be `15` in this shortened
example, but they serve different domains and are not required to match.

Handle rules:

- a `HandleRefId` must resolve to one compatible `HandleId`;
- handle identity is local to the serialized CR2W object graph;
- duplicating a handled object without repairing its internal references can
  create dangling or aliased structure;
- **Structurally validated:** WolvenKit round trips can normalize handle
  allocation while preserving the same node/socket graph.

For this reason, exact diagrams fingerprint semantic nodes, sockets, and edges,
not the incidental handle numbers assigned by one serialization pass.

## NodeRefs

A `NodeRef` identifies something registered in the world or beneath a
quest-prefab root:

```text
#cqa_example_trigger
$/mod/cqa/#cqa_example_prefab/#cqa_example_trigger
```

It is not a CR2W handle. A valid-looking NodeRef string still fails if no loaded
streaming resource registers that reference or if the questphase does not
declare the required prefab dependency.

Later world chapters explain:

- streaming-sector `nodeRefs`;
- `QuestPrefabRefHash`;
- streaming-block `questPrefabNodeRef`;
- questphase `phasePrefabs`;
- full versus local NodeRef paths.

Lab 1 contains no NodeRef, which is why it has no position or streaming
requirement.

## Journal paths

A journal path names a position in the merged journal tree:

```text
quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait
```

The accompanying `fileEntryIndex` identifies the path component that belongs
to the containing `gameJournalFileEntry`. For the Lab 1 path it is `2`, the
zero-based position of `cqa001`:

```text
0: quests
1: minor_quest
2: cqa001
```

It is not the objective's index, a graph node ID, or a CR2W handle.

## Names are typed

Plain text in WolvenKit can represent several serialized types:

```text
"Out1"                                  CName
"mod\cqa\...\cqa001.questphase"         ResourcePath
"#cqa_example_trigger"                  NodeRef
"Items.ExampleItem"                     TweakDBID
"cqa001_completed"                      fact name
```

Record the type beside a value when documenting it. “Set this field to
`cqa001`” is incomplete if the reader cannot tell whether the field expects a
path, CName, fact, journal ID, or record ID.

## Scene IDs are not one pool

Scenes add several numeric domains: scene graph nodes, actors, performers,
screenplay items, localization strings, localization variants, and timed
events. **Observed in vanilla** patterns can constrain one of those domains,
but they do not authorize reusing the same number across all of them.

The scene section will document each domain when the corresponding object is
introduced. Until then, treat “scene ID” as an ambiguous phrase that needs a
type.
