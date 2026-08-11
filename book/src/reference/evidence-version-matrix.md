# Lab status and research provenance

An evidence label belongs to one claim, one artifact set, and one tested
boundary. It does not automatically transfer to a similar graph or to a later
archive.

This page is the optional provenance lookup for the first five labs and the
older runtime observations cited by some advanced chapters. You do not need it
to follow the authoring guides. The repository's
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

## Current lab matrix

All five completed checkpoints are mod-owned. Their resources have been
deserialized, checked, and round-tripped with WolvenKit `8.19.0`. The lines
below show whether each lab's full in-game test campaign has been completed:

**Lab 1 runtime evidence:** **Experimental** — pending.

**Lab 2 runtime evidence:** **Experimental** — pending.

**Lab 3 runtime evidence:** **Experimental** — pending.

**Lab 4 runtime evidence:** **Experimental** — pending.

**Lab 5 runtime evidence:** **Experimental** — pending.

| Lab | Structural status | Canonical runtime status | Save-backed hold points | Acceptance guide |
| --- | --- | --- | --- | --- |
| `cqa001` — First Signal | **Structurally validated** | See Lab 1 status above | Completion fact, journal activation/success, graph state | [Install, test, and reset](../start-here/install-and-test.md#run-the-save-matrix) |
| `cqa002` — Signal Race | **Structurally validated** | See Lab 2 status above | Variant facts, race/monitor state, journal state, completion | [Test Signal Race](../gates/lab-02-test.md) |
| `cqa003` — Boundary Check | **Structurally validated** | See Lab 3 status above | Trigger state, journal/mappin state, streaming return, completion | [Test Boundary Check](../world/lab-03-test.md) |
| `cqa004` — Handoff Point | **Structurally validated** | See Lab 4 status above | Active child, parent confirmation, stream return, completion | [Test Handoff Point](../questphases/lab-04-test.md) |
| `cqa005` — First Contact | **Structurally validated** | See Lab 5 status above | Community/actor, scene, named outcome, delayed cleanup, completion | [Test First Contact](../scenes/lab-05-test.md) |

Pending and failed campaigns remain **Experimental**. A passing campaign
applies only to the routes it actually exercises; for example, Lab 5 does not
cover active-line interruption, `CutDestination`, arbitrary pre-scene states,
or facial and workspot-animation quality.

## Retained legacy runtime evidence

Ghostline was the research source for the bounded results below. It is not a
reader dependency and its authoring system is not part of these procedures.
The source commit identifies the retained record or resource lineage; the
archive SHA-256 identifies the runtime payload.

| Claim | Label and exact provenance | Recorded environment boundary |
| --- | --- | --- |
| One root-owned quest prefab remained usable across four external children whose own `phasePrefabs` arrays were empty | **Runtime-proven** for GQT003 at source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f`; archive SHA-256 `B082D157978347A126DAACB0A5404AF298B88E549731609D81D5A569CBA81FDF` | WolvenKit `8.17.4`, WKit JSON `0.0.9`, CR2W `GameVersion: 2310`; no complete record binding this book's game/RED4ext set |
| The same GQT003 extraction harness advanced through its access-point release, three ordered escort gates, follower-retaining handoff, three-attacker 20-second defend success, surviving-attacker cleanup, and follower-role clear after success | **Runtime-proven** only for archive SHA-256 `B082D157978347A126DAACB0A5404AF298B88E549731609D81D5A569CBA81FDF` at source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f` | Same incomplete legacy environment record; defend failure/retry, generic movement recovery, carry, trunk placement, and other device combinations are not proved |
| The preceding sequential-route candidate advanced through all three escort gates, then cleared the follower role too early and allowed the persistent target to walk back toward her original AI spot | **Runtime-proven** for that bounded partial result in archive SHA-256 `3EB9FCB4DBD1CA8BA6730C02CDF81B8A89B855C75372FFF8927DC66F0423D597` at source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f` | Incomplete legacy environment record; the later corrected handoff, combat wave, and any generic follower-clear policy are not proved by this hash |
| Ordinary guard awareness could fail one optional stealth objective; after the player selected the named laptop interaction, the quest waited for `IsPersonalLinkConnected`, showed its timed presentation, sent `QuestForceDisconnectPersonalLink`, consumed the exact keylogger, cleaned up guards, and completed | **Runtime-proven** only for GQT002 archive SHA-256 `C3F7608385CDA9E4436AF92E5DA23B866D47504BE889058E0527457470BE71AD` at source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f` | Incomplete legacy environment record; no general controller/action, workspot, encounter, or monitor-cancellation law follows |
| A Files-only laptop exposed its authored Files tab, and opening the named document advanced the quest through its document-read fact | **Runtime-proven** for that partial GQT001 result in archive SHA-256 `791ED71FB1B443734153304DB609961D193BF7ECEE300CD09818BEEE10D5C166` at source commit `6e959d2149e664432eaff3b7d4905e8b1d342f2f` | Incomplete legacy environment record; other computer content types and quest-complete presentation are not proved |
| A consumed readable item advanced one shard stage through its acquisition fact and three-second presentation delay; the next security trigger then waited silently with its volume below the rooftop route | **Runtime-proven** for those bounded partial GQ002 results in archive SHA-256 `82C221619EBA15D39D5F82D53B9CCE86AEEB9107AEC15166718143043284B312` at source commit `5f0e0d5558c35b0fe58b9dd732d4039c91e9c2eb` | Incomplete legacy environment record; reader visitation, generic shard/trigger semantics, and the later corrected trigger route are not proved |
| A fresh-identity theft vehicle existed during the contact drive but disappeared exactly when the intermediate contact-vehicle cleanup handed off while both custom player-vehicle records had live instances | **Runtime-proven** for that bounded partial GQT004 result in archive SHA-256 `707CA5603E84D802B11400CF98761624A1B9156E56BF6752B695C30AA29B5D19` at source commit `a24c341c1e2eca43f05a100f5776baba377b2260` | Incomplete legacy environment record; no universal causal law for the operation or safe reuse with another record follows |
| The later stage-50-bypass candidate reached the intermediate fact-only cleanup child, failed to hand off, and lost the theft vehicle as that child was entered | **Runtime-proven** for that bounded failed GQT004 result in archive SHA-256 `0BB4540D0EF1C74BFBAF3BEA3F84CF290A72CF62B10D4C1DA473602F57E815A8` at source commit `a24c341c1e2eca43f05a100f5776baba377b2260` | Incomplete legacy environment record; the precise cause, generic fact-only child behavior, and the later passing route are not proved |
| The final GQT004 candidate completed its exact six-stage route: named contact-vehicle mount, Patch passenger assignment, contact destination, designated-vehicle theft, delivery-trigger arrival, and final player-vehicle cleanup | **Runtime-proven** only for archive SHA-256 `84BA33E902360BC4F1ED32A0865CE8B15C35D9442FD519CC6C3E85A06D1AE77B` at source commit `a24c341c1e2eca43f05a100f5776baba377b2260` | Incomplete legacy environment record; stopped delivery, generic community/world-vehicle cleanup, removed intermediate cleanup, reload/interruption, chase, and race are not proved |
| Entering the corrected rooftop trigger activated the security encounter and downstream route | **Runtime-proven** for that partial GQ002 result in archive SHA-256 `8FF1835A73F93B032FC4E1602FA1CC80234779706B085C385EBB7DFB91CE945B` at source commit `5f0e0d5558c35b0fe58b9dd732d4039c91e9c2eb` | Incomplete legacy environment record; later GPS/return presentation and generic trigger or encounter behavior are not proved |
| The pre-correction meeting candidate reproducibly crashed when launching its scene | **Runtime-proven** only for the bounded failed result in archive SHA-256 `177500B67B2A6B975A597DF5D582797F006643BA6BC975E1D9CFBC66BC498BFD` at source commit `68f311c8f2511aeba679b76a68062ef5e446aaa0` | Legacy diagnostic environment; it does not prove that every multi-row lipsync table crashes or that the corrected candidate has good facial-animation quality |
| A community-acquired meeting scene completed after both actors used addressable lipsync slot `0` | **Runtime-proven** for the diagnostic candidate at source commit `68f311c8f2511aeba679b76a68062ef5e446aaa0`; archive SHA-256 `87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D` | Legacy scene/community environment; diagnostic slot sharing does not prove facial quality or a general slot policy |
| Three configured generic Tyger Claws spawned and remained passive | **Runtime-proven** for the recorded GQ000 candidate at source record commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; archive SHA-256 `2C5179349DBD1AFF5A5A01123F83FF1DC76D8D91E45FE946CEA4DCAF0166BF80` | Legacy environment; the result is bound to its entry/spot joins, placement, and route; its retained result does not explicitly confirm cleanup |
| Surviving community actors deactivated after the leave-area cleanup boundary | **Runtime-proven** for the later hostile-patrol candidate recorded at source commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; archive SHA-256 `DE2A28EF7F7D8D20B4FADF3B97BD0B96BB420FED8456AC0D57E9987B00ACFB2A` | Different legacy candidate and actor behavior; do not combine its cleanup result with the earlier passive-candidate claim |
| The complete GQ000 route displayed its intended onscreen strings, five scene-choice labels, spoken subtitles/VO, phone choices, native drop-point deposit, package removal, both recorded Morrow response routes, reward, quest success, and completion presentation | **Runtime-proven** for the recorded complete route at source record commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`; archive SHA-256 `1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC` | Legacy environment; no single acceptance record binds its game executable and RED4ext version to the pinned book baseline, and later GPS/marker corrections are not part of this result |

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
| Stage 9 character, AI, scene, device, and cleanup comparisons | **Observed in vanilla** | Exact installed `2.31a` depot paths in the [vanilla index](vanilla-depot-paths.md); every guide limits the observation to its stated fields and ownership question |
| Mod-owned braindance `.questphase`/`.scene`/`.scenerid` chain | **Structurally validated** | Research commit `832e1f1a18cb4d6c63b083ec3699a9fddb91a184`; exact binaries `23552A40E862915FE1C450DD96D423BA4400F7AED5FC4F766B0F61092720E53D`, `0F92C6B8E74DEEB657600FFCC3874D8A61C4A6F564F03DA8DD5D7CA466637D0F`, and `B08879CCE964E00CDDB4B2384B013FAE587CBC8496B7D6F8BE35B11CB0FD9257` serialized to JSON and back with WolvenKit `8.19.0` on 2026-08-09; all eight custom runtime cases remain **Experimental** |
| Lab 1–5 CR2Ws, exact graphs, manifests, and packaged checkpoints | **Structurally validated** | Current repository manifests and validators at the pinned WolvenKit `8.19.0` baseline; runtime follows each lab's separate record |

Vanilla resources are citations only. Readers extract them from their own
installed archives; this repository does not redistribute their cooked files
or complete serialized exports.
