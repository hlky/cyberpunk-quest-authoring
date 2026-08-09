# Registering a root questphase

A mod-owned questphase becomes reachable from the game's root quest structure
through ArchiveXL registration.

## Registration shape

Lab 1 uses:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa001\phases\cqa001.questphase
    parent: base\quest\cyberpunk2077.quest
```

`path` is the depot path of the mod-owned `.questphase`. `parent` is the
vanilla root quest resource under which ArchiveXL attaches it.

The base-game resource is a reference only. Do not place an extracted copy in
the example or mod archive.

## Registration is not content ownership

Root registration does not merge the other resources used by the quest. Lab 1
also registers its journal and onscreen localization:

```yaml
journal:
- mod\cqa\cqa001\journal\cqa001.journal

localization:
  onscreens:
    en-us:
    - mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json
```

These three operations answer different questions:

| Registration | Makes available |
| --- | --- |
| `quest.phases` | Executable root questphase |
| `journal` | Journal tree and entries |
| `localization.onscreens` | Resolved player-facing strings |

A phase can be registered successfully and still fail later because its
journal path or localization key is absent.

## Root does not mean location

Registration has no geographic coordinate, radius, or NodeRef. Location enters
a quest only when the graph or a referenced resource introduces it—for
example, a trigger condition, distance check, world NodeRef, mappin, scene
marker, or community.

Lab 1 contains none of those. Its first executable decision is the
`cqa001_completed == 0` fact guard, so player position is not an input to its
flow.

This does not yet establish the precise frame or lifecycle moment at which a
newly registered root is first evaluated. That timing remains
**Experimental** for the Lab 1 acceptance run. It does establish structurally
that the phase has no location gate capable of restricting it.

## A root needs a re-entry policy

Being attached to the root makes re-entry a design concern. Lab 1 uses a
persistent one-shot guard:

```text
root input
  -> cqa001_completed == 0?
       False -> terminating output
       True  -> perform quest -> set completion fact -> terminate
```

Without the already-completed route, repeated evaluation could repeat
player-facing work. A different quest may deliberately resume, retry, or
repeat, but it must encode that policy explicitly.

See [Facts, journals, and saves](../foundations/persistent-state.md) before
choosing the guard. A clean save is required to prove the first-run route;
changing the files alone does not clear save-backed facts or journal state.

## Verification ladder

Check root registration in this order:

1. Confirm the `.archive.xl` uses the exact mod depot path.
2. Confirm the packed archive contains the `.questphase` at that path.
3. Confirm the loose `.archive.xl` is installed beside the mod as required by
   ArchiveXL.
4. Inspect the ArchiveXL log for registration errors.
5. Run from a save whose relevant facts and journal state are known.
6. Record which route executed and retain the installed resource hashes.
7. Reload and repeat the cases required by the root's re-entry policy.

Archive packing proves the payload exists. An ArchiveXL log proves the
framework processed the registration. Only the controlled game run proves the
runtime route.
