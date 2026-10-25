# Custom effects

Build an optics glitch that draws animated shapes over V's view or above an
NPC's head, then fades them out when the status ends. The gameplay action,
status duration, effect timeline, and rendered image have separate owners.

```text
item, quickhack, or other gameplay action
  -> status effect record
     -> VFX entry: cqa_optics_glitch
        -> target entity's named effect descriptor
           -> worldEffect timeline (.effect)
              -> particle system (.particle)
                 -> material and textures (.xbm)
```

Screen overlays and head-attached billboards using this chain are
**Runtime-proven**. Build and test the two presentations separately before
combining them with a quest.

## Start with one presentation

| Result | Particle drawer | Entity registration | Placement |
| --- | --- | --- | --- |
| Shapes over V's view | `CParticleDrawerScreen` | Player entity templates | Screen rendering; test first and third person separately |
| Shapes above an NPC | `CParticleDrawerBillboard` | The NPC's actual entity template | A compatible slot such as `Head`, with a relative offset |

The effect name can be the same on both entities while their descriptors
select different `.effect` files. A player patch does not register the effect
on NPCs, and patching one generic NPC does not cover every custom character.

## Tools and versions

Use the [book's toolchain](../reference/tested-versions.md), including
TweakXL `1.11.3` for the status and item records. Prepare original RGBA textures
in an image editor and import them with WolvenKit.

The particle and effect property examples were inspected with Cyberpunk `2.31`
resources and WolvenKit `8.17.4`. The book's normal authoring target is
WolvenKit `8.19.0`; reopen your resources and check their compiled data before
installing. Follow each page's field paths rather than relying on editor tab
positions.

## Author in this order

1. [Particles, textures, and materials](particles-and-materials.md): make one
   readable, transparent image before adding animation.
2. [Effect timelines](effect-timelines.md): schedule the intro, loop, outro,
   and optional sound.
3. [Entity spawners and status effects](entity-spawners-and-status-effects.md):
   connect the effect name to the target entity and trigger it through a
   native status.
4. [Test and troubleshoot](test-and-troubleshoot.md): check V, NPCs, expiry,
   cancellation, and reapplication independently.

Read [Character records, entities, and
appearances](../communities/character-records-entities-and-appearances.md)
first if entity templates and component packages are unfamiliar.

## Files in a small effect mod

These are example names for resources you author, not additional downloads:

| File | Owns |
| --- | --- |
| `mod\cqa\effects\optics_v.effect` | V's presentation timeline |
| `mod\cqa\effects\optics_npc.effect` | NPC presentation timeline |
| `mod\cqa\effects\particles\v_intro.particle` | Intro emitter and material for V |
| `mod\cqa\effects\textures\intro_d.xbm` | Color image |
| `mod\cqa\effects\textures\intro_m.xbm` | Independent opacity mask |
| `mod\cqa\effects\registration\optics_v.ent` | Player spawner component |
| `mod\cqa\effects\registration\optics_npc.ent` | NPC spawner component |
| `CQA_Effects.archive.xl` | Entity patch targets and onscreen-text registration |
| `r6\tweaks\cqa_effects.yaml` | Duration, VFX, status, action, and item records |

Archive the `.effect`, `.particle`, `.xbm`, and patch `.ent` resources at their
depot paths. Keep the ArchiveXL file and TweakXL YAML under
`source\resources` so they install as loose framework files.

## Vanilla references

Extract references into a separate inspection project from your own game:

| Depot path | Inspect it for |
| --- | --- |
| `base\fx\player\status_effects\blindness\p_blindness.particle` | Screen drawer, emitter modules, material, and compiled particle data |
| `base\fx\player\p_hacking_glitch\p_hacking_glitch_low.effect` | A `worldEffect` resource and its track/event relationships |
| `engine\materials\particles_generic.remt` | Textured particle material parameters |
| `base\characters\entities\player\player_wa_fpp.ent` | Player components and effect-slot availability |
| `base\characters\entities\player\player_ma_fpp.ent` | The other player body template's components and slots |

These structures are **Observed in vanilla**. Keep the original extracted
resources out of shared projects and downloads.
