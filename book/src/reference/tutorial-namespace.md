# Tutorial namespace

The tutorials use the neutral prefix **`cqa`**, short for Cyberpunk Quest
Authoring.

| Domain | Lab 1 value | Rule |
| --- | --- | --- |
| Mod namespace | `cqa` | Shared namespace for tutorial-owned resources |
| Quest ID | `cqa001` | Three-letter prefix plus a three-digit lab number |
| Depot root | `mod\cqa\cqa001\` | Keeps every Lab 1 resource under one mod-owned root |
| Completion fact | `cqa001_completed` | Quest ID first; descriptive suffix second |
| Localization keys | `cqa_cqa001_*` | Namespace and quest remain visible in global lookup tables |
| WolvenKit project | `CQA_Lab01_OneShot` | Human-readable checkpoint name |

Each numbered lab is a separate installed quest and uses its own ID. Lab 2 is
`cqa002` / `CQA_Lab02_SignalRace`; Lab 3 is `cqa003` /
`CQA_Lab03_BoundaryCheck`; Lab 4 is `cqa004` /
`CQA_Lab04_HandoffPoint`. Start and completed checkpoints within one lab keep
the same depot root, so they are alternatives and must not be installed
together.

Lab 4 keeps both questphases and every supporting resource under
`mod\cqa\cqa004\`. Its sole persistent fact is `cqa004_completed`. The root
prefab NodeRef is `#cqa004_pr_handoff`; the marker and trigger child refs are
`#cqa004_mp_handoff`, `#cqa004_tr_reach`, and `#cqa004_tr_leave`. These names
belong to the tutorial resource set; they are not vanilla depot paths.

The prefix is intentionally not `q`, `mq`, `sq`, `sts`, or another
vanilla-looking family. Tutorial resources should be recognizable as mod-owned
when they appear in logs or depot browsers.

These names are stable book conventions, not game requirements. Authors should
choose a distinct prefix for their own released mods to avoid collisions with
the downloadable tutorials.
