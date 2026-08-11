# NodeRefs, streaming, and placement

A valid-looking NodeRef does not create a world object. The reference must join
the questphase's namespace to a loaded streaming block, the intended sector,
a registered full child identity, and a concrete placed node.

## Audit the complete identity chain

For a quest-prefab child, write all four values side by side:

```text
quest local child:       #example_trigger
phase prefab root:       #example_prefab
block full root:         $/mod/example/#example_prefab
sector full child:       $/mod/example/#example_prefab/#example_trigger
```

Then find the concrete node and placement data associated with that full child
in the authored sector. In the compact tutorial sectors, `NodeIndex` connects
node data to `nodes[]`; do not assume row position is the relationship, and do
not generalize that compact layout to every cooked vanilla sector.

## Route by symptom

| Symptom | First diagnosis | Decisive test |
| --- | --- | --- |
| Trigger never fires anywhere | Broken identity chain, notifier, activator contract, or condition state | Trace local child, root, descriptor, full child, concrete trigger/notifier, and consuming condition |
| Object works only when already nearby | Streaming descriptor/bounds or lifecycle dependency | Start outside, approach normally, then stream away and return on a controlled save |
| Marker exists but quest cannot find it | Marker identity differs from quest NodeRef | Compare exact local/full paths and phase-prefab owner |
| Quest finds a trigger but it is in the wrong place | Placement transform or trigger geometry | Inspect position, rotation, scale, and shape points in the sector |
| Mappin log cannot resolve position | UI lookup cannot resolve the target identity | Use a proven marker strategy and keep gameplay/UI identities explicit |
| Device looks correct but old behavior persists | Save-backed controller identity | Retest from pre-install save; for deliberate identity invalidation, use a fresh NodeRef |
| Fast travel crashes while ordinary approach works | Streaming-time activation race or malformed streamed resource | Preserve crash boundary, test block/sector alone, then reintroduce quest activation |

## Check loading before logic

1. Confirm ArchiveXL registers the exact streaming block path.
2. Confirm every descriptor's sector path exists in the archive.
3. Check the descriptor category and bounds. A finite Quest descriptor must
   cover the approach and intended activity; an AlwaysLoaded sector has a
   different lifetime and should not become a default dumping ground.
4. Confirm `questPrefabNodeRef` is present where the world-side root binding is
   required.
5. Confirm the sector registers each full child in `nodeRefs`.
6. Inspect the associated concrete node and its node data.
7. For a trigger, inspect its `questTriggerNotifier_Quest`: require the intended
   `isEnabled`, `includeChannels`, and `excludeChannels` values.
8. Inspect the consuming `questTriggerCondition`: match `triggerAreaRef` and
   predicate `type`, and verify `isPlayerActivator` plus `activatorRef`. Labs
   3–5 use `isPlayerActivator: 1` with the exact empty entity-reference payload;
   do not substitute an arbitrary actor NodeRef.
9. Test the world resource without starting the dependent scene or complex
   quest branch when possible.

If the sector does not load, editing the trigger condition cannot help. If the
sector loads but the quest cannot resolve a child, compare the prefab namespace
before moving geometry.

## Check placement and trigger geometry

A NodeRef can resolve perfectly while its object is above, below, rotated away
from, or too far from the player. Record:

- world position and orientation;
- sector node transform and any local transform;
- trigger point order, height, and scale;
- expected horizontal and vertical approach paths;
- descriptor bounds and streaming distance;
- whether the player was teleported, fast-travelled, or approached normally.

Test trigger state with one route at a time. An `IsInside` wait and an
`IsOutside` cleanup condition need different starting positions and save
points. Increasing every trigger radius after one missed activation can hide a
vertical placement error or make several scene conditions true in the same
startup tick.

## Separate world and UI targets

A gameplay operation may need a native device NodeRef while the journal UI
needs a marker whose position is reliably resolvable. Keep the responsibilities
explicit:

| Responsibility | Possible owner |
| --- | --- |
| Device reservation/interaction | Native or mod-owned device NodeRef |
| Quest condition | Trigger or device NodeRef under the quest prefab |
| In-world scene placement | Scene marker NodeRef |
| Journal/map presentation | Dedicated static marker/mappin NodeRef |

Using separate identities is not automatically correct; it is a design that
must preserve coordinates, lifecycle, and cleanup. Conversely, forcing one
NodeRef into every subsystem is not automatically simpler if one lookup cannot
resolve it.

## Stream-away and reload tests

After ordinary activation works, test independently:

1. load a named pre-activation seed outside the finite descriptor;
2. approach normally and verify one activation;
3. stream away by ordinary movement, return, and check reacquisition without
   duplication;
4. load a separate save captured while the world-dependent stage is active;
5. finish and verify cleanup;
6. reload a completed save and confirm the root guard prevents reactivation.

Fast travel is a separate stress case because it can cross streaming and quest
activation boundaries in one transition. Do not treat a normal-approach pass
as proof of fast-travel safety.

## Avoid speculative fixes

- Do not add both local and full forms to arbitrary fields.
- Do not duplicate `phasePrefabs` across root and child without an
  evidence-matched ownership policy.
- Do not move a marker into AlwaysLoaded merely because one Quest-sector test
  used the wrong bounds.
- Do not rename a persistent device NodeRef without deciding whether the old
  saved identity should be abandoned.
- Do not copy a vanilla sector into the mod; cite and inspect it, then author
  mod-owned resources.

Previous: [Handles, sockets, and resources](handles-sockets-resources.md).
Next: [Actors, scenes, and lipsync](actors-scenes-lipsync.md).
