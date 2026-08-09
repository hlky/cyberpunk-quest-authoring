# Questphase resource anatomy

A `.questphase` file is a CR2W resource whose root chunk is
`questQuestPhaseResource`. Its executable graph is only one part of that root.

## The outer resource

These focused excerpts show the two completed Lab 4 phase resources.
Serialization metadata and handle details are omitted:

```text
cqa004.questphase
questQuestPhaseResource
├── cookingPlatform: PLATFORM_PC
├── graph: questGraphDefinition
│   └── nodes: [12 nodes]
├── inplacePhases: []
└── phasePrefabs:
    └── questQuestPrefabEntry
        └── prefabNodeRef: #cqa004_pr_handoff

cqa004_boundary.questphase
questQuestPhaseResource
├── cookingPlatform: PLATFORM_PC
├── graph: questGraphDefinition
│   └── nodes: [10 nodes]
├── inplacePhases: []
└── phasePrefabs: []
```

| Property | Supported interpretation |
| --- | --- |
| `cookingPlatform` | Target cooking platform recorded by the resource |
| `graph` | Handle to the executable `questGraphDefinition` |
| `inplacePhases` | Storage associated with inline/in-place phases; empty in Labs 1–4 |
| `phasePrefabs` | Quest-prefab roots declared by this resource; the exact active composition determines which descendants can resolve against that scope |

**Structurally validated:** Lab 4's root contains one prefab entry and its
external child contains none. Empty arrays are meaningful serialized values,
not omitted work and not a universal rule.

## The graph

`questGraphDefinition.nodes` contains handles to node definitions. Each node
definition has:

- a graph-local integer `id`;
- one or more `questSocketDefinition` objects;
- properties specific to its node type.

Connections are stored from a source socket to a destination socket. The
corresponding socket objects retain the connection handle, so a valid
serialized graph must be internally consistent in both directions.

```text
source node
  output questSocketDefinition
    graphGraphConnectionDefinition
      source      -> that output socket
      destination -> input socket on destination node
```

The graph-local `id` is the useful identity when discussing behavior.
`HandleId` and `HandleRefId` are CR2W serialization references and can change
during a WolvenKit round trip. See
[Identifier domains](../foundations/identifier-domains.md) before comparing raw
exports.

## Nodes are typed records

Common fields do not make all nodes interchangeable. A condition node has a
condition payload and branch sockets; a journal node has a typed journal
operation and path; a phase node has either an external resource reference or
an inline graph arrangement.

Lab 4 uses these types across its two graphs:

| Node type | Decisive payload |
| --- | --- |
| `questInputNodeDefinition` | Exposed phase input name |
| `questOutputNodeDefinition` | Exposed phase output name and output type |
| `questConditionNodeDefinition` | Immediate completion-fact comparison |
| `questJournalNodeDefinition` | Journal entry type, path, and incoming state socket |
| `questPauseConditionNodeDefinition` | Realtime delay or state-shaped trigger condition |
| `questMappinManagerNodeDefinition` | Journal map-pin path and active/inactive operation |
| `questFactsDBManagerNodeDefinition` | Exact fact write operation |
| `questPhaseNodeDefinition` | External child path, interface sockets, and instance fields |

The [Lab 4 overview](lab-04.md#exact-root-phase) explains every supplied node.
The raw WolvenKit JSON beside each completed project is a review artifact, not
a second reader authoring format.

## Anatomy of an external phase node

Lab 4's parent node uses this focused shape:

```text
questPhaseNodeDefinition
├── id: 13
├── phaseGraph: null
├── phaseInstancePrefabs: []
├── phaseResource:
│   ├── DepotPath: mod\cqa\cqa004\phases\cqa004_boundary.questphase
│   └── Flags: Soft
├── saveLock: 0
├── sockets: [CutDestination, In1, Out1]
└── unfreezingTriggerNodeRef: 0
```

`phaseGraph: null` distinguishes this focused external-child shape from an
inline graph. The soft depot path is not ArchiveXL registration. It is the
parent resource's reference to another archived CR2W resource.

`saveLock: 0` and a zero unfreezing ref are exact values in the inspected
shape. Their broader behavior is not inferred here. Lab 4 also leaves
`CutDestination` unwired because the runtime semantics of a complete cut and
recovery route remain **Experimental**.

## Sockets carry semantics

A socket is not merely a visual port. Its name and type tell the runtime how
execution enters, branches, or leaves a node.

```text
name: "Active"          type: Input
name: "True"            type: Output
name: "Out1"            type: Output
name: "CutDestination"  type: CutDestination
```

The layer matters. The child input node exposes interface name `In1`, then
emits internal graph flow through `Out`. The child's terminating output node
accepts internal flow through `In`, then exposes interface name `Out1` to its
parent. The parent phase node has its own `In1` and `Out1` sockets to match.

`CutDestination` belongs to interruption routing and is not an ordinary
success edge. Structural presence alone does not prove runtime cut behavior.

## Inspect without over-reading

When reviewing a `.questphase`:

1. Confirm `RootChunk.$type` is `questQuestPhaseResource`.
2. Confirm `graph.Data.$type` is `questGraphDefinition`.
3. Inventory every node by graph-local `id` and RED type.
4. Record each connected source socket and destination socket.
5. Inspect only the properties decisive for that node's behavior.
6. Review `inplacePhases`, root `phasePrefabs`, and every phase node's
   `phaseInstancePrefabs` separately.
7. For an external child, confirm `phaseGraph` is null and the soft
   `phaseResource` path resolves to an archived CR2W file.
8. Match the parent phase-node interface to child input/output node names.
9. Round-trip each binary and compare semantics, not raw handle numbering.

A successful parse is **Structurally validated** evidence. It does not prove
that the game resolves the path, preserves an active child through reload, or
returns control to the parent.

Previous: [Questphases](index.md). Next: [Registering a root
questphase](root-registration.md).
