# Completed checkpoint

**Lab 5 runtime evidence:** **Experimental** — pending.

Open `CQA_Lab05_FirstContact.cpmodproj` in WolvenKit. The completed root owns
the `cqa005_completed` one-shot guard, quest lifecycle, external child call,
and final fact write. Its graph has seven nodes and seven edges.

The archived child has fifteen nodes and fourteen edges. It activates the meet
objective and pin, activates community entry `contact` phase `default`, waits
for more than zero members of the entire community, waits inside
`#cqa005_tr_setup`, checkpoints, invokes scene input `start`, continues only
from named output `contact_done`, clears the meet/pin, waits outside
`#cqa005_tr_cleanup`, deactivates the whole community with `None` entry/phase,
and returns through terminating `Out1`.

The completed scene is version 5, PC, `minorQuests`. `Start 1` fans to
`Section 2` at input stamp `0/0` and to scene-local `scnQuestNode 4` at `0/1`.
The quest node wraps a Cinematic `questPuppetAIManagerNodeDefinition` for the
community actor. The section owns one dialog event and reaches terminating
`End 3`; the Puppet AI output remains empty. Entry `start` and exit
`contact_done` bind nodes 1 and 3.

The line `All clear. Keep moving.` uses RUID `9638591835734011695`. The
subtitle entry and both VO-map gender paths use that exact ID; both VO paths
resolve the mod-owned `contact_i_85c3283507e7ef2f.wem`. Ordinary audio
playback, subtitle display, lipsync presence, and the other in-matrix runtime
claims follow the synchronized marker above, including the named pre-scene
seed loads in Cases 3, 4, and 7. Facial-animation quality, active-line
interruption or `CutDestination`, and arbitrary or unlisted pre-scene
active-child states remain **Experimental** outside that campaign.

The Quest sector owns setup/cleanup triggers, the community area, and AI spot.
The AlwaysLoaded sector owns the scene marker, mappin marker, and community
registry. The root alone declares `#cqa005_pr_first_contact`; child
`phasePrefabs` and external node `phaseInstancePrefabs` are empty.

Begin the acceptance campaign from the two documented untouched originals
that have never loaded any CQA Lab 1–5 candidate. Case 1 follows one continuous
ordinary route and creates exactly three manual seeds:
`seed-pre-scene-outside-setup`, `seed-post-contact-inside-cleanup`, and
`seed-completed`. With the game closed, clone complete slot directories into
distinct execution slots. Cases 1/10 share `original-outside-setup`; Case 2
uses `original-near-setup`; Cases 3/4/7 share the pre-scene seed; Cases 5/6/8
share the post-contact seed; and Cases 9/11 share the completed seed. Each
group is byte-identical by `sav.dat` hash. The removal diagnostic loads its
disposable completed-seed clone with the exact candidate pair absent; it does
not reset facts or edit the save.
