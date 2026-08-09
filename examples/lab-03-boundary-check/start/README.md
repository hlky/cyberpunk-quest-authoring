# Start checkpoint

**Lab 3 runtime evidence:** **Experimental** — pending.

Open `CQA_Lab03_BoundaryCheck_Start.cpmodproj` in WolvenKit. This checkpoint
already contains the six mod-owned resources used throughout the lab:

```text
mod\cqa\cqa003\phases\cqa003.questphase
mod\cqa\cqa003\journal\cqa003.journal
mod\cqa\cqa003\localization\en-us\onscreens\cqa003.json
mod\cqa\cqa003\world\cqa003_boundary.streamingblock
mod\cqa\cqa003\world\cqa003_boundary.streamingsector
mod\cqa\cqa003\world\cqa003_always_loaded.streamingsector
```

The questphase contains only `Input -> Terminating Output`, but its
`phasePrefabs` already declares `#cqa003_pr_boundary`. The Quest sector owns
the nested reach and leave trigger NodeRefs; the separate AlwaysLoaded sector
owns the static marker. The streaming block registers both sector `data`
paths. Its Quest descriptor binds the mod-owned root
`$/mod/cqa/cqa003/#cqa003_pr_boundary`; the Quest sector registers both full
trigger child NodeRefs, while the separate AlwaysLoaded sector registers the
full marker child NodeRef.

Inspect and edit these resources in WolvenKit. The repository generator is
documentation-author infrastructure, not a reader prerequisite.

Do not install the start and completed checkpoints together. Use a distinct
save created before either checkpoint was first installed; quest, journal,
world, and completion state can become save-backed.
