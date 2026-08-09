# Documentation scripts

This directory is reserved for small, optional maintenance utilities such as
diagram rendering, link validation, or example-project checks.

Scripts must support the documentation workflow; they must not become a
prerequisite for understanding or authoring native Cyberpunk 2077 quests.

Current utilities:

- `validate.py` is the single local and CI validation command. It regenerates
  Lab 1's CR2W-JSON into a temporary directory; checks the manifest, source
  and checkpoint inventories, Git tracking, LF-normalized text, exact
  ArchiveXL section nesting, manifest SHA-256 values, the immutable runtime
  acceptance contract and reader-facing evidence status, cooked CR2W headers,
  graph fingerprint, and exact SVG; and builds each checkpoint twice to verify
  ZIP entries, metadata, atomic failure behavior, and repeatability.
- `build_lab01_sources.py` deterministically rebuilds the book-owned Lab 1
  CR2W-JSON review artifacts. It is not part of the reader workflow.
- `render_quest_graph.py` renders an exact SVG from WolvenKit CR2W-JSON plus a
  layout-only override and rejects stale source fingerprints.
- `package_examples.py` creates deterministic ZIP downloads for the start and
  completed checkpoints.

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
