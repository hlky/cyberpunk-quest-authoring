# Sector nodes and placement

A placed sector object is not represented by one array entry. In the compact
mod-owned arrangement used for the lab, its type lives in `nodes[]`, its
transform and streaming metadata live in `nodeData`, and its addressable
identity is registered in `nodeRefs`. Cooked vanilla sectors show that these
collections are not universally parallel, so review their explicit
relationships before assuming a marker or trigger is complete.

## Evidence and version boundary

**Observed in vanilla:** the node/data/reference relationships described here
occur in focused extracts from:

```text
base\worlds\03_night_city\_compiled\default\quest_606b61008df2ba6f.streamingsector
base\worlds\03_night_city\_compiled\default\always_loaded_0.streamingsector
base\worlds\03_night_city\_compiled\default\exterior_-18_28_0_0.streamingsector
base\worlds\03_night_city\_compiled\default\bd21168eed6c6d62.streamingsector_inplace
```

The retained extracts use WolvenKit JSON `0.0.9`, serialized by WolvenKit
`8.17.4`, with CR2W `GameVersion: 2310`. Extract your own copies for
inspection; this book does not ship the vanilla CR2W resources.

**Structurally validated:** the basic three-part placement shape and separate
`.streamingsector_inplace` reference survived round-trip inspection in prior
mod-owned research under WolvenKit `8.17.4`. Lab 3's three concrete nodes,
placement records, transforms, full child refs, and registered refs were
separately cooked and serialized back with WolvenKit `8.19.0`.

**Experimental:** the placement and streaming behavior has not passed the
target runtime stack: Cyberpunk 2077 Windows GOG `2.31a`, ArchiveXL `1.27.0`,
RED4ext `1.30.0`, and redscript `0.5.31`.

## The placement triad

| Sector structure | Responsibility |
| --- | --- |
| `nodes[index]` | Concrete node object and type-specific properties, such as a trigger's outline and notifiers |
| `nodeData.Data[*]` | Placement and cooked metadata; compact authored sectors use `NodeIndex` to associate a local concrete node |
| `nodeRefs[]` | Registered NodeRef identities that other resources can address |

A focused conceptual excerpt of that compact shape looks like this:

```text
nodes[3]
  $type: worldTriggerAreaNode
  ...type-specific properties...

nodeData.Data[*]
  NodeIndex: 3
  Position: Vector4(...)
  Orientation: Quaternion(...)
  Scale: Vector3(...)
  Pivot: Vector3(...)
  Bounds: Box(...)
  QuestPrefabRefHash: $/mod/.../#root/#trigger

nodeRefs[]
  $/mod/.../#root/#trigger
```

This is a property-focused explanation, not a complete serialized resource.
The actual CR2W also contains cooked and versioned data that should be
preserved through a supported editor rather than recreated from an abbreviated
excerpt.

## Do not assume the arrays are parallel

In the compact mod-owned shape and the focused vanilla Quest-sector sample,
`NodeIndex` associates a placement record with a concrete node. Do not infer
that association from the placement row's position. More importantly, do not
assume every cooked sector keeps the addressed concrete node in the same
local `nodes[]` array. `nodeRefs[]` is a registration set, not a guaranteed
one-for-one mirror of either collection.

The focused vanilla Quest-sector extract happens to contain 21 concrete
nodes, 21 placement records, and 21 registered NodeRefs. Its `NodeIndex`
values are `0` through `20`, and its 21 non-zero `QuestPrefabRefHash` values
match the registered NodeRef set. A focused vanilla AlwaysLoaded extract has
no local concrete nodes, four placement records, and 32 registered NodeRefs;
its placement indices are `3269`, `3273`, `3277`, and `3291`. Those two
arrangements are **Observed in vanilla**. Separately, a retained mod-owned
comparison has six nodes and four registered references and is
**Structurally validated** in its prior arrangement. Together they show why
equal counts and local array indices in one file are not schema rules.

## Transform and bounds

The retained `worldNodeData` shape includes:

- `Position` as a `Vector4`;
- `Orientation` as a quaternion;
- `Scale`, `Pivot`, and `Bounds`;
- `NodeIndex` and `QuestPrefabRefHash`;
- `CookedPrefabData`, `MaxStreamingDistance`, and `UkHash1`;
- fields exposed by WolvenKit as `UkFloat1` and `Uk10` through `Uk14`.

`QuestPrefabRefHash` is exposed as a NodeRef string in WolvenKit JSON despite
its name. Use the field's observed serialized type and value; do not replace
it with a numeric hash because the property name contains “Hash.”

The `Uk*` names mark an evidence boundary. Their exact meanings are not
established here. Earlier research treated `UkFloat1` as a
streaming-range-like value, but that hypothesis is not enough to rename or
explain the field as a universal engine contract. Preserve values from a
known-good, mod-owned seed or an editor-created resource, and isolate changes.

As an authoring approximation, one world coordinate unit is often treated as
roughly one metre. That is **Experimental** for player-facing distance: HUD
rounding, navigation routes, collision, slopes, and vertical geometry can all
make the experienced distance differ. Calibrate the actual site in game.

## Concrete nodes own behavior-specific data

The sector's concrete node carries properties unique to its type. The focused
vanilla Quest-sector extract includes 11 `worldAISpotNode` objects, six
`worldTriggerAreaNode` objects, three `worldSplineNode` objects, and one
`worldVehicleForbiddenAreaNode`. Its trigger nodes include area outlines and
quest trigger notifiers. That inventory is **Observed in vanilla** only for
the focused extract; it is not a complete catalogue of sector node types.

The later triggers chapter will explain `AreaShapeOutline`, outline height,
points, and `questTriggerNotifier_Quest`. The later markers chapter will
separate marker placement from [journal map-pin](../journal/mappins.md)
presentation. At this stage, the important rule is that type-specific data
belongs on the concrete node while placement and identity remain separate.

## Inplace resources are another ownership layer

`worldStreamingSector` can carry `localInplaceResource` and
`externInplaceResource`. An external entry can softly reference a
`.streamingsector_inplace`, whose `worldStreamingSectorInplaceContent` owns an
`inplaceResources[]` collection. In the retained serialized view, the embedded
CR2W bodies themselves are represented in top-level `Data.EmbeddedFiles`.

**Observed in vanilla:** the retained
`exterior_-18_28_0_0.streamingsector` references
`bd21168eed6c6d62.streamingsector_inplace`. That inplace resource has 45
`inplaceResources` references: 31 `.ent`, eight `.mesh`, and six `.xbm`. Its
top-level `Data.EmbeddedFiles` has 43 bodies: 31 `entEntityTemplate`, six
`CMesh`, and six `CBitmapTexture`. The unequal counts are another reason not
to infer array pairing without inspecting the actual handles and paths.

Do not confuse that sector-level resource with a node-local
`worldEntityNode.instanceData`, which can resolve through
`entEntityInstanceData` to a `RedPackage`. They are different owners even when
found during the same world investigation. Questphase `inplacePhases` is a
third, unrelated property domain; a shared word in the name does not make
these resources interchangeable. These observations are an ownership clue,
not permission to copy the extracted resources.

## Placement review procedure

Use WolvenKit's resource and property views so cooked structures remain under
editor control. For each mod-owned addressable node:

1. Inspect the concrete `nodes[]` object and explain every behavior-specific
   property the example supplies.
2. In the compact mod-owned sector, find the placement record whose
   `NodeIndex` is authored to associate with that object.
3. Verify position, orientation, scale, pivot, and bounds against the intended
   site.
4. Verify `QuestPrefabRefHash` is the intended full child NodeRef.
5. Confirm `nodeRefs[]` registers that identity when another resource must
   address it.
6. Review local and external inplace-resource ownership independently.
7. Save and round-trip the resource, then re-open it and repeat the checks.
8. Pack, inspect the archive paths, confirm block registration, and test the
   node in game from controlled saves.

Do not use a shortened text excerpt as an import template. The downloadable
Lab 3 project must contain complete mod-owned resources, and its authoring
reference must account for every supplied node and resource.

## Boundary Check placement contract

**Structurally validated:** the canonical resource places the checkpoint
marker at `(-1000.02, 1497.2208, 8.3)`. The reach trigger uses a 25-unit radius,
16 outline points, height 12, and base Z `2.3`. The leave trigger uses a
110-unit radius, 20 outline points, height 16, and base Z `0.3`. Its finite
padded block box encloses both areas and the intended approach.

Those values are inherited research inputs. Their encoded form is checked; it
does not prove that vertical coverage, placement, bounds, or streaming behavior
is correct in game. Regenerate and inspect `AreaShapeOutline.buffer` together
with `points` and `height` after any edit. Then test approach from several
directions, ordinary foot crossing, fast travel as a separate case,
reload before reach, reload between the boundaries, ordinary stream-away and
return while reach is active, departure, and completed-save reload. This set
does not support a separate post-completion re-entry claim.
[Triggers and
areas](triggers-and-areas.md) connects the state-shaped conditions to these
nodes.

## Common failures

| Symptom | Inspect |
| --- | --- |
| A different concrete node receives the transform | The authored `nodeData.NodeIndex` association; never rely on placement row order alone |
| Quest lookup fails for one placed node | Full `QuestPrefabRefHash`, `nodeRefs[]`, descriptor root, and questphase local path |
| Area appears offset or rotated | Position, quaternion orientation, pivot, scale, outline-local points, and Z coverage |
| Behavior changes near the site edge | Descriptor box, node bounds, streaming-distance fields, and test approach direction |
| An entity node exists but a referenced template is missing | Check the separate external/local inplace-resource layer and exact depot path |
| Editor save succeeds but runtime behavior is absent | Round-trip structure, archive contents, ArchiveXL registration, external resources, and runtime logs are separate gates |
| Old saves disagree with clean tests | Saved facts, journal state, checkpoints, and persistent world/device state may survive the archive edit |

For Lab 3 acceptance, use a save created before any version of the quest was
installed. Derive separate saves before the reach crossing and after reach has
succeeded while the player remains inside the outer leave area. A static
placement edit may appear after a new process while the quest still follows
old saved facts or journal state; neither observation diagnoses the other. The
[persistent-state](../foundations/persistent-state.md) chapter defines that
boundary.
