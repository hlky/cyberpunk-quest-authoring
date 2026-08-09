# ArchiveXL registration reference

An archive makes a resource available at a depot path. ArchiveXL registration
attaches selected mod-owned roots to game-owned systems. Most files in a quest
are packed dependencies and must *not* receive their own top-level
registration.

| Record | Value |
| --- | --- |
| Reference review date | 2026-08-09 |
| ArchiveXL syntax baseline | `1.27.0` |
| Complete practical baseline | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Lab 1–5 registration files | **Structurally validated** |
| Exact Lab 1–5 game registration | Governed by each lab's canonical marker: pending/failed is **Experimental**; passed promotes only its recorded cases to **Runtime-proven** |

This reference covers only the roots exercised by Labs 1–5. It is not a
catalog of every ArchiveXL feature.

## Registered roots versus packed dependencies

| Concern | Register this | Leave these as packed dependencies |
| --- | --- | --- |
| Quest composition | One intended root questphase under `quest.phases` | External child questphases reached through `phaseResource` |
| Journal | Each contributed `.journal` under `journal` | Journal entries and handles inside that resource |
| Journal/UI text | Cooked onscreen localization resource under `localization.onscreens.<locale>` | Journal resources that carry its textual keys |
| Spoken subtitles | Subtitle *map* under `localization.subtitles.<locale>` | Subtitle-entry resource reached by the map |
| Spoken VO | VO map under `localization.vomaps.<locale>` | WEM files reached by map entries |
| World streaming | One `.streamingblock` under `streaming.blocks` | Sector files reached by block descriptors, plus resources inside those sectors |
| Scene | Nothing in the Lab 5 ArchiveXL file | `.scene` reached through the quest scene node's resource path |

Registration and depot resolution are different edges. A root can register
successfully while its child phase, sector, scene, subtitle entries, or WEM is
missing from the archive.

## Exact Lab 5 shape

Lab 5 exercises every registration family used in the first five labs:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa005\phases\cqa005.questphase
    parent: base\quest\cyberpunk2077.quest

journal:
- mod\cqa\cqa005\journal\cqa005.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa005\localization\en-us\onscreens\cqa005_onscreens.json
  subtitles:
    en-us:
    - mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json
  vomaps:
    en-us:
    - mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json

streaming:
  blocks:
  - mod\cqa\cqa005\world\cqa005_first_contact.streamingblock
```

The YAML values are REDengine depot paths relative to `source\archive`. They
are not Windows paths, project paths, or paths beneath `source\raw`.

## Quest root registration

```yaml
quest:
  phases:
  - path: mod\myquest\phases\myquest.questphase
    parent: base\quest\cyberpunk2077.quest
```

| Key | Meaning |
| --- | --- |
| `path` | Packed depot path of the mod-owned composition root |
| `parent` | Game-owned quest resource below which ArchiveXL attaches it |

`base\quest\cyberpunk2077.quest` is a reference to a vanilla resource. Do not
extract it into the mod or include it in the archive.

For a parent and external child:

```text
ArchiveXL quest.phases
  -> myquest.questphase
       questPhaseNodeDefinition.phaseResource (Soft)
         -> myquest_activity.questphase
```

Register only `myquest.questphase`. Pack the child at the exact
`phaseResource.DepotPath`. Registering the child as another `quest.phases`
entry turns it into an additional root attachment; it does not merely satisfy
the parent's resource reference.

## Journal and onscreen registration

```yaml
journal:
- mod\myquest\journal\myquest.journal

localization:
  onscreens:
    en-us:
    - mod\myquest\localization\en-us\onscreens\myquest.json
```

The journal registration merges entry definitions. The onscreen registration
merges separately owned display text. A valid journal path does not imply that
its `LocalizationString.value` resolves, and a merged localization entry does
not create a journal entry.

Use [Journal path reference](journal-path-reference.md) and [Localization
reference](localization-reference.md) to validate the two joins independently.

## Subtitle and VO registration

```yaml
localization:
  subtitles:
    en-us:
    - mod\myquest\localization\en-us\subtitles\myquest_subtitles_map.json
  vomaps:
    en-us:
    - mod\myquest\localization\en-us\vo\myquest_vo.json
```

The subtitle map owns a resource reference to the subtitle-entry CR2W. The VO
map owns resource paths to WEMs. Therefore all of these must be packed, but
only the two maps appear in the ArchiveXL YAML:

```text
registered subtitle map
  -> packed subtitle entries

registered VO map
  -> packed WEM
```

Do not register the subtitle-entry file in place of the map. Do not add a WEM
path as though it were another VO map.

## Streaming registration

```yaml
streaming:
  blocks:
  - mod\myquest\world\myquest.streamingblock
```

The streaming block's descriptors reach the packed sectors:

```text
registered streaming block
  +-> Quest streaming sector
  +-> AlwaysLoaded streaming sector
```

Register the block once. Do not add its `.streamingsector` files to
`streaming.blocks`. A clean block registration still cannot repair a wrong
sector depot path, descriptor category, bounds, quest-prefab root, NodeRef, or
world identity.

## Filesystem and deployment

The WolvenKit project separates the two delivery channels:

```text
source\archive\...      cooked resources packed into ModName.archive
source\resources\...    loose ModName.archive.xl configuration
```

After a normal install, both top-level payloads are expected beneath the game
directory:

```text
<Cyberpunk 2077>\archive\pc\mod\ModName.archive
<Cyberpunk 2077>\archive\pc\mod\ModName.archive.xl
```

Do not author in WolvenKit's generated `packed` directory. Repacking may
replace it.

## Verification order

1. Close the game and framework processes before replacing either payload.
2. Inventory installed candidates; do not leave a start checkpoint, completed
   checkpoint, or older archive with the same depot paths enabled.
3. Confirm every registered value is an exact cooked depot path and every
   referenced dependency is present in the archive.
4. Confirm `quest.phases` contains only the intended composition root or roots.
5. Confirm subtitle registration names the map, streaming registration names
   the block, and neither indirect leaf is added as a root.
6. Pack and list the archive's depot paths.
7. Install the `.archive` and matching `.archive.xl`; retain hashes for both.
8. Start the game and inspect RED4ext and ArchiveXL logs for load,
   registration, merge, and missing-resource errors.
9. Run from a save created before the relevant quest, journal, scene,
   community, and device state existed.
10. Remove the exact pair with the game closed and repeat the documented
    isolation case where the lab requires one.

A file appearing under `archive\pc\mod` proves deployment only. A clean
ArchiveXL log proves the configuration was processed, not that graph execution
or an indirect resource works.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Root quest never starts | YAML nesting, root depot path, `parent`, installed `.archive.xl`, ArchiveXL log, and starting save |
| Parent starts but child never resolves | Packed child path and parent `phaseResource`; do not add a second root registration as a shortcut |
| Journal transition node runs but no entry appears | Journal registration, typed journal path, and save-backed state |
| Journal entry exists but text is blank | Onscreen registration and localization key join |
| Subtitle is absent | Registered subtitle map, its `subtitleFile` reference, and line RUID |
| Subtitle works but audio is silent | Registered VO map, WEM path and payload, line RUID, and audio logs |
| World content never appears | Registered block, descriptor-to-sector paths, bounds/category, and quest-prefab scope |
| Scene path cannot load | Packed `.scene` and quest node soft resource path; no separate Lab 5 scene registration exists |
| Old behavior survives a rebuild | Duplicate installed candidate, mismatched archive/YAML hashes, or save-backed graph/journal/scene/world state |

The supplied Lab 1–5 YAML and dependency sets are **Structurally validated**
with the pinned tooling. Their exact in-game merges remain **Experimental**
until the corresponding canonical clean-save records pass.
