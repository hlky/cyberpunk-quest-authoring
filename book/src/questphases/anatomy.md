# Questphase resource anatomy

A `.questphase` file is a CR2W resource whose root chunk is
`questQuestPhaseResource`. Its executable graph is only one part of that root.

## The outer resource

This focused excerpt describes the top level of the completed Lab 1 resource.
Serialization metadata and handle details are omitted:

```text
questQuestPhaseResource
├── cookingPlatform: PLATFORM_PC
├── graph: questGraphDefinition
│   └── nodes: [...]
├── inplacePhases: []
└── phasePrefabs: []
```

| Property | Role in this book |
| --- | --- |
| `cookingPlatform` | Target cooking platform recorded by the resource |
| `graph` | Handle to the executable `questGraphDefinition` |
| `inplacePhases` | Storage associated with inline/in-place phases; empty in Lab 1 |
| `phasePrefabs` | Quest-prefab roots used directly by this phase; empty in Lab 1 |

**Structurally validated:** Lab 1 uses a non-null graph, no in-place phases,
and no prefab dependencies. That is the smallest shape needed for its
location-independent fact, delay, and journal flow. Empty arrays are not a
universal rule for questphases.

## The graph

`questGraphDefinition.nodes` contains handles to node definitions. Each node
definition has:

- a graph-local integer `id`;
- one or more `questSocketDefinition` objects;
- properties specific to its node type.

Connections are stored from a source socket to a destination socket. The
corresponding socket objects also retain the connection handle, so a valid
serialized graph must be internally consistent in both directions.

```text
source node
  output questSocketDefinition
    graphGraphConnectionDefinition
      source      -> that output socket
      destination -> input socket on destination node
```

The `id` is the useful identity when discussing the graph. `HandleId` and
`HandleRefId` are CR2W serialization references and can change during a
WolvenKit round trip. See [Identifier domains](../foundations/identifier-domains.md)
before reviewing a raw export.

## Nodes are typed records

The common fields do not make all nodes interchangeable. A condition node has
a condition payload and branch sockets; a journal node has a typed journal
operation and path; a phase node has a child resource reference.

For example, Lab 1 contains these graph-level roles:

| Node type | Type-specific payload |
| --- | --- |
| `questInputNodeDefinition` | Exposed phase input name |
| `questConditionNodeDefinition` | Immediate fact comparison |
| `questJournalNodeDefinition` | Journal entry type, path, and incoming state socket |
| `questPauseConditionNodeDefinition` | Realtime delay condition |
| `questFactsDBManagerNodeDefinition` | Exact fact write operation |
| `questOutputNodeDefinition` | Exposed phase output name and output type |

The [exact Lab 1 graph](../start-here/lab-01.md#exact-questphase) explains every
supplied node. The raw WolvenKit JSON beside the completed project is a review
artifact, not a second authoring format.

## Sockets carry semantics

A socket is not merely a visual port. Its name and type tell the runtime how
execution enters or leaves a node.

```text
name: "Active"   type: Input
name: "True"     type: Output
name: "Out"      type: Output
name: "CutDestination" type: CutDestination
```

For journal nodes, entering `Active` requests that journal state. For a
condition, `True` and `False` are different results. `CutDestination` belongs
to interruption routing and is not an ordinary success edge.

The graph editor can make the topology easier to inspect, but the serialized
node type, socket name, socket type, and type-specific properties form the
actual contract.

## Inspect without over-reading

When reviewing a `.questphase`:

1. Confirm `RootChunk.$type` is `questQuestPhaseResource`.
2. Confirm `graph.Data.$type` is `questGraphDefinition`.
3. Inventory every node by graph-local `id` and RED type.
4. Record each connected source socket and destination socket.
5. Inspect only the properties decisive for that node's behavior.
6. Review `inplacePhases` and `phasePrefabs` instead of assuming they are empty.
7. Round-trip the binary and compare semantics, not raw handle numbering.

A successful parse proves structure. It does not prove that external depot
paths resolve or that the game executes the intended lifecycle.
