# Start checkpoint

**Lab 5 runtime evidence:** **Experimental** — pending.

Open `CQA_Lab05_FirstContact_Start.cpmodproj` in WolvenKit. The checkpoint
contains eleven mod-owned CR2W resources and the one canonical archived WEM.

The root graph is a three-node `Input -> external child -> Terminating Output`
pass-through. The archived child is a two-node `Input -> Terminating Output`
pass-through. Neither graph invokes the scene. The start scene retains the same
actor, performer-debug, entry `start`, exit `contact_done`, localization,
resource-reference, and interruption shell as the completed scene, but its
screenplay is empty and its exact graph is only `Start 1 -> End 3`.

ArchiveXL registers the root phase, journal, onscreen table, subtitle map,
voiceover map, and streaming block. It deliberately does not register the
child phase, scene, subtitle entries, WEM, or either sector.

The WEM is present so the checkpoint inventories remain symmetric; the inert
start graph cannot request it. Do not install this checkpoint together with
the completed checkpoint. Frozen runtime acceptance starts from two untouched
manual originals that have never loaded any CQA Lab 1–5 candidate, then Case 1
creates three named manual seeds under the completed candidate, beginning with
`seed-pre-scene-outside-setup`. Loading this start checkpoint makes a save
ineligible as either original or as a source for that five-capture lineage.

## Resource inventory

```text
mod\cqa\cqa005\phases\cqa005.questphase
mod\cqa\cqa005\phases\cqa005_contact.questphase
mod\cqa\cqa005\scenes\cqa005_first_contact.scene
mod\cqa\cqa005\journal\cqa005.journal
mod\cqa\cqa005\localization\en-us\onscreens\cqa005_onscreens.json
mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles.json
mod\cqa\cqa005\localization\en-us\subtitles\cqa005_subtitles_map.json
mod\cqa\cqa005\localization\en-us\vo\cqa005_vo.json
mod\cqa\cqa005\world\cqa005_first_contact.streamingblock
mod\cqa\cqa005\world\cqa005_first_contact.streamingsector
mod\cqa\cqa005\world\cqa005_always_loaded.streamingsector
mod\cqa\cqa005\localization\en-us\vo\contact_i_85c3283507e7ef2f.wem
```
