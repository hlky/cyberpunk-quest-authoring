# Troubleshooting

A useful quest diagnosis starts by locating the first boundary that failed.
Do not edit a scene because a journal entry is missing, or rebuild a graph
because an old save already contains its earlier state.

Use this section after the focused authoring chapter for the resource in
question. Each guide follows the same route:

```text
symptom
  -> earliest failing boundary
  -> smallest decisive test
  -> one controlled correction
  -> structural verification
  -> clean-save runtime retest
```

## First-release test boundary

The procedures target the book's pinned first-release stack:

| Component | Version |
| --- | --- |
| Cyberpunk 2077 | Windows GOG `2.31a` |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

See [Tested versions](../reference/tested-versions.md) before carrying a result
to another game build, storefront, or tool version. Some pages also cite
retained Ghostline research. Those records are explicitly called **legacy**:
their archive hashes and observed routes are useful **Runtime-proven** evidence
for those arrangements, but their incomplete environment records do not prove
the same behavior on this pinned stack. Ghostline is never required to follow
the procedures.

## Route by symptom

| Symptom | Start here | First question |
| --- | --- | --- |
| A file saves or packs, but content is absent or the game crashes | [Serialization versus runtime](serialization-vs-runtime.md) | Did the cooked binary retain the authored topology and scalar values? |
| The root never starts, or a child/resource reports missing | [Registration and depot paths](registration-and-depot-paths.md) | Is the exact resource both packed and reached by the correct registration/reference edge? |
| An edge disappears, a node points at the wrong object, or conversion fails | [Handles, sockets, and resources](handles-sockets-resources.md) | Is this an internal handle, graph socket, or external resource reference? |
| A trigger, marker, actor, or device is unresolved or location-dependent | [NodeRefs, streaming, and placement](noderefs-streaming-placement.md) | Does every local/full NodeRef join reach a loaded concrete world node? |
| A scene crashes at launch, an actor is missing, or dialogue never starts | [Actors, scenes, and lipsync](actors-scenes-lipsync.md) | Was the actor ready, acquired by the same identity, and assigned an addressable lipsync slot? |
| A quest has no title, a subtitle is missing, audio is silent, or a choice label is stale | [Journal, localization, and audio](journal-localization-audio.md) | Which of the separate journal/UI, spoken-line, or embedded-choice lookup paths failed? |
| Only old saves fail, a completed quest repeats, or a device keeps stale state | [Save state and clean retests](save-state-clean-retests.md) | What state did the save already contain before these bytes were installed? |
| Several changes landed together and causality is unclear | [Controlled isolation and evidence](controlled-isolation-evidence.md) | What one variable differs from the last hash-bound baseline? |

## Find the earliest failing layer

Check layers in order. A later symptom can be the consequence of an earlier
failure.

| Layer | Decisive evidence | If it fails |
| --- | --- | --- |
| Authored resource | Exact node/resource/property inventory | Correct the WolvenKit project before cooking |
| CR2W round trip | Serialized output retains semantic topology and values | Repair the resource; do not continue to packing |
| Archive payload | Archive listing and extracted payload hashes | Correct project paths or stale build output |
| Loose framework files | Installed `.archive.xl` and dependency inventory | Correct staging before opening a save |
| Registration | ArchiveXL/RED4ext/redscript logs | Correct the exact path or registration class |
| Native lookup | Journal path, ResourcePath, NodeRef, actor, or localization join | Test the relevant ownership chain |
| Runtime lifecycle | Player-facing oracle plus logs | Test readiness, ordering, cleanup, and interruption |
| Save restoration | Named starting save and reload observations | Return to a valid seed; do not infer from a contaminated save |

An archive existing in `archive\pc\mod` proves only that a file was copied
there. A clean ArchiveXL log proves only that the framework processed its
configuration. Neither proves the quest graph ran.

## Preserve the failing state before editing

Before changing anything:

1. Close the game and framework processes.
2. Record the installed mod and framework inventory.
3. Hash the `.archive`, `.archive.xl`, and every other candidate-owned loose
   file.
4. Preserve the full relevant logs and hash them before the next launch
   overwrites or appends to them.
5. Record the starting save slot and whether it predates the first candidate.
6. Write the expected player-facing result and the exact observed deviation.
7. Preserve a privacy-reviewed focused excerpt, screenshot, video, or note.

That snapshot turns “it broke” into a reproducible candidate. The final guide
explains how to reduce it without changing several boundaries at once.

## Evidence labels do not transfer automatically

- **Structurally validated** means that serialization, round trips, graph and
  resource checks support the described shape.
- **Observed in vanilla** means that the cited shape exists in extracted
  base-game resources; it is not proof that a mod-owned adaptation runs.
- **Runtime-proven** means that the stated bounded behavior or result was
  observed in game for the exact retained arrangement. The result can be a
  success or a failure; a failed lab campaign remains **Experimental** for the
  intended behavior that did not occur.
- **Experimental** means that the relevant runtime or lifecycle acceptance is
  incomplete.

Fixing a known defect does not promote every surrounding feature. A
one-variable crash isolation can prove the tested lookup while facial quality,
reload safety, or interruption behavior remain **Experimental**.

Next: [Serialization versus runtime](serialization-vs-runtime.md).
