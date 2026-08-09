#!/usr/bin/env python3
"""Build the mod-owned CR2W-JSON sources for the Lab 4 checkpoints.

This is documentation-author infrastructure. Readers inspect and edit the
same native resources in WolvenKit and do not need this script.

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
from build_lab02_sources import realtime_delay_node  # noqa: E402
from build_lab03_sources import (  # noqa: E402
    descriptor,
    entity_reference,
    marker_node,
    node_data,
    node_ref,
    resource_path,
    streaming_sector_document,
    trigger_condition_node,
    trigger_node,
)


ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = ROOT / "examples" / "lab-04-handoff-point"
CHECKPOINTS = {
    "start": LAB_ROOT / "start",
    "completed": LAB_ROOT / "completed",
}
DEPOT_ROOT = Path("mod") / "cqa" / "cqa004"

ROOT_PHASE_PATH = "mod\\cqa\\cqa004\\phases\\cqa004.questphase"
CHILD_PHASE_PATH = (
    "mod\\cqa\\cqa004\\phases\\cqa004_boundary.questphase"
)
JOURNAL_DEPOT_PATH = "mod\\cqa\\cqa004\\journal\\cqa004.journal"
LOCALIZATION_DEPOT_PATH = (
    "mod\\cqa\\cqa004\\localization\\en-us\\onscreens\\cqa004.json"
)

QUEST_PATH = "quests/minor_quest/cqa004"
PHASE_PATH = f"{QUEST_PATH}/cqa004_01"
REACH_PATH = f"{PHASE_PATH}/cqa004_01_obj_reach"
LEAVE_PATH = f"{PHASE_PATH}/cqa004_01_obj_leave"
CONFIRM_PATH = f"{PHASE_PATH}/cqa004_01_obj_confirm"
MAPPIN_PATH = f"{REACH_PATH}/cqa004_01_qmp_handoff"

PREFAB_LOCAL = "#cqa004_pr_handoff"
PREFAB_FULL = "$/mod/cqa/cqa004/#cqa004_pr_handoff"
REACH_REF_LOCAL = "#cqa004_tr_reach"
LEAVE_REF_LOCAL = "#cqa004_tr_leave"
MARKER_REF_LOCAL = "#cqa004_mp_handoff"
REACH_REF_FULL = f"{PREFAB_FULL}/{REACH_REF_LOCAL}"
LEAVE_REF_FULL = f"{PREFAB_FULL}/{LEAVE_REF_LOCAL}"
MARKER_REF_FULL = f"{PREFAB_FULL}/{MARKER_REF_LOCAL}"

BLOCK_PATH = "mod\\cqa\\cqa004\\world\\cqa004_handoff.streamingblock"
QUEST_SECTOR_PATH = (
    "mod\\cqa\\cqa004\\world\\cqa004_handoff.streamingsector"
)
ALWAYS_LOADED_PATH = (
    "mod\\cqa\\cqa004\\world\\cqa004_always_loaded.streamingsector"
)

# Lab 4 deliberately reuses Lab 3's reviewed Allen Street geometry. Splitting
# the phase is the independent variable in this checkpoint.
MARKER_POSITION = (-1000.02, 1497.2208, 8.3)
MARKER_YAW = 88.6
REACH_POSITION = (-1000.02, 1497.2208, 2.3)
LEAVE_POSITION = (-1000.02, 1497.2208, 0.3)
REACH_RADIUS = 25
LEAVE_RADIUS = 110


def external_phase_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    """Create the external terminating-child contract taught in Lab 4."""

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
                MAPPIN_PATH,
                "gameJournalQuestMapPin",
            ),
        },
    )


def questphase_document(
    builder: GraphBuilder,
    archive_path: str,
    *,
    phase_prefabs: list[str],
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
                    for prefab in phase_prefabs
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
    return questphase_document(
        builder,
        ROOT_PHASE_PATH,
        phase_prefabs=[PREFAB_LOCAL],
    )


def build_start_child_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    builder.connect(phase_input, phase_output)
    return questphase_document(
        builder,
        CHILD_PHASE_PATH,
        phase_prefabs=[],
    )


def build_completed_root_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    completed_guard = fact_condition_node(builder, 10, "cqa004_completed")
    quest_active = journal_node(builder, 11, QUEST_PATH, "gameJournalQuest")
    phase_active = journal_node(builder, 12, PHASE_PATH, "gameJournalQuestPhase")
    child = external_phase_node(builder, 13)
    confirmation_active = journal_node(
        builder,
        14,
        CONFIRM_PATH,
        "gameJournalQuestObjective",
    )
    confirmation_delay = realtime_delay_node(builder, 15, 30)
    confirmation_succeeded = journal_node(
        builder,
        16,
        CONFIRM_PATH,
        "gameJournalQuestObjective",
    )
    phase_succeeded = journal_node(
        builder,
        17,
        PHASE_PATH,
        "gameJournalQuestPhase",
    )
    completed_fact = set_fact_node(builder, 18, "cqa004_completed")
    quest_succeeded = journal_node(builder, 19, QUEST_PATH, "gameJournalQuest")

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
        child,
        destination_socket="In1",
    )
    builder.connect(
        child,
        confirmation_active,
        source_socket="Out1",
        destination_socket="Active",
    )
    builder.connect(confirmation_active, confirmation_delay)
    builder.connect(
        confirmation_delay,
        confirmation_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect(
        confirmation_succeeded,
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
    return questphase_document(
        builder,
        ROOT_PHASE_PATH,
        phase_prefabs=[PREFAB_LOCAL],
    )


def build_completed_child_phase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    reach_active = journal_node(
        builder,
        10,
        REACH_PATH,
        "gameJournalQuestObjective",
    )
    mappin_active = mappin_node(builder, 11, disable_previous=0)
    reach_wait = trigger_condition_node(
        builder,
        12,
        REACH_REF_LOCAL,
        "IsInside",
    )
    mappin_inactive = mappin_node(builder, 13, disable_previous=0)
    reach_succeeded = journal_node(
        builder,
        14,
        REACH_PATH,
        "gameJournalQuestObjective",
    )
    leave_active = journal_node(
        builder,
        15,
        LEAVE_PATH,
        "gameJournalQuestObjective",
    )
    leave_wait = trigger_condition_node(
        builder,
        16,
        LEAVE_REF_LOCAL,
        "IsOutside",
    )
    leave_succeeded = journal_node(
        builder,
        17,
        LEAVE_PATH,
        "gameJournalQuestObjective",
    )

    builder.connect(
        phase_input,
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
    builder.connect_to_output(leave_succeeded, phase_output)
    return questphase_document(
        builder,
        CHILD_PHASE_PATH,
        phase_prefabs=[],
    )


def journal_mappin() -> dict[str, Any]:
    return Handles.define(
        "6",
        journal_entry(
            "gameJournalQuestMapPin",
            "cqa004_01_qmp_handoff",
            [],
            enableGPS=1,
            mappinData={
                "$type": "gamemappinsMappinData",
                "active": 0,
                "debugCaption": "cqa_cqa004_mappin_handoff",
                "localizedCaption": localized_string(
                    "cqa_cqa004_mappin_handoff"
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
        "cqa004_01_obj_reach",
        "cqa_cqa004_objective_reach",
        [journal_mappin()],
    )
    leave = objective(
        "7",
        "cqa004_01_obj_leave",
        "cqa_cqa004_objective_leave",
        [],
    )
    confirm = objective(
        "8",
        "cqa004_01_obj_confirm",
        "cqa_cqa004_objective_confirm",
        [],
    )
    phase = Handles.define(
        "4",
        journal_entry(
            "gameJournalQuestPhase",
            "cqa004_01",
            [reach, leave, confirm],
            locationPrefabRef=node_ref(0),
        ),
    )
    quest = Handles.define(
        "3",
        journal_entry(
            "gameJournalQuest",
            "cqa004",
            [phase],
            districtID="",
            recommendedLevelID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            title=localized_string("cqa_cqa004_title"),
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
            "ArchiveFileName": JOURNAL_DEPOT_PATH,
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
        "cqa_cqa004_title": "Handoff Point",
        "cqa_cqa004_objective_reach": "Reach the handoff point.",
        "cqa_cqa004_objective_leave": "Clear the handoff area.",
        "cqa_cqa004_objective_confirm": "Wait for handoff confirmation.",
        "cqa_cqa004_mappin_handoff": "Handoff Point",
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
            "ArchiveFileName": LOCALIZATION_DEPOT_PATH,
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


def write_checkpoint(
    checkpoint: str,
    root_phase: dict[str, Any],
    child_phase: dict[str, Any],
) -> None:
    raw_root = CHECKPOINTS[checkpoint] / "source" / "raw" / DEPOT_ROOT
    write_json(raw_root / "phases" / "cqa004.questphase.json", root_phase)
    write_json(
        raw_root / "phases" / "cqa004_boundary.questphase.json",
        child_phase,
    )
    write_json(raw_root / "journal" / "cqa004.journal.json", build_journal())
    write_json(
        raw_root / "localization" / "en-us" / "onscreens" / "cqa004.json.json",
        build_localization(),
    )
    write_json(
        raw_root / "world" / "cqa004_handoff.streamingblock.json",
        build_streaming_block(),
    )
    write_json(
        raw_root / "world" / "cqa004_handoff.streamingsector.json",
        build_quest_sector(),
    )
    write_json(
        raw_root / "world" / "cqa004_always_loaded.streamingsector.json",
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
