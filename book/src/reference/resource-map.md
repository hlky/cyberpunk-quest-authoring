# Resource map

Use this page to answer two questions before editing a graph:

1. Which resource owns the missing definition or behavior?
2. Which registration or native reference makes that owner reachable?

The rows introduced by the completed Lab 1–5 projects are **Structurally
validated** with WolvenKit `8.19.0`. Advanced rows inherit the narrower label
and acceptance boundary of their linked chapter. Rows explicitly marked
**Observed in vanilla** are research surfaces rather than supplied tutorial
resources. This map adds no runtime promotion; each lab or advanced candidate's
retained record governs its exact in-game claims.

## Project and installation layers

| Project path or artifact | Owns | Installed or consumed by | Do not confuse it with |
| --- | --- | --- | --- |
| `source\archive\` | Complete CR2W resources and archived non-CR2W payloads at their intended depot paths | WolvenKit packing/deployment produces a game `.archive` | Loose ArchiveXL configuration |
| `source\resources\` | Loose framework configuration such as `<project>.archive.xl` | Deployed beside the archive to the framework's expected game path | A CR2W resource inside the archive |
| `source\raw\` | WolvenKit CR2W-JSON review artifacts for mod-owned resources | Documentation review, round trips, diagrams, and semantic comparison | Runtime payloads or the beginner authoring format |
| `*.cpmodproj` | WolvenKit project metadata and source-root configuration | WolvenKit | A depot resource or registration file |
| `*.archive` | Packed runtime payload container | Cyberpunk 2077's resource loader | Proof that ArchiveXL saw a loose registration file |
| `*.archive.xl` | ArchiveXL merge and registration instructions | ArchiveXL | The packed archive or a native soft reference |
| Lab ZIP | Downloadable checkpoint assembled from the project | Reader extraction | An installed mod; start and completed alternatives must not coexist |

The same depot path can appear as a file below `source\archive`, a
`ResourcePath` inside another CR2W, a registration value, and a runtime log
entry. A path below `source\raw` normally has an extra conversion suffix and
must not be registered.

## Native control, journal, and scene resources

| Resource | Root or decisive native type | Owns | Becomes reachable through | Coverage |
| --- | --- | --- | --- | --- |
| `*.questphase` | `questQuestPhaseResource` | Quest graph, phase interface, condition scheduling, fact/journal operations, scene and child handoff, prefab declarations | A root uses ArchiveXL `quest.phases`; an external child uses the parent's soft `phaseResource` | 1–5 |
| `*.journal` | `gameJournalResource` | The contributed journal-entry tree: quests, phases, objectives, map pins, messages, files, and related entries | ArchiveXL `journal` merge | 1–5 |
| `*.scene` | `scnSceneResource` | Actors, screenplay items, choices, timed events, ordinary or rewindable graph flow, entry/exit names, interruption policy, and animation references | A `questSceneNodeDefinition.sceneFile` soft reference; it is not a quest-root registration | Lab 5 plus advanced scenes |
| `*.scenerid` | `scnRidResource` | Recorded actor/camera tags, channel serials, animation buffers, and RID-local allocation | A scene `scnRidResourceHandler`, then scene-local RID reference arrays and timed events | Advanced braindance; structurally validated candidate, runtime **Experimental** |

Important ownership boundaries:

- A questphase journal node changes state at a typed path; it does not define
  the target entry.
- A root registration does not register external children or scenes as
  independent quest roots.
- A `.scene` owns its named `contact_done` exit; the calling questphase owns
  the same-named output socket and the continuation after it.
- Termination ends a graph route. It does not automatically clean a marker,
  community, scene, journal entry, or fact.

See [Questphase resource anatomy](../questphases/anatomy.md), [Journal trees
and typed paths](../journal/trees-and-paths.md), and [Scene resource
anatomy](../scenes/resource-anatomy.md).

## Localization and audio resources

Several different CR2W resource types use the depot suffix `.json`. Inspect
the root type and registration branch instead of treating the suffix as an
ownership contract.

| Player-facing content | Resource type | Owns the decisive lookup | Registration or reference |
| --- | --- | --- | --- |
| Journal and onscreen UI | `JsonResource` containing `localizationPersistenceOnScreenEntries` | Text entries keyed by textual `secondaryKey` | ArchiveXL `localization.onscreens.<locale>` |
| Spoken subtitles: map | `JsonResource` containing `localizationPersistenceSubtitleMap` | Map entries whose `subtitleFile` points to subtitle-entry resources | ArchiveXL `localization.subtitles.<locale>` |
| Spoken subtitles: entries | `JsonResource` containing `localizationPersistenceSubtitleEntries` | Subtitle text keyed by unsigned `stringId` | Reached through the registered subtitle map; not registered in its place |
| Spoken voice: map | `JsonResource` containing `locVoiceoverMap` | `locVoLineEntry` rows joining the same `stringId` to female/male audio paths | ArchiveXL `localization.vomaps.<locale>` |
| Spoken voice: audio | `*.wem` | Cooked audio bytes | Archived at the `femaleResPath` / `maleResPath` named by the VO map |
| Scene choice text | Embedded `scnlocLocStoreEmbedded` inside `*.scene` | Descriptor/payload tables joined from screenplay choice RUIDs | No ArchiveXL localization branch; the scene owns it |

The subtitle map and VO map are registration roots. The subtitle-entry file
and WEM are referenced leaves. Registering a leaf where a map is expected
does not complete the lookup.

For the complete joins and locale spelling differences, use [Localization
paths](../journal/localization-paths.md). Lab 5's externally localized one-line
route is explained in [Author one spoken line](../scenes/one-spoken-line.md).

## World and streaming resources

| Resource | Root or decisive native type | Owns | Becomes reachable through | Evidence boundary |
| --- | --- | --- | --- | --- |
| `*.streamingblock` | `worldStreamingBlock` | Sector descriptors, sector paths, streaming boxes, categories, levels, and quest-prefab roots | ArchiveXL `streaming.blocks` | Lab 3–5 shapes are **Structurally validated** |
| `*.streamingsector` | `worldStreamingSector` | Concrete world nodes, placement/cooked metadata, registered NodeRefs, and references to inplace content | `worldStreamingSectorDescriptor.data` in a registered block | Lab 3–5 compact shapes are **Structurally validated** |
| `*.streamingsector_inplace` | `worldStreamingSectorInplaceContent` | An `inplaceResources[]` collection with corresponding embedded CR2W bodies represented separately in the serialized container | A sector's local or external inplace-resource relationship | **Observed in vanilla** here; not supplied by Labs 1–5 |
| Base `*.streamingworld` | `worldStreamingWorld` | References compiled blocks and broader global world resources | Game-owned world root | **Observed in vanilla**; inspect, do not replace or redistribute |

The compact placed-node chain used by the labs is:

```text
registered streaming block
  -> descriptor.data
  -> streaming sector
  -> concrete nodes[] object
  +  nodeData placement and QuestPrefabRefHash
  +  nodeRefs[] identity registration
```

The three sector collections are related but not universally parallel.
`nodeData.NodeIndex` is the explicit association in the compact mod-owned
shape; array position is not a schema rule. See [Sector nodes and
placement](../world/sector-nodes-and-placement.md).

## Community and character resources

Lab 5 embeds its community template data in a world registry node rather than
shipping a standalone `.community` resource.

| Owner | Native type or resource | Responsibility | Discovery path |
| --- | --- | --- | --- |
| Registry node | `worldCommunityRegistryNode` in an AlwaysLoaded sector | Community template, initial entry state, persistent AI-spot data, and the registry side of the community identity join | Concrete sector node plus placement/identity records |
| Compiled area | `worldCompiledCommunityAreaNode_Streamable` in a Quest sector | Streamed source placement and entry/phase/time-period mirror to AI-spot IDs | Concrete sector node plus placement/identity records |
| Community entry | `communitySpawnEntry` inside `communityCommunityTemplateData` | Entry CName, character TweakDB record, quantity, and spawn phases | Embedded in the Lab 5 registry item |
| Spawn phase | `communitySpawnPhase` and `communityPhaseTimePeriod` | Phase, appearance, period, sequencing, and spot references | Embedded beneath the community entry |
| AI spot | `worldAISpotNode` containing `AIActionSpot` | Placed activity and soft workspot resource path | Quest sector placement and NodeRef registration |
| Standalone community | `*.community` rooted at `communityCommunityTemplate` | Reusable community template data in the cited vanilla examples | **Observed in vanilla** comparison source; not a Lab 5 dependency |
| Character record | `TweakDBID` such as `Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa` | Gameplay record that leads onward to a character/template dependency chain | TweakDB; it is not a depot path |
| Entity template | `*.ent`, commonly rooted at `entEntityTemplate` | Template-specific components, slots, appearances, interactions, and other entity composition | Referenced from records or world entity nodes; advanced authoring is bounded by the compatible mod-owned-shell requirement |
| Appearance resource | `*.app` rooted at `appearanceAppearanceResource` | Internal appearance definitions and their component graphs | An entity template's exposed appearance mapping; advanced custom behavior remains **Experimental** |
| Workspot | `*.workspot` | Referenced activity/animation behavior | `worldAISpotNode.spot.resource`; the AI spot still owns placement |

The exact Lab 5 join is developed in [Registries and compiled
areas](../communities/registries-and-areas.md) and [Entries, phases, and AI
spots](../communities/entries-phases-and-ai-spots.md). The advanced chain and
its legal-shell boundary are in [Character records, entities, and
appearances](../communities/character-records-entities-and-appearances.md),
while [AI roles, behavior, and
workspots](../communities/ai-roles-behavior-and-workspots.md) separates actor,
role, route, and activity ownership. Never add an extracted vanilla CR2W to a
downloadable project.

## Referenced world and device surfaces

These owners form the advanced device research model. Their linked procedure
is complete as an **Experimental** authoring and acceptance boundary, not as a
generic **Runtime-proven** custom-device recipe:

| Surface | Owner | Boundary |
| --- | --- | --- |
| Placed entity or device | `worldEntityNode` or `worldDeviceNode` | Refers to an entity template and may carry node-local `instanceData` |
| Node-local controller/component state | `entEntityInstanceData` leading to a `RedPackage` | Different from sector inplace content |
| Global device tables | `*.devices` and `*.psrep` | Context-dependent; absence from one focused vanilla flow is not a universal no-registration rule |
| Persistent device identity | Save plus world identity/NodeRef | A materially changed device may require both a clean save and deliberate identity policy |

See [Devices and persistence](../world/devices-and-persistence.md) and
[Advanced devices and
interactions](../world/advanced-devices-and-interactions.md) before using any
of these surfaces. The current Labs 1–5 do not supply a custom device.

## Registration versus native reference

This is the quickest lookup for “which file do I put in ArchiveXL?”

| Target | ArchiveXL registration? | Native reference that reaches non-root dependencies |
| --- | --- | --- |
| Registered root questphase | Yes: `quest.phases` | Parent is `base\quest\cyberpunk2077.quest` |
| External child questphase | No independent root entry | Parent `questPhaseNodeDefinition.phaseResource` |
| Journal contribution | Yes: `journal` | Quest nodes then use typed `gameJournalPath` values |
| Onscreen localization | Yes: `localization.onscreens.<locale>` | Journal/UI `LocalizationString.value` joins to `secondaryKey` |
| Subtitle map | Yes: `localization.subtitles.<locale>` | Map entry `subtitleFile` reaches subtitle entries |
| Subtitle entries | No direct registration in this route | Registered subtitle map |
| VO map | Yes: `localization.vomaps.<locale>` | Its line entries reach WEM resource paths |
| WEM | No direct registration | VO-map `femaleResPath` / `maleResPath` |
| Streaming block | Yes: `streaming.blocks` | Its descriptors reach sectors |
| Streaming sector | No separate block registration | Descriptor `data` resource reference |
| Scene | No quest-root registration | `questSceneNodeDefinition.sceneFile` |
| Scene RID or animation-set leaf | No independent quest-root registration | Scene RID handlers and `resouresReferences` arrays |
| Mod-owned character record | Not through ArchiveXL; use the locally pinned TweakXL `1.11.3` route | Record `entityTemplatePath` reaches the archived `.ent` |
| Mod-owned entity/appearance resource | Archived at a unique depot path; no root merge | Character record reaches `.ent`; entity appearance mapping reaches `.app` |
| Vanilla workspot or animation set | No new registration in the taught route | AI spot or scene resource-reference path |

## Save-state overlay

Resource ownership and saved runtime state overlap but are not the same layer:

| Definition in installed resources | State that can remain in the save |
| --- | --- |
| Fact names and graph writers/readers | Current fact integer values |
| Journal entries and typed paths | Active, inactive, succeeded, failed, visited, and tracking state |
| Questphase nodes and edges | Active phase work and checkpoints |
| Scene graph, actors, and exits | Active or completed scene state |
| Community registry, area, and spots | Activation and actor lifecycle state |
| Device template and instance data | Persistent controller/device state associated with identity |

Repacking a definition cannot be used as evidence that the corresponding
saved state was reset. Route stale or contradictory retests through [Facts,
journals, and saves](../foundations/persistent-state.md) before changing more
resource fields.
