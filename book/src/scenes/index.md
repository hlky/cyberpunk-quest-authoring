# Scenes

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

A native scene is not a self-contained quest. It owns performers, screenplay
items, timed events, scene-graph flow, entry points, and named exits. Other
resources must make its actors available, start it, consume its outcome, and
clean up durable world and quest state.

```text
world/community                  .scene                         .questphase
activate + spawn actor  ->  acquire + perform + named exit  ->  outcome + cleanup
                                     |
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

## Evidence boundary

| Label | Bounded claim |
| --- | --- |
| **Observed in vanilla** | The resource families and focused arrangements taught here were compared with scenes at the four cited `mq003`, `mq007`, and `mq010` depot paths. They are observations from comparable resources, not universal templates. |
| **Structurally validated** | The exact First Contact `scnSceneResource` v5, its canonical four-node completed graph, its start checkpoint, and its questphase socket contract serialize and round-trip with WolvenKit `8.19.0`. |
| **Runtime-proven** | Retained legacy archive `2C5179349DBD1AFF5A5A01123F83FF1DC76D8D91E45FE946CEA4DCAF0166BF80` proved the generic community activation/spawn/deactivation lineage. Archive `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` proved a community-acquired conversation that completed after both actors used addressable lipsync slot `0`. These bounded results do not promote a newly assembled quest automatically. |
| **Acceptance-gated** | The exact `cqa005` world, community, named pre-scene seed loads for Cases 3/4/7, ordinary one-line playback, named exit, fact handoff, cleanup, post-`contact_done` reload, completed reload, and clean-save integration follow the synchronized marker above. |
| **Experimental** | Active-line interruption and `CutDestination` behavior, arbitrary or unlisted pre-scene active-child states, and facial/workspot-animation quality are outside the frozen campaign and remain experimental independently of the marker. |

The pinned practical baseline is Cyberpunk 2077 Windows GOG `2.31a`,
WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript
`0.5.31`, reviewed on 2026-08-09. See [Tested
versions](../reference/tested-versions.md).

## Stage 6 reading route

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
7. [Lab 5: First Contact](lab-05.md) — the complete resource inventory,
   ownership model, exact graphs, and evidence boundary.
8. [Author First Contact in WolvenKit](lab-05-authoring.md) — the field-level
   construction and round-trip procedure.
9. [Test First Contact](lab-05-test.md) — the hash-bound clean-save runtime
   campaign and promotion rules.

This first pass intentionally excludes choices, scene-local choice
localization, cinematic animation production, combat, holocalls, complex
devices, and exact WEM production. Those belong to later cookbook and advanced
audio/scene work. The empty embedded `locStore` in this example is therefore a
deliberate typed value, not missing spoken-line text.

## Vanilla research anchors

Use WolvenKit to extract these resources from your own installed archives and
inspect only the fields needed for comparison:

- `base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene`
- `base\quest\minor_quests\mq003\scenes\mq003_03_orbital_pod.scene`
- `base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene`
- `base\quest\minor_quests\mq010\scenes\mq010_02_barry_talk.scene`

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
| Line plays but the quest does not continue | Scene exit name and node, scene-node output socket name, and outgoing questphase connection |
| Contact remains after completion | Leave condition, community `Deactivate`, and any durable community/device state; reaching `scnEndNode` is not cleanup |
| A rebuild behaves like an older graph | Save provenance, active scene/checkpoint state, facts, and journal state before editing more resources |

Next: [Scene resource anatomy](resource-anatomy.md).
