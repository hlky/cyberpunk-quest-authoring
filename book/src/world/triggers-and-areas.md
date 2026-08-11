# Triggers and areas

A trigger objective crosses two resources. A streamed `worldTriggerAreaNode`
owns the volume and its notifier; a questphase `questTriggerCondition` asks
about that volume through a NodeRef. Neither side creates the other.

```text
streaming sector
  -> worldTriggerAreaNode
     -> AreaShapeOutline.buffer
     -> questTriggerNotifier_Quest

questphase
  -> questTriggerCondition
     -> triggerAreaRef
     -> Entered / Exited / IsInside / IsOutside
```

## The world node owns the volume

The concrete sector node supplies type-specific behavior. Its compact shape
is:

```text
worldTriggerAreaNode
  debugName
  outline: AreaShapeOutline
    buffer
    points
    height
  notifiers[]
    questTriggerNotifier_Quest
```

The sector's separate `nodeData` record supplies position, orientation, scale,
bounds, `NodeIndex`, and the full `QuestPrefabRefHash`. The outline points are
local to that placement. Moving only the points is not equivalent to moving
the node, and changing only the node position does not resize its outline. See
[Sector nodes and placement](sector-nodes-and-placement.md).

## `AreaShapeOutline.buffer` is authoritative

In the inspected serialized shape, `AreaShapeOutline.buffer` contains:

```text
little-endian uint32 point count
  -> point 0: four little-endian floats (X, Y, Z, W)
  -> point 1: four little-endian floats (X, Y, Z, W)
  -> ...
  -> trailing little-endian float height
```

The inspected mod-owned outlines use local `Vector4` points with `W = 1`.
WolvenKit can serialize the visible `points` property as a default square even
when the buffer contains a different polygon. Therefore the visible array is
not sufficient evidence of the effective volume.

For every edit:

1. Review the intended local points, point order, and height.
2. Regenerate or edit the authoritative buffer through a supported,
   reproducible authoring path.
3. Round-trip the CR2W and verify the buffer still decodes to the intended
   count, points, and height.
4. Review the node transform and vertical placement separately.
5. Test crossings from several directions and elevations in game.

Do not paste a buffer from a different location simply because its visible
`points` look plausible. The count, point payload, height, transform, bounds,
and intended approach form one geometry contract.

## The notifier exposes the area to quest logic

The focused Quest-sector sample uses `questTriggerNotifier_Quest` on trigger
nodes. Retained values include `isEnabled`, `includeChannels`, and
`excludeChannels`; one inspected quest-notifier shape uses `TC_Default` for
the included channels. Those values are **Observed in vanilla**, not a promise
that every trigger family or activator uses the same channel configuration.

An outline without the intended notifier may be valid geometry but invisible
to the quest condition. Conversely, a condition with a valid-looking NodeRef
does not attach a notifier to the world node. Inspect both owners.

## The condition owns the question

`questTriggerCondition` carries four decisive properties in the retained
shape:

| Property | Responsibility |
| --- | --- |
| `type` | Selects edge-shaped or state-shaped trigger semantics |
| `triggerAreaRef` | Local NodeRef of the area being queried |
| `activatorRef` | Explicit activator identity where the authored shape uses one |
| `isPlayerActivator` | Selects player activation in the inspected player-targeted shape |

A focused **Observed in vanilla** condition excerpt is:

```text
questTriggerCondition
  activatorRef: gameEntityReference
    reference: 0
    type: EntityRef
  isPlayerActivator: 1
  triggerAreaRef: #q108_tr_mainframe
  type: IsInside
```

The zero reference and `isPlayerActivator: 1` belong to that inspected player
condition. Do not replace an empty, local, or explicit activator reference
from a known-good comparison without understanding that comparison's context.

## Edge and state conditions are not synonyms

| `type` | Question asked | Important test boundary |
| --- | --- | --- |
| `Entered` | Did the activator cross from outside to inside? | An already-inside reload may not produce a new entry edge. |
| `Exited` | Did the activator cross from inside to outside? | Starting outside is not the same event as leaving. |
| `IsInside` | Is the activator currently inside? | Suitable for a state check, but reload evaluation still needs runtime evidence. |
| `IsOutside` | Is the activator currently outside? | Can already be true before the intended sequence unless graph order constrains it. |

The retained enum also exposes `AllInsideMP` and `AllOutsideMP`. Their names
are not enough to teach multiplayer semantics, so this chapter records their
existence without prescribing them.

Choose semantics from the player story. “Cross the threshold now” is an edge.
“Proceed whenever the player is already in the area” is a state. A leave step
must activate only after the reach step; otherwise `IsOutside` can satisfy
before the player ever enters.

## Boundary Check trigger contract

**Structurally validated:** Lab 3 uses two independently placed areas beneath
one quest-prefab root:

| Area | Condition | Encoded geometry |
| --- | --- | --- |
| `#cqa003_tr_reach` | `IsInside` | 25-unit radius, 16 points, height 12 |
| `#cqa003_tr_leave` | `IsOutside` | 110-unit radius, 20 points, height 16 |

The graph activates the reach objective and waits for `IsInside`; only after
that succeeds does it activate the leave objective and wait for `IsOutside`.
The larger outer area prevents an ordinary step back across the reach boundary
from completing both stages at once. The resource values and graph order are
checked; vertical coverage, state evaluation, and approach behavior remain
**Experimental** acceptance questions.

## Save-aware acceptance matrix

Use a save made before any version of the mod was installed. Retain separate
save slots; do not keep overwriting the only clean control.

| Case | What it distinguishes |
| --- | --- |
| Start outside both areas | Negative control for premature `IsInside` success |
| Walk into the reach area | Normal state or edge activation path |
| Save before reaching, then reload | Quest and journal state restoration before a crossing |
| After reach succeeds, save inside the outer leave area and reload | The active `IsOutside` wait stays false until departure |
| Leave the outer area | Ordered leave behavior and vertical/outline coverage |
| Reload after completion | One-shot fact, journal cleanup, and stale trigger state |
| Reinstall and use an old save | Demonstrates why archive replacement does not reset save-backed state |

This matrix does not load a save while the active reach wait is already inside
`#cqa003_tr_reach`. It therefore does not prove `IsInside` evaluation for that
on-load state; add a separately bound case before making that claim.

Record the exact installed archive, resource hashes, starting save provenance,
approach direction, player Z, observed objective transition, and relevant
ArchiveXL/game logs. A successful pack or WolvenKit open cannot support
**Runtime-proven** by itself.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Condition never changes | Trigger notifier, local/full NodeRef chain, sector registration, and activator selection |
| Trigger fires at a default square | Authoritative `AreaShapeOutline.buffer`, not only visible `points` |
| Trigger is offset | Node placement, outline-local coordinates, pivot, orientation, and scale |
| Enter works but an inside reload stalls | `Entered` versus `IsInside`, then retained runtime evidence for that exact graph |
| Leave succeeds before reach | Graph activation order and premature `IsOutside` evaluation |
| Behavior differs by elevation | Base Z, trailing buffer height, placement bounds, and real site geometry |
| A clean run works but an old save does not | Facts, journal state, checkpoints, and prior trigger lifecycle are separate saved variables |

Previous: [Sector nodes and placement](sector-nodes-and-placement.md). Next:
[Markers and navigation](markers-and-navigation.md).
