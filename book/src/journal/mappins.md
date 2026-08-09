# Mappins: journal intent meets the world

A quest mappin is not a coordinate stored in a questphase. It is a journal
entry that describes presentation and points at a world-owned `NodeRef`. A
questphase changes the entry's state; the world resource still has to supply a
resolvable target.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Authoring target | [Pinned first-release versions](../reference/tested-versions.md) |
| Native type and property shapes | **Observed in vanilla** |
| New mod-owned mappin lifecycle | **Experimental** until exercised from a clean save on the pinned baseline |

The examples below are focused resource shapes, not a complete downloadable
world project. World-marker and streaming-sector construction is deliberately
deferred to [World integration](../world/index.md).

## The ownership chain

```text
questphase
  -> questMappinManagerNodeDefinition
     -> gameJournalPath
        -> gameJournalQuestMapPin
           +-> mappinData                 presentation and routing policy
           +-> reference.reference        NodeRef
                                          -> world-owned marker or entity
```

Each link answers a different question:

| Owner | Responsibility |
| --- | --- |
| Questphase | Decide when the pin becomes active or inactive |
| Journal resource | Own the pin entry, caption key, map style, and target reference |
| World resource | Own the marker or entity identified by the `NodeRef` |
| Onscreen localization | Resolve the caption key to player-facing text |
| Save | Retain journal and tracking state after activation |

A valid journal path does not create its target. A valid `NodeRef` does not
make a journal entry active. Packing both resources does not prove that the
target is loaded or that the player sees a route.

## `gameJournalQuestMapPin`

A quest pin normally sits beneath the objective it presents. The exact leaf
type is `gameJournalQuestMapPin`.

| Property | Type or domain | Responsibility |
| --- | --- | --- |
| `id` | Journal entry ID | Final component of the journal path |
| `enableGPS` | Boolean | Allows the pin to participate in GPS routing; it does not activate the pin by itself |
| `mappinData.active` | Boolean | Authored initial presentation state; runtime journal state is still changed by quest nodes |
| `mappinData.localizedCaption.value` | Localization key | Player-facing caption lookup |
| `mappinData.mappinType` | `TweakDBID` | Mappin definition, commonly `Mappins.QuestStaticMappinDefinition` in the cited shape |
| `mappinData.variant` | Mappin variant | Visual role such as `DefaultQuestVariant` |
| `mappinData.visibleThroughWalls` | Boolean | Whether the world indicator may remain visible through geometry |
| `reference.reference` | `NodeRef` | World target; this is not a journal ID or graph node ID |
| `slotName` | `CName` | Attachment slot such as `UI_Interaction` when the target exposes one |
| `offset` | `Vector3` | Local display offset from the referenced target |
| `uiAnimation` | `TweakDBID` | Optional UI animation record; `0` means none in the cited shape |

`mappinData.debugCaption` is useful during inspection, but it is not a
replacement for `localizedCaption.value`. A copied vanilla `LocKey#...` also
does not become mod-owned text. Use a unique key registered through the mod's
onscreen localization resource.

The SQ021 journal contains an **Observed in vanilla** example beneath one of
its objectives:

```text
gameJournalQuestObjective
└── gameJournalQuestMapPin  id: lab_mp
    ├── enableGPS: 1
    ├── mappinData.mappinType: Mappins.QuestStaticMappinDefinition
    ├── mappinData.variant: DefaultQuestVariant
    ├── reference.reference: #sq021_mp_inside_lab
    └── slotName: UI_Interaction
```

Inspect it by extracting your own copy of:

```text
base\journal\cooked_journal.journal
```

Navigate to the SQ021 quest entries rather than redistributing the extracted
resource.

## Activating and hiding a quest pin

The questphase-side node is `questMappinManagerNodeDefinition`.

| Property | Required meaning |
| --- | --- |
| `path.className` | `gameJournalQuestMapPin` |
| `path.realPath` | Full path to the exact pin entry |
| `path.fileEntryIndex` | Index of the containing quest file entry; `2` for a path shaped like `quests/minor_quest/cqa003/...` |
| `path.editorPath` | Normally empty in the cited serialized resources |
| `disablePreviousMappins` | Whether this transition also clears earlier mappin/GPS state |

Its normal socket contract is:

| Socket | Direction | Meaning |
| --- | --- | --- |
| `CutDestination` | Cut destination | Interruption obligation; do not guess a connection |
| `Active` | Input | Request the referenced quest pin's active state |
| `Inactive` | Input | Request its inactive state |
| `Out` | Output | Continue after the state request |

The state is selected by the incoming socket. `disablePreviousMappins` does not
turn an `Inactive` connection into an activation, and `Out` is not evidence
that the UI has already redrawn.

A minimal lifecycle is:

```text
activate and track objective
  -> mappin manager through Active
  -> wait for the objective's world condition
  -> succeed objective
  -> same mappin path through Inactive
  -> activate the next destination
```

SQ021 contains an **Observed in vanilla** manager node at:

```text
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
```

The cited node addresses
`quests/side_quest/sq021_sick_dreams/randys_room/investigation/investigation_mp`
with `className: gameJournalQuestMapPin`, `fileEntryIndex: 2`, and
`disablePreviousMappins: 0`. This is a concrete comparison point, not a whole
phase to copy.

## When to clear previous routing

Keep `disablePreviousMappins: 0` as the ordinary value unless the transition
is intentionally establishing a replacement destination.

**Runtime-proven in a retained legacy fixture:** in one delivery transition,
inactivating the earlier pin still left a stale second dotted GPS leg. Setting
`disablePreviousMappins: 1` on the activation node for the new destination
cleared that route. The later deactivation node retained `0`.

That result proves one transition, not a universal rule that every activation
must clear every earlier pin. Overusing it can erase a different objective's
valid destination. For a new arrangement, test these separately:

1. the first pin appears;
2. its GPS route targets the intended marker;
3. inactivation removes its presentation;
4. the next pin does not retain a stale route;
5. reloading at each boundary produces the same intended state.

The legacy run was not retained against the complete pinned book environment,
so this chapter does not promote a new `cqa` mappin project to
**Runtime-proven**.

## Quest pins and point-of-interest entries are different

`gameJournalPointOfInterestMappin` is a separate journal family. It associates
a map POI with a quest and supports both static and dynamic presentation data;
it is not merely a quest pin with a longer name.

| Concern | `gameJournalQuestMapPin` | `gameJournalPointOfInterestMappin` |
| --- | --- | --- |
| Typical owner | Nested beneath a quest objective | Entry beneath `points_of_interest/<group>` |
| Quest association | Implied by its containing objective path | Explicit `questPath` handle |
| World target | `reference.reference` | `staticNodeRef` and, when used, `dynamicEntityRef` |
| Presentation data | `gamemappinsMappinData` | `gamemappinsPointOfInterestMappinData` |
| Definition fields | `mappinType`, `variant` | `dynamicMappinDef`, `staticMappinDef`, `typedVariant` |
| Questphase lifecycle in this chapter | `questMappinManagerNodeDefinition` Active/Inactive | Do not substitute it for the quest-pin path without evidence for that exact use |

The decisive POI properties are:

| Property | Meaning |
| --- | --- |
| `mappinData.active` | Authored POI availability in the cited shape |
| `mappinData.dynamicMappinDef` | Dynamic POI definition `TweakDBID` |
| `mappinData.staticMappinDef` | Static POI definition `TweakDBID` |
| `mappinData.typedVariant` | Handle containing a typed mappin variant |
| `mappinData.slotName` / `slotOffset` | Attachment slot and local offset |
| `staticNodeRef` | Static world marker |
| `questPath` | Typed `gameJournalPath` back to the associated quest |

In `base\journal\cooked_journal.journal`, the entry at
`points_of_interest/minor_quests/mq025_psycho_brawl` is **Observed in
vanilla** with:

```text
staticNodeRef: #mq025_mp_quest_start
questPath.realPath: quests/minor_quest/mq025_psycho_brawl
questPath.className: gameJournalQuest
questPath.fileEntryIndex: 2
dynamicMappinDef: Mappins.DynamicPointOfInterestMappinDefinition
staticMappinDef: Mappins.StaticPointOfInterestMappinDefinition
typedVariant.variant: DefaultQuestVariant
```

There are two index domains here. If a node addresses the POI entry itself,
the containing file entry in `points_of_interest/minor_quests/...` is
`minor_quests`, at index `1`. The POI's internal `questPath` points into
`quests/minor_quest/...`, whose containing quest entry is at index `2`.
Neither value is a leaf index or handle ID.

## The world boundary

Before blaming the journal, prove the target exists in the relevant world
scope:

1. Resolve the exact `NodeRef`, including its `#`-relative or `$`-absolute
   form.
2. Identify the streaming sector, prefab, or entity that owns it.
3. Confirm that resource is installed at the intended depot path.
4. Confirm the target is loaded when the pin is activated.
5. Check whether `slotName` is valid for the target or whether the pin should
   use the marker origin plus `offset`.

A cross-world entity reference can be valid text and still fail to resolve at
runtime. A dedicated static marker at the intended coordinates can make a
better quest-pin target than an unrelated interactive device, but constructing
and streaming that marker belongs to the world chapter. Do not patch a vanilla
sector merely to avoid creating a mod-owned world resource.

## Save-aware verification

Mappin activation, journal state, quest tracking, and GPS history can be
save-backed. Repacking the same path does not erase an earlier route. A fact
edit also does not clear journal or tracker state.

Use a save made before the custom journal and target were first installed for
the initial run. Retain separate saves for active-pin, completed-objective, and
next-destination reload checks. When changing a world target's identity or
streaming ownership, return to that pre-install save rather than interpreting
old state as the new resource's behavior.

## Failure routing

| Symptom | First boundary to inspect |
| --- | --- |
| Manager node runs but no pin appears | `path.className`, full `realPath`, `fileEntryIndex`, and ArchiveXL journal registration |
| Pin appears at the wrong place | `reference.reference`, target ownership, `slotName`, and `offset` |
| Caption is blank | `localizedCaption.value` versus the registered onscreen localization key |
| Pin appears but GPS does not route | `enableGPS`, mappin definition/variant, target resolution, and current tracking state |
| Old dotted route remains | Explicit inactivation order, next activation, then a focused `disablePreviousMappins` test |
| Pin works only on an old save | Treat that as suspect; repeat from a save that never loaded the custom journal/world identity |
| POI appears but objective pin does not | Verify that the quest pin and POI are separate entries with separate paths and targets |

Validate in layers: resource deserialization, journal path resolution, archive
and ArchiveXL registration, world-target resolution, controlled runtime
activation, deactivation, reload, and clean replay. No earlier layer proves the
later one.
