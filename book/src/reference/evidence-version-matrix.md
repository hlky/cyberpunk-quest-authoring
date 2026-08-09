# Evidence and version matrix

An evidence label belongs to one claim, one artifact set, and one tested
boundary. It does not automatically transfer to a similar graph or to a later
archive.

This page is the release-wide lookup for the first five labs and the legacy
research claims already used by the book. The canonical machine-readable
status of each lab remains its supplied `runtime-acceptance.json`.
The repository's
[legacy runtime ledger](https://github.com/hlky/cyberpunk-quest-authoring/blob/main/evidence/legacy-runtime.json)
separately freezes each historical archive hash, source commit, bounded
observation, exclusion, and exact reader-page inventory.

## Evidence labels

| Label | What it supports | What it does not support |
| --- | --- | --- |
| **Runtime-proven** | The stated behavior was observed in game for a retained, bounded candidate | A different payload, untested branch, different save lineage, or universal engine law |
| **Structurally validated** | Types, handles, paths, joins, graphs, round trips, manifests, or packages passed the stated checks | Successful mounting, graph execution, presentation, cleanup, or reload behavior |
| **Observed in vanilla** | The focused shape occurs in a named resource extracted from the user's game | Permission to redistribute it, a standalone template, or a guarantee that the same shape works in a mod |
| **Experimental** | The claim is pending, failed, out of matrix, or not sufficiently version/hash/save bound | A negative claim that the engine can never support the behavior |

Use the narrowest applicable statement. For example, a legacy archive can be
**Runtime-proven** for its tested community cleanup while the new Lab 5
community remains **Experimental** and its CR2W joins remain **Structurally
validated**.

## Pinned first-release baseline

| Component | Exact version | Applies to |
| --- | --- | --- |
| Cyberpunk 2077 for Windows | `2.31a` GOG build; public patch `2.31` | Practical runtime target |
| WolvenKit | `8.19.0` | CR2W inspection, conversion, round trips, packing, deployment |
| ArchiveXL | `1.27.0` | Quest, journal, localization, and streaming-root registration |
| RED4ext | `1.30.0` | ArchiveXL runtime |
| redscript | `0.5.31` | ArchiveXL dependency; Labs 1–5 add no `.reds` source |
| mdBook | `0.5.4` | Publication build only |

Version review date: **2026-08-09**. This is an exact supported combination,
not a minimum-version claim. See [Tested versions](tested-versions.md) for
release links and compatibility context.

## Current lab matrix

All five completed checkpoints are mod-owned and retain hashes in
`example.json`. Their resources have been deserialized, checked, and
round-tripped with WolvenKit `8.19.0` as specified by their validators.

These dedicated lines are checked directly against the five manifests by the
release validator:

**Lab 1 runtime evidence:** **Experimental** — pending.

**Lab 2 runtime evidence:** **Experimental** — pending.

**Lab 3 runtime evidence:** **Experimental** — pending.

**Lab 4 runtime evidence:** **Experimental** — pending.

**Lab 5 runtime evidence:** **Experimental** — pending.

| Lab | Structural status | Canonical runtime status | Save-backed hold points | Acceptance guide |
| --- | --- | --- | --- | --- |
| `cqa001` — First Signal | **Structurally validated** | Synchronized Lab 1 marker above | Completion fact, journal activation/success, graph state | [Install, test, and reset](../start-here/install-and-test.md#run-the-save-matrix) |
| `cqa002` — Signal Race | **Structurally validated** | Synchronized Lab 2 marker above | Variant facts, race/monitor state, journal state, completion | [Test Signal Race](../gates/lab-02-test.md) |
| `cqa003` — Boundary Check | **Structurally validated** | Synchronized Lab 3 marker above | Trigger state, journal/mappin state, streaming return, completion | [Test Boundary Check](../world/lab-03-test.md) |
| `cqa004` — Handoff Point | **Structurally validated** | Synchronized Lab 4 marker above | Active child, parent confirmation, stream return, completion | [Test Handoff Point](../questphases/lab-04-test.md) |
| `cqa005` — First Contact | **Structurally validated** | Synchronized Lab 5 marker above | Community/actor, scene, named outcome, delayed cleanup, completion | [Test First Contact](../scenes/lab-05-test.md) |

Pending and failed records map to **Experimental**. A passed record may promote
only the cases explicitly frozen in that record. Lab 5 Cases 3, 4, and 7 load
distinct full-slot copies of the named `seed-pre-scene-outside-setup` capture;
those exact loads follow its synchronized marker. Lab 5 active-line
interruption, `CutDestination`, arbitrary or unlisted pre-scene states, and
facial/workspot-animation quality remain **Experimental** even if its ordinary
eleven-case campaign passes.

Do not edit this table alone to promote a lab. Complete the canonical
acceptance record with exact installed hashes, versions, distinct execution
evidence, and save provenance; then update every synchronized status marker
through the repository's validation workflow.

## Retained legacy runtime evidence

Ghostline was the research source for the bounded results below. It is not a
reader dependency and its authoring system is not part of these procedures.
The source commit identifies the retained record or resource lineage; the
archive SHA-256 identifies the runtime payload.

| Claim | Label and exact provenance | Recorded environment boundary |
| --- | --- | --- |
| One root-owned quest prefab remained usable across four external children whose own `phasePrefabs` arrays were empty | **Runtime-proven** for GQT003 at source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f`; archive SHA-256 `B082D157978347A126DAACB0A5404AF298B88E549731609D81D5A569CBA81FDF` | WolvenKit `8.17.4`, WKit JSON `0.0.9`, CR2W `GameVersion: 2310`; no complete record binding this book's game/RED4ext set |
| A community-acquired meeting scene completed after both actors used addressable lipsync slot `0` | **Runtime-proven** for the diagnostic candidate at source commit `68f311c8f2511aeba679b76a68062ef5e446aaa0`; archive SHA-256 `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` | Legacy scene/community environment; diagnostic slot sharing does not prove facial quality or a general slot policy |
| Three configured generic Tyger Claws spawned and remained passive | **Runtime-proven** for the recorded GQ000 candidate at source record commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; archive SHA-256 `2C5179349DBD1AFF5A5A01123F83FF1DC76D8D91E45FE946CEA4DCAF0166BF80` | Legacy environment; the result is bound to its entry/spot joins, placement, and route; its retained result does not explicitly confirm cleanup |
| Surviving community actors deactivated after the leave-area cleanup boundary | **Runtime-proven** for the later hostile-patrol candidate recorded at source commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; archive SHA-256 `DE2A28EF7F7D8D20B4FADF3B97BD0B96BB420FED8456AC0D57E9987B00ACFB2A` | Different legacy candidate and actor behavior; do not combine its cleanup result with the earlier passive-candidate claim |
| The complete GQ000 route displayed its intended onscreen strings, five scene-choice labels, spoken subtitles/VO, phone choices, and completion presentation | **Runtime-proven** for the recorded complete route at source record commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; archive SHA-256 `1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC` | Legacy environment; no single acceptance record binds its game executable and RED4ext version to the pinned book baseline |

The surrounding legacy metadata names WolvenKit
`8.17.4-nightly.2026-03-20`, ArchiveXL `1.27.0`, and TweakXL `1.11.3`, but not
as one uniform acceptance record, and it does not bind the game executable or
RED4ext version. These results support their exact claims; they do not promote
`cqa004`, `cqa005`, or another newly assembled package.

## Retained structural and vanilla evidence

| Evidence set | Label | Provenance and limit |
| --- | --- | --- |
| Legacy community registry, compiled area, AI spot, activation, readiness, acquisition, and scene fields | **Structurally validated** | Research commit `68f311c8f2511aeba679b76a68062ef5e446aaa0`; serialized with the legacy WolvenKit lineage, not the pinned Lab 5 resources |
| Focused quest-building-block corpus | **Observed in vanilla** | Research corpus commit `29066f7b76ad4b7435b3fa2a7c0b20ecea464b5e`; extracted on 2026-07-23/24 without one retained record binding the precise game executable |
| `mq003`, `mq007`, and `mq010` scene shapes | **Observed in vanilla** | Named depot paths in the [vanilla index](vanilla-depot-paths.md); observations are field- and question-specific |
| Lab 1–5 CR2Ws, exact graphs, manifests, and packaged checkpoints | **Structurally validated** | Current repository manifests and validators at the pinned WolvenKit `8.19.0` baseline; runtime follows each lab's separate record |

Vanilla resources are citations only. Readers extract them from their own
installed archives; this repository does not redistribute their cooked files
or complete serialized exports.

## Promotion checklist

A runtime promotion requires all of the following for the exact claim:

1. Record the game and framework versions, game distribution/build, test date,
   and relevant authoring-tool version.
2. Hash the installed archive and every loose configuration payload that can
   affect the route.
3. Identify the original untouched save and every derived manual save or full
   slot copy used by the matrix.
4. Close the game before installing, removing, or cloning candidates.
5. Freeze unrelated mods and prove that no competing lab checkpoint or older
   candidate is enabled.
6. Retain startup/registration logs and route-specific game evidence for each
   required execution.
7. Exercise reload, revisit, clean-save replay, and removal isolation where
   the claim depends on them.
8. Mark out-of-matrix branches **Experimental** instead of inheriting the
   ordinary-route result.
9. Re-run structural, package, documentation, and synchronization validators.

Changing a resource identity, graph topology, registration root, save-backed
state boundary, or installed hash creates a new candidate. A later candidate
may cite an earlier observation as research, but it cannot silently inherit
the earlier **Runtime-proven** label.
