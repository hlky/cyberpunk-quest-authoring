# Communities and characters

A community is the native world-side system that turns a character record and
one or more AI spots into actors that quest logic can activate, wait for, hand
to a scene, and eventually deactivate. No single resource owns that complete
lifecycle:

```text
always-loaded community registry
  + streamed compiled community area
  + streamed AI spot and workspot
  + questphase activation and readiness gate
  + scene actor acquisition
  + delayed questphase cleanup
```

Treat those as cooperating owners. A valid `TweakDBID` does not place an actor,
an AI spot does not activate its community, and a scene actor definition does
not spawn the character it intends to acquire.

Advanced characters add two more chains without replacing the community:

```text
Character record -> .ent exposed mapping -> .app internal definition

spawned community actor -> Gameplay AI tier -> temporary role/workspot
  -> observed result -> scene/phase/cleanup handoff
```

The first controls gameplay defaults and renderable presentation. The second
temporarily changes what one spawned actor is doing. Neither should borrow a
story-unique character or mutate a shared vanilla resource.

The beginner-safe lifecycle is:

```text
Activate community
  -> wait for CharacterSpawned
  -> enter a broad setup area
  -> start the scene
  -> acquire the community entry
  -> consume the named scene outcome
  -> advance outcome-specific journal or branch state
  -> wait until V leaves a cleanup area
  -> Deactivate community
  -> complete the owning phase and its terminal one-shot state
```

The order is part of the design. Starting the scene immediately after
`Activate` creates a race between actor materialization and scene acquisition.
Deactivating on the scene's last spoken line can remove an actor while the
scene, AI, or workspot still owns it.

## Native ownership map

| Owner | Responsibility |
| --- | --- |
| `worldCommunityRegistryNode` | Makes community template data and initial entry state available independently of the local streamed area. |
| `worldCompiledCommunityAreaNode_Streamable` | Places the community source in the streamed world and mirrors which entry/phase/time period uses which AI-spot identities. |
| `worldAISpotNode` | Places an `AIActionSpot` and names the workspot resource an actor can use there. |
| `communitySpawnEntry` | Associates one community entry name with a character `TweakDBID` and one or more spawn phases. |
| `communitySpawnPhase` | Selects the phase name, appearance set, and time-period behavior for that entry. |
| `Character.*` TweakDB record | Selects the entity template and supplies inherited reaction, faction, action-map, archetype, equipment, voice, and other gameplay defaults. |
| `entEntityTemplate` | Owns the puppet scaffold, root components, default exposed appearance, and exposed-to-internal appearance mappings. |
| `appearanceAppearanceResource` | Owns internal appearance definitions, component graphs, frame type, and render/runtime dependencies. |
| `questSpawnManagerNodeDefinition` | Sends `Activate` or `Deactivate` to a community reference; it does not prove the actor already exists or is gone. |
| `questCharacterSpawned_ConditionType` | Waits for the configured spawned-character comparison to become true. |
| `questPuppetAIManagerNodeDefinition` | Requests an AI/story tier for selected spawned actors. |
| `questMiscAICommandNode` | Carries a typed AI command such as follower/patrol role assignment or role clear. |
| `questUseWorkspotNodeDefinition` | Issues a direct workspot command to an actor; its output does not replace state observation. |
| `scnActorDef` with `acquisitionPlan: community` | Acquires an already available community entry for scene performance. |
| Save | Retains quest, scene, community, and actor-related state that can invalidate a dirty retest. |

This builds on the [resource model](../foundations/resource-model.md),
[identifier domains](../foundations/identifier-domains.md), [world streaming
model](../world/streaming-model.md), and [persistent
state](../foundations/persistent-state.md).

## Three world identity domains

The retained compact community shape places three numeric identity domains
beside one another:

1. the community/source identity shared by the compiled area's
   `sourceObjectId` and its registry item's `communityId`;
2. the separate world-node identity of the registry node itself;
3. one separate world-global identity for every AI spot.

They must not be collapsed because all three can appear as 64-bit values. The
AI spot's full `NodeRef`, the community entry's `CName`, and its character
record's `TweakDBID` are additional typed identities. A debug name is none of
them.

[Registries and compiled areas](registries-and-areas.md) explains the exact
joins and the collision that motivated this rule.

## Reading route

Read these chapters in order:

1. [Registries and compiled areas](registries-and-areas.md) — where template
   data lives, how a streamed source meets its registry item, and why registry,
   source, and spot identities stay separate.
2. [Entries, phases, and AI spots](entries-phases-and-ai-spots.md) — how an
   entry selects a character record, appearance, time period, and placed
   workspot.
3. [Activation, readiness, and acquisition](activation-readiness-and-acquisition.md)
   — why `Activate`, `CharacterSpawned`, broad setup, and scene acquisition
   are four different lifecycle steps.
4. [Cleanup and character safety](cleanup-and-character-safety.md) — delayed
   deactivation, save-aware tests, unique-character hazards, and the bounded
   generic-character recommendation.
5. [Character records, entities, and appearances](character-records-entities-and-appearances.md)
   — the native record-to-entity-to-appearance chain, typed identities,
   mod-owned authoring boundary, and render/lifecycle acceptance matrix.
6. [AI roles, behavior, and workspots](ai-roles-behavior-and-workspots.md) —
   record behavior, Gameplay tier, follower/patrol roles, direct workspot
   commands, state observation, and ownership transfer.

The later scene chapters own screenplay, actor/performer, entry-point, and
named-exit details. This section explains only the community side of their
join.

## Focused vanilla research route

Extract the following resources from your own game with WolvenKit. Do not copy
or redistribute the extracted CR2W files.

| Depot path | Question it answers |
| --- | --- |
| `base\quest\minor_quests\mq003\mq003_orbitals.questphase` | How a vanilla parent activates a whole community, waits for spawned readiness, and invokes the activity phase. |
| `base\quest\minor_quests\mq003\phases\mq003_homeless.questphase` | How named community entries change phase and how the activity eventually deactivates them. |
| `base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene` | How scene actors use `acquisitionPlan: community`, a community `NodeRef`, and an entry `CName`. |
| `base\open_world\minor_activities\westbrook\japantown\ma_wbr_jpn_13\community\ma_wbr_jpn_013_claws_com.community` | How a vanilla `communityCommunityTemplate` stores generic Tyger Claw entries, phases, appearances, time periods, quantities, and AI-spot references. |
| `ep1\characters\entities\gang\gang__ep1_tyger_wa.ent` | How one installed entity exposes external appearance mappings, internal names, a shared `.app`, and a root default. Requires Phantom Liberty. |
| `base\characters\appearances\gang\gang__tyger_wa.app` | How one appearance resource stores multiple internal definitions and a `WomanAverage` frame contract. |
| `base\quest\side_quests\sq031\phases\sq031_rogue.questphase` | How one actor is promoted to `Gameplay` AI and how direct `questUseWorkspotNodeDefinition` objects are shaped. |
| `base\open_world\street_stories\watson\kabuki\sts_wat_kab_02\phases\sts_wat_kab_02_openworld.questphase` | How a named community actor receives an `AIFollowerRole` targeting `#player` and later receives role clear. |
| `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_gameplay.questphase` | How six `AIPatrolRole` payloads reference separate spline paths and explicit patrol parameters. |

Each path supplies **Observed in vanilla** evidence for its own focused shape.
It is not a template for copying unrelated IDs, records, appearances, or world
positions.

## First-pass failure routing

| Symptom | Inspect first |
| --- | --- |
| Nothing spawns after `Activate` | Registered block and sectors, quest prefab dependency, area/registry community identity, entry/phase spelling, AI-spot identities, and character record |
| Spawn wait never opens | Whether activation addressed the same community, `entireCommunity`/count comparison, area streaming, and the requested entry phase |
| Actor exists but the scene cannot bind it | Scene `acquisitionPlan`, `communityParams.reference`, `communityParams.entryName`, and scene start ordering |
| Actor appears at the wrong place or pose | AI-spot placement, exact full spot `NodeRef`, area `spotNodeIds`, registry `spotNodeRefs`, and workspot resource |
| Actor exists logically but is invisible or malformed | Character record entity path, exposed entity appearance, internal `.app` name, frame/component graph, and saved appearance history |
| Actor is unexpectedly hostile or armed | Character-record base, reaction/faction, action map, archetype, abilities, and equipment |
| Role command fires but the actor does not move | Spawn readiness, AI tier, command target, concrete typed params, path/workspot streaming, and navmesh |
| Actor walks back when the next activity starts | Follower/patrol role was cleared before the next scene, defend, phase, or cleanup owner took over |
| Actor vanishes during the scene | Cleanup edge ordering, scene outcome handoff, and the distance/trigger used before `Deactivate` |
| A clean resource change behaves like an older build | Starting save, community activation history, scene state, checkpoints, and installed archive hash |

WolvenKit opening every file and ArchiveXL mounting the block are intermediate
checks. Use the Lab 5 clean-save procedure to verify the complete `cqa005`
activation, acquisition, and cleanup route in game.
