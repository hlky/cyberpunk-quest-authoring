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

Later labs extend the same quest rather than claiming unrelated global names.
For example, Lab 2 uses `cqa002_*` only if it is a separate installed quest; an
incremental checkpoint that still represents Lab 1 keeps `cqa001`.

The prefix is intentionally not `q`, `mq`, `sq`, `sts`, or another
vanilla-looking family. Tutorial resources should be recognizable as mod-owned
when they appear in logs or depot browsers.

These names are stable book conventions, not game requirements. Authors should
choose a distinct prefix for their own released mods to avoid collisions with
the downloadable tutorials.
