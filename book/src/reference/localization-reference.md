# Localization reference

Choose the localization route from the content owner. Cyberpunk 2077 does not
resolve journal text, spoken lines, and scene choices through one shared
table, even when all three values are called a string or locstring in an
editor.

| Record | Value |
| --- | --- |
| Reference review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Lab 1–5 localization resources | **Structurally validated** |
| Exact Lab 1–5 runtime presentation | Governed by each lab's canonical marker: pending/failed is **Experimental**; passed promotes only its recorded cases to **Runtime-proven** |

The complete model and property tables are in [Localization
paths](../journal/localization-paths.md). This page is the lookup and failure
reference.

## Pick the owning path

| Content on screen | Source identity | Runtime owner | ArchiveXL registration |
| --- | --- | --- | --- |
| Quest title, phase, objective, description, journal mappin, phone UI, file, shard, or onscreen text | Textual `LocalizationString.value` | `localizationPersistenceOnScreenEntries` | `localization.onscreens.<locale>` |
| Spoken scene subtitle and VO | Unsigned numeric `scnlocLocstringId.ruid` | Subtitle map -> subtitle entries, plus VO map -> WEM | `localization.subtitles.<locale>` and `localization.vomaps.<locale>` |
| Scene choice label | Unsigned numeric `scnlocLocstringId.ruid` reached through a screenplay option | Scene-embedded `scnlocLocStoreEmbedded` | None; it is inside the `.scene` |

ArchiveXL locale keys use a spelling such as `en-us`. Embedded scene locStore
descriptors use identifiers such as `en_us`, `pl_pl`, and `db_db`. Preserve
the schema's spelling; do not normalize one into the other.

## Journal and onscreen UI

The exact join is textual:

```text
journal LocalizationString.value
  -> onscreen entry secondaryKey
       -> femaleVariant / maleVariant
```

| Onscreen entry property | Contract used by Labs 1–5 |
| --- | --- |
| Root data type | `localizationPersistenceOnScreenEntries` |
| Entry type | `localizationPersistenceOnScreenEntry` |
| `primaryKey` | `0` in the mod-added textual-key shape |
| `secondaryKey` | Globally unique text equal to `LocalizationString.value` |
| `femaleVariant` | Authored text in the supplied labs |
| `maleVariant` | Optional override; empty in the supplied labs |

Register the cooked `JsonResource` beneath `source\archive`, not its
`.json.json` conversion source beneath `source\raw`:

```yaml
localization:
  onscreens:
    en-us:
    - mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json
```

`LocalizationString.unk1`, a scene line RUID, and a localization
`primaryKey` are not replacements for the textual `secondaryKey` join.

## Spoken scene lines

One unsigned line RUID must survive four joins:

```text
scene screenplayStore.lines[].locstringId.ruid
  +-> subtitle map -> subtitle-entry resource -> entry.stringId
  +-> VO map -> locVoLineEntry.stringId -> femaleResPath / maleResPath -> WEM
```

| Resource or item | Decisive field |
| --- | --- |
| `scnscreenplayDialogLine` | `locstringId.ruid` |
| `localizationPersistenceSubtitleMapEntry` | `subtitleFile` soft resource reference |
| `localizationPersistenceSubtitleEntry` | Matching `stringId`, `femaleVariant`, `maleVariant` |
| `locVoLineEntry` | Matching `stringId`, `femaleResPath`, `maleResPath` |
| WEM | Cooked depot resource reached by the VO-map path |

The screenplay line's separate `itemId.id` is local to that screenplay store
and is not the localization ID. Keep the full unsigned 64-bit RUID in the scene, subtitle
entries, and VO map.

ArchiveXL registers the subtitle *map*, not the subtitle-entry resource it
references. It registers the VO map, not each WEM:

```yaml
localization:
  subtitles:
    en-us:
    - mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json
  vomaps:
    en-us:
    - mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json
```

First Contact uses this exact identity and path set:

| Item | Value |
| --- | --- |
| Authored line key | `cqa005_contact_line_0001` |
| Unsigned line RUID | `9638591835734011695` |
| Subtitle map | `mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json` |
| Subtitle entries | `mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles.json` |
| VO map | `mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json` |
| WEM | `mod\cqa\cqa005\localization\en-us\vo\contact_i_85c3283507e7ef2f.wem` |

The supplied scene, maps, subtitle entry, and WEM contract are
**Structurally validated**. Audible playback and subtitle presentation on the
exact tested `cqa005` route follow its synchronized marker. Male-versus-female
path selection remains **Experimental** even if that campaign passes, because
both fields point to the same WEM and the matrix does not exercise distinct
gender-path cases.

## Scene choice labels

A choice is an entirely scene-local lookup:

```text
scnChoiceNodeOption.screenplayOptionId.id
  -> screenplayStore.options[].itemId.id
  -> screenplayStore.options[].locstringId.ruid
  -> locStore.vdEntries[] descriptor
  -> descriptor.vpeIndex
  -> locStore.vpEntries[] payload.content
```

| Field | Rule |
| --- | --- |
| Choice `caption` | Authoring/debug `CName`; not authoritative displayed text |
| Descriptor identity | Match locale, locstring RUID, signature, and variant |
| `vpeIndex` | Zero-based index into `vpEntries[]` |
| `variantId.ruid` | Preserve between descriptor and intended payload |
| Numeric ordering | Compare unsigned numeric RUID values, not decimal strings |

**Observed in vanilla:** the four scene resources listed in the [vanilla
depot-path index](vanilla-depot-paths.md#scenes-communities-and-presentation)
group descriptors into locale blocks and sort unsigned locstring IDs within
each inspected block. This supports a known-good authoring shape, not a
universal theorem about every scene or locale set.

There is no ArchiveXL registration for an embedded choice locStore. Adding a
choice RUID to onscreens, subtitles, or vomaps cannot repair its descriptor or
payload join.

## What the legacy runtime evidence proves

Two retained Ghostline candidates bound useful, narrower results:

| Source and artifact | **Runtime-proven** bounded result | Missing version binding |
| --- | --- | --- |
| Research commit `68f311c8f2511aeba679b76a68062ef5e446aaa0`; archive SHA-256 `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` | A community-acquired meeting scene completed; all spoken subtitles and VO in that route resolved while a slot-0 lipsync diagnostic avoided the prior startup crash | Not one acceptance record binding the game executable, RED4ext, and this book's package |
| Research commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; complete-route archive SHA-256 `1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC` | The retained route displayed the intended onscreen quest text, all five meeting choice labels, spoken subtitles/VO, phone choices, and completion presentation | Legacy environment; not proof against the pinned Lab 1–5 payloads |

The historical metadata mentions WolvenKit
`8.17.4-nightly.2026-03-20`, ArchiveXL `1.27.0`, and TweakXL `1.11.3`, but not
as one uniform run record, and it does not bind the game executable or
RED4ext version. Reusing the same resource shape does not transfer either
runtime result to a new archive. See the [evidence and version
matrix](evidence-version-matrix.md).

## Symptom routing

| Symptom | Inspect first |
| --- | --- |
| Journal entry exists but title/objective is blank | `LocalizationString.value` -> onscreen `secondaryKey`; `primaryKey: 0`; `localization.onscreens.<locale>` registration |
| Only one player variant is correct | Both `femaleVariant` and `maleVariant`; test both intended player configurations |
| Spoken subtitle is absent | Scene line RUID -> subtitle `stringId`; subtitle-map registration; map's `subtitleFile` path |
| Subtitle appears but audio is silent | Same RUID in VO map; both WEM resource paths; packed WEM; audio and ArchiveXL logs |
| Choice caption is right but menu text is blank or stale | Option ID -> screenplay option -> locStore descriptor -> `vpeIndex` -> matching variant payload |
| Only one embedded locale is wrong | That locale's descriptor block, numeric ordering, payload indices, and variant identities |
| A rebuilt string behaves like an older candidate | Installed archive/control-file hashes and a save made before the journal or scene became active |

Packing and a clean deserialize prove resource structure, not runtime lookup.
Retain hashes for the archive and loose configuration, inspect registration
logs, and run journal tests from a pre-install save and scene tests from a save
made before scene activation.
