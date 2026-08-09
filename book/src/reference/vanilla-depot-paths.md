# Vanilla depot-path index

These are focused **Observed in vanilla** research anchors used by the book.
Extract them from your own Cyberpunk 2077 installation with WolvenKit, answer
one narrow question, and keep the extracted files out of distributable
projects.

The workflow is in [Inspect a vanilla
questphase](../start-here/inspecting-vanilla.md). A path in this index is a
citation, not a template and not a file supplied by this repository.

| Record | Value |
| --- | --- |
| Index review date | 2026-08-09 |
| Practical comparison target | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0` |
| Evidence class | **Observed in vanilla**, limited to the question named for each path |

## Core roots, journal, and localization

| Depot path | Inspect it for |
| --- | --- |
| `base\quest\cyberpunk2077.quest` | Game-owned parent used by ArchiveXL root-questphase registration; cite it, do not add an extracted copy to the mod |
| `base\journal\descriptor.journaldesc` | Standard soft descriptor reference used by contributed journal roots |
| `base\journal\cooked_journal.journal` | Focused journal entry families, typed paths, file-entry indices, mappins, contacts, messages, files, and saved presentation targets |
| `base\localization\en-us\onscreens\onscreens.json` | Focused English onscreen key lookup, including the Allen Street fast-travel label comparison |

The cooked journal is large. Search for one path and record only its entry
types, IDs, and relevant properties. Do not publish its complete
serialization.

## Questphases and control patterns

| Depot path | Focused question |
| --- | --- |
| `base\quest\side_quests\sq021\phases\sq021_randys_room.questphase` | How a computer-page output sets a fact and how a phase waits for that authored document signal |
| `base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase` | Prefab dependencies, trigger/device/scene-marker/AI-spot refs, Boolean gates, and a plant-item comparison |
| `base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase` | Facts, logical trees, trigger/time/journal/content conditions, and investigation progression |
| `base\open_world\minor_activities\watson\little_china\ma_wat_lch_03\ma_wat_lch_03_phase.questphase` | A focused `read_shard` objective whose progression does not use `questJournalEntryVisited_ConditionType` |
| `base\open_world\minor_activities\watson\little_china\ma_wat_lch_05\ma_wat_lch_05_phase.questphase` | A second focused `read_shard` comparison without a journal-visited condition |
| `base\open_world\minor_activities\watson\little_china\ma_wat_lch_15\phases\ma_wat_lch_15.questphase` | A third focused `read_shard` comparison using inventory, loot, or interaction state rather than a universal visited recipe |
| `base\quest\side_quests\sq011\phases\sq011_concert.questphase` | Game-time and real-time payloads plus delayed contact orchestration |
| `base\quest\side_quests\sq011\phases\sq011_follow_up.questphase` | Multi-day game-time delay before later contact logic |
| `base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase` | Parallel stealth-failure monitoring, stop/converge behavior, and optional outcomes |
| `base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_combat.questphase` | Combat-side stealth outcome handling and cleanup context |
| `base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_phase.questphase` | Parent prefab scope and external-child composition |
| `base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_openworld.questphase` | Device interaction, upload, and scan condition shapes |
| `base\open_world\street_stories\watson\little_china\sts_wat_lch_01\phase\sts_wat_lch_01_combat.questphase` | Device, killed, spawned, workspot, quickhack, and combat lifecycle shapes |
| `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03.questphase` | A parent that owns one prefab while external children use nested world refs |
| `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase` | Empty child `phasePrefabs`, destruction/device/combat/vehicle conditions, and nested refs |
| `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_gameplay.questphase` | Escort movement and ordered destination-gate research |
| `base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase` | Inventory, scan, scene, character-mount/carry, and vehicle-trunk condition shapes |
| `base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_09\phases\sts_wbr_jpn_09_gameplay.questphase` | Spawner readiness, distance, mount, and defend-target comparison |
| `base\open_world\street_stories\watson\kabuki\sts_wat_kab_05\phases\sts_wat_kab_05_openworld.questphase` | Journal completion/reward context and native drop-point reservation comparison |
| `base\quest\side_quests\sq004\phases\sq004_02_drive.questphase` | Player/contact mount conditions, vehicle assignment, seat roles, and destination-driving comparison |
| `base\quest\side_quests\sq031\phases\sq031_rogue.questphase` | Spawned readiness, puppet-AI tier work, and vehicle-forbidden-trigger context |
| `base\quest\side_quests\sq031\phases\sq031_porsche.questphase` | Player-vehicle record enable/despawn payload context; not a generic world-vehicle cleanup operation |
| `base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_02\phases\sts_wat_nid_02_gameplay.questphase` | Player-trigger contrasts and a van `CT_NOT_EQUAL`/`0` moving-state condition, not an exact stopped-inside delivery chain |
| `base\open_world\street_stories\badlands\inland_avenue\sts_bls_ina_07\phases\sts_bls_ina_07_gpl.questphase` | Composite chase staging: vehicle-seat assignment, AI roles, and route/lost-state facts |
| `base\quest\side_quests\sq024\phases\sq024_05_the_big_race.questphase` | Race start/stop/recovery, course splines, competitor parameters, checkpoints, and restriction lifecycle |
| `base\quest\side_quests\sq004\phases\sq004_03_raffen_shiv_camp.questphase` | Release/escort comparison, target readiness, follower AI, and later handoff context |
| `base\open_world\street_stories\watson\kabuki\sts_wat_kab_02\phases\sts_wat_kab_02_openworld.questphase` | Device release plus named-target readiness comparison |
| `base\open_world\street_stories\santo_domingo\arroyo\sts_std_arr_05\phases\sts_std_arr_05_openworld.questphase` | Plant-item device action/condition and inventory-consumption comparison |
| `base\open_world\phases\cyberpsychos\open_world_cyberpsychos.questphase` | Shared cyberpsycho orchestration, reveal/resolution families, and metaquest ownership; not a complete custom encounter recipe |

These phases depend on quest-local facts, journal entries, NodeRefs,
communities, devices, vehicles, and other child resources. A copied node is
not a self-contained recipe.

## Scenes, communities, and presentation

| Depot path | Focused question |
| --- | --- |
| `base\quest\minor_quests\mq003\mq003_orbitals.questphase` | Whole-community activation, spawned readiness, and activity-phase invocation |
| `base\quest\minor_quests\mq003\phases\mq003_homeless.questphase` | Named community phase changes and later deactivation |
| `base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene` | Community actor acquisition, entry/exit shape, performers, screenplay, events, and embedded localization ordering |
| `base\quest\minor_quests\mq003\scenes\mq003_03_orbital_pod.scene` | Comparable scene resource, actor, screenplay, event, and locStore structures |
| `base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene` | Comparable scene graph and embedded locStore ordering |
| `base\quest\minor_quests\mq010\scenes\mq010_02_barry_talk.scene` | Comparable dialogue scene and embedded locStore ordering |
| `base\animations\quest\minor_quests\mq007\anim\body\mq007__talking_gun__male_fpp.anims` | Direct scene-animation resource ownership and event-reference comparison; not a reusable custom clip |
| `base\localization\en-us\lipsync\base\quest\minor_quests\mq007\scenes\mq007_01_gun_found\skippy.anims` | English Skippy lipsync-set resource selected by the scene's lipsync reference row |
| `base\localization\en-us\lipsync\base\quest\minor_quests\mq007\scenes\mq007_01_gun_found\v.anims` | Separate English V lipsync-set resource and performer-slot/cardinality comparison |
| `base\quest\side_quests\sq011\scenes\sq011_09_nancy_call.scene` | Holocall scene invocation, entry/exit, and quest handoff comparison |
| `base\open_world\minor_activities\westbrook\japantown\ma_wbr_jpn_13\community\ma_wbr_jpn_013_claws_com.community` | Generic Tyger Claw entries, phases, appearances, time periods, quantities, and AI-spot references |
| `ep1\characters\entities\gang\gang__ep1_tyger_wa.ent` | Entity-template appearance mappings exposed by the focused `Character.*` record inheritance chain |
| `base\characters\appearances\gang\gang__tyger_wa.app` | Internal appearance definitions selected by the focused entity's exposed mapping; not a portable appearance template |
| `base\workspots\common\ground\generic__stand_ground_cigarette__smoke__01.workspot` | The stationary workspot byte-bound to the retained generic-character research lineage used by Lab 5 |
| `base\workspots\common\ground\generic__stand_ground__guard__02.workspot` | A different standing-guard lineage; do not substitute it for the cigarette mapping without new evidence |
| `base\workspots\common\wall\generic__stand_wall_lean_left__stand_around__01.workspot` | A scene-referenced wall-lean workspot used to distinguish workspot acquisition from direct animation events |
| `base\workspots\patrolling\guard_stand.workspot` | Finite-patrol research only; not a universal guard workspot |
| `base\animations\facial\generic\interactive_scene\generic_facial_lipsync_gestures.anims` | Generic scene lipsync resource row and slot-cardinality comparison, not proof of facial quality |

Keep actor ID, performer ID, screenplay item ID, localization RUID, event ID,
community identity, AI-spot identity, NodeRef, and CR2W handle separate while
recording a comparison.

## Braindance resources

| Depot path | Focused question |
| --- | --- |
| `base\quest\side_quests\sq012\scenes\sq012_02a_braindance.scene` | Rewindable section, RID handlers/references, support props, layered clue events, entry/exit, and interruption ownership |
| `base\animations\quest\side_quests\sq012\sq012_braindance\rid\sq012_braindance__part_a.scenerid` | Version-5 RID actor/camera tags, body/facial/cyberware channels, serials, cardinalities, and compressed buffers |
| `base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdview.ent` | BD-view entity template selected through a scene prop record and global spawn marker |
| `base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdfog.ent` | BD-fog entity template selected through a separate scene prop record |
| `base\quest\side_quests\sq012\entities\sq012_02a_braindance_bdsetup.ent` | Render-to-texture BD-setup entity template selected through a separate scene prop record |
| `base\quest\main_quests\prologue\q004\scenes\q004_05_bd_yorinobu.scene` | Larger main-quest rewindable scene with visual/audio/thermal conditions, clue discovery, RID playback, visibility, and BD action management |
| `base\quest\main_quests\prologue\q004\phases\q004_braindance.questphase` | Quest-side setup/teardown decomposition around the Q004 braindance; not a self-contained custom-scene template |
| `engine\scenesystem\camera.ent` | Scene-camera entity shape used for a placed RID-camera comparison; it does not supply a candidate's world placement |

## World, placement, and devices

| Depot path | Focused question |
| --- | --- |
| `base\worlds\03_night_city\_compiled\default\03_night_city.streamingworld` | Global Night City resource roots and compiled block ownership |
| `base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock` | Sector descriptors, categories, bounds, levels, and quest-prefab roots |
| `base\worlds\03_night_city\_compiled\default\quest_606b61008df2ba6f.streamingsector` | Focused Quest-sector nodes, placements, NodeRefs, trigger data, and prefab namespace |
| `base\worlds\03_night_city\_compiled\default\always_loaded_0.streamingsector` | AlwaysLoaded references and marker-related content without assuming compact array pairing |
| `base\worlds\03_night_city\_compiled\default\exterior_-18_28_0_0.streamingsector` | Ambient terminal placement comparison |
| `base\worlds\03_night_city\_compiled\default\bd21168eed6c6d62.streamingsector_inplace` | Separate inplace payload associated with that focused terminal placement |
| `base\worlds\03_night_city\_compiled\default\exterior_-17_22_0_0.streamingsector` | Allen Street fast-travel terminal placement, transform, entity template, and NodeRef chain |
| `base\worlds\03_night_city\_compiled\default\always_loaded_1.streamingsector` | Allen Street destination-marker registration and placement |
| `base\gameplay\devices\fast_travel\data_term_1.ent` | Entity template used by the focused fast-travel placement |
| `base\worlds\03_night_city\_compiled\default\exterior_19_-8_0_0.streamingsector` | Placed laptop node data, entity template, instance data, and cooked prefab link |
| `base\worlds\03_night_city\_compiled\default\4fd0915183681e53.streamingsector_inplace` | What the laptop placement's separate inplace resource embeds and omits |
| `base\gameplay\devices\drop_points\drop_point.ent` | Drop-point components and local UI/navigation slots |
| `base\gameplay\devices\masters\computers\laptop_1.ent` | Base computer components, controller package, and interaction/workspot ownership used by focused laptop comparisons |
| `base\worlds\03_night_city\_compiled\default\03_night_city.devices` | Focused lookup of a device identity in the global device registry |

World identities and transforms are not portable guarantees. Reusing a
vanilla location still requires measured geometry, streaming tests, collision
and navmesh checks, and save-aware device/community acceptance.

## Provenance boundary

The focused quest-block corpus was retained in Ghostline research commit
`29066f7b76ad4b7435b3fa2a7c0b20ecea464b5e`. Its README summarizes focused
base-game archive extraction across 2026-07-23 and 2026-07-24; the manifest at
that commit records the 2026-07-24 corpus state. Later research supplied the
scene, community, and world comparisons used by the book.

That provenance is not one fully bound Cyberpunk `2.31a` acceptance record.
Treat every row as **Observed in vanilla**, then re-extract the named resource
from the pinned installation before depending on version-sensitive fields.
Ghostline remains research input only; readers do not need it.

For every focused inspection, record:

1. the exact depot path and installed game build;
2. the root type and only the fields or graph edges needed to answer the
   question;
3. the identifier domains and external dependencies involved;
4. whether the shape was observed once or across multiple resources;
5. what the observation does *not* prove.

Do not commit extracted vanilla CR2Ws, complete serialized resources, or
assets derived by copying their payloads. Cite the depot path and teach the
reader how to reproduce the inspection.
