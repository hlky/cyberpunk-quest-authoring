# Editorial And Visual Style

## Voice

Write for an intelligent reader who is new to Cyberpunk quest authoring. Define
engine-specific terms when they first appear. Prefer concrete explanations over
large property dumps or unexplained recipes.

Lead with the outcome and mental model, then introduce exact RED types and
properties.

## Terminology

- Use **questphase** for a `.questphase` resource.
- Use **scene** for a `.scene` resource.
- Use **graph node** for an executable quest or scene graph node.
- Use **NodeRef** for a world reference. Do not use it as a synonym for a CR2W
  handle.
- Keep actor ID, performer ID, screenplay item ID, localization ID, event ID,
  and CR2W handle ID distinct.
- Use **vanilla** for resources shipped with the game.
- Use **native quest resource** for the game's own quest/scene resource model;
  avoid implying RED4ext native-plugin development.

## Graph figures

Do not use WolvenKit graph screenshots as instructional figures.

Use three levels where appropriate:

1. **Story view** — a small Mermaid or equivalent flow describing player-facing
   behavior.
2. **Engine view** — a deterministic SVG containing exact node types, IDs,
   sockets, and edges.
3. **Resource view** — a diagram or table showing which resource owns each
   responsibility.

Exact node graphs should show:

- stable tutorial node IDs;
- concrete node types or familiar editor labels;
- input and output socket names;
- edge socket names where they are not obvious;
- cut/interrupt edges;
- short summaries of decisive conditions;
- child-phase or subsystem boundaries.

Move large nested properties into nearby node-detail cards or tables.

## Visual grammar

| Visual | Meaning |
| --- | --- |
| Grey capsule | Input, output, start, or end |
| Amber diamond | Condition, pause, gate, or wait |
| Purple rectangle | Fact or persistent state |
| Green rectangle | Journal, objective, message, or mappin |
| Blue rectangle | Gameplay action |
| Teal rectangle | World, community, actor, vehicle, or device |
| Rose rectangle | Scene, dialogue, or screenplay |
| Red rectangle | Failure, cleanup, or interruption |
| Solid edge | Normal execution |
| Dashed red edge | Cut or interrupt |
| Dotted edge | Resource or lookup relationship |

Do not rely on color alone. Shapes, labels, line styles, and accessible text
must preserve meaning.

## Screenshots

Screenshots may be used only when a genuinely visual editor action cannot be
explained more clearly with a diagram, property path, or table. Crop to the
relevant control and accompany the image with textual instructions.

## Code and data excerpts

- Prefer the smallest excerpt that proves the relationship.
- Use depot paths exactly as the game and WolvenKit display them.
- Explain whether a value is a string, CName, NodeRef, ResourcePath, TweakDBID,
  numeric ID, or handle.
- Do not make raw JSON editing the default beginner workflow.
