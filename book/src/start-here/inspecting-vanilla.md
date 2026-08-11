# Inspect a vanilla questphase

Here you will extract one named game resource into a disposable WolvenKit
project, inspect its ownership and graph shape, and record observations without
shipping CD Projekt RED's file.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Extraction target | Cyberpunk 2077 `2.31a` Windows archives |
| Inspection tool | WolvenKit `8.19.0` |
| Runtime test | Not applicable; read-only research procedure |

> **Vanilla reference:** the depot path and focused behavior below are
> **Observed in vanilla**. A retained research extraction reported game version
> `2310`, was extracted on 2026-07-24, and was serialized for inspection with
> WolvenKit 8.17.4. No extracted binary or complete serialization is included
> in this book. Re-extract it from the pinned `2.31a` installation with
> WolvenKit 8.19.0 before relying on its current structure.

## Why use a separate inspection project

Use a project such as `CQA_Vanilla_Inspection`, not the Lab 1 project. Adding a
vanilla file to a WolvenKit project places the cooked resource beneath that
project's `source\archive`; packing the project would therefore copy the
vanilla resource into a distributable archive.

A separate project creates a simple safety boundary:

- extracted game resources stay local;
- notes can cite their original depot paths;
- tutorial projects contain only mod-owned resources;
- the inspection project is never packaged or committed.

The reference is evidence, not a template. It contains quest-local facts,
NodeRefs, journal paths, scenes, devices, and nested phases that will not become
valid merely because the file was copied.

## Extract the named resource

Create or open the disposable project, then enable the **Asset Browser** from
WolvenKit's **View** menu if it is hidden. Ensure Mod Browsing mode is off so
the search covers the installed base-game archives.

Search for this exact depot path:

```text
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
```

Select the exact result, open its context menu, and choose **Add selected items
to project**. The official
[Asset Browser guide](https://wiki.redmodding.org/wolvenkit/wolvenkit-app/editor/asset-browser)
documents that action and explains that it extracts individual files from
installed archives without uncooking the entire game.

Verify that the project now contains:

```text
source\archive\base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
```

The leading `source\archive` is project structure. The depot path begins at
`base`. Do not rename the extracted file before recording its provenance.

If you only want to browse another reference without retaining it, **Open
without adding to project** is the safer read-only route. It does not satisfy
this extraction checkpoint because no project copy is retained. The upstream
[File Editor documentation](https://wiki.redmodding.org/wolvenkit/wolvenkit-app/editor/file-editor)
describes both workflows.

## Inspect ownership before graph layout

Open the project copy. Start with the resource tree/properties, then use the
quest graph view as an index into exact nodes. Record these facts:

| Question | What this resource shows |
| --- | --- |
| What is the resource root? | `questQuestPhaseResource` |
| What owns executable topology? | Its `questGraphDefinition` and nested phase graphs |
| How can execution enter or leave? | Named input/output node sockets, not the filename |
| Are all dependencies embedded? | No; nodes refer to quest-local facts, journal paths, a computer NodeRef, and a scene |
| Can screen position prove order? | No; socket connections and node semantics prove flow |

Do not take a graph screenshot as your structural record. Write down node ID,
concrete type, decisive properties, input/output socket names, and connected
node/socket pairs. That record survives editor zoom, layout, and theme changes.

The resource is intentionally large. Do not try to understand all of it on the
first pass. The focused computer-document sequence is useful because it shows
ownership crossing from a device/scene flow into a fact-backed quest wait:

| Node | Focused observation |
| --- | --- |
| `175` | Computer manager enables UI interactivity for `#sq021_randy_pc` |
| `176` | Waits for `sq021_randy_pc_webfile_found > 0` |
| `177` | Disables computer UI interactivity |
| `182` | Activates journal page `internet_sites/drugs_are_bad/05_secret_page` |
| `191` | Sets `sq021_thisisfucked_read = 1` from the computer-page output |
| `192` | Waits until `sq021_thisisfucked_read > 0` |
| `193` | Sets the next quest fact after the read signal is observed |

These rows are **Observed in vanilla**, not a universal recipe. The important
boundary is that the authored computer flow emits a dedicated fact and the
questphase waits for it. The journal activation alone is not evidence that an
arbitrary document-read condition exists.

## Record provenance, not the asset

For a research note, retain:

- the exact depot path;
- game and WolvenKit versions;
- extraction date;
- the small node/property excerpt needed for the claim;
- optionally, a local SHA-256 of the extracted file;
- your interpretation and its evidence label.

Do not publish the cooked `.questphase`, a complete CR2W-JSON export, or a ZIP
containing the inspection project. A hash identifies your local reference but
does not grant redistribution permission.

When the game updates, extract again into a fresh disposable project and
compare focused facts. Do not silently carry a previous-build observation
forward.

## Inspection checkpoint

You are ready to continue when you can explain why:

1. the Windows path and depot path are different;
2. adding the file to a project extracts a distributable cooked resource;
3. a vanilla phase's external references do not become mod-owned dependencies;
4. node sockets, not visual placement, establish execution;
5. your notes can support a claim without redistributing the source asset.

Next, read [Graph execution](../foundations/graph-execution.md) and the rest of
[Foundations](../foundations/index.md).
