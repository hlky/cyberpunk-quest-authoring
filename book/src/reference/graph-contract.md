# Exact graph contract

Exact quest and scene figures use **WolvenKit CR2W-JSON plus a small layout
override**.

The serialized resource is the only structural source. The renderer reads:

- graph node IDs and RED types;
- socket names and socket direction;
- graph connections;
- decisive fact, journal, time, scene, and resource properties.

The layout file may specify canvas size, node positions, and box dimensions. It
must not declare nodes, sockets, edges, or condition values. This prevents a
hand-maintained diagram manifest from drifting into a second, more convenient
version of the quest.

## Fingerprint

The renderer canonicalizes the structural graph and records its SHA-256
fingerprint in the layout file and SVG metadata. Rendering fails when the
recorded fingerprint does not match the CR2W-JSON source.

This detects changes to node IDs, node types, sockets, edges, and decisive
property summaries. Moving a box does not change the fingerprint.

## Repository layout

For an example named `cqa001`:

```text
examples/.../source/raw/.../cqa001.questphase.json
assets/diagrams/lab-01/cqa001.questphase.layout.json
book/src/images/lab-01/cqa001.questphase.svg
```

The JSON is a serialized review artifact for a mod-owned CR2W resource. Readers
author and inspect the resource in WolvenKit; raw JSON editing is not the
beginner workflow. The renderer is optional documentation infrastructure under
`scripts/`.

## Review rule

A graph figure is exact only when all of the following are true:

1. its source is a supplied or cited CR2W resource;
2. its recorded fingerprint matches;
3. every rendered node and edge comes from that source;
4. any omitted property is described beside the figure;
5. its evidence label states whether the custom arrangement is runtime-proven,
   structurally validated, observed in vanilla, or experimental.
