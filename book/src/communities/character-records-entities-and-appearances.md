# Character records, entities, and appearances

This chapter follows the native identity chain behind a community character.
Its practical outcome is a reviewable, mod-owned character definition whose
record, entity template, exposed appearance mapping, and internal appearance
definition agree before the character is introduced into quest logic.

It is an advanced authoring boundary, not a promise that an arbitrary set of
meshes will form a production-ready NPC. Rig compatibility, garment support,
materials, deformation, facial animation, LODs, censorship, and streaming all
remain runtime surfaces.

## Prerequisites and tested baseline

Read [Entries, phases, and AI spots](entries-phases-and-ai-spots.md),
[Activation, readiness, and acquisition](activation-readiness-and-acquisition.md),
and [Persistent state](../foundations/persistent-state.md) first. Use a separate
WolvenKit project for extracted comparison resources so that a vanilla file
cannot enter the distributable project by accident.

The focused inspection and structural checks on this page use:

- Cyberpunk 2077 Windows GOG `2.31a`, with Phantom Liberty for the cited
  `ep1\...` entity;
- WolvenKit `8.19.0`;
- ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31` for the wider
  quest package; and
- TweakXL `1.11.3` when adding a mod-owned `Character.*` record.

TweakXL is an authoring and loading mechanism for TweakDB changes. The engine
model described here remains the native `Character` record and its referenced
resources. A character that only reuses an existing record does not need a new
TweakXL record, but it also inherits that record's ownership and behavior.

## Vanilla references

The generic Tyger Claw record used in this chapter resolves through these
focused resources. Extract them into a separate research project:

```text
ep1\characters\entities\gang\gang__ep1_tyger_wa.ent
base\characters\appearances\gang\gang__tyger_wa.app
```

## The native resource chain

The community does not spawn an `.app` file directly:

```text
communitySpawnEntry.characterRecordId                 TweakDBID
  -> Character.<record>
       -> entityTemplatePath                          ResourcePath to .ent
       -> baseline reaction / faction / AI / equipment records
  -> entEntityTemplate
       -> defaultAppearance                           exposed mapping CName
       -> appearances[]
            entTemplateAppearance.name                exposed mapping CName
            entTemplateAppearance.appearanceName      internal .app CName
            entTemplateAppearance.appearanceResource  ResourcePath to .app
  -> appearanceAppearanceResource
       -> baseEntityType                              body-frame contract
       -> appearances[].appearanceAppearanceDefinition.name
       -> components[] + compiledData                 render/runtime graph
       -> meshes, morph targets, rigs, materials, animations, and support data
```

An appearance request therefore succeeds only when every boundary resolves.
The same visible word can occur in several layers, but the values do not become
interchangeable merely because they are all stored as `CName`.

## Keep the identifier domains separate

| Value | Type and owner | What it selects |
| --- | --- | --- |
| `Character.cqa_contact` | `TweakDBID` in TweakDB | Character gameplay record |
| `mod\cqa\characters\contact\contact.ent` | `ResourcePath` on the record | Root entity template |
| `cqa_contact_default` | `CName` on `entTemplateAppearance.name` | Appearance exposed by the entity |
| `default` | `CName` on `entTemplateAppearance.appearanceName` and the `.app` definition | Internal appearance payload |
| `mod\cqa\characters\contact\contact.app` | `ResourcePath` on the entity mapping | Appearance resource |
| Component names and bind names | `CName` values inside the appearance graph | Individual runtime components and attachment relationships |
| Community entry and phase names | Community-local `CName` values | Which actor definition and mode the community requests |
| Community and AI-spot references | `NodeRef` / world identity values | The spawned instance's world ownership and position |
| Scene `actorId` | Scene-local ID | Performer references inside one scene |

Do not use the character record, entity path, entry name, exposed appearance,
or scene actor ID as substitutes for one another. Record each typed value in
the resource inventory even when a UI label shortens it.

## The character record owns gameplay defaults

A `Character` record is more than a path to geometry. The installed schema
includes fields for the entity template, appearance selection, voice,
reactions, senses, faction and attitude, action map, archetype, equipment,
abilities, stats, loot, object actions, UI presentation, and persistence
priority.

For quest work, review at least these inherited surfaces:

| Record surface | Why it matters to a quest |
| --- | --- |
| `$base` inheritance | Pulls in a large behavior and interaction baseline; `Quest_NPC_Base` and a gang gameplay base are not neutral equivalents. |
| `entityTemplatePath` | Must resolve to the intended mod-owned `.ent` or an explicitly accepted game dependency. |
| `appearanceName` | Can participate in the requested exposed appearance; it is not the internal `.app` definition by default. |
| `reactionPreset`, `baseAttitudeGroup`, `affiliation` | Influence passivity, hostility, reactions, and other systems outside the quest graph. |
| `actionMap`, `archetypeData`, `abilities` | Supply gameplay AI actions and capabilities; assigning a quest role does not erase them. |
| equipment and loot | Can arm the actor and create drops or rewards the quest did not intend. |
| `voiceTag` and audio fields | Join later spoken/audio systems; a visible actor is not proof that casting is correct. |
| display-name fields | Join localization/UI; they are not community or scene identities. |
| savable/priority behavior inherited from the base | Can change reload and lifecycle behavior and therefore needs clean-save testing. |

The cited Tyger Claw record is useful because its exact spawn lineage is
retained. It is not a neutral contact: its inherited faction, aggression,
weapons, loot, action map, archetype, and abilities remain part of the actor.
Prefer a purpose-authored record for a recurring story character, and make its
base-class choice an explicit design decision.

## The entity exposes appearance mappings

An `entEntityTemplate` owns the runtime entity scaffold and a list of
`entTemplateAppearance` mappings. A focused mapping has three decisive values:

```text
entTemplateAppearance
  name: cqa_contact_default
  appearanceName: default
  appearanceResource: mod\cqa\characters\contact\contact.app
```

`name` is the exposed selection used by the entity/default/world-facing
contract. `appearanceName` chooses one definition inside the referenced
appearance resource. The two may intentionally differ.

The entity also owns its default exposed selection, runtime entity class, root
components, includes, bindings, and compiled representation. A root built for
one body frame is not converted into another frame by changing a single
appearance name. The retained research male entity has 110 root components;
the installed EP1 Tyger woman entity has a different graph. Those counts are
observations, not targets to copy.

## The appearance owns the renderable component graph

An `appearanceAppearanceResource` contains one or more
`appearanceAppearanceDefinition` objects. A definition can own skinned and
static mesh components, facial and animation setup, garment support, shadows,
dangle/physics relationships, chunk masks, bind names, visual tags, proxy and
LOD data, and resolved dependencies.

The focused properties to audit are:

| Property | Contract |
| --- | --- |
| `baseEntityType` | Declares the expected entity/body frame such as `ManAverage` or `WomanAverage`. |
| definition `name` | Must match the entity mapping's internal `appearanceName`. |
| `components[]` | Authored component graph, including resources, bindings, enabled state, and visual settings. |
| `compiledData` | Cooked/runtime representation associated with the appearance; do not assume an edit to the visible component list regenerated it. |
| `resolvedDependencies` and resource fields | Must resolve to installed game assets or mod-owned paths that the package actually ships. |
| mesh appearance, chunk mask, bind and skinning values | Select presentation inside each component; a valid mesh path alone is insufficient. |

The installed Tyger `.app` demonstrates that one appearance resource can serve
many internal definitions. The retained mod-owned pair demonstrates the
smaller one-definition arrangement. Neither is a magic template. Do not copy
the extracted Tyger resource into a mod or redistribute any of its binary
dependencies.

## Manual WolvenKit inspection

Use a comparison project that will never be packed:

1. In WolvenKit's Asset Browser, find the exact entity and appearance depot
   paths cited above. Confirm that the entity comes from `ep1` and record that
   dependency.
2. Extract or add them only to the comparison project. Open the `.ent` in the
   CR2W editor and inspect `RootChunk`, `defaultAppearance`, and
   `appearances[]`.
3. For one mapping, record the exposed `name`, internal `appearanceName`, and
   full `appearanceResource` path.
4. Open that `.app`. Confirm `RootChunk` is
   `appearanceAppearanceResource`, inspect `baseEntityType`, and locate the
   exact internal definition by `name` rather than array position.
5. Inspect a few decisive components and their compiled counterparts. Follow
   their resource paths locally; do not paste the complete resource or copy it
   into the distributable project.
6. In WolvenKit's Tweak Browser, inspect the selected `Character.*` record and
   its inheritance. Record the effective entity path, appearance/default,
   reaction, faction, action map, archetype, equipment, abilities, voice, and
   expansion requirements.
7. Close the comparison project and verify that none of its extracted
   game-owned resources appear in the distributable project's packed file
   list.

This is **Observed in vanilla** inspection. It becomes neither permission to
redistribute the files nor runtime proof for a new character.

## Manual authoring boundary

Author under a unique namespace, for example:

```text
archive\mod\cqa\characters\contact\contact.ent
archive\mod\cqa\characters\contact\contact.app
r6\tweaks\cqa\character_contact.yaml
```

Use a mod-owned, redistributable entity/appearance shell that is compatible
with the intended body frame. Do not turn an extracted vanilla CR2W into the
shipping shell. Building a complete NPC entity scaffold from an empty CR2W is
outside the retained evidence; if no legal shell exists, keep the character
**Experimental** and create a dedicated resource fixture before integrating
it into a quest.

In the WolvenKit CR2W editor:

1. Open the mod-owned `.ent` and reduce the first test to one exposed
   appearance mapping.
2. Set a unique exposed `name`, point `appearanceResource` at the mod-owned
   `.app`, and set `appearanceName` to the exact internal definition.
3. Set `defaultAppearance` to that exposed name. Remove or rename stale shell
   mappings that can be selected accidentally.
4. Open the mod-owned `.app`, confirm the frame-compatible
   `baseEntityType`, and give the one test definition the intended internal
   name.
5. Add or change one reviewed component bundle at a time. Preserve the
   component class, bind/skin target, companion pieces, chunk mask, mesh
   appearance, animation/physics support, and both authored and compiled
   representations required by the shell.
6. Save, reopen, and inspect both files. A successful save is only a
   **Structurally validated** intermediate check after a WolvenKit
   serialize/deserialize round trip.

Then add the mod-owned TweakDB record with TweakXL. At minimum, explicitly
review its unique record name, inherited base, `entityTemplatePath`, display
localization, affiliation/attitude policy, `voiceTag`, and any appearance
selection. Add combat archetype, action map, abilities, equipment, stats, and
loot only when the quest actually needs them. Do not inherit a gang or boss
record merely to obtain one visual.

Finally, put the new record's `TweakDBID` in the community entry and make the
community phase request the intended exposed appearance contract. Keep the
existing community, world, readiness, and cleanup identifiers unchanged for
the first isolated character swap; changing all layers at once destroys the
failure boundary.

## Structural acceptance before launch

Before packing, make a compact inventory and reject the build unless:

- the TweakDB record name and every mod depot path are unique;
- the record's `entityTemplatePath` resolves to the packed `.ent`;
- `defaultAppearance` is present in the entity's exposed mapping set;
- every exposed mapping has a non-empty internal name and a resolvable `.app`;
- every internal name exists exactly once in the referenced `.app`;
- entity frame, appearance `baseEntityType`, rigs, skinning targets, and
  component bundles agree;
- no generated or edited file overrides a game-owned depot path;
- every game-owned dependency is referenced by path rather than redistributed;
- expansion-only paths are declared as requirements;
- WolvenKit reopens the cooked resources without dropping handles,
  components, mappings, or dependencies; and
- the final archive contains only the intended mod-owned resources.

ArchiveXL mounting, TweakXL loading, WolvenKit reopening, and a clean log are
necessary diagnostics. They do not prove that the puppet renders or behaves.

## Clean-save and lifecycle matrix

Character records, community actors, death/defeat state, scene ownership, and
appearance/lifecycle state can interact with the save. After changing a record
name, entity path, exposed mapping, internal definition, community identity,
or actor topology, begin from an untouched pre-activation save.

| Start | Action | Required observation |
| --- | --- | --- |
| Clean pre-activation save | Activate only the character's community | Exactly one actor spawns with the intended exposed appearance and no invisible logical puppet |
| Same clean baseline clone | Approach from each supported route | Correct LODs, materials, hair/clothing behavior, facing, collision, and no late component pop |
| Active actor | Stream out and return | Same record, appearance, equipment, and community entry return without duplication |
| Supported pre-scene save | Reload, then start the scene | Scene acquires the same actor; facial/body animation and voice casting remain coherent |
| Active actor in intended passive/combat cases | Exercise reactions and damage policy | Faction, attitude, equipment, archetype, mortality, and loot match the quest design |
| Post-outcome save | Reload, leave the cleanup boundary, revisit | Outcome persists; actor releases once; no stale appearance or reactivation |
| Completed save | Remove the mod archive and load only a disposable clone | Failure is isolated and understood; never use a valuable save for removal testing |

Record the archive SHA-256, TweakXL file hash, complete version set, starting
save, community/entry/appearance names, route, and first/last visible state for
each run. Promote only the exact in-matrix artifact.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Logical actor exists but is invisible | Requested exposed name, entity mapping, internal `.app` name, resource path, component enabled state, and compiled representation |
| Appearance from another NPC appears | Record inheritance, `appearanceName`, entity default, community phase appearance, dirty-save history, and mapping-name collision |
| Body, clothing, or hair is malformed | `baseEntityType`, rig/skin target, bind names, garment support, chunk masks, companion components, and frame compatibility |
| Actor is unexpectedly hostile or armed | Record base, reaction preset, attitude/faction, action map, archetype, abilities, and equipment |
| Actor works until stream-out or reload | Persistent identity, community lifecycle, entity dependencies, LOD/proxy data, and clean-save provenance |
| Scene has the actor but face/body animation fails | Rig and facial setup, scene performer binding, animsets, voice/lipsync resources, and whether the body frame matches the authored performance |
| Package replaces a vanilla NPC globally | A game-owned CR2W was shipped or a shared vanilla record was mutated instead of adding mod-owned paths and records |

Next: [AI roles, behavior, and workspots](ai-roles-behavior-and-workspots.md).
