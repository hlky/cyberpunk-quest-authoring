# Braindance and specialized scenes

Braindance authoring is the book's deliberately bounded advanced-research
section. It is complete as an ownership, inspection, and acceptance guide; it
is not presented as a runtime-proven recipe for shipping a custom recording.

The native feature is not one resource or one scene-node option. A reviewable
candidate crosses all of these owners:

```text
questphase entry, player hold, and exit cleanup
  -> rewindable .scene and its entry/exit contract
  -> .scenerid actor, facial, cyberware, and camera channels
  -> world scene markers, camera entity, clue entities, and support props
  -> visual/audio/thermal clue events and discovery facts
  -> journal progress, interruption cleanup, and replay policy
```

Breaking any join can still leave the neighboring files structurally valid.
For example, a `.scenerid` can serialize while its scene event points at the
wrong resource/serial pair, and a clue can appear on a timeline while its
world entity or discovery handoff is absent.

## Evidence and version boundary

| Label | Bounded claim |
| --- | --- |
| **Observed in vanilla** | Focused extractions from the installed Cyberpunk 2077 `2.31a` archives show `scnRewindableSectionNode`, RID resource handlers and event references, body/facial/cyberware/camera channels, support props, layered clue events, and quest-side BD management in the exact depot paths cited by these chapters. |
| **Structurally validated** | A retained mod-owned research chain consisting of one `.questphase`, one rewindable `.scene`, and one `.scenerid` serialized to JSON and back to CR2W with WolvenKit `8.19.0` on 2026-08-09. This proves readable shapes and internal serialization, not gameplay. |
| **Experimental** | Custom animation playback, recorded-perspective camera behavior, seek/rewind, analysis-layer switching, clue discovery, normal cleanup, interrupted cleanup, and replay all remain experimental until the exact packaged candidate passes the eight-case matrix in [Clue layers, cleanup, and acceptance](clue-layers-cleanup-and-acceptance.md). |

There is no **Runtime-proven** custom-braindance claim in this section. No
retained eight-case record exists, so a structurally complete candidate cannot
be promoted by inference.

The practical inspection baseline is Cyberpunk 2077 Windows GOG `2.31a`,
WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript
`0.5.31`. The current structural round trip did not launch the game and did not
exercise ArchiveXL, RED4ext, or redscript behavior. See [Tested
versions](../reference/tested-versions.md).

## Reading route

Read these pages in order:

1. [Ownership and resource chain](ownership-and-resource-chain.md) — which
   resource owns quest flow, rewindable screenplay, recorded animation,
   support entities, markers, clue state, and cleanup.
2. [RID playback and rewind](rid-playback-and-rewind.md) — how RID
   resource/serial identities meet scene event references, and why body,
   facial, cyberware, camera, duration, and rewindability form one contract.
3. [Clue layers, cleanup, and acceptance](clue-layers-cleanup-and-acceptance.md)
   — visual/audio/thermal clue ownership, normal and interrupted exits,
   save-backed state, replay policy, and the mandatory eight-case campaign.

Read [Scene resource anatomy](../scenes/resource-anatomy.md), [Screenplay
sections and events](../scenes/screenplay-sections-and-events.md), [Entry,
exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md), and
[Persistent state](../foundations/persistent-state.md) first. Braindance adds
contracts to ordinary scenes; it does not replace them.

## Focused vanilla research route

Extract these resources from your own installed archives into a disposable
inspection project. Do not publish or package the extracted files.

| Depot path | Focused question |
| --- | --- |
| `base\quest\side_quests\sq012\scenes\sq012_02a_braindance.scene` | How one current vanilla scene joins a rewindable section, three RID handlers, support props, clue layers, interruption, and named entry/exit points. |
| `base\animations\quest\side_quests\sq012\sq012_braindance\rid\sq012_braindance__part_a.scenerid` | How a version-5 `scnRidResource` owns actor and camera tags plus body, facial, cyberware, and camera animation buffers. |
| `base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdview.ent` | The visual-layer support entity selected by a scene prop record. |
| `base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdfog.ent` | The fog support entity selected by a scene prop record. |
| `base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdsetup.ent` | The render-to-texture setup entity selected by a scene prop record. |
| `base\quest\main_quests\prologue\q004\scenes\q004_05_bd_yorinobu.scene` | A much larger main-quest comparison with one rewindable section, layered clues, RID events, quest nodes, and BD action management. |
| `base\quest\main_quests\prologue\q004\phases\q004_braindance.questphase` | The surrounding quest-side setup and teardown decomposition; it is not a self-contained scene template. |

The first two resources were re-extracted from the local `2.31a` archives and
serialized with WolvenKit `8.19.0` on 2026-08-09. The focused `sq012` scene
contains three `scnRidResourceHandler` entries, one
`scnRewindableSectionNode`, 24 `scnPlayRidAnimEvent` events, three RID-camera
events, six clue events, and two braindance-visibility events. Those counts are
**Observed in vanilla** for that exact resource only, not minimums or a
copy-ready design.

## What completion means here

This section is complete when a reader can:

- name every owner in the resource chain and the typed identity used at each
  join;
- inspect a current vanilla reference without redistributing it;
- distinguish serialization success from RID/event compatibility and runtime
  behavior;
- design a mod-owned candidate and its cleanup contract without relying on a
  hidden generator;
- execute and retain the eight acceptance cases required for any future
  **Runtime-proven** promotion.

It does not promise that WolvenKit exposes a one-click custom-braindance
wizard, that a vanilla RID may be redistributed as a template, or that a
custom Blender/export pipeline is part of the reader workflow. Creating new
compressed animation buffers is a specialized production problem; this book
documents the native contract they must satisfy and the evidence needed to
claim that they work.

Next: [Ownership and resource chain](ownership-and-resource-chain.md).
