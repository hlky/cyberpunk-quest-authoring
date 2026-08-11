# Markers and navigation

A marker, a quest pin, and a GPS route are related, but they are not one
resource. The world supplies an addressable anchor; the journal supplies UI
intent; a questphase changes journal state; the navigation system decides
whether a usable route exists.

```text
worldStaticMarkerNode + placement + registered NodeRef
  <- gameJournalQuestMapPin.reference.reference
     <- questMappinManagerNodeDefinition Active / Inactive
        -> HUD icon, map pin, and possible GPS route
```

## Vanilla references

These focused base-game resources are useful comparisons. Extract them from
your own installation; they are references, not files to copy into the project.

```text
base\worlds\03_night_city\_compiled\default\always_loaded_0.streamingsector
base\journal\cooked_journal.journal
base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase
base\gameplay\devices\drop_points\drop_point.ent
```

## Four records with different jobs

| Record | Owner | What it does not prove |
| --- | --- | --- |
| `worldStaticMarkerNode` | Streaming sector | It does not create a journal entry or activate UI. |
| `gameJournalQuestMapPin` | Journal resource | It does not place or stream its target. |
| `questMappinManagerNodeDefinition` | Questphase | Its `Out` signal does not prove the HUD redrew or GPS found a route. |
| `scnWorldMarker` | Scene/quest scene-location payload | It is not a substitute for a quest journal pin. |

The shared word “marker” describes several identifier consumers, not one
interchangeable type.

## `worldStaticMarkerNode` is the anchor

The concrete node is intentionally small:

```text
nodes[index]
  worldStaticMarkerNode
    debugName

nodeData[...]
  NodeIndex: index
  Position / Orientation / Scale / Bounds
  QuestPrefabRefHash: $/.../#root/#marker

nodeRefs[]
  $/.../#root/#marker
```

The node's placement determines the world anchor. Its full NodeRef is
registered world-side; a questphase or journal normally uses the corresponding
local reference beneath an available prefab root. A visible debug name is not
the identity and does not compensate for a mismatched NodeRef.

**Observed in vanilla:** retained AlwaysLoaded sectors register static-marker
NodeRefs in arrangements that are not always one-for-one with local concrete
nodes. Therefore the compact mod-owned shape above is useful for authoring,
but equal `nodes`, `nodeData`, and `nodeRefs` counts are not a schema rule.

## The journal entry owns presentation intent

`gameJournalQuestMapPin` owns the player-facing map-pin data:

| Property | Responsibility |
| --- | --- |
| `reference.reference` | Target NodeRef |
| `enableGPS` | Allows routing participation; it does not guarantee a route |
| `mappinData.mappinType` | Mappin definition TweakDBID |
| `mappinData.variant` | Visual role, such as `DefaultQuestVariant` in the cited shape |
| `mappinData.localizedCaption.value` | Onscreen localization key |
| `reference.slotName` | Optional slot exposed by an entity target |
| `offset` | Local display offset from the resolved target |

The focused vanilla journal includes local marker references beneath quest
objectives. Extract `base\journal\cooked_journal.journal` and inspect the
small containing quest subtree instead of copying the full resource. The
complete journal lifecycle is in [Mappins: journal intent meets the
world](../journal/mappins.md).

## The quest node owns activation and cleanup

`questMappinManagerNodeDefinition` addresses a typed `gameJournalPath`. Its
incoming `Active` or `Inactive` socket selects the requested state.
`disablePreviousMappins` is a transition policy, not the activation switch.

```text
objective Active
  -> mappin manager through Active
  -> wait for world condition
  -> mappin manager through Inactive
  -> objective Succeeded
```

Use `disablePreviousMappins: 0` unless the transition is deliberately
replacing prior routing, then prove the changed behavior. One retained legacy
route needed `1` on the new destination activation to clear a stale dotted
leg. That **Runtime-proven** result is bounded to that transition; applying it
everywhere can hide another valid objective.

## `scnWorldMarker` belongs to scene location semantics

Focused vanilla questphase extracts contain `scnWorldMarker` values inside
scene-related payloads, with a `nodeRef` selecting a scene location. This is a
different record from the streamed `worldStaticMarkerNode` and from a journal
pin. A scene may ultimately resolve a world marker NodeRef, but its scene
payload does not acquire journal caption, GPS, or quest-pin lifecycle merely
because it contains the word “marker.”

Keep distinct NodeRefs when scene placement and quest UI have different
ownership or lifetime needs. Do not point a journal pin at a scene marker
simply because that marker already exists without testing load scope and
cleanup.

## Slots are template-specific

An entity target can expose authored slots. **Observed in vanilla:** the
`drop_point.ent` template has UI and navigation-related slots at distinct
local transforms, including `UI_Interaction`, `poi_mappin`, `roleMappin`, and
`main_slot/navQuery`. The exact names and offsets belong to that template.

A static marker has no automatic knowledge of those entity-local slots. If a
mod-owned marker is used instead of the device NodeRef, calculate and test the
intended world position explicitly. Never generalize `UI_Interaction` or
`main_slot/navQuery` to unrelated templates; inspect the actual `.ent` and its
component hierarchy.

## GPS is an outcome, not a field

A route depends on more than `enableGPS`:

```text
active tracked objective
  + active quest mappin
  + resolvable loaded target
  + suitable endpoint near traversable space
  + navigation state
  -> possible route
```

Pin visibility, map visibility, a yellow world icon, and a complete drivable
or walkable route are separate observations. Test each one and record the
endpoint. A route to the marker origin can be wrong even when the icon appears
correctly above the target.

`worldStaticGpsLocationEntranceMarkerNode` also occurs in retained
world-location research. That is a narrow **Observed in vanilla** node-type
observation, not evidence that every quest pin needs an entrance marker or
that adding one repairs arbitrary GPS failures. Location systems, quest pins,
and entity navigation slots must be investigated in their actual owning
resources.

## Boundary Check marker contract

**Structurally validated:** Lab 3 has an AlwaysLoaded static marker named
`#cqa003_mp_checkpoint` at `(-1000.02, 1497.2208, 8.3)`. Its journal pin uses
`DefaultQuestVariant`, GPS enabled, and a unique localized caption. The quest
graph activates the pin before waiting for the reach area and deactivates it
after reach succeeds.

Both manager nodes use `disablePreviousMappins: 0`. The lab has no deliberate
previous route to replace, so the `Active` and `Inactive` sockets alone own the
requested transition. The separate retained replacement-route result above
does not justify setting this isolated activation to `1`.

The marker's category does not guarantee UI resolution, and the coordinate
does not guarantee a sensible route endpoint. Acceptance must cover target
resolution before approach, icon height, map presentation, route endpoint,
ordinary walking, deactivation, save/reload while active, and completed-state
reload.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| No pin, but the marker exists | Journal path, mappin manager socket, journal registration, and saved journal state |
| Pin appears at the origin or wrong place | `reference.reference`, full/local NodeRef chain, target load scope, slot, and offset |
| Icon is too low or high | Marker transform versus entity slot transform and journal offset |
| Pin appears but no GPS route exists | Tracking state, `enableGPS`, target resolution, route endpoint, and nearby traversable space |
| A stale dotted route remains | Explicit prior inactivation and a focused `disablePreviousMappins` replacement test |
| A scene starts but the quest pin fails | `scnWorldMarker` and journal mappin are separate records; inspect both owners |
| Old saves disagree with clean runs | Journal activation, tracking, routes, facts, and checkpoints may all be save-backed |

Previous: [Triggers and areas](triggers-and-areas.md). Next: [Devices and
persistence](devices-and-persistence.md).
