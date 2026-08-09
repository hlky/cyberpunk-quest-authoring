# Quest prefabs and NodeRefs

In the compact single-phase arrangement used for this section, a quest NodeRef
has four links to audit: the phase's prefab dependency, the block's root
binding, the sector's full child registration, and the sector's authored node
arrangement. Nested phases add a dependency-lifetime question that the
retained evidence does not settle universally.

```text
questphase local NodeRef
  -> questphase.phasePrefabs root declaration
  -> block descriptor full questPrefabNodeRef
  -> sector full NodeRef registration
  -> sector nodeData / concrete-node arrangement
```

This chain explains why copying a plausible `#child` string into a quest graph
is insufficient.

## Evidence and version boundary

**Observed in vanilla:** this page's chain is present in focused extracts from
the following depot paths:

```text
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_phase.questphase
base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_openworld.questphase
base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock
base\worlds\03_night_city\_compiled\default\quest_606b61008df2ba6f.streamingsector
base\worlds\03_night_city\_compiled\default\always_loaded_0.streamingsector
```

The retained evidence is WolvenKit JSON `0.0.9`, serialized by WolvenKit
`8.17.4`, with CR2W `GameVersion: 2310`. Extract the named resources from your
own installation rather than redistributing them. `GameVersion: 2310` is not
a record of a runtime test.

**Structurally validated:** the same local-root/full-child relationship
round-tripped in a prior mod-owned fixture under WolvenKit `8.17.4`. Lab 3's
single root, two trigger children, and marker child were separately cooked and
serialized back with WolvenKit `8.19.0`.

**Runtime classification:** Lab 3's retained matrix governs NodeRef resolution
and activation in the target runtime stack: Cyberpunk 2077 Windows GOG
`2.31a`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`.
Pending or failed evidence is **Experimental**; only an all-pass record is
**Runtime-proven**.

## A quest prefab is a namespace and binding

In this workflow, “quest prefab” names the root beneath which related world
NodeRefs are resolved. It does not imply that a separate `.prefab` CR2W file
must exist. The relevant serialized owners are:

| Link | Owner and property | Example form |
| --- | --- | --- |
| Direct dependency | `questQuestPhaseResource.phasePrefabs[]` → `questQuestPrefabEntry.prefabNodeRef` | `#cqa003_pr_boundary` |
| World binding | `worldStreamingSectorDescriptor.questPrefabNodeRef` | `$/mod/cqa/cqa003/#cqa003_pr_boundary` |
| Placed child identity | sector `nodeData[].QuestPrefabRefHash` | `$/mod/cqa/cqa003/#cqa003_pr_boundary/#cqa003_tr_reach` |
| Registered child identity | sector `nodeRefs[]` | The same full child path |
| Concrete object | sector `nodes[]`, associated with `nodeData[].NodeIndex` in the compact authored shape used by this lab | A trigger or marker node |

All `cqa003` values in this table are the exact **Structurally validated**
serialized values. Their runtime resolution remains **Experimental**.

## Local and full paths are different representations

A local questphase reference is normally written relative to a declared root:

```text
#cqa003_tr_reach
```

The world-side registration includes the depot namespace, root, and child:

```text
$/mod/cqa/cqa003/#cqa003_pr_boundary/#cqa003_tr_reach
```

The root itself appears in local form in `phasePrefabs` and full form on the
block descriptor:

```text
phasePrefabs prefabNodeRef:       #cqa003_pr_boundary
descriptor questPrefabNodeRef:   $/mod/cqa/cqa003/#cqa003_pr_boundary
```

Do not compare these strings as though one were a typo merely because one has
a prefix. Compare each value in its identifier domain. The [identifier
domains](../foundations/identifier-domains.md) chapter distinguishes NodeRefs,
TweakDBIDs, CNames, facts, and depot paths.

## What each link proves

`phasePrefabs` declares a dependency; it does not create or place anything.
The descriptor root associates a Quest sector with a prefab namespace; it
does not prove the child exists. A full path in `nodeRefs` registers an
identity; it does not by itself describe the concrete node. In a compact
mod-owned sector, `nodeData.NodeIndex` associates the placement with its local
`nodes[]` object. Cooked vanilla sectors can contain non-local-looking indices
or placement data without concrete nodes in the same retained view, so that
local lookup is not a universal file invariant.

For Lab 3's compact single-root phase, review one child through every owner:

1. Find the local NodeRef in the quest node or condition payload.
2. Find its root in that questphase's `phasePrefabs`.
3. Find the same root in full form on the intended block descriptor.
4. Find the full child path in the sector's `nodeRefs` and node data.
5. In the authored mod sector, confirm `NodeIndex` associates that placement
   with the intended concrete node; do not infer the relation from row order.
6. Confirm that the block and sector depot paths are actually registered and
   packed.

The retained vanilla block supplies a concrete comparison: a Quest descriptor
points to
`base\worlds\03_night_city\_compiled\default\quest_606b61008df2ba6f.streamingsector`
and carries a full quest-prefab root ending in `#mq003_pr_homeless`. The
focused sector extract then registers full child NodeRefs beneath that root.
This is **Observed in vanilla**; it is evidence for the relationship, not a
template to copy blindly.

## Dependency locations across phases

Two serialized locations are visible in the retained evidence:

- root `questQuestPhaseResource.phasePrefabs`;
- `questPhaseNodeDefinition.phaseInstancePrefabs` on a phase node.

They are distinct properties. Their exact activation and lifetime semantics
cannot be derived from names alone. In the retained 41-resource vanilla
survey, 16 resource roots had non-empty `phasePrefabs`, containing 20 entries
in total. Ten phase-node records across three files had non-empty
`phaseInstancePrefabs`. Every surveyed root `inplacePhases` was empty.

**Observed in vanilla:** `sts_wat_lch_01_phase.questphase` declares
`#sts_wat_lch_01_streetstory` at its root. Its external open-world child has
empty root `phasePrefabs` yet directly uses trigger NodeRefs; the inspected
phase nodes also have empty `phaseInstancePrefabs`. This disproves a universal
claim that every external child always repeats every root it directly uses.
It does not, by itself, prove the engine's complete inheritance or lifetime
rule.

For mod-owned resources, declaring a directly used root again in an external
child is a conservative authoring convention that avoids relying on an
unresolved transitive rule. It must be described as a convention, not a
vanilla invariant. Lab 3 intentionally stays in one root phase, so its first
world test does not depend on that ambiguity. [Prefab
dependencies](../questphases/prefab-dependencies.md) contains the book's
conservative review procedure; apply its ownership rule within this evidence
boundary.

## Names are part of persisted identity

A NodeRef is an asset identity, while facts and journal state are separately
saved lifecycle data. Not every NodeRef is itself proof of persisted runtime
state, but changing a NodeRef can orphan references and, for stateful devices,
can select a different persistent identity. Later device work must record when
a materially changed device needs a fresh NodeRef.

For the trigger-and-marker lab, test with a save made before any version of
the quest was installed. Reload once before crossing the reach boundary, and
reload a separate save after reach has succeeded while the player remains
inside the outer leave area. Those cases exercise restoration before entry and
the active `IsOutside` wait after reach. They do not establish how an active
`IsInside` wait behaves when loaded with the player already inside its area.
All runtime behavior remains **Experimental** until the recorded matrix passes.

## Common failures

| Symptom | Inspect |
| --- | --- |
| Quest logic cannot find a visible object | Local child spelling, phase root declaration, and full world registration |
| `phasePrefabs` is populated but nothing exists in world | Block registration, descriptor path, sector, concrete node, and node data |
| Sector loads but one child is unresolved | Full child in `nodeRefs`, `QuestPrefabRefHash`, and `NodeIndex` |
| Parent resolves a child but an external child phase does not | Both dependency locations, the parent/child activation shape, and the child resource; do not assume either inheritance or mandatory duplication |
| Two similar roots behave differently | Compare every segment, delimiter, case, and the descriptor-to-sector pairing; do not rely on visual similarity |
| Behavior differs only on an old save | Inspect facts, journal state, activation history, and any stateful world identity before changing the strings again |

A textual match is necessary but still not runtime evidence. Record the exact
installed resources, ArchiveXL registration, clean starting save, and the
route exercised before applying **Runtime-proven**. See [Persistent
state](../foundations/persistent-state.md) and [Lifecycle, cleanup, and
evidence](../foundations/lifecycle-and-evidence.md).
