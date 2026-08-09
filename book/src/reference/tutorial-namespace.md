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
`CQA_Lab04_HandoffPoint`; Lab 5 is `cqa005` /
`CQA_Lab05_FirstContact`. Start and completed checkpoints within one lab keep
the same depot root, so they are alternatives and must not be installed
together.

Lab 4 keeps both questphases and every supporting resource under
`mod\cqa\cqa004\`. Its sole persistent fact is `cqa004_completed`. The root
prefab NodeRef is `#cqa004_pr_handoff`; the marker and trigger child refs are
`#cqa004_mp_handoff`, `#cqa004_tr_reach`, and `#cqa004_tr_leave`. These names
belong to the tutorial resource set; they are not vanilla depot paths.

Lab 5 keeps its root, external child, scene, journal, three external spoken-line
localization resources, streaming block, two sectors, and WEM beneath
`mod\cqa\cqa005\`. Its completion fact is `cqa005_completed`, and its root
prefab is `#cqa005_pr_first_contact`. The local child names are:

```text
#cqa005_tr_setup
#cqa005_tr_cleanup
#cqa005_spot_contact
#cqa005_com_contact
#cqa005_sm_contact
#cqa005_mp_contact
```

The spoken-line key `cqa005_contact_line_0001` deterministically identifies
unsigned locstring `9638591835734011695`. That locstring domain is separate
from quest facts, scene nodes, world identities, and localization secondary
keys.

The prefix is intentionally not `q`, `mq`, `sq`, `sts`, or another
vanilla-looking family. Tutorial resources should be recognizable as mod-owned
when they appear in logs or depot browsers.

These names are stable book conventions, not game requirements. Authors should
choose a distinct prefix for their own released mods to avoid collisions with
the downloadable tutorials.
