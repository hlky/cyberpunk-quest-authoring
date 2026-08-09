#!/usr/bin/env python3
"""Build the mod-owned CR2W-JSON sources for the Lab 3 checkpoints.

This is documentation-author infrastructure. Readers inspect and edit the
same native resources in WolvenKit and do not need this script.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64
import math
import struct
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


ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = ROOT / "examples" / "lab-03-boundary-check"
CHECKPOINTS = {
    "start": LAB_ROOT / "start",
    "completed": LAB_ROOT / "completed",
}
DEPOT_ROOT = Path("mod") / "cqa" / "cqa003"

QUEST_PATH = "quests/minor_quest/cqa003"
PHASE_PATH = f"{QUEST_PATH}/cqa003_01"
REACH_PATH = f"{PHASE_PATH}/cqa003_01_obj_reach"
LEAVE_PATH = f"{PHASE_PATH}/cqa003_01_obj_leave"
MAPPIN_PATH = f"{REACH_PATH}/cqa003_01_qmp_checkpoint"

PREFAB_LOCAL = "#cqa003_pr_boundary"
PREFAB_FULL = "$/mod/cqa/cqa003/#cqa003_pr_boundary"
REACH_REF_LOCAL = "#cqa003_tr_reach"
LEAVE_REF_LOCAL = "#cqa003_tr_leave"
MARKER_REF_LOCAL = "#cqa003_mp_checkpoint"
REACH_REF_FULL = f"{PREFAB_FULL}/{REACH_REF_LOCAL}"
LEAVE_REF_FULL = f"{PREFAB_FULL}/{LEAVE_REF_LOCAL}"
MARKER_REF_FULL = f"{PREFAB_FULL}/{MARKER_REF_LOCAL}"

BLOCK_PATH = "mod\\cqa\\cqa003\\world\\cqa003_boundary.streamingblock"
QUEST_SECTOR_PATH = (
    "mod\\cqa\\cqa003\\world\\cqa003_boundary.streamingsector"
)
ALWAYS_LOADED_PATH = (
    "mod\\cqa\\cqa003\\world\\cqa003_always_loaded.streamingsector"
)

MARKER_POSITION = (-1000.02, 1497.2208, 8.3)
MARKER_YAW = 88.6
REACH_POSITION = (-1000.02, 1497.2208, 2.3)
LEAVE_POSITION = (-1000.02, 1497.2208, 0.3)
REACH_RADIUS = 25
LEAVE_RADIUS = 110


def node_ref(value: str | int) -> dict[str, Any]:
    storage = "string" if isinstance(value, str) else "uint64"
    return {
        "$type": "NodeRef",
        "$storage": storage,
        "$value": str(value),
    }


def resource_path(
    value: str | int,
    *,
    flags: str = "Soft",
) -> dict[str, Any]:
    storage = "string" if isinstance(value, str) else "uint64"
    return {
        "DepotPath": {
            "$type": "ResourcePath",
            "$storage": storage,
            "$value": str(value),
        },
        "Flags": flags,
    }


def vector3(value: tuple[float, float, float]) -> dict[str, Any]:
    return {
        "$type": "Vector3",
        "X": value[0],
        "Y": value[1],
        "Z": value[2],
    }


def vector4(
    value: tuple[float, float, float],
    *,
    w: float = 0,
) -> dict[str, Any]:
    return {
        "$type": "Vector4",
        "W": w,
        "X": value[0],
        "Y": value[1],
        "Z": value[2],
    }


def quaternion_from_yaw(yaw: float) -> dict[str, Any]:
    half_angle = math.radians(yaw) / 2
    return {
        "$type": "Quaternion",
        "i": 0,
        "j": 0,
        "k": math.sin(half_angle),
        "r": math.cos(half_angle),
    }


def entity_reference() -> dict[str, Any]:
    return {
        "$type": "gameEntityReference",
        "dynamicEntityUniqueName": cname("None"),
        "names": [],
        "reference": node_ref(0),
        "sceneActorContextName": cname("None"),
        "slotName": cname("None"),
        "type": "EntityRef",
    }


def trigger_condition_node(
    builder: GraphBuilder,
    quest_id: int,
    trigger_ref: str,
    condition_type: str,
) -> GraphNode:
    condition = builder.handles.wrap(
        {
            "$type": "questTriggerCondition",
            "activatorRef": entity_reference(),
            "isPlayerActivator": 1,
            "triggerAreaRef": node_ref(trigger_ref),
            "type": condition_type,
        }
    )
    return builder.node(
        quest_id,
        "questPauseConditionNodeDefinition",
        inputs=("In",),
        properties={"condition": condition},
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
                MAPPIN_PATH,
                "gameJournalQuestMapPin",
            ),
        },
    )


def questphase_document(builder: GraphBuilder) -> dict[str, Any]:
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": "mod\\cqa\\cqa003\\phases\\cqa003.questphase",
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
                        "prefabNodeRef": node_ref(PREFAB_LOCAL),
                    }
                ],
            },
            "EmbeddedFiles": [],
        },
    }


def build_start_questphase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    builder.connect(phase_input, phase_output)
    return questphase_document(builder)


def build_completed_questphase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    completed_guard = fact_condition_node(builder, 10, "cqa003_completed")
    quest_active = journal_node(builder, 11, QUEST_PATH, "gameJournalQuest")
    phase_active = journal_node(builder, 12, PHASE_PATH, "gameJournalQuestPhase")
    reach_active = journal_node(
        builder,
        13,
        REACH_PATH,
        "gameJournalQuestObjective",
    )
    mappin_active = mappin_node(builder, 14, disable_previous=0)
    reach_wait = trigger_condition_node(
        builder,
        15,
        REACH_REF_LOCAL,
        "IsInside",
    )
    mappin_inactive = mappin_node(builder, 16, disable_previous=0)
    reach_succeeded = journal_node(
        builder,
        17,
        REACH_PATH,
        "gameJournalQuestObjective",
    )
    leave_active = journal_node(
        builder,
        18,
        LEAVE_PATH,
        "gameJournalQuestObjective",
    )
    leave_wait = trigger_condition_node(
        builder,
        19,
        LEAVE_REF_LOCAL,
        "IsOutside",
    )
    leave_succeeded = journal_node(
        builder,
        20,
        LEAVE_PATH,
        "gameJournalQuestObjective",
    )
    phase_succeeded = journal_node(
        builder,
        21,
        PHASE_PATH,
        "gameJournalQuestPhase",
    )
    completed_fact = set_fact_node(builder, 22, "cqa003_completed")
    quest_succeeded = journal_node(builder, 23, QUEST_PATH, "gameJournalQuest")

    builder.connect(phase_input, completed_guard)
    builder.connect(
        completed_guard,
        quest_active,
        source_socket="True",
        destination_socket="Active",
    )
    builder.connect(
        quest_active,
        phase_active,
        destination_socket="Active",
    )
    builder.connect(
        phase_active,
        reach_active,
        destination_socket="Active",
    )
    builder.connect(
        reach_active,
        mappin_active,
        destination_socket="Active",
    )
    builder.connect(mappin_active, reach_wait)
    builder.connect(
        reach_wait,
        mappin_inactive,
        destination_socket="Inactive",
    )
    builder.connect(
        mappin_inactive,
        reach_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect(
        reach_succeeded,
        leave_active,
        destination_socket="Active",
    )
    builder.connect(leave_active, leave_wait)
    builder.connect(
        leave_wait,
        leave_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect(
        leave_succeeded,
        phase_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect(phase_succeeded, completed_fact)
    builder.connect(
        completed_fact,
        quest_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect_to_output(
        completed_guard,
        phase_output,
        source_socket="False",
    )
    builder.connect_to_output(quest_succeeded, phase_output)
    return questphase_document(builder)


def journal_mappin() -> dict[str, Any]:
    return Handles.define(
        "6",
        journal_entry(
            "gameJournalQuestMapPin",
            "cqa003_01_qmp_checkpoint",
            [],
            enableGPS=1,
            mappinData={
                "$type": "gamemappinsMappinData",
                "active": 0,
                "debugCaption": "cqa_cqa003_mappin_checkpoint",
                "localizedCaption": localized_string(
                    "cqa_cqa003_mappin_checkpoint"
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
                "reference": node_ref(MARKER_REF_LOCAL),
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
    reach = objective(
        "5",
        "cqa003_01_obj_reach",
        "cqa_cqa003_objective_reach",
        [journal_mappin()],
    )
    leave = objective(
        "7",
        "cqa003_01_obj_leave",
        "cqa_cqa003_objective_leave",
        [],
    )
    phase = Handles.define(
        "4",
        journal_entry(
            "gameJournalQuestPhase",
            "cqa003_01",
            [reach, leave],
            locationPrefabRef=node_ref(0),
        ),
    )
    quest = Handles.define(
        "3",
        journal_entry(
            "gameJournalQuest",
            "cqa003",
            [phase],
            districtID="",
            recommendedLevelID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            title=localized_string("cqa_cqa003_title"),
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
            "ArchiveFileName": "mod\\cqa\\cqa003\\journal\\cqa003.journal",
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


def build_localization() -> dict[str, Any]:
    strings = {
        "cqa_cqa003_title": "Boundary Check",
        "cqa_cqa003_objective_reach": "Reach the marked checkpoint.",
        "cqa_cqa003_objective_leave": "Leave the checkpoint area.",
        "cqa_cqa003_mappin_checkpoint": "Boundary Check checkpoint",
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
            "ArchiveFileName": (
                "mod\\cqa\\cqa003\\localization\\en-us\\onscreens\\cqa003.json"
            ),
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


def circle_points(radius: float, count: int) -> list[tuple[float, float, float]]:
    return [
        (
            math.cos(2 * math.pi * index / count) * radius,
            math.sin(2 * math.pi * index / count) * radius,
            0,
        )
        for index in range(count)
    ]


def outline_buffer(
    points: list[tuple[float, float, float]],
    height: float,
) -> str:
    payload = struct.pack("<I", len(points))
    for x, y, z in points:
        payload += struct.pack("<ffff", x, y, z, 1.0)
    payload += struct.pack("<f", height)
    return base64.b64encode(payload).decode("ascii")


def trigger_node(
    handles: Handles,
    ref: str,
    *,
    radius: float,
    point_count: int,
    height: float,
) -> dict[str, Any]:
    points = circle_points(radius, point_count)
    notifier = handles.wrap(
        {
            "$type": "questTriggerNotifier_Quest",
            "excludeChannels": 0,
            "includeChannels": "TC_Default",
            "isEnabled": 1,
        }
    )
    outline = handles.wrap(
        {
            "$type": "AreaShapeOutline",
            "buffer": outline_buffer(points, height),
            "height": height,
            "points": [vector3(point) for point in points],
        }
    )
    return handles.wrap(
        {
            "$type": "worldTriggerAreaNode",
            "color": {
                "$type": "Color",
                "Alpha": 0,
                "Blue": 0,
                "Green": 0,
                "Red": 0,
            },
            "debugName": cname(f"{{{ref.removeprefix('#')}}}"),
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "notifiers": [notifier],
            "outline": outline,
            "proxyScale": None,
            "sourcePrefabHash": "0",
            "tag": "None",
            "tagExt": "None",
        }
    )


def marker_node(handles: Handles, ref: str) -> dict[str, Any]:
    return handles.wrap(
        {
            "$type": "worldStaticMarkerNode",
            "debugName": cname(f"{{{ref.removeprefix('#')}}}"),
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "proxyScale": None,
            "sourcePrefabHash": "0",
            "tag": "None",
            "tagExt": "None",
        }
    )


def node_data(
    node_index: int,
    ref: str,
    position: tuple[float, float, float],
    yaw: float,
    *,
    max_streaming_distance: float,
    opaque_distance: float,
) -> dict[str, Any]:
    return {
        "Id": "0",
        "NodeIndex": node_index,
        "Position": vector4(position),
        "Orientation": quaternion_from_yaw(yaw),
        "Scale": {"$type": "Vector3", "X": 1.0, "Y": 1.0, "Z": 1.0},
        "Pivot": vector3(position),
        "Bounds": {
            "$type": "Box",
            "Max": vector4(position),
            "Min": vector4(position),
        },
        "QuestPrefabRefHash": node_ref(ref),
        "UkHash1": node_ref(0),
        "CookedPrefabData": resource_path(0, flags="Default"),
        "MaxStreamingDistance": max_streaming_distance,
        "UkFloat1": opaque_distance,
        "Uk10": 1024,
        "Uk11": 512,
        "Uk12": 0,
        "Uk13": "0",
        "Uk14": "0",
    }


def streaming_sector_document(
    archive_path: str,
    *,
    category: str,
    level: int,
    nodes: list[dict[str, Any]],
    refs: list[str],
    placement: list[dict[str, Any]],
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
                    "Data": placement,
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
            REACH_REF_LOCAL,
            radius=REACH_RADIUS,
            point_count=16,
            height=12,
        ),
        trigger_node(
            handles,
            LEAVE_REF_LOCAL,
            radius=LEAVE_RADIUS,
            point_count=20,
            height=16,
        ),
    ]
    placement = [
        node_data(
            0,
            REACH_REF_FULL,
            REACH_POSITION,
            MARKER_YAW,
            max_streaming_distance=320,
            opaque_distance=280,
        ),
        node_data(
            1,
            LEAVE_REF_FULL,
            LEAVE_POSITION,
            MARKER_YAW,
            max_streaming_distance=360,
            opaque_distance=320,
        ),
    ]
    return streaming_sector_document(
        QUEST_SECTOR_PATH,
        category="Quest",
        level=255,
        nodes=nodes,
        refs=[REACH_REF_FULL, LEAVE_REF_FULL],
        placement=placement,
    )


def build_always_loaded_sector() -> dict[str, Any]:
    handles = Handles()
    nodes = [marker_node(handles, MARKER_REF_LOCAL)]
    placement = [
        node_data(
            0,
            MARKER_REF_FULL,
            MARKER_POSITION,
            MARKER_YAW,
            max_streaming_distance=360,
            opaque_distance=320,
        )
    ]
    return streaming_sector_document(
        ALWAYS_LOADED_PATH,
        category="AlwaysLoaded",
        level=1,
        nodes=nodes,
        refs=[MARKER_REF_FULL],
        placement=placement,
    )


def descriptor(
    category: str,
    depot_path: str,
    level: int,
    prefab_ref: str | None,
    minimum: tuple[float, float, float],
    maximum: tuple[float, float, float],
) -> dict[str, Any]:
    max_float = 3.40282347e38
    return {
        "$type": "worldStreamingSectorDescriptor",
        "blockIndex": {
            "$type": "worldStreamingBlockIndex",
            "oup": "Base",
            "rldGridCell": 0,
        },
        "category": category,
        "data": resource_path(depot_path),
        "level": level,
        "numNodeRanges": 1,
        "questPrefabNodeRef": node_ref(prefab_ref if prefab_ref else 0),
        "streamingBox": {
            "$type": "Box",
            "Max": vector4(maximum, w=max_float),
            "Min": vector4(minimum, w=-max_float),
        },
        "variants": [],
    }


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
            ALWAYS_LOADED_PATH,
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


def write_checkpoint(checkpoint: str, questphase: dict[str, Any]) -> None:
    raw_root = CHECKPOINTS[checkpoint] / "source" / "raw" / DEPOT_ROOT
    write_json(raw_root / "phases" / "cqa003.questphase.json", questphase)
    write_json(raw_root / "journal" / "cqa003.journal.json", build_journal())
    write_json(
        raw_root / "localization" / "en-us" / "onscreens" / "cqa003.json.json",
        build_localization(),
    )
    write_json(
        raw_root / "world" / "cqa003_boundary.streamingblock.json",
        build_streaming_block(),
    )
    write_json(
        raw_root / "world" / "cqa003_boundary.streamingsector.json",
        build_quest_sector(),
    )
    write_json(
        raw_root / "world" / "cqa003_always_loaded.streamingsector.json",
        build_always_loaded_sector(),
    )


def main() -> None:
    write_checkpoint("start", build_start_questphase())
    write_checkpoint("completed", build_completed_questphase())


if __name__ == "__main__":
    main()
