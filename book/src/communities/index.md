# Communities and characters

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

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

## Evidence and version boundary

These chapters separate vanilla structure, retained historical behavior, and
the new Lab 5 candidate.

| Label | Bounded claim |
| --- | --- |
| **Observed in vanilla** | The cited `mq003` questphases and scene use community activation, `CharacterSpawned`, and scene actors with community acquisition. The cited Japantown `.community` resource contains the entry, phase, time-period, character-record, and spot-reference shapes described here. |
| **Structurally validated** | The retained research resources at commit `68f311c8f2511aeba679b76a68062ef5e446aaa0` serialize the registry, streamed area, AI spot, activation, readiness, and acquisition relationships described below. This is legacy research, not validation of `cqa005`. |
| **Runtime-proven** | Two retained historical archives exercised bounded parts of the lifecycle. Archive `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` completed the meeting route after community readiness and acquisition; archive `2C5179349DBD1AFF5A5A01123F83FF1DC76D8D91E45FE946CEA4DCAF0166BF80` spawned all three configured guards, kept them passive, and cleaned them up. These are legacy fixture results only. |
| **Acceptance-gated** | The exact `cqa005` identity set, world placement, `Activate` -> `CharacterSpawned` -> broad-setup join, scene acquisition, named pre-scene seed loads for Cases 3/4/7, ordinary lifecycle, post-`contact_done` reload, completed reload, and delayed `Deactivate` follow the synchronized marker above. |
| **Experimental** | Active-line interruption and `CutDestination` behavior, arbitrary or unlisted pre-scene active-child states, and workspot/facial-animation quality are outside the frozen campaign and remain experimental independently of the synchronized marker. |

The retained CR2W research was serialized with WolvenKit `8.17.4` as WKit
JSON `0.0.9` and records CR2W `GameVersion: 2310`. The historical records do
not bind one complete run to this book's pinned practical baseline. They do not
promote a new package merely because it follows the same shape.

The practical acceptance target remains Cyberpunk 2077 Windows GOG `2.31a`,
WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript
`0.5.31`. See [Tested versions](../reference/tested-versions.md).

## Native ownership map

| Owner | Responsibility |
| --- | --- |
| `worldCommunityRegistryNode` | Makes community template data and initial entry state available independently of the local streamed area. |
| `worldCompiledCommunityAreaNode_Streamable` | Places the community source in the streamed world and mirrors which entry/phase/time period uses which AI-spot identities. |
| `worldAISpotNode` | Places an `AIActionSpot` and names the workspot resource an actor can use there. |
| `communitySpawnEntry` | Associates one community entry name with a character `TweakDBID` and one or more spawn phases. |
| `communitySpawnPhase` | Selects the phase name, appearance set, and time-period behavior for that entry. |
| `questSpawnManagerNodeDefinition` | Sends `Activate` or `Deactivate` to a community reference; it does not prove the actor already exists or is gone. |
| `questCharacterSpawned_ConditionType` | Waits for the configured spawned-character comparison to become true. |
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
| Actor vanishes during the scene | Cleanup edge ordering, scene outcome handoff, and the distance/trigger used before `Deactivate` |
| A clean resource change behaves like an older build | Starting save, community activation history, scene state, checkpoints, and installed archive hash |

WolvenKit opening every file and ArchiveXL mounting the block are intermediate
checks. The exact `cqa005` join follows the synchronized marker above; only the
hash-bound, clean-save campaign may change that marker.
