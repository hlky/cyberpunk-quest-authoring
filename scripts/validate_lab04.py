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
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
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

MANIFEST = COMPLETED / "example.json"
ACCEPTANCE = COMPLETED / "runtime-acceptance.json"
BOOK_QUESTPHASES = ROOT / "book" / "src" / "questphases"
MANIFEST_BASELINE = {"recorded": "2026-08-09", **BASELINE}
EXPECTED_INSTALLED_FILES = (
    "archive\\pc\\mod\\CQA_Lab04_HandoffPoint.archive",
    "archive\\pc\\mod\\CQA_Lab04_HandoffPoint.archive.xl",
)
EXPECTED_LOGS = (
    "red4ext\\plugins\\ArchiveXL\\ArchiveXL.log",
    "red4ext\\logs\\red4ext.log",
    "red4ext\\logs\\game.log",
    "r6\\logs\\redscript_rCURRENT.log",
)
EXPECTED_RUNS = (
    ("clean-walk", "untouched-preinstall-outside-reach", "canonical-original"),
    ("pre-reach-reload", "child-active-before-reach", "canonical-clean-derived"),
    (
        "between-boundaries-reload",
        "child-active-reach-succeeded-inside-leave",
        "canonical-clean-derived",
    ),
    ("post-return-reload", "parent-confirmation-delay-active", "canonical-clean-derived"),
    ("stream-away-return", "child-active-before-reach", "canonical-clean-derived"),
    ("completed-reload", "completed", "canonical-completed"),
    ("completed-reinstall", "completed", "canonical-completed"),
    ("clean-replay", "untouched-preinstall-outside-reach", "canonical-original"),
)
EXPECTED_CASES: dict[str, tuple[list[str], str, str]] = {
    "clean-walk": (
        ["clean-walk"],
        "Install the canonical candidate and load an untouched pre-Lab-4 save with the player outside the reach volume.",
        "The root invokes the external child once; reach and leave advance once; child Out1 activates the parent confirmation objective; thirty realtime seconds later the quest completes once. Logs contain no cqa004 registration, child phaseResource, NodeRef, journal, localization, or streaming error.",
    ),
    "pre-reach-reload": (
        ["pre-reach-reload"],
        "Save after the child activates but before entering the reach volume, then reload without changing the installation.",
        "The active child, reach objective, and pin return once; entering and leaving advance once and return through child Out1. Logs contain no child-resolution or duplicated-activation error.",
    ),
    "between-boundaries-reload": (
        ["between-boundaries-reload"],
        "Save after reach succeeds while the child waits inside the leave volume, then reload.",
        "The child remains at the leave wait, does not complete until the boundary is crossed, and then returns to the parent once. Logs contain no child-state or NodeRef error.",
    ),
    "post-return-reload": (
        ["post-return-reload"],
        "Cross outside, verify the child returned, save while the parent's thirty-second confirmation delay is active, and reload.",
        "The child does not restart; the confirmation objective resumes coherently and completes once. Record whether elapsed realtime resumes or restarts. Logs contain no phase continuation error.",
    ),
    "stream-away-return": (
        ["stream-away-return"],
        "While the child is active before reach, travel by ordinary movement beyond the finite Quest descriptor box, return by ordinary movement, and finish the route.",
        "The active child remains coherent; the returned trigger crossings advance once; child Out1 continues the parent once. Logs contain no cqa004 streaming, phaseResource, or NodeRef resolution error.",
    ),
    "completed-reload": (
        ["completed-reload"],
        "Save after ordinary completion and reload without changing the installation.",
        "The cqa004_completed guard bypasses the child; no objective, pin, confirmation delay, or quest state reactivates. Logs remain free of cqa004 errors.",
    ),
    "completed-reinstall": (
        ["completed-reinstall"],
        "Remove and reinstall the identical canonical candidate, then load its completed save.",
        "The quest remains completed and the child is not reinvoked. ArchiveXL logs show the root registered without a separate child-phase registration and no cqa004 error.",
    ),
    "clean-replay": (
        ["clean-replay"],
        "Reload the original untouched pre-install save with the canonical candidate still installed and walk the full route again.",
        "The root-to-child-to-root sequence, visible journal states, world gates, confirmation delay, and completion reproduce once with no cqa004 errors in any retained log.",
    ),
}
PROMOTION_RULE = (
    "Set status to passed and evidence_class to runtime-proven only when all eight required cases pass and evidence "
    "binds the exact candidate build, all eight executions, the untouched pre-install save and every derived save, "
    "exact versions, visible observations, and all four logs for every execution. CutDestination remains outside "
    "this promotion rule because the lab leaves it unwired."
)
EVIDENCE_TYPES = {"screenshot", "video", "log", "save-metadata", "notes"}
WINDOWS_RESERVED_NAMES = {
    "aux",
    "con",
    "nul",
    "prn",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}
SAVE_EQUIVALENCE_CLASSES = (
    ("clean-walk", "clean-replay"),
    ("pre-reach-reload", "stream-away-return"),
    ("completed-reload", "completed-reinstall"),
    ("between-boundaries-reload",),
    ("post-return-reload",),
)

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


@dataclass(frozen=True)
class ManifestInfo:
    runtime_status: str
    runtime_class: str
    runtime_date: str | None


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def normalize_relative(value: Any, context: str) -> str:
    require(isinstance(value, str) and value, f"{context}: expected a non-empty path")
    normalized = value.replace("\\", "/")
    parsed = PurePosixPath(normalized)
    require(not parsed.is_absolute(), f"{context}: path must be relative")
    require(".." not in parsed.parts and "." not in parsed.parts, f"{context}: path traversal is not allowed")
    return parsed.as_posix()


def safe_evidence_path(reference: Any, *, label: str) -> Path:
    require(isinstance(reference, str) and reference, f"{label}: missing reference")
    relative = PurePosixPath(reference)
    require(
        reference == relative.as_posix()
        and not relative.is_absolute()
        and "\\" not in reference
        and len(relative.parts) >= 2
        and relative.parts[0] == "evidence"
        and all(part not in {"", ".", ".."} for part in relative.parts),
        f"{label}: unsafe POSIX evidence path {reference!r}",
    )
    for part in relative.parts:
        stem = part.split(".", 1)[0].casefold()
        require(
            stem not in WINDOWS_RESERVED_NAMES
            and not part.endswith((" ", "."))
            and not any(character in '<>:"|?*' or ord(character) < 32 for character in part),
            f"{label}: unsafe Windows path component {part!r}",
        )
    source = COMPLETED.joinpath(*relative.parts)
    cursor = COMPLETED
    for part in relative.parts:
        cursor /= part
        require(not cursor.is_symlink(), f"{label}: linked evidence path is forbidden: {reference}")
    require(source.is_file(), f"{label}: missing retained evidence file: {reference}")
    require(
        source.resolve().is_relative_to((COMPLETED / "evidence").resolve()),
        f"{label}: evidence path escapes completed/evidence: {reference}",
    )
    require(
        source.name.casefold() != "sav.dat" and source.suffix.casefold() != ".dat",
        f"{label}: private save binaries cannot be retained",
    )
    return source


def valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def valid_observed_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def observed_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or "T" not in value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


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


def retained_evidence_inventory() -> set[str]:
    acceptance = load_json(ACCEPTANCE)
    cases = acceptance.get("cases")
    require(isinstance(cases, list), f"{display(ACCEPTANCE)}: cases must be an array")
    references: set[str] = set()
    for case_index, case in enumerate(cases):
        require(isinstance(case, dict), f"{display(ACCEPTANCE)}: cases[{case_index}] must be an object")
        evidence = case.get("evidence")
        require(isinstance(evidence, list), f"{display(ACCEPTANCE)}: cases[{case_index}].evidence must be an array")
        for evidence_index, item in enumerate(evidence):
            require(
                isinstance(item, dict),
                f"{display(ACCEPTANCE)}: cases[{case_index}].evidence[{evidence_index}] must be an object",
            )
            label = (
                f"{display(ACCEPTANCE)}: cases[{case_index}]"
                f".evidence[{evidence_index}]"
            )
            source = safe_evidence_path(item.get("reference"), label=label)
            references.add(source.relative_to(COMPLETED).as_posix())
    return references


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
    retained_evidence = retained_evidence_inventory()
    require(actual_files(START) == expected_checkpoint_files(completed=False), "Lab 4 start inventory changed")
    require(
        actual_files(COMPLETED) == expected_checkpoint_files(completed=True) | retained_evidence,
        "Lab 4 completed inventory changed",
    )
    evidence_root = COMPLETED / "evidence"
    if evidence_root.exists() or evidence_root.is_symlink():
        require(not evidence_root.is_symlink(), "Lab 4 retained evidence directory cannot be a symlink")
        for path in evidence_root.rglob("*"):
            require(not path.is_symlink(), f"{display(path)}: retained evidence paths cannot contain symlinks")
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


def validate_manifest() -> ManifestInfo:
    manifest = load_json(MANIFEST)
    require(
        set(manifest)
        == {
            "schema_version",
            "id",
            "title",
            "book_chapter",
            "baseline",
            "depot_paths",
            "registered_depot_paths",
            "persistent_facts",
            "evidence",
            "graphs",
            "artifacts",
        },
        f"{display(MANIFEST)}: top-level schema changed",
    )
    require(
        manifest.get("schema_version") == 2
        and manifest.get("id") == "cqa004"
        and manifest.get("title") == "Handoff Point",
        f"{display(MANIFEST)}: identity/schema changed",
    )
    chapter = normalize_relative(manifest.get("book_chapter"), f"{display(MANIFEST)} book_chapter")
    require(
        chapter == "book/src/questphases/lab-04.md" and (ROOT / chapter).is_file(),
        f"{display(MANIFEST)}: wrong or missing book chapter",
    )
    require(manifest.get("baseline") == MANIFEST_BASELINE, f"{display(MANIFEST)}: pinned baseline changed")
    require(manifest.get("depot_paths") == list(DEPOT_PATHS), f"{display(MANIFEST)}: depot inventory changed")
    require(
        manifest.get("registered_depot_paths") == list(REGISTERED_PATHS),
        f"{display(MANIFEST)}: registered depot inventory changed",
    )
    require(
        DEPOT_PATHS[1] not in manifest["registered_depot_paths"],
        f"{display(MANIFEST)}: child phase must not be registered",
    )
    require(
        manifest.get("persistent_facts") == ["cqa004_completed"],
        f"{display(MANIFEST)}: persistent fact inventory changed",
    )

    evidence = manifest.get("evidence")
    require(
        isinstance(evidence, dict) and set(evidence) == {"structure", "runtime"},
        f"{display(MANIFEST)}: evidence object changed",
    )
    require(
        evidence.get("structure")
        == {
            "status": "structurally-validated",
            "date": "2026-08-09",
            "method": "WolvenKit 8.19.0 deserialize and serialize round-trip inspection",
            "resource_pairs": 14,
        },
        f"{display(MANIFEST)}: round-trip evidence metadata changed",
    )
    runtime = evidence.get("runtime")
    require(
        isinstance(runtime, dict) and set(runtime) == {"status", "class", "date", "record"},
        f"{display(MANIFEST)}: runtime evidence object changed",
    )
    runtime_status = runtime.get("status")
    runtime_class = runtime.get("class")
    runtime_date = runtime.get("date")
    require(runtime_status in {"pending", "failed", "passed"}, f"{display(MANIFEST)}: invalid runtime status")
    require(
        runtime_class == ("runtime-proven" if runtime_status == "passed" else "experimental"),
        f"{display(MANIFEST)}: runtime status and class disagree",
    )
    if runtime_date is not None:
        require(valid_observed_date(runtime_date), f"{display(MANIFEST)}: runtime date must be null or YYYY-MM-DD")
    require(
        runtime.get("record") == "runtime-acceptance.json" and ACCEPTANCE.is_file(),
        f"{display(MANIFEST)}: runtime acceptance record changed or is missing",
    )

    graphs = manifest.get("graphs")
    require(isinstance(graphs, dict) and set(graphs) == {"root", "child"}, f"{display(MANIFEST)}: graph inventory changed")
    for key, expected_layout in (
        ("root", "assets/diagrams/lab-04/cqa004.questphase.layout.json"),
        ("child", "assets/diagrams/lab-04/cqa004_boundary.questphase.layout.json"),
    ):
        graph = graphs.get(key)
        require(
            isinstance(graph, dict) and set(graph) == {"layout", "source_fingerprint"},
            f"{display(MANIFEST)}: {key} graph shape changed",
        )
        require(graph.get("layout") == expected_layout, f"{display(MANIFEST)}: {key} graph layout changed")
        fingerprint = graph.get("source_fingerprint")
        require(
            isinstance(fingerprint, str)
            and fingerprint.startswith("sha256:")
            and valid_sha256(fingerprint.removeprefix("sha256:")),
            f"{display(MANIFEST)}: {key} graph fingerprint is invalid",
        )

    artifacts = manifest.get("artifacts")
    require(
        isinstance(artifacts, dict) and set(artifacts) == {"algorithm", "files"},
        f"{display(MANIFEST)}: artifact hash schema changed",
    )
    require(artifacts.get("algorithm") == "sha256", f"{display(MANIFEST)}: artifact algorithm must be sha256")
    raw_hashes = artifacts.get("files")
    require(isinstance(raw_hashes, dict), f"{display(MANIFEST)}: artifact files must be an object")
    hashes: dict[str, str] = {}
    for raw_path, digest in raw_hashes.items():
        relative = normalize_relative(raw_path, f"{display(MANIFEST)} artifact path")
        require(relative not in hashes, f"{display(MANIFEST)}: duplicate artifact path {relative}")
        require(valid_sha256(digest), f"{display(MANIFEST)}: invalid SHA-256 for {relative}")
        hashes[relative] = digest
    expected_artifacts = expected_checkpoint_files(completed=True) - {"README.md", "example.json"}
    require(set(hashes) == expected_artifacts, f"{display(MANIFEST)}: artifact inventory changed")
    for relative, expected in hashes.items():
        require(sha256(COMPLETED / relative) == expected, f"{display(MANIFEST)}: stale SHA-256 for {relative}")

    return ManifestInfo(
        runtime_status=runtime_status,
        runtime_class=runtime_class,
        runtime_date=runtime_date,
    )


def validate_candidates(value: Any) -> dict[str, tuple[str | None, ...]]:
    require(isinstance(value, list), f"{display(ACCEPTANCE)}: candidates must be an array")
    require(
        [item.get("id") if isinstance(item, dict) else None for item in value] == ["canonical"],
        f"{display(ACCEPTANCE)}: exact one-candidate identity/order changed",
    )
    candidate = value[0]
    require(
        isinstance(candidate, dict) and set(candidate) == {"id", "manifest", "installed_files", "depot_paths"},
        f"{display(ACCEPTANCE)}: canonical candidate shape changed",
    )
    require(candidate.get("manifest") == "example.json", f"{display(ACCEPTANCE)}: canonical manifest reference changed")
    installed = candidate.get("installed_files")
    require(isinstance(installed, list) and len(installed) == 2, f"{display(ACCEPTANCE)}: expected two installed files")
    expected_paths = [normalize_relative(path, "installed path") for path in EXPECTED_INSTALLED_FILES]
    installed_paths: list[str] = []
    installed_hashes: list[str | None] = []
    for index, item in enumerate(installed):
        require(
            isinstance(item, dict) and set(item) == {"path", "sha256"},
            f"{display(ACCEPTANCE)}: installed_files[{index}] shape changed",
        )
        installed_paths.append(
            normalize_relative(item.get("path"), f"{display(ACCEPTANCE)}: installed_files[{index}].path")
        )
        digest = item.get("sha256")
        require(digest is None or valid_sha256(digest), f"{display(ACCEPTANCE)}: invalid installed-file SHA-256")
        installed_hashes.append(digest)
    require(installed_paths == expected_paths, f"{display(ACCEPTANCE)}: installed-file inventory changed")
    require(candidate.get("depot_paths") == list(DEPOT_PATHS), f"{display(ACCEPTANCE)}: candidate depot paths changed")
    return {"canonical": tuple(installed_hashes)}


def save_was_created_before_install(save_state: str) -> bool:
    return save_state.startswith("untouched-preinstall")


def validate_runs(value: Any) -> dict[str, dict[str, Any]]:
    require(isinstance(value, list), f"{display(ACCEPTANCE)}: runs must be an array")
    require(
        [item.get("id") if isinstance(item, dict) else None for item in value]
        == [item[0] for item in EXPECTED_RUNS],
        f"{display(ACCEPTANCE)}: immutable eight-run identity/order changed",
    )
    expected_log_paths = [normalize_relative(path, "runtime log path") for path in EXPECTED_LOGS]
    runs: dict[str, dict[str, Any]] = {}
    for run, (run_id, save_state, save_provenance) in zip(value, EXPECTED_RUNS, strict=True):
        require(
            isinstance(run, dict)
            and set(run)
            == {
                "id",
                "candidate_id",
                "save_state",
                "save_provenance",
                "performed_at",
                "tester",
                "observed_environment",
                "save",
                "logs",
            },
            f"{display(ACCEPTANCE)}:{run_id}: run shape changed",
        )
        require(
            run.get("candidate_id") == "canonical"
            and run.get("save_state") == save_state
            and run.get("save_provenance") == save_provenance,
            f"{display(ACCEPTANCE)}:{run_id}: immutable candidate/save provenance changed",
        )
        timestamp = run.get("performed_at")
        require(
            timestamp is None or observed_timestamp(timestamp) is not None,
            f"{display(ACCEPTANCE)}:{run_id}: performed_at must be null or an offset ISO 8601 timestamp",
        )
        tester = run.get("tester")
        require(
            tester is None or (isinstance(tester, str) and tester.strip()),
            f"{display(ACCEPTANCE)}:{run_id}: tester must be null or a non-empty string",
        )
        environment = run.get("observed_environment")
        require(
            isinstance(environment, dict) and set(environment) == set(BASELINE),
            f"{display(ACCEPTANCE)}:{run_id}: observed-environment shape changed",
        )
        for key, observed in environment.items():
            require(
                observed is None or observed == BASELINE[key],
                f"{display(ACCEPTANCE)}:{run_id}: observed {key} must be null or the pinned value",
            )
        save = run.get("save")
        require(
            isinstance(save, dict)
            and set(save) == {"label", "slot_directory", "artifact", "created_before_first_install", "sha256"},
            f"{display(ACCEPTANCE)}:{run_id}: save shape changed",
        )
        require(save.get("artifact") == "sav.dat", f"{display(ACCEPTANCE)}:{run_id}: save artifact must remain sav.dat")
        for key in ("label", "slot_directory"):
            entry = save.get(key)
            require(
                entry is None or (isinstance(entry, str) and entry.strip()),
                f"{display(ACCEPTANCE)}:{run_id}: save.{key} must be null or a non-empty string",
            )
        created = save.get("created_before_first_install")
        require(
            created is None or created is save_was_created_before_install(save_state),
            f"{display(ACCEPTANCE)}:{run_id}: created_before_first_install disagrees with save_state",
        )
        digest = save.get("sha256")
        require(digest is None or valid_sha256(digest), f"{display(ACCEPTANCE)}:{run_id}: invalid save SHA-256")
        logs = run.get("logs")
        require(isinstance(logs, list) and len(logs) == 4, f"{display(ACCEPTANCE)}:{run_id}: expected four logs")
        log_paths: list[str] = []
        for index, item in enumerate(logs):
            require(
                isinstance(item, dict) and set(item) == {"path", "sha256"},
                f"{display(ACCEPTANCE)}:{run_id}: logs[{index}] shape changed",
            )
            log_paths.append(
                normalize_relative(item.get("path"), f"{display(ACCEPTANCE)}:{run_id}: logs[{index}].path")
            )
            log_digest = item.get("sha256")
            require(log_digest is None or valid_sha256(log_digest), f"{display(ACCEPTANCE)}:{run_id}: invalid log SHA-256")
        require(log_paths == expected_log_paths, f"{display(ACCEPTANCE)}:{run_id}: exact four-log inventory changed")
        runs[run_id] = run
    return runs


def validate_retained_evidence(case_id: str, value: Any) -> None:
    require(isinstance(value, list) and value, f"{display(ACCEPTANCE)}:{case_id}: completed case needs retained evidence")
    references: set[str] = set()
    for index, item in enumerate(value):
        require(
            isinstance(item, dict) and set(item) == {"type", "reference", "sha256"},
            f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] shape changed",
        )
        evidence_type = item.get("type")
        require(
            evidence_type in EVIDENCE_TYPES,
            f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] has an invalid type",
        )
        label = f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}]"
        evidence_path = safe_evidence_path(
            item.get("reference"),
            label=label,
        )
        reference = evidence_path.relative_to(COMPLETED).as_posix()
        require(reference not in references, f"{display(ACCEPTANCE)}:{case_id}: duplicate evidence reference {reference}")
        references.add(reference)
        digest = item.get("sha256")
        require(valid_sha256(digest), f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] needs a SHA-256")
        if evidence_type == "save-metadata":
            require(
                evidence_path.suffix.lower() in {".md", ".txt", ".json"},
                f"{display(evidence_path)}: save metadata must be sanitized text",
            )
        require(sha256(evidence_path) == digest, f"{display(evidence_path)}: retained evidence SHA-256 mismatch")


def validate_completed_run(
    run_id: str,
    run: dict[str, Any],
    candidates: dict[str, tuple[str | None, ...]],
) -> datetime:
    require(
        all(valid_sha256(digest) for digest in candidates[run["candidate_id"]]),
        f"{display(ACCEPTANCE)}:{run_id}: completed run needs both installed candidate hashes",
    )
    timestamp = observed_timestamp(run.get("performed_at"))
    require(timestamp is not None, f"{display(ACCEPTANCE)}:{run_id}: completed run needs an offset timestamp")
    require(
        isinstance(run.get("tester"), str) and run["tester"].strip(),
        f"{display(ACCEPTANCE)}:{run_id}: completed run needs a tester",
    )
    require(
        run.get("observed_environment") == BASELINE,
        f"{display(ACCEPTANCE)}:{run_id}: completed run must record the exact observed environment",
    )
    save = run["save"]
    require(
        isinstance(save.get("label"), str)
        and save["label"].strip()
        and isinstance(save.get("slot_directory"), str)
        and save["slot_directory"].strip()
        and valid_sha256(save.get("sha256")),
        f"{display(ACCEPTANCE)}:{run_id}: completed run needs a labelled, hash-bound save",
    )
    require(
        save.get("created_before_first_install") is save_was_created_before_install(run["save_state"]),
        f"{display(ACCEPTANCE)}:{run_id}: untouched saves must be pre-install and derived saves must not be",
    )
    require(
        all(valid_sha256(item.get("sha256")) for item in run["logs"]),
        f"{display(ACCEPTANCE)}:{run_id}: completed run needs four hash-bound logs",
    )
    return timestamp


def validate_pending_run(run_id: str, run: dict[str, Any]) -> None:
    require(
        run.get("performed_at") is None and run.get("tester") is None,
        f"{display(ACCEPTANCE)}:{run_id}: pending run execution identity must be null",
    )
    require(
        all(value is None for value in run["observed_environment"].values()),
        f"{display(ACCEPTANCE)}:{run_id}: pending observed environment must be null",
    )
    save = run["save"]
    require(
        all(save.get(key) is None for key in ("label", "slot_directory", "created_before_first_install", "sha256")),
        f"{display(ACCEPTANCE)}:{run_id}: pending save result fields must be null",
    )
    require(
        all(item.get("sha256") is None for item in run["logs"]),
        f"{display(ACCEPTANCE)}:{run_id}: pending log hashes must be null",
    )


def require_related_save_hash(runs: dict[str, dict[str, Any]], source_id: str, reuse_id: str) -> None:
    source_digest = runs[source_id]["save"].get("sha256")
    reuse_digest = runs[reuse_id]["save"].get("sha256")
    require(
        valid_sha256(source_digest) and valid_sha256(reuse_digest) and source_digest == reuse_digest,
        f"{display(ACCEPTANCE)}:{reuse_id}: save hash must match {source_id}",
    )


def validate_runtime_acceptance(info: ManifestInfo) -> None:
    acceptance = load_json(ACCEPTANCE)
    require(
        set(acceptance)
        == {
            "schema_version",
            "example_id",
            "status",
            "evidence_class",
            "required_environment",
            "candidates",
            "runs",
            "cases",
            "promotion_rule",
        },
        f"{display(ACCEPTANCE)}: top-level schema changed",
    )
    require(
        acceptance.get("schema_version") == 3 and acceptance.get("example_id") == "cqa004",
        f"{display(ACCEPTANCE)}: identity/schema changed",
    )
    require(acceptance.get("required_environment") == BASELINE, f"{display(ACCEPTANCE)}: required environment changed")
    candidates = validate_candidates(acceptance.get("candidates"))
    runs = validate_runs(acceptance.get("runs"))
    cases = acceptance.get("cases")
    require(isinstance(cases, list), f"{display(ACCEPTANCE)}: cases must be an array")
    require(
        [case.get("id") if isinstance(case, dict) else None for case in cases] == list(EXPECTED_CASES),
        f"{display(ACCEPTANCE)}: immutable eight-case identity/order changed",
    )
    statuses: list[str] = []
    completed_run_ids: set[str] = set()
    for case, (case_id, (run_ids, precondition, expected)) in zip(cases, EXPECTED_CASES.items(), strict=True):
        require(
            isinstance(case, dict)
            and set(case) == {"id", "required", "status", "run_ids", "precondition", "expected", "observed", "evidence"},
            f"{display(ACCEPTANCE)}:{case_id}: case shape changed",
        )
        require(case.get("required") is True, f"{display(ACCEPTANCE)}:{case_id}: every case must remain required")
        require(case.get("run_ids") == run_ids, f"{display(ACCEPTANCE)}:{case_id}: immutable run_ids changed")
        require(case.get("precondition") == precondition, f"{display(ACCEPTANCE)}:{case_id}: immutable precondition changed")
        require(case.get("expected") == expected, f"{display(ACCEPTANCE)}:{case_id}: immutable expected result changed")
        status = case.get("status")
        require(status in {"pending", "passed", "failed"}, f"{display(ACCEPTANCE)}:{case_id}: invalid status")
        statuses.append(status)
        if status == "pending":
            require(
                case.get("observed") is None and case.get("evidence") == [],
                f"{display(ACCEPTANCE)}:{case_id}: pending case cannot claim observations/evidence",
            )
            for run_id in run_ids:
                validate_pending_run(run_id, runs[run_id])
        else:
            require(
                isinstance(case.get("observed"), str) and case["observed"].strip(),
                f"{display(ACCEPTANCE)}:{case_id}: completed case needs a non-empty observation",
            )
            validate_retained_evidence(case_id, case.get("evidence"))
            completed_run_ids.update(run_ids)

    if any(status == "failed" for status in statuses):
        expected_status = "failed"
    elif all(status == "passed" for status in statuses):
        expected_status = "passed"
    else:
        expected_status = "pending"
    expected_class = "runtime-proven" if expected_status == "passed" else "experimental"
    require(
        acceptance.get("status") == expected_status,
        f"{display(ACCEPTANCE)}: top-level status disagrees with required cases",
    )
    require(
        acceptance.get("evidence_class") == expected_class,
        f"{display(ACCEPTANCE)}: evidence_class disagrees with derived status",
    )
    require(info.runtime_status == expected_status, f"{display(MANIFEST)}: runtime status disagrees with acceptance cases")
    require(info.runtime_class == expected_class, f"{display(MANIFEST)}: runtime class disagrees with acceptance cases")

    completed_timestamps: dict[str, datetime] = {}
    completed_slot_directories: dict[str, str] = {}
    for run_id in sorted(completed_run_ids):
        completed_timestamps[run_id] = validate_completed_run(run_id, runs[run_id], candidates)
        slot_directory = runs[run_id]["save"]["slot_directory"].strip().replace("/", "\\").rstrip("\\").casefold()
        require(slot_directory, f"{display(ACCEPTANCE)}:{run_id}: slot directory normalizes to empty")
        completed_slot_directories[run_id] = slot_directory
    require(
        len(set(completed_timestamps.values())) == len(completed_timestamps),
        f"{display(ACCEPTANCE)}: completed executions must use distinct performed_at instants",
    )
    require(
        len(set(completed_slot_directories.values())) == len(completed_slot_directories),
        f"{display(ACCEPTANCE)}: completed executions must use distinct normalized save slot directories",
    )
    completed_log_bundles = {
        run_id: tuple(item["sha256"] for item in runs[run_id]["logs"])
        for run_id in completed_run_ids
    }
    require(
        len(set(completed_log_bundles.values())) == len(completed_log_bundles),
        f"{display(ACCEPTANCE)}: completed executions must use distinct four-log hash bundles",
    )

    related_saves = SAVE_EQUIVALENCE_CLASSES[:3]
    for source_id, reuse_id in related_saves:
        source_digest = runs[source_id]["save"].get("sha256")
        reuse_digest = runs[reuse_id]["save"].get("sha256")
        if source_digest is not None and reuse_digest is not None:
            require(
                source_digest == reuse_digest,
                f"{display(ACCEPTANCE)}:{reuse_id}: populated save hash must match {source_id}",
            )
        if reuse_id in completed_run_ids:
            require_related_save_hash(runs, source_id, reuse_id)

    completed_class_hashes: dict[str, str] = {}
    for save_class in SAVE_EQUIVALENCE_CLASSES:
        class_runs = [run_id for run_id in save_class if run_id in completed_run_ids]
        if not class_runs:
            continue
        class_hashes = {runs[run_id]["save"]["sha256"] for run_id in class_runs}
        require(
            len(class_hashes) == 1,
            f"{display(ACCEPTANCE)}: save-equivalence class {save_class!r} must share one hash",
        )
        completed_class_hashes[save_class[0]] = next(iter(class_hashes))
    require(
        len(set(completed_class_hashes.values())) == len(completed_class_hashes),
        f"{display(ACCEPTANCE)}: unrelated original/derived/completed save classes must have distinct hashes",
    )

    expected_date = (
        max(completed_timestamps.values()).date().isoformat()
        if completed_timestamps
        else None
    )
    require(
        info.runtime_date == expected_date,
        f"{display(MANIFEST)}: runtime date must equal the latest completed execution date {expected_date!r}",
    )
    require(acceptance.get("promotion_rule") == PROMOTION_RULE, f"{display(ACCEPTANCE)}: promotion rule changed")


def marker_lines(path: Path) -> list[str]:
    require(path.is_file(), f"{display(path)}: missing reader-facing Lab 4 page")
    return [
        line
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("**Lab 4 runtime evidence:**")
    ]


def validate_reader_status(info: ManifestInfo) -> None:
    marker_by_state = {
        ("pending", "experimental"): "**Lab 4 runtime evidence:** **Experimental** — pending.",
        ("failed", "experimental"): "**Lab 4 runtime evidence:** **Experimental** — failed.",
        ("passed", "runtime-proven"): "**Lab 4 runtime evidence:** **Runtime-proven** — passed.",
    }
    state = (info.runtime_status, info.runtime_class)
    require(state in marker_by_state, f"{display(MANIFEST)}: runtime status/class cannot produce a reader marker")
    expected_marker = marker_by_state[state]
    expected_date = info.runtime_date if info.runtime_date is not None else "Not yet recorded"
    date_row = f"| Runtime test date | {expected_date} |"
    practical_pages = (
        BOOK_QUESTPHASES / "lab-04.md",
        BOOK_QUESTPHASES / "lab-04-authoring.md",
        BOOK_QUESTPHASES / "lab-04-test.md",
    )
    passed_example = marker_by_state[("passed", "runtime-proven")]
    failed_example = marker_by_state[("failed", "experimental")]
    for page in practical_pages:
        text_value = page.read_text(encoding="utf-8")
        expected_markers = (
            [expected_marker, passed_example, failed_example]
            if page.name == "lab-04-test.md"
            else [expected_marker]
        )
        require(
            marker_lines(page) == expected_markers,
            f"{display(page)}: Lab 4 runtime evidence markers are stale or duplicated",
        )
        date_rows = [line for line in text_value.splitlines() if line.startswith("| Runtime test date |")]
        require(date_rows == [date_row], f"{display(page)}: runtime test date must be {expected_date!r}")

    status_pages = (
        ROOT / "README.md",
        ROOT / "HANDOFF.md",
        ROOT / "ROADMAP.md",
        ROOT / "book" / "src" / "introduction.md",
        BOOK_QUESTPHASES / "index.md",
        ROOT / "book" / "src" / "reference" / "evidence-version-matrix.md",
        LAB / "README.md",
        START / "README.md",
        COMPLETED / "README.md",
    )
    for page in status_pages:
        require(
            marker_lines(page) == [expected_marker],
            f"{display(page)}: missing, stale, or duplicate Lab 4 runtime evidence marker",
        )


def validate_diagram_reader_status(info: ManifestInfo, manifest: dict[str, Any]) -> None:
    result = subprocess.run(
        [sys.executable, "-B", str(DIAGRAM_BUILDER), "--check"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = "".join(part for part in (result.stdout, result.stderr) if part)
    require(result.returncode == 0, f"Lab 4 diagrams are stale:\n{output}".rstrip())
    graphs = manifest["graphs"]
    for key, layout_name in (
        ("root", "cqa004.questphase.layout.json"),
        ("child", "cqa004_boundary.questphase.layout.json"),
    ):
        layout = load_json(ASSETS / layout_name)
        require(
            graphs[key]["source_fingerprint"] == layout["source_fingerprint"],
            f"Lab 4 {key} graph fingerprint drift",
        )

    display_class = {
        "experimental": "Experimental",
        "runtime-proven": "Runtime-proven",
    }[info.runtime_class]
    date_suffix = f" • test date: {info.runtime_date}" if info.runtime_date is not None else ""
    expected_footers = {
        "cqa004.root.questphase.svg": f"{display_class} — runtime acceptance {info.runtime_status}{date_suffix}",
        "cqa004.child.questphase.svg": f"{display_class} — runtime acceptance {info.runtime_status}{date_suffix}",
        "cqa004.resource-chain.svg": f"{display_class} — runtime behavior {info.runtime_status}{date_suffix}",
        "cqa004.handoff-contract.svg": f"{display_class} — parent/child runtime acceptance {info.runtime_status}{date_suffix}",
    }
    namespace = "http://www.w3.org/2000/svg"
    for name in PUBLISHED_FILES:
        asset = ASSETS / name
        published = PUBLISHED / name
        require(asset.read_bytes() == published.read_bytes(), f"Lab 4 published {name} differs from source")
        text_value = published.read_text(encoding="utf-8")
        require("WolvenKit" not in text_value, f"Lab 4 {name}: WolvenKit screenshot boundary changed")
        try:
            root = ET.parse(asset).getroot()
        except (OSError, ET.ParseError) as error:
            raise ValidationError(f"{display(asset)}: invalid SVG XML: {error}") from error
        metadata = root.find(f"{{{namespace}}}metadata")
        require(metadata is not None and isinstance(metadata.text, str), f"{display(asset)}: missing SVG metadata")
        try:
            metadata_value = json.loads(metadata.text, object_pairs_hook=reject_duplicate_keys)
        except json.JSONDecodeError as error:
            raise ValidationError(f"{display(asset)}: invalid SVG metadata JSON: {error}") from error
        require(
            isinstance(metadata_value, dict) and metadata_value.get("evidence_class") == display_class,
            f"{display(asset)}: stale evidence class in SVG metadata",
        )
        text_values = [
            element.text
            for element in root.findall(f".//{{{namespace}}}text")
            if isinstance(element.text, str)
        ]
        require(
            text_values.count(expected_footers[name]) == 1,
            f"{display(asset)}: stale or duplicate runtime evidence footer",
        )
        if name in {"cqa004.root.questphase.svg", "cqa004.child.questphase.svg"}:
            require(text_values.count(display_class) == 1, f"{display(asset)}: stale or duplicate graph evidence badge")


def validate_manifest_acceptance_and_diagrams() -> None:
    manifest = load_json(MANIFEST)
    info = validate_manifest()
    validate_runtime_acceptance(info)
    validate_reader_status(info)
    validate_diagram_reader_status(info, manifest)


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
