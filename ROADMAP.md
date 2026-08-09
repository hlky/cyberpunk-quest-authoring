# Completion roadmap

This roadmap records the audited state of *Cyberpunk 2077 Quest Authoring* and
the stages used to finish it. It is a delivery plan, not reader-facing engine
documentation. The audit date is **2026-08-09**.

The canonical editorial scope remains [HANDOFF.md](HANDOFF.md). Ghostline is
research input only: readers must be able to follow every procedure with
WolvenKit, ArchiveXL, the game, and tools explicitly introduced by the book.

## Delivery status

**Lab 1 runtime evidence:** **Experimental** — pending.

**Lab 2 runtime evidence:** **Experimental** — pending.

**Lab 3 runtime evidence:** **Experimental** — pending.

**Lab 4 runtime evidence:** **Experimental** — pending.

**Lab 5 runtime evidence:** **Experimental** — pending.

| Stage | Status on 2026-08-09 |
| --- | --- |
| 0 — audit and validation baseline | Complete; committed and published |
| 1 — zero-assumption start and Lab 1 closeout | Complete; runtime evidence is governed by the dedicated marker and canonical acceptance record |
| 2 — journal, UI, and localization | Complete; seven substantive chapters, a deterministic lookup diagram, and Lab 1 semantic checks |
| 3 — conditions and gates plus Lab 2 | Complete; eight control/reference chapters, a three-page practical lab, two deterministic checkpoints, an exact 21-node graph, and schema-v3 two-variant acceptance |
| 4 — world integration plus Lab 3 | Complete; ten world chapters, two deterministic six-resource checkpoints, three exact/conceptual SVGs, and schema-v3 eight-run acceptance |
| 5 — root/child composition plus Lab 4 | Complete; six focused questphase chapters, a three-page practical lab, two deterministic seven-resource checkpoints, exact parent/child graphs, and an eight-run acceptance matrix |
| 6 — communities, scene basics, and Lab 5 | Complete; twelve focused community/scene chapters, a three-page practical lab, two deterministic twelve-artifact checkpoints, seven diagrams, and an eleven-case acceptance matrix |
| 7 — first-release hardening | Complete; eight symptom-led troubleshooting guides, eleven lookup/reference pages, canonical five-lab navigation, synchronized release status, a validated legacy-evidence ledger, and full-repository lint/build/package checks |
| 8–9 | Planned below |

## Completion standard

A category is complete when:

1. its landing page routes readers through substantive chapters rather than a
   list of promises;
2. native resources, ownership boundaries, identifiers, graph semantics, and
   lifecycle obligations are explained from first principles;
3. practical claims carry one of the book's four evidence labels;
4. practical guides record tested versions, save-state requirements, expected
   behavior, verification, and failure boundaries;
5. every supplied node and resource is explained, and mod-owned examples are
   downloadable without requiring Ghostline;
6. the book, generated figures, manifests, and example packages pass the
   repository validation gate.

Completeness does not turn an untested feature into a proven one. A bounded
research page may be complete while remaining **Experimental**. A practical
guide is promoted to **Runtime-proven** only when its retained acceptance
record supports that label.

## Audited baseline

| Area | State on 2026-08-09 | Principal gap |
| --- | --- | --- |
| Publication and CI | Operational | Validation was Lab-1-specific; checkpoint ZIP bytes differed by host OS |
| Start here | Placeholder plus a partial Lab 1 | Zero-assumption setup, project creation, vanilla inspection, installation, and test workflow |
| Foundations | Substantive first pass | Stronger fixture/depot-path citations and final cross-links |
| Questphases | Substantive first pass | Practical child-phase checkpoint and final evidence pass |
| Lab 1 — First Signal | Structurally validated design and completed checkpoint | Manual WolvenKit procedure and retained clean-save runtime acceptance |
| Conditions and gates | Placeholder | All control semantics, condition families, and Lab 2 |
| Journal, UI, and localization | Placeholder | Journal trees, states, mappins, messages/files, and three localization lookup systems |
| World integration | Complete Stage 4 first pass | Lab 3 runtime class is governed by its retained clean-save acceptance record |
| Communities and characters | Placeholder | Community lifecycle, spawn readiness, AI, entity, appearance, and Lab 5 prerequisites |
| Scenes | Placeholder | Resource anatomy, screenplay graph, IDs, localization, quest handoff, audio, and cleanup |
| Gameplay patterns | Placeholder | Evidence-backed cookbook pages organized by player behavior |
| Braindance | Experimental scope notice | Bounded conceptual/resource pages and the eight-case runtime boundary |
| Troubleshooting | Placeholder | Symptom-led diagnosis, isolation, logs, clean-save tests, and crash boundaries |
| Reference | Three focused notes | Glossary, resource/node/condition indexes, evidence matrix, and vanilla path index |
| Labs 4–5 | Absent | Projects, exact diagrams, tutorials, downloads, and acceptance records |

At audit time, the table of contents had no missing file targets or orphaned
reader-facing Markdown. Its weakness was depth: nine category pages were short
placeholders, and only Lab 1 existed. The delivery-status table above records
progress after that frozen baseline.

## Research inventory

The current Ghostline tree contains a larger evidence base than the original
handoff paths imply. Its relevant maintained routes include:

- `H:\projects\Ghostline\docs\authoring\` for scenes, world resources,
  characters, items, ArchiveXL patching, and experimental braindance work;
- `H:\projects\Ghostline\docs\workflows\` for build, package, automated-test,
  runtime-test, and isolated test-quest records;
- `H:\projects\Ghostline\docs\reference\` for vanilla quest and focused
  system studies;
- `H:\projects\Ghostline\tools\quest_spec.md` and the quest compiler for the
  typed building-block inventory;
- `H:\projects\Ghostline\reference\vanilla_quest_blocks\` for focused vanilla
  CR2W research and provenance.

These locations may contain extracted vanilla binaries. They are evidence for
research, never files to copy into this repository. Book pages cite depot paths
and teach readers to extract their own references.

The building-block compiler currently exposes 30 stage types, superseding the
handoff's older count of 28. That count is a research inventory, not a claim
that 30 reader-facing recipes are already proved. GQ000 provides the strongest
representative evidence for root/child flow, a contact scene, community
readiness, journal/mappins, device interaction, localization, delivery, and
completion. Isolated GQT002–GQT004 fixtures provide strong runtime evidence for
stealth/plant, rescue/escort/defend, and vehicle lifecycle families. Other
patterns range from partial runtime passes to structural or vanilla-only
evidence and must be labelled individually.

The retained Ghostline records bind packages to hashes. Their metadata and
historical notes show `WolvenKit 8.17.4-nightly.2026-03-20`, ArchiveXL
`1.27.0`, and TweakXL `1.11.3`, but not as one uniform acceptance record, and
they do not bind the game executable or RED4ext version. They are therefore
legacy runtime evidence, not automatic proof under this book's pinned
`2.31a`/`8.19.0`/`1.27.0`/`1.30.0`/`0.5.31` practical baseline. Stage 5 migrated
one bounded GQT003 composition claim into this book with its source commit and
candidate archive hash; that claim remains legacy runtime evidence rather than
proof under the pinned practical baseline. The remaining GQT002–GQT004 proof
narratives still survive primarily in Ghostline Git history and must be
migrated into equally explicit, durable evidence records before new
publication claims rely on them.

## Delivery stages

Each stage ends with the same gate: run repository validation, inspect the
diff, commit only that stage, push `main`, wait for its matching Pages workflow
to succeed, and smoke-test affected pages and downloads.

### Stage 0 — audit and validation baseline

- publish this status/category matrix and current Ghostline routes;
- make checkpoint ZIPs byte-for-byte deterministic across supported hosts;
- add one local validation entry point for generated sources, exact figures,
  manifests, CR2W presence, registration paths, and packages;
- run the baseline locally and in GitHub Actions.

### Stage 1 — zero-assumption start and Lab 1 closeout

- install/configure the pinned toolchain from a clean starting state;
- create a WolvenKit project and explain depot paths, archives, and framework
  resource registration;
- inspect a named vanilla questphase without redistributing it;
- complete the click-by-click Lab 1 authoring, install, log, clean-save, and
  reset procedure;
- add a machine-readable acceptance record. Keep runtime claims experimental
  until the clean-save matrix is actually retained.

### Stage 2 — journal, UI, and localization

- document quest/phase/objective/mappin trees and state transitions;
- separate journal/UI keys, spoken-line localization, and embedded scene
  choice localization;
- cover messages, files, emails, shards, onscreens, rewards, and presentation;
- reconcile every Lab 1 journal/localization property with these chapters.

### Stage 3 — conditions and gates plus Lab 2

- teach immediate branches, pause conditions, Boolean trees, joins, races,
  monitors, ordering, switches, delays, one-shot guards, and repeatability;
- index the condition families observed in the retained vanilla corpus;
- ship Lab 2 start/completed checkpoints and exact graphs.

### Stage 4 — world integration plus Lab 3

Status: **Complete** on 2026-08-09. Runtime behavior is governed by the Lab 3
acceptance record and synchronized status marker above.

- teach streaming blocks/sectors, inplace packages, quest prefabs, NodeRefs,
  triggers, markers, mappins, navigation endpoints, and device identity;
- ship Lab 3's reach/leave objective with streamed-state and save-state tests.

### Stage 5 — root/child composition plus Lab 4

Status: **Complete** on 2026-08-09. The exact Lab 4 child lifetime, handoff,
stream-return, and save behavior remain **Experimental** pending its retained
acceptance matrix.

- turn the existing phase-composition theory into a complete external-child
  procedure;
- distinguish the one ArchiveXL-registered root from an archived external
  child resolved by `phaseResource`;
- teach `In1`/`Out1` handoff, root-owned prefab scope, and the evidence boundary
  around `CutDestination` rather than treating compiler inheritance policy as
  native law;
- ship Lab 4 start/completed checkpoints, exact parent/child diagrams, manual
  authoring, and an eight-run acceptance procedure.

### Stage 6 — communities, scene basics, and Lab 5

Status: **Complete** on 2026-08-09. The exact Lab 5 community, scene,
localization/audio, ordinary cleanup, stream-away/return,
post-`contact_done` reload, and completed reload behavior follows the
synchronized marker above, including the named pre-scene seed loads in Cases
3, 4, and 7. Active-line interruption/`CutDestination`, arbitrary/unlisted
pre-scene active-child states, and facial/workspot-animation quality remain
**Experimental** outside its retained eleven-case acceptance matrix.

- teach community registries, entries, phases, AI spots, activation, spawn
  readiness, acquisition, and cleanup;
- teach scene anatomy, actors/performers, one-line screenplay flow, entry
  points, named exits, questphase handoff, and persistent completion;
- ship the first-contact Lab 5 without hiding setup or cleanup in a template.

### Stage 7 — first-release hardening

Status: **Complete** on 2026-08-09. The reference matrix mirrors all five
canonical runtime records; it does not promote pending gameplay claims.

- add symptom-led troubleshooting and clean-save isolation procedures;
- add the glossary, resource map, node/socket/condition indexes, ID-domain
  quick reference, evidence/version matrix, and vanilla depot-path index;
- normalize lab naming and navigation;
- run a complete editorial, link, figure, package, and live-site pass.

### Stage 8 — gameplay cookbook

Publish in independently verifiable batches:

1. communications, journal presentation, and branching;
2. areas, devices, items, files, shards, scans, and workspots;
3. NPC interaction, stealth, combat, rescue, escort, defend, and carry;
4. vehicle mount, ride, drive, theft, delivery, cleanup, chase, and race;
5. rewards, destruction, switches, and outcome-dependent debriefs.

Every recipe names its exact evidence source. Close equivalents and known gaps
remain visible instead of being promoted to exact support.

### Stage 9 — advanced systems and final publication pass

- complete advanced scenes, choices, VO/lipsync, animations, characters,
  appearances, AI, devices, and complex cleanup;
- publish braindance ownership and resource-chain material as
  **Experimental** until all eight acceptance cases are retained;
- perform the final cross-category consistency and release audit.

## Runtime evidence hold points

Codex can complete resources, explanations, structural checks, hashes, and
acceptance procedures in this repository. In-game claims require a compatible
Cyberpunk 2077 installation and a human-verifiable play session. If no retained
run is available, work continues with the correct **Structurally validated**,
**Observed in vanilla**, or **Experimental** label; it does not fabricate a
runtime result.
