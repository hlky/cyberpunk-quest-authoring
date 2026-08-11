# Ownership and resource chain

A braindance review scene is a coordinated set of native resources. Treating
the `.scene` or `.scenerid` as the whole feature hides the world placement,
quest lifecycle, clue-state, and cleanup owners that make playback usable.

| Record | Value |
| --- | --- |
| Research review | 2026-08-09 |
| Game archives inspected | Cyberpunk 2077 Windows GOG `2.31a` |
| Inspection and structural round trip | WolvenKit `8.19.0` |
| Practical framework baseline | ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Runtime status | **Experimental** — no retained eight-case custom-candidate pass |

> **Research note:** the named vanilla shapes on this page are
> **Observed in vanilla**. The mod-owned `.questphase`/`.scene`/`.scenerid`
> research chain is **Structurally validated** because each binary serialized
> and deserialized with WolvenKit `8.19.0`. Its in-game playback, seek, rewind,
> layers, cleanup, interruption, and replay remain **Experimental**.

## Start with owners, not filenames

```text
registered root questphase
  -> child questphase owns entry preparation and scene invocation
       -> questSceneNodeDefinition resolves a mod-owned .scene
            -> scnSceneResource owns screenplay, events, exits, and RID refs
                 -> scnRidResource owns recorded actor/camera animation data
            -> scene props resolve records and support .ent resources
            -> scene markers and clue references resolve placed world nodes
       -> named scene outcome returns to the questphase
  -> questphase restores player/world/UI state and commits durable outcome
```

No arrow can be replaced by a same-looking identifier from another domain.
A scene event ID is not a RID serial number, a scene performer ID is not a
community entry name, and a `NodeRef` is not a depot path.

## Native ownership table

| Owner | What it owns | What it does not prove |
| --- | --- | --- |
| ArchiveXL root registration | The one root questphase visible to the quest loader | That external child phases, scenes, RID files, or world nodes resolve |
| `questQuestPhaseResource` | Entry flow, preparation, scene invocation, exit branch, post-scene cleanup, journal/fact handoff | Rewindable timeline semantics or recorded animation buffers |
| `questSceneNodeDefinition` | Soft scene depot path, scene input, world marker, and named output sockets | That the scene can acquire all actors/props or play its events |
| `scnSceneResource` | Actors, player actors, props, workspots, screenplay store, scene graph, entry/exit points, interruption scenarios, RID handlers, and resource-reference tables | The bytes for recorded actor/camera motion or world placement |
| `scnRidResource` in `.scenerid` | Actor and camera tags, serial numbers, body/facial/cyberware channels, camera channels, compressed buffers, duration, joint/track cardinality | Scene performer assignment, clue logic, entry/exit, or cleanup |
| `scnPropDef` plus TweakDB record | How a scene acquires/spawns a support prop such as BD view, fog, setup, or camera | The world marker at which it appears |
| Streamed world resources | Scene origin, support-prop marker, camera entity, clue entities, player hold/return anchors, and their transforms | Scene or quest execution |
| `scneventsClueEvent` and scene quest nodes | Layer, active time interval, clue entity, discovery operation, and fact handoff | Journal state unless the quest consumes the result |
| Save | Facts, journal progress, active quest/scene state, and other persistent side effects | A clean replay of a rebuilt candidate |

This is why cleanup belongs to the questphase even when the last visible event
is inside the scene. Scene completion is a signal; it does not automatically
restore every state changed before playback.

## The six typed joins

Record these joins explicitly in design notes and acceptance evidence.

### 1. Quest node to scene resource

The scene node's soft resource reference is a depot path such as
`mod\my_quest\scenes\my_bd.scene`. Its configured scene input and world marker
must exist in that exact scene/world pair. Filename similarity cannot satisfy
either join.

The owning phase also declares the prefab root needed for its local NodeRefs.
Follow [Quest prefabs and NodeRefs](../world/quest-prefabs-and-noderefs.md) and
[Entry, exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md).

### 2. Scene handler to RID resource

`scnSceneResource.ridResources[]` contains `scnRidResourceHandler` values. A
handler couples an `scnRidResourceId` with a `.scenerid` depot path. Later
scene-reference entries use that resource ID again; array position or a file's
basename is not the durable join.

In the current `sq012_02a_braindance.scene`, three handlers address parts A,
B, and C. That is **Observed in vanilla** for this recording, not a requirement
that custom work use three files.

### 3. RID tag to recorded performer or camera

The `.scenerid` root is `scnRidResource`. Its actor and camera entries have an
`scnRidTag` containing a typed signature (`CName`) and an
`scnRidSerialNumber`. The inspected SQ012 part-A RID is version 5, contains
nine actor entries and one camera entry, and has separate body, facial, and in
one case cyberware channels. Those counts are **Observed in vanilla** only.

A scene's `resouresReferences` collection maps animation references back to a
RID `resourceId` and animation serial number. Events then select an entry in
those scene-local reference arrays. All three levels must agree:

```text
.scenerid tag / animation serial
  <-> scene resourceId + serial reference
       <-> event's scene-local animResRefId or animSRRefId
```

### 4. Scene performer to actor acquisition

RID animation events target an `scnPerformerId`; scene actors use
`scnActorId`, actor names, and acquisition plans. Community-backed performers
still require the readiness/acquisition lifecycle described in [Activation,
readiness, and acquisition](../communities/activation-readiness-and-acquisition.md).
Recorded motion does not spawn a performer.

### 5. Scene prop to support entity and world marker

The inspected SQ012 scene defines `bdview`, `bdfog`, and `bdsetup` as
`scnPropDef` entries using `entityAcquisitionPlan: spawnDespawn`. Each entry
selects a `Props.*` TweakDB record and a global spawn-marker `NodeRef`. The
records ultimately select the three `.ent` resources cited by this section.

The focused entity roots are `entEntityTemplate`. The BD view and fog
resources contain mesh components; the BD setup resource contains a
render-to-texture camera component. A successful `.ent` round trip does not
prove that its record exists, its marker resolves, or the scene spawns it.

### 6. Clue event to world entity, discovery fact, and journal

An `scneventsClueEvent` owns a timeline interval and analysis layer. Its
`gameEntityReference` may address an actor within a community or a standalone
world `NodeRef`. Scene quest nodes can discover/toggle the clue and write a
fact. The owning questphase must deliberately consume that fact and update the
journal. See [Clue layers, cleanup, and
acceptance](clue-layers-cleanup-and-acceptance.md).

## Focused current-archive observation

Use the disposable-project procedure in [Inspect a vanilla
questphase](../start-here/inspecting-vanilla.md), but search for these exact
paths:

```text
base\quest\side_quests\sq012\scenes\sq012_02a_braindance.scene
base\animations\quest\side_quests\sq012\sq012_braindance\rid\sq012_braindance__part_a.scenerid
base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdview.ent
base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdfog.ent
base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdsetup.ent
```

Open the current `.scene` and inspect properties before its graph. Record only
focused notes:

| Property area | Current focused observation |
| --- | --- |
| `entryPoints` / `exitPoints` | Two named entries and one named exit bind names to `scnNodeId` values. Names, not editor position, form the quest handoff. |
| `interruptionScenarios` | One enabled distance-based scenario has separate interrupt and return thresholds. This is not proof of custom interruption cleanup. |
| `ridResources` | Three handler entries each pair a typed resource ID with an exact `.scenerid` depot path. |
| `resouresReferences` | RID body, facial, cyberware, and camera reference arrays sit beside ordinary gameplay/cinematic/lipsync sets. |
| `props` | BD view, fog, setup, and camera are separate props rather than flags on the rewindable node. |
| `sceneGraph` | One rewindable section owns timed RID, camera, clue, visibility, VFX, dialog, audio, attachment, and socket events. |

Do not copy the extracted resource into a mod project. It contains quest-local
actors, records, NodeRefs, facts, scene IDs, and animation references. Retain
the path, versions, a small property inventory, and—if useful—a local hash.

## Author a mod-owned chain manually in WolvenKit

This is a planning and inspection order, not a claim that every field has a
safe from-scratch editor default.

1. Define the terminal quest outcome, replay policy, and cleanup obligations
   before creating animation.
2. Allocate a mod-owned namespace for depot paths, facts, full NodeRefs,
   community entries, scene entry/exit names, actor/prop names, RID resource
   IDs, and serial numbers.
3. Create or place the scene origin, support-prop marker, camera entity, clue
   entities, and player hold/return anchors in mod-owned world resources.
4. Declare those world roots in the exact questphase that resolves them.
5. Build an ordinary scene shell first: actors, props, entry, exit,
   interruption scenario, and a non-rewindable diagnostic route.
6. Add a mod-owned `.scenerid`; inventory every actor/camera tag, animation
   serial, channel, duration, joint count, and track count.
7. Add scene RID handlers and reference tables, then bind events by typed
   reference ID. Do not infer array indexes from another scene.
8. Add the rewindable section, its timed events, layer conditions, clue
   events, and named outputs.
9. Add quest-side preparation, scene invocation, normal cleanup, interrupted
   cleanup, journal/fact handoff, and replay guard/reset.
10. Round-trip every CR2W with WolvenKit, pack only mod-owned resources, and
    execute the eight-case matrix from clean saves.

The scene editor may make some of these arrays easier to edit, but the native
contract remains the same. If a required table or buffer cannot be authored
safely in the current WolvenKit UI, stop at a focused inspection/structural
prototype. Do not substitute a hidden generator and call that a reader-facing
manual procedure.

## Structural research result

A retained mod-owned snapshot contains a `.scenerid`, rewindable `.scene`, and
owning `.questphase` built as one resource chain. Exact artifact identities are
kept in [Lab status and research
provenance](../reference/evidence-version-matrix.md#retained-structural-and-vanilla-evidence).

On 2026-08-09, WolvenKit `8.19.0` serialized all three binaries to CR2W-JSON
and deserialized those documents back to CR2W without error. This is
**Structurally validated** evidence for readable, writable resource shapes.
It excludes ArchiveXL mounting, world resolution, actor acquisition,
animation correctness, seek/rewind, clue layers, UI, audio, save behavior,
cleanup, interruption, and replay.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Scene node never starts | Root registration, child resource path, input name, phase prefab root, scene origin, and actor readiness |
| Scene starts but recorded bodies do not move | RID handler path/ID, actor signature and serial, scene RID-reference row, event `animResRefId`, performer mapping, duration, and joint cardinality |
| Recorded camera is absent | Camera RID tag/serial, scene camera-reference row, camera event `animSRRefId`, camera `NodeRef`, camera entity, origin marker, and activation flag |
| View/fog/setup layer is missing | Scene prop record, corresponding `.ent`, support marker, prop spawn policy, visibility events, and stream availability |
| Clue appears but quest does not advance | Layer/time interval, clue entity reference, discovery node, fact name/value, and quest-side fact wait |
| Exit leaves V or UI in the wrong state | Named output route, normal/interrupted cleanup symmetry, teleport/restore ordering, UI/input restoration, and save provenance |
| Replay uses stale results | Discovery facts, journal state, one-shot guards, active scene state, and explicit reset/preserve policy |

Next: [RID playback and rewind](rid-playback-and-rewind.md).
