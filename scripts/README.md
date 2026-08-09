# Documentation scripts

This directory is reserved for small, optional maintenance utilities such as
diagram rendering, link validation, or example-project checks.

Scripts must support the documentation workflow; they must not become a
prerequisite for understanding or authoring native Cyberpunk 2077 quests.

Current utilities:

- `build_lab01_sources.py` deterministically rebuilds the book-owned Lab 1
  CR2W-JSON review artifacts. It is not part of the reader workflow.
- `render_quest_graph.py` renders an exact SVG from WolvenKit CR2W-JSON plus a
  layout-only override and rejects stale source fingerprints.
- `package_examples.py` creates deterministic ZIP downloads for the start and
  completed checkpoints.

Scripts in this directory are licensed under the MIT License.
