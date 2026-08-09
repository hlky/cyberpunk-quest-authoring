# Documentation scripts

This directory is reserved for small, optional maintenance utilities such as
diagram rendering, link validation, or example-project checks.

Scripts must support the documentation workflow; they must not become a
prerequisite for understanding or authoring native Cyberpunk 2077 quests.

Current utilities:

- `validate.py` is the single local and CI validation command. It regenerates
  all five labs' CR2W-JSON into temporary directories; checks manifests, source
  and checkpoint inventories, Git tracking, LF-normalized text, exact
  ArchiveXL section nesting, manifest SHA-256 values, runtime-acceptance
  contracts and reader-facing evidence status, mdBook SUMMARY coverage and
  internal links, first-release troubleshooting/reference coverage, canonical
  lab identities and navigation, the bounded legacy-runtime ledger and every
  reader-page hash occurrence, journal/localization semantics, cooked CR2W
  headers, graph fingerprints, and exact SVGs; and builds every checkpoint
  twice to verify ZIP entries, metadata, atomic failure behavior, and repeatability.
- `build_lab01_sources.py` deterministically rebuilds the book-owned Lab 1
  CR2W-JSON review artifacts. It is not part of the reader workflow.
- `build_lab02_sources.py` deterministically rebuilds both Lab 2 checkpoints'
  mod-owned CR2W-JSON review artifacts. It is not part of the reader workflow.
- `validate_lab02.py` supplies Lab 2's exact graph, two-variant evidence,
  journal/localization, resource-pair, and checkpoint validation to the shared
  entry point.
- `build_lab03_sources.py` deterministically rebuilds both Lab 3 checkpoints'
  six mod-owned CR2W-JSON resources. It is not part of the reader workflow.
- `build_lab03_diagrams.py` validates Lab 3's exact graph and emits its graph,
  resource-chain, and trigger-volume SVGs plus the bound layout fingerprint.
- `validate_lab03.py` supplies Lab 3's exact graph, journal/mappin, trigger
  buffer, NodeRef, sector/block, manifest, and acceptance checks to the shared
  entry point.
- `build_lab04_sources.py` deterministically rebuilds both Lab 4 checkpoints'
  seven mod-owned resources, including the registered root and archive-resolved
  child questphases.
- `build_lab04_diagrams.py` validates the exact Lab 4 root and child graphs and
  emits their SVGs plus the resource-chain and terminating-handoff diagrams.
- `validate_lab04.py` supplies Lab 4's root-only registration, external-phase
  socket, prefab-scope, graph, world, evidence, and diagram checks. Pass
  `--wkit <WolvenKit.CLI>` to repeat the pinned 8.19.0 cook and serialize
  round trip locally; the shared CI entry point remains dependency-free.
- `build_lab05_sources.py` deterministically rebuilds both Lab 5 checkpoints'
  eleven mod-owned CR2W-JSON resources and preserves the separately licensed,
  hash-bound WAV/WEM assets.
- `build_lab05_diagrams.py` validates the frozen root, child, scene, community,
  resource, lifecycle, and trigger contracts and emits seven deterministic
  exact or conceptual SVGs with explicit metadata.
- `validate_lab05.py` supplies Lab 5's community identity joins, graph and
  scene topology, localization/voice chain, world ownership, audio provenance,
  schema-version-4 five-capture save lineage, acceptance record, manifest, and
  diagram checks. It freezes two originals, three Case-1 manual seeds,
  closed-game full-slot execution clones, exact fan-out hashes, and unique
  execution directories. Pass `--wkit <WolvenKit.CLI>` to repeat the pinned
  8.19.0 cook and serialize round trip.
- `render_quest_graph.py` renders an exact SVG from WolvenKit CR2W-JSON plus a
  geometry-only override (including optional edge waypoints) and rejects stale
  source fingerprints.
- `package_examples.py` creates deterministic ZIP downloads for all start and
  completed checkpoints. Lab 2 through Lab 5 evidence files are included only
  when a safe `evidence/` path is named by the matching acceptance record;
  unreferenced extras keep failing the closed-inventory check. Each Lab 5 ZIP
  also receives the one repository-owned `voice-source` provenance bundle as
  explicit, hash-checked external entries rather than duplicating it in both
  project trees.

From the repository root, run the complete validation suite with:

```console
python scripts/validate.py
```

The suite has no third-party Python dependencies and does not invoke
WolvenKit. Its default binary/source check is intentionally limited to locally
provable provenance: CR2W magic, the CR2W-JSON archive filename and resource
type, and the cooked resource's matching root-type string. It does not prove a
WolvenKit round trip or in-game behavior. The optional Lab 4 and Lab 5
`--wkit` gates are explicit local exceptions and are not run by `validate.py`.

Scripts in this directory are licensed under the MIT License.
