# Devices and persistence

A placed device is a resource chain, not merely a mesh with a NodeRef. The
world node selects an entity template and placement; the template supplies
components and slots; optional node-local instance data can override
controllers; quest logic addresses an identity; save data can retain the
result after the archive changes.

```text
worldEntityNode or worldDeviceNode
  -> entityTemplate (*.ent)
  -> optional instanceData
     -> entEntityInstanceData
        -> RedPackage controller/component chunks
  -> world placement and NodeRef
  -> context-dependent global device/persistence resources
```

## Evidence and version boundary

| Label | Bounded claim |
| --- | --- |
| **Observed in vanilla** | The world-node, template, node-local package, slot, `.devices`, and `.psrep` relationships below come from focused extracts of the named depot resources. |
| **Structurally validated** | Prior mod-owned research round-tripped a `worldDeviceNode`, entity-template reference, and nonzero RedPackage buffer without conflating it with sector inplace content. |
| **Runtime-proven** | Retained device tests showed that preserving template-matched component CRUIDs restored one laptop's authored Files UI, and that a save could retain an earlier device package. This does not prove a universal controller recipe. |
| **Experimental** | No custom-device procedure in the current book has passed the complete pinned clean-save matrix. Lab 3 deliberately contains no device. |

The most useful vanilla paths are:

```text
base\worlds\03_night_city\_compiled\default\exterior_19_-8_0_0.streamingsector
base\worlds\03_night_city\_compiled\default\4fd0915183681e53.streamingsector_inplace
base\gameplay\devices\drop_points\drop_point.ent
base\worlds\03_night_city\_compiled\default\03_night_city.devices
```

The retained extracts are WolvenKit JSON `0.0.9`, serialized by WolvenKit
`8.17.4`, with CR2W `GameVersion: 2310`. Extract your own comparison resources
and keep excerpts focused. The practical target is Cyberpunk 2077 Windows GOG
`2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript
`0.5.31`.

## `worldEntityNode` and `worldDeviceNode`

Retained vanilla sectors contain both types. Treat the serialized node type as
evidence; do not classify a placement solely from its visible appearance or
the filename of its entity template.

| Concern | `worldEntityNode` | `worldDeviceNode` |
| --- | --- | --- |
| Entity-template placement | Yes, in observed contexts | Yes, in observed contexts |
| Node-local `instanceData` | Present in observed entity examples | Present in mod-owned and vanilla device research shapes |
| Device-specific world fields | Not established by the generic type name | Retained shapes expose fields such as device class, alpha-hack streaming override, and entity streaming properties |
| Controller behavior | Comes from the template and/or bound package, not the node name alone | Comes from the template and/or bound package, not the node name alone |

A focused placement excerpt is:

```text
worldEntityNode or worldDeviceNode
  entityTemplate: base\...\template.ent
  instanceData
    entEntityInstanceData
      buffer: RedPackage

worldNodeData
  Position / Orientation / Scale
  QuestPrefabRefHash: full device NodeRef
```

Do not raw-copy an unrelated vanilla `RedPackage`. Controller chunks can
contain template-coupled component IDs, quest state, messages, actions, and
other instance-specific data.

## The entity template owns components and slots

The `.ent` supplies controller components, scanner components, appearances,
interaction components, workspots, and attachment slots. Which of these
exists is template-specific.

**Observed in vanilla:** `base\gameplay\devices\drop_points\drop_point.ent`
contains distinct UI and approach positions. Its retained slot investigation
found `UI_Interaction`, `poi_mappin`, `roleMappin`, and
`main_slot/navQuery` at different local offsets. That explains one drop-point
layout; it is not a standard slot set for computers, doors, access points, or
vending machines.

When a quest needs a slot:

1. Inspect the exact entity template and component hierarchy.
2. Record the component transform and slot-local transform.
3. Apply the owning entity's world transform.
4. Test interaction, icon height, and navigation endpoint separately.

A `slotName` written into a quest or journal reference is not proof that the
target template exposes that slot.

## NodeRef forms depend on context

The retained resources show several forms:

| Form | Observed context | Example |
| --- | --- | --- |
| Local child | Questphase device-manager target beneath available prefab dependencies | `#q108_dvc_door_to_soulkiller` |
| Local device-prefab root | A phase-node dependency that makes a device namespace available | `#loc_sq021_trailer_park_devices` |
| Local device target | Quest logic in that inspected location context | `#sq021_randy_pc` |
| Absolute world identity | Cross-resource world/device lookup and sector registration | The full SQ021 path below |

The retained SQ021 laptop identity is:

```text
$/03_night_city/se1/#loc_sq021_trailer_park/
loc_sq021_trailer_park_gameplay_prefabV4S2BNI/
#loc_sq021_trailer_park_devices/#sq021_randy_pc
```

These are **Observed in vanilla** examples, not string-rewrite rules. A local
target is resolved in its prefab context; an absolute reference carries the
world hierarchy. Do not mechanically concatenate a local root and child or
shorten an absolute native device reference without verifying the owner that
establishes resolution.

Device-relative identities can also appear beneath a location's device-prefab
root, as the SQ021 chain demonstrates. The root, target, phase dependency,
sector registration, and concrete placement must agree. Review [Quest prefabs
and NodeRefs](quest-prefabs-and-noderefs.md) before authoring a custom target.

## RedPackage is not an inplace sector

The retained SQ021 laptop chain provides a useful ownership boundary:

```text
exterior_19_-8_0_0.streamingsector
  worldEntityNode
    instanceData -> entEntityInstanceData -> RedPackage

nodeData.CookedPrefabData
  -> 4fd0915183681e53.streamingsector_inplace
     -> embedded entity templates
```

The node-local RedPackage contains controller/component chunks for that placed
entity. The `.streamingsector_inplace` owns embedded resources used by the
sector. They are separate even when the same placement refers to both. A
sector's `localInplaceResource` or `externInplaceResource` is a third property
location; questphase `inplacePhases` is unrelated again.

In the inspected laptop, component CRUIDs had to match the controller and
scanner components from its template for the authored controller data to bind.
Arbitrary replacement IDs left a visible, usable laptop but selected default
empty Files content. That is a bounded **Runtime-proven** result for that
template/package, not permission to reuse its IDs or payload elsewhere.

## `.devices` and `.psrep` are context-dependent

Do not teach either resource as universally mandatory or universally
irrelevant.

**Observed in vanilla:** the inspected SQ021 laptop's NodeRef hash,
node-data ID, and component CRUIDs were absent from the searched global
`03_night_city.devices`, `03_night_city_init.devices`, and direct values in
`03_night_city.psrep`. Its Files UI came from node-local instance data, so
those global resources were not prerequisites for that behavior.

In a different mod-owned research case, a sparse `.devices` entry was needed
as the candidate registration path for reliable quest-side controller lookup.
A `.psrep` patch remained optional until persistence evidence justified it.
This contrast is the rule: begin with the native comparison for the exact
device and operation, then add the smallest resource whose absence is actually
demonstrated.

| Requirement | Evidence to collect |
| --- | --- |
| Visible entity | Sector registration, node placement, entity template, appearance |
| Interaction | Template components, slots/workspots, controller binding |
| Quest device-manager action | Exact NodeRef context, controller class, lookup/registry behavior |
| Persisted controller state | Fresh-save and reload matrix, then `.psrep` or other persistence evidence if required |

One success does not prove the next row.

## Device identity is save-sensitive

Device persistent state can survive in the save after a package is removed or
changed. A retained test save continued to expose earlier copied content after
the authored arrays had been cleared. Repacking the same NodeRef therefore did
not create a clean experiment.

Use a new NodeRef when materially changing a test device's controller shape,
or return to a save that never streamed that identity. Keep the old and new
identities out of the same acceptance run. Resetting a quest fact does not
erase device controller state, journal state, or a streamed checkpoint.

## Device research procedure

For a chosen vanilla comparison:

1. Record its full NodeRef, source sector, `NodeIndex`, transform, and node
   type.
2. Inspect its exact entity-template path and appearance mapping.
3. Inspect template components, CRUIDs, workspots, and relevant slots.
4. Determine whether node-local `instanceData` exists and inventory its
   RedPackage chunks without copying the whole payload.
5. Follow sector inplace references separately.
6. Search `.devices` and `.psrep` for the exact identity, but treat absence and
   presence as evidence for that device only.
7. Inspect the quest node or condition that addresses it and record whether
   the NodeRef is local or absolute in that context.
8. Build a mod-owned minimal fixture and test visibility, interaction, quest
   action, persistence, cleanup, and replay as separate cases.

Never patch a shared vanilla entity template merely to change one placed
device. Prefer a mod-owned clone or a mod-owned placement with an explicitly
documented dependency chain.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Device is visible but action data is missing | Template/component binding and node-local RedPackage CRUIDs |
| Journal icon appears at the wrong height | Exact template slot and transform, not a presumed universal slot |
| Quest device-manager node cannot find a usable device | Local/absolute NodeRef context, prefab dependency, controller class, and `.devices` evidence |
| Adding `.devices` changes nothing | Verify that the failed behavior actually consumes that registry and that the sparse patch merged |
| State returns after removing an override | Save-backed device identity; use a clean save or fresh NodeRef |
| Inplace extraction lacks controller data | Check node-local `instanceData`; do not conflate RedPackage with `.streamingsector_inplace` |
| A copied controller works on one template only | Template-coupled components, slots, and CRUIDs were copied as hidden assumptions |

Previous: [Markers and navigation](markers-and-navigation.md). Next: [Location
research](location-research.md).
