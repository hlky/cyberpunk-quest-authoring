# Cyberpunk 2077 Quest Authoring — Project Handoff

## Purpose

This repository will host a living, first-principles handbook for authoring
Cyberpunk 2077 quests and scenes.

It is deliberately separate from Ghostline. Ghostline is a quest project and a
manifest-driven creation system; this book documents the underlying native game
resources and manual authoring concepts. Ghostline's tools, fixtures, vanilla
research, and runtime investigations are evidence used to decide what the book
needs to explain. They are not reader prerequisites.

The project originated from:

- <https://github.com/CDPR-Modding-Documentation/Cyberpunk-Modding-Docs/issues/80>
- the maintainer suggestion to host an independently deployed book and link it
  from the main Cyberpunk modding documentation;
- the Audioware mdBook model at
  <https://github.com/cyb3rpsych0s1s/audioware/tree/main/book>.

## Decisions already made

1. The repository and publication are named **Cyberpunk 2077 Quest Authoring**.
2. The repository slug is `cyberpunk-quest-authoring`.
3. The book is hosted independently with mdBook and GitHub Pages.
4. The writing assumes no previous WolvenKit use and no existing service
   accounts.
5. The guides teach native quest resources rather than Ghostline tooling.
6. Downloadable WolvenKit projects will accompany hands-on tutorials.
7. WolvenKit graph screenshots will not be used to explain graph structure.
8. Conceptual diagrams, deterministic SVG node graphs, property tables, and
   downloadable projects form the instructional visual system.
9. Simple foundations ship before broad pattern and advanced-system coverage.
10. Experimental subjects such as custom braindance authoring remain visible
    but clearly separated from runtime-proven guides.

## Current repository state

The local repository is initialized at:

`H:\cyberpunk-quest-authoring`

It has:

- a `main` branch;
- a public `origin` at
  `https://github.com/hlky/cyberpunk-quest-authoring.git`;
- an initial publication history pushed to `main`;
- an mdBook configuration;
- GitHub Pages build/deploy automation;
- a confirmed published base URL at
  `https://hlky.github.io/cyberpunk-quest-authoring/`;
- contributor and style guidance;
- chapter landing pages matching the planned information architecture;
- CC BY 4.0 licensing for prose, diagrams, and examples plus MIT licensing for
  scripts;
- the pinned first-release version set;
- a designed and structurally validated Lab 1 reference project;
- a deterministic CR2W-JSON graph renderer and first exact SVG.

## Research evidence available in Ghostline

The evidence repository is currently:

`H:\projects\Ghostline`

Important routing sources:

- `ROADMAP.md`
- `docs/quest-scene-flow.md`
- `docs/scene-authoring-rules.md`
- `docs/crash-investigation.md`
- `docs/testing.md`
- `docs/packaging.md`
- `docs/test-quests.md`
- `docs/vanilla-sq021-computer-flow.md`
- `docs/drop-points.md`
- `docs/world-asset-catalog.md`
- `docs/character-creation-pipeline.md`
- `docs/braindance-authoring.md` — currently untracked in Ghostline
- `tools/quest_spec.md`
- `tools/scene_spec.md`
- `tools/world_spec.md`
- `reference/vanilla_quest_blocks/README.md`

The initial inventory established:

- 28 typed Ghostline quest activity/control patterns;
- exact playable coverage for 24;
- close runtime-equivalent coverage for three more;
- `carry_npc` as the clearest remaining exact runtime gap;
- four isolated building-block test quests;
- full GQ000/GQ001/GQ002 quest flows;
- 41 vanilla questphase CR2W resources with 41 serialized counterparts;
- 416 surveyed vanilla quests and 5,376 objectives represented by 444 local
  journal slices;
- 15 retained vanilla scene binaries and four focused serialized scene
  references;
- vanilla world references covering streaming blocks, sectors, inplace
  packages, devices, communities, markers, and triggers;
- an experimental custom braindance pipeline covering Blender-authored
  animation, `.scenerid`, rewindable scenes, clue layers, and quest linkage.

The local public `modding_docs` snapshot has useful isolated material but lacks
an end-to-end model:

- `creating-custom-scenes.md` remains a stub;
- the `.scene` theory page is explicitly incomplete;
- quest visualization teaches inspection rather than complete authoring;
- the node-definition page explains several logical nodes but not the wider
  condition/lifecycle system;
- existing guides rely heavily on difficult-to-read WolvenKit screenshots.

## Tool inventory and what it revealed

Ghostline's tools fall into five evidence domains.

### Resource inspection and research

- questphase, scene, journal, localization, world, entity, and appearance
  explorers;
- vanilla quest/journal reference builders;
- world asset and drop-point indexes;
- collision-instance inspection.

Documentation consequence: the book needs searchable resource references,
focused examples, ownership maps, and vanilla provenance rather than complete
JSON dumps.

### Authoring and composition

- typed quest composition and reduced vanilla-derived building blocks;
- deterministic scene generation and validation;
- world, community, trigger, marker, and device generation;
- journal and localization generation;
- character manifest and asset-index work.

Documentation consequence: concepts cross resource boundaries. A questphase
chapter cannot pretend that world, journal, localization, device, or character
resources appear automatically.

### Audio and localization

- subtitle, subtitle-map, VO-map, and WEM workflows;
- the separation between journal/UI localization, spoken line localization,
  and embedded choice localization.

Documentation consequence: the three lookup systems require separate diagrams
and verification procedures.

### Build and validation

- CR2W conversion, archive packing/extraction, round-trip checks, handle graph
  validation, payload comparisons, and runtime evidence records.

Documentation consequence: “WolvenKit saved the file” and “the archive packed”
must never be presented as sufficient proof of runtime correctness.

### Experimental braindance work

- relocatable Blender performance authoring;
- body, facial, cyberware, and camera animation channels;
- new RED compressed buffers in `.scenerid`;
- scene RID tables and playback events;
- visual/audio/thermal clues;
- forward seek, rewind, cleanup, interruption, and replay acceptance cases.

Documentation consequence: braindance belongs in the long-term scope, but the
custom pipeline remains experimental until every runtime case is exercised.

## Editorial contract

Every practical guide should provide:

1. a concrete outcome;
2. prerequisites from a clean installation/account state;
3. the first-principles engine model;
4. a simplified behavior diagram;
5. an exact resource/node representation;
6. manual WolvenKit authoring instructions;
7. a downloadable project checkpoint;
8. expected in-game behavior;
9. logs and verification;
10. common failure modes;
11. tested versions and evidence status.

Claims should use these confidence classes:

- **Runtime-proven**
- **Structurally validated**
- **Observed in vanilla**
- **Experimental**

Maintain a distinction between universal engine invariants and shapes observed
in one scene or quest. For example, unsigned scene IDs and lipsync slot
cardinality have strong runtime evidence, while a particular duplicate
`db_db` payload ordering may be an authoring-fixture contract rather than a
universal vanilla rule.

## Visual and diagram contract

WolvenKit graph screenshots are not acceptable as the main explanation of a
graph.

Each substantial graph guide should provide:

1. **Story view** — conceptual player-facing flow.
2. **Engine view** — exact SVG graph with nodes, IDs, sockets, edges, and
   decisive condition summaries.
3. **Resource view** — ownership and lookup relationships across files.

Large nested node properties belong in detail cards or tables beside the graph.

The future diagram renderer is documentation-author infrastructure. It may
consume serialized example resources or a compact diagram manifest and emit
deterministic SVG. Readers will not be required to run it.

Before implementing the renderer, decide whether exact graphs are generated:

- directly from serialized CR2W-JSON;
- from a tutorial-owned normalized graph manifest;
- or from CR2W-JSON with a small checked layout-override file.

The third option is likely the best balance: structural truth comes from the
example resource while layout remains deliberate and readable.

CI should eventually reject figures whose recorded source fingerprint no
longer matches the example project.

## Proposed book architecture

### Start here

- What a Cyberpunk quest consists of
- Zero-assumption setup
- WolvenKit project creation
- Depot paths, CR2W, archives, and framework resources
- Inspecting vanilla questphases and scenes
- Safe testing and save-state awareness

### Foundations

- Resource ownership and lifecycle
- Nodes, sockets, ordinals, handles, and references
- Facts and persistent state
- Parent/child phases
- Completion, cleanup, and re-entry

### Questphases

- Root registration under `base\quest\cyberpunk2077.quest`
- Inputs, outputs, named outcomes, and termination
- Child-phase handoff
- Phase-prefab ownership and inheritance
- Cut/interrupt paths

### Conditions and gates

- `Condition` versus `PauseCondition`
- snapshot decisions versus wait-until gates
- AND/OR/NOT condition trees
- hubs, joins, XOR races, and switches
- fact, journal, time, trigger, distance, inventory, content, character,
  device, vehicle, scene, and phone conditions
- ordered events versus simultaneous prerequisites
- one-shot activation, cooldown, and repeatable flows
- parallel monitors and stop conditions

### Journal, UI, and localization

- quest, phase, objective, description, and mappin entries
- contacts, messages, choices, and replies
- files, emails, shards, and onscreens
- full journal paths and `fileEntryIndex`
- journal/UI keys, spoken line IDs, and embedded scene choice localization
- rewards and completion presentation

### World integration

- streaming blocks, sectors, and inplace packages
- AlwaysLoaded versus Quest sectors
- quest prefabs and NodeRefs
- triggers, markers, navigation endpoints, and device slots
- safe vanilla-location research
- save-backed device identity

### Communities and characters

- compiled community areas, registries, entries, phases, and AI spots
- activation, spawn readiness, acquisition, and cleanup
- gameplay AI tiers, followers, hostility, and combat threats
- `.ent`, `.app`, TweakDB records, and appearance namespaces

### Scenes

- scene anatomy
- actors, performers, props, and debug symbols
- screenplay stores, graph nodes, sections, and events
- one-line scenes
- choices and embedded `locStore`
- scene-local quest nodes
- entry points, named exits, and questphase sockets
- animations, lipsync resources, and slot cardinality
- interruptions, returns, and cleanup
- distinct ID domains

### Gameplay pattern cookbook

- messages and job offers
- holocalls and conversation scenes
- reach/leave area
- meet contact
- device interaction and hacking
- terminal documents
- time gates
- acquire/remove items
- readable shards
- clue investigations
- combat and waves
- optional stealth monitors
- plant item
- rescue/release
- escort, defend, carry, and trunk placement
- workspots and doors
- destruction and rewards
- vehicle mounting, riding, driving, stealing, delivery, cleanup, chase, and
  racing
- two-way choices and general switches
- outcome-dependent debriefs

### Braindance and specialized scenes

- `.scenerid` responsibilities
- RID/scene/quest resource chain
- actor and camera channels
- rewindable sections
- clue layers
- visibility, exits, interruptions, cleanup, and replay
- runtime acceptance matrix

### Troubleshooting

- successful serialization versus runtime validity
- handles and references
- registration and depot paths
- NodeRefs and streaming
- actor readiness
- save-backed facts, journals, scenes, and devices
- localization lookup failures
- locStore ordering
- lipsync crashes
- controlled isolation and clean-save tests

### Reference

- glossary
- file/resource map
- node and condition index
- ID domain reference
- evidence and version matrix
- vanilla depot-path index

## First release plan

Do not begin with a contact scene or full narrative quest. The first complete
release should contain five incremental labs.

Before extending the lab sequence, complete the shared Foundations chapters:
resource ownership, graph execution, identifier domains, persistent state,
root/child phase composition, and lifecycle/evidence. Labs may link back to
those concepts instead of redefining them.

### Lab 1 — One-shot minimal quest

```text
registered root
  -> if tutorial_completed == 0
  -> activate quest and objective
  -> wait 10 real-time seconds
  -> succeed objective
  -> set tutorial_completed = 1
  -> succeed quest
  -> terminate
```

It teaches registration, facts, a root phase, a pause condition, journal state,
localization, completion, packaging, and save persistence without world or NPC
dependencies.

### Lab 2 — Activation gates

Add:

- prerequisite facts;
- immediate branches;
- wait-until conditions;
- AND/OR/NOT composition;
- real-time and game-time delays;
- timeout races;
- one-shot protection.

### Lab 3 — World objective

Add:

- streaming block and sector;
- quest prefab;
- marker and trigger;
- map pin;
- reach and leave phases.

### Lab 4 — Root and child phases

Move the activity into a child phase and teach:

- `In1` and `Out1`;
- parent/child ownership;
- resource paths;
- phase-prefab inheritance;
- completion handoff.

### Lab 5 — First contact and scene

Add:

- community and AI spot;
- community activation and `CharacterSpawned`;
- broad setup trigger;
- one spoken line;
- one named exit;
- persistent fact handoff;
- safe cleanup.

Choices, VO production, combat, complex devices, and AI movement come after
these five labs.

## Condition and gate taxonomy

The documentation should not reduce “start after X, Y, Z” to a single generic
recipe.

Teach these separate control semantics:

- evaluate now and branch;
- wait until one condition becomes true;
- wait for every prerequisite;
- proceed on any prerequisite;
- accept the first success/failure/timeout signal;
- monitor failure while another path runs;
- require an ordered sequence;
- choose an ordered or all-matching switch case;
- prevent re-entry;
- reset or permit repeatable activation.

Condition families found in the vanilla corpus include:

- fact comparison;
- journal entry state and visited state;
- real-time delay, game-time delay, and time period;
- trigger and distance;
- inventory and content availability;
- character spawn, death, mount, state, combat, health, hit, quickhack, and
  workspot state;
- device controller state;
- vehicle speed, mount, trunk, water, and destination state;
- scene and phone state;
- spawning readiness;
- scan and destruction thresholds.

An eventual creation system may represent these as composable control blocks,
but the book must first explain their engine semantics.

## Relationship to Ghostline building blocks

The book should organize patterns by player/game behavior, not by compiler API.
For design and research purposes, it is still useful to separate:

- **activities:** reach, talk, hack, fight, scan, plant, rescue, escort, drive,
  deliver;
- **control flow:** wait, branch, join, race, monitor, switch, delay,
  activate-once.

Strong next research candidates from the vanilla corpus are:

- conversation scene without the full meet-contact lifecycle;
- voiced contact call/holocall;
- generalized wait-for-condition;
- workspot use;
- target destruction;
- standalone reward;
- NPC trunk placement;
- encounter waves;
- vehicle chase/race;
- door control;
- n-way switch.

The exact current coverage gaps should be closed with isolated runtime fixtures
before their corresponding pages are marked runtime-proven.

## Braindance publication boundary

The current untracked Ghostline work is sufficient for research pages covering:

- what `.scenerid` owns;
- actor/body/facial/cyberware/camera channel relationships;
- recorded-perspective camera data;
- rewindable scene playback;
- visual/audio/thermal clue layers;
- quest linkage;
- normal/interrupted cleanup and replay.

It is not sufficient for a guaranteed end-to-end custom braindance tutorial.
The checked candidate still requires concrete authored scene/quest templates,
installation, and all eight runtime cases:

- forward seek;
- backward rewind;
- visual layer;
- audio layer;
- thermal layer;
- normal cleanup;
- interrupted cleanup;
- replay after cleanup.

Publish conceptual and experimental material first. Promote it to a practical
guide only when the tested resource hashes and runtime evidence are retained.

## Example project policy

Examples belong under `examples` and should be released as convenient ZIP
downloads.

Each lab should provide:

- a **start** project;
- a **completed** project;
- mod-owned CR2W resources;
- ArchiveXL/framework files needed by that lab;
- a manifest of expected depot paths;
- tested version metadata;
- an expected graph fingerprint;
- clean-save and reset instructions.

Avoid making raw CR2W-JSON editing the beginner workflow. Serialized extracts
may be included as generated review artifacts for diagrams and diffs if the
mod-owned source and provenance are clear.

No extracted vanilla binaries should be committed. A guide may instruct the
reader to extract a named depot resource for comparison.

## Repository and publication infrastructure

The book currently uses mdBook `0.5.4` in CI.

The GitHub Pages workflow follows the artifact deployment model:

- `actions/checkout@v7`
- `actions/configure-pages@v6`
- `actions/upload-pages-artifact@v5`
- `actions/deploy-pages@v5`

Pull requests build the book without deploying. Pushes to `main` and manual
workflow runs build and deploy.

The workflow intentionally does not force-push a generated `gh-pages` branch.

## Immediate next actions

Completed on 2026-07-27:

1. Applied CC BY 4.0 to prose, diagrams, and example projects and MIT to
   scripts.
2. Confirmed the public repository, pushed `main`, GitHub Actions Pages source,
   published base URL, and edit links.
3. Chose `cqa` as the neutral tutorial namespace and `cqa001` as Lab 1.
4. Pinned Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, and
   RED4ext `1.30.0`.
5. Designed Lab 1's journal tree and root questphase.
6. Selected CR2W-JSON plus layout-only overrides as the exact graph contract.
7. Built the first deterministic SVG from the Lab 1 questphase and enforced a
   source fingerprint.
8. Added start and completed WolvenKit checkpoints and began the Lab 1 chapter.
9. Filled out the shared Foundations and placed them before Lab 1 in the
   reading order.
10. Filled the first Questphases pass: resource anatomy, root registration,
    phase interfaces, external children, prefab dependencies, completion, and
    cut obligations.

Next:

1. Run the completed checkpoint in Cyberpunk 2077 2.31a on a clean save and
   retain logs and hashes for the acceptance record.
2. Fill Conditions and gates, then Journal/UI/localization, before designing
   another lab.
3. Complete the click-by-click WolvenKit authoring instructions, linking each
   step to the relevant Foundation rather than repeating the engine model.
4. Publish both automatically generated Lab 1 checkpoint ZIPs.
5. Promote Lab 1 claims from experimental/structurally validated only where the
   retained runtime evidence supports it.
6. Ask the Cyberpunk Modding Docs maintainers to add the published book to
   their navigation when Lab 1 is usable.

## Resolved decisions

- Prose, diagrams, and example projects use CC BY 4.0; scripts use MIT.
- “The RED Questbook” is the informal subtitle.
- Tutorials use prefix `cqa`; Lab 1 is `cqa001`, titled “First Signal.”
- Exact diagrams use WolvenKit CR2W-JSON plus layout-only overrides and a
  checked structural fingerprint.
- Release ZIPs will be built automatically from the checked example projects.
- The first release supports the exact pinned version set rather than claiming
  compatibility with older WolvenKit or framework versions.
- Translations are deferred until the English Lab 1 structure is stable; they
  should use later sibling books rather than partially translated chapters in
  this repository.
