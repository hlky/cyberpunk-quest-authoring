#!/usr/bin/env python3
"""Build the native resource set for Lab 5 First Contact.

The voice source and prebuilt WEM are separately pinned binary assets. This
generator builds their scene and localization references; it does not claim
that Wwise conversion is byte reproducible. This is documentation-author
infrastructure, not a reader prerequisite.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from build_lab01_sources import (  # noqa: E402
    GraphBuilder,
    GraphNode,
    Handles,
    cname,
    fact_condition_node,
    input_node,
    journal_entry,
    journal_node,
    journal_path,
    localized_string,
    output_node,
    set_fact_node,
    write_json,
)
from build_lab03_sources import (  # noqa: E402
    descriptor,
    entity_reference,
    marker_node,
    node_data,
    node_ref,
    resource_path,
    trigger_condition_node,
    trigger_node,
)


ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = ROOT / "examples" / "lab-05-first-contact"
CHECKPOINTS = {
    "start": LAB_ROOT / "start",
    "completed": LAB_ROOT / "completed",
}
DEPOT_ROOT = Path("mod") / "cqa" / "cqa005"

ROOT_PHASE_PATH = "mod\\cqa\\cqa005\\phases\\cqa005.questphase"
CHILD_PHASE_PATH = "mod\\cqa\\cqa005\\phases\\cqa005_contact.questphase"
SCENE_PATH = "mod\\cqa\\cqa005\\scenes\\cqa005_first_contact.scene"
JOURNAL_PATH = "mod\\cqa\\cqa005\\journal\\cqa005.journal"
ONSCREEN_PATH = (
    "mod\\cqa\\cqa005\\localization\\en-us\\onscreens\\cqa005_onscreens.json"
)
SUBTITLES_PATH = (
    "mod\\cqa\\cqa005\\localization\\en-us\\subtitles\\cqa005_subtitles.json"
)
SUBTITLE_MAP_PATH = (
    "mod\\cqa\\cqa005\\localization\\en-us\\subtitles\\"
    "cqa005_subtitles_map.json"
)
VOICE_MAP_PATH = (
    "mod\\cqa\\cqa005\\localization\\en-us\\vo\\cqa005_vo.json"
)
VOICE_WEM_PATH = (
    "mod\\cqa\\cqa005\\localization\\en-us\\vo\\"
    "contact_i_85c3283507e7ef2f.wem"
)
BLOCK_PATH = (
    "mod\\cqa\\cqa005\\world\\cqa005_first_contact.streamingblock"
)
QUEST_SECTOR_PATH = (
    "mod\\cqa\\cqa005\\world\\cqa005_first_contact.streamingsector"
)
ALWAYS_SECTOR_PATH = (
    "mod\\cqa\\cqa005\\world\\cqa005_always_loaded.streamingsector"
)

QUEST_JOURNAL_PATH = "quests/minor_quest/cqa005"
PHASE_JOURNAL_PATH = f"{QUEST_JOURNAL_PATH}/cqa005_01"
MEET_JOURNAL_PATH = f"{PHASE_JOURNAL_PATH}/cqa005_01_obj_meet"
LEAVE_JOURNAL_PATH = f"{PHASE_JOURNAL_PATH}/cqa005_01_obj_leave"
MAPPIN_JOURNAL_PATH = f"{MEET_JOURNAL_PATH}/cqa005_01_qmp_contact"

PREFAB_LOCAL = "#cqa005_pr_first_contact"
PREFAB_FULL = "$/mod/cqa/cqa005/#cqa005_pr_first_contact"
SETUP_LOCAL = "#cqa005_tr_setup"
CLEANUP_LOCAL = "#cqa005_tr_cleanup"
COMMUNITY_LOCAL = "#cqa005_com_contact"
AI_SPOT_LOCAL = "#cqa005_spot_contact"
SCENE_MARKER_LOCAL = "#cqa005_sm_contact"
MAPPIN_LOCAL = "#cqa005_mp_contact"
SETUP_FULL = f"{PREFAB_FULL}/{SETUP_LOCAL}"
CLEANUP_FULL = f"{PREFAB_FULL}/{CLEANUP_LOCAL}"
COMMUNITY_FULL = f"{PREFAB_FULL}/{COMMUNITY_LOCAL}"
AI_SPOT_FULL = f"{PREFAB_FULL}/{AI_SPOT_LOCAL}"
SCENE_MARKER_FULL = f"{PREFAB_FULL}/{SCENE_MARKER_LOCAL}"
MAPPIN_FULL = f"{PREFAB_FULL}/{MAPPIN_LOCAL}"

CONTACT_ENTRY = "contact"
CONTACT_PHASE = "default"
CONTACT_CHARACTER = "Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa"
CONTACT_APPEARANCE = "default"
CONTACT_WORKSPOT = (
    "base\\workspots\\common\\ground\\"
    "generic__stand_ground_cigarette__smoke__01.workspot"
)

CONTACT_LINE_KEY = "cqa005_contact_line_0001"
CONTACT_LINE_TEXT = "All clear. Keep moving."
CONTACT_LINE_RUID = "9638591835734011695"
CONTACT_LINE_ITEM_ID = 1
CONTACT_LINE_DURATION_MS = 2598
SCENE_START_NODE_ID = 1
SCENE_SECTION_NODE_ID = 2
SCENE_END_NODE_ID = 3
SCENE_AI_NODE_ID = 4

CENTER = (-1000.02, 1497.2208, 8.3)
SETUP_POSITION = (-1000.02, 1497.2208, 2.3)
CLEANUP_POSITION = (-1000.02, 1497.2208, 0.3)
CONTACT_POSITION = (-1000.02, 1497.2208, 6.957)
YAW = 88.6
SETUP_RADIUS = 25
CLEANUP_RADIUS = 110


def fnv1a64(value: str) -> str:
    result = 0xCBF29CE484222325
    for octet in value.encode("utf-8"):
        result ^= octet
        result = (result * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return str(result)


def node_ref_hash(value: str) -> int:
    """Match RED4 NodeRef hashing while skipping inline alias markers."""

    if not value:
        return 0
    result = 0xCBF29CE484222325
    index = 0
    while index < len(value):
        if value[index] == "#":
            index += 1
            if index < len(value) and value[index] == ";":
                next_slash = value.find("/", index)
                index = len(value) if next_slash == -1 else next_slash
        if index >= len(value):
            break
        result ^= ord(value[index])
        result = (result * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
        index += 1
    return result


def scene_actor_id(value: int) -> dict[str, int | str]:
    return {"$type": "scnActorId", "id": value}


def scene_performer_id(value: int) -> dict[str, int | str]:
    return {"$type": "scnPerformerId", "id": value}


def scene_node_id(value: int) -> dict[str, int | str]:
    return {"$type": "scnNodeId", "id": value}


def screenplay_item_id(value: int) -> dict[str, int | str]:
    return {"$type": "scnscreenplayItemId", "id": value}


def locstring_id(value: str) -> dict[str, str]:
    return {"$type": "scnlocLocstringId", "ruid": value}


def scene_time(value: int) -> dict[str, int | str]:
    return {"$type": "scnSceneTime", "stu": value}


def scene_input_socket(
    node_id_value: int,
    name: int = 0,
    ordinal: int = 0,
) -> dict[str, Any]:
    return {
        "$type": "scnInputSocketId",
        "isockStamp": {
            "$type": "scnInputSocketStamp",
            "name": name,
            "ordinal": ordinal,
        },
        "nodeId": scene_node_id(node_id_value),
    }


def scene_output_socket(
    destinations: list[tuple[int, int, int]],
    *,
    name: int = 0,
    ordinal: int = 0,
) -> dict[str, Any]:
    return {
        "$type": "scnOutputSocket",
        "destinations": [
            scene_input_socket(node, input_name, input_ordinal)
            for node, input_name, input_ordinal in destinations
        ],
        "stamp": {
            "$type": "scnOutputSocketStamp",
            "name": name,
            "ordinal": ordinal,
        },
    }


def json_resource_document(
    archive_path: str,
    root_type: str,
    **properties: Any,
) -> dict[str, Any]:
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": archive_path,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "JsonResource",
                "cookingPlatform": "PLATFORM_PC",
                "root": Handles.define(
                    "0",
                    {"$type": root_type, **properties},
                ),
            },
            "EmbeddedFiles": [],
        },
    }


COMMUNITY_SOURCE_ID = str(node_ref_hash(COMMUNITY_FULL))
REGISTRY_NODE_ID = str(node_ref_hash(f"{COMMUNITY_FULL}_registry"))
AI_SPOT_GLOBAL_ID = str(node_ref_hash(AI_SPOT_FULL))


def external_phase_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    return builder.node(
        quest_id,
        "questPhaseNodeDefinition",
        inputs=("In1",),
        outputs=("Out1",),
        properties={
            "phaseGraph": None,
            "phaseInstancePrefabs": [],
            "phaseResource": resource_path(CHILD_PHASE_PATH),
            "saveLock": 0,
            "unfreezingTriggerNodeRef": node_ref(0),
        },
    )


def mappin_node(
    builder: GraphBuilder,
    quest_id: int,
    *,
    disable_previous: int,
) -> GraphNode:
    return builder.node(
        quest_id,
        "questMappinManagerNodeDefinition",
        inputs=("Active", "Inactive"),
        properties={
            "disablePreviousMappins": disable_previous,
            "path": journal_path(
                builder,
                MAPPIN_JOURNAL_PATH,
                "gameJournalQuestMapPin",
            ),
        },
    )


def community_node(
    builder: GraphBuilder,
    quest_id: int,
    action: str,
    entry: str,
    phase: str,
) -> GraphNode:
    action_type = builder.handles.wrap(
        {
            "$type": "questCommunityTemplate_NodeType",
            "action": action,
            "communityEntryName": cname(entry),
            "communityEntryPhaseName": cname(phase),
            "spawnerReference": node_ref(COMMUNITY_LOCAL),
        }
    )
    return builder.node(
        quest_id,
        "questSpawnManagerNodeDefinition",
        inputs=("In",),
        properties={
            "actions": [
                {
                    "$type": "questSpawnManagerNodeActionEntry",
                    "type": action_type,
                }
            ]
        },
    )


def character_spawned_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    comparison = builder.handles.wrap(
        {
            "$type": "questComparisonParam",
            "comparisonType": "Greater",
            "count": 0,
            "entireCommunity": 1,
        }
    )
    spawned = builder.handles.wrap(
        {
            "$type": "questCharacterSpawned_ConditionType",
            "comparisonParams": comparison,
            "objectRef": {
                **entity_reference(),
                "reference": node_ref(COMMUNITY_LOCAL),
            },
        }
    )
    condition = builder.handles.wrap(
        {"$type": "questCharacterCondition", "type": spawned}
    )
    return builder.node(
        quest_id,
        "questPauseConditionNodeDefinition",
        inputs=("In",),
        properties={"condition": condition},
    )


def checkpoint_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    return builder.node(
        quest_id,
        "questCheckpointNodeDefinition",
        inputs=("In",),
        properties={
            "additionalEndGameRewardsTweak": [],
            "debugString": "cqa005_first_contact",
            "endGameSave": 0,
            "ignoreSaveLocks": 0,
            "pointOfNoReturn": 0,
            "retryOnFailure": 0,
            "saveLock": 0,
        },
    )


def scene_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    return builder.node(
        quest_id,
        "questSceneNodeDefinition",
        inputs=("start",),
        outputs=("contact_done", "Default INT", "Default RET"),
        properties={
            "interruptionOperations": [],
            "notAllowedToBeFrozen": 0,
            "reapplyInterruptionOperationsAfterGameLoad": 0,
            "sceneFile": resource_path(SCENE_PATH),
            "sceneLocation": {
                "$type": "scnWorldMarker",
                "nodeRef": node_ref(SCENE_MARKER_LOCAL),
                "tag": cname("None"),
                "type": "NodeRef",
            },
            "syncToMusic": 0,
        },
    )


def phase_document(
    builder: GraphBuilder,
    archive_path: str,
    *,
    prefabs: list[str],
) -> dict[str, Any]:
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": archive_path,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "questQuestPhaseResource",
                "cookingPlatform": "PLATFORM_PC",
                "graph": builder.graph,
                "inplacePhases": [],
                "phasePrefabs": [
                    {
                        "$type": "questQuestPrefabEntry",
                        "prefabNodeRef": node_ref(prefab),
                    }
                    for prefab in prefabs
                ],
            },
            "EmbeddedFiles": [],
        },
    }


def build_start_root_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    child = external_phase_node(builder, 13)
    builder.connect(phase_input, child, destination_socket="In1")
    builder.connect_to_output(child, phase_output, source_socket="Out1")
    return phase_document(builder, ROOT_PHASE_PATH, prefabs=[PREFAB_LOCAL])


def build_start_child_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    builder.connect(phase_input, phase_output)
    return phase_document(builder, CHILD_PHASE_PATH, prefabs=[])


def build_completed_root_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    completed_guard = fact_condition_node(builder, 10, "cqa005_completed")
    quest_active = journal_node(
        builder,
        11,
        QUEST_JOURNAL_PATH,
        "gameJournalQuest",
    )
    child = external_phase_node(builder, 12)
    quest_succeeded = journal_node(
        builder,
        13,
        QUEST_JOURNAL_PATH,
        "gameJournalQuest",
    )
    completed_fact = set_fact_node(builder, 14, "cqa005_completed")

    builder.connect(phase_input, completed_guard)
    builder.connect(
        completed_guard,
        quest_active,
        source_socket="True",
        destination_socket="Active",
    )
    builder.connect(
        quest_active,
        child,
        destination_socket="In1",
    )
    builder.connect(
        child,
        quest_succeeded,
        source_socket="Out1",
        destination_socket="Succeeded",
    )
    builder.connect(quest_succeeded, completed_fact)
    builder.connect_to_output(completed_fact, phase_output)
    builder.connect_to_output(
        completed_guard,
        phase_output,
        source_socket="False",
    )
    return phase_document(builder, ROOT_PHASE_PATH, prefabs=[PREFAB_LOCAL])


def build_completed_child_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    meet_active = journal_node(
        builder,
        10,
        MEET_JOURNAL_PATH,
        "gameJournalQuestObjective",
    )
    pin_active = mappin_node(builder, 11, disable_previous=0)
    activate_contact = community_node(
        builder,
        12,
        "Activate",
        CONTACT_ENTRY,
        CONTACT_PHASE,
    )
    spawned = character_spawned_node(builder, 13)
    setup = trigger_condition_node(builder, 14, SETUP_LOCAL, "IsInside")
    checkpoint = checkpoint_node(builder, 15)
    scene = scene_node(builder, 16)
    meet_succeeded = journal_node(
        builder,
        17,
        MEET_JOURNAL_PATH,
        "gameJournalQuestObjective",
    )
    pin_inactive = mappin_node(builder, 18, disable_previous=0)
    leave_active = journal_node(
        builder,
        19,
        LEAVE_JOURNAL_PATH,
        "gameJournalQuestObjective",
    )
    cleanup = trigger_condition_node(builder, 20, CLEANUP_LOCAL, "IsOutside")
    deactivate_contact = community_node(
        builder,
        21,
        "Deactivate",
        "None",
        "None",
    )
    leave_succeeded = journal_node(
        builder,
        22,
        LEAVE_JOURNAL_PATH,
        "gameJournalQuestObjective",
    )

    builder.connect(phase_input, meet_active, destination_socket="Active")
    builder.connect(meet_active, pin_active, destination_socket="Active")
    builder.connect(pin_active, activate_contact)
    builder.connect(activate_contact, spawned)
    builder.connect(spawned, setup)
    builder.connect(setup, checkpoint)
    builder.connect(checkpoint, scene, destination_socket="start")
    builder.connect(
        scene,
        meet_succeeded,
        source_socket="contact_done",
        destination_socket="Succeeded",
    )
    builder.connect(
        meet_succeeded,
        pin_inactive,
        destination_socket="Inactive",
    )
    builder.connect(pin_inactive, leave_active, destination_socket="Active")
    builder.connect(leave_active, cleanup)
    builder.connect(cleanup, deactivate_contact)
    builder.connect(
        deactivate_contact,
        leave_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect_to_output(leave_succeeded, phase_output)
    return phase_document(builder, CHILD_PHASE_PATH, prefabs=[])


def journal_mappin() -> dict[str, Any]:
    return Handles.define(
        "6",
        journal_entry(
            "gameJournalQuestMapPin",
            "cqa005_01_qmp_contact",
            [],
            enableGPS=1,
            mappinData={
                "$type": "gamemappinsMappinData",
                "active": 0,
                "debugCaption": "cqa_cqa005_mappin_contact",
                "localizedCaption": localized_string(
                    "cqa_cqa005_mappin_contact"
                ),
                "mappinType": {
                    "$type": "TweakDBID",
                    "$storage": "string",
                    "$value": "Mappins.QuestStaticMappinDefinition",
                },
                "scriptData": None,
                "variant": "DefaultQuestVariant",
                "visibleThroughWalls": 1,
            },
            offset={"$type": "Vector3", "X": 0, "Y": 0, "Z": 0.5},
            reference={
                **entity_reference(),
                "reference": node_ref(MAPPIN_LOCAL),
            },
        ),
    )


def objective(
    handle_id: str,
    entry_id: str,
    localization_key: str,
    entries: list[dict[str, Any]],
) -> dict[str, Any]:
    return Handles.define(
        handle_id,
        journal_entry(
            "gameJournalQuestObjective",
            entry_id,
            entries,
            counter=0,
            description=localized_string(localization_key),
            districtID="",
            itemID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            locationPrefabRef=node_ref(0),
            optional=0,
        ),
    )


def build_journal() -> dict[str, Any]:
    meet = objective(
        "5",
        "cqa005_01_obj_meet",
        "cqa_cqa005_objective_meet",
        [journal_mappin()],
    )
    leave = objective(
        "7",
        "cqa005_01_obj_leave",
        "cqa_cqa005_objective_leave",
        [],
    )
    phase = Handles.define(
        "4",
        journal_entry(
            "gameJournalQuestPhase",
            "cqa005_01",
            [meet, leave],
            locationPrefabRef=node_ref(0),
        ),
    )
    quest = Handles.define(
        "3",
        journal_entry(
            "gameJournalQuest",
            "cqa005",
            [phase],
            districtID="",
            recommendedLevelID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            title=localized_string("cqa_cqa005_title"),
            type="MinorQuest",
        ),
    )
    minor_quest = Handles.define(
        "2",
        journal_entry("gameJournalFolderEntry", "minor_quest", [quest]),
    )
    quests = Handles.define(
        "1",
        journal_entry("gameJournalPrimaryFolderEntry", "quests", [minor_quest]),
    )
    root = Handles.define(
        "0",
        {
            "$type": "gameJournalRootFolderEntry",
            "descriptor": resource_path("base\\journal\\descriptor.journaldesc"),
            "entries": [quests],
        },
    )
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": JOURNAL_PATH,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "gameJournalResource",
                "cookingPlatform": "PLATFORM_PC",
                "entry": root,
            },
            "EmbeddedFiles": [],
        },
    }


def build_onscreen_localization() -> dict[str, Any]:
    strings = {
        "cqa_cqa005_title": "First Contact",
        "cqa_cqa005_objective_meet": "Meet the contact.",
        "cqa_cqa005_objective_leave": "Leave the meeting area.",
        "cqa_cqa005_mappin_contact": "First Contact",
    }
    entries = [
        {
            "$type": "localizationPersistenceOnScreenEntry",
            "femaleVariant": text,
            "maleVariant": "",
            "primaryKey": "0",
            "secondaryKey": key,
        }
        for key, text in strings.items()
    ]
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": ONSCREEN_PATH,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "JsonResource",
                "cookingPlatform": "PLATFORM_PC",
                "root": Handles.define(
                    "0",
                    {
                        "$type": "localizationPersistenceOnScreenEntries",
                        "entries": entries,
                    },
                ),
            },
            "EmbeddedFiles": [],
        },
    }


def scene_entity_reference(
    reference: str | int = 0,
    *,
    names: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "$type": "gameEntityReference",
        "dynamicEntityUniqueName": cname("None"),
        "names": [cname(name) for name in names],
        "reference": node_ref(reference),
        "sceneActorContextName": cname("None"),
        "slotName": cname("None"),
        "type": "EntityRef",
    }


def build_scene_actor() -> dict[str, Any]:
    return {
        "$type": "scnActorDef",
        "acquisitionPlan": "community",
        "actorId": scene_actor_id(0),
        "actorName": "contact",
        "animSets": [],
        "bodyCinematicAnimSets": [],
        "communityParams": {
            "$type": "scnCommunityParams",
            "entryName": cname(CONTACT_ENTRY),
            "forceMaxVisibility": 0,
            "reference": node_ref(COMMUNITY_LOCAL),
        },
        "cyberwareAnimSets": [],
        "cyberwareCinematicAnimSets": [],
        "deformationAnimSets": [],
        "dynamicAnimSets": [],
        "facialAnimSets": [],
        "facialCinematicAnimSets": [],
        "findActorInContextParams": {
            "$type": "scnFindEntityInContextParams",
            "contextActorName": cname("None"),
            "contextualName": "Player",
            "forceMaxVisibility": 0,
            "specRecordId": tweakdbid_uint64(0),
            "voiceVagId": {"$type": "scnVoicetagId", "id": "0"},
        },
        "findActorInWorldParams": {
            "$type": "scnFindEntityInWorldParams",
            "actorRef": scene_entity_reference(),
            "forceMaxVisibility": 0,
        },
        "holocallInitScn": resource_path(0),
        "lipsyncAnimSet": {
            "$type": "scnLipsyncAnimSetSRRefId",
            "id": 0,
        },
        "spawnDespawnParams": {
            "$type": "scnSpawnDespawnEntityParams",
            "alwaysSpawned": 0,
            "appearance": cname("None"),
            "dynamicEntityUniqueName": cname("None"),
            "findInWorld": 0,
            "forceMaxVisibility": 0,
            "isEnabled": 1,
            "itemOwnerId": scene_performer_id(4294967040),
            "keepAlive": 0,
            "prefetchAppearance": 0,
            "spawnMarker": cname("None"),
            "spawnMarkerNodeRef": node_ref(0),
            "spawnMarkerType": "Local",
            "spawnOffset": {
                "$type": "Transform",
                "orientation": {
                    "$type": "Quaternion",
                    "i": 0,
                    "j": 0,
                    "k": 0,
                    "r": 1,
                },
                "position": {
                    "$type": "Vector4",
                    "W": 0,
                    "X": 0,
                    "Y": 0,
                    "Z": 0,
                },
            },
            "spawnOnStart": 1,
            "specRecordId": tweakdbid_uint64(0),
            "validateSpawnPostion": 1,
        },
        "spawnerParams": {
            "$type": "scnSpawnerParams",
            "forceMaxVisibility": 0,
            "reference": node_ref(0),
        },
        "spawnSetParams": {
            "$type": "scnSpawnSetParams",
            "entryName": cname("None"),
            "forceMaxVisibility": 0,
            "reference": node_ref(0),
        },
        "specAppearance": cname(CONTACT_APPEARANCE),
        "specCharacterRecordId": tweakdbid_uint64(0),
        "voicetagId": {"$type": "scnVoicetagId", "id": "0"},
    }


def tweakdbid_uint64(value: int) -> dict[str, str]:
    return {"$type": "TweakDBID", "$storage": "uint64", "$value": str(value)}


def build_scene_player_actor() -> dict[str, Any]:
    player_record = "Character.Player_Puppet_Base"
    return {
        "$type": "scnPlayerActorDef",
        "acquisitionPlan": "findInContext",
        "actorId": scene_actor_id(1),
        "animSets": [],
        "bodyCinematicAnimSets": [],
        "cyberwareAnimSets": [],
        "cyberwareCinematicAnimSets": [],
        "deformationAnimSets": [],
        "dynamicAnimSets": [],
        "facialAnimSets": [],
        "facialCinematicAnimSets": [],
        "findActorInContextParams": {
            "$type": "scnFindEntityInContextParams",
            "contextActorName": cname("None"),
            "contextualName": "Player",
            "forceMaxVisibility": 0,
            "specRecordId": tweakdbid(player_record),
            "voiceVagId": {"$type": "scnVoicetagId", "id": "0"},
        },
        "findNetworkPlayerParams": {
            "$type": "scnFindNetworkPlayerParams",
            "networkId": 0,
        },
        "lipsyncAnimSet": {
            "$type": "scnLipsyncAnimSetSRRefId",
            "id": 0,
        },
        "playerName": "V",
        "specAppearance": cname("default"),
        "specCharacterRecordId": tweakdbid(player_record),
        "specTemplate": cname("(None)"),
        "voicetagId": {
            "$type": "scnVoicetagId",
            "id": "1103967280742240864",
        },
    }


def build_scene_debug_symbols() -> dict[str, Any]:
    return {
        "$type": "scnDebugSymbols",
        "performersDebugSymbols": [
            {
                "$type": "scnPerformerSymbol",
                "editorPerformerId": "0",
                "entityRef": scene_entity_reference(
                    COMMUNITY_LOCAL,
                    names=(CONTACT_ENTRY,),
                ),
                "performerId": scene_performer_id(1),
            },
            {
                "$type": "scnPerformerSymbol",
                "editorPerformerId": "0",
                "entityRef": scene_entity_reference("#player"),
                "performerId": scene_performer_id(257),
            },
        ],
        "sceneEventsDebugSymbols": [],
        "sceneNodesDebugSymbols": [],
        "workspotsDebugSymbols": [],
    }


def build_interruption_scenarios() -> list[dict[str, Any]]:
    return [
        {
            "$type": "scnInterruptionScenario",
            "enabled": 1,
            "forcePlayReturnLine": 0,
            "id": {"$type": "scnInterruptionScenarioId", "id": 0},
            "interruptConditions": [
                Handles.define(
                    "0",
                    {
                        "$type": "scnCheckSpeakersDistanceInterruptCondition",
                        "params": {
                            "$type": (
                                "scnCheckSpeakersDistanceInterruptConditionParams"
                            ),
                            "comparisonType": "Greater",
                            "distance": 6,
                        },
                    },
                )
            ],
            "interruptionSpammingSafeguard": 0,
            "name": cname("Default"),
            "playingLinesBehavior": "Default",
            "playInterruptLine": 1,
            "postInterruptSignalFactCondition": None,
            "postInterruptSignalTimeDelay": 0,
            "postReturnSignalFactCondition": None,
            "postReturnSignalTimeDelay": 0,
            "queueName": cname("None"),
            "returnConditions": [
                Handles.define(
                    "1",
                    {
                        "$type": "scnCheckSpeakersDistanceReturnCondition",
                        "params": {
                            "$type": (
                                "scnCheckSpeakersDistanceReturnConditionParams"
                            ),
                            "comparisonType": "Less",
                            "distance": 5,
                        },
                    },
                )
            ],
            "talkOnReturn": 1,
        }
    ]


def scene_quest_socket(
    handles: Handles,
    name: str,
    socket_type: str,
) -> dict[str, Any]:
    return handles.wrap(
        {
            "$type": "questSocketDefinition",
            "connections": [],
            "name": cname(name),
            "type": socket_type,
        }
    )


def build_scene_graph(completed: bool) -> dict[str, Any]:
    handles = Handles()
    handles.reserve()
    handles.reserve()
    scene_graph_handle = handles.reserve()

    if not completed:
        start = handles.wrap(
            {
                "$type": "scnStartNode",
                "ffStrategy": "automatic",
                "nodeId": scene_node_id(SCENE_START_NODE_ID),
                "outputSockets": [
                    scene_output_socket(
                        [(SCENE_END_NODE_ID, 0, 0)],
                    )
                ],
            }
        )
        end = handles.wrap(
            {
                "$type": "scnEndNode",
                "ffStrategy": "automatic",
                "nodeId": scene_node_id(SCENE_END_NODE_ID),
                "outputSockets": [],
                "type": "Terminating",
            }
        )
        return Handles.define(
            scene_graph_handle,
            {
                "$type": "scnSceneGraph",
                "endNodes": [scene_node_id(SCENE_END_NODE_ID)],
                "graph": [start, end],
                "startNodes": [scene_node_id(SCENE_START_NODE_ID)],
            },
        )

    start = handles.wrap(
        {
            "$type": "scnStartNode",
            "ffStrategy": "automatic",
            "nodeId": scene_node_id(SCENE_START_NODE_ID),
            "outputSockets": [
                scene_output_socket(
                    [
                        (SCENE_SECTION_NODE_ID, 0, 0),
                        (SCENE_AI_NODE_ID, 0, 1),
                    ]
                )
            ],
        }
    )
    event = handles.wrap(
        {
            "$type": "scnDialogLineEvent",
            "additionalSpeakers": {
                "$type": "scnAdditionalSpeakers",
                "executionTag": 0,
                "role": "Full",
                "speakers": [],
            },
            "duration": CONTACT_LINE_DURATION_MS,
            "executionTagFlags": 0,
            "id": {
                "$type": "scnSceneEventId",
                "id": fnv1a64(
                    "CQA_Lab05_FirstContact:contact:"
                    f"{CONTACT_LINE_KEY}:{CONTACT_LINE_ITEM_ID}"
                ),
            },
            "scalingData": None,
            "screenplayLineId": screenplay_item_id(CONTACT_LINE_ITEM_ID),
            "startTime": 0,
            "type": "0",
            "visualStyle": "regular",
            "voParams": {
                "$type": "scnDialogLineVoParams",
                "alwaysUseBrainGender": 0,
                "customVoEvent": cname("None"),
                "disableHeadMovement": 0,
                "ignoreSpeakerIncapacitation": 0,
                "isHolocallSpeaker": 0,
                "voContext": "Vo_Context_Quest",
                "voExpression": "Vo_Expression_Spoken",
            },
        }
    )
    section = handles.wrap(
        {
            "$type": "scnSectionNode",
            "actorBehaviors": [
                {
                    "$type": "scnSectionInternalsActorBehavior",
                    "actorId": scene_actor_id(actor),
                    "behaviorMode": "OnlyIfAlive",
                }
                for actor in (0, 1)
            ],
            "events": [event],
            "ffStrategy": "automatic",
            "isFocusClue": 0,
            "nodeId": scene_node_id(SCENE_SECTION_NODE_ID),
            "outputSockets": [
                scene_output_socket([(SCENE_END_NODE_ID, 0, 0)]),
                scene_output_socket([], name=1),
            ],
            "sectionDuration": scene_time(CONTACT_LINE_DURATION_MS + 400),
        }
    )
    quest_node = handles.wrap(
        {
            "$type": "questPuppetAIManagerNodeDefinition",
            "id": SCENE_AI_NODE_ID,
            "sockets": [],
        }
    )
    quest_node["Data"]["entries"] = [
        {
            "$type": "questPuppetAIManagerNodeDefinitionEntry",
            "aiTier": "Cinematic",
            "entityReference": scene_entity_reference(
                COMMUNITY_LOCAL,
                names=(CONTACT_ENTRY,),
            ),
        }
    ]
    quest_node["Data"]["sockets"] = [
        scene_quest_socket(handles, "CutDestination", "CutDestination"),
        scene_quest_socket(handles, "In", "Input"),
        scene_quest_socket(handles, "Out", "Output"),
    ]
    ai_manager = handles.wrap(
        {
            "$type": "scnQuestNode",
            "ffStrategy": "automatic",
            "isockMappings": [cname("CutDestination"), cname("In")],
            "nodeId": scene_node_id(SCENE_AI_NODE_ID),
            "osockMappings": [cname("Out")],
            "outputSockets": [scene_output_socket([])],
            "questNode": quest_node,
        }
    )
    end = handles.wrap(
        {
            "$type": "scnEndNode",
            "ffStrategy": "automatic",
            "nodeId": scene_node_id(SCENE_END_NODE_ID),
            "outputSockets": [],
            "type": "Terminating",
        }
    )
    return Handles.define(
        scene_graph_handle,
        {
            "$type": "scnSceneGraph",
            "endNodes": [scene_node_id(SCENE_END_NODE_ID)],
            "graph": [start, section, ai_manager, end],
            "startNodes": [scene_node_id(SCENE_START_NODE_ID)],
        },
    )


def build_scene(completed: bool) -> dict[str, Any]:
    screenplay_lines: list[dict[str, Any]] = []
    if completed:
        screenplay_lines.append(
            {
                "$type": "scnscreenplayDialogLine",
                "addressee": scene_actor_id(1),
                "femaleLipsyncAnimationName": cname("None"),
                "itemId": screenplay_item_id(CONTACT_LINE_ITEM_ID),
                "locstringId": locstring_id(CONTACT_LINE_RUID),
                "maleLipsyncAnimationName": cname("None"),
                "speaker": scene_actor_id(0),
                "usage": {
                    "$type": "scnscreenplayLineUsage",
                    "playerGenderMask": {
                        "$type": "scnGenderMask",
                        "mask": 3,
                    },
                },
            }
        )
    root = {
        "$type": "scnSceneResource",
        "actors": [build_scene_actor()],
        "cookingPlatform": "PLATFORM_PC",
        "debugSymbols": build_scene_debug_symbols(),
        "effectDefinitions": [],
        "effectInstances": [],
        "entryPoints": [
            {
                "$type": "scnEntryPoint",
                "name": cname("start"),
                "nodeId": scene_node_id(SCENE_START_NODE_ID),
            }
        ],
        "executionTagEntries": [],
        "executionTags": [],
        "exitPoints": [
            {
                "$type": "scnExitPoint",
                "name": cname("contact_done"),
                "nodeId": scene_node_id(SCENE_END_NODE_ID),
            }
        ],
        "interruptionScenarios": build_interruption_scenarios(),
        "localMarkers": [],
        "locStore": {
            "$type": "scnlocLocStoreEmbedded",
            "vdEntries": [],
            "vpEntries": [],
        },
        "notablePoints": [],
        "playerActors": [build_scene_player_actor()],
        "props": [],
        "referencePoints": [],
        "resouresReferences": {
            "$type": "scnSRRefCollection",
            "cinematicAnimNames": [],
            "cinematicAnimSets": [],
            "dynamicAnimNames": [],
            "dynamicAnimSets": [],
            "gameplayAnimNames": [],
            "gameplayAnimSets": [],
            "lipsyncAnimSets": [
                {
                    "$type": "scnLipsyncAnimSetSRRef",
                    "asyncRefLipsyncAnimSet": resource_path(
                        "base\\animations\\facial\\generic\\interactive_scene\\"
                        "generic_facial_lipsync_gestures.anims"
                    ),
                    "lipsyncAnimSet": resource_path(0, flags="Default"),
                }
            ],
            "ridAnimationContainers": [],
            "ridAnimations": [],
            "ridAnimSets": [],
            "ridCameraAnimations": [],
            "ridCyberwareAnimSets": [],
            "ridDeformationAnimSets": [],
            "ridFacialAnimSets": [],
        },
        "ridResources": [],
        "sceneCategoryTag": "minorQuests",
        "sceneGraph": build_scene_graph(completed),
        "sceneSolutionHash": {
            "$type": "scnSceneSolutionHash",
            "sceneSolutionHash": {
                "$type": "scnSceneSolutionHashHash",
                "sceneSolutionHashDate": fnv1a64("CQA_Lab05_FirstContact"),
            },
        },
        "screenplayStore": {
            "$type": "scnscreenplayStore",
            "lines": screenplay_lines,
            "options": [],
        },
        "version": 5,
        "voInfo": [],
        "workspotInstances": [],
        "workspots": [],
    }
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": SCENE_PATH,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": root,
            "EmbeddedFiles": [],
        },
    }


def build_subtitles() -> dict[str, Any]:
    return json_resource_document(
        SUBTITLES_PATH,
        "localizationPersistenceSubtitleEntries",
        entries=[
            {
                "$type": "localizationPersistenceSubtitleEntry",
                "femaleVariant": CONTACT_LINE_TEXT,
                "maleVariant": CONTACT_LINE_TEXT,
                "stringId": CONTACT_LINE_RUID,
            }
        ],
    )


def build_subtitle_map() -> dict[str, Any]:
    return json_resource_document(
        SUBTITLE_MAP_PATH,
        "localizationPersistenceSubtitleMap",
        entries=[
            {
                "$type": "localizationPersistenceSubtitleMapEntry",
                "subtitleFile": resource_path(SUBTITLES_PATH),
                "subtitleGroup": cname("quest"),
            }
        ],
    )


def build_voiceover_map() -> dict[str, Any]:
    return json_resource_document(
        VOICE_MAP_PATH,
        "locVoiceoverMap",
        entries=[
            {
                "$type": "locVoLineEntry",
                "femaleResPath": resource_path(VOICE_WEM_PATH),
                "maleResPath": resource_path(VOICE_WEM_PATH),
                "stringId": CONTACT_LINE_RUID,
            }
        ],
    )


def global_node_id(value: str) -> dict[str, str]:
    return {"$type": "worldGlobalNodeID", "hash": value}


def tweakdbid(value: str) -> dict[str, str]:
    return {"$type": "TweakDBID", "$storage": "string", "$value": value}


def ai_spot_node(handles: Handles) -> dict[str, Any]:
    spot = handles.wrap(
        {
            "$type": "AIActionSpot",
            "ActorBodytypeE3": "Undefined",
            "clippingSpaceOrientation": 180.0,
            "clippingSpaceRange": 120.0,
            "enabledWhenMasterOccupied": 0,
            "masterNodeRef": node_ref(0),
            "resource": resource_path(CONTACT_WORKSPOT),
            "snapToGround": 0,
            "useClippingSpace": 0,
        }
    )
    return handles.wrap(
        {
            "$type": "worldAISpotNode",
            "crowdBlacklist": {"$type": "redTagList", "tags": []},
            "crowdWhitelist": {"$type": "redTagList", "tags": []},
            "debugName": cname("{cqa005_spot_contact}"),
            "disableBumps": 0,
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "isWorkspotInfinite": 1,
            "isWorkspotStatic": 0,
            "lookAtTarget": node_ref(0),
            "markings": [],
            "proxyScale": None,
            "sourcePrefabHash": "0",
            "spot": spot,
            "spotDef": None,
            "tag": "None",
            "tagExt": "None",
            "useCrowdBlacklist": 1,
            "useCrowdWhitelist": 1,
        }
    )


def community_area_node(handles: Handles) -> dict[str, Any]:
    area = handles.wrap(
        {
            "$type": "communityArea",
            "entriesData": [
                {
                    "$type": "communityCommunityEntrySpotsData",
                    "entryName": cname(CONTACT_ENTRY),
                    "phasesData": [
                        {
                            "$type": "communityCommunityEntryPhaseSpotsData",
                            "entryPhaseName": cname(CONTACT_PHASE),
                            "timePeriodsData": [
                                {
                                    "$type": "communityCommunityEntryPhaseTimePeriodData",
                                    "isSequence": 0,
                                    "periodName": cname("Day"),
                                    "spotNodeIds": [
                                        global_node_id(AI_SPOT_GLOBAL_ID)
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    )
    return handles.wrap(
        {
            "$type": "worldCompiledCommunityAreaNode_Streamable",
            "area": area,
            "debugName": cname("{cqa005_com_contact}"),
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "proxyScale": None,
            "sourceObjectId": {
                "$type": "entEntityID",
                "hash": COMMUNITY_SOURCE_ID,
            },
            "sourcePrefabHash": "0",
            "streamingDistance": 160.0,
            "tag": "None",
            "tagExt": "None",
        }
    )


def fixed_point(value: float) -> dict[str, int | str]:
    return {"$type": "FixedPoint", "Bits": round(value * 131072)}


def community_registry_node(handles: Handles) -> dict[str, Any]:
    time_period = {
        "$type": "communityPhaseTimePeriod",
        "categories": [],
        "hour": "Day",
        "isSequence": 0,
        "markings": [],
        "quantity": 1,
        "spotNodeRefs": [node_ref(AI_SPOT_FULL)],
    }
    phase = handles.wrap(
        {
            "$type": "communitySpawnPhase",
            "alwaysSpawned": "default__false_",
            "appearances": [cname(CONTACT_APPEARANCE)],
            "phaseName": cname(CONTACT_PHASE),
            "prefetchAppearance": 0,
            "timePeriods": [time_period],
        }
    )
    spawn_entry = handles.wrap(
        {
            "$type": "communitySpawnEntry",
            "characterRecordId": tweakdbid(CONTACT_CHARACTER),
            "entryName": cname(CONTACT_ENTRY),
            "initializers": [],
            "phases": [phase],
            "spawnInView": "default__true_",
        }
    )
    template = handles.wrap(
        {
            "$type": "communityCommunityTemplateData",
            "crowdEntries": [],
            "entries": [spawn_entry],
            "spawnSetReference": cname("None"),
        }
    )
    return handles.wrap(
        {
            "$type": "worldCommunityRegistryNode",
            "communitiesData": [
                {
                    "$type": "worldCommunityRegistryItem",
                    "communityAreaType": "Regular",
                    "communityId": {
                        "$type": "gameCommunityID",
                        "entityId": {
                            "$type": "entEntityID",
                            "hash": COMMUNITY_SOURCE_ID,
                        },
                    },
                    "entriesInitialState": [
                        {
                            "$type": "worldCommunityEntryInitialState",
                            "entryActiveOnStart": 0,
                            "entryName": cname(CONTACT_ENTRY),
                            "initialPhaseName": cname(CONTACT_PHASE),
                        }
                    ],
                    "template": template,
                }
            ],
            "crowdCreationRegistry": None,
            "debugName": cname("cqa005_contact_registry"),
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "proxyScale": None,
            "representsCrowd": 0,
            "sourcePrefabHash": "0",
            "spawnSetNameToCommunityID": {
                "$type": "gameCommunitySpawnSetNameToID",
                "entries": [],
            },
            "tag": "None",
            "tagExt": "None",
            "workspotsPersistentData": [
                {
                    "$type": "AISpotPersistentData",
                    "globalNodeId": global_node_id(AI_SPOT_GLOBAL_ID),
                    "isEnabled": 1,
                    "worldPosition": {
                        "$type": "WorldPosition",
                        "x": fixed_point(CONTACT_POSITION[0]),
                        "y": fixed_point(CONTACT_POSITION[1]),
                        "z": fixed_point(CONTACT_POSITION[2]),
                    },
                    "yaw": YAW,
                }
            ],
        }
    )


def sector_document(
    archive_path: str,
    *,
    category: str,
    level: int,
    nodes: list[dict[str, Any]],
    refs: list[str],
    placements: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": archive_path,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "worldStreamingSector",
                "category": category,
                "cookingPlatform": "PLATFORM_None",
                "externInplaceResource": resource_path(0),
                "level": level,
                "localInplaceResource": [],
                "nodeData": {
                    "BufferId": "0",
                    "Flags": 0,
                    "Type": (
                        "WolvenKit.RED4.Archive.Buffer.worldNodeDataBuffer, "
                        "WolvenKit.RED4, Version=8.19.0.0, Culture=neutral, "
                        "PublicKeyToken=null"
                    ),
                    "Data": placements,
                },
                "nodeRefs": [node_ref(ref) for ref in refs],
                "nodes": nodes,
                "persistentNodeIndex": 0,
                "persistentNodes": [],
                "variantIndices": [0],
                "variantNodes": [],
                "version": 62,
            },
            "EmbeddedFiles": [],
        },
    }


def build_quest_sector() -> dict[str, Any]:
    handles = Handles()
    nodes = [
        trigger_node(
            handles,
            SETUP_LOCAL,
            radius=SETUP_RADIUS,
            point_count=16,
            height=12,
        ),
        trigger_node(
            handles,
            CLEANUP_LOCAL,
            radius=CLEANUP_RADIUS,
            point_count=20,
            height=16,
        ),
        ai_spot_node(handles),
        community_area_node(handles),
    ]
    placements = [
        node_data(
            0,
            SETUP_FULL,
            SETUP_POSITION,
            YAW,
            max_streaming_distance=320,
            opaque_distance=280,
        ),
        node_data(
            1,
            CLEANUP_FULL,
            CLEANUP_POSITION,
            YAW,
            max_streaming_distance=360,
            opaque_distance=320,
        ),
        node_data(
            2,
            AI_SPOT_FULL,
            CONTACT_POSITION,
            YAW,
            max_streaming_distance=320,
            opaque_distance=280,
        ),
        node_data(
            3,
            COMMUNITY_FULL,
            CONTACT_POSITION,
            YAW,
            max_streaming_distance=320,
            opaque_distance=280,
        ),
    ]
    return sector_document(
        QUEST_SECTOR_PATH,
        category="Quest",
        level=255,
        nodes=nodes,
        refs=[SETUP_FULL, CLEANUP_FULL, AI_SPOT_FULL, COMMUNITY_FULL],
        placements=placements,
    )


def registry_placement(node_index: int) -> dict[str, Any]:
    placement = node_data(
        node_index,
        int(REGISTRY_NODE_ID),
        (0, 0, 0),
        0,
        max_streaming_distance=17.320507,
        opaque_distance=100000000.0,
    )
    placement["Uk10"] = 32
    return placement


def build_always_loaded_sector() -> dict[str, Any]:
    handles = Handles()
    nodes = [
        marker_node(handles, SCENE_MARKER_LOCAL),
        marker_node(handles, MAPPIN_LOCAL),
        community_registry_node(handles),
    ]
    placements = [
        node_data(
            0,
            SCENE_MARKER_FULL,
            CENTER,
            YAW,
            max_streaming_distance=360,
            opaque_distance=320,
        ),
        node_data(
            1,
            MAPPIN_FULL,
            CENTER,
            YAW,
            max_streaming_distance=360,
            opaque_distance=320,
        ),
        registry_placement(2),
    ]
    return sector_document(
        ALWAYS_SECTOR_PATH,
        category="AlwaysLoaded",
        level=1,
        nodes=nodes,
        refs=[SCENE_MARKER_FULL, MAPPIN_FULL],
        placements=placements,
    )


def build_streaming_block() -> dict[str, Any]:
    descriptors = [
        descriptor(
            "Quest",
            QUEST_SECTOR_PATH,
            0,
            PREFAB_FULL,
            (-1300.02, 1197.2208, -291.7),
            (-700.02, 1797.2208, 308.3),
        ),
        descriptor(
            "AlwaysLoaded",
            ALWAYS_SECTOR_PATH,
            1,
            None,
            (-99999, -99999, -99999),
            (99999, 99999, 99999),
        ),
    ]
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": BLOCK_PATH,
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "worldStreamingBlock",
                "cookingPlatform": "PLATFORM_PC",
                "descriptors": descriptors,
                "index": {
                    "$type": "worldStreamingBlockIndex",
                    "oup": "Base",
                    "rldGridCell": 0,
                },
            },
            "EmbeddedFiles": [],
        },
    }


def write_checkpoint(
    checkpoint: str,
    root_phase: dict[str, Any],
    child_phase: dict[str, Any],
) -> None:
    raw_root = CHECKPOINTS[checkpoint] / "source" / "raw" / DEPOT_ROOT
    completed = checkpoint == "completed"
    write_json(raw_root / "phases" / "cqa005.questphase.json", root_phase)
    write_json(
        raw_root / "phases" / "cqa005_contact.questphase.json",
        child_phase,
    )
    write_json(raw_root / "journal" / "cqa005.journal.json", build_journal())
    write_json(
        raw_root
        / "localization"
        / "en-us"
        / "onscreens"
        / "cqa005_onscreens.json.json",
        build_onscreen_localization(),
    )
    write_json(
        raw_root
        / "localization"
        / "en-us"
        / "subtitles"
        / "cqa005_subtitles.json.json",
        build_subtitles(),
    )
    write_json(
        raw_root
        / "localization"
        / "en-us"
        / "subtitles"
        / "cqa005_subtitles_map.json.json",
        build_subtitle_map(),
    )
    write_json(
        raw_root / "localization" / "en-us" / "vo" / "cqa005_vo.json.json",
        build_voiceover_map(),
    )
    write_json(
        raw_root / "scenes" / "cqa005_first_contact.scene.json",
        build_scene(completed),
    )
    write_json(
        raw_root / "world" / "cqa005_first_contact.streamingblock.json",
        build_streaming_block(),
    )
    write_json(
        raw_root / "world" / "cqa005_first_contact.streamingsector.json",
        build_quest_sector(),
    )
    write_json(
        raw_root / "world" / "cqa005_always_loaded.streamingsector.json",
        build_always_loaded_sector(),
    )


def main() -> None:
    write_checkpoint(
        "start",
        build_start_root_phase(),
        build_start_child_phase(),
    )
    write_checkpoint(
        "completed",
        build_completed_root_phase(),
        build_completed_child_phase(),
    )


if __name__ == "__main__":
    main()
