# Glossary

This glossary defines the terms used by the book. It is intentionally about
native Cyberpunk 2077 resources and runtime systems. Names used only by a
research tool are not part of the reader vocabulary.

The short definitions below route to the chapter that owns the complete
contract. When a term names a resource shape, its runtime behavior still
inherits the evidence label and version boundary stated by that chapter.

## A–C

| Term | Meaning | Continue with |
| --- | --- | --- |
| **Acceptance gate** | A retained, hash-bound test record that controls whether a bounded claim remains **Experimental** or can become **Runtime-proven**. It is a promotion mechanism, not a fifth evidence label. | [Lifecycle, cleanup, and evidence](../foundations/lifecycle-and-evidence.md) |
| **Actor** | A scene role declared with `scnActorDef` or `scnPlayerActorDef`. Its `scnActorId` is scene-local and is not a performer ID, community ID, or TweakDB record. | [Actors and performers](../scenes/actors-and-performers.md) |
| **AI spot** | A placed `worldAISpotNode` whose `AIActionSpot` refers to a workspot resource. Placement, world identity, workspot behavior, and actor selection have separate owners. | [Entries, phases, and AI spots](../communities/entries-phases-and-ai-spots.md) |
| **Archive** | The packed `.archive` that carries CR2W resources and other archived payloads at depot paths. Its existence does not prove that a loose ArchiveXL registration file was installed. | [Resources and ownership](../foundations/resource-model.md) |
| **ArchiveXL registration** | Loose configuration that attaches or merges a mod-owned resource at the appropriate game root, such as `quest.phases`, `journal`, localization, or `streaming.blocks`. It is different from a native soft reference between archived resources. | [Registering a root questphase](../questphases/root-registration.md) |
| **Child questphase** | A questphase invoked by a `questPhaseNodeDefinition` in another phase. The external-child form used in Labs 4–5 is archived at its depot path and resolved through `phaseResource`; it is not independently attached to the game quest root. | [Calling child phases](../questphases/child-phases.md) |
| **Clean save** | For the book's focused start tests, a manual save made before any version of the candidate quest was installed or registered. Resetting a fact does not clear all journal, phase, scene, community, or device state. | [Facts, journals, and saves](../foundations/persistent-state.md) |
| **CName** | A REDengine name token used for values such as socket names, entry points, community entries, and phases. A CName that prints as text is not therefore a fact, depot path, NodeRef, or TweakDBID. | [Identifier domains](../foundations/identifier-domains.md) |
| **Community** | The native world-side system that combines registry template data, a compiled area, entries, phases, AI spots, and quest-controlled activation to materialize actors. A scene can acquire an available community entry but does not create the community. | [Communities and characters](../communities/index.md) |
| **Compiled community area** | A streamed `worldCompiledCommunityAreaNode_Streamable` that places a community source and mirrors its entry/phase/time-period route to world-global AI-spot identities. | [Registries and compiled areas](../communities/registries-and-areas.md) |
| **Condition** | In graph prose, an immediate `questConditionNodeDefinition` that evaluates its predicate on entry and selects a result such as `True` or `False`. The nested condition object decides what is tested. | [Immediate branches and waiting gates](../gates/immediate-and-waiting.md) |
| **Condition payload** | The typed predicate beneath a Condition or Pause Condition node, often represented as a domain wrapper plus a concrete `type` handle. For example, `questFactsDBCondition` wraps `questVarComparison_ConditionType`. | [Condition payloads](../gates/condition-payloads.md) |
| **Connection** | A `graphGraphConnectionDefinition` joining one source output socket to one destination input socket in a quest graph. Reciprocal handle references from both sockets still describe one edge. | [Graph execution](../foundations/graph-execution.md) |
| **CR2W** | REDengine's typed resource container used by questphases, journals, scenes, world resources, and many referenced assets. A successful parse or save proves structure was accepted, not that external references resolve in game. | [Resources and ownership](../foundations/resource-model.md) |
| **CR2W handle** | A serialization-local `HandleId` / `HandleRefId` relationship between objects in one CR2W object graph. It is not a quest node ID or NodeRef. | [Identifier domains](../foundations/identifier-domains.md) |
| **CR2W-JSON** | WolvenKit's serialized review form for a CR2W resource. The book uses it for deterministic inspection and figures; readers author CR2W resources through WolvenKit rather than treating raw JSON editing as the beginner workflow. | [Exact graph contract](graph-contract.md) |
| **Cut** | An explicit interruption route from a `CutSource` to one or more `CutDestination` sockets. The presence of cut sockets does not establish cleanup, rollback, re-entry, or propagation behavior. | [Parallel monitors and cancellation](../gates/monitors-and-cancellation.md) |

## D–L

| Term | Meaning | Continue with |
| --- | --- | --- |
| **Depot path** | A resource address in the game's virtual depot, written with backslashes, such as `mod\cqa\cqa005\scenes\cqa005_first_contact.scene`. It is not a Windows filesystem path. | [Resources and ownership](../foundations/resource-model.md) |
| **Descriptor** | In the streaming chapters, a `worldStreamingSectorDescriptor` in a block. Its `data` points to a sector and its other fields carry streaming metadata such as bounds, category, level, and an optional quest-prefab root. | [Streaming model](../world/streaming-model.md) |
| **Entry point** | A named `.scene` interface entry that maps a CName such as `start` to an `scnNodeId`. The caller's `questSceneNodeDefinition` must expose a same-named input socket. | [Entry, exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md) |
| **Evidence label** | One of exactly four claim classes: **Runtime-proven**, **Structurally validated**, **Observed in vanilla**, or **Experimental**. | [Claim labels](#claim-labels) |
| **External child** | The Lab 4–5 child-phase arrangement in which `phaseGraph` is null and `phaseResource` softly names another archived `.questphase`. It contrasts with an inline/in-place graph. | [Questphase resource anatomy](../questphases/anatomy.md) |
| **Fact** | A named signed-integer slot in the facts database. Authors commonly use `0` and `1` by convention, but the resource does not turn the fact into a Boolean. | [Facts, journals, and saves](../foundations/persistent-state.md) |
| **Fan-out** | Several connections leaving one output socket. It starts several downstream routes and does not establish an order or a later join. | [Graph execution](../foundations/graph-execution.md) |
| **Graph-local node ID** | The numeric `id` of a node inside one questphase or scene graph. Its scope must be recorded; another graph may reuse the same number. It is independent of CR2W handle allocation. | [Identifier domains](../foundations/identifier-domains.md) |
| **Inplace resource** | A resource stored or referenced through a containing resource rather than addressed as the same kind of standalone owner. Questphase `inplacePhases`, sector `.streamingsector_inplace` content, and node-local `instanceData` are separate domains despite the shared word. | [Sector nodes and placement](../world/sector-nodes-and-placement.md) |
| **Journal entry** | A typed object in the merged journal tree, such as a quest, phase, objective, map pin, message, file, or onscreen. Its authored definition is separate from its save-backed runtime state. | [Journal trees and typed paths](../journal/trees-and-paths.md) |
| **Journal path** | A typed `gameJournalPath` containing `realPath`, `className`, `fileEntryIndex`, and `editorPath`. It identifies an entry in the merged journal tree, not a depot resource or CR2W object. | [Journal trees and typed paths](../journal/trees-and-paths.md) |
| **Join** | A graph topology where several execution routes converge. The RED node type and retained runtime evidence determine whether it waits, passes through, remembers arrivals, resets, or restores across saves. | [Signal flow](../gates/signal-flow.md) |
| **Localization key** | The identifier used by one localization system. Journal/UI secondary keys, spoken-line RUIDs, and embedded scene-choice RUIDs belong to different lookup paths. | [Localization paths](../journal/localization-paths.md) |
| **Locstring RUID** | The unsigned `scnlocLocstringId.ruid` used by a scene line or choice. For spoken lines it joins the scene to subtitle and VO records; it is not a screenplay item ID. | [Localization paths](../journal/localization-paths.md) |

## M–R

| Term | Meaning | Continue with |
| --- | --- | --- |
| **Mappin** | Map/HUD presentation backed by a typed journal entry and, for the quest-pin route taught here, a world marker NodeRef. The journal pin, world marker, and quest manager node are separate owners. | [Mappins: journal intent meets the world](../journal/mappins.md) |
| **Native quest resource** | The game's own quest, scene, journal, localization, world, community, and related resource model. In this book, “native” does not mean RED4ext native-plugin development. | [Resources and ownership](../foundations/resource-model.md) |
| **NodeRef** | A typed world reference used to address a registered world object or a child beneath a quest-prefab root. It is not a CR2W handle, ResourcePath, or TweakDBID. | [Quest prefabs and NodeRefs](../world/quest-prefabs-and-noderefs.md) |
| **Node data** | A sector placement record, commonly `worldNodeData`, that carries transform, bounds, streaming metadata, `NodeIndex`, and `QuestPrefabRefHash`. It is distinct from the concrete node and `nodeRefs[]` registration. | [Sector nodes and placement](../world/sector-nodes-and-placement.md) |
| **Ordinals** | Node-local values used to distinguish ordered sockets, options, or scene socket stamps. They do not define execution order for the whole graph. | [Graph execution](../foundations/graph-execution.md) |
| **Pause Condition** | A `questPauseConditionNodeDefinition` that retains one execution path until its predicate is fulfilled, then emits `Out`. It is not an immediate false branch. | [Immediate branches and waiting gates](../gates/immediate-and-waiting.md) |
| **Performer** | A scene debug-symbol identity represented by `scnPerformerId`. It helps map editor-facing performer information but cannot replace the `scnActorId` used by screenplay and actor behavior. | [Actors and performers](../scenes/actors-and-performers.md) |
| **Phase prefab** | A `questQuestPrefabEntry` in a questphase's `phasePrefabs` array. It declares a quest-prefab root available to that composition; it does not place the referenced world content. | [Prefab dependencies](../questphases/prefab-dependencies.md) |
| **Quest prefab** | The world-reference namespace rooted at a prefab NodeRef and bound through a Quest-sector descriptor. In the workflow taught here it does not imply that a standalone `.prefab` file exists. | [Quest prefabs and NodeRefs](../world/quest-prefabs-and-noderefs.md) |
| **Questphase** | A `.questphase` CR2W resource rooted at `questQuestPhaseResource`. It coordinates execution, conditions, journal operations, facts, scenes, world references, and child phases; it does not create those external resources. | [Questphase resource anatomy](../questphases/anatomy.md) |
| **Race** | Several active execution routes converging on a winner-shaped node. An XOR-shaped topology is not evidence that losing listeners are automatically cancelled. | [Signal flow](../gates/signal-flow.md) |
| **ResourcePath** | The typed serialized value used to address another depot resource. A soft ResourcePath is a reference-loading policy, not ArchiveXL registration. | [Identifier domains](../foundations/identifier-domains.md) |
| **Root questphase** | The composition root attached beneath `base\quest\cyberpunk2077.quest` through ArchiveXL. A root still needs explicit re-entry, completion, and termination policy. | [Registering a root questphase](../questphases/root-registration.md) |

## S–W

| Term | Meaning | Continue with |
| --- | --- | --- |
| **Save-backed state** | Runtime state retained independently of a later archive edit, including facts, journal state, active quest work, scenes, communities, and some device state. | [Facts, journals, and saves](../foundations/persistent-state.md) |
| **Scene** | A `.scene` CR2W resource rooted at `scnSceneResource`. It owns actors, screenplay, timed events, graph flow, entry/exit names, interruption policy, and referenced animation data. | [Scene resource anatomy](../scenes/resource-anatomy.md) |
| **Screenplay item** | A line or option in `scnscreenplayStore`, identified by `scnscreenplayItemId`. A timed event points to a line item; the line separately points to its localization RUID. | [Screenplay, sections, and events](../scenes/screenplay-sections-and-events.md) |
| **Socket** | A named quest-graph connection point with a role such as `Input`, `Output`, `CutSource`, or `CutDestination`. The name and the node type together define its local meaning. | [Node and socket index](node-and-socket-index.md) |
| **Socket stamp** | A scene-graph name/ordinal pair used to connect scene nodes. It is a different representation from `questSocketDefinition` even when both are discussed as graph ports. | [Entry, exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md) |
| **Soft reference** | A resource reference whose flags are `Soft`, such as an external child `phaseResource` or a scene `sceneFile`. It still requires the target at the exact depot path and does not register it as a root. | [Calling child phases](../questphases/child-phases.md) |
| **Streaming block** | A `worldStreamingBlock` whose descriptors point to sectors and carry their streaming metadata. ArchiveXL registers the block, not each sector separately. | [Streaming model](../world/streaming-model.md) |
| **Streaming sector** | A `worldStreamingSector` that owns or references concrete world nodes, placement records, and registered NodeRefs. Its arrays are not universally parallel. | [Sector nodes and placement](../world/sector-nodes-and-placement.md) |
| **Terminating output** | A `questOutputNodeDefinition` whose output type is `Terminating`. Reaching it ends that phase route; it does not automatically reset state or clean external systems. | [Inputs and outputs](../questphases/inputs-and-outputs.md) |
| **TweakDBID** | A typed identifier for a gameplay record in TweakDB, such as a character record. It is not an `.ent` depot path or a world NodeRef. | [Entries, phases, and AI spots](../communities/entries-phases-and-ai-spots.md) |
| **WEM** | A cooked audio payload resolved from a voiceover-map resource path. The WEM is archived, while the VO map is the ArchiveXL registration root for the spoken-audio branch. | [Author one spoken line](../scenes/one-spoken-line.md) |
| **WolvenKit** | The editor and resource tool used by the reader to inspect, author, convert, pack, and deploy the resource shapes taught by the book. Documentation-author scripts are not reader prerequisites. | [Set up from zero](../start-here/setup.md) |
| **Workspot** | A referenced resource that supplies an AI activity or animation setup. A `worldAISpotNode` supplies placement and points to it; the workspot does not choose the community actor or world transform. | [Entries, phases, and AI spots](../communities/entries-phases-and-ai-spots.md) |

## Claim labels

Use the narrowest label supported by the retained evidence:

| Label | Meaning |
| --- | --- |
| **Runtime-proven** | The stated bounded behavior or result was observed in game for the exact retained arrangement. The observed result can be a success or a failure; a failed campaign remains **Experimental** for the intended behavior that did not occur. The claim remains bounded by its versions, hashes, save lineage, and tested cases. |
| **Structurally validated** | The resource serialized, round-tripped, and passed the stated structural checks, but the claimed runtime behavior has not been established for that arrangement. |
| **Observed in vanilla** | The focused shape occurs in one or more cited game resources. It is a research precedent, not automatic proof that a new mod-owned arrangement works. |
| **Experimental** | The investigation, resource contract, or required runtime acceptance remains incomplete. |

One page can contain all four labels for different claims. Never promote a
whole node family because one specific fixture passed, and never demote a
focused vanilla observation merely because a new custom arrangement remains
**Experimental**.
