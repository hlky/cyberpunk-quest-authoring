# Registering a root questphase

A mod-owned root questphase becomes reachable from the game's root quest
structure through ArchiveXL registration. An external child becomes reachable
through the parent's native `phaseResource` reference. Those are different
mechanisms.

## Register exactly one composition root

Lab 4 registers only its parent:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa004\phases\cqa004.questphase
    parent: base\quest\cyberpunk2077.quest
```

`path` is the depot path of the mod-owned root. `parent` is the vanilla root
quest resource under which ArchiveXL attaches it. The base-game resource is a
reference only; do not place an extracted copy in the project or archive.

The child does **not** receive a second registration entry:

```text
mod\cqa\cqa004\phases\cqa004_boundary.questphase
```

It must still be packed at that exact depot path. Parent node `13` reaches it
through a soft `phaseResource`. Registering it independently would turn the
child into another root attachment instead of merely satisfying the parent
reference.

## Registration and resolution are different edges

```text
ArchiveXL quest.phases
  -> cqa004.questphase
       questPhaseNodeDefinition.phaseResource (Soft)
         -> cqa004_boundary.questphase in archive
```

| Edge | Owner | What failure looks like |
| --- | --- | --- |
| Root attachment | Loose `.archive.xl` | Root never becomes reachable or ArchiveXL logs registration error |
| Child resolution | Parent `questPhaseNodeDefinition` plus packed archive | Parent reaches the phase node but the depot reference cannot load |

The archive manifest should list both phase resources. The ArchiveXL
`quest.phases` list should contain only `cqa004.questphase`. Lab 4's validator
rejects an independently registered child so the teaching boundary cannot
silently drift.

## Registration is not content ownership

Lab 4 also registers its journal, onscreen localization, and streaming block:

```yaml
journal:
- mod\cqa\cqa004\journal\cqa004.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa004\localization\en-us\onscreens\cqa004.json

streaming:
  blocks:
  - mod\cqa\cqa004\world\cqa004_handoff.streamingblock
```

These operations answer separate questions:

| Registration | Makes available |
| --- | --- |
| `quest.phases` | Executable root questphase |
| `journal` | Journal tree and entries |
| `localization.onscreens` | Resolved player-facing strings |
| `streaming.blocks` | World block whose descriptors reach the two sectors |

ArchiveXL registers the streaming block, not its sector files separately. A
root phase can register successfully and still fail because its child path,
journal path, localization key, sector descriptor, or nested NodeRef is wrong.

## Root does not mean location

Registration has no coordinate, radius, or NodeRef. Lab 4's root gains world
scope through its `phasePrefabs` declaration, but the external child contains
the trigger conditions that use that scope. The world resources own the
actual trigger geometry and marker placement.

This separation is deliberate:

| Root owns | Child owns |
| --- | --- |
| Completion guard and first-run activation | Reach/leave activity |
| Root prefab declaration | Direct trigger and marker references |
| Starting the child | Returning `Out1` |
| Post-handoff confirmation and final completion | Local objective and pin transitions |

## A root needs a re-entry policy

Being attached to the root makes re-entry a design concern. Lab 4 keeps one
persistent fact, `cqa004_completed`:

```text
root input
  -> cqa004_completed == 0?
       False -> terminating output
       True  -> activate quest -> run child -> confirm handoff
             -> set cqa004_completed = 1 -> terminate
```

The write happens after the child has returned and after the parent's 30-second
confirmation step. A save made while the child is active and a save made in
that parent confirmation window exercise different recovery boundaries.

Use an untouched save created before any Lab 4 candidate was installed. A
console reset of the fact does not remove save-backed journal, phase, mappin,
world, or active-node state.

## Verification ladder

Check root composition in this order:

1. Confirm the `.archive.xl` registers only the exact root depot path.
2. Confirm the packed archive contains both root and child at the manifest
   paths.
3. Confirm the parent `phaseResource.DepotPath` exactly matches the child.
4. Confirm the loose `.archive.xl` is installed beside the archive as required
   by ArchiveXL.
5. Inspect ArchiveXL and RED4ext logs for registration and resource errors.
6. Run from a save whose relevant facts and journal state are known.
7. Observe child entry, child `Out1`, and the first parent-only operation after
   the handoff.
8. Retain installed hashes and repeat the reload/streaming matrix.

Packing proves that both payloads exist. A clean ArchiveXL log proves the
framework processed registration. Only the controlled game run proves native
child resolution and the return route.

Previous: [Questphase resource anatomy](anatomy.md). Next: [Inputs and
outputs](inputs-and-outputs.md).
