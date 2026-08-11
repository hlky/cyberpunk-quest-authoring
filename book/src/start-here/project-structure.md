# Project and resource structure

This chapter creates an empty WolvenKit project and establishes the path model
used throughout the book. It also explains why a valid `.archive` is only one
part of a quest installation.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| WolvenKit | `8.19.0` |
| Runtime baseline | Cyberpunk 2077 `2.31a`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Runtime test date | Not yet recorded |

> **Version note:** the project layout is the WolvenKit 8.19.0 layout
> used by the supplied checkpoints. Lab 1's CR2W resources are **Structurally
> validated**. This page makes no claim that an untested archive executes in
> game.

## Create the Lab 1 project

Open WolvenKit and use either **File > New Project** or **Create New
Project** on the home view. Enter:

| Field | Lab 1 value |
| --- | --- |
| Project name | `CQA Lab 01 One Shot` |
| Creation location | A writable projects directory outside Cyberpunk 2077 |
| Mod name | `CQA_Lab01_OneShot` |
| Author | Your name |
| Version | `0.1.0` |

Choose **Finish**. WolvenKit creates a project directory and a `.cpmodproj`
file; the source subdirectories are created or populated as the project gains
files. The upstream
[WolvenKit project guide](https://wiki.redmodding.org/wolvenkit/wolvenkit-app/usage/wolvenkit-projects)
documents the same fields and explicitly warns against creating a project
inside the game directory.

If you prefer the book's checkpoint, extract the
[Lab 1 start download](../downloads/cqa-lab-01-start.zip) into that projects
directory and open `CQA_Lab01_OneShot_Start.cpmodproj`. Do not open a project
directly inside the ZIP.

## Keep four path domains separate

The word “path” refers to four different things in this workflow:

| Domain | Example | Meaning |
| --- | --- | --- |
| Game filesystem path | `C:\Games\Cyberpunk 2077\archive\pc\mod` | A location Windows can open |
| Project filesystem path | `C:\CyberpunkModding\Projects\CQA_Lab01_OneShot\source\archive` | Authoring files owned by this project |
| WolvenKit cache/depot directory | `C:\CyberpunkModding\WolvenKitDepot` | Extracted/cache data used by WolvenKit |
| REDengine depot path | `mod\cqa\cqa001\phases\cqa001.questphase` | A resource address in the game's virtual depot |

Only the last value belongs in a CR2W `ResourcePath` or an ArchiveXL
registration. Never serialize a drive letter or your personal project
directory as a resource address.

## Understand the source layers

The completed Lab 1 checkpoint has this deliberate shape:

```text
CQA_Lab01_OneShot.cpmodproj
source\
├── archive\
│   └── mod\cqa\cqa001\
│       ├── phases\cqa001.questphase
│       ├── journal\cqa001.journal
│       └── localization\en-us\onscreens\cqa001.json
├── raw\
│   └── mod\cqa\cqa001\...
└── resources\
    └── CQA_Lab01_OneShot.archive.xl
```

`source\archive` contains cooked REDengine resources. The folders beneath it
are their depot paths, so the phase's project path

```text
source\archive\mod\cqa\cqa001\phases\cqa001.questphase
```

becomes this virtual address when packed:

```text
mod\cqa\cqa001\phases\cqa001.questphase
```

`source\resources` contains loose control files that WolvenKit stages beside
the packed archive. Lab 1's `.archive.xl` tells ArchiveXL to attach the
mod-owned questphase below `base\quest\cyberpunk2077.quest` and merge the
mod-owned journal and localization resources.

`source\raw` is a working/review layer. The completed checkpoint includes
WolvenKit CR2W-JSON there so the book can produce exact diffs and diagrams.
Those files are not loaded by the game, and raw JSON editing is not the
beginner authoring path.

WolvenKit generates `packed` as staging output. A normal **Install** rebuilds
that output and copies its game-relative hierarchy. Do not author in `packed`:
the tool may delete and recreate it.

## CR2W is a container, not a quest language

CR2W is the binary resource container used by REDengine. The extension and
root type tell the engine how to interpret a particular container:

| File | Root responsibility |
| --- | --- |
| `.questphase` | Quest graph, nodes, sockets, handles, phase interfaces |
| `.journal` | Journal entry hierarchy and entry state targets |
| localization `.json` CR2W | Cooked localization entries, despite the filename suffix |

The Lab 1 `.questphase` has a `questQuestPhaseResource` root containing a
`questGraphDefinition`. Nodes inside that graph refer to other resources and
identifiers; they do not embed everything the player sees.

A WolvenKit CR2W-JSON export is a text serialization of the same object model.
It is useful for inspection and deterministic tooling, but its `$type`, handle,
and buffer structure is not a separate runtime format. Saving JSON-shaped text
with a `.questphase` extension does not create a cooked resource.

## Archives and framework resources solve different problems

Packing turns `source\archive` into a `.archive` bundle. The archive preserves
the internal depot paths so the engine can resolve the resources.

ArchiveXL's loose file is not part of that CR2W bundle. For Lab 1 it contains:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa001\phases\cqa001.questphase
    parent: base\quest\cyberpunk2077.quest

journal:
- mod\cqa\cqa001\journal\cqa001.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json
```

The `.archive` answers “does the resource exist at this depot path?” The
`.archive.xl` answers “under which game-owned root should this resource be
registered or merged?” Both must reach the installation.

After a normal install of the completed checkpoint, expect these two top-level
payloads:

```text
<Cyberpunk 2077>\archive\pc\mod\CQA_Lab01_OneShot.archive
<Cyberpunk 2077>\archive\pc\mod\CQA_Lab01_OneShot.archive.xl
```

Their presence still proves only staging. The archive path list, framework
log, game behavior, and save-state matrix are separate checks.

## Project checkpoint

Before adding nodes, verify:

1. the `.cpmodproj` is outside the game directory;
2. the mod name is unique and stable;
3. every cooked resource will live below `source\archive` at its intended depot
   path;
4. loose `.archive.xl` configuration will live below `source\resources`;
5. nothing below `source\raw` is being mistaken for runtime input.

Continue with [Inspect a vanilla questphase](inspecting-vanilla.md), then read
[Resources and ownership](../foundations/resource-model.md) before authoring
Lab 1.
