# External VO, WEM, and lipsync

Voice playback and lip movement are parallel resource chains. A scene line
selects external subtitle and voice audio with one localization RUID, while
each performer selects a lipsync animation-set slot from the scene root. A
working subtitle does not prove either of the other chains.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Lab 5 external subtitle/VO resource chain | **Structurally validated** |
| Focused vanilla lipsync slots and localized assets | **Observed in vanilla** |
| Exact Lab 5 playback | **Experimental** while its synchronized marker is pending or failed; **Runtime-proven** only when that marker passes |
| Arbitrary WEM encoding and custom lipsync generation | **Experimental** |

> **Clean-save requirement:** an active scene and its checkpoint may retain
> actor, line, and interruption state across archive changes. Restart the game
> after replacing localization or audio resources, then begin acceptance from
> an untouched pre-scene save. Do not diagnose a new WEM from a save captured
> during the old line.

The native integration can be authored and inspected in WolvenKit. Producing
a finished WEM or custom lipsync animation may require a compatible audio or
animation tool, but no project-specific generator is a reader prerequisite.

## Three independent lookup chains

```text
                         one unsigned line RUID
                                    |
              +---------------------+---------------------+
              |                                           |
              v                                           v
ArchiveXL subtitles registration                ArchiveXL VO-map registration
 -> subtitle map                                -> locVoiceoverMap
 -> subtitle-entry resource                     -> locVoLineEntry.stringId
 -> subtitle entry stringId                     -> femaleResPath / maleResPath
 -> displayed text                              -> archived WEM bytes

scene actor/player actor
 -> lipsyncAnimSet.id
 -> scene.resouresReferences.lipsyncAnimSets[id]
 -> addressable .anims resource
 -> facial/lipsync animation data
```

| Question | Correct owner |
| --- | --- |
| Which sentence is displayed? | External subtitle entry selected by the line RUID |
| Which audio file is played? | External `locVoiceoverMap` entry selected by the same RUID |
| Which gender-specific audio path is used? | `femaleResPath` or `maleResPath` on that VO entry |
| Which mouth/gesture animation table is available to an actor? | The actor's scene-local lipsync slot and the root `lipsyncAnimSets` collection |
| When does the line start and how long can it run? | `scnDialogLineEvent` and its owning section |

A WEM is not embedded in `screenplayStore`, and a lipsync `.anims` row is not
the VO file. The WEM path does not determine the actor's slot. The actor's slot
does not repair a missing VO-map entry.

## The external subtitle and WEM route

Lab 5 provides a focused, mod-owned chain:

| Role | Exact depot path |
| --- | --- |
| Subtitle map | `mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json` |
| Subtitle entries | `mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles.json` |
| VO map | `mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json` |
| Synthetic voice asset | `mod\cqa\cqa005\localization\en-us\vo\contact_i_85c3283507e7ef2f.wem` |

Its line, subtitle entry, and `locVoLineEntry` all use unsigned RUID
`9638591835734011695`. The VO entry points both gender fields at the same
synthetic WEM. That is an exact lab choice, not a rule that female and male
paths must be equal.

ArchiveXL registers the subtitle *map* under
`localization.subtitles.en-us` and the VO map under
`localization.vomaps.en-us`. The subtitle map reaches the subtitle-entry
resource; the VO map reaches WEMs through its line entries. The subtitle-entry
resource and each WEM are archive dependencies, not separate ArchiveXL root
registrations in this design.

Use the same unsigned RUID at the semantic join, but keep these other
identifiers independent:

| Typed or path domain | Purpose |
| --- | --- |
| `scnscreenplayItemId` | Joins the timed dialog event to the screenplay line |
| `scnSceneEventId` | Identifies that timed event instance |
| `scnlocLocstringId.ruid` | Joins line, subtitle entry, and VO entry |
| WEM depot path | Locates audio bytes selected by the VO entry |
| `scnLipsyncAnimSetSRRefId.id` | Indexes the scene root's lipsync rows |

Do not derive one domain from another merely because a filename happens to
contain a hexadecimal suffix.

## Lipsync ownership and slot cardinality

The scene root property is spelled `resouresReferences`. Its
`lipsyncAnimSets` array contains `scnLipsyncAnimSetSRRef` rows. Every ordinary
actor and player-actor definition selects one row through
`scnLipsyncAnimSetSRRefId.id`.

For a cooked scene with `N` addressable rows, every selected ID must satisfy:

```text
0 <= actor.lipsyncAnimSet.id < N
```

This is a cardinality check, not a quality check. It proves that the lookup is
in range; it does not prove that the resource matches the actor's rig,
language, gender, line set, or desired facial performance.

### Distinct vanilla rows

**Observed in vanilla**: in
`base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene`, the non-player
actor selects slot `0` and V selects slot `1`. The installed English
localization archive contains distinct assets at:

- `base\localization\en-us\lipsync\base\quest\minor_quests\mq007\scenes\mq007_01_gun_found\skippy.anims`
- `base\localization\en-us\lipsync\base\quest\minor_quests\mq007\scenes\mq007_01_gun_found\v.anims`

That resource proves the two-slot shape for this scene. It does not make those
assets appropriate for another actor or permit redistribution.

### The retained cardinality isolation

One retained legacy candidate asked for slots `0` and `1` after two identical
source paths cooked to one addressable import. Archive SHA-256
`177500B67B2A6B975A597DF5D582797F006643BA6BC975E1D9CFBC66BC498BFD`
reproduced the scene-launch crash. Candidate
`87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D`
reduced the resource table to one row and made both actors select slot `0`;
the full meeting route, subtitles, and VO then completed. Those two exact
results are **Runtime-proven** in their recorded legacy environment.

The comparison isolates an addressability defect. It does **not** prove that
all multi-row tables fail, that duplicate paths always deduplicate, that a
shared slot is production-quality, or that a generic resource provides correct
facial animation for both performers. The intended production correction is
distinct valid resources whose rows remain addressable after cooking, followed
by visual and lifecycle acceptance.

Lab 5 deliberately keeps both actors on slot `0` with the generic resource:

`base\animations\facial\generic\interactive_scene\generic_facial_lipsync_gestures.anims`

That one-row resource and both indices are **Structurally validated**. Exact
facial and gesture quality remains **Experimental**.

## Separate asset validity from lookup validity

Diagnose an audio/lipsync failure in this order:

1. **Line scheduling:** confirm the section reaches the
   `scnDialogLineEvent`, its `screenplayLineId` resolves, and the duration does
   not clip the line.
2. **Subtitle join:** confirm the exact unsigned RUID, subtitle-map
   registration, subtitle-entry path, locale, and matching `stringId`.
3. **VO join:** confirm VO-map registration, exact `locVoLineEntry.stringId`,
   selected gender path, archive presence, path case, and game/audio logs.
4. **WEM bytes:** confirm the authored asset is a complete playable WEM made
   from audio you have the right to distribute. Validate duration and decode
   independently of the scene.
5. **Actor readiness:** confirm the intended actor was acquired and the event's
   performer maps to it.
6. **Lipsync cardinality:** inspect the cooked/round-tripped root collection
   and every selected slot, not only the raw source rows.
7. **Presentation compatibility:** only after startup and lookup are stable,
   evaluate mouth movement, emotion, gesture, rig fit, and interruption.

This ordering distinguishes common boundaries:

| Observation | Most likely branch to inspect first |
| --- | --- |
| Subtitle absent and audio silent | Line event/RUID or both localization registrations |
| Subtitle present, audio silent | VO map, selected WEM path, WEM presence/bytes, audio logs |
| Audio present, mouth motion wrong | Lipsync resource, actor slot, resource compatibility, line-specific animation data |
| Crash at scene launch before text/audio | Actor acquisition and cooked lipsync slot addressability |
| Correct first line, later line silent | Later line RUID, VO entry, WEM path/bytes, event timing |
| Works for one performer configuration only | Gender path, actor identity, slot/resource assignment, or rig compatibility |

## Manual WolvenKit authoring procedure

1. Start with a mod-owned v5 scene whose actor acquisition and one spoken-line
   event already round-trip. Record actor IDs, performer IDs, selected lipsync
   slots, line item ID, event ID, and full unsigned line RUID.
2. Create a subtitle-entry resource containing the matching `stringId`, then a
   subtitle map whose entry soft-references that resource. Keep both files
   under a stable mod depot path.
3. Create a `locVoiceoverMap`. Add one `locVoLineEntry` with the same unsigned
   `stringId` and deliberate `femaleResPath` and `maleResPath` values.
4. Add original or licensed WEM assets at those exact archive paths. If both
   fields select one file, document that choice; if they differ, test both
   selection routes. This guide does not promote one Wwise encoder version or
   codec preset as a universal Cyberpunk contract.
5. Register the subtitle map and VO map under the exact ArchiveXL locale
   branches. Do not register a subtitle-entry file as if it were the map, and
   do not register each WEM as a VO map.
6. In `resouresReferences.lipsyncAnimSets`, add only the lipsync resources the
   scene actually uses. Give each actor an in-range row ID. Do not manufacture
   two logical slots by duplicating one path without inspecting the cooked
   result.
7. Save and reopen every CR2W in WolvenKit `8.19.0`. Convert focused resources
   to JSON and compare the RUID join, map references, gender paths, root array
   length, actor slot IDs, and event-to-line join.
8. Pack the normal project. List the archive and prove every referenced WEM is
   present at the exact path. Extract the cooked scene for a focused comparison
   of addressable lipsync rows.
9. Fully restart the game, load the untouched pre-scene save, and run the
   acceptance matrix. Serialization, registration, and archive presence are
   **Structurally validated** evidence only.

Do not copy vanilla WEM or lipsync resources into your download. Cite their
depot paths and teach readers to inspect their own installation. The synthetic
Lab 5 WEM is mod-owned and may be used only under that example's documented
license and provenance.

## Acceptance and lifecycle matrix

| Case | Required observation |
| --- | --- |
| Normal line from untouched pre-scene save | One subtitle, one audio playback, correct speaker, no launch crash |
| Every distinct line RUID | Correct text and WEM; no stale prior line |
| Every supported gender path | Correct path selection and asset, or documented shared-path behavior |
| Every actor slot | In-range after cooking; intended resource and acceptable facial result |
| Save before scene launch | Reload starts one coherent scene and resolves current assets |
| Save between lines | If permitted, no duplicate/omitted line or stale lipsync state |
| Interrupt and return | Audio, subtitle, actor tier, and lipsync recover without a false named exit |
| Stream away and return | Actor/resources reacquire without duplicate playback |
| Reload after named exit | No repeated VO or retained Cinematic AI/lipsync ownership |
| Missing-WEM negative control in a disposable candidate | Expected log/absence without misattributing the failure to lipsync |

Active-line save/reload, arbitrary encoder settings, generated custom lipsync,
facial quality, interruption, and stream-return behavior remain
**Experimental** until tested for the exact asset set.

## Evidence boundary

**Observed in vanilla**: the scene-local two-slot lipsync table and distinct
installed localized assets are bounded observations from the cited `mq007`
resource. The `mq003` and `mq010` scene paths listed on the [Scenes](index.md)
page provide further focused comparisons.

**Structurally validated:** Lab 5's scene line, subtitle map and entries, VO
map, synthetic WEM paths, one-row lipsync collection, actor slot IDs, and
WolvenKit `8.19.0` round trips are structurally checked.

**Runtime-proven:** the two retained diagnostic archive results prove their
crash and passing one-row meeting observations only. The complete retained
route at archive SHA-256
`1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC`
also displayed its intended spoken subtitles and VO in its recorded legacy
environment; it does not establish the pinned baseline or arbitrary assets.

**Experimental:** new WEM production, a new VO-map chain, distinct custom
lipsync resources, facial quality, active-line interruption/reload, and
cleanup are experimental until their own hash-bound runtime evidence passes.

Previous: [Choices, outcomes, and scene-local
localization](choices-outcomes-and-localization.md). Next: [Animation events
and scene workspots](animation-events-and-workspots.md).
