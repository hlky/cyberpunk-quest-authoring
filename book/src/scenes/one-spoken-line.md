# Author one spoken line

This procedure turns the First Contact start scene's inert Start-to-End shell
into one community-acquired spoken line with one named exit. It uses native
WolvenKit project resources; no documentation generator, manifest, explorer,
or custom compiler is a reader prerequisite.

## Procedure boundary

| Record | Exact value |
| --- | --- |
| Review date | 2026-08-09 |
| Game | Cyberpunk 2077 Windows GOG `2.31a` |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |
| Structural status | **Structurally validated** |
| In-game verification | Follow the Lab 5 test procedure for playback, handoff, reload, and cleanup |

> **Clean-save requirement:** authoring and structural checks can use any
> disposable project copy, but runtime acceptance establishes two untouched
> manual originals that have never loaded any CQA Lab 1–5 candidate. Case 1
> creates the exact pre-scene, post-contact, and completed manual seeds; later
> cases use closed-game full-slot clones. Labs 3 and 4 share the Lab 5 site.
> Active quest nodes, checkpoints, journal state, facts, community state,
> scene state, triggers, and streamed-world state can survive archive removal
> or replacement. A save made after any tutorial checkpoint or failed probe
> is not an eligible original.

Work in a copy of the Lab 5 start project. Keep the completed checkpoint beside
it as executable reference material, but enter and inspect every supplied node
and property rather than treating it as a magic template.

## 1. Audit the inert start scene

Open
`mod\cqa\cqa005\scenes\cqa005_first_contact.scene` in WolvenKit. Before
adding dialogue, verify this exact shell:

| Area | Start checkpoint contract |
| --- | --- |
| Root | `scnSceneResource`, `version: 5`, `PLATFORM_PC`, `minorQuests` |
| Actors | Contact actor `0` from community entry `contact`; V actor `1` by `findInContext` |
| Debug symbols | Performer `1` for the contact and `257` for V; other debug arrays explicitly empty |
| Lipsync | Both actors reference slot `0`; one generic lipsync row exists |
| Public routes | Entry `start` -> node `1`; exit `contact_done` -> node `3` |
| Graph | Start `1` output `0/0` -> End `3` input `0/0`; `startNodes[1]`; `endNodes[3]` |
| Screenplay | Typed `scnscreenplayStore`; `lines: []`; `options: []` |
| Embedded localization | Typed `scnlocLocStoreEmbedded`; `vdEntries: []`; `vpEntries: []` |

The start root and start child questphase graphs must not invoke this scene.
That invariant makes the start checkpoint safe even though the `.scene` shell
already exists. If it is reachable, a learner could apparently complete the
meeting without authoring the line, invalidating the exercise and its test
provenance.

## 2. Add the screenplay item

Under `screenplayStore.lines`, add one `scnscreenplayDialogLine` with:

| Property | Value |
| --- | --- |
| `itemId` | `scnscreenplayItemId(1)` |
| `speaker` | `scnActorId(0)` |
| `addressee` | `scnActorId(1)` |
| `locstringId.ruid` | unsigned `9638591835734011695` |
| `usage.playerGenderMask.mask` | `3` |
| Male/female lipsync animation name | `None` |

Do not paste `All clear. Keep moving.` into the scene. The RUID owns the join;
the English text lives in the external subtitle-entry resource.

## 3. Replace the direct edge with a timed section

Keep Start ID `1` and End ID `3`. Add Section ID `2`, containing:

- actor `0` behavior `OnlyIfAlive`;
- actor `1` behavior `OnlyIfAlive`;
- one handled `scnDialogLineEvent` at `startTime: 0`;
- `screenplayLineId: scnscreenplayItemId(1)`;
- unsigned event ID `8646165628675208917`;
- event duration `2598` ms;
- `sectionDuration: scnSceneTime(stu = 2998)`;
- normal output stamp `0/0` to End `3` input `0/0`;
- cancel output stamp `1/0` with no destination.

The section is 400 ms longer than the line in this fixture. Preserve that
explicit tail; do not let End become reachable at 2598 ms.

## 4. Add the parallel PuppetAI branch

Add scene node `4` as an `scnQuestNode` wrapping a
`questPuppetAIManagerNodeDefinition`. Give the inner node `CutDestination`,
`In`, and `Out` sockets, map them through the wrapper, target the contact entry,
and set `aiTier: Cinematic`.

Rebuild Start `1` as one output socket stamped `0/0` with two destinations:

```text
destination Section 2: input stamp name 0 / ordinal 0
destination PuppetAI 4: input stamp name 0 / ordinal 1
```

The PuppetAI wrapper retains one output stamped `0/0` with no destination. It
is fire-and-forget. Do not connect it to End and do not add a join. Keep
`startNodes[1]`, `endNodes[3]`, entry `start -> 1`, and exit
`contact_done -> 3` unchanged.

## 5. Verify actor and resource joins

Confirm actor `0` still selects community acquisition from
`#cqa005_com_contact`, entry `contact`, while actor `1` still selects
`findInContext` with `Character.Player_Puppet_Base`. Confirm performer IDs
remain `1` and `257`.

Both actors must reference lipsync slot `0`, and slot `0` must remain backed by:

```text
base\animations\facial\generic\interactive_scene\
generic_facial_lipsync_gestures.anims
```

The native collection property is `resouresReferences`. Do not add a duplicate
row merely because two actors share it, and do not change V to slot `1` while
the array still contains one row.

## 6. Complete the external localization and audio path

Use the same unsigned RUID in all three joins:

```text
scene line: scnlocLocstringId.ruid = 9638591835734011695
  |
  +-> registered subtitle map
  |     -> cqa005_subtitles.json
  |     -> localizationPersistenceSubtitleEntry.stringId
  |     -> "All clear. Keep moving."
  |
  +-> registered VO map
        -> locVoLineEntry.stringId
        -> femaleResPath / maleResPath
        -> contact_i_85c3283507e7ef2f.wem
```

The subtitle branch needs two resources: a
`localizationPersistenceSubtitleMap` registered under
`localization.subtitles.en-us`, and the
`localizationPersistenceSubtitleEntries` resource referenced by that map. The
VO branch needs a `locVoiceoverMap` registered under
`localization.vomaps.en-us`; both gender paths point to the supplied WEM in
this focused fixture.

| Role | Cooked depot path |
| --- | --- |
| Subtitle map | `mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json` |
| Subtitle entries | `mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles.json` |
| VO map | `mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json` |
| Voice asset | `mod\cqa\cqa005\localization\en-us\vo\contact_i_85c3283507e7ef2f.wem` |

The supplied WAV source and derived WEM are synthetic lab assets. They are not
extracted or redistributed game dialogue. Preserve that provenance whenever
repackaging the project. This chapter teaches the native scene-to-subtitle and
scene-to-WEM joins, not audio mastering or Wwise conversion. Exact WEM
production is deferred to Stage 9; byte-identical Wwise output is not part of
the Stage 6 acceptance contract.

For the full field-level localization chain, see [Localization
paths](../journal/localization-paths.md).

## 7. Connect the questphase only in the completed project

In the completed child phase, reach the scene only after community activation,
`CharacterSpawned`, and broad setup. The `questSceneNodeDefinition` must use:

- soft scene path
  `mod\cqa\cqa005\scenes\cqa005_first_contact.scene`;
- `scnWorldMarker` NodeRef `#cqa005_sm_contact`;
- input `start`;
- output `contact_done`;
- unconnected `CutDestination`, `Default INT`, and `Default RET` routes;
- `interruptionOperations: []`;
- `notAllowedToBeFrozen: 0`;
- `reapplyInterruptionOperationsAfterGameLoad: 0`;
- `syncToMusic: 0`.

There is no `end` output. Connect `contact_done` to the quest's success and
post-scene flow. Keep the start root and start child unable to reach the scene.

## 8. Round-trip and inspect

Use WolvenKit `8.19.0` to convert/serialize the edited resource, deserialize it
again, and compare the focused contract:

1. root type, v5/platform/category, typed empty containers, and exact native
   property names;
2. actor acquisition and performer-symbol joins;
3. lipsync reference array length and every slot index;
4. screenplay item `1`, event-to-item join, distinct unsigned event/RUID
   values, and `2598`/`2998` timing;
5. graph IDs, all five output-socket states, all three connected edges, and
   both destination input stamps;
6. `startNodes[1]`, `endNodes[3]`, and the named entry/exit;
7. questphase socket names/types, soft depot path, and marker NodeRef;
8. subtitle map-to-entries path, VO map-to-WEM paths, and exact matching RUIDs.

Then pack the normal WolvenKit project and inspect ArchiveXL and game logs for
missing paths or localization merge errors. A clean round trip and successful
pack are **Structurally validated** evidence only.

## 9. Runtime acceptance

From the pre-install manual save, verify in one recorded run:

1. the community activates and the contact becomes ready before scene launch;
2. normal approach does not crash or race actor acquisition;
3. the contact says `All clear. Keep moving.` once;
4. the subtitle appears and the synthetic WEM plays;
5. the scene reaches `contact_done`, not a nonexistent `end` route;
6. the post-scene objective/pin handoff occurs once;
7. leaving the cleanup area deactivates the contact, after which the child
   returns and the root writes its terminal fact;
8. the named pre-scene seed loads in Cases 3/4/7 and the post-`contact_done`
   and completed save/reload cases behave as recorded in the Lab 5 matrix.

The supplied Lab 5 cases cover the ordinary `cqa005` route. Facial and
animation quality, active-line interruption or `CutDestination`
behavior, arbitrary/unlisted pre-scene active-child states, and
active-line/interruption reload remain **Experimental** independently of that
marker.

## Common mismatches

| Symptom | Likely first mismatch |
| --- | --- |
| Line has no text | RUID differs between scene and subtitle entry, subtitle map is not registered, or the map points to the wrong entries resource |
| Subtitle appears but audio is silent | VO-map registration, VO `stringId`, gender WEM path, missing WEM, or incompatible audio asset |
| Crash near scene launch | Actor not ready or a lipsync index is not addressable after cooking |
| Scene exits immediately | Root/child start graph invoked the shell, or Section is bypassed by a retained Start-to-End edge |
| Scene never completes | Section normal output misses End, End is absent from `endNodes`, or the quest expects `end` instead of `contact_done` |
| Line is clipped | Event duration and section duration do not preserve the measured line plus tail |

Previous: [Entry, exit, and quest
handoff](entry-exit-and-quest-handoff.md). Next: [Cleanup and save
state](cleanup-and-save-state.md).
