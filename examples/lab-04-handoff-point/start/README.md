# Start checkpoint

**Lab 4 runtime evidence:** **Experimental** — pending.

Open `CQA_Lab04_HandoffPoint_Start.cpmodproj` in WolvenKit. This checkpoint
contains seven mod-owned resources:

```text
mod\cqa\cqa004\phases\cqa004.questphase
mod\cqa\cqa004\phases\cqa004_boundary.questphase
mod\cqa\cqa004\journal\cqa004.journal
mod\cqa\cqa004\localization\en-us\onscreens\cqa004.json
mod\cqa\cqa004\world\cqa004_handoff.streamingblock
mod\cqa\cqa004\world\cqa004_handoff.streamingsector
mod\cqa\cqa004\world\cqa004_always_loaded.streamingsector
```

The root graph is `Input -> external child -> Terminating Output`. The child is
`Input -> Terminating Output`. The phase node has soft resource path
`mod\cqa\cqa004\phases\cqa004_boundary.questphase`, `phaseGraph: null`, empty
`phaseInstancePrefabs`, `saveLock: 0`, a zero unfreezing NodeRef, and the exact
`In1`, `Out1`, and `CutDestination` socket contract.

Only the root phase is registered by ArchiveXL. The child must remain archived
but unregistered. The root declares `#cqa004_pr_handoff`; the child declares no
phase prefabs. Every `CutDestination` socket remains unwired because cut
behavior is still **Experimental**.

Do not install the start and completed checkpoints together. Use a distinct
save created before either checkpoint was first installed.
