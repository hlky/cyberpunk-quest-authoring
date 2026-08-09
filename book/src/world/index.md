# World integration

A quest can name a place, but the streamed world must supply the thing at that
place. The useful mental model is therefore a chain of owners:

```text
ArchiveXL registration
  -> streaming block
  -> sector descriptor
  -> streaming sector
  -> node data + registered NodeRef + concrete node
  -> questphase or journal reference
```

No link substitutes for another. A valid quest graph does not create its
trigger, and a visible world marker does not prove that a questphase declared
the prefab root needed to address it.

**Lab 3 runtime evidence:** **Experimental** — pending.

## Evidence and version boundary

The world chapters deliberately separate retained research evidence from the
book's current acceptance target.

| Label | What it means in this section |
| --- | --- |
| **Observed in vanilla** | The named fields and arrangements occur in focused extracts from cited game depot paths. The retained extracts were serialized by WolvenKit `8.17.4` as WolvenKit JSON `0.0.9` with CR2W `GameVersion: 2310`. That header is a resource-format value, not proof of a particular running executable. |
| **Structurally validated** | The stated `cqa003` block/sector/NodeRef arrangement was cooked and serialized back for decisive semantic inspection with WolvenKit `8.19.0`. Earlier mod-owned research shapes retain their own narrower version boundary. |
| **Experimental** | This label applies to the new `cqa003` block mounting, sector resolution, marker/GPS, trigger, streaming-return, and save behavior while its required matrix is pending or failed. A design inherited from earlier research is not evidence that the new package works in game. |

The pinned practical acceptance environment is Cyberpunk 2077 Windows GOG
`2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and
redscript `0.5.31`. See [Tested versions](../reference/tested-versions.md).
Lab 3 has passed the structural and packaging gates. Its marker above and
hash-bound acceptance record govern whether the exact runtime candidate is
**Experimental** or **Runtime-proven**.

## What owns what

| Owner | Responsibility in this section |
| --- | --- |
| `worldStreamingWorld` | References the world's compiled streaming blocks and global world resources. |
| ArchiveXL configuration | Adds a mod-owned block to the game's streaming registration without replacing the base streaming world. |
| `worldStreamingBlock` | Holds sector descriptors, including sector depot paths, streaming bounds, categories, levels, and quest-prefab roots. |
| `worldStreamingSector` | Holds or references concrete world nodes, their placement records, and registered NodeRefs. |
| `questQuestPhaseResource` | Executes quest logic and carries quest-prefab dependency declarations. |
| Journal resource | Owns journal presentation and map-pin records; it can refer to a world marker but does not place one. |
| Save | Retains facts, journal state, checkpoints, and some world/device state independently of the installed archive. |

This ownership split builds on the [resource
model](../foundations/resource-model.md), [identifier
domains](../foundations/identifier-domains.md), and [persistent
state](../foundations/persistent-state.md).

## Stage 4 reading route

Read the chapters in order:

1. [Streaming model](streaming-model.md) — world, block, descriptor, sector,
   and registration responsibilities.
2. [Quest prefabs and NodeRefs](quest-prefabs-and-noderefs.md) — the
   single-phase dependency and lookup chain from a questphase to a sector node,
   plus the unresolved nested-phase boundary.
3. [Sector nodes and placement](sector-nodes-and-placement.md) — concrete
   nodes, `nodeData`, `nodeRefs`, transforms, and inplace resources.
4. [Triggers and areas](triggers-and-areas.md) — outlines, notifiers,
   state-shaped and edge-shaped conditions.
5. [Markers and navigation](markers-and-navigation.md) — world markers,
   journal pins, navigation endpoints, and route expectations.
6. [Devices and persistence](devices-and-persistence.md) — entity nodes,
   slots, controller state, and fresh NodeRef identity.
7. [Location research](location-research.md) — extracting quest-safe vanilla
   references without redistributing them.
8. [Lab 3: Boundary Check](lab-03.md) — the learner-facing resource and graph
   contract.
9. [Author Boundary Check in WolvenKit](lab-03-authoring.md) — every supplied
   resource and property explained.
10. [Test Boundary Check](lab-03-test.md) — clean-save, reload, streaming, and
    boundary acceptance cases.

## Lab 3 design boundary

**Structurally validated:** Boundary Check uses one quest prefab root, one
Quest sector containing a reach trigger and a leave trigger, and one
AlwaysLoaded sector containing the checkpoint marker. Its candidate site is
near world position `(-1000.02, 1497.2208, 8.3)`. The geometry is a 25-unit
reach area with 16 outline points and height 12, plus a 110-unit leave area with
20 outline points and height 16. The graph uses state-shaped `IsInside` and
`IsOutside` conditions. The acceptance matrix tests ordinary entry, reload
before the reach crossing, and reload after reach while the player is still
inside the outer leave area. It does not claim coverage for loading while an
active reach condition is already inside its area.

These numbers came from prior research. Their serialization is checked;
finite padded block bounds, marker visibility, trigger firing, vertical
coverage, navigation behavior, and reload semantics are runtime acceptance
claims governed by the recorded matrix. The lab intentionally omits devices,
child phases, communities, and scenes so each failure has a small search
surface.

## First-pass failure routing

| Symptom | Inspect first |
| --- | --- |
| Nothing from the mod-owned world content appears | ArchiveXL block registration, exact depot path, and ArchiveXL logs |
| One sector is absent | Its block descriptor `data`, category, level, and streaming box |
| The object exists but quest logic cannot resolve it | `phasePrefabs`, descriptor `questPrefabNodeRef`, full sector NodeRef, and local questphase NodeRef |
| The wrong object or transform is used | `nodeData.NodeIndex`, the corresponding `nodes[]` entry, position, orientation, scale, and bounds |
| A journal pin has UI state but no expected world anchor | Journal mappin data and the marker node/NodeRef are separate owners; inspect both |
| A result changes between new game, reload, and an old save | Treat save-backed facts and journal state as a separate variable before editing more CR2W fields |

Packing, registration, and a clean WolvenKit round trip are intermediate
checks. Runtime acceptance must begin from a save made before any version of
the test quest was installed, then cover normal entry, reload before reaching,
reload between the two boundaries, departure through the outer area,
stream-away/return while reach is active, completion, and completed-save
reload. This matrix does not make a separate post-completion re-entry claim.
Changing an archive cannot reset a fact or journal state already stored in a
save. The full evidence ladder is in [Lifecycle, cleanup, and
evidence](../foundations/lifecycle-and-evidence.md).
