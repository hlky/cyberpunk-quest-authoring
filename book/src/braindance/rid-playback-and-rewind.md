# RID playback and rewind

The `.scenerid` stores recorded scene animation data. The `.scene` decides
which recorded channel plays, which performer or camera receives it, where it
is placed, and when it appears on a rewindable timeline. Neither resource is
self-sufficient.

> **Research note:** the field shapes and focused counts from
> `sq012_braindance__part_a.scenerid` and `sq012_02a_braindance.scene` are
> **Observed in vanilla** on Cyberpunk 2077 `2.31a`, re-extracted and inspected
> with WolvenKit `8.19.0` on 2026-08-09. The retained mod-owned RID/scene pair
> round-trips with WolvenKit `8.19.0` and is **Structurally validated**. Custom
> playback, camera, seek, rewind, facial/cyberware channels, and interruption
> remain **Experimental**.

Runtime promotion requires a clean retest on an untouched pre-install save.
Scene playback, current playhead position, clue state, camera ownership, and
quest facts are save-backed or session-backed observations; do not infer a
clean replay from a save that has already entered the candidate braindance.

## Two resources, three reference levels

The complete recorded-animation lookup is:

```text
scnRidResource (.scenerid)
  actor/camera scnRidTag(signature, serialNumber)
  animation scnRidSerialNumber + buffer
          |
          | selected by resource ID + animation serial
          v
scnSceneResource.resouresReferences
  ridAnimations[] / ridFacialAnimSets[] / ridCyberwareAnimSets[]
  ridCameraAnimations[]
          |
          | selected by scene-local reference-array ID
          v
scnRewindableSectionNode event
  performer + animResRefId
  or cameraRef + animSRRefId
```

The misspelled serialized property name `resouresReferences` is the native
field exposed by these resources. Preserve the field name WolvenKit presents;
do not “correct” a serialized property based on prose.

### RID resource identity

An `scnRidResourceHandler` in the scene binds:

- a typed `scnRidResourceId`; and
- an exact `.scenerid` `ResourcePath`.

The resource ID is scene data, not the depot-path hash and not an array index.
A scene reference such as `scnRidAnimationSRRef` then combines that resource
ID with an animation `scnRidSerialNumber` from the selected RID.

### Scene-local reference identity

RID animation events do not carry the resource path and serial directly. A
body event's `scnRidAnimationSRRefId` selects an entry in the scene's RID
animation-reference arrays. A camera event's
`scnRidCameraAnimationSRRefId` selects a camera-reference entry. Array
membership and typed ID must be re-audited whenever resources or channels are
added, removed, or reordered.

### Performer and camera identity

`scnPlayRidAnimEvent.performer` is an `scnPerformerId`; it is not the RID
signature. The scene's actor/player/prop definitions establish the performer
map. A camera event instead carries a world `cameraRef` `NodeRef`, a camera RID
reference, and an origin marker.

This produces two independent joins:

```text
RID actor signature -> RID animation serial -> scene RID ref -> performer
RID camera signature -> RID camera serial -> scene camera ref -> camera NodeRef
```

Do not force actor and camera identities into one shared counter scheme.

## What version-5 `.scenerid` owns

The focused SQ012 part-A resource has root type `scnRidResource`, `version: 5`,
and these principal fields:

| Field | Role |
| --- | --- |
| `nextSerialNumber` | Next RID-local serial allocation; not a scene node/event ID |
| `actors[]` | `scnActorRid` entries identified by `scnRidTag` |
| `cameras[]` | `scnCameraRid` entries identified by `scnRidTag` |
| Actor `animations[]` | Body/root-motion `scnAnimationRid` channels |
| Actor `facialAnimations[]` | Facial channels with their own animation objects and cardinality |
| Actor `cyberwareAnimations[]` | Optional cyberware channels; absence is a valid empty array for many actors |
| Camera `animations[]` | Camera transform/optical channels referenced by RID-camera scene events |

In this exact vanilla part, nine actor entries and one camera entry are
present. Seven actor entries have one body and one facial animation; one of
those also has a cyberware animation. Two prop-like RID actors have no
animation arrays. This observation demonstrates optional channel sets; it
does not define a required custom layout.

## Animation buffer invariants

An animation entry ultimately owns an `animAnimation` and an animation buffer
such as `animAnimationBufferCompressed`. Focused properties include:

- animation and buffer duration;
- frame count;
- joint count and track count;
- raw/constant key counts;
- extra joint/track counts;
- compressed or deferred buffer bytes;
- optional motion extraction;
- camera LOD samples for camera animation.

Those numbers must describe one compatible rig/channel layout. A binary can
serialize while still containing the wrong joint order, wrong track mapping,
invalid root-motion basis, mismatched duration, or incompatible facial/
cyberware cardinality. WolvenKit round-trip success is therefore necessary but
not sufficient.

For every custom channel, record a small manifest like this before linking the
scene:

| Manifest field | Record |
| --- | --- |
| RID depot path and local SHA-256 | Binds evidence to bytes |
| RID root version | Prevents assumptions from another layout version |
| Actor/camera signature | Names the intended RID slot |
| Tag serial and animation serial | Proves RID-local identity |
| Channel | Body, facial, cyberware, or camera |
| Duration and frame rate basis | Supports event timing comparison |
| Joint/track counts and ordered rig contract | Detects compatible-looking but wrong buffers |
| Motion-extraction/root policy | Distinguishes trajectory motion from in-place pose |
| Source and conversion versions | Makes a later rebuild comparable |

Do not publish a vanilla `.scenerid`, its full serialized JSON, or its
compressed buffer bytes. The table is a focused provenance record, not a
redistribution mechanism.

## Recorded placement is another contract

A body event observed in the SQ012 scene includes:

- `performer` (`scnPerformerId`);
- `animResRefId` (`scnRidAnimationSRRefId`);
- `animOriginMarker` with a global scene-marker `NodeRef`;
- `actorPlacement: SceneOrigin`;
- `startTime` and `duration`;
- blend, collision, component, camera-parallax, and trajectory settings.

The first event in the inspected section uses the global origin
`#sq012_02a_sm_braindance`, begins at `0`, and lasts `33333` scene-time units.
That exact value is **Observed in vanilla**, not a universal conversion rule
for seconds or frames.

If an actor's recorded root is authored in a different coordinate basis than
the scene marker, every otherwise valid pose can appear offset or rotated.
Audit these as one transform equation:

```text
world scene-marker transform
  * event placement/origin policy
  * RID actor root / motion extraction
  = expected world-space performance
```

Test translation, yaw, elevation, and return-to-origin separately. A single
actor standing at `(0, 0, 0)` cannot expose every basis error.

## Recorded-perspective camera

The inspected `scneventsPlayRidCameraAnimEvent` contains:

| Property | Focused meaning |
| --- | --- |
| `animSRRefId` | Scene-local index into a RID-camera reference array |
| `cameraRef` | Full world `NodeRef` for the camera entity |
| `animOriginMarker` | Marker defining the recorded coordinate origin |
| `cameraPlacement` | Placement policy such as `SceneOrigin` |
| `activateAsGameCamera` | Whether the event takes over the game camera |
| `controlRenderToTextureState` | Whether this event controls that state; not equivalent to the BD setup prop |
| `startTime` / `duration` | Timeline interval that must agree with the recorded channel |
| `markCamerCut` | Cut marking for this event |

The SQ012 scene's camera `NodeRef`, the camera prop/entity, the RID camera
reference, the origin marker, and the event are five separate checks. Seeing a
camera in the streamed world does not prove the RID camera channel is active.

`engine\scenesystem\camera.ent` exists in the installed `2.31a` archives and
is a useful type/shape comparison for a placed scene camera. Its existence is
not permission to reuse arbitrary vanilla placement or quest-local IDs.

## Rewindable section anatomy

The native timeline container is `scnRewindableSectionNode`, not an ordinary
`scnSectionNode` with a rewind flag added elsewhere. In the focused SQ012
scene it owns:

- `sectionDuration.stu: 89300`;
- `ffStrategy: automatic`;
- forward slow/fast/very-fast modifiers `0.5`, `3`, and `6`;
- backward slow/fast/very-fast modifiers `0.5`, `3`, and `6`;
- 115 timed events;
- output sockets for ordinary progress and side routes.

Its event inventory includes dialog/audio, skeletal animation, RID actor
animation, RID camera animation, clue windows, BD visibility, VFX, prop
attachment, and socket events. This is **Observed in vanilla** for the named
scene. It demonstrates that rewindability coordinates multiple event types;
it does not require every custom recording to contain all of them.

### Rewind safety questions

For each event, answer:

1. Is it a pure function of current timeline time, or does it cause a durable
   side effect?
2. What state must be reconstructed when the playhead seeks into its middle?
3. What is undone when the playhead moves backward across its start?
4. Does its end state differ when playback jumps past the whole interval?
5. Does it target an actor, prop, camera, clue, VFX, UI state, fact, or socket?
6. Is the side effect allowed to happen more than once?

Facts, journal mutations, item operations, spawning, and quest sockets deserve
special scrutiny. A timeline may revisit their event time, while the quest
side effect may be intentionally one-shot. Make that policy explicit instead
of assuming rewind will undo persistent state.

## Inspect the RID link in WolvenKit

Use a disposable project and extract:

```text
base\quest\side_quests\sq012\scenes\sq012_02a_braindance.scene
base\animations\quest\side_quests\sq012\sq012_braindance\rid\sq012_braindance__part_a.scenerid
```

Then record this focused cross-reference without copying the resources:

1. In the scene, list each `ridResources[]` handler's resource ID and depot
   path.
2. In `resouresReferences`, list each RID animation/camera reference's
   resource ID and serial number.
3. In the RID, find the corresponding actor/camera tag and animation serial.
4. In the rewindable section, select one body event and one camera event;
   record their local reference IDs, performer/camera, origin, start, and
   duration.
5. Verify that the event's local reference resolves to the expected RID
   resource/serial pair.
6. Compare the event interval with the animation duration and the section
   duration.

Do not rely on graph-screen position. The typed IDs and property values are
the evidence.

## Manual composition order for a mod-owned candidate

1. Finish the ordinary scene actor/prop acquisition and named entry/exit
   contract before introducing RID playback.
2. Add the mod-owned RID resource and inventory all tags, serials, channels,
   durations, joint counts, and track counts.
3. Allocate a unique scene `scnRidResourceId` and add its handler/path.
4. Add scene-level body/facial/cyberware/camera references, pairing the exact
   resource ID with exact RID animation serials.
5. Add one short body event and verify its performer, origin, placement,
   duration, and local reference ID structurally.
6. Add one short camera event and verify its camera entity and marker chain.
7. Only then add the full rewindable section and the remaining channels.
8. Re-inspect every reference ID after array edits; do not assume earlier
   indexes stayed stable.
9. Serialize to CR2W, serialize the binary back to JSON, and compare root
   type, RID handlers, serial mappings, event references, durations, and
   cardinalities.
10. Keep the result **Experimental** until all runtime cases pass on the exact
    package hash.

This sequence localizes failures. It is not a claim that arbitrary compressed
animation buffers can be authored correctly by filling WolvenKit fields by
hand. A buffer-production tool may be needed, but it remains an author tool,
not evidence that the native runtime contract passed.

## Structural acceptance checklist

- [ ] `.scenerid` root type/version and each actor/camera tag are recorded.
- [ ] Every tag and animation serial is unique in its required scope.
- [ ] Every buffer has expected duration, frame, joint, and track counts.
- [ ] Every scene RID handler resolves an exact mod-owned depot path.
- [ ] Every scene RID reference resolves an existing resource/serial pair.
- [ ] Every event's local reference ID selects the intended scene reference.
- [ ] Performer/camera, origin marker, placement, start, and duration are
      explicit.
- [ ] The rewindable section contains no unexplained durable side effect.
- [ ] WolvenKit binary-to-JSON-to-binary conversion succeeds.
- [ ] Packed paths and hashes are retained before runtime testing.

Passing this checklist supports **Structurally validated**, not
**Runtime-proven**.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Nothing moves but the scene advances | RID handler path/ID, scene reference resource/serial, event local ID, performer, and event interval |
| Wrong actor receives motion | RID signature/serial map, scene performer map, and event `performer` |
| Actor snaps or drifts | Scene marker transform, recorded root basis, motion extraction, placement policy, and duration/stretch |
| Body works but face or cyberware does not | Separate channel presence, joint/track cardinality, scene anim-set reference, actor component, and event binding |
| Camera remains gameplay camera | RID camera serial/reference, event local ID, `cameraRef`, `activateAsGameCamera`, marker, and camera entity |
| Forward playback works but seeking breaks | Event reconstruction at arbitrary time, side effects crossed by seek, interval coverage, and replayable state |
| Binary round-trips but crashes or corrupts at runtime | Buffer layout/cardinality, resource/serial mapping, actor rig compatibility, and current package hash; serialization alone is not runtime proof |

Next: [Clue layers, cleanup, and
acceptance](clue-layers-cleanup-and-acceptance.md).
