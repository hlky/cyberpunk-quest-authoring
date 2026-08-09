#!/usr/bin/env python3
"""Validate the complete Lab 3 Boundary Check reference project.

This validator is intentionally standalone and standard-library-only. It does
not invoke WolvenKit or depend on the repository-local ``.tmp`` directory.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import math
import subprocess
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-03-boundary-check"
START = LAB / "start"
COMPLETED = LAB / "completed"
BOOK_WORLD = ROOT / "book" / "src" / "world"
MANIFEST = COMPLETED / "example.json"
ACCEPTANCE = COMPLETED / "runtime-acceptance.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_lab03_sources.py"
RENDER_SCRIPT = ROOT / "scripts" / "render_quest_graph.py"
DIAGRAM_SCRIPT = ROOT / "scripts" / "build_lab03_diagrams.py"
DIAGRAM_ASSET_DIR = ROOT / "assets" / "diagrams" / "lab-03"
DIAGRAM_PUBLISH_DIR = ROOT / "book" / "src" / "images" / "lab-03"
DIAGRAM_NAMES = (
    "cqa003.questphase.svg",
    "cqa003.resource-chain.svg",
    "cqa003.trigger-volume-plan.svg",
)

DEPOT_PATHS = (
    "mod/cqa/cqa003/phases/cqa003.questphase",
    "mod/cqa/cqa003/journal/cqa003.journal",
    "mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json",
    "mod/cqa/cqa003/world/cqa003_boundary.streamingblock",
    "mod/cqa/cqa003/world/cqa003_boundary.streamingsector",
    "mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector",
)
QUEST_PHASE_PATH, JOURNAL_PATH, LOCALIZATION_PATH, BLOCK_PATH, QUEST_SECTOR_PATH, ALWAYS_SECTOR_PATH = DEPOT_PATHS

BASELINE = {
    "recorded": "2026-08-09",
    "cyberpunk_2077": "2.31a",
    "wolvenkit": "8.19.0",
    "archive_xl": "1.27.0",
    "red4ext": "1.30.0",
    "redscript": "0.5.31",
}
REQUIRED_ENVIRONMENT = {key: value for key, value in BASELINE.items() if key != "recorded"}

RAW_RELATIVE = frozenset(f"source/raw/{path}.json" for path in DEPOT_PATHS)
COOKED_RELATIVE = frozenset(f"source/archive/{path}" for path in DEPOT_PATHS)
START_FILES = frozenset(
    {
        "CQA_Lab03_BoundaryCheck_Start.cpmodproj",
        "README.md",
        *RAW_RELATIVE,
        *COOKED_RELATIVE,
        "source/resources/CQA_Lab03_BoundaryCheck_Start.archive.xl",
    }
)
COMPLETED_FILES = frozenset(
    {
        "CQA_Lab03_BoundaryCheck.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        *RAW_RELATIVE,
        *COOKED_RELATIVE,
        "source/resources/CQA_Lab03_BoundaryCheck.archive.xl",
    }
)
START_TEXT_FILES = START_FILES - COOKED_RELATIVE
COMPLETED_TEXT_FILES = COMPLETED_FILES - COOKED_RELATIVE
LAB_FILES = frozenset(
    {
        "LICENSE.md",
        "README.md",
        *(f"start/{path}" for path in START_FILES),
        *(f"completed/{path}" for path in COMPLETED_FILES),
    }
)

EXPECTED_ROOT_TYPES = {
    ".questphase": "questQuestPhaseResource",
    ".journal": "gameJournalResource",
    ".json": "JsonResource",
    ".streamingblock": "worldStreamingBlock",
    ".streamingsector": "worldStreamingSector",
}

QUEST_PATH = "quests/minor_quest/cqa003"
PHASE_PATH = f"{QUEST_PATH}/cqa003_01"
REACH_PATH = f"{PHASE_PATH}/cqa003_01_obj_reach"
LEAVE_PATH = f"{PHASE_PATH}/cqa003_01_obj_leave"
MAPPIN_PATH = f"{REACH_PATH}/cqa003_01_qmp_checkpoint"

PREFAB_LOCAL = "#cqa003_pr_boundary"
PREFAB_FULL = "$/mod/cqa/cqa003/#cqa003_pr_boundary"
REACH_LOCAL = "#cqa003_tr_reach"
LEAVE_LOCAL = "#cqa003_tr_leave"
MARKER_LOCAL = "#cqa003_mp_checkpoint"
REACH_FULL = f"{PREFAB_FULL}/{REACH_LOCAL}"
LEAVE_FULL = f"{PREFAB_FULL}/{LEAVE_LOCAL}"
MARKER_FULL = f"{PREFAB_FULL}/{MARKER_LOCAL}"

MARKER_POSITION = (-1000.02, 1497.2208, 8.3)
REACH_POSITION = (-1000.02, 1497.2208, 2.3)
LEAVE_POSITION = (-1000.02, 1497.2208, 0.3)
MARKER_YAW = 88.6
REACH_RADIUS = 25
LEAVE_RADIUS = 110

EXPECTED_NODE_TYPES = {
    0: "questInputNodeDefinition",
    1: "questOutputNodeDefinition",
    10: "questConditionNodeDefinition",
    11: "questJournalNodeDefinition",
    12: "questJournalNodeDefinition",
    13: "questJournalNodeDefinition",
    14: "questMappinManagerNodeDefinition",
    15: "questPauseConditionNodeDefinition",
    16: "questMappinManagerNodeDefinition",
    17: "questJournalNodeDefinition",
    18: "questJournalNodeDefinition",
    19: "questPauseConditionNodeDefinition",
    20: "questJournalNodeDefinition",
    21: "questJournalNodeDefinition",
    22: "questFactsDBManagerNodeDefinition",
    23: "questJournalNodeDefinition",
}
EXPECTED_EDGES = frozenset(
    {
        (0, "Out", 10, "In"),
        (10, "False", 1, "In"),
        (10, "True", 11, "Active"),
        (11, "Out", 12, "Active"),
        (12, "Out", 13, "Active"),
        (13, "Out", 14, "Active"),
        (14, "Out", 15, "In"),
        (15, "Out", 16, "Inactive"),
        (16, "Out", 17, "Succeeded"),
        (17, "Out", 18, "Active"),
        (18, "Out", 19, "In"),
        (19, "Out", 20, "Succeeded"),
        (20, "Out", 21, "Succeeded"),
        (21, "Out", 22, "In"),
        (22, "Out", 23, "Succeeded"),
        (23, "Out", 1, "In"),
    }
)

EXPECTED_INSTALLED_FILES = (
    "archive\\pc\\mod\\CQA_Lab03_BoundaryCheck.archive",
    "archive\\pc\\mod\\CQA_Lab03_BoundaryCheck.archive.xl",
)
EXPECTED_LOGS = (
    "red4ext\\plugins\\ArchiveXL\\ArchiveXL.log",
    "red4ext\\logs\\red4ext.log",
    "red4ext\\logs\\game.log",
    "r6\\logs\\redscript_rCURRENT.log",
)
EXPECTED_RUNS = (
    ("clean-walk", "untouched-preinstall-outside-reach", "canonical-original"),
    ("pre-reach-reload", "active-before-reach", "canonical-clean-derived"),
    ("between-boundaries-reload", "reach-succeeded-inside-leave", "canonical-clean-derived"),
    ("stream-away-return", "active-before-reach", "canonical-clean-derived"),
    ("fast-travel-exit", "reach-succeeded-inside-leave", "fast-travel-original"),
    ("completed-reload", "completed", "canonical-completed"),
    ("completed-reinstall", "completed", "canonical-completed"),
    ("clean-replay", "untouched-preinstall-outside-reach", "canonical-original"),
)
EXPECTED_CASES: dict[str, tuple[list[str], str, str]] = {
    "outside-negative-control-and-foot-route": (
        ["clean-walk"],
        "Install the canonical candidate and load an untouched pre-Lab-3 save with the player outside the "
        "25-metre reach volume.",
        "Waiting outside does not advance the reach objective. Entering the reach volume retires the pin and "
        "succeeds the reach objective once; remaining inside the 110-metre leave volume does not complete; "
        "crossing its boundary on foot succeeds the leave objective and quest once.",
    ),
    "marker-and-navigation": (
        ["clean-walk"],
        "Observe the journal objective, map pin, minimap, and route before entering the reach volume.",
        "The checkpoint pin is visible at the intended location and any GPS route is usable; record missing, "
        "displaced, inaccessible, or unstable presentation without inferring the hidden sector owner from UI alone.",
    ),
    "pre-reach-reload": (
        ["pre-reach-reload"],
        "Save after activation while still outside the reach volume, then reload without changing the installation.",
        "The active reach objective and pin return once; entering the reach volume advances once with no duplicate "
        "journal update.",
    ),
    "between-boundaries-reload": (
        ["between-boundaries-reload"],
        "Save after reach succeeds while the player remains inside the 110-metre leave volume, then reload.",
        "The leave objective remains active and does not complete until the player crosses outside the leave volume "
        "after reload.",
    ),
    "stream-away-and-return": (
        ["stream-away-return"],
        "Restore the exact hash-bound pre-reach save used by the pre-reach-reload run; by ordinary movement travel "
        "from Allen Street well beyond the finite Quest descriptor box without using fast travel, return by ordinary "
        "movement, and then walk the full route.",
        "The visible objective and pin remain coherent and the returned reach and leave crossings each advance once. "
        "Logs contain no cqa003 streaming or NodeRef resolution error. No precise unload or reload moment is claimed "
        "without independent instrumentation.",
    ),
    "fast-travel-characterization": (
        ["fast-travel-exit"],
        "From a separate between-boundaries save, reach the unlocked Allen Street terminal by ordinary movement "
        "while the leave objective remains visibly active; record the pre-activation position and Z, use an unlocked "
        "destination independently known to be outside the 110-metre leave outline, and record the arrival position.",
        "If leave completes before the terminal opens, mark this required case failed and retain the position evidence; "
        "do not continue it as a fast-travel characterization. Otherwise record whether the state-shaped IsOutside "
        "gate completes after arrival and bind the result to the exact candidate and logs.",
    ),
    "completed-save-reload": (
        ["completed-reload"],
        "Save after ordinary completion and reload without changing the installation.",
        "No quest, objective, or pin reactivation occurs. Exact graph evidence maps the bypass to the "
        "cqa003_completed guard's False route.",
    ),
    "completed-save-reinstall": (
        ["completed-reinstall"],
        "Remove and reinstall the identical canonical candidate, then load its completed save.",
        "The quest remains completed, the pin stays inactive, and no duplicate activation occurs.",
    ),
    "clean-replay": (
        ["clean-replay"],
        "Reload the original untouched pre-install save with the canonical candidate still installed and walk the "
        "route again.",
        "The same visible activation, reach, leave, and completion sequence occurs once.",
    ),
    "registration-and-lookup-logs": (
        [run_id for run_id, _, _ in EXPECTED_RUNS],
        "Retain a fresh four-file RED4ext, ArchiveXL, game, and redscript log set from every execution.",
        "All eight log sets contain no cqa003 registration, depot-path, streaming-block, sector, NodeRef, journal, "
        "localization, or condition error.",
    ),
}
PROMOTION_RULE = (
    "Set status to passed and evidence_class to runtime-proven only when every required case passes and evidence "
    "binds the exact candidate build, all eight executions, the untouched pre-install save and every derived save, "
    "exact versions, visible observations, and all four logs for every execution."
)


class ValidationError(RuntimeError):
    """A Lab 3 repository invariant was not satisfied."""


@dataclass(frozen=True)
class ManifestInfo:
    depot_paths: tuple[str, ...]
    graph_fingerprint: str
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


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON file: {display(path)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"{display(path)}: invalid UTF-8 JSON: {error}") from error
    require(isinstance(value, dict), f"{display(path)}: root must be an object")
    return value


def actual_files(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}


def difference(expected: set[str] | frozenset[str], actual: set[str]) -> str:
    missing = sorted(set(expected) - actual)
    extra = sorted(actual - set(expected))
    parts = []
    if missing:
        parts.append("missing " + ", ".join(missing))
    if extra:
        parts.append("unexpected " + ", ".join(extra))
    return "; ".join(parts) or "no difference"


def retained_evidence_inventory() -> set[str]:
    """Return every acceptance-bound evidence file allowed in completed/."""

    record = load_json(ACCEPTANCE)
    cases = record.get("cases")
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
            reference = normalize_relative(
                item.get("reference"),
                f"{display(ACCEPTANCE)} cases[{case_index}].evidence[{evidence_index}].reference",
            )
            require(
                reference.startswith("evidence/"),
                f"{display(ACCEPTANCE)}: retained evidence must stay below completed/evidence",
            )
            references.add(reference)
    return references


def load_module(path: Path, name: str) -> ModuleType:
    specification = importlib.util.spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None, f"cannot load {display(path)}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    try:
        specification.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def checkpoint_file(checkpoint: Path, depot_path: str, *, raw: bool) -> Path:
    suffix = f"{depot_path}.json" if raw else depot_path
    return checkpoint / "source" / ("raw" if raw else "archive") / suffix


def validate_inventories() -> None:
    retained_evidence = retained_evidence_inventory()
    completed_files = set(COMPLETED_FILES) | retained_evidence
    evidence_root = COMPLETED / "evidence"
    if evidence_root.exists() or evidence_root.is_symlink():
        require(not evidence_root.is_symlink(), f"{display(evidence_root)}: retained evidence directories cannot be symlinks")
        for path in evidence_root.rglob("*"):
            require(not path.is_symlink(), f"{display(path)}: retained evidence paths cannot contain symlinks")
    for root, expected, text_files, label in (
        (START, START_FILES, START_TEXT_FILES, "start"),
        (COMPLETED, completed_files, COMPLETED_TEXT_FILES, "completed"),
    ):
        actual = actual_files(root)
        require(actual == set(expected), f"Lab 3 {label} inventory: {difference(expected, actual)}")
        for relative in sorted(text_files):
            path = root / relative
            payload = path.read_bytes()
            require(not payload.startswith(b"\xef\xbb\xbf"), f"{display(path)}: UTF-8 BOM is not allowed")
            require(b"\r" not in payload, f"{display(path)}: text must use LF line endings")
            try:
                payload.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ValidationError(f"{display(path)}: text is not valid UTF-8") from error

    lab_files = set(LAB_FILES) | {f"completed/{path}" for path in retained_evidence}
    actual_lab = actual_files(LAB)
    require(actual_lab == lab_files, f"Lab 3 full inventory: {difference(lab_files, actual_lab)}")
    for path in (LAB / "LICENSE.md", LAB / "README.md"):
        payload = path.read_bytes()
        require(not payload.startswith(b"\xef\xbb\xbf"), f"{display(path)}: UTF-8 BOM is not allowed")
        require(b"\r" not in payload, f"{display(path)}: text must use LF line endings")
        try:
            payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValidationError(f"{display(path)}: text is not valid UTF-8") from error


def generated_raw_set(checkpoint: Path) -> set[str]:
    raw_root = checkpoint / "source" / "raw"
    return {path.relative_to(raw_root).as_posix() for path in raw_root.rglob("*.json")}


def generate_into(root: Path, module_name: str) -> None:
    module = load_module(BUILD_SCRIPT, module_name)
    try:
        module.CHECKPOINTS = {"start": root / "start", "completed": root / "completed"}
        module.LAB_ROOT = root
        module.main()
    finally:
        sys.modules.pop(module_name, None)


def validate_generated_raw() -> None:
    expected = {f"{path}.json" for path in DEPOT_PATHS}
    with tempfile.TemporaryDirectory(prefix="cqa-lab03-raw-a-") as first_name, tempfile.TemporaryDirectory(
        prefix="cqa-lab03-raw-b-"
    ) as second_name:
        first = Path(first_name)
        second = Path(second_name)
        generate_into(first, "_cqa_build_lab03_sources_a")
        generate_into(second, "_cqa_build_lab03_sources_b")
        for checkpoint_name, checked_root in (("start", START), ("completed", COMPLETED)):
            first_checkpoint = first / checkpoint_name
            second_checkpoint = second / checkpoint_name
            first_set = generated_raw_set(first_checkpoint)
            second_set = generated_raw_set(second_checkpoint)
            require(first_set == expected, f"Lab 3 {checkpoint_name} generator inventory: {difference(expected, first_set)}")
            require(second_set == expected, f"Lab 3 {checkpoint_name} second generator inventory differs")
            for relative in sorted(expected):
                generated_a = first_checkpoint / "source" / "raw" / relative
                generated_b = second_checkpoint / "source" / "raw" / relative
                checked = checked_root / "source" / "raw" / relative
                require(generated_a.read_bytes() == generated_b.read_bytes(), f"Lab 3 {checkpoint_name} generator is not deterministic for {relative}")
                require(generated_a.read_bytes() == checked.read_bytes(), f"{display(checked)}: generated CR2W-JSON is stale")


def expected_archive_xl_lines() -> list[str]:
    return [
        "quest:",
        "  phases:",
        "  - path: mod\\cqa\\cqa003\\phases\\cqa003.questphase",
        "    parent: base\\quest\\cyberpunk2077.quest",
        "",
        "journal:",
        "- mod\\cqa\\cqa003\\journal\\cqa003.journal",
        "",
        "localization:",
        "  onscreens:",
        "    en-us:",
        "    - mod\\cqa\\cqa003\\localization\\en-us\\onscreens\\cqa003.json",
        "",
        "streaming:",
        "  blocks:",
        "  - mod\\cqa\\cqa003\\world\\cqa003_boundary.streamingblock",
    ]


def validate_projects_archive_xl_and_cr2w_pairs() -> None:
    projects = (
        (START / "CQA_Lab03_BoundaryCheck_Start.cpmodproj", "CQA Lab 03 Boundary Check Start", "CQA_Lab03_BoundaryCheck_Start"),
        (COMPLETED / "CQA_Lab03_BoundaryCheck.cpmodproj", "CQA Lab 03 Boundary Check", "CQA_Lab03_BoundaryCheck"),
    )
    for path, name, mod_name in projects:
        try:
            root = ET.parse(path).getroot()
        except (OSError, ET.ParseError) as error:
            raise ValidationError(f"{display(path)}: invalid WolvenKit project XML: {error}") from error
        require(root.tag == "CP77Mod", f"{display(path)}: wrong project root")
        require(root.findtext("Name") == name, f"{display(path)}: project name changed")
        require(root.findtext("ModName") == mod_name, f"{display(path)}: mod name changed")
        require(root.findtext("Version") == "0.1.0", f"{display(path)}: project version changed")

    archive_xl_files = (
        START / "source/resources/CQA_Lab03_BoundaryCheck_Start.archive.xl",
        COMPLETED / "source/resources/CQA_Lab03_BoundaryCheck.archive.xl",
    )
    for path in archive_xl_files:
        lines = path.read_text(encoding="utf-8").splitlines()
        while lines and not lines[-1]:
            lines.pop()
        require(lines == expected_archive_xl_lines(), f"{display(path)}: exact ArchiveXL registration changed")

    pair_count = 0
    for checkpoint in (START, COMPLETED):
        for depot_path in DEPOT_PATHS:
            pair_count += 1
            raw_path = checkpoint_file(checkpoint, depot_path, raw=True)
            cooked_path = checkpoint_file(checkpoint, depot_path, raw=False)
            source = load_json(raw_path)
            header = source.get("Header")
            data = source.get("Data")
            require(isinstance(header, dict) and isinstance(data, dict), f"{display(raw_path)}: missing Header/Data")
            require(
                header.get("WolvenKitVersion") == "8.19.0"
                and header.get("WKitJsonVersion") == "0.0.9"
                and header.get("GameVersion") == 2310
                and header.get("DataType") == "CR2W",
                f"{display(raw_path)}: CR2W review-source baseline changed",
            )
            archive_name = normalize_relative(header.get("ArchiveFileName"), f"{display(raw_path)} Header.ArchiveFileName")
            require(archive_name == depot_path, f"{display(raw_path)}: ArchiveFileName does not match its depot path")
            suffix = next((candidate for candidate in EXPECTED_ROOT_TYPES if depot_path.endswith(candidate)), None)
            require(suffix is not None, f"{depot_path}: no expected root type")
            root_type = data.get("RootChunk", {}).get("$type")
            require(root_type == EXPECTED_ROOT_TYPES[suffix], f"{display(raw_path)}: wrong root type {root_type!r}")
            payload = cooked_path.read_bytes()
            require(payload.startswith(b"CR2W"), f"{display(cooked_path)}: missing CR2W magic")
            require(root_type.encode("ascii") in payload, f"{display(cooked_path)}: cooked string table does not contain {root_type}")
    require(pair_count == 12, "Lab 3 must contain exactly twelve raw/cooked CR2W pairs")

    for depot_path in DEPOT_PATHS[1:]:
        for raw in (True, False):
            start_path = checkpoint_file(START, depot_path, raw=raw)
            completed_path = checkpoint_file(COMPLETED, depot_path, raw=raw)
            require(start_path.read_bytes() == completed_path.read_bytes(), f"Lab 3 checkpoints disagree on shared {depot_path}{'.json' if raw else ''}")
    require(
        checkpoint_file(START, QUEST_PHASE_PATH, raw=False).read_bytes()
        != checkpoint_file(COMPLETED, QUEST_PHASE_PATH, raw=False).read_bytes(),
        "Lab 3 start and completed cooked questphases must differ",
    )


def collect_handles(value: Any, result: dict[str, dict[str, Any]]) -> None:
    if isinstance(value, dict):
        handle_id = value.get("HandleId")
        data = value.get("Data")
        if isinstance(handle_id, str) and isinstance(data, dict):
            require(handle_id not in result, f"duplicate CR2W handle definition {handle_id}")
            result[handle_id] = data
        for child in value.values():
            collect_handles(child, result)
    elif isinstance(value, list):
        for child in value:
            collect_handles(child, result)


def handle_id(value: Any) -> str:
    require(isinstance(value, dict), "expected a CR2W handle object")
    identifier = value.get("HandleId") or value.get("HandleRefId")
    require(isinstance(identifier, str), "CR2W handle has no string ID")
    return identifier


def resolve(value: Any, handles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    identifier = handle_id(value)
    require(identifier in handles, f"unresolved CR2W handle {identifier}")
    return handles[identifier]


def iter_json_objects(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_json_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_json_objects(child)


def cname(value: str) -> dict[str, str]:
    return {"$type": "CName", "$storage": "string", "$value": value}


def node_ref(value: str | int) -> dict[str, str]:
    return {"$type": "NodeRef", "$storage": "string" if isinstance(value, str) else "uint64", "$value": str(value)}


def resource_path(value: str | int, *, flags: str = "Soft") -> dict[str, Any]:
    return {
        "DepotPath": {
            "$type": "ResourcePath",
            "$storage": "string" if isinstance(value, str) else "uint64",
            "$value": str(value),
        },
        "Flags": flags,
    }


def vector_values(value: Any, dimensions: int, context: str) -> tuple[float, ...]:
    require(isinstance(value, dict), f"{context}: vector must be an object")
    fields = ("X", "Y", "Z", "W")[:dimensions]
    require(value.get("$type") == f"Vector{dimensions}", f"{context}: wrong vector type")
    require(set(value) == {"$type", *fields}, f"{context}: vector fields changed")
    result = tuple(value.get(field) for field in fields)
    require(all(isinstance(item, (int, float)) and not isinstance(item, bool) and math.isfinite(item) for item in result), f"{context}: vector must be finite")
    return result


def close_tuple(actual: tuple[float, ...], expected: tuple[float, ...], context: str, *, tolerance: float = 1e-6) -> None:
    require(len(actual) == len(expected), f"{context}: tuple length changed")
    require(all(math.isclose(a, b, rel_tol=0, abs_tol=tolerance) for a, b in zip(actual, expected)), f"{context}: expected {expected!r}, got {actual!r}")


def graph_nodes(source: dict[str, Any]) -> tuple[dict[int, dict[str, Any]], dict[str, dict[str, Any]]]:
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(source, handles)
    root = source.get("Data", {}).get("RootChunk", {})
    require(
        set(root) == {"$type", "cookingPlatform", "graph", "inplacePhases", "phasePrefabs"}
        and root.get("$type") == "questQuestPhaseResource"
        and root.get("cookingPlatform") == "PLATFORM_PC"
        and root.get("inplacePhases") == [],
        "Lab 3 questphase root contract changed",
    )
    require(
        root.get("phasePrefabs") == [{"$type": "questQuestPrefabEntry", "prefabNodeRef": node_ref(PREFAB_LOCAL)}],
        "Lab 3 questphase must declare exactly the local cqa003 prefab root",
    )
    graph = resolve(root.get("graph"), handles)
    require(set(graph) == {"$type", "nodes"} and graph.get("$type") == "questGraphDefinition", "Lab 3 graph wrapper changed")
    wrappers = graph.get("nodes")
    require(isinstance(wrappers, list), "Lab 3 graph has no node array")
    nodes: dict[int, dict[str, Any]] = {}
    for wrapper in wrappers:
        node = resolve(wrapper, handles)
        node_id_value = node.get("id")
        require(isinstance(node_id_value, int) and node_id_value not in nodes, "Lab 3 graph has an invalid or duplicate node ID")
        nodes[node_id_value] = node
    return nodes, handles


def expected_sockets(node_id_value: int) -> list[tuple[str, str]]:
    red_type = EXPECTED_NODE_TYPES[node_id_value]
    if red_type == "questInputNodeDefinition":
        return [("CutDestination", "CutDestination"), ("Out", "Output")]
    if red_type == "questOutputNodeDefinition":
        return [("CutDestination", "CutDestination"), ("In", "Input")]
    if red_type == "questConditionNodeDefinition":
        return [("CutDestination", "CutDestination"), ("In", "Input"), ("True", "Output"), ("False", "Output")]
    if red_type == "questJournalNodeDefinition":
        return [
            ("CutDestination", "CutDestination"),
            ("Active", "Input"),
            ("Inactive", "Input"),
            ("Succeeded", "Input"),
            ("Failed", "Input"),
            ("Out", "Output"),
        ]
    if red_type == "questMappinManagerNodeDefinition":
        return [("CutDestination", "CutDestination"), ("Active", "Input"), ("Inactive", "Input"), ("Out", "Output")]
    return [("CutDestination", "CutDestination"), ("In", "Input"), ("Out", "Output")]


def validate_node_shell(node_id_value: int, node: dict[str, Any], handles: dict[str, dict[str, Any]]) -> None:
    require(node.get("$type") == EXPECTED_NODE_TYPES[node_id_value], f"Lab 3 node {node_id_value}: wrong type")
    sockets = node.get("sockets")
    require(isinstance(sockets, list), f"Lab 3 node {node_id_value}: sockets must be an array")
    actual: list[tuple[str, str]] = []
    for wrapper in sockets:
        socket = resolve(wrapper, handles)
        require(set(socket) == {"$type", "connections", "name", "type"} and socket.get("$type") == "questSocketDefinition", f"Lab 3 node {node_id_value}: socket payload changed")
        name = socket.get("name")
        require(isinstance(name, dict) and name.get("$type") == "CName" and isinstance(name.get("$value"), str), f"Lab 3 node {node_id_value}: invalid socket CName")
        actual.append((name["$value"], socket.get("type")))
    require(actual == expected_sockets(node_id_value), f"Lab 3 node {node_id_value}: exact socket inventory changed: {actual!r}")


def require_journal_path(value: Any, handles: dict[str, dict[str, Any]], real_path: str, class_name: str, context: str) -> None:
    path = resolve(value, handles)
    require(
        path
        == {
            "$type": "gameJournalPath",
            "className": cname(class_name),
            "editorPath": "",
            "fileEntryIndex": 2,
            "realPath": real_path,
        },
        f"{context}: journal path/class payload changed",
    )


def graph_edges(nodes: dict[int, dict[str, Any]], handles: dict[str, dict[str, Any]]) -> frozenset[tuple[int, str, int, str]]:
    socket_owner: dict[str, tuple[int, str]] = {}
    for node_id_value, node in nodes.items():
        for wrapper in node.get("sockets", []):
            identifier = handle_id(wrapper)
            socket = resolve(wrapper, handles)
            socket_owner[identifier] = (node_id_value, socket["name"]["$value"])

    edges: set[tuple[int, str, int, str]] = set()
    connections = [item for item in handles.values() if item.get("$type") == "graphGraphConnectionDefinition"]
    for connection in connections:
        source_id = handle_id(connection.get("source"))
        destination_id = handle_id(connection.get("destination"))
        require(source_id in socket_owner and destination_id in socket_owner, "Lab 3 graph connection targets an unowned socket")
        source_node, source_socket = socket_owner[source_id]
        destination_node, destination_socket = socket_owner[destination_id]
        edge = (source_node, source_socket, destination_node, destination_socket)
        require(edge not in edges, f"Lab 3 graph contains duplicate edge {edge!r}")
        edges.add(edge)
    return frozenset(edges)


def validate_graph_semantics() -> None:
    start_path = checkpoint_file(START, QUEST_PHASE_PATH, raw=True)
    start_nodes, start_handles = graph_nodes(load_json(start_path))
    require(set(start_nodes) == {0, 1}, f"{display(start_path)}: start graph must contain IDs 0 and 1 only")
    for node_id_value in (0, 1):
        validate_node_shell(node_id_value, start_nodes[node_id_value], start_handles)
    require(set(start_nodes[0]) == {"$type", "id", "sockets", "socketName"} and start_nodes[0].get("socketName") == cname("In1"), "Lab 3 start input payload changed")
    require(set(start_nodes[1]) == {"$type", "id", "sockets", "socketName", "type"} and start_nodes[1].get("socketName") == cname("Out1") and start_nodes[1].get("type") == "Terminating", "Lab 3 start output payload changed")
    require(graph_edges(start_nodes, start_handles) == frozenset({(0, "Out", 1, "In")}), "Lab 3 start graph must be the one-edge terminating scaffold")
    require(sum(item.get("$type") == "graphGraphConnectionDefinition" for item in start_handles.values()) == 1, "Lab 3 start graph must define one connection")

    completed_path = checkpoint_file(COMPLETED, QUEST_PHASE_PATH, raw=True)
    source = load_json(completed_path)
    nodes, handles = graph_nodes(source)
    require(set(nodes) == set(EXPECTED_NODE_TYPES), f"{display(completed_path)}: exact 16-node ID inventory changed")
    for node_id_value, node in nodes.items():
        validate_node_shell(node_id_value, node, handles)
    require(set(nodes[0]) == {"$type", "id", "sockets", "socketName"} and nodes[0].get("socketName") == cname("In1"), "Lab 3 node 0 payload changed")
    require(set(nodes[1]) == {"$type", "id", "sockets", "socketName", "type"} and nodes[1].get("socketName") == cname("Out1") and nodes[1].get("type") == "Terminating", "Lab 3 node 1 payload changed")

    condition = resolve(nodes[10].get("condition"), handles)
    comparison = resolve(condition.get("type"), handles)
    require(
        set(nodes[10]) == {"$type", "id", "sockets", "condition"}
        and condition == {"$type": "questFactsDBCondition", "type": condition["type"]}
        and comparison
        == {"$type": "questVarComparison_ConditionType", "comparisonType": "Equal", "factName": "cqa003_completed", "value": 0},
        "Lab 3 node 10 completed guard changed",
    )

    fact_writer = resolve(nodes[22].get("type"), handles)
    require(
        set(nodes[22]) == {"$type", "id", "sockets", "type"}
        and fact_writer == {"$type": "questSetVar_NodeType", "factName": "cqa003_completed", "setExactValue": 1, "value": 1},
        "Lab 3 node 22 persistent completion write changed",
    )

    journal_contract = {
        11: (QUEST_PATH, "gameJournalQuest"),
        12: (PHASE_PATH, "gameJournalQuestPhase"),
        13: (REACH_PATH, "gameJournalQuestObjective"),
        17: (REACH_PATH, "gameJournalQuestObjective"),
        18: (LEAVE_PATH, "gameJournalQuestObjective"),
        20: (LEAVE_PATH, "gameJournalQuestObjective"),
        21: (PHASE_PATH, "gameJournalQuestPhase"),
        23: (QUEST_PATH, "gameJournalQuest"),
    }
    for node_id_value, (real_path, class_name) in journal_contract.items():
        node = nodes[node_id_value]
        require(set(node) == {"$type", "id", "sockets", "type"}, f"Lab 3 node {node_id_value}: unexpected journal-node fields")
        node_type = resolve(node.get("type"), handles)
        require(
            set(node_type) == {"$type", "optional", "path", "sendNotification", "trackQuest", "version"}
            and node_type.get("$type") == "questJournalQuestEntry_NodeType"
            and node_type.get("optional") == 0
            and node_type.get("sendNotification") == 1
            and node_type.get("trackQuest") == 1
            and node_type.get("version") == "Initial",
            f"Lab 3 node {node_id_value}: journal presentation contract changed",
        )
        require_journal_path(node_type.get("path"), handles, real_path, class_name, f"Lab 3 node {node_id_value}")

    for node_id_value, disable_previous in ((14, 0), (16, 0)):
        node = nodes[node_id_value]
        require(set(node) == {"$type", "id", "sockets", "disablePreviousMappins", "path"}, f"Lab 3 node {node_id_value}: mappin fields changed")
        require(node.get("disablePreviousMappins") == disable_previous, f"Lab 3 node {node_id_value}: disablePreviousMappins changed")
        require_journal_path(node.get("path"), handles, MAPPIN_PATH, "gameJournalQuestMapPin", f"Lab 3 node {node_id_value}")

    empty_entity_ref = {
        "$type": "gameEntityReference",
        "dynamicEntityUniqueName": cname("None"),
        "names": [],
        "reference": node_ref(0),
        "sceneActorContextName": cname("None"),
        "slotName": cname("None"),
        "type": "EntityRef",
    }
    for node_id_value, ref, condition_type in ((15, REACH_LOCAL, "IsInside"), (19, LEAVE_LOCAL, "IsOutside")):
        node = nodes[node_id_value]
        require(set(node) == {"$type", "id", "sockets", "condition"}, f"Lab 3 node {node_id_value}: trigger-gate fields changed")
        trigger = resolve(node.get("condition"), handles)
        require(
            trigger
            == {
                "$type": "questTriggerCondition",
                "activatorRef": empty_entity_ref,
                "isPlayerActivator": 1,
                "triggerAreaRef": node_ref(ref),
                "type": condition_type,
            },
            f"Lab 3 node {node_id_value}: trigger condition changed",
        )

    fact_names = {item["factName"] for item in iter_json_objects(source) if isinstance(item.get("factName"), str)}
    require(fact_names == {"cqa003_completed"}, f"Lab 3 questphase fact inventory changed: {sorted(fact_names)!r}")
    edges = graph_edges(nodes, handles)
    require(len(edges) == 16 and edges == EXPECTED_EDGES, "Lab 3 completed exact 16-edge contract changed")
    require(sum(item.get("$type") == "graphGraphConnectionDefinition" for item in handles.values()) == 16, "Lab 3 completed source must define exactly 16 connections")


def visit_journal_entries(root: dict[str, Any], handles: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}

    def visit(entry: dict[str, Any], parents: tuple[str, ...]) -> None:
        entry_id_value = entry.get("id")
        parts = parents
        if entry_id_value is not None:
            require(isinstance(entry_id_value, str) and entry_id_value, "Lab 3 journal entry has an invalid ID")
            parts = (*parents, entry_id_value)
            path = "/".join(parts)
            require(path not in entries, f"Lab 3 journal has duplicate path {path}")
            entries[path] = entry
        children = entry.get("entries", [])
        require(isinstance(children, list), "Lab 3 journal child entries must be an array")
        for wrapper in children:
            visit(resolve(wrapper, handles), parts)

    visit(root, ())
    return entries


def validate_journal_localization_and_mappin() -> None:
    journal_path = checkpoint_file(COMPLETED, JOURNAL_PATH, raw=True)
    journal = load_json(journal_path)
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(journal, handles)
    root_chunk = journal.get("Data", {}).get("RootChunk", {})
    require(root_chunk.get("$type") == "gameJournalResource", f"{display(journal_path)}: wrong root type")
    journal_root = resolve(root_chunk.get("entry"), handles)
    require(journal_root.get("$type") == "gameJournalRootFolderEntry", f"{display(journal_path)}: missing journal root folder")
    require(journal_root.get("descriptor") == resource_path("base\\journal\\descriptor.journaldesc"), f"{display(journal_path)}: journal descriptor changed")
    entries = visit_journal_entries(journal_root, handles)
    expected_types = {
        "quests": "gameJournalPrimaryFolderEntry",
        "quests/minor_quest": "gameJournalFolderEntry",
        QUEST_PATH: "gameJournalQuest",
        PHASE_PATH: "gameJournalQuestPhase",
        REACH_PATH: "gameJournalQuestObjective",
        MAPPIN_PATH: "gameJournalQuestMapPin",
        LEAVE_PATH: "gameJournalQuestObjective",
    }
    require({path: entry.get("$type") for path, entry in entries.items()} == expected_types, f"{display(journal_path)}: exact journal tree changed")

    quest = entries[QUEST_PATH]
    reach = entries[REACH_PATH]
    leave = entries[LEAVE_PATH]
    mappin = entries[MAPPIN_PATH]
    require(quest.get("title") == {"unk1": "0", "value": "cqa_cqa003_title"} and quest.get("type") == "MinorQuest", "Lab 3 quest journal identity changed")
    require(reach.get("description") == {"unk1": "0", "value": "cqa_cqa003_objective_reach"} and reach.get("optional") == 0, "Lab 3 reach objective changed")
    require(leave.get("description") == {"unk1": "0", "value": "cqa_cqa003_objective_leave"} and leave.get("optional") == 0, "Lab 3 leave objective changed")
    require(mappin.get("enableGPS") == 1 and mappin.get("offset") == {"$type": "Vector3", "X": 0, "Y": 0, "Z": 0.5}, "Lab 3 journal mappin GPS/offset changed")
    reference = mappin.get("reference")
    require(isinstance(reference, dict) and reference.get("reference") == node_ref(MARKER_LOCAL) and reference.get("type") == "EntityRef", "Lab 3 journal mappin marker reference changed")
    mappin_data = mappin.get("mappinData")
    require(
        isinstance(mappin_data, dict)
        and mappin_data.get("$type") == "gamemappinsMappinData"
        and mappin_data.get("active") == 0
        and mappin_data.get("debugCaption") == "cqa_cqa003_mappin_checkpoint"
        and mappin_data.get("localizedCaption") == {"unk1": "0", "value": "cqa_cqa003_mappin_checkpoint"}
        and mappin_data.get("mappinType") == {"$type": "TweakDBID", "$storage": "string", "$value": "Mappins.QuestStaticMappinDefinition"}
        and mappin_data.get("variant") == "DefaultQuestVariant"
        and mappin_data.get("visibleThroughWalls") == 1,
        "Lab 3 journal mappin presentation changed",
    )

    localization_path = checkpoint_file(COMPLETED, LOCALIZATION_PATH, raw=True)
    localization = load_json(localization_path)
    localization_handles: dict[str, dict[str, Any]] = {}
    collect_handles(localization, localization_handles)
    onscreens = resolve(localization.get("Data", {}).get("RootChunk", {}).get("root"), localization_handles)
    require(onscreens.get("$type") == "localizationPersistenceOnScreenEntries", f"{display(localization_path)}: wrong onscreen root")
    raw_entries = onscreens.get("entries")
    require(isinstance(raw_entries, list) and len(raw_entries) == 4, f"{display(localization_path)}: expected four onscreen entries")
    localized: dict[str, str] = {}
    for index, entry in enumerate(raw_entries):
        require(
            isinstance(entry, dict)
            and set(entry) == {"$type", "femaleVariant", "maleVariant", "primaryKey", "secondaryKey"}
            and entry.get("$type") == "localizationPersistenceOnScreenEntry"
            and entry.get("primaryKey") == "0"
            and entry.get("maleVariant") == "",
            f"{display(localization_path)}: invalid onscreen entry {index}",
        )
        key = entry.get("secondaryKey")
        text = entry.get("femaleVariant")
        require(isinstance(key, str) and key not in localized and isinstance(text, str), f"{display(localization_path)}: invalid or duplicate localization key")
        localized[key] = text
    require(
        localized
        == {
            "cqa_cqa003_title": "Boundary Check",
            "cqa_cqa003_objective_reach": "Reach the marked checkpoint.",
            "cqa_cqa003_objective_leave": "Leave the checkpoint area.",
            "cqa_cqa003_mappin_checkpoint": "Boundary Check checkpoint",
        },
        f"{display(localization_path)}: exact lookup strings changed",
    )


def validate_sector_shell(root: dict[str, Any], category: str, level: int, node_count: int, context: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], dict[str, dict[str, Any]]]:
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
    require(root.get("$type") == "worldStreamingSector" and root.get("category") == category and root.get("level") == level, f"{context}: category/level changed")
    require(root.get("cookingPlatform") == "PLATFORM_None" and root.get("version") == 62, f"{context}: platform/version changed")
    require(root.get("externInplaceResource") == resource_path(0) and root.get("localInplaceResource") == [], f"{context}: inplace-resource contract changed")
    require(root.get("persistentNodeIndex") == 0 and root.get("persistentNodes") == [], f"{context}: persistent-node contract changed")
    require(root.get("variantIndices") == [0] and root.get("variantNodes") == [], f"{context}: variant contract changed")

    handles: dict[str, dict[str, Any]] = {}
    collect_handles(root, handles)
    wrappers = root.get("nodes")
    require(isinstance(wrappers, list) and len(wrappers) == node_count, f"{context}: expected {node_count} nodes")
    nodes = [resolve(wrapper, handles) for wrapper in wrappers]
    node_refs_raw = root.get("nodeRefs")
    require(isinstance(node_refs_raw, list) and len(node_refs_raw) == node_count, f"{context}: nodeRefs count changed")
    refs: list[str] = []
    for index, ref in enumerate(node_refs_raw):
        require(isinstance(ref, dict) and ref.get("$type") == "NodeRef" and ref.get("$storage") == "string" and isinstance(ref.get("$value"), str), f"{context}: invalid full nodeRef {index}")
        refs.append(ref["$value"])

    node_data = root.get("nodeData")
    require(
        isinstance(node_data, dict)
        and set(node_data) == {"BufferId", "Flags", "Type", "Data"}
        and node_data.get("BufferId") == "0"
        and node_data.get("Flags") == 0
        and node_data.get("Type") == "WolvenKit.RED4.Archive.Buffer.worldNodeDataBuffer, WolvenKit.RED4, Version=8.19.0.0, Culture=neutral, PublicKeyToken=null",
        f"{context}: worldNodeDataBuffer wrapper changed",
    )
    placements = node_data.get("Data")
    require(isinstance(placements, list) and len(placements) == node_count, f"{context}: nodeData count changed")
    indices = [item.get("NodeIndex") if isinstance(item, dict) else None for item in placements]
    require(indices == list(range(node_count)), f"{context}: nodeData.NodeIndex no longer aligns with nodes[]")
    return nodes, placements, refs, handles


def validate_placement(item: dict[str, Any], *, node_index: int, ref: str, position: tuple[float, float, float], max_distance: float, opaque_distance: float, context: str) -> None:
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
        f"{context}: nodeData fields changed",
    )
    require(item.get("Id") == "0" and item.get("NodeIndex") == node_index, f"{context}: placement identity changed")
    close_tuple(vector_values(item.get("Position"), 4, f"{context} Position"), (*position, 0), f"{context} Position")
    close_tuple(vector_values(item.get("Pivot"), 3, f"{context} Pivot"), position, f"{context} Pivot")
    require(item.get("Scale") == {"$type": "Vector3", "X": 1.0, "Y": 1.0, "Z": 1.0}, f"{context}: scale changed")
    bounds = item.get("Bounds")
    require(isinstance(bounds, dict) and set(bounds) == {"$type", "Max", "Min"} and bounds.get("$type") == "Box", f"{context}: bounds changed")
    close_tuple(vector_values(bounds.get("Min"), 4, f"{context} bounds min"), (*position, 0), f"{context} bounds min")
    close_tuple(vector_values(bounds.get("Max"), 4, f"{context} bounds max"), (*position, 0), f"{context} bounds max")
    orientation = item.get("Orientation")
    half_angle = math.radians(MARKER_YAW) / 2
    require(isinstance(orientation, dict) and set(orientation) == {"$type", "i", "j", "k", "r"} and orientation.get("$type") == "Quaternion", f"{context}: orientation shape changed")
    close_tuple((orientation["i"], orientation["j"], orientation["k"], orientation["r"]), (0, 0, math.sin(half_angle), math.cos(half_angle)), f"{context} orientation")
    require(item.get("QuestPrefabRefHash") == node_ref(ref), f"{context}: full child QuestPrefabRefHash changed")
    require(item.get("UkHash1") == node_ref(0) and item.get("CookedPrefabData") == resource_path(0, flags="Default"), f"{context}: prefab placeholder fields changed")
    require(item.get("MaxStreamingDistance") == max_distance and item.get("UkFloat1") == opaque_distance, f"{context}: streaming/opaque floats changed")
    require((item.get("Uk10"), item.get("Uk11"), item.get("Uk12"), item.get("Uk13"), item.get("Uk14")) == (1024, 512, 0, "0", "0"), f"{context}: opaque nodeData fields changed")


def decode_outline(outline: dict[str, Any], *, radius: float, point_count: int, height: float, context: str) -> None:
    require(set(outline) == {"$type", "buffer", "height", "points"} and outline.get("$type") == "AreaShapeOutline", f"{context}: outline fields changed")
    encoded = outline.get("buffer")
    require(isinstance(encoded, str), f"{context}: outline buffer is not base64 text")
    try:
        payload = base64.b64decode(encoded, validate=True)
    except (ValueError, base64.binascii.Error) as error:
        raise ValidationError(f"{context}: invalid outline base64") from error
    require(len(payload) == 4 + point_count * 16 + 4, f"{context}: authoritative outline buffer length changed")
    count = struct.unpack_from("<I", payload, 0)[0]
    require(count == point_count, f"{context}: authoritative outline point count changed")
    decoded: list[tuple[float, float, float, float]] = []
    offset = 4
    for _ in range(count):
        decoded.append(struct.unpack_from("<ffff", payload, offset))
        offset += 16
    decoded_height = struct.unpack_from("<f", payload, offset)[0]
    require(math.isclose(decoded_height, height, rel_tol=0, abs_tol=1e-6) and outline.get("height") == height, f"{context}: authoritative/visible heights disagree")
    visible = outline.get("points")
    require(isinstance(visible, list) and len(visible) == point_count, f"{context}: visible point count changed")
    for index, ((x, y, z, w), visible_point) in enumerate(zip(decoded, visible)):
        expected = (math.cos(2 * math.pi * index / point_count) * radius, math.sin(2 * math.pi * index / point_count) * radius, 0.0)
        close_tuple((x, y, z), expected, f"{context} authoritative point {index}", tolerance=1e-4)
        require(math.isclose(w, 1.0, rel_tol=0, abs_tol=1e-6), f"{context}: point {index} W changed")
        visible_xyz = vector_values(visible_point, 3, f"{context} visible point {index}")
        close_tuple(visible_xyz, (x, y, z), f"{context} visible/buffer point {index}", tolerance=1e-4)


def validate_trigger(node: dict[str, Any], handles: dict[str, dict[str, Any]], *, local_ref: str, radius: float, point_count: int, height: float, context: str) -> None:
    require(
        set(node) == {"$type", "color", "debugName", "isHostOnly", "isVisibleInGame", "notifiers", "outline", "proxyScale", "sourcePrefabHash", "tag", "tagExt"}
        and node.get("$type") == "worldTriggerAreaNode",
        f"{context}: trigger node shape changed",
    )
    require(node.get("debugName") == cname("{" + local_ref.removeprefix("#") + "}"), f"{context}: trigger debugName changed")
    require(node.get("isHostOnly") == 0 and node.get("isVisibleInGame") == 1 and node.get("proxyScale") is None, f"{context}: trigger visibility/host fields changed")
    require(node.get("sourcePrefabHash") == "0" and node.get("tag") == "None" and node.get("tagExt") == "None", f"{context}: trigger source/tag fields changed")
    require(node.get("color") == {"$type": "Color", "Alpha": 0, "Blue": 0, "Green": 0, "Red": 0}, f"{context}: trigger color changed")
    notifiers = node.get("notifiers")
    require(isinstance(notifiers, list) and len(notifiers) == 1, f"{context}: expected one notifier")
    notifier = resolve(notifiers[0], handles)
    require(notifier == {"$type": "questTriggerNotifier_Quest", "excludeChannels": 0, "includeChannels": "TC_Default", "isEnabled": 1}, f"{context}: quest notifier changed")
    outline = resolve(node.get("outline"), handles)
    decode_outline(outline, radius=radius, point_count=point_count, height=height, context=context)


def validate_world_sectors() -> None:
    quest_path = checkpoint_file(COMPLETED, QUEST_SECTOR_PATH, raw=True)
    quest_root = load_json(quest_path).get("Data", {}).get("RootChunk", {})
    nodes, placements, refs, handles = validate_sector_shell(quest_root, "Quest", 255, 2, "Lab 3 Quest sector")
    require(refs == [REACH_FULL, LEAVE_FULL], "Lab 3 Quest sector full nodeRefs changed")
    require([node.get("$type") for node in nodes] == ["worldTriggerAreaNode", "worldTriggerAreaNode"], "Lab 3 Quest sector nodes[] types changed")
    validate_trigger(nodes[0], handles, local_ref=REACH_LOCAL, radius=REACH_RADIUS, point_count=16, height=12, context="Lab 3 reach trigger")
    validate_trigger(nodes[1], handles, local_ref=LEAVE_LOCAL, radius=LEAVE_RADIUS, point_count=20, height=16, context="Lab 3 leave trigger")
    validate_placement(placements[0], node_index=0, ref=REACH_FULL, position=REACH_POSITION, max_distance=320, opaque_distance=280, context="Lab 3 reach placement")
    validate_placement(placements[1], node_index=1, ref=LEAVE_FULL, position=LEAVE_POSITION, max_distance=360, opaque_distance=320, context="Lab 3 leave placement")

    always_path = checkpoint_file(COMPLETED, ALWAYS_SECTOR_PATH, raw=True)
    always_root = load_json(always_path).get("Data", {}).get("RootChunk", {})
    marker_nodes, marker_placements, marker_refs, marker_handles = validate_sector_shell(always_root, "AlwaysLoaded", 1, 1, "Lab 3 AlwaysLoaded sector")
    require(marker_refs == [MARKER_FULL], "Lab 3 AlwaysLoaded sector full nodeRef changed")
    marker = marker_nodes[0]
    require(
        marker
        == {
            "$type": "worldStaticMarkerNode",
            "debugName": cname("{cqa003_mp_checkpoint}"),
            "isHostOnly": 0,
            "isVisibleInGame": 1,
            "proxyScale": None,
            "sourcePrefabHash": "0",
            "tag": "None",
            "tagExt": "None",
        },
        "Lab 3 static marker node changed",
    )
    require(marker_handles, "Lab 3 AlwaysLoaded sector marker must be handle-backed")
    validate_placement(marker_placements[0], node_index=0, ref=MARKER_FULL, position=MARKER_POSITION, max_distance=360, opaque_distance=320, context="Lab 3 marker placement")


def require_box(value: Any, minimum: tuple[float, float, float], maximum: tuple[float, float, float], context: str) -> None:
    require(isinstance(value, dict) and set(value) == {"$type", "Max", "Min"} and value.get("$type") == "Box", f"{context}: box fields changed")
    min_values = vector_values(value.get("Min"), 4, f"{context} min")
    max_values = vector_values(value.get("Max"), 4, f"{context} max")
    close_tuple(min_values[:3], minimum, f"{context} minimum")
    close_tuple(max_values[:3], maximum, f"{context} maximum")
    require(math.isclose(min_values[3], -3.40282347e38, rel_tol=1e-7) and math.isclose(max_values[3], 3.40282347e38, rel_tol=1e-7), f"{context}: W sentinel bounds changed")
    require(all(low <= high for low, high in zip(min_values, max_values)), f"{context}: bounds are inverted")


def validate_streaming_block() -> None:
    path = checkpoint_file(COMPLETED, BLOCK_PATH, raw=True)
    root = load_json(path).get("Data", {}).get("RootChunk", {})
    require(set(root) == {"$type", "cookingPlatform", "descriptors", "index"} and root.get("$type") == "worldStreamingBlock" and root.get("cookingPlatform") == "PLATFORM_PC", f"{display(path)}: streaming block root changed")
    block_index = {"$type": "worldStreamingBlockIndex", "oup": "Base", "rldGridCell": 0}
    require(root.get("index") == block_index, "Lab 3 streaming block index changed")
    descriptors = root.get("descriptors")
    require(isinstance(descriptors, list) and len(descriptors) == 2, "Lab 3 streaming block must contain Quest and AlwaysLoaded descriptors")
    expected = (
        ("Quest", QUEST_SECTOR_PATH, 0, node_ref(PREFAB_FULL), (-1300.02, 1197.2208, -291.7), (-700.02, 1797.2208, 308.3)),
        ("AlwaysLoaded", ALWAYS_SECTOR_PATH, 1, node_ref(0), (-99999, -99999, -99999), (99999, 99999, 99999)),
    )
    for index, (descriptor, contract) in enumerate(zip(descriptors, expected)):
        category, sector_path, level, prefab_ref, minimum, maximum = contract
        require(
            isinstance(descriptor, dict)
            and set(descriptor) == {"$type", "blockIndex", "category", "data", "level", "numNodeRanges", "questPrefabNodeRef", "streamingBox", "variants"}
            and descriptor.get("$type") == "worldStreamingSectorDescriptor",
            f"Lab 3 descriptor {index}: fields changed",
        )
        require(descriptor.get("blockIndex") == block_index and descriptor.get("category") == category and descriptor.get("level") == level, f"Lab 3 descriptor {index}: category/index/level changed")
        require(descriptor.get("data") == resource_path(sector_path.replace("/", "\\")), f"Lab 3 descriptor {index}: sector depot path changed")
        require(descriptor.get("numNodeRanges") == 1 and descriptor.get("variants") == [], f"Lab 3 descriptor {index}: node-range/variant contract changed")
        require(descriptor.get("questPrefabNodeRef") == prefab_ref, f"Lab 3 descriptor {index}: quest prefab root changed")
        require_box(descriptor.get("streamingBox"), minimum, maximum, f"Lab 3 descriptor {index} streamingBox")


def valid_sha256(value: Any, *, prefixed: bool = False) -> bool:
    if not isinstance(value, str):
        return False
    digest = value.removeprefix("sha256:") if prefixed else value
    if prefixed and not value.startswith("sha256:"):
        return False
    return len(digest) == 64 and all(character in "0123456789abcdef" for character in digest)


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


def validate_manifest() -> ManifestInfo:
    value = load_json(MANIFEST)
    require(
        set(value) == {"schema_version", "id", "title", "book_chapter", "baseline", "depot_paths", "persistent_facts", "evidence", "graph", "artifacts"},
        f"{display(MANIFEST)}: top-level schema changed",
    )
    require(value.get("schema_version") == 2 and value.get("id") == "cqa003" and value.get("title") == "Boundary Check", f"{display(MANIFEST)}: identity/schema changed")
    chapter = normalize_relative(value.get("book_chapter"), f"{display(MANIFEST)} book_chapter")
    require(chapter == "book/src/world/lab-03.md" and (ROOT / chapter).is_file(), f"{display(MANIFEST)}: wrong or missing book chapter")
    require(value.get("baseline") == BASELINE, f"{display(MANIFEST)}: pinned baseline changed")
    raw_depot_paths = value.get("depot_paths")
    require(isinstance(raw_depot_paths, list), f"{display(MANIFEST)}: depot_paths must be an array")
    depot_paths = tuple(
        normalize_relative(path, f"{display(MANIFEST)} depot_paths[{index}]")
        for index, path in enumerate(raw_depot_paths)
    )
    require(depot_paths == DEPOT_PATHS, f"{display(MANIFEST)}: exact six depot paths changed")
    require(value.get("persistent_facts") == ["cqa003_completed"], f"{display(MANIFEST)}: persistent fact inventory changed")
    evidence = value.get("evidence")
    require(
        isinstance(evidence, dict) and set(evidence) == {"structure", "runtime"},
        f"{display(MANIFEST)}: invalid evidence object",
    )
    require(
        evidence.get("structure")
        == {
            "status": "structurally-validated",
            "date": "2026-08-09",
            "method": "WolvenKit 8.19.0 deserialize and round-trip inspection",
        },
        f"{display(MANIFEST)}: structural evidence record changed",
    )
    runtime = evidence.get("runtime")
    require(isinstance(runtime, dict) and set(runtime) == {"status", "class", "date", "record"}, f"{display(MANIFEST)}: invalid runtime evidence object")
    runtime_status = runtime.get("status")
    runtime_class = runtime.get("class")
    runtime_date = runtime.get("date")
    require(runtime_status in {"pending", "passed", "failed"}, f"{display(MANIFEST)}: invalid runtime status")
    require(runtime_class == ("runtime-proven" if runtime_status == "passed" else "experimental"), f"{display(MANIFEST)}: runtime status and evidence class disagree")
    if runtime_status == "pending":
        require(runtime_date is None or valid_observed_date(runtime_date), f"{display(MANIFEST)}: pending runtime date must be null or YYYY-MM-DD")
    else:
        require(valid_observed_date(runtime_date), f"{display(MANIFEST)}: completed runtime evidence needs a YYYY-MM-DD date")
    runtime_record = normalize_relative(runtime.get("record"), f"{display(MANIFEST)} evidence.runtime.record")
    require(runtime_record == "runtime-acceptance.json", f"{display(MANIFEST)}: wrong runtime acceptance record")

    graph = value.get("graph")
    require(isinstance(graph, dict) and set(graph) == {"layout", "source_fingerprint"}, f"{display(MANIFEST)}: invalid graph object")
    layout = normalize_relative(graph.get("layout"), f"{display(MANIFEST)} graph.layout")
    require(layout == "assets/diagrams/lab-03/cqa003.questphase.layout.json", f"{display(MANIFEST)}: graph layout changed")
    fingerprint = graph.get("source_fingerprint")
    require(valid_sha256(fingerprint, prefixed=True), f"{display(MANIFEST)}: invalid graph fingerprint")

    artifacts = value.get("artifacts")
    require(isinstance(artifacts, dict) and set(artifacts) == {"algorithm", "files"}, f"{display(MANIFEST)}: artifact hash schema changed")
    require(artifacts.get("algorithm") == "sha256", f"{display(MANIFEST)}: artifact algorithm must be sha256")
    raw_hashes = artifacts.get("files")
    require(isinstance(raw_hashes, dict), f"{display(MANIFEST)}: artifact files must be an object")
    hashes: dict[str, str] = {}
    for raw_path, digest in raw_hashes.items():
        relative = normalize_relative(raw_path, f"{display(MANIFEST)} artifact path")
        require(relative not in hashes, f"{display(MANIFEST)}: duplicate artifact path {relative}")
        require(valid_sha256(digest), f"{display(MANIFEST)}: invalid SHA-256 for {relative}")
        hashes[relative] = digest
    expected_files = set(COMPLETED_FILES) - {"README.md", "example.json"}
    require(set(hashes) == expected_files, f"{display(MANIFEST)} artifact inventory: {difference(expected_files, set(hashes))}")
    for relative, expected_hash in hashes.items():
        actual_hash = hashlib.sha256((COMPLETED / relative).read_bytes()).hexdigest()
        require(actual_hash == expected_hash, f"{display(MANIFEST)}: stale SHA-256 for {relative}")
    return ManifestInfo(
        depot_paths=depot_paths,
        graph_fingerprint=fingerprint,
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
        f"{display(ACCEPTANCE)}:canonical: candidate shape changed",
    )
    require(candidate.get("manifest") == "example.json", f"{display(ACCEPTANCE)}:canonical: wrong manifest reference")
    installed = candidate.get("installed_files")
    require(isinstance(installed, list) and len(installed) == 2, f"{display(ACCEPTANCE)}:canonical: expected two installed files")
    expected_installed = [normalize_relative(path, "installed path") for path in EXPECTED_INSTALLED_FILES]
    installed_paths: list[str] = []
    installed_hashes: list[str | None] = []
    for index, item in enumerate(installed):
        require(isinstance(item, dict) and set(item) == {"path", "sha256"}, f"{display(ACCEPTANCE)}:canonical: installed_files[{index}] shape changed")
        installed_paths.append(normalize_relative(item.get("path"), f"{display(ACCEPTANCE)}:canonical: installed_files[{index}].path"))
        digest = item.get("sha256")
        require(digest is None or valid_sha256(digest), f"{display(ACCEPTANCE)}:canonical: invalid installed-file SHA-256")
        installed_hashes.append(digest)
    require(installed_paths == expected_installed, f"{display(ACCEPTANCE)}:canonical: installed-file inventory changed")
    raw_depot_paths = candidate.get("depot_paths")
    require(isinstance(raw_depot_paths, list), f"{display(ACCEPTANCE)}:canonical: depot_paths must be an array")
    depot_paths = [
        normalize_relative(path, f"{display(ACCEPTANCE)}:canonical: depot_paths[{index}]")
        for index, path in enumerate(raw_depot_paths)
    ]
    require(depot_paths == list(DEPOT_PATHS), f"{display(ACCEPTANCE)}:canonical: depot-path contract changed")
    return {"canonical": tuple(installed_hashes)}


def save_was_created_before_install(save_state: str) -> bool:
    return save_state.startswith("untouched-preinstall")


def validate_runs(value: Any) -> dict[str, dict[str, Any]]:
    require(isinstance(value, list), f"{display(ACCEPTANCE)}: runs must be an array")
    require(
        [item.get("id") if isinstance(item, dict) else None for item in value] == [item[0] for item in EXPECTED_RUNS],
        f"{display(ACCEPTANCE)}: exact eight-run identity/order changed",
    )
    expected_log_paths = [normalize_relative(path, "runtime log path") for path in EXPECTED_LOGS]
    runs: dict[str, dict[str, Any]] = {}
    for run, (run_id_value, save_state, save_provenance) in zip(value, EXPECTED_RUNS, strict=True):
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
            f"{display(ACCEPTANCE)}:{run_id_value}: run shape changed",
        )
        require(
            run.get("candidate_id") == "canonical"
            and run.get("save_state") == save_state
            and run.get("save_provenance") == save_provenance,
            f"{display(ACCEPTANCE)}:{run_id_value}: immutable candidate/save provenance changed",
        )
        timestamp = run.get("performed_at")
        require(timestamp is None or observed_timestamp(timestamp) is not None, f"{display(ACCEPTANCE)}:{run_id_value}: performed_at must be null or an offset ISO 8601 timestamp")
        tester = run.get("tester")
        require(tester is None or (isinstance(tester, str) and tester.strip()), f"{display(ACCEPTANCE)}:{run_id_value}: tester must be null or a non-empty string")

        environment = run.get("observed_environment")
        require(isinstance(environment, dict) and set(environment) == set(REQUIRED_ENVIRONMENT), f"{display(ACCEPTANCE)}:{run_id_value}: observed-environment shape changed")
        for key, observed in environment.items():
            require(observed is None or observed == REQUIRED_ENVIRONMENT[key], f"{display(ACCEPTANCE)}:{run_id_value}: observed {key} must be null or the pinned value")

        save = run.get("save")
        require(
            isinstance(save, dict) and set(save) == {"label", "slot_directory", "artifact", "created_before_first_install", "sha256"},
            f"{display(ACCEPTANCE)}:{run_id_value}: save shape changed",
        )
        require(save.get("artifact") == "sav.dat", f"{display(ACCEPTANCE)}:{run_id_value}: save artifact must remain sav.dat")
        for key in ("label", "slot_directory"):
            entry = save.get(key)
            require(entry is None or (isinstance(entry, str) and entry.strip()), f"{display(ACCEPTANCE)}:{run_id_value}: save.{key} must be null or a non-empty string")
        created = save.get("created_before_first_install")
        expected_created = save_was_created_before_install(save_state)
        require(created is None or created is expected_created, f"{display(ACCEPTANCE)}:{run_id_value}: created_before_first_install disagrees with save_state")
        digest = save.get("sha256")
        require(digest is None or valid_sha256(digest), f"{display(ACCEPTANCE)}:{run_id_value}: invalid save SHA-256")

        logs = run.get("logs")
        require(isinstance(logs, list) and len(logs) == 4, f"{display(ACCEPTANCE)}:{run_id_value}: expected four logs")
        log_paths: list[str] = []
        for index, item in enumerate(logs):
            require(isinstance(item, dict) and set(item) == {"path", "sha256"}, f"{display(ACCEPTANCE)}:{run_id_value}: logs[{index}] shape changed")
            log_paths.append(normalize_relative(item.get("path"), f"{display(ACCEPTANCE)}:{run_id_value}: logs[{index}].path"))
            log_digest = item.get("sha256")
            require(log_digest is None or valid_sha256(log_digest), f"{display(ACCEPTANCE)}:{run_id_value}: invalid log SHA-256")
        require(log_paths == expected_log_paths, f"{display(ACCEPTANCE)}:{run_id_value}: exact four-log inventory changed")
        runs[run_id_value] = run
    return runs


def validate_retained_evidence(case_id: str, value: Any) -> None:
    require(isinstance(value, list) and value, f"{display(ACCEPTANCE)}:{case_id}: completed case needs retained evidence")
    references: set[str] = set()
    completed_root = COMPLETED.resolve()
    for index, item in enumerate(value):
        require(isinstance(item, dict) and set(item) == {"type", "reference", "sha256"}, f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] shape changed")
        evidence_type = item.get("type")
        require(evidence_type in {"screenshot", "video", "log", "save-metadata", "notes"}, f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] has an invalid type")
        reference = normalize_relative(item.get("reference"), f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}].reference")
        require(reference.startswith("evidence/"), f"{display(ACCEPTANCE)}:{case_id}: evidence must stay below completed/evidence")
        require(
            all(":" not in part and part.casefold() not in {"con", "prn", "aux", "nul"} for part in PurePosixPath(reference).parts),
            f"{display(ACCEPTANCE)}:{case_id}: evidence reference uses an unsafe Windows path component",
        )
        require(reference not in references, f"{display(ACCEPTANCE)}:{case_id}: duplicate evidence reference {reference}")
        references.add(reference)
        digest = item.get("sha256")
        require(valid_sha256(digest), f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] needs a SHA-256")
        evidence_path = COMPLETED / reference
        require(evidence_path.is_file(), f"{display(evidence_path)}: retained evidence is missing")
        try:
            evidence_path.resolve().relative_to(completed_root)
        except ValueError as error:
            raise ValidationError(f"{display(evidence_path)}: evidence resolves outside the completed checkpoint") from error
        cursor = COMPLETED
        for part in PurePosixPath(reference).parts:
            cursor /= part
            require(not cursor.is_symlink(), f"{display(cursor)}: retained evidence paths cannot contain symlinks")
        require(evidence_path.name.lower() != "sav.dat" and evidence_path.suffix.lower() != ".dat", f"{display(evidence_path)}: private save binaries cannot be retained")
        if evidence_type == "save-metadata":
            require(evidence_path.suffix.lower() in {".md", ".txt", ".json"}, f"{display(evidence_path)}: save metadata must be sanitized text")
        require(hashlib.sha256(evidence_path.read_bytes()).hexdigest() == digest, f"{display(evidence_path)}: retained evidence SHA-256 mismatch")


def validate_completed_run(run_id_value: str, run: dict[str, Any], candidates: dict[str, tuple[str | None, ...]]) -> datetime:
    require(all(valid_sha256(digest) for digest in candidates[run["candidate_id"]]), f"{display(ACCEPTANCE)}:{run_id_value}: completed run needs both installed candidate hashes")
    timestamp = observed_timestamp(run.get("performed_at"))
    require(timestamp is not None, f"{display(ACCEPTANCE)}:{run_id_value}: completed run needs an offset timestamp")
    require(isinstance(run.get("tester"), str) and run["tester"].strip(), f"{display(ACCEPTANCE)}:{run_id_value}: completed run needs a tester")
    require(run.get("observed_environment") == REQUIRED_ENVIRONMENT, f"{display(ACCEPTANCE)}:{run_id_value}: completed run must record the exact observed environment")
    save = run["save"]
    require(
        isinstance(save.get("label"), str)
        and save["label"].strip()
        and isinstance(save.get("slot_directory"), str)
        and save["slot_directory"].strip()
        and valid_sha256(save.get("sha256")),
        f"{display(ACCEPTANCE)}:{run_id_value}: completed run needs a labelled, hash-bound save",
    )
    expected_created = save_was_created_before_install(run["save_state"])
    require(save.get("created_before_first_install") is expected_created, f"{display(ACCEPTANCE)}:{run_id_value}: untouched saves must be pre-install and derived saves must not be")
    require(all(valid_sha256(item.get("sha256")) for item in run["logs"]), f"{display(ACCEPTANCE)}:{run_id_value}: completed run needs four hash-bound logs")
    return timestamp


def require_related_save_hash(runs: dict[str, dict[str, Any]], source_id: str, reuse_id: str) -> None:
    source_digest = runs[source_id]["save"].get("sha256")
    reuse_digest = runs[reuse_id]["save"].get("sha256")
    require(valid_sha256(source_digest) and valid_sha256(reuse_digest) and source_digest == reuse_digest, f"{display(ACCEPTANCE)}:{reuse_id}: save hash must match {source_id}")


def validate_runtime_acceptance(info: ManifestInfo) -> None:
    value = load_json(ACCEPTANCE)
    require(
        set(value) == {"schema_version", "example_id", "status", "evidence_class", "required_environment", "candidates", "runs", "cases", "promotion_rule"},
        f"{display(ACCEPTANCE)}: top-level schema changed",
    )
    require(value.get("schema_version") == 3 and value.get("example_id") == "cqa003", f"{display(ACCEPTANCE)}: identity/schema changed")
    require(value.get("required_environment") == REQUIRED_ENVIRONMENT, f"{display(ACCEPTANCE)}: required environment changed")
    candidates = validate_candidates(value.get("candidates"))
    runs = validate_runs(value.get("runs"))

    cases = value.get("cases")
    require(isinstance(cases, list), f"{display(ACCEPTANCE)}: cases must be an array")
    require([case.get("id") if isinstance(case, dict) else None for case in cases] == list(EXPECTED_CASES), f"{display(ACCEPTANCE)}: immutable ten-case identity/order changed")
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
            require(case.get("observed") is None and case.get("evidence") == [], f"{display(ACCEPTANCE)}:{case_id}: pending case cannot claim observations/evidence")
        else:
            require(isinstance(case.get("observed"), str) and case["observed"].strip(), f"{display(ACCEPTANCE)}:{case_id}: completed case needs a non-empty observation")
            validate_retained_evidence(case_id, case.get("evidence"))
            completed_run_ids.update(run_ids)

    if any(status == "failed" for status in statuses):
        expected_status = "failed"
    elif all(status == "passed" for status in statuses):
        expected_status = "passed"
    else:
        expected_status = "pending"
    expected_class = "runtime-proven" if expected_status == "passed" else "experimental"
    require(value.get("status") == expected_status, f"{display(ACCEPTANCE)}: top-level status disagrees with required cases")
    require(value.get("evidence_class") == expected_class, f"{display(ACCEPTANCE)}: evidence_class disagrees with derived status")
    require(info.runtime_status == expected_status, f"{display(MANIFEST)}: runtime status disagrees with acceptance cases")
    require(info.runtime_class == expected_class, f"{display(MANIFEST)}: runtime evidence class disagrees with acceptance cases")

    completed_timestamps: dict[str, datetime] = {}
    for run_id_value in sorted(completed_run_ids):
        completed_timestamps[run_id_value] = validate_completed_run(run_id_value, runs[run_id_value], candidates)
    require(
        len(set(completed_timestamps.values())) == len(completed_timestamps),
        f"{display(ACCEPTANCE)}: completed executions must use distinct performed_at timestamps",
    )
    completed_log_bundles = {
        run_id_value: tuple(item["sha256"] for item in runs[run_id_value]["logs"])
        for run_id_value in completed_run_ids
    }
    require(
        len(set(completed_log_bundles.values())) == len(completed_log_bundles),
        f"{display(ACCEPTANCE)}: completed executions must use distinct four-log hash bundles",
    )

    related_saves = (
        ("clean-walk", "clean-replay"),
        ("pre-reach-reload", "stream-away-return"),
        ("completed-reload", "completed-reinstall"),
    )
    for source_id, reuse_id in related_saves:
        source_digest = runs[source_id]["save"].get("sha256")
        reuse_digest = runs[reuse_id]["save"].get("sha256")
        if source_digest is not None and reuse_digest is not None:
            require(source_digest == reuse_digest, f"{display(ACCEPTANCE)}:{reuse_id}: populated save hash must match {source_id}")
        if reuse_id in completed_run_ids:
            require_related_save_hash(runs, source_id, reuse_id)

    expected_date = max((timestamp.date().isoformat() for timestamp in completed_timestamps.values()), default=None)
    require(info.runtime_date == expected_date, f"{display(MANIFEST)}: runtime date must equal the latest completed referenced-run date {expected_date!r}")
    require(value.get("promotion_rule") == PROMOTION_RULE, f"{display(ACCEPTANCE)}: promotion rule changed")


def marker_lines(path: Path) -> list[str]:
    require(path.is_file(), f"{display(path)}: missing reader-facing Lab 3 page")
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("**Lab 3 runtime evidence:**")]


def validate_diagram_reader_status(info: ManifestInfo) -> None:
    expected_asset_paths = {DIAGRAM_ASSET_DIR / name for name in DIAGRAM_NAMES}
    expected_publish_paths = {DIAGRAM_PUBLISH_DIR / name for name in DIAGRAM_NAMES}
    require(
        set(DIAGRAM_ASSET_DIR.glob("*.svg")) == expected_asset_paths,
        f"{display(DIAGRAM_ASSET_DIR)}: exact three-SVG inventory changed",
    )
    require(
        set(DIAGRAM_PUBLISH_DIR.glob("*.svg")) == expected_publish_paths,
        f"{display(DIAGRAM_PUBLISH_DIR)}: exact three-SVG inventory changed",
    )
    display_class = {
        "experimental": "Experimental",
        "runtime-proven": "Runtime-proven",
    }[info.runtime_class]
    display_date = info.runtime_date if info.runtime_date is not None else "Not yet recorded"
    expected_badge = f"cqa003 • {display_class}"
    expected_footer = (
        f"{display_class} — runtime evidence {info.runtime_status}"
        f" • test date: {display_date}"
    )
    expected_description_state = (
        f"Diagram evidence state: {info.runtime_status}; runtime test date: "
        f"{display_date}."
    )
    expected_titles = {
        "cqa003.questphase.svg": f"cqa003 Boundary Check exact quest graph — {display_class}",
        "cqa003.resource-chain.svg": f"cqa003 resource ownership and reference chain — {display_class}",
        "cqa003.trigger-volume-plan.svg": f"cqa003 polygonal trigger-volume plan — {display_class}",
    }
    namespace = "http://www.w3.org/2000/svg"
    for name in DIAGRAM_NAMES:
        asset = DIAGRAM_ASSET_DIR / name
        published = DIAGRAM_PUBLISH_DIR / name
        require(asset.read_bytes() == published.read_bytes(), f"{display(published)}: published SVG differs from its canonical asset")
        try:
            root = ET.parse(asset).getroot()
        except (OSError, ET.ParseError) as error:
            raise ValidationError(f"{display(asset)}: invalid SVG XML: {error}") from error
        require(root.tag == f"{{{namespace}}}svg", f"{display(asset)}: wrong SVG root")
        title = root.find(f"{{{namespace}}}title")
        description = root.find(f"{{{namespace}}}desc")
        metadata = root.find(f"{{{namespace}}}metadata")
        require(title is not None and title.text == expected_titles[name], f"{display(asset)}: stale evidence class in SVG title")
        require(description is not None and isinstance(description.text, str) and expected_description_state in description.text, f"{display(asset)}: stale evidence state/date in SVG description")
        require(metadata is not None and isinstance(metadata.text, str), f"{display(asset)}: missing SVG metadata")
        try:
            metadata_value = json.loads(metadata.text, object_pairs_hook=reject_duplicate_keys)
        except json.JSONDecodeError as error:
            raise ValidationError(f"{display(asset)}: invalid SVG metadata JSON: {error}") from error
        require(
            isinstance(metadata_value, dict)
            and metadata_value.get("evidence")
            == {"status": info.runtime_status, "class": info.runtime_class, "date": info.runtime_date},
            f"{display(asset)}: stale evidence state/date in SVG metadata",
        )
        text_values = [
            element.text
            for element in root.findall(f".//{{{namespace}}}text")
            if isinstance(element.text, str)
        ]
        badges = [value for value in text_values if value.startswith("cqa003 •")]
        footers = [value for value in text_values if "runtime evidence" in value]
        require(badges == [expected_badge], f"{display(asset)}: stale or duplicate SVG evidence badge")
        require(footers == [expected_footer], f"{display(asset)}: stale or duplicate SVG evidence footer")


def validate_reader_status(info: ManifestInfo) -> None:
    marker_by_state = {
        ("pending", "experimental"): "**Lab 3 runtime evidence:** **Experimental** — pending.",
        ("failed", "experimental"): "**Lab 3 runtime evidence:** **Experimental** — failed.",
        ("passed", "runtime-proven"): "**Lab 3 runtime evidence:** **Runtime-proven** — passed.",
    }
    state = (info.runtime_status, info.runtime_class)
    require(state in marker_by_state, f"{display(MANIFEST)}: runtime status/class cannot produce a reader marker")
    expected_marker = marker_by_state[state]
    expected_date = info.runtime_date if info.runtime_date is not None else "Not yet recorded"
    date_row = f"| Runtime test date | {expected_date} |"

    book_pages = sorted(BOOK_WORLD.glob("lab-03*.md"))
    expected_book_pages = {
        BOOK_WORLD / "lab-03.md",
        BOOK_WORLD / "lab-03-authoring.md",
        BOOK_WORLD / "lab-03-test.md",
    }
    require(
        set(book_pages) == expected_book_pages,
        f"{display(BOOK_WORLD)}: expected exactly lab-03.md, lab-03-authoring.md, and lab-03-test.md",
    )
    for page in book_pages:
        text = page.read_text(encoding="utf-8")
        require(
            marker_lines(page) == [expected_marker],
            f"{display(page)}: Lab 3 runtime evidence marker must be exactly {expected_marker!r}",
        )
        require(date_row in text, f"{display(page)}: runtime test date must be {expected_date!r}")

    status_pages = (
        ROOT / "README.md",
        ROOT / "HANDOFF.md",
        ROOT / "ROADMAP.md",
        ROOT / "book" / "src" / "introduction.md",
        BOOK_WORLD / "index.md",
        ROOT / "book" / "src" / "reference" / "evidence-version-matrix.md",
        LAB / "README.md",
        START / "README.md",
        COMPLETED / "README.md",
    )
    for page in status_pages:
        require(
            marker_lines(page) == [expected_marker],
            f"{display(page)}: missing, stale, or duplicate Lab 3 runtime evidence marker",
        )
    validate_diagram_reader_status(info)


def validate_generated_diagrams() -> None:
    require(DIAGRAM_SCRIPT.is_file(), f"{display(DIAGRAM_SCRIPT)}: missing Lab 3 diagram generator")
    completed = subprocess.run(
        [sys.executable, "-B", str(DIAGRAM_SCRIPT), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    require(
        completed.returncode == 0,
        f"Lab 3 generated diagram check failed{': ' + output if output else ''}",
    )


def validate_manifest_graph_fingerprint(info: ManifestInfo) -> None:
    module = load_module(RENDER_SCRIPT, "_cqa_render_lab03_validation")
    try:
        nodes, edges = module.parse_graph(load_json(checkpoint_file(COMPLETED, QUEST_PHASE_PATH, raw=True)))
        fingerprint = module.fingerprint(nodes, edges)
    finally:
        sys.modules.pop(module.__name__, None)
    require(fingerprint == info.graph_fingerprint, f"{display(MANIFEST)}: graph fingerprint is stale")


def run_check(name: str, check: Callable[[], None]) -> bool:
    try:
        check()
    except Exception as error:
        print(f"[FAIL] {name}: {error}", file=sys.stderr)
        return False
    print(f"[ OK ] {name}")
    return True


def main() -> int:
    manifest_info: ManifestInfo | None = None
    try:
        manifest_info = validate_manifest()
    except Exception as error:
        print(f"[FAIL] Lab 3 manifest and artifact hashes: {error}", file=sys.stderr)
    else:
        print("[ OK ] Lab 3 manifest and artifact hashes")

    checks: list[tuple[str, Callable[[], None]]] = [
        ("Lab 3 exact checkpoint inventories and LF text", validate_inventories),
        ("Lab 3 generator byte determinism", validate_generated_raw),
        ("Lab 3 deterministic diagram outputs", validate_generated_diagrams),
        ("Lab 3 projects, ArchiveXL, and twelve CR2W pairs", validate_projects_archive_xl_and_cr2w_pairs),
        ("Lab 3 exact start/completed graph semantics", validate_graph_semantics),
        ("Lab 3 journal, localization, and mappin contract", validate_journal_localization_and_mappin),
        ("Lab 3 Quest and AlwaysLoaded sector semantics", validate_world_sectors),
        ("Lab 3 streaming-block descriptor semantics", validate_streaming_block),
    ]
    if manifest_info is not None:
        checks.append(("Lab 3 state-aware runtime-acceptance contract", lambda: validate_runtime_acceptance(manifest_info)))
        checks.append(("Lab 3 reader-facing evidence state and runtime dates", lambda: validate_reader_status(manifest_info)))
        checks.append(("Lab 3 graph fingerprint", lambda: validate_manifest_graph_fingerprint(manifest_info)))
    results = [run_check(name, check) for name, check in checks]
    passed = manifest_info is not None and all(results)
    if passed:
        print("Lab 3 validation passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
