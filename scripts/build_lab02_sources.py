#!/usr/bin/env python3
"""Build the mod-owned CR2W-JSON sources for the Lab 2 checkpoints.

This is documentation-author infrastructure. Readers author the same resources
in WolvenKit and do not need this script.

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
    input_node,
    journal_entry,
    journal_node,
    localized_string,
    output_node,
    write_json,
)


ROOT = Path(__file__).resolve().parents[1]
LAB_ROOT = ROOT / "examples" / "lab-02-signal-race"
CHECKPOINTS = {
    "start": LAB_ROOT / "start",
    "completed": LAB_ROOT / "completed",
}
DEPOT_ROOT = Path("mod") / "cqa" / "cqa002"

QUEST_PATH = "quests/minor_quest/cqa002"
REQUIRED_OBJECTIVE_PATH = (
    "quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_wait"
)
OPTIONAL_OBJECTIVE_PATH = (
    "quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_stable"
)


def fact_db_condition(
    builder: GraphBuilder,
    fact_name: str,
    *,
    comparison: str,
    value: int,
) -> dict[str, Any]:
    comparison_type = builder.handles.wrap(
        {
            "$type": "questVarComparison_ConditionType",
            "comparisonType": comparison,
            "factName": fact_name,
            "value": value,
        }
    )
    return builder.handles.wrap(
        {"$type": "questFactsDBCondition", "type": comparison_type}
    )


def immediate_fact_condition_node(
    builder: GraphBuilder,
    quest_id: int,
    fact_name: str,
    *,
    comparison: str,
    value: int,
) -> GraphNode:
    return builder.node(
        quest_id,
        "questConditionNodeDefinition",
        inputs=("In",),
        outputs=("True", "False"),
        properties={
            "condition": fact_db_condition(
                builder,
                fact_name,
                comparison=comparison,
                value=value,
            )
        },
    )


def pause_fact_condition_node(
    builder: GraphBuilder,
    quest_id: int,
    fact_name: str,
    *,
    comparison: str,
    value: int,
) -> GraphNode:
    return builder.node(
        quest_id,
        "questPauseConditionNodeDefinition",
        inputs=("In",),
        properties={
            "condition": fact_db_condition(
                builder,
                fact_name,
                comparison=comparison,
                value=value,
            )
        },
    )


def pause_and_condition_node(
    builder: GraphBuilder,
    quest_id: int,
    conditions: tuple[tuple[str, str, int], ...],
) -> GraphNode:
    children = [
        fact_db_condition(
            builder,
            fact_name,
            comparison=comparison,
            value=value,
        )
        for fact_name, comparison, value in conditions
    ]
    logical = builder.handles.wrap(
        {
            "$type": "questLogicalCondition",
            "conditions": children,
            "operation": "AND",
        }
    )
    return builder.node(
        quest_id,
        "questPauseConditionNodeDefinition",
        inputs=("In",),
        properties={"condition": logical},
    )


def realtime_delay_node(
    builder: GraphBuilder, quest_id: int, seconds: int
) -> GraphNode:
    delay = builder.handles.wrap(
        {
            "$type": "questRealtimeDelay_ConditionType",
            "hours": 0,
            "miliseconds": 0,
            "minutes": 0,
            "seconds": seconds,
        }
    )
    condition = builder.handles.wrap(
        {"$type": "questTimeCondition", "type": delay}
    )
    return builder.node(
        quest_id,
        "questPauseConditionNodeDefinition",
        inputs=("In",),
        properties={"condition": condition},
    )


def set_fact_node(
    builder: GraphBuilder,
    quest_id: int,
    fact_name: str,
    value: int,
) -> GraphNode:
    node_type = builder.handles.wrap(
        {
            "$type": "questSetVar_NodeType",
            "factName": fact_name,
            "setExactValue": 1,
            "value": value,
        }
    )
    return builder.node(
        quest_id,
        "questFactsDBManagerNodeDefinition",
        inputs=("In",),
        properties={"type": node_type},
    )


def logical_xor_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    return builder.node(
        quest_id,
        "questLogicalXorNodeDefinition",
        inputs=("In1", "In2"),
        outputs=("Out1",),
        properties={"inputSocketCount": 2, "outputSocketCount": 1},
    )


def questphase_document(builder: GraphBuilder) -> dict[str, Any]:
    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": "mod\\cqa\\cqa002\\phases\\cqa002.questphase",
        },
        "Data": {
            "Version": 195,
            "BuildVersion": 0,
            "RootChunk": {
                "$type": "questQuestPhaseResource",
                "cookingPlatform": "PLATFORM_PC",
                "graph": builder.graph,
                "inplacePhases": [],
                "phasePrefabs": [],
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

    completed_guard = immediate_fact_condition_node(
        builder,
        10,
        "cqa002_completed",
        comparison="Equal",
        value=0,
    )
    test_mode = set_fact_node(builder, 11, "cqa002_test_mode", 2)
    quest_active = journal_node(builder, 12, QUEST_PATH, "gameJournalQuest")
    required_active = journal_node(
        builder,
        13,
        REQUIRED_OBJECTIVE_PATH,
        "gameJournalQuestObjective",
    )
    optional_active = journal_node(
        builder,
        14,
        OPTIONAL_OBJECTIVE_PATH,
        "gameJournalQuestObjective",
    )
    failed_listener = pause_fact_condition_node(
        builder,
        15,
        "cqa002_signal_failed",
        comparison="Greater",
        value=0,
    )
    stable_listener = pause_and_condition_node(
        builder,
        16,
        (
            ("cqa002_signal_stop", "Greater", 0),
            ("cqa002_test_mode", "Equal", 2),
        ),
    )
    mode_selector = immediate_fact_condition_node(
        builder,
        17,
        "cqa002_test_mode",
        comparison="Equal",
        value=1,
    )
    failure_delay = realtime_delay_node(builder, 18, 30)
    set_failed = set_fact_node(builder, 19, "cqa002_signal_failed", 1)
    stable_delay = realtime_delay_node(builder, 20, 120)
    set_stop = set_fact_node(builder, 21, "cqa002_signal_stop", 1)
    optional_failed = journal_node(
        builder,
        22,
        OPTIONAL_OBJECTIVE_PATH,
        "gameJournalQuestObjective",
    )
    optional_succeeded = journal_node(
        builder,
        23,
        OPTIONAL_OBJECTIVE_PATH,
        "gameJournalQuestObjective",
    )
    set_succeeded = set_fact_node(
        builder, 24, "cqa002_signal_succeeded", 1
    )
    xor_convergence = logical_xor_node(builder, 25)
    required_succeeded = journal_node(
        builder,
        26,
        REQUIRED_OBJECTIVE_PATH,
        "gameJournalQuestObjective",
    )
    set_completed = set_fact_node(builder, 27, "cqa002_completed", 1)
    quest_succeeded = journal_node(
        builder, 28, QUEST_PATH, "gameJournalQuest"
    )

    builder.connect(phase_input, completed_guard)
    builder.connect(
        completed_guard,
        test_mode,
        source_socket="True",
    )
    builder.connect(test_mode, quest_active, destination_socket="Active")
    builder.connect(
        quest_active, required_active, destination_socket="Active"
    )
    builder.connect(
        required_active, optional_active, destination_socket="Active"
    )

    # One ordinary output fans out to the two live monitors and the one-shot
    # mode selector. Only the selected writer branch is activated.
    builder.connect(optional_active, failed_listener)
    builder.connect(optional_active, stable_listener)
    builder.connect(optional_active, mode_selector)

    builder.connect(mode_selector, failure_delay, source_socket="True")
    builder.connect(failure_delay, set_failed)
    builder.connect(mode_selector, stable_delay, source_socket="False")
    builder.connect(stable_delay, set_stop)

    builder.connect(
        failed_listener,
        optional_failed,
        destination_socket="Failed",
    )
    builder.connect(
        optional_failed,
        xor_convergence,
        destination_socket="In1",
    )
    builder.connect(
        stable_listener,
        optional_succeeded,
        destination_socket="Succeeded",
    )
    builder.connect(optional_succeeded, set_succeeded)
    builder.connect(
        set_succeeded,
        xor_convergence,
        destination_socket="In2",
    )

    builder.connect(
        xor_convergence,
        required_succeeded,
        source_socket="Out1",
        destination_socket="Succeeded",
    )
    builder.connect(required_succeeded, set_completed)
    builder.connect(
        set_completed,
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


def objective(
    handle_id: str,
    entry_id: str,
    localization_key: str,
    *,
    optional: int,
) -> dict[str, Any]:
    return Handles.define(
        handle_id,
        journal_entry(
            "gameJournalQuestObjective",
            entry_id,
            [],
            counter=0,
            description=localized_string(localization_key),
            districtID="",
            itemID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            locationPrefabRef={
                "$type": "NodeRef",
                "$storage": "uint64",
                "$value": "0",
            },
            optional=optional,
        ),
    )


def build_journal() -> dict[str, Any]:
    required = objective(
        "5",
        "cqa002_01_obj_wait",
        "cqa_cqa002_objective_wait",
        optional=0,
    )
    stable = objective(
        "6",
        "cqa002_01_obj_stable",
        "cqa_cqa002_objective_stable",
        optional=1,
    )
    phase = Handles.define(
        "4",
        journal_entry(
            "gameJournalQuestPhase",
            "cqa002_01",
            [required, stable],
            locationPrefabRef={
                "$type": "NodeRef",
                "$storage": "uint64",
                "$value": "0",
            },
        ),
    )
    quest = Handles.define(
        "3",
        journal_entry(
            "gameJournalQuest",
            "cqa002",
            [phase],
            districtID="",
            recommendedLevelID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            title=localized_string("cqa_cqa002_title"),
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
            "descriptor": {
                "DepotPath": {
                    "$type": "ResourcePath",
                    "$storage": "string",
                    "$value": "base\\journal\\descriptor.journaldesc",
                },
                "Flags": "Soft",
            },
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
            "ArchiveFileName": "mod\\cqa\\cqa002\\journal\\cqa002.journal",
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
        "cqa_cqa002_title": "Signal Race",
        "cqa_cqa002_objective_wait": "Wait for the signal test to resolve.",
        "cqa_cqa002_objective_stable": "Keep the signal stable.",
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
                "mod\\cqa\\cqa002\\localization\\en-us\\onscreens\\cqa002.json"
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


def write_checkpoint(checkpoint: str, questphase: dict[str, Any]) -> None:
    raw_root = CHECKPOINTS[checkpoint] / "source" / "raw" / DEPOT_ROOT
    write_json(raw_root / "phases" / "cqa002.questphase.json", questphase)
    write_json(raw_root / "journal" / "cqa002.journal.json", build_journal())
    write_json(
        raw_root
        / "localization"
        / "en-us"
        / "onscreens"
        / "cqa002.json.json",
        build_localization(),
    )


def main() -> None:
    write_checkpoint("start", build_start_questphase())
    write_checkpoint("completed", build_completed_questphase())


if __name__ == "__main__":
    main()
