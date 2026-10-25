# Entity spawners and status effects

The status system requests an effect by name. The target entity must have an
effect descriptor with that same name, pointing to your timeline. A successful
status application can still produce no custom visual if that descriptor is
missing.

Use the [custom-effects toolchain](index.md#tools-and-versions), including
TweakXL for the records below. Restart the game after changing records or
entity patches.

## Keep the names and paths separate

| Domain | Example | Must match |
| --- | --- | --- |
| TweakDB VFX record | `CQAEffects.FX` | The status's `VFX` array |
| Effect CName | `cqa_optics_glitch` | `StatusEffectFX.name` and `entEffectDesc.effectName` |
| Component CName | `cqa_optics_fx` | Your independently named spawner component |
| Effect resource path | `mod\cqa\effects\optics_npc.effect` | Descriptor's `effect` reference |
| Placement tag | `Head` | A compatible slot on the target entity |
| Timeline event RUID | An unsigned 64-bit value | The matching compiled `eventRUID` |

The component name is not the effect name. The effect name is not a depot
path. Changing one does not rename the other fields.

## Add one named spawner

For a character entity you own, add the spawner to that entity's compiled
component package in WolvenKit. For patching an existing entity, create a
small mod-owned patch `.ent` containing an entity root and your spawner:

```text
entEntityTemplate
  compiledData -> RedPackage
    Chunks
      entEntity
      entEffectSpawnerComponent
        name: cqa_optics_fx
        id: <unique component CRUID>
        effectDescs[] -> entEffectDesc
          id: <unique descriptor CRUID>
          effectName: cqa_optics_glitch
          effect: mod\cqa\effects\optics_npc.effect
          compiledEffectInfo: worldCompiledEffectInfo
```

Generate new component and descriptor IDs in WolvenKit. Keep the package's
component-ID entries consistent when adding chunks. Add the effect path to
the template's `resolvedDependencies` where required by its resource shape.

Use a new component name. Replacing the target's existing status-effect
spawner can remove unrelated game effects. The patch entity should contain
your additions, not a complete copied player or NPC template.

## Bind events to a placement

The descriptor's `compiledEffectInfo` joins the timeline's events to a target
slot and relative transform:

```text
placementTags[0]: Head
relativePositions[0]: (0, 0, 0.18)
relativeRotations[0]: identity quaternion
placementInfos[0]
  placementTagIndex: 0
  relativePositionIndex: 0
  relativeRotationIndex: 0
eventsSortedByRUID[]
  eventRUID: <same ruid as the timeline item>
  placementIndexMask: 1
```

For this single-placement layout, mask `1` selects the first placement. Each
particle or sound item gets a matching event row; the loop marker does not
need one. Sort rows by the full unsigned numeric RUID. Preserve compatible
native flags when adapting the placement structure.

`0.18` is an example offset above the NPC's head slot. Tune it on the actual
character. Check the slot's binding to its bone in the entity's slot component;
writing `Head` in a descriptor does not create that slot.

After adding or deleting a timeline event, update this table too. A valid
`.effect` with stale placement rows can fail at a different point from a
missing particle or material.

## Patch the actual entity templates

ArchiveXL maps a patch resource to the templates receiving it:

```yaml
resource:
  patch:
    mod\cqa\effects\registration\optics_v.ent:
    - base\characters\entities\player\player_ma_fpp.ent
    - base\characters\entities\player\player_wa_fpp.ent
    - base\characters\entities\player\player_ma_tpp.ent
    - base\characters\entities\player\player_wa_tpp.ent
```

This list covers the named player templates. Add the appropriate cutscene,
reflection, or Phantom Liberty templates when those views are part of your
supported behavior. Do not infer coverage from a single first-person test.

For NPCs, map `optics_npc.ent` to the exact entity template used by the
character record. Add a custom character's own depot path explicitly; a list
of vanilla gang templates does not cover it. Start with one supported target
before expanding to more body types or factions.

The `.effect`, particles, and textures are reached through native references.
They do not need separate quest-root registrations.

## Define the status records

The following TweakXL YAML gives a derived visual status a six-second duration
and requests the named spawner effect:

```yaml
CQAEffects.DurationValue:
  $type: ConstantStatModifier
  modifierType: Additive
  statType: BaseStats.MaxDuration
  value: 6.0
CQAEffects.Duration:
  $type: StatModifierGroup
  statModsLimit: -1
  statModifiers: [CQAEffects.DurationValue]
CQAEffects.FX:
  $type: StatusEffectFX
  name: cqa_optics_glitch
  shouldReapply: false
BaseStatusEffect.CQAOpticsVision:
  $base: BaseStatusEffect.QuickHackBlind
  duration: CQAEffects.Duration
  VFX: [CQAEffects.FX]
  SFX: []
BaseStatusEffect.CQAOpticsBlind:
  $base: BaseStatusEffect.ShortBlind
  duration: CQAEffects.Duration
```

Use the exact field names `VFX` and `SFX`. Lowercase `vfx` or `sfx` does not
override them. This can leave the inherited white blindness presentation in
place even though the custom item and status exist.

The two status records have different responsibilities: the visual status
requests your effect, while the short-blind status supplies the paired native
gameplay effect. Do not apply the same pair twice from different routes.
`shouldReapply: false` is a starting policy, not a guarantee about overlapping
status applications; check reapplication in game.

## Trigger a player test through an inventory action

Use `Instigator` for a self-test. `Target` is appropriate for the recipient of
a targeted action such as a quickhack.

```yaml
CQAEffects.ApplySelfVision:
  $type: ObjectActionEffect
  recipient: ObjectActionReference.Instigator
  statusEffect: BaseStatusEffect.CQAOpticsVision
CQAEffects.ApplySelfBlind:
  $type: ObjectActionEffect
  recipient: ObjectActionReference.Instigator
  statusEffect: BaseStatusEffect.CQAOpticsBlind
CQAEffects.SelfTestAction:
  $base: ItemAction.Eat
  completionEffects:
  - CQAEffects.ApplySelfBlind
  - CQAEffects.ApplySelfVision
Items.CQAOpticsSelfTest:
  $base: Items.LowQualityFood1
  displayName: cqa_optics_selftest_name
  localizedDescription: cqa_optics_selftest_description
  objectActions: [CQAEffects.SelfTestAction, ItemAction.Drop]
  itemSecondaryAction: CQAEffects.SelfTestAction
  OnEquip: []
  statModifierGroups: []
  statModifiers: []
```

`OnEquip` is also case-sensitive. Clearing the derived food item's stat
modifiers avoids inheriting unrelated food bonuses in this test item.

Create the two onscreen text keys and register their resource using
[Localization paths](../journal/localization-paths.md). To make the item
available through a native vendor, append your own stock record:

```yaml
CQAEffects.SelfTestStock:
  $type: VendorItem
  item: Items.CQAOpticsSelfTest
  quantity: [Vendors.Always_Present]
Vendors.wat_lch_netrunner_01:
  itemStock:
  - !append-once CQAEffects.SelfTestStock
```

Vendor availability and refresh are **Experimental** for a new item. Check on
a suitable clean save; a previously generated inventory may retain old stock.

## Connect a targeted quickhack

1. Inspect `QuickHack.BlindHack`, `Items.BlindProgram`, and their inherited
   action effects in the installed TweakDB.
2. Derive new item and action records under your own namespace.
3. Create `ObjectActionEffect` records using `ObjectActionReference.Target`
   for the two custom statuses.
4. In the derived action's `completionEffects`, replace the original
   blindness payloads and deliberately handle any spread payload. Preserve
   unrelated upload and control effects.
5. Point the derived item's `objectActions` at your action. Give its UI fields
   matching localized keys.
6. Equip the item and use it through the scanner on the NPC whose entity you
   patched. Check both status behavior and the rendered effect.

Remove inherited entries by their exact record IDs from your installed build.
Do not use an inline record number as a reusable base or copy an array index
without inspecting the effect it selects.

Next: [Test and troubleshoot](test-and-troubleshoot.md).
