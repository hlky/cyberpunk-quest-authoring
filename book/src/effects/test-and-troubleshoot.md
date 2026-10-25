# Test and troubleshoot custom effects

Test the visual on V and on a supported NPC before integrating it with a
quest. A working item, a successful status application, and a visible effect
are three different checkpoints.

Use the [custom-effects toolchain](index.md#tools-and-versions). Close the game
before replacing archives, entity patches, or TweakXL records, then restart.
Use a disposable save made before installing the item or changing its vendor
stock. Keep a separate save for checking behavior after expiry and reload.

## Check the resource chain before launch

1. Reopen the cooked `.effect`, particles, and patch entities in WolvenKit.
2. Compare the status's VFX name with the descriptor's `effectName` exactly.
3. Check that the patch targets the entity template the character actually
   uses, and that the patch adds your independently named spawner.
4. Match each particle and sound RUID to its compiled placement row.
5. Check the loop range, finite outro, root length, and sound position.
6. Check particle drawers, compiled simulation settings, materials, texture
   paths, and opacity masks.
7. Run WolvenKit's project validation and install normally. Confirm the
   archive, `.archive.xl`, and TweakXL YAML reached their game directories.

## Start with normal expiry

Consume the native self-test item on V. Watch the entire sequence:

```text
status starts -> intro -> repeating motion -> status expires -> outro -> clear view
```

Check that transparent regions reveal the game, the shapes fit the screen,
the loop has no obvious jump, and old frames do not accumulate. Repeat against
bright and dark backgrounds and with both supported player body templates.

Use the targeted quickhack on the supported NPC. Check the same lifecycle,
then move around the character: the billboard should follow the intended slot
without sitting inside the head or remaining at the spawn point.

## Exercise cleanup separately

New cancellation, sound, split-material, and reapplication behavior is
**Experimental** until exercised in game.

| Test | What to watch |
| --- | --- |
| Normal expiry | Status ends; outro finishes; no particles remain |
| Early status removal through your gameplay route | Visual leaves by the intended outro or immediate-stop policy |
| Reapply while active | No uncontrolled layering, unexpected restart, or duplicated exit sound |
| Reapply after expiry | A complete fresh sequence starts and ends once |
| Target dies or leaves streaming range | No floating image or sound remains without its owner |
| Change first/third-person view | Supported player templates resolve the correct presentation |
| Reload after expiry | No restored blindness, stranded overlay, or unexpected replay |
| Save during the active status, if permitted | Loaded state behaves coherently; record whether the timer resumes or restarts |
| Enable another mod affecting the same character | The custom spawner and the character's existing effects coexist |

Listen to the game while testing the sound. A silent video or an authored
frame preview cannot tell you whether an audio event played.

## Diagnose the first failing link

| Symptom | Inspect first |
| --- | --- |
| Item has no name or description | Onscreen keys, localization resource, ArchiveXL registration |
| Item exists but produces no status | Item action, `completionEffects`, recipient, status record IDs |
| Blindness works but V shows a white screen | Exact `VFX`/`SFX` casing, derived status, custom name, player spawner patch |
| V works but an NPC has no custom visual | The NPC's real entity path, separate NPC patch, descriptor name |
| Vanilla NPC works but custom character does not | Explicit patch target for the custom `.ent` and compatible slot bindings |
| Status starts but neither variant renders | Effect-name join, patch loading, descriptor path, event placement rows |
| Sound or particles appear at the wrong place | Placement tag, slot binding, relative transform, RUID-to-placement join |
| Image is much too large despite a size edit | Compiled particle size and screen/billboard drawer settings |
| Old frames remain visible | Baked lifetime, emission rate, burst count, emitter loops, overlapping intervals |
| Shapes are invisible | Track alpha/emission scale, material opacity, imported alpha channel, texture paths |
| Dark shapes look like faint outlines | Independent coverage mask, blend choice, material layer, background contrast |
| Pink looks red or excessively bright | Texture color multiplied by tint and `ColorMultiplier`, then in-game exposure |
| Sound repeats on every motion cycle | Sound event placed inside the loop |
| Outro never appears | Loop-break route, loop boundaries, outro timing, root length, immediate-stop behavior |
| Effect persists after the status | Particle lifetime, surviving emitter, stop policy, other active status applications |

Inspect ArchiveXL's log under `red4ext\plugins\ArchiveXL` and TweakXL's log
under `red4ext\plugins\TweakXL` for missing targets, unresolved paths, or
unknown record properties. If the template does not receive the spawner,
retuning the texture will not fix it.

Back to: [Custom effects](index.md).
