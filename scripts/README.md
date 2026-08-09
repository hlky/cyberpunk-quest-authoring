# Documentation scripts

This directory is reserved for small, optional maintenance utilities such as
diagram rendering, link validation, or example-project checks.

Scripts must support the documentation workflow; they must not become a
prerequisite for understanding or authoring native Cyberpunk 2077 quests.

Current utilities:

- `validate.py` is the single local and CI validation command. It regenerates
  both labs' CR2W-JSON into temporary directories; checks manifests, source
  and checkpoint inventories, Git tracking, LF-normalized text, exact
  ArchiveXL section nesting, manifest SHA-256 values, runtime-acceptance
  contracts and reader-facing evidence status, mdBook SUMMARY coverage and
  internal links, journal/localization semantics, cooked CR2W headers, graph
  fingerprints, and exact SVGs; and builds every checkpoint twice to verify
  ZIP entries, metadata, atomic failure behavior, and repeatability.
- `build_lab01_sources.py` deterministically rebuilds the book-owned Lab 1
  CR2W-JSON review artifacts. It is not part of the reader workflow.
- `build_lab02_sources.py` deterministically rebuilds both Lab 2 checkpoints'
  mod-owned CR2W-JSON review artifacts. It is not part of the reader workflow.
- `validate_lab02.py` supplies Lab 2's exact graph, two-variant evidence,
  journal/localization, resource-pair, and checkpoint validation to the shared
  entry point.
- `render_quest_graph.py` renders an exact SVG from WolvenKit CR2W-JSON plus a
  geometry-only override (including optional edge waypoints) and rejects stale
  source fingerprints.
- `package_examples.py` creates deterministic ZIP downloads for all start and
  completed checkpoints. Lab 2 evidence files are included only when a safe
  `evidence/` path is named by its acceptance record; unreferenced extras keep
  failing the closed-inventory check.

From the repository root, run the complete validation suite with:

```console
python scripts/validate.py
```

The suite has no third-party Python dependencies and does not invoke
WolvenKit. Its binary/source check is intentionally limited to locally
provable provenance: CR2W magic, the CR2W-JSON archive filename and resource
type, and the cooked resource's matching root-type string. It does not prove a
WolvenKit round trip or in-game behavior.

Scripts in this directory are licensed under the MIT License.
