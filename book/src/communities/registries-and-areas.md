# Registries and compiled areas

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

A compact quest community has two world-side owners with different streaming
jobs:

```text
AlwaysLoaded sector
  worldCommunityRegistryNode
    communitiesData[]
      worldCommunityRegistryItem
        communityId
        entriesInitialState[]
        template -> communityCommunityTemplateData

Quest sector
  worldCompiledCommunityAreaNode_Streamable
    sourceObjectId
    area -> communityArea
      entriesData[] -> phasesData[] -> timePeriodsData[] -> spotNodeIds[]
```

The registry describes what the community can spawn. The compiled area places
the community source in the streamed world and binds its entry/phase periods to
world AI-spot identities. Neither substitutes for the other.

## Evidence boundary

**Structurally validated:** legacy mod-owned resources retained at commit
`68f311c8f2511aeba679b76a68062ef5e446aaa0` contain the focused
registry/area shape described here. Their CR2W exports record WolvenKit
`8.17.4`, WKit JSON `0.0.9`, and `GameVersion: 2310`.

**Runtime-proven:** legacy fixture only. Installed archive
`87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D`
resolved its registry, streamable area, and AI spot strongly enough to spawn
the configured meeting actor and complete the later meeting route. That
candidate deliberately used a unique vanilla character record for isolation;
it is evidence for the exact historical lifecycle, not safe character-selection
guidance.

**Experimental** while the synchronized marker is pending or failed, and
**Runtime-proven** only when it passes: the exact `cqa005` registry node,
compiled area, streaming placement, identities, ordinary scene join, stream-away/return route,
post-`contact_done` reload, and completed reload follow the synchronized marker
above, including the named pre-scene seed loads in Cases 3, 4, and 7.
Arbitrary or unlisted pre-scene active-child states and
active-line/interruption reload remain out-of-matrix **Experimental** claims.

## Registry responsibility

The inspected mod-owned shape places a `worldCommunityRegistryNode` in an
AlwaysLoaded sector. Its decisive properties are:

| Property | Responsibility |
| --- | --- |
| `communitiesData` | Holds one or more `worldCommunityRegistryItem` records. |
| `communityId.entityId.hash` | Selects the matching compiled community source. |
| `entriesInitialState` | Gives each named entry its initial active state and initial phase. |
| `template` | Embeds `communityCommunityTemplateData` for the entries available to this registry item. |
| `workspotsPersistentData` | Retains spot identities and initial enabled/placement data in the inspected compact shape. |

An AlwaysLoaded registry is a useful mod-owned arrangement because the
definition remains reachable before the local quest sector finishes streaming.
It does not make the actor AlwaysLoaded. The compiled area and AI spots still
belong to their streamed sector, and activation still requires quest logic when
`entryActiveOnStart` is false.

Do not elevate the sector category to a universal schema rule. It is the
retained, tested arrangement used by this section and must still be checked in
the exact new package.

## Compiled-area responsibility

The local Quest sector contains a
`worldCompiledCommunityAreaNode_Streamable`. Its `communityArea` mirrors the
spawn topology using world identities rather than character records:

```text
entryName
  -> entryPhaseName
     -> periodName + isSequence
        -> spotNodeIds[]
```

The registry side names `spotNodeRefs`; the compiled-area side names
`spotNodeIds`. Those values must resolve to the same placed AI spots. A
community can therefore be internally well-formed yet still fail because the
area points at a different spot identity than the registry template.

Important compiled-area fields in the retained shape are:

| Property | Responsibility |
| --- | --- |
| `sourceObjectId` | Supplies the community/source identity that joins the area to the registry item. |
| `area.entriesData[].entryName` | Mirrors one registry entry `CName`. |
| `phasesData[].entryPhaseName` | Mirrors one spawn phase `CName`. |
| `timePeriodsData[].periodName` | Mirrors the selected period such as `Day`. |
| `timePeriodsData[].isSequence` | Mirrors whether the period uses its spot set as a sequence. |
| `timePeriodsData[].spotNodeIds` | Names the world-global AI-spot identities used by the period. |
| `streamingDistance` | Participates in when the compiled area is available; it does not guarantee actor readiness at scene start. |

Placement still uses the ordinary streaming-sector chain described in [Sector
nodes and placement](../world/sector-nodes-and-placement.md): one concrete node,
one matching `nodeData` record, a registered NodeRef where the arrangement uses
one, and the block descriptor that mounts the sector beneath the intended
quest-prefab root.

## The three identity joins

Derive each world identity from its own canonical full `NodeRef`; do not mint
numbers from labels or from a neighbouring identity:

```text
community/source ID
  <- RED4 NodeRef hash(full community NodeRef)

registry-node ID
  <- RED4 NodeRef hash(full community NodeRef with `_registry`
                       appended to the final community name)

AI-spot global ID
  <- RED4 NodeRef hash(full AI-spot NodeRef)
```

The hash operation must understand RED4 NodeRef aliases and segments. The `#`
marker is NodeRef hierarchy/alias syntax and is skipped as a marker by that
operation; it is not an ordinary byte to feed into a generic hash. Do not use
plain FNV-1a over a debug label, the last `#name`, or the printed full path as a
substitute. When a numeric value must be audited outside normal WolvenKit
serialization, use RED4-aware NodeRef logic such as WolvenKit's `NodeRef`
implementation and retain the originating full string beside the result.

Reject zero results and reject every collision across the source, registry,
and spot sets before cooking. Equality is required only at the documented
source join below; a source/registry collision, source/spot collision,
registry/spot collision, or sibling-spot collision is an authoring error.

### Community/source identity

In the retained compact shape, these represent one community/source identity
and therefore match:

```text
compiled area NodeRef-derived identity
  == worldCompiledCommunityAreaNode_Streamable.sourceObjectId.hash
  == worldCommunityRegistryItem.communityId.entityId.hash
```

This equality joins the registry item to its streamed source. It does not mean
every nearby 64-bit ID should reuse the same value.

### Registry-node identity

The `worldCommunityRegistryNode` is a separate world node and needs a separate
world-node identity. The historical crashing arrangement reused the
community/source value for that registry node. The repaired candidate assigned
a distinct identity and rejected future collisions.

The rule is not “add one” or “hash the debug name.” Preserve typed values and
derive the registry identity from the canonical full community NodeRef with
`_registry` appended to its final community name. Let the same RED4-aware
NodeRef path produce all related forms. Record the full synthetic registry
string as well as the serialized number so a review can explain where the
identity came from.

### AI-spot identity

Every `worldAISpotNode` has its own registered world identity. It appears in at
least three roles in the retained shape:

```text
registry template: spotNodeRefs[]       full NodeRef
compiled area:     spotNodeIds[]        worldGlobalNodeID
registry node:     workspotsPersistentData[].globalNodeId
```

That spot identity must be distinct from the community/source identity, the
registry-node identity, and every sibling spot. Array position and visible
debug text are not identity joins.

## Standalone `.community` resources are comparison sources

The vanilla depot also contains `communityCommunityTemplate` CR2W resources.
For example:

```text
base\open_world\minor_activities\westbrook\japantown\
  ma_wbr_jpn_13\community\ma_wbr_jpn_013_claws_com.community
```

**Observed in vanilla:** that resource's root owns
`communityCommunityTemplateData` with three `communitySpawnEntry` objects,
their character records, phases, appearances, time periods, quantities, and
local spot references.

Use it to study template semantics. Do not infer that the inspected mod-owned
`worldCommunityRegistryItem.template` is a soft path to this file: in the
retained compact registry it is embedded template data. Copying a vanilla
`.community` resource into a mod archive would also redistribute extracted
game content and preserve identities intended for another activity. Extract
your own reference and author a mod-owned registry instead.

## Focused WolvenKit review

For a mod-owned community, inspect these joins without pasting a complete
sector into your notes:

1. record the full compiled-area NodeRef and its derived source identity;
2. confirm the registry item's `communityId` matches that source identity;
3. derive the registry node identity from the full community NodeRef plus
   `_registry`, and confirm it is different;
4. list each entry and initial phase once;
5. derive each world-global AI-spot ID from that spot's full NodeRef and list
   both forms;
6. confirm the registry `spotNodeRefs`, area `spotNodeIds`, and persistent spot
   rows describe the same set;
7. reject zero values and every source/registry/spot/sibling collision;
8. confirm the block mounts both the AlwaysLoaded registry sector and the
   Quest area/spot sector;
9. confirm the questphase declares the prefab root required for its local
   community reference.

Do not use a numerical sort of the JSON arrays as a shortcut. The decisive
links are `NodeIndex`, typed IDs, entry/phase names, and NodeRefs.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Activation node runs but no community appears | Area sector streaming, `sourceObjectId`/`communityId` equality, prefab root, and entry initial state |
| One community affects another | Reused community/source identity or copied vanilla identity |
| Loading near the area crashes | Registry-node collision, malformed handles, bad spot IDs, or another resource activated at the same boundary |
| Registry looks correct but the actor never gets a place | Area `entriesData`/phase/period mirror and exact `spotNodeIds` |
| Spot exists but is not persistent or enabled as expected | Registry `workspotsPersistentData` and the spot's world-global identity |
| Old behavior survives a corrected archive | Return to a save made before any version of the community was installed |

Next: [Entries, phases, and AI spots](entries-phases-and-ai-spots.md).
