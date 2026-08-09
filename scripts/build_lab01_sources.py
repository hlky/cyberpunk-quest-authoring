#!/usr/bin/env python3
"""Build the mod-owned CR2W-JSON sources for the Lab 1 reference project.

This is documentation-author infrastructure. Readers author the same resources
in WolvenKit and do not need this script.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "examples" / "lab-01-one-shot" / "completed"
RAW_ROOT = PROJECT / "source" / "raw" / "mod" / "cqa" / "cqa001"


def cname(value: str) -> dict[str, Any]:
    return {"$type": "CName", "$storage": "string", "$value": value}


class Handles:
    def __init__(self) -> None:
        self.next_id = 0

    def reserve(self) -> str:
        value = str(self.next_id)
        self.next_id += 1
        return value

    @staticmethod
    def define(handle_id: str, data: dict[str, Any]) -> dict[str, Any]:
        return {"HandleId": handle_id, "Data": data}

    @staticmethod
    def ref(value: str | dict[str, Any]) -> dict[str, Any]:
        if isinstance(value, dict):
            value = value.get("HandleId") or value.get("HandleRefId")
        if value is None:
            raise ValueError("handle reference has no ID")
        return {"HandleRefId": value}

    def wrap(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.define(self.reserve(), data)


@dataclass
class GraphNode:
    wrapper: dict[str, Any]
    inputs: dict[str, dict[str, Any]]
    outputs: dict[str, dict[str, Any]]

    @property
    def data(self) -> dict[str, Any]:
        return self.wrapper["Data"]


class GraphBuilder:
    def __init__(self) -> None:
        self.handles = Handles()
        graph_id = self.handles.reserve()
        self.graph = self.handles.define(
            graph_id, {"$type": "questGraphDefinition", "nodes": []}
        )

    def socket(self, name: str, socket_type: str) -> dict[str, Any]:
        return self.handles.wrap(
            {
                "$type": "questSocketDefinition",
                "connections": [],
                "name": cname(name),
                "type": socket_type,
            }
        )

    def node(
        self,
        quest_id: int,
        node_type: str,
        *,
        inputs: tuple[str, ...],
        outputs: tuple[str, ...] = ("Out",),
        properties: dict[str, Any] | None = None,
    ) -> GraphNode:
        handle_id = self.handles.reserve()
        cut = self.socket("CutDestination", "CutDestination")
        input_sockets = {name: self.socket(name, "Input") for name in inputs}
        output_sockets = {name: self.socket(name, "Output") for name in outputs}
        data: dict[str, Any] = {
            "$type": node_type,
            "id": quest_id,
            "sockets": [
                cut,
                *input_sockets.values(),
                *output_sockets.values(),
            ],
        }
        if properties:
            data.update(properties)
        wrapper = self.handles.define(handle_id, data)
        self.graph["Data"]["nodes"].append(wrapper)
        return GraphNode(wrapper, input_sockets, output_sockets)

    @staticmethod
    def replace_socket(
        node: GraphNode,
        socket: dict[str, Any],
        replacement: dict[str, Any],
    ) -> None:
        index = next(
            index
            for index, candidate in enumerate(node.data["sockets"])
            if candidate is socket
        )
        node.data["sockets"][index] = replacement

    def connect(
        self,
        source: GraphNode,
        destination: GraphNode,
        *,
        source_socket: str = "Out",
        destination_socket: str = "In",
    ) -> None:
        source_handle = source.outputs[source_socket]
        destination_handle = destination.inputs[destination_socket]
        connection_id = self.handles.reserve()
        destination_handle["Data"]["connections"].append(
            self.handles.ref(connection_id)
        )
        connection = self.handles.define(
            connection_id,
            {
                "$type": "graphGraphConnectionDefinition",
                "destination": destination_handle,
                "source": self.handles.ref(source_handle),
            },
        )
        source_handle["Data"]["connections"].append(connection)
        self.replace_socket(
            destination,
            destination_handle,
            self.handles.ref(destination_handle),
        )

    def connect_to_output(
        self,
        source: GraphNode,
        output: GraphNode,
        *,
        source_socket: str = "Out",
    ) -> None:
        source_handle = source.outputs[source_socket]
        destination_handle = output.inputs["In"]
        connection_id = self.handles.reserve()
        source_handle["Data"]["connections"].append(self.handles.ref(connection_id))
        connection = self.handles.define(
            connection_id,
            {
                "$type": "graphGraphConnectionDefinition",
                "destination": self.handles.ref(destination_handle),
                "source": source_handle,
            },
        )
        destination_handle["Data"]["connections"].append(connection)
        self.replace_socket(source, source_handle, self.handles.ref(source_handle))


def input_node(builder: GraphBuilder) -> GraphNode:
    return builder.node(
        0,
        "questInputNodeDefinition",
        inputs=(),
        properties={"socketName": cname("In1")},
    )


def output_node(builder: GraphBuilder) -> GraphNode:
    return builder.node(
        1,
        "questOutputNodeDefinition",
        inputs=("In",),
        outputs=(),
        properties={"socketName": cname("Out1"), "type": "Terminating"},
    )


def fact_condition_node(
    builder: GraphBuilder, quest_id: int, fact_name: str
) -> GraphNode:
    comparison = builder.handles.wrap(
        {
            "$type": "questVarComparison_ConditionType",
            "comparisonType": "Equal",
            "factName": fact_name,
            "value": 0,
        }
    )
    condition = builder.handles.wrap(
        {"$type": "questFactsDBCondition", "type": comparison}
    )
    return builder.node(
        quest_id,
        "questConditionNodeDefinition",
        inputs=("In",),
        outputs=("True", "False"),
        properties={"condition": condition},
    )


def journal_path(
    builder: GraphBuilder, real_path: str, class_name: str
) -> dict[str, Any]:
    return builder.handles.wrap(
        {
            "$type": "gameJournalPath",
            "className": cname(class_name),
            "editorPath": "",
            "fileEntryIndex": 2,
            "realPath": real_path,
        }
    )


def journal_node(
    builder: GraphBuilder,
    quest_id: int,
    real_path: str,
    class_name: str,
) -> GraphNode:
    node_type = builder.handles.wrap(
        {
            "$type": "questJournalQuestEntry_NodeType",
            "optional": 0,
            "path": journal_path(builder, real_path, class_name),
            "sendNotification": 1,
            "trackQuest": 1,
            "version": "Initial",
        }
    )
    return builder.node(
        quest_id,
        "questJournalNodeDefinition",
        inputs=("Active", "Inactive", "Succeeded", "Failed"),
        properties={"type": node_type},
    )


def realtime_delay_node(builder: GraphBuilder, quest_id: int) -> GraphNode:
    delay = builder.handles.wrap(
        {
            "$type": "questRealtimeDelay_ConditionType",
            "hours": 0,
            "miliseconds": 0,
            "minutes": 0,
            "seconds": 10,
        }
    )
    condition = builder.handles.wrap({"$type": "questTimeCondition", "type": delay})
    return builder.node(
        quest_id,
        "questPauseConditionNodeDefinition",
        inputs=("In",),
        properties={"condition": condition},
    )


def set_fact_node(builder: GraphBuilder, quest_id: int, fact_name: str) -> GraphNode:
    node_type = builder.handles.wrap(
        {
            "$type": "questSetVar_NodeType",
            "factName": fact_name,
            "setExactValue": 1,
            "value": 1,
        }
    )
    return builder.node(
        quest_id,
        "questFactsDBManagerNodeDefinition",
        inputs=("In",),
        properties={"type": node_type},
    )


def build_questphase() -> dict[str, Any]:
    builder = GraphBuilder()
    phase_input = input_node(builder)
    phase_output = output_node(builder)
    guard = fact_condition_node(builder, 10, "cqa001_completed")
    quest_active = journal_node(
        builder, 11, "quests/minor_quest/cqa001", "gameJournalQuest"
    )
    objective_active = journal_node(
        builder,
        12,
        "quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait",
        "gameJournalQuestObjective",
    )
    delay = realtime_delay_node(builder, 13)
    objective_succeeded = journal_node(
        builder,
        14,
        "quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait",
        "gameJournalQuestObjective",
    )
    completed = set_fact_node(builder, 15, "cqa001_completed")
    quest_succeeded = journal_node(
        builder, 16, "quests/minor_quest/cqa001", "gameJournalQuest"
    )

    builder.connect(phase_input, guard)
    builder.connect(
        guard, quest_active, source_socket="True", destination_socket="Active"
    )
    builder.connect(quest_active, objective_active, destination_socket="Active")
    builder.connect(objective_active, delay)
    builder.connect(delay, objective_succeeded, destination_socket="Succeeded")
    builder.connect(objective_succeeded, completed)
    builder.connect(completed, quest_succeeded, destination_socket="Succeeded")
    builder.connect_to_output(guard, phase_output, source_socket="False")
    builder.connect_to_output(quest_succeeded, phase_output)

    return {
        "Header": {
            "WolvenKitVersion": "8.19.0",
            "WKitJsonVersion": "0.0.9",
            "GameVersion": 2310,
            "ExportedDateTime": "1970-01-01T00:00:00Z",
            "DataType": "CR2W",
            "ArchiveFileName": ("mod\\cqa\\cqa001\\phases\\cqa001.questphase"),
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


def localized_string(key: str) -> dict[str, str]:
    return {"unk1": "0", "value": key}


def journal_entry(
    entry_type: str, entry_id: str, entries: list[dict[str, Any]], **extra: Any
) -> dict[str, Any]:
    data = {
        "$type": entry_type,
        "entries": entries,
        "id": entry_id,
        "journalEntryOverrideDataList": [],
    }
    data.update(extra)
    return data


def build_journal() -> dict[str, Any]:
    objective = Handles.define(
        "5",
        journal_entry(
            "gameJournalQuestObjective",
            "cqa001_01_obj_wait",
            [],
            counter=0,
            description=localized_string("cqa_cqa001_objective_wait"),
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
            optional=0,
        ),
    )
    phase = Handles.define(
        "4",
        journal_entry(
            "gameJournalQuestPhase",
            "cqa001_01",
            [objective],
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
            "cqa001",
            [phase],
            districtID="",
            recommendedLevelID={
                "$type": "TweakDBID",
                "$storage": "uint64",
                "$value": "0",
            },
            title=localized_string("cqa_cqa001_title"),
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
            "ArchiveFileName": "mod\\cqa\\cqa001\\journal\\cqa001.journal",
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
        "cqa_cqa001_title": "First Signal",
        "cqa_cqa001_objective_wait": "Wait for the signal.",
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
                "mod\\cqa\\cqa001\\localization\\en-us\\onscreens\\cqa001.json"
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


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    write_json(
        RAW_ROOT / "phases" / "cqa001.questphase.json",
        build_questphase(),
    )
    write_json(
        RAW_ROOT / "journal" / "cqa001.journal.json",
        build_journal(),
    )
    write_json(
        RAW_ROOT / "localization" / "en-us" / "onscreens" / "cqa001.json.json",
        build_localization(),
    )


if __name__ == "__main__":
    main()
