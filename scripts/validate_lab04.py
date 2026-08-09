#!/usr/bin/env python3
"""Validate the Lab 4 external-phase example and its generated diagrams.

The default check is standard-library-only. Pass ``--wkit PATH`` to repeat
the WolvenKit 8.19.0 JSON-to-CR2W cook and CR2W-to-JSON inspection locally.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import math
import struct
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-04-handoff-point"
START = LAB / "start"
COMPLETED = LAB / "completed"
BUILDER = ROOT / "scripts" / "build_lab04_sources.py"
DIAGRAM_BUILDER = ROOT / "scripts" / "build_lab04_diagrams.py"
ASSETS = ROOT / "assets" / "diagrams" / "lab-04"
PUBLISHED = ROOT / "book" / "src" / "images" / "lab-04"

BASELINE = {
    "cyberpunk_2077": "2.31a",
    "wolvenkit": "8.19.0",
    "archive_xl": "1.27.0",
    "red4ext": "1.30.0",
    "redscript": "0.5.31",
}
DEPOT_PATHS = (
    "mod\\cqa\\cqa004\\phases\\cqa004.questphase",
    "mod\\cqa\\cqa004\\phases\\cqa004_boundary.questphase",
    "mod\\cqa\\cqa004\\journal\\cqa004.journal",
    "mod\\cqa\\cqa004\\localization\\en-us\\onscreens\\cqa004.json",
    "mod\\cqa\\cqa004\\world\\cqa004_handoff.streamingblock",
    "mod\\cqa\\cqa004\\world\\cqa004_handoff.streamingsector",
    "mod\\cqa\\cqa004\\world\\cqa004_always_loaded.streamingsector",
)
REGISTERED_PATHS = (
    DEPOT_PATHS[0],
    DEPOT_PATHS[2],
    DEPOT_PATHS[3],
    DEPOT_PATHS[4],
)
ROOT_TYPES = {
    DEPOT_PATHS[0]: "questQuestPhaseResource",
    DEPOT_PATHS[1]: "questQuestPhaseResource",
    DEPOT_PATHS[2]: "gameJournalResource",
    DEPOT_PATHS[3]: "JsonResource",
    DEPOT_PATHS[4]: "worldStreamingBlock",
    DEPOT_PATHS[5]: "worldStreamingSector",
    DEPOT_PATHS[6]: "worldStreamingSector",
}

START_STATIC = {
    "CQA_Lab04_HandoffPoint_Start.cpmodproj",
    "README.md",
    "source/resources/CQA_Lab04_HandoffPoint_Start.archive.xl",
}
COMPLETED_STATIC = {
    "CQA_Lab04_HandoffPoint.cpmodproj",
    "README.md",
    "example.json",
    "runtime-acceptance.json",
    "source/resources/CQA_Lab04_HandoffPoint.archive.xl",
}
ASSET_FILES = {
    "cqa004.questphase.layout.json",
    "cqa004_boundary.questphase.layout.json",
    "cqa004.root.questphase.svg",
    "cqa004.child.questphase.svg",
    "cqa004.resource-chain.svg",
    "cqa004.handoff-contract.svg",
}
PUBLISHED_FILES = {
    "cqa004.root.questphase.svg",
    "cqa004.child.questphase.svg",
    "cqa004.resource-chain.svg",
    "cqa004.handoff-contract.svg",
}

ROOT_COMPLETED_TYPES = {
    0: "questInputNodeDefinition",
    1: "questOutputNodeDefinition",
    10: "questConditionNodeDefinition",
    11: "questJournalNodeDefinition",
    12: "questJournalNodeDefinition",
    13: "questPhaseNodeDefinition",
    14: "questJournalNodeDefinition",
    15: "questPauseConditionNodeDefinition",
    16: "questJournalNodeDefinition",
    17: "questJournalNodeDefinition",
    18: "questFactsDBManagerNodeDefinition",
    19: "questJournalNodeDefinition",
}
ROOT_COMPLETED_EDGES = {
    (0, "Out", 10, "In"),
    (10, "False", 1, "In"),
    (10, "True", 11, "Active"),
    (11, "Out", 12, "Active"),
    (12, "Out", 13, "In1"),
    (13, "Out1", 14, "Active"),
    (14, "Out", 15, "In"),
    (15, "Out", 16, "Succeeded"),
    (16, "Out", 17, "Succeeded"),
    (17, "Out", 18, "In"),
    (18, "Out", 19, "Succeeded"),
    (19, "Out", 1, "In"),
}
CHILD_COMPLETED_TYPES = {
    0: "questInputNodeDefinition",
    1: "questOutputNodeDefinition",
    10: "questJournalNodeDefinition",
    11: "questMappinManagerNodeDefinition",
    12: "questPauseConditionNodeDefinition",
    13: "questMappinManagerNodeDefinition",
    14: "questJournalNodeDefinition",
    15: "questJournalNodeDefinition",
    16: "questPauseConditionNodeDefinition",
    17: "questJournalNodeDefinition",
}
CHILD_COMPLETED_EDGES = {
    (0, "Out", 10, "Active"),
    (10, "Out", 11, "Active"),
    (11, "Out", 12, "In"),
    (12, "Out", 13, "Inactive"),
    (13, "Out", 14, "Succeeded"),
    (14, "Out", 15, "Active"),
    (15, "Out", 16, "In"),
    (16, "Out", 17, "Succeeded"),
    (17, "Out", 1, "In"),
}


class ValidationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        shown = path.relative_to(ROOT)
    except ValueError:
        shown = path
    require(path.is_file(), f"missing {shown}")
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream, object_pairs_hook=reject_duplicate_keys)
    require(isinstance(value, dict), f"{shown}: root must be object")
    return value


def actual_files(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}


def raw_relative(depot_path: str) -> str:
    return "source/raw/" + depot_path.replace("\\", "/") + ".json"


def cooked_relative(depot_path: str) -> str:
    return "source/archive/" + depot_path.replace("\\", "/")


def expected_checkpoint_files(*, completed: bool) -> set[str]:
    paired = {raw_relative(path) for path in DEPOT_PATHS} | {
        cooked_relative(path) for path in DEPOT_PATHS
    }
    return paired | (COMPLETED_STATIC if completed else START_STATIC)


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def generate_into(root: Path, name: str) -> None:
    module = load_module(BUILDER, name)
    module.CHECKPOINTS = {"start": root / "start", "completed": root / "completed"}
    module.main()


def validate_inventories_and_generation() -> None:
    require(actual_files(START) == expected_checkpoint_files(completed=False), "Lab 4 start inventory changed")
    require(actual_files(COMPLETED) == expected_checkpoint_files(completed=True), "Lab 4 completed inventory changed")
    require(actual_files(ASSETS) == ASSET_FILES, "Lab 4 diagram-source inventory changed")
    require(actual_files(PUBLISHED) == PUBLISHED_FILES, "Lab 4 published-diagram inventory changed")

    with tempfile.TemporaryDirectory(prefix="cqa-lab04-a-") as first_dir, tempfile.TemporaryDirectory(prefix="cqa-lab04-b-") as second_dir:
        first = Path(first_dir)
        second = Path(second_dir)
        generate_into(first, "cqa_build_lab04_a")
        generate_into(second, "cqa_build_lab04_b")
        first_files = actual_files(first)
        require(first_files == actual_files(second), "two Lab 4 generation runs emitted different files")
        expected_raw = {f"{checkpoint}/{raw_relative(path)}" for checkpoint in ("start", "completed") for path in DEPOT_PATHS}
        require(first_files == expected_raw, "Lab 4 generator raw inventory changed")
        for relative in sorted(first_files):
            generated_a = first / relative
            generated_b = second / relative
            checked = LAB / relative
            require(generated_a.read_bytes() == generated_b.read_bytes(), f"{relative}: generation is nondeterministic")
            require(generated_a.read_bytes() == checked.read_bytes(), f"{relative}: checked CR2W-JSON is stale")
            require(str(ROOT).encode() not in generated_a.read_bytes(), f"{relative}: generated source contains an absolute repository path")


def archive_xl_text() -> str:
    return """quest:
  phases:
  - path: mod\\cqa\\cqa004\\phases\\cqa004.questphase
    parent: base\\quest\\cyberpunk2077.quest

journal:
- mod\\cqa\\cqa004\\journal\\cqa004.journal

localization:
  onscreens:
    en-us:
    - mod\\cqa\\cqa004\\localization\\en-us\\onscreens\\cqa004.json

streaming:
  blocks:
  - mod\\cqa\\cqa004\\world\\cqa004_handoff.streamingblock
"""


def validate_projects_registration_and_pairs() -> None:
    for checkpoint, project_name, mod_name, manifest_name in (
        (START, "CQA Lab 04 Handoff Point Start", "CQA_Lab04_HandoffPoint_Start", "CQA_Lab04_HandoffPoint_Start.archive.xl"),
        (COMPLETED, "CQA Lab 04 Handoff Point", "CQA_Lab04_HandoffPoint", "CQA_Lab04_HandoffPoint.archive.xl"),
    ):
        project = checkpoint / f"{mod_name}.cpmodproj"
        root = ET.parse(project).getroot()
        require(root.tag == "CP77Mod", f"{project.name}: project root changed")
        values = {child.tag: child.text for child in root}
        require(values.get("Name") == project_name and values.get("ModName") == mod_name, f"{project.name}: identity changed")
        archive_xl = checkpoint / "source" / "resources" / manifest_name
        content = archive_xl.read_text(encoding="utf-8")
        require(content == archive_xl_text(), f"{archive_xl.name}: registration manifest changed")
        require("cqa004_boundary.questphase" not in content, f"{archive_xl.name}: external child must not be registered")

        for depot_path, root_type in ROOT_TYPES.items():
            raw = checkpoint / raw_relative(depot_path)
            cooked = checkpoint / cooked_relative(depot_path)
            source = load_json(raw)
            header = source.get("Header", {})
            chunk = source.get("Data", {}).get("RootChunk", {})
            require(
                header.get("WolvenKitVersion") == "8.19.0"
                and header.get("WKitJsonVersion") == "0.0.9"
                and header.get("GameVersion") == 2310
                and header.get("DataType") == "CR2W"
                and header.get("ArchiveFileName") == depot_path,
                f"{raw.relative_to(ROOT)}: WolvenKit baseline or depot path changed",
            )
            require(chunk.get("$type") == root_type, f"{raw.relative_to(ROOT)}: root type changed")
            payload = cooked.read_bytes()
            require(payload.startswith(b"CR2W") and root_type.encode("ascii") in payload, f"{cooked.relative_to(ROOT)}: cooked CR2W provenance changed")

    for phase_path in DEPOT_PATHS[:2]:
        require(
            (START / cooked_relative(phase_path)).read_bytes()
            != (COMPLETED / cooked_relative(phase_path)).read_bytes(),
            f"{phase_path}: start and completed phase binaries must differ",
        )
    for shared_path in DEPOT_PATHS[2:]:
        require(
            (START / cooked_relative(shared_path)).read_bytes()
            == (COMPLETED / cooked_relative(shared_path)).read_bytes(),
            f"{shared_path}: non-phase checkpoint resources must remain identical",
        )


def collect_handles(value: Any, handles: dict[str, dict[str, Any]]) -> None:
    if isinstance(value, dict):
        handle_id = value.get("HandleId")
        if isinstance(handle_id, str):
            require(handle_id not in handles, f"duplicate CR2W handle {handle_id}")
            data = value.get("Data")
            require(isinstance(data, dict), f"handle {handle_id} has no data")
            handles[handle_id] = data
        for child in value.values():
            collect_handles(child, handles)
    elif isinstance(value, list):
        for child in value:
            collect_handles(child, handles)


def resolve(value: Any, handles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    require(isinstance(value, dict), "expected CR2W handle")
    identifier = value.get("HandleRefId", value.get("HandleId"))
    require(isinstance(identifier, str) and identifier in handles, "unresolved CR2W handle")
    return handles[identifier]


def iter_objects(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_objects(child)


def cname_value(value: Any) -> str:
    require(isinstance(value, dict), "expected CName")
    return str(value.get("$value"))


def resource_value(value: Any) -> tuple[str, str]:
    require(isinstance(value, dict), "expected resource reference")
    path = value.get("DepotPath")
    require(isinstance(path, dict), "resource reference has no DepotPath")
    return str(path.get("$value")), str(value.get("Flags"))


def cname(value: str) -> dict[str, str]:
    return {"$type": "CName", "$storage": "string", "$value": value}


def node_ref(value: str | int) -> dict[str, str]:
    return {
        "$type": "NodeRef",
        "$storage": "string" if isinstance(value, str) else "uint64",
        "$value": str(value),
    }


def resource_path(value: str | int, *, flags: str = "Soft") -> dict[str, Any]:
    return {
        "DepotPath": {
            "$type": "ResourcePath",
            "$storage": "string" if isinstance(value, str) else "uint64",
            "$value": str(value),
        },
        "Flags": flags,
    }


def phase_graph(source: dict[str, Any]) -> tuple[dict[str, Any], dict[int, dict[str, Any]], dict[str, dict[str, Any]]]:
    root = source["Data"]["RootChunk"]
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(source, handles)
    graph = resolve(root["graph"], handles)
    nodes = {int(resolve(wrapper, handles)["id"]): resolve(wrapper, handles) for wrapper in graph["nodes"]}
    return root, nodes, handles


def socket_contract(node: dict[str, Any], handles: dict[str, dict[str, Any]]) -> list[tuple[str, str, int]]:
    result = []
    for wrapper in node["sockets"]:
        socket = resolve(wrapper, handles)
        result.append((cname_value(socket["name"]), str(socket["type"]), len(socket["connections"])))
    return result


def expected_sockets(red_type: str) -> list[tuple[str, str]]:
    if red_type == "questInputNodeDefinition":
        return [("CutDestination", "CutDestination"), ("Out", "Output")]
    if red_type == "questOutputNodeDefinition":
        return [("CutDestination", "CutDestination"), ("In", "Input")]
    if red_type == "questConditionNodeDefinition":
        return [("CutDestination", "CutDestination"), ("In", "Input"), ("True", "Output"), ("False", "Output")]
    if red_type == "questJournalNodeDefinition":
        return [("CutDestination", "CutDestination"), ("Active", "Input"), ("Inactive", "Input"), ("Succeeded", "Input"), ("Failed", "Input"), ("Out", "Output")]
    if red_type == "questMappinManagerNodeDefinition":
        return [("CutDestination", "CutDestination"), ("Active", "Input"), ("Inactive", "Input"), ("Out", "Output")]
    if red_type == "questPhaseNodeDefinition":
        return [("CutDestination", "CutDestination"), ("In1", "Input"), ("Out1", "Output")]
    return [("CutDestination", "CutDestination"), ("In", "Input"), ("Out", "Output")]


def parsed_edges(source: Path) -> set[tuple[int, str, int, str]]:
    renderer = load_module(ROOT / "scripts" / "render_quest_graph.py", f"cqa_render_{hash(source)}")
    nodes, edges = renderer.parse_graph(load_json(source))
    del nodes
    return {(edge.source, edge.source_socket, edge.destination, edge.destination_socket) for edge in edges}


def validate_phase(
    path: Path,
    *,
    expected_types: dict[int, str],
    expected_edges: set[tuple[int, str, int, str]],
    root_prefabs: list[str],
) -> tuple[dict[int, dict[str, Any]], dict[str, dict[str, Any]]]:
    source = load_json(path)
    root, nodes, handles = phase_graph(source)
    require(set(nodes) == set(expected_types), f"{path.name}: node IDs changed")
    require({node_id: node["$type"] for node_id, node in nodes.items()} == expected_types, f"{path.name}: node types changed")
    require(parsed_edges(path) == expected_edges, f"{path.name}: graph edges changed")
    prefabs = [cname_value(entry["prefabNodeRef"]) for entry in root["phasePrefabs"]]
    require(prefabs == root_prefabs and root.get("inplacePhases") == [], f"{path.name}: phase prefab scope changed")
    for node_id, node in nodes.items():
        sockets = socket_contract(node, handles)
        require([(name, kind) for name, kind, _ in sockets] == expected_sockets(node["$type"]), f"{path.name} node {node_id}: socket contract changed")
        cut = next(item for item in sockets if item[0] == "CutDestination")
        require(cut[2] == 0, f"{path.name} node {node_id}: CutDestination must remain unwired")
    require(cname_value(nodes[0]["socketName"]) == "In1", f"{path.name}: child/root input name changed")
    require(cname_value(nodes[1]["socketName"]) == "Out1" and nodes[1]["type"] == "Terminating", f"{path.name}: output must remain terminating Out1")
    return nodes, handles


def find_typed(value: Any, red_type: str, handles: dict[str, dict[str, Any]], seen: set[str] | None = None) -> dict[str, Any] | None:
    if seen is None:
        seen = set()
    if isinstance(value, dict):
        identifier = value.get("HandleRefId", value.get("HandleId"))
        if isinstance(identifier, str):
            if identifier in seen:
                return None
            seen.add(identifier)
            value = resolve(value, handles)
        if value.get("$type") == red_type:
            return value
        for key, child in value.items():
            if key not in {"HandleId", "HandleRefId"}:
                found = find_typed(child, red_type, handles, seen)
                if found is not None:
                    return found
    elif isinstance(value, list):
        for child in value:
            found = find_typed(child, red_type, handles, seen)
            if found is not None:
                return found
    return None


def validate_graphs() -> None:
    start_root = START / raw_relative(DEPOT_PATHS[0])
    start_child = START / raw_relative(DEPOT_PATHS[1])
    completed_root = COMPLETED / raw_relative(DEPOT_PATHS[0])
    completed_child = COMPLETED / raw_relative(DEPOT_PATHS[1])

    start_root_types = {0: "questInputNodeDefinition", 1: "questOutputNodeDefinition", 13: "questPhaseNodeDefinition"}
    start_root_edges = {(0, "Out", 13, "In1"), (13, "Out1", 1, "In")}
    start_child_types = {0: "questInputNodeDefinition", 1: "questOutputNodeDefinition"}
    start_child_edges = {(0, "Out", 1, "In")}
    start_nodes, _ = validate_phase(start_root, expected_types=start_root_types, expected_edges=start_root_edges, root_prefabs=["#cqa004_pr_handoff"])
    validate_phase(start_child, expected_types=start_child_types, expected_edges=start_child_edges, root_prefabs=[])
    root_nodes, root_handles = validate_phase(completed_root, expected_types=ROOT_COMPLETED_TYPES, expected_edges=ROOT_COMPLETED_EDGES, root_prefabs=["#cqa004_pr_handoff"])
    child_nodes, child_handles = validate_phase(completed_child, expected_types=CHILD_COMPLETED_TYPES, expected_edges=CHILD_COMPLETED_EDGES, root_prefabs=[])

    for graph_name, nodes in (("root", root_nodes), ("child", child_nodes)):
        require(set(nodes[0]) == {"$type", "id", "sockets", "socketName"}, f"{graph_name} input fields changed")
        require(set(nodes[1]) == {"$type", "id", "sockets", "socketName", "type"}, f"{graph_name} output fields changed")
        require(nodes[1]["type"] == "Terminating" and cname_value(nodes[1]["socketName"]) == "Out1", f"{graph_name} output must remain terminating Out1")

    for phase_node in (start_nodes[13], root_nodes[13]):
        require(set(phase_node) == {"$type", "id", "sockets", "phaseGraph", "phaseInstancePrefabs", "phaseResource", "saveLock", "unfreezingTriggerNodeRef"}, "external phase node fields changed")
        require(phase_node["phaseGraph"] is None and phase_node["phaseInstancePrefabs"] == [] and phase_node["saveLock"] == 0, "external phase node inline/prefab/save contract changed")
        require(resource_value(phase_node["phaseResource"]) == (DEPOT_PATHS[1], "Soft"), "external phaseResource must remain the soft child path")
        require(phase_node["unfreezingTriggerNodeRef"] == {"$type": "NodeRef", "$storage": "uint64", "$value": "0"}, "external phase unfreezing ref must remain zero")

    facts = {str(item.get("factName")) for item in iter_objects(load_json(completed_root)) if "factName" in item}
    require(facts == {"cqa004_completed"}, "root graph must use only cqa004_completed")
    require(not any("factName" in item for item in iter_objects(load_json(completed_child))), "child graph must not read or write persistent facts")

    guard_condition = resolve(root_nodes[10]["condition"], root_handles)
    guard_comparison = resolve(guard_condition["type"], root_handles)
    require(
        set(root_nodes[10]) == {"$type", "id", "sockets", "condition"}
        and guard_condition == {"$type": "questFactsDBCondition", "type": guard_condition["type"]}
        and guard_comparison
        == {
            "$type": "questVarComparison_ConditionType",
            "comparisonType": "Equal",
            "factName": "cqa004_completed",
            "value": 0,
        },
        "root completion guard payload changed",
    )
    fact_writer = resolve(root_nodes[18]["type"], root_handles)
    require(
        set(root_nodes[18]) == {"$type", "id", "sockets", "type"}
        and fact_writer
        == {
            "$type": "questSetVar_NodeType",
            "factName": "cqa004_completed",
            "setExactValue": 1,
            "value": 1,
        },
        "root completion fact write changed",
    )

    journal_contract = {
        ("root", 11): ("quests/minor_quest/cqa004", "gameJournalQuest"),
        ("root", 12): ("quests/minor_quest/cqa004/cqa004_01", "gameJournalQuestPhase"),
        ("root", 14): ("quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_confirm", "gameJournalQuestObjective"),
        ("root", 16): ("quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_confirm", "gameJournalQuestObjective"),
        ("root", 17): ("quests/minor_quest/cqa004/cqa004_01", "gameJournalQuestPhase"),
        ("root", 19): ("quests/minor_quest/cqa004", "gameJournalQuest"),
        ("child", 10): ("quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_reach", "gameJournalQuestObjective"),
        ("child", 14): ("quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_reach", "gameJournalQuestObjective"),
        ("child", 15): ("quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_leave", "gameJournalQuestObjective"),
        ("child", 17): ("quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_leave", "gameJournalQuestObjective"),
    }
    graph_data = {"root": (root_nodes, root_handles), "child": (child_nodes, child_handles)}
    for (graph_name, node_id), (real_path, class_name) in journal_contract.items():
        nodes, handles = graph_data[graph_name]
        node = nodes[node_id]
        require(set(node) == {"$type", "id", "sockets", "type"}, f"{graph_name} journal node {node_id}: fields changed")
        node_type = resolve(node["type"], handles)
        require(
            set(node_type) == {"$type", "optional", "path", "sendNotification", "trackQuest", "version"}
            and node_type["$type"] == "questJournalQuestEntry_NodeType"
            and node_type["optional"] == 0
            and node_type["sendNotification"] == 1
            and node_type["trackQuest"] == 1
            and node_type["version"] == "Initial",
            f"{graph_name} journal node {node_id}: presentation contract changed",
        )
        journal_path = resolve(node_type["path"], handles)
        require(
            journal_path
            == {
                "$type": "gameJournalPath",
                "className": cname(class_name),
                "editorPath": "",
                "fileEntryIndex": 2,
                "realPath": real_path,
            },
            f"{graph_name} journal node {node_id}: path/class changed",
        )

    delay = find_typed(root_nodes[15].get("condition"), "questRealtimeDelay_ConditionType", root_handles)
    require(delay == {"$type": "questRealtimeDelay_ConditionType", "hours": 0, "miliseconds": 0, "minutes": 0, "seconds": 30}, "parent confirmation delay must remain 30 realtime seconds")
    for node_id, trigger_ref, condition_type in ((12, "#cqa004_tr_reach", "IsInside"), (16, "#cqa004_tr_leave", "IsOutside")):
        node = child_nodes[node_id]
        require(set(node) == {"$type", "id", "sockets", "condition"}, f"child node {node_id}: trigger-gate fields changed")
        condition = resolve(node["condition"], child_handles)
        require(
            condition
            == {
                "$type": "questTriggerCondition",
                "activatorRef": {
                    "$type": "gameEntityReference",
                    "dynamicEntityUniqueName": cname("None"),
                    "names": [],
                    "reference": node_ref(0),
                    "sceneActorContextName": cname("None"),
                    "slotName": cname("None"),
                    "type": "EntityRef",
                },
                "isPlayerActivator": 1,
                "triggerAreaRef": node_ref(trigger_ref),
                "type": condition_type,
            },
            f"child node {node_id}: trigger condition changed",
        )
    for node_id in (11, 13):
        node = child_nodes[node_id]
        require(set(node) == {"$type", "id", "sockets", "disablePreviousMappins", "path"}, f"child mappin node {node_id}: fields changed")
        require(node.get("disablePreviousMappins") == 0, f"child mappin node {node_id}: disablePreviousMappins changed")
        path = resolve(node["path"], child_handles)
        require(
            path
            == {
                "$type": "gameJournalPath",
                "className": cname("gameJournalQuestMapPin"),
                "editorPath": "",
                "fileEntryIndex": 2,
                "realPath": "quests/minor_quest/cqa004/cqa004_01/cqa004_01_obj_reach/cqa004_01_qmp_handoff",
            },
            f"child mappin node {node_id}: journal path changed",
        )


def decode_outline(outline: dict[str, Any], radius: float, count: int, height: float) -> None:
    payload = base64.b64decode(outline["buffer"], validate=True)
    require(len(payload) == 4 + count * 16 + 4, "AreaShapeOutline buffer length changed")
    require(struct.unpack_from("<I", payload)[0] == count, "AreaShapeOutline point count changed")
    points = outline["points"]
    require(len(points) == count and math.isclose(float(outline["height"]), height), "AreaShapeOutline points/height changed")
    for index, point in enumerate(points):
        expected_x = struct.unpack("<f", struct.pack("<f", math.cos(2 * math.pi * index / count) * radius))[0]
        expected_y = struct.unpack("<f", struct.pack("<f", math.sin(2 * math.pi * index / count) * radius))[0]
        expected = (expected_x, expected_y, 0.0, 1.0)
        packed = struct.unpack_from("<ffff", payload, 4 + index * 16)
        actual = (float(point["X"]), float(point["Y"]), float(point["Z"]), packed[3])
        require(all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(actual, expected)), f"AreaShapeOutline point {index} changed")
        require(all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(packed, expected)), f"AreaShapeOutline buffer point {index} changed")
    require(math.isclose(struct.unpack_from("<f", payload, len(payload) - 4)[0], height), "AreaShapeOutline buffer height changed")


def vector_values(value: Any, dimensions: int, context: str) -> tuple[float, ...]:
    require(isinstance(value, dict), f"{context}: expected vector")
    keys = ("X", "Y", "Z", "W")[:dimensions]
    expected_keys = {"$type", *keys}
    require(set(value) == expected_keys, f"{context}: vector fields changed")
    return tuple(float(value[key]) for key in keys)


def close_values(actual: tuple[float, ...], expected: tuple[float, ...], context: str) -> None:
    require(len(actual) == len(expected), f"{context}: vector dimensions changed")
    require(all(math.isclose(left, right, abs_tol=1e-6) for left, right in zip(actual, expected)), f"{context}: expected {expected}, got {actual}")


def sector_shell(
    source: dict[str, Any],
    category: str,
    level: int,
    node_count: int,
    context: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, dict[str, Any]]]:
    root = source["Data"]["RootChunk"]
    require(
        set(root)
        == {
            "$type",
            "category",
            "cookingPlatform",
            "externInplaceResource",
            "level",
            "localInplaceResource",
            "nodeData",
            "nodeRefs",
            "nodes",
            "persistentNodeIndex",
            "persistentNodes",
            "variantIndices",
            "variantNodes",
            "version",
        },
        f"{context}: sector root fields changed",
    )
    require(root["$type"] == "worldStreamingSector" and root["category"] == category and root["level"] == level, f"{context}: category/level changed")
    require(root["cookingPlatform"] == "PLATFORM_None" and root["version"] == 62, f"{context}: platform/version changed")
    require(root["externInplaceResource"] == resource_path(0) and root["localInplaceResource"] == [], f"{context}: inplace resource fields changed")
    require(root["persistentNodeIndex"] == 0 and root["persistentNodes"] == [], f"{context}: persistent node fields changed")
    require(root["variantIndices"] == [0] and root["variantNodes"] == [], f"{context}: variant fields changed")
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(root, handles)
    require(len(root["nodes"]) == node_count and len(root["nodeRefs"]) == node_count, f"{context}: node/ref count changed")
    nodes = [resolve(wrapper, handles) for wrapper in root["nodes"]]
    refs = [str(item.get("$value")) for item in root["nodeRefs"]]
    for ref in root["nodeRefs"]:
        require(ref.get("$type") == "NodeRef" and ref.get("$storage") == "string", f"{context}: nodeRef encoding changed")
    node_data = root["nodeData"]
    require(
        set(node_data) == {"BufferId", "Flags", "Type", "Data"}
        and node_data["BufferId"] == "0"
        and node_data["Flags"] == 0
        and node_data["Type"]
        == "WolvenKit.RED4.Archive.Buffer.worldNodeDataBuffer, WolvenKit.RED4, Version=8.19.0.0, Culture=neutral, PublicKeyToken=null",
        f"{context}: nodeData buffer metadata changed",
    )
    placements = node_data["Data"]
    require(isinstance(placements, list) and len(placements) == node_count, f"{context}: nodeData placement count changed")
    require([item.get("NodeIndex") for item in placements] == list(range(node_count)), f"{context}: nodeData NodeIndex no longer joins nodes[] by index")
    require(all(item.get("Id") == node_data["BufferId"] for item in placements), f"{context}: placement Id no longer joins nodeData BufferId")
    return nodes, placements, refs, handles


def validate_placement(
    item: dict[str, Any],
    *,
    node_index: int,
    ref: str,
    position: tuple[float, float, float],
    max_distance: float,
    opaque_distance: float,
    context: str,
) -> None:
    require(
        set(item)
        == {
            "Id",
            "NodeIndex",
            "Position",
            "Orientation",
            "Scale",
            "Pivot",
            "Bounds",
            "QuestPrefabRefHash",
            "UkHash1",
            "CookedPrefabData",
            "MaxStreamingDistance",
            "UkFloat1",
            "Uk10",
            "Uk11",
            "Uk12",
            "Uk13",
            "Uk14",
        },
        f"{context}: placement fields changed",
    )
    require(item["Id"] == "0" and item["NodeIndex"] == node_index, f"{context}: buffer/node index join changed")
    close_values(vector_values(item["Position"], 4, f"{context} Position"), (*position, 0), f"{context} Position")
    close_values(vector_values(item["Pivot"], 3, f"{context} Pivot"), position, f"{context} Pivot")
    require(item["Scale"] == {"$type": "Vector3", "X": 1.0, "Y": 1.0, "Z": 1.0}, f"{context}: scale changed")
    bounds = item["Bounds"]
    require(set(bounds) == {"$type", "Max", "Min"} and bounds["$type"] == "Box", f"{context}: bounds fields changed")
    close_values(vector_values(bounds["Min"], 4, f"{context} bounds min"), (*position, 0), f"{context} bounds min")
    close_values(vector_values(bounds["Max"], 4, f"{context} bounds max"), (*position, 0), f"{context} bounds max")
    orientation = item["Orientation"]
    require(set(orientation) == {"$type", "i", "j", "k", "r"} and orientation["$type"] == "Quaternion", f"{context}: orientation fields changed")
    half_angle = math.radians(88.6) / 2
    close_values((float(orientation["i"]), float(orientation["j"]), float(orientation["k"]), float(orientation["r"])), (0, 0, math.sin(half_angle), math.cos(half_angle)), f"{context} yaw")
    require(item["QuestPrefabRefHash"] == node_ref(ref), f"{context}: full prefab child ref changed")
    require(item["UkHash1"] == node_ref(0) and item["CookedPrefabData"] == resource_path(0, flags="Default"), f"{context}: prefab placeholder fields changed")
    require(item["MaxStreamingDistance"] == max_distance and item["UkFloat1"] == opaque_distance, f"{context}: streaming distances changed")
    require((item["Uk10"], item["Uk11"], item["Uk12"], item["Uk13"], item["Uk14"]) == (1024, 512, 0, "0", "0"), f"{context}: opaque nodeData fields changed")


def validate_trigger(
    node: dict[str, Any],
    handles: dict[str, dict[str, Any]],
    *,
    local_ref: str,
    radius: float,
    count: int,
    height: float,
    context: str,
) -> None:
    require(
        set(node) == {"$type", "color", "debugName", "isHostOnly", "isVisibleInGame", "notifiers", "outline", "proxyScale", "sourcePrefabHash", "tag", "tagExt"}
        and node["$type"] == "worldTriggerAreaNode",
        f"{context}: trigger node fields/type changed",
    )
    require(node["debugName"] == cname("{" + local_ref.removeprefix("#") + "}"), f"{context}: debugName changed")
    require(node["isHostOnly"] == 0 and node["isVisibleInGame"] == 1 and node["proxyScale"] is None, f"{context}: host/visibility fields changed")
    require(node["sourcePrefabHash"] == "0" and node["tag"] == "None" and node["tagExt"] == "None", f"{context}: source/tag fields changed")
    require(node["color"] == {"$type": "Color", "Alpha": 0, "Blue": 0, "Green": 0, "Red": 0}, f"{context}: color changed")
    require(len(node["notifiers"]) == 1, f"{context}: notifier count changed")
    require(resolve(node["notifiers"][0], handles) == {"$type": "questTriggerNotifier_Quest", "excludeChannels": 0, "includeChannels": "TC_Default", "isEnabled": 1}, f"{context}: notifier payload changed")
    decode_outline(resolve(node["outline"], handles), radius, count, height)


def require_streaming_box(value: Any, minimum: tuple[float, float, float], maximum: tuple[float, float, float], context: str) -> None:
    require(isinstance(value, dict) and set(value) == {"$type", "Max", "Min"} and value["$type"] == "Box", f"{context}: box fields changed")
    low = vector_values(value["Min"], 4, f"{context} min")
    high = vector_values(value["Max"], 4, f"{context} max")
    close_values(low[:3], minimum, f"{context} minimum")
    close_values(high[:3], maximum, f"{context} maximum")
    require(math.isclose(low[3], -3.40282347e38, rel_tol=1e-7) and math.isclose(high[3], 3.40282347e38, rel_tol=1e-7), f"{context}: W sentinel bounds changed")
    require(all(left <= right for left, right in zip(low, high)), f"{context}: inverted bounds")


def validate_world_journal_localization() -> None:
    quest_source = load_json(COMPLETED / raw_relative(DEPOT_PATHS[5]))
    nodes, placements, refs, handles = sector_shell(quest_source, "Quest", 255, 2, "Lab 4 Quest sector")
    require(refs == ["$/mod/cqa/cqa004/#cqa004_pr_handoff/#cqa004_tr_reach", "$/mod/cqa/cqa004/#cqa004_pr_handoff/#cqa004_tr_leave"], "Quest sector NodeRefs changed")
    validate_trigger(nodes[0], handles, local_ref="#cqa004_tr_reach", radius=25, count=16, height=12, context="Lab 4 reach trigger")
    validate_trigger(nodes[1], handles, local_ref="#cqa004_tr_leave", radius=110, count=20, height=16, context="Lab 4 leave trigger")
    validate_placement(placements[0], node_index=0, ref=refs[0], position=(-1000.02, 1497.2208, 2.3), max_distance=320, opaque_distance=280, context="Lab 4 reach placement")
    validate_placement(placements[1], node_index=1, ref=refs[1], position=(-1000.02, 1497.2208, 0.3), max_distance=360, opaque_distance=320, context="Lab 4 leave placement")

    always_source = load_json(COMPLETED / raw_relative(DEPOT_PATHS[6]))
    marker_nodes, marker_placements, marker_refs, marker_handles = sector_shell(always_source, "AlwaysLoaded", 1, 1, "Lab 4 AlwaysLoaded sector")
    require(marker_refs == ["$/mod/cqa/cqa004/#cqa004_pr_handoff/#cqa004_mp_handoff"], "marker sector NodeRef changed")
    require(
        marker_nodes[0]
        == {
            "$type": "worldStaticMarkerNode",
            "debugName": cname("{cqa004_mp_handoff}"),
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "proxyScale": None,
            "sourcePrefabHash": "0",
            "tag": "None",
            "tagExt": "None",
        },
        "Lab 4 marker node type/payload changed",
    )
    require(marker_handles, "Lab 4 marker must remain handle-backed")
    validate_placement(marker_placements[0], node_index=0, ref=marker_refs[0], position=(-1000.02, 1497.2208, 8.3), max_distance=360, opaque_distance=320, context="Lab 4 marker placement")

    block = load_json(COMPLETED / raw_relative(DEPOT_PATHS[4]))["Data"]["RootChunk"]
    block_index = {"$type": "worldStreamingBlockIndex", "oup": "Base", "rldGridCell": 0}
    require(set(block) == {"$type", "cookingPlatform", "descriptors", "index"} and block["$type"] == "worldStreamingBlock" and block["cookingPlatform"] == "PLATFORM_PC" and block["index"] == block_index, "streaming block root/index changed")
    descriptors = block["descriptors"]
    require(len(descriptors) == 2 and [item["category"] for item in descriptors] == ["Quest", "AlwaysLoaded"], "streaming descriptors changed")
    descriptor_contracts = (
        ("Quest", DEPOT_PATHS[5], 0, node_ref("$/mod/cqa/cqa004/#cqa004_pr_handoff"), (-1300.02, 1197.2208, -291.7), (-700.02, 1797.2208, 308.3)),
        ("AlwaysLoaded", DEPOT_PATHS[6], 1, node_ref(0), (-99999, -99999, -99999), (99999, 99999, 99999)),
    )
    for index, (descriptor, contract) in enumerate(zip(descriptors, descriptor_contracts)):
        category, depot_path, level, prefab_ref, minimum, maximum = contract
        require(set(descriptor) == {"$type", "blockIndex", "category", "data", "level", "numNodeRanges", "questPrefabNodeRef", "streamingBox", "variants"} and descriptor["$type"] == "worldStreamingSectorDescriptor", f"descriptor {index}: fields/type changed")
        require(descriptor["blockIndex"] == block_index and descriptor["category"] == category and descriptor["level"] == level, f"descriptor {index}: index/category/level changed")
        require(descriptor["data"] == resource_path(depot_path), f"descriptor {index}: sector depot path changed")
        require(descriptor["numNodeRanges"] == 1 and descriptor["variants"] == [], f"descriptor {index}: range/variant fields changed")
        require(descriptor["questPrefabNodeRef"] == prefab_ref, f"descriptor {index}: prefab root changed")
        require_streaming_box(descriptor["streamingBox"], minimum, maximum, f"descriptor {index} streamingBox")

    journal = load_json(COMPLETED / raw_relative(DEPOT_PATHS[2]))
    entry_ids = {str(item.get("id")) for item in iter_objects(journal) if item.get("$type", "").startswith("gameJournal") and "id" in item}
    require({"cqa004", "cqa004_01", "cqa004_01_obj_reach", "cqa004_01_obj_leave", "cqa004_01_obj_confirm", "cqa004_01_qmp_handoff"} <= entry_ids, "journal entry tree changed")
    refs = {str(item.get("$value")) for item in iter_objects(journal) if item.get("$type") == "NodeRef"}
    require("#cqa004_mp_handoff" in refs, "journal mappin local NodeRef changed")
    mappins = [item for item in iter_objects(journal) if item.get("$type") == "gameJournalQuestMapPin"]
    require(len(mappins) == 1, "journal must contain exactly one handoff mappin")
    mappin = mappins[0]
    require(mappin["reference"] == {"$type": "gameEntityReference", "dynamicEntityUniqueName": cname("None"), "names": [], "reference": node_ref("#cqa004_mp_handoff"), "sceneActorContextName": cname("None"), "slotName": cname("None"), "type": "EntityRef"}, "journal mappin marker path/reference changed")
    require(mappin["offset"] == {"$type": "Vector3", "X": 0, "Y": 0, "Z": 0.5}, "journal mappin offset changed")
    require(mappin["mappinData"]["mappinType"] == {"$type": "TweakDBID", "$storage": "string", "$value": "Mappins.QuestStaticMappinDefinition"} and mappin["mappinData"]["variant"] == "DefaultQuestVariant", "journal mappin type/variant changed")
    localization = load_json(COMPLETED / raw_relative(DEPOT_PATHS[3]))
    keys = {str(item.get("secondaryKey")) for item in iter_objects(localization) if item.get("$type") == "localizationPersistenceOnScreenEntry"}
    require(keys == {"cqa_cqa004_title", "cqa_cqa004_objective_reach", "cqa_cqa004_objective_leave", "cqa_cqa004_objective_confirm", "cqa_cqa004_mappin_handoff"}, "localization key set changed")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_manifest_acceptance_and_diagrams() -> None:
    manifest = load_json(COMPLETED / "example.json")
    require(manifest.get("schema_version") == 2 and manifest.get("id") == "cqa004" and manifest.get("title") == "Handoff Point", "Lab 4 manifest identity changed")
    require({key: manifest["baseline"][key] for key in BASELINE} == BASELINE, "Lab 4 baseline versions changed")
    require(tuple(manifest["depot_paths"]) == DEPOT_PATHS, "Lab 4 manifest depot inventory changed")
    require(tuple(manifest["registered_depot_paths"]) == REGISTERED_PATHS, "Lab 4 registered depot inventory changed")
    require(DEPOT_PATHS[1] not in manifest["registered_depot_paths"], "Lab 4 child phase must not be registered")
    require(manifest["persistent_facts"] == ["cqa004_completed"], "Lab 4 persistent fact inventory changed")
    structure = manifest["evidence"]["structure"]
    require(structure == {"status": "structurally-validated", "date": "2026-08-09", "method": "WolvenKit 8.19.0 deserialize and serialize round-trip inspection", "resource_pairs": 14}, "Lab 4 round-trip evidence metadata changed")
    require(manifest["evidence"]["runtime"] == {"status": "pending", "class": "experimental", "date": None, "record": "runtime-acceptance.json"}, "Lab 4 runtime evidence must remain pending/Experimental")
    artifacts = manifest["artifacts"]
    require(artifacts.get("algorithm") == "sha256" and len(artifacts["files"]) == 17, "Lab 4 artifact hash inventory changed")
    for relative, expected in artifacts["files"].items():
        require(sha256(COMPLETED / relative) == expected, f"Lab 4 artifact hash drift: {relative}")

    acceptance = load_json(COMPLETED / "runtime-acceptance.json")
    require(acceptance.get("schema_version") == 3 and acceptance.get("example_id") == "cqa004", "Lab 4 acceptance identity changed")
    require(acceptance.get("status") == "pending" and acceptance.get("evidence_class") == "experimental", "Lab 4 acceptance must remain pending/Experimental")
    require(acceptance.get("required_environment") == BASELINE, "Lab 4 acceptance environment changed")
    expected_ids = ["clean-walk", "pre-reach-reload", "between-boundaries-reload", "post-return-reload", "stream-away-return", "completed-reload", "completed-reinstall", "clean-replay"]
    runs = acceptance.get("runs")
    cases = acceptance.get("cases")
    require(isinstance(runs, list) and [run.get("id") for run in runs] == expected_ids, "Lab 4 acceptance run matrix changed")
    require(isinstance(cases, list) and [case.get("id") for case in cases] == expected_ids, "Lab 4 acceptance case matrix changed")
    for run in runs:
        require(run.get("performed_at") is None and run.get("tester") is None, f"{run.get('id')}: pending run execution fields must be null")
        require(all(value is None for value in run["observed_environment"].values()), f"{run.get('id')}: pending observed environment must be null")
        require(run["save"]["label"] is None and run["save"]["slot_directory"] is None and run["save"]["created_before_first_install"] is None and run["save"]["sha256"] is None, f"{run.get('id')}: pending save fields must be null")
        require(len(run["logs"]) == 4 and all(item["sha256"] is None for item in run["logs"]), f"{run.get('id')}: pending log hashes must be null")
    for case in cases:
        require(case.get("required") is True and case.get("status") == "pending" and case.get("observed") is None and case.get("evidence") == [], f"{case.get('id')}: pending case fields changed")
        require(case.get("run_ids") == [case.get("id")], f"{case.get('id')}: case/run binding changed")
    require("CutDestination remains outside" in acceptance.get("promotion_rule", ""), "Lab 4 promotion rule must exclude unwired CutDestination")

    result = subprocess.run([sys.executable, str(DIAGRAM_BUILDER), "--check"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
    require(result.returncode == 0, f"Lab 4 diagrams are stale:\n{result.stdout}{result.stderr}".rstrip())
    graphs = manifest["graphs"]
    for key, layout_name in (("root", "cqa004.questphase.layout.json"), ("child", "cqa004_boundary.questphase.layout.json")):
        layout = load_json(ASSETS / layout_name)
        require(graphs[key]["source_fingerprint"] == layout["source_fingerprint"], f"Lab 4 {key} graph fingerprint drift")
    for name in PUBLISHED_FILES:
        require((ASSETS / name).read_bytes() == (PUBLISHED / name).read_bytes(), f"Lab 4 published {name} differs from source")
        text_value = (PUBLISHED / name).read_text(encoding="utf-8")
        require("Experimental" in text_value and "WolvenKit" not in text_value, f"Lab 4 {name}: evidence label or screenshot boundary changed")


def run_wkit(wkit: Path) -> None:
    require(wkit.is_file(), f"WolvenKit CLI not found: {wkit}")
    version = subprocess.run([str(wkit), "--version"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
    require(version.returncode == 0 and version.stdout.strip() == "8.19.0", f"expected WolvenKit CLI 8.19.0, got {version.stdout.strip()!r}")
    with tempfile.TemporaryDirectory(prefix="cqa-lab04-wkit-") as temporary:
        temp = Path(temporary)
        for checkpoint in (START, COMPLETED):
            name = checkpoint.name
            cooked_out = temp / name / "cooked"
            json_out = temp / name / "json"
            cooked_out.mkdir(parents=True)
            json_out.mkdir(parents=True)
            cook = subprocess.run([str(wkit), "convert", "deserialize", str(checkpoint / "source" / "raw"), "-o", str(cooked_out), "-v", "Quiet"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", timeout=120)
            require(cook.returncode == 0, f"WolvenKit cook failed for {name}:\n{cook.stdout}{cook.stderr}".rstrip())
            for depot_path in DEPOT_PATHS:
                generated = cooked_out / Path(depot_path).name
                checked = checkpoint / cooked_relative(depot_path)
                require(generated.read_bytes() == checked.read_bytes(), f"WolvenKit 8.19.0 cook drift: {name}/{depot_path}")
            serialize = subprocess.run([str(wkit), "convert", "serialize", str(checkpoint / "source" / "archive"), "-o", str(json_out), "-v", "Quiet"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", timeout=120)
            require(serialize.returncode == 0, f"WolvenKit serialize failed for {name}:\n{serialize.stdout}{serialize.stderr}".rstrip())
            for depot_path, root_type in ROOT_TYPES.items():
                roundtrip = load_json(json_out / (Path(depot_path).name + ".json"))
                require(roundtrip["Header"]["WolvenKitVersion"] == "8.19.0" and roundtrip["Data"]["RootChunk"]["$type"] == root_type, f"WolvenKit round trip changed {name}/{depot_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wkit", type=Path, help="repeat the WolvenKit 8.19.0 cook and serialize round trip")
    return parser.parse_args()


def run_check(name: str, function: Any) -> bool:
    try:
        function()
    except Exception as error:
        print(f"[FAIL] {name}: {error}", file=sys.stderr)
        return False
    print(f"[ OK ] {name}")
    return True


def main() -> int:
    args = parse_args()
    checks = [
        ("Lab 4 inventories and deterministic CR2W-JSON generation", validate_inventories_and_generation),
        ("Lab 4 projects, root-only registration, and fourteen CR2W pairs", validate_projects_registration_and_pairs),
        ("Lab 4 root/child graph and socket contracts", validate_graphs),
        ("Lab 4 world, journal, and localization contracts", validate_world_journal_localization),
        ("Lab 4 evidence, hashes, and deterministic diagrams", validate_manifest_acceptance_and_diagrams),
    ]
    if args.wkit is not None:
        checks.append(("Lab 4 WolvenKit 8.19.0 cook and serialize round trip", lambda: run_wkit(args.wkit)))
    return 0 if all(run_check(name, function) for name, function in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
