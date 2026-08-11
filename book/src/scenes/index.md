# Scenes

A native scene is not a self-contained quest. It owns performers, screenplay
items, timed events, scene-graph flow, entry points, and named exits. Other
resources must make its actors available, start it, consume its outcome, and
clean up durable world and quest state.

```text
world/community                  .scene                         .questphase
activate + spawn actor  ->  acquire + perform + named exit  ->  outcome + cleanup
                               |             |
                               |             +-> embedded choice locStore
                               v
                   subtitle map/entries + VO map/WEM
```

That ownership boundary is the central rule of this section:

| Owner | Responsibility in the First Contact example |
| --- | --- |
| Streaming sector and community | Register `#cqa005_com_contact`, materialize the contact, and provide the scene marker `#cqa005_sm_contact` |
| `.scene` / `scnSceneResource` | Acquire actor `0` and V as actor `1`, play one timed line, run a small PuppetAI branch, and expose `contact_done` |
| `.questphase` / `questSceneNodeDefinition` | Resolve the soft scene path at the marker, enter through `start`, and receive `contact_done` |
| Journal and facts | Advance the meet/leave presentation after the scene returns, then record terminal completion after child cleanup |
| ArchiveXL localization | Merge the external subtitle and voiceover resources used by the spoken-line RUID |
| Save | Retain active quest, journal, fact, checkpoint, community, and scene state independently of a later archive edit |

## Reading route

Read these pages in order:

1. [Scene resource anatomy](resource-anatomy.md) — the v5 root, typed empty
   stores, resource references, debug data, and interruption scaffold.
2. [Actors and performers](actors-and-performers.md) — community acquisition,
   player context lookup, performer symbols, actor behavior, and lipsync slot
   cardinality.
3. [Screenplay, sections, and events](screenplay-sections-and-events.md) — the
   separate line, event, section, duration, and ID domains.
4. [Entry, exit, and quest handoff](entry-exit-and-quest-handoff.md) — the exact
   four-node topology and the `questSceneNodeDefinition` interface.
5. [Author one spoken line](one-spoken-line.md) — a bounded WolvenKit procedure
   for `All clear. Keep moving.` and its external subtitle/VO join.
6. [Cleanup and save state](cleanup-and-save-state.md) — interruption versus
   completion, named-outcome handling, community teardown, and clean-save
   acceptance.
7. [Choices, outcomes, and scene-local
   localization](choices-outcomes-and-localization.md) — native choice items,
   padded socket observations, embedded locStore joins, and multi-exit quest
   handoff.
8. [External VO, WEM, and
   lipsync](external-vo-wem-and-lipsync.md) — the parallel subtitle, audio, and
   actor-slot chains plus cardinality-first diagnosis.
9. [Animation events and scene
   workspots](animation-events-and-workspots.md) — animation-set visibility,
   timed cinematic events, scene workspot identity, and cleanup boundaries.
10. [Lab 5: First Contact](lab-05.md) — the complete resource inventory,
   ownership model, exact graphs, and evidence boundary.
11. [Author First Contact in WolvenKit](lab-05-authoring.md) — the field-level
   construction and round-trip procedure.
12. [Test First Contact](lab-05-test.md) — clean-save playback, reload,
   streaming, handoff, and cleanup checks.

The First Contact lab intentionally remains a one-line scene with an empty
embedded `locStore` and no cinematic-animation or scene-workspot payload. The
advanced pages explain how those additional native structures are owned and
inspected; they do not silently add them to the lab or promote unexecuted
runtime behavior. Combat, holocalls, and complex devices remain owned by their
cookbook and system chapters.

## Vanilla research anchors

Use WolvenKit to extract these resources from your own installed archives and
inspect only the fields needed for comparison:

- `base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene`
- `base\quest\minor_quests\mq003\scenes\mq003_03_orbital_pod.scene`
- `base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene`
- `base\quest\minor_quests\mq010\scenes\mq010_02_barry_talk.scene`
- `base\animations\quest\minor_quests\mq007\anim\body\mq007__talking_gun__male_fpp.anims`
- `base\workspots\common\wall\generic__stand_wall_lean_left__stand_around__01.workspot`
- `base\localization\en-us\lipsync\base\quest\minor_quests\mq007\scenes\mq007_01_gun_found\skippy.anims`
- `base\localization\en-us\lipsync\base\quest\minor_quests\mq007\scenes\mq007_01_gun_found\v.anims`

These paths are citations, not redistributable examples. Do not publish the
extracted CR2W files or complete serialized exports. Record focused types,
properties, IDs, and edges instead; the workflow is described in [Inspect a
vanilla questphase](../start-here/inspecting-vanilla.md).

## First-pass failure routing

| Symptom | Inspect first |
| --- | --- |
| Scene never begins | Community `Activate`, `CharacterSpawned`, world marker resolution, phase prefab scope, soft scene path, and `start` socket |
| Crash or failure during scene startup | Actor acquisition, readiness, lipsync ID-to-array cardinality, and missing referenced resources |
| Subtitle is absent | Scene line RUID, registered subtitle map, its subtitle-entry reference, and matching `stringId` |
| Subtitle works but audio is silent | VO-map registration, matching `stringId`, both gender paths, WEM depot path, and audio logs |
| Choice labels are blank or stale | Screenplay option locstring, unsigned locale-block ordering, descriptor/payload `variantId`, and `vpeIndex` |
| Choice takes the wrong branch | Option order, output ordinal, destination, and stale active-scene state |
| Line plays but the quest does not continue | Scene exit name and node, scene-node output socket name, and outgoing questphase connection |
| Animation does not play or deforms the actor | Performer mapping, actor-visible animation-set slot, animation name, component/mask, and rig compatibility |
| Scene workspot never succeeds | Actor reference, workspot data/instance IDs, transform, params, wrapper mapping, and output semantics |
| Contact remains after completion | Leave condition, community `Deactivate`, and any durable community/device state; reaching `scnEndNode` is not cleanup |
| A rebuild behaves like an older graph | Save provenance, active scene/checkpoint state, facts, and journal state before editing more resources |

Next: [Scene resource anatomy](resource-anatomy.md).
