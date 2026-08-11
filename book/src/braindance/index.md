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
   save-backed state, replay policy, and a practical eight-case test campaign.

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

## What you will learn

This section is complete when a reader can:

- name every owner in the resource chain and the typed identity used at each
  join;
- inspect a current vanilla reference without redistributing it;
- distinguish serialization success from RID/event compatibility and runtime
  behavior;
- design a mod-owned candidate and its cleanup contract without relying on a
  hidden generator;
- run the eight test cases that cover forward playback, rewind, clue layers,
  normal cleanup, interrupted cleanup, and replay.

It does not promise that WolvenKit exposes a one-click custom-braindance
wizard, that a vanilla RID may be redistributed as a template, or that a
custom Blender/export pipeline is part of the reader workflow. Creating new
compressed animation buffers is a specialized production problem; this book
documents the native contract they must satisfy and how to test the result.

Next: [Ownership and resource chain](ownership-and-resource-chain.md).
