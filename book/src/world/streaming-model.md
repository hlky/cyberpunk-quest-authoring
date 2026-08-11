# Streaming model

World integration starts with a registration path, not with a loose sector
file. A mod-owned node becomes discoverable only when a registered streaming
block has a descriptor that points to its sector and gives the engine enough
context to stream it.

## Vanilla references

These focused base-game resources are useful comparisons. Extract them from
your own installation; they are references, not files to copy into the project.

```text
base\worlds\03_night_city\_compiled\default\03_night_city.streamingworld
base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock
base\worlds\03_night_city\_compiled\default\quest_606b61008df2ba6f.streamingsector
base\worlds\03_night_city\_compiled\default\always_loaded_0.streamingsector
```

## The ownership chain

```text
worldStreamingWorld
└─ blockRefs[]
   └─ worldStreamingBlock
      └─ descriptors[]
         └─ worldStreamingSectorDescriptor
            ├─ data -> *.streamingsector
            ├─ streamingBox
            ├─ category
            ├─ level
            └─ questPrefabNodeRef
```

The base `worldStreamingWorld` is useful research evidence, but a mod should
not replace it merely to add a sector. ArchiveXL can register a separate,
mod-owned block:

```yaml
streaming:
  blocks:
    - mod\cqa\cqa003\world\cqa003_boundary.streamingblock
```

That is Lab 3's structurally checked registration path. The runtime protocol
must still bind the installed `.archive.xl` hash and confirm that ArchiveXL
logged its registration.

## `worldStreamingWorld`

The world root's `blockRefs` identifies compiled streaming blocks. The same
resource also has references for global world systems, including device,
mappin, point-of-interest mappin, area, loot, and location resources. Those
references show that world registration is broader than quest placement;
they do not mean a quest author should edit every global resource.

For a focused quest addition, inspect the world root to understand the native
shape, then add the mod block through ArchiveXL. Replacing the vanilla root
would couple a small quest to a large, shared resource and create needless
conflict and redistribution risk.

## Blocks and descriptors

`worldStreamingBlock` contains a block `index` and a `descriptors` array. Each
`worldStreamingSectorDescriptor` supplies the streaming metadata for one
sector.

| Descriptor property | Role | Evidence boundary |
| --- | --- | --- |
| `data` | Async resource reference to the sector depot path | **Observed in vanilla** |
| `streamingBox` | World-space box used by the streaming system | Shape **Observed in vanilla**; exact load/unload behavior must be runtime-tested |
| `questPrefabNodeRef` | Full quest-prefab root associated with a Quest descriptor | **Observed in vanilla** and part of the structurally validated prior fixture |
| `numNodeRanges` and `variants` | Cooked streaming metadata | **Observed in vanilla**; do not invent semantics from field names |
| `blockIndex` | Descriptor's block association | **Observed in vanilla** |
| `level` and `category` | Streaming classification values | Values are observable; universal policy is not established |

The `worldStreamingSectorCategory` values present in the retained type
information are `Exterior = 0`, `Interior = 1`, `Quest = 2`, `Navigation = 3`,
`AlwaysLoaded = 4`, and `Unknown = -1`. This enum explains serialized values;
it does not prove when every category loads or unloads.

In the structurally validated prior fixture, the Quest sector root used
category `Quest` and level `255`, while its block descriptor used category
`Quest` and level `0`. The AlwaysLoaded sector and descriptor used category
`AlwaysLoaded` and level `1`. Preserve known-good values when studying that
shape, but do not elevate this small sample into a universal invariant.

The vanilla mq003 comparison likewise has a Quest sector root at level `255`
and its Quest block descriptor at level `0`; this is **Observed in vanilla**.
The retained vanilla `always_loaded_0.streamingsector` root is category
`AlwaysLoaded` at level `255`. These examples reinforce that sector-root and
descriptor values occupy different records, while also showing that level is
not a single constant for every AlwaysLoaded arrangement.

## Quest and AlwaysLoaded responsibilities

Lab 3 separates responsibilities:

| Sector | Content | Why it is separated |
| --- | --- | --- |
| Quest | Reach and leave trigger nodes | The descriptor can bind the quest-prefab root used by quest logic. |
| AlwaysLoaded | Checkpoint marker node | Its registration is kept in a separate sector category from the bounded trigger sector. |

**Experimental runtime boundary:** the checked structure is not a promise that
any node in an AlwaysLoaded sector is perpetually active under every runtime
condition. Nor is AlwaysLoaded a reason to put all quest content into one
sector. Category, block bounds, node bounds, distance fields, and game state
can have distinct roles that must be isolated in game.

The focused vanilla Quest sector at
`quest_606b61008df2ba6f.streamingsector` is useful because its retained
extract contains AI spots, trigger areas, splines, and a vehicle-forbidden
area under a quest-prefab namespace.

A separate derived world-asset index catalogs 23 `worldStaticMarkerNode`
records across `always_loaded_0`, `always_loaded_1`, and
`always_loaded_2.streamingsector`. One representative record is node index
`1550` in `always_loaded_0.streamingsector`, with debug name
`q104_02a_sm_breaking_antena_carmocap`. That index was built from 760
serialized sectors and 10,055 selected assets; it is not an exhaustive node
census or a substitute for inspecting the cited depot resource. This is
**Observed in vanilla** support for the category pattern, not proof that Lab
3's marker will load or display correctly.

## Bounds are part of the experiment

A descriptor `streamingBox` and a sector node's placement bounds are separate
records. A box should enclose the content it is intended to stream, with
deliberate padding for approach and test movement. Making a box finite is more
diagnostic than using an unexplained enormous volume: the author can test
outside, approach, inside, reload, and departure states.

Do not infer exact activation distance from `streamingBox` alone. Node data
also contains values such as `MaxStreamingDistance`, while retained WolvenKit
schemas expose fields named `UkFloat1` and `Uk10` through `Uk14`. Those `Uk*`
names are opaque serialization labels. Preserve known-good values and change
one variable at a time; do not rename them conceptually as proven range or
culling controls.

## Validation sequence

1. Open the block and every referenced sector in the pinned WolvenKit version.
2. Confirm exact depot paths, descriptor categories, levels, bounds, and
   quest-prefab roots.
3. Save, convert or pack as required, then round-trip the CR2W and re-inspect
   the same properties.
4. Confirm the intended files are present in the packed archive.
5. Confirm ArchiveXL registered the mod-owned block in its log.
6. Test approach, entry, active-state save/reload, ordinary stream-away and
   return, departure, and completed-save reload from a clean starting save.

Steps 1–4 can support **Structurally validated**. Step 5 proves registration,
not player-facing behavior. Only the controlled in-game cases can support a
bounded **Runtime-proven** claim. See [Lifecycle, cleanup, and
evidence](../foundations/lifecycle-and-evidence.md).

## Common failures

| Symptom | Likely boundary |
| --- | --- |
| No mod-owned sector appears | ArchiveXL config not installed, block path misspelled, or registration failed |
| One sector fails while another works | Its descriptor `data` path, category, level, or serialized sector is wrong |
| The sector appears only at surprising distances | Descriptor box, node bounds, and streaming-related node fields need isolated testing |
| A trigger exists but a quest reference does not resolve | Streaming succeeded; inspect the separate quest-prefab and NodeRef chain |
| WolvenKit opens the file but the game ignores it | Editor acceptance did not prove packing, registration, external references, or runtime compatibility |
| A resource edit appears ineffective on an old save | Quest facts, journal state, or a previously reached checkpoint may already select another lifecycle route |

An archive change cannot erase save-backed facts or journal state. Use a save
created before any version of the lab was installed for the acceptance matrix,
and also test a mid-flow reload as its own case. Resetting one quest fact is
not a substitute for diagnosing an unregistered block or bad sector path.
