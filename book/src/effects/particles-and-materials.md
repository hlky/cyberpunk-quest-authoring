# Particles, textures, and materials

A `.particle` resource decides how an image is emitted and drawn. Its material
decides how color, opacity, tint, and blending turn that image into pixels.
An effect can start correctly while its particles remain invisible, oversized,
or opaque.

Use the [custom-effects toolchain](index.md#tools-and-versions). Begin with one
static image and one presentation; add motion after it looks right in game.

## Inspect the emitter

The focused resource shape is:

```text
CParticleSystem
  emitters[] -> CParticleEmitter
    modules[]
      CParticleInitializerLifeTime
      CParticleInitializerSize
      CParticleInitializerVelocity
      CParticleModificatorAlphaOverLife
      CParticleModificatorAlphaOverEffect
    particleDrawer
    material
    localMaterialInstance -> CMaterialInstance
    lods[]
    emitterLoops
    renderResourceBlob
```

**Observed in vanilla:** inspect this shape in
`base\fx\player\status_effects\blindness\p_blindness.particle`.
The emitter has both editable module values and compiled render data. They
must describe the same simulation.

| Property | Question to answer |
| --- | --- |
| `modules[].lifeTime` | How long can a spawned particle live? |
| `modules[].size` and `scale` | How large is the particle? |
| `particleDrawer` | Is it a screen image or a world-space billboard? |
| `lods[].birthRate` | Are more particles emitted over time? |
| `lods[].burstList[].spawnCount` | How many spawn in a burst? |
| `emitterLoops` | Can the emitter repeat? |
| `renderResourceBlob` | Which compiled settings and updater data will rendering use? |

For a frame-based image, one burst of one particle avoids accumulating many
copies of the same glyph. A finite emitter and a finite particle lifetime are
separate settings.

## Make a local texture-replacement test

1. Extract the particle reference into your inspection project. Inspect its
   drawer, modules, compiled data, and material before changing anything.
2. Make a local working copy at a unique mod depot path. Keep the original
   reference separate. For this first test, preserve its compiled size,
   lifetime, and emission settings.
3. Draw a simple shape on a transparent RGBA canvas. Use a large, clear glyph
   before adding tiny details or fragment animation.
4. Import the PNG through WolvenKit's texture import workflow. Confirm that
   the resulting `.xbm` exists under `source\archive` at the intended path.
   Reopen or export it to check that the alpha channel survived.
5. Open the particle's `localMaterialInstance`. Inspect its `baseMaterial`
   and set the texture parameters to your imported assets.
6. Keep the drawer compatible with the presentation. First test V using the
   screen drawer; make the NPC variant separately.
7. Connect the particle to an [effect track](effect-timelines.md), then
   [register and trigger it](entity-spawners-and-status-effects.md).
8. Check visibility, transparency, placement, and removal in game before
   changing the simulation or adding more frames.

This material-only adaptation is **Experimental** until checked in your game.
Changing the texture does not give the particle a new size or lifetime.

## Set material parameters deliberately

The textured route uses `engine\materials\particles_generic.remt` as both the
emitter material reference and the local material's `baseMaterial`.

| Local material value | Purpose |
| --- | --- |
| `Diffuse` | Color texture `.xbm` reference |
| `AlphaMask` | Opacity-mask `.xbm` reference |
| `UseAlphaMask` | Enables mask use in this material setup |
| `Color` | Material tint applied to the texture |
| `ColorMultiplier` | Color intensity; start conservatively |
| `AlphaGlobal` | Overall opacity |
| `AdditiveAlphaBlend` | Selects the material's additive/alpha blend behavior |
| `SubUVWidth`, `SubUVHeight` | Texture-sheet dimensions; use `1`, `1` for a single image |
| `TexCoordSpeed` | Texture-coordinate movement; keep zero for a static frame |
| `DistortAmount` | Distortion amount; keep zero while checking the image |

Parameter names are case-sensitive. Add values with the parameter's actual
RED type: texture references, `Color`, `Float`, or `Vector4` as appropriate.
Reopen the cooked particle to check the material and referenced depot paths.

Tint and texture color multiply. A pink texture with a strong pink tint and
high multiplier can lose its intended hue or look much brighter than the PNG.
Start with a white tint when tuning a texture that already contains its final
colors. Check against both bright and dark game backgrounds.

## Keep opacity independent of dark color

An opacity mask describes coverage, not the artwork's brightness. For an
opaque black bow on a transparent background, its mask should be white inside
the bow and black outside. Using the dark color image as its own mask can make
the interior disappear.

Additive rendering adds light; it cannot supply a convincing opaque black
interior. If one design mixes dark silhouettes and glowing hearts, give the
layers separate materials:

| Layer | Color texture | Opacity | Starting blend choice |
| --- | --- | --- | --- |
| Glowing shapes | Colored glyphs | Independent coverage mask | Additive |
| Dark silhouettes | Dark artwork with visible edges | White inside the shape | Non-additive alpha |

The split-layer composition is **Experimental**. Check actual rendering;
changing one blend parameter does not diagnose every faint or missing shape.
Track alpha, texture alpha, the mask, material opacity, and the cooked material
can each suppress the image.

## Screen and billboard drawers need matching compiled settings

`CParticleDrawerScreen` draws the player presentation. The NPC variant uses
`CParticleDrawerBillboard`, with placement supplied by the entity descriptor.
Moving a screen particle to a head slot does not turn it into a billboard.

In the inspected particle layout, the screen variant's compiled
`renderResourceBlob.header.emitterInfo.vertexDrawerType` is `1`; the billboard
variant uses `0`. Keep the authored drawer and compiled header consistent.
These values describe this layout, rather than every possible drawer type.

## Check cooked size and lifetime

The compiled emitter header also contains its own loops, LOD emission data,
and burst counts. Size and lifetime can additionally be baked into updater
data. Saving a new module value is not enough if rendering still reads an old
compiled value.

After changing simulation settings, reopen the cooked resource and inspect an
export from it. If your authoring workflow does not regenerate the updater,
keep the existing compatible simulation for the texture exercise. Do not
reuse byte offsets from another particle or expect a JSON round trip to
compile a new simulation.

For [animated frame particles](effect-timelines.md#animate-images-with-tracks),
prepare compatible finite-lived particles before adding the sequence. Match
each particle's lifetime to its frame interval and test that old frames do not
remain visible underneath new ones.

Next: [Effect timelines](effect-timelines.md).
