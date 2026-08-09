# Journal, localization, and audio

Journal UI, spoken dialogue, and embedded scene choices use different lookup
systems. A fix in one does not repair the others.

## Evidence and version boundary

Use Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31` for current tests.

**Observed in vanilla:** the journal and scene chapters cite extracted vanilla
resources that expose full journal paths, external spoken-line localization,
and embedded scene locStores. Four focused legacy scene extracts sort each
locale block by unsigned numeric `locstringId`; the relative ordering of equal
ID fallback/source pairs is not asserted as universal.

**Structurally validated:** Labs 1–5 freeze journal paths, `fileEntryIndex`,
onscreen secondary keys, scene RUID joins, subtitle-map paths, VO-map WEM paths,
and the exact embedded/empty locStore shape required by each lab.

**Runtime-proven:** bounded legacy research retained at commit
`97b5c5330acfc259bc1e5b814a83b7902cbd70bf` recorded a scene route with all
five intended choice labels, spoken dialogue, subtitles, VO, and scene exit
after numeric locStore ordering was corrected. The complete passing route is
bound to archive
`1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC`.
Earlier archive
`FEAEC7D66E6C3E492ACE2454A0E32FFB7E1DCBA6B8C08B7E44A427745BF21CAC`
was an intermediate sorted candidate, not the artifact that carries the
complete-route claim. The legacy record does not promote current Lab 5
behavior or make that exact duplicate-payload ordering a universal vanilla
rule.

## Identify the lookup path

| Player-facing content | Authoritative key | Runtime owners |
| --- | --- | --- |
| Quest title, objective, mappin, message, shard, onscreen | Textual secondary key | Journal entry plus ArchiveXL-registered onscreen localization |
| Spoken subtitle | Unsigned numeric localization RUID | Scene line plus subtitle map plus subtitle entries |
| Spoken audio | Same unsigned numeric RUID | Scene line plus VO map plus WEM ResourcePath |
| Player choice label | Scene-local numeric locstring ID | Choice option to screenplay option to embedded `locStore` descriptor/payload |

The screenplay item ID is not a localization RUID. The `caption` CName on a
choice is useful authoring/debug text but is not the authoritative rendered
label.

## Journal entry is missing or has the wrong state

Trace one entry from definition to operation:

1. Confirm the journal resource is packed and registered under the journal
   registration class.
2. Copy the exact full `gameJournalPath.realPath` from the quest node.
3. Split the path into components and verify each parent/child ID in the
   journal tree.
4. Verify `fileEntryIndex` identifies the component represented by the
   containing `gameJournalFileEntry`; it is not the objective's child index.
5. Confirm the quest edge enters the correct journal node socket, such as
   `Active`, `Succeeded`, `Failed`, or `Inactive`.
6. Check the starting save for an existing state or visited flag.
7. Confirm the localized key exists only after the state transition itself is
   known to occur.

| Symptom | Likely first boundary |
| --- | --- |
| No entry and no state transition | Registration, path, `fileEntryIndex`, or graph socket |
| Entry exists with blank title | Onscreen localization registration/key |
| Objective activates but pin does not | Mappin journal child/state and world marker lookup |
| Entry is already succeeded on first test | Starting save or an earlier candidate's graph state |
| File/shard exists but read gate never advances | Exact entry path, visited-state condition, and save lineage |

Do not rewrite localization while the journal node itself never executes.

## Journal/UI text is blank

Compare the journal field and onscreen entry character for character:

```text
journal localized field secondary key
  -> registered en-us onscreen resource
       -> localizationPersistenceOnScreenEntry.secondaryKey
       -> femaleVariant / maleVariant text
```

Then inspect:

- correct `localization.onscreens` locale registration;
- exact packed resource path;
- `primaryKey`/`secondaryKey` shape used by the focused lab;
- duplicate secondary keys in the installed candidate set;
- current save state, since an inactive journal entry cannot display its text.

Do not convert a textual onscreen key into a scene RUID. They are separate
domains.

## Subtitle is missing

For one spoken line, make a four-column audit:

| Join | Expected equality |
| --- | --- |
| Scene screenplay line | `locstringId.ruid` equals the authored spoken-line RUID |
| Subtitle map | Registered map points to the exact subtitle-entries ResourcePath |
| Subtitle entry | `stringId` equals the scene RUID |
| Locale | Map is registered for the locale being tested |

Check ArchiveXL logs for the map registration and missing nested path. A
subtitle map can register while its entries resource is absent from the
archive.

## Subtitle works but audio is silent

Keep the proven subtitle join unchanged and audit the VO branch:

1. confirm `localization.vomaps` registration for the tested locale;
2. confirm the VO entry `stringId` equals the scene RUID;
3. confirm female and male ResourcePaths intentionally target existing WEMs;
4. list/extract the archive and hash each WEM;
5. confirm the game follows the expected gender path;
6. compare format/provenance with the chapter's known synthetic or authored
   source, without substituting extracted vanilla audio.

A present WEM is not proof of a valid VO-map join, and a valid VO-map join is
not proof that the WEM encoding is accepted. Change one boundary per
candidate.

## Choice label is blank, stale, or belongs to another option

Trace the complete scene-local chain:

```text
choice node option screenplayOptionId
  -> screenplayStore.options[].itemId
  -> option locstringId
  -> locStore.vdEntries matching locale, ID, and signature
  -> descriptor vpeIndex
  -> locStore.vpEntries[vpeIndex]
```

Then verify:

- every option ID resolves to one screenplay option;
- descriptor locale blocks are contiguous in the evidence-matched order;
- `locstringId` values are sorted numerically as unsigned integers within the
  arrangement being copied, not lexicographically as decimal strings;
- duplicate descriptors preserve their intended relative mapping;
- every `vpeIndex` remains zero-based and points to the matching payload;
- descriptor and payload `variantId` values match without signed truncation.

Legacy evidence showed a scene whose correct captions coexisted with blank and
stale rendered labels. Round-trip serialization preserved the malformed order;
it did not repair it. Treat ordering as authored data.

## Localization isolation matrix

| Test | What a pass proves | What remains unproved |
| --- | --- | --- |
| Journal state changes with placeholder-visible debug inspection | Graph path/state operation | Onscreen localization and player presentation |
| Onscreen title/objective renders | Journal/UI lookup | Scene subtitle, audio, and choices |
| Subtitle renders with audio disabled/unchanged | Scene-to-subtitle path | VO-map/WEM path |
| WEM plays with matching subtitle | Spoken-line external joins | Choice locStore |
| Every choice label maps correctly | Embedded locStore chain | Branch behavior and scene cleanup |

After fixing a lookup, repeat the scene or journal route from a save eligible
for that transition. A save that already visited the message or passed the
scene node cannot prove first presentation.

Previous: [Actors, scenes, and lipsync](actors-scenes-lipsync.md). Next: [Save
state and clean retests](save-state-clean-retests.md).
