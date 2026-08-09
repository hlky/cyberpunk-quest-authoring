# Cyberpunk Quest Authoring Agent Guide

This repository contains first-principles documentation for authoring native
Cyberpunk 2077 quest resources. The rules below are the durable scope for broad
planning and content work.

## Core rules

- Document the game resource model, not the Ghostline authoring system.
- Reader-facing procedures may use WolvenKit, ArchiveXL, the game, and
  chapter-specific standard tools. They must not require Ghostline generators,
  manifests, explorers, or compilers.
- Do not use WolvenKit graph screenshots to explain graph structure. Use
  conceptual diagrams, deterministic SVG node graphs, property tables, and
  downloadable WolvenKit projects.
- Treat downloadable example projects as executable reference material, but
  explain every supplied node and resource instead of presenting templates as
  magic.
- Do not redistribute extracted vanilla CR2W resources. Cite depot paths and
  teach readers how to extract their own references.
- Label claims as runtime-proven, structurally validated, observed in vanilla,
  or experimental.
- Record the tested Cyberpunk, WolvenKit, ArchiveXL, and other relevant
  versions on practical guides.
- Call out clean-save requirements and save-backed facts, journal state,
  scenes, communities, and device persistent state.
- Prefer focused CR2W excerpts. Do not paste complete large serialized
  resources into chapters.

## Repository map

- `book/src` contains the mdBook source.
- `book/theme` contains book presentation assets.
- `examples` is reserved for downloadable incremental WolvenKit projects.
- `assets/diagrams` is reserved for generated SVG source and outputs that are
  shared across chapters.
- `evidence` contains machine-readable provenance and acceptance boundaries
  used by repository validators. It must not become a reader prerequisite.
- `scripts` is reserved for documentation-author infrastructure. Scripts here
  must not become reader prerequisites unless a guide explicitly teaches them.
- `.github/workflows/pages.yml` builds and deploys the book through GitHub
  Pages.

## Source evidence

The initial evidence was developed in `H:\projects\Ghostline`. That repository
is research input, not a runtime or build dependency of this book.
