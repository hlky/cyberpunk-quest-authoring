#!/usr/bin/env python3
"""Validate the complete Lab 2 Signal Race reference project.

This validator is intentionally standalone and standard-library-only.  It is
called by ``scripts/validate.py``, but can also be run directly from the
repository root while authoring Lab 2.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-02-signal-race"
START = LAB / "start"
COMPLETED = LAB / "completed"
BOOK_GATES = ROOT / "book" / "src" / "gates"
MANIFEST = COMPLETED / "example.json"
ACCEPTANCE = COMPLETED / "runtime-acceptance.json"
BUILD_SCRIPT = ROOT / "scripts" / "build_lab02_sources.py"
RENDER_SCRIPT = ROOT / "scripts" / "render_quest_graph.py"
LAYOUT = ROOT / "assets" / "diagrams" / "lab-02" / "cqa002.questphase.layout.json"
SVG = ROOT / "book" / "src" / "images" / "lab-02" / "cqa002.questphase.svg"

DEPOT_PATHS = (
    "mod/cqa/cqa002/phases/cqa002.questphase",
    "mod/cqa/cqa002/journal/cqa002.journal",
    "mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json",
)
FACTS = (
    "cqa002_test_mode",
    "cqa002_signal_failed",
    "cqa002_signal_stop",
    "cqa002_signal_succeeded",
    "cqa002_completed",
)
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
        "CQA_Lab02_SignalRace_Start.cpmodproj",
        "README.md",
        *RAW_RELATIVE,
        *COOKED_RELATIVE,
        "source/resources/CQA_Lab02_SignalRace_Start.archive.xl",
    }
)
COMPLETED_FILES = frozenset(
    {
        "CQA_Lab02_SignalRace.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        *RAW_RELATIVE,
        *COOKED_RELATIVE,
        "source/resources/CQA_Lab02_SignalRace.archive.xl",
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
}
EXPECTED_INSTALLED_FILES = [
    "archive\\pc\\mod\\CQA_Lab02_SignalRace.archive",
    "archive\\pc\\mod\\CQA_Lab02_SignalRace.archive.xl",
]
EXPECTED_LOGS = [
    "red4ext\\plugins\\ArchiveXL\\ArchiveXL.log",
    "red4ext\\logs\\red4ext.log",
    "red4ext\\logs\\game.log",
    "r6\\logs\\redscript_rCURRENT.log",
]
PROMOTION_RULE = (
    "Set status to passed and evidence_class to runtime-proven only when every required case passes and evidence "
    "binds both candidate builds, all six executions, the two distinct untouched pre-install saves and derived "
    "mid-flow/completed saves, exact versions, and all four logs for every execution."
)
EXPECTED_CASES: dict[str, tuple[list[str], str, str]] = {
    "clean-save-stable-route": (
        ["canonical-clean"],
        "Install the canonical mode-2 candidate and load an untouched pre-Lab-2 save.",
        "Signal Race and both objectives activate once; the optional objective remains active before the 120-second "
        "stable result, then succeeds, and the required objective and quest succeed.",
    ),
    "immediate-selector-versus-pause": (
        ["canonical-clean"],
        "Run the canonical mode-2 candidate and record the visible objective states before and after the 120-second result.",
        "Both objectives remain active before the 120-second result, then the optional objective succeeds once. Exact "
        "graph evidence owns the immediate-selector and waiting-gate attribution; this runtime case records visible "
        "state and timing.",
    ),
    "logical-and-fulfilment": (
        ["canonical-clean"],
        "Use canonical test_mode 2 and measure from objective activation without pausing the game.",
        "With canonical mode 2, the optional objective remains active before the 120-second result and succeeds "
        "afterward. Exact source and graph evidence own the configured two-child AND attribution; this is not a "
        "one-child negative control.",
    ),
    "source-edit-failure-route": (
        ["source-edit-failure"],
        "Change only node [11] to set exact test_mode 1, rebuild, retain the edited archive hash, and load a "
        "separate untouched pre-Lab-2 save.",
        "The optional objective remains active before the 30-second failure result, then fails, and the required "
        "objective and quest still succeed. Exact source and graph evidence own the internal route attribution.",
    ),
    "xor-route-convergence": (
        ["canonical-clean", "source-edit-failure"],
        "Complete one clean canonical run and one clean source-edit failure run; retain visible journal transitions "
        "and exact candidate hashes.",
        "The canonical optional objective succeeds and the edited optional objective fails; both are followed by "
        "required-objective and quest completion. Exact graph evidence maps those routes to In2 and In1 respectively. "
        "This does not test winner, cancellation, repeat-emission, or simultaneous-arrival policy.",
    ),
    "mid-flow-reload": (
        ["canonical-mid-flow-reload"],
        "After both canonical objectives activate, save while the optional objective remains visibly active before "
        "its roughly 120-second outcome; reload and record whether elapsed time resumes or restarts.",
        "Reloading neither duplicates journal activation nor blocks eventual single completion; timer behavior is "
        "recorded explicitly.",
    ),
    "completed-save-reload": (
        ["canonical-completed-reload"],
        "Save after canonical completion and reload without changing the installation.",
        "No quest or objective reactivation and no delayed visible journal update occurs. Exact graph evidence maps "
        "this bypass to the cqa002_completed guard's False route.",
    ),
    "completed-save-reinstall": (
        ["canonical-reinstall"],
        "Remove and reinstall the identical canonical candidate, then load its completed save.",
        "The quest remains completed and does not create a second activation.",
    ),
    "clean-replay": (
        ["canonical-clean-replay"],
        "Reload the original untouched pre-install save with the canonical candidate still installed.",
        "The stable route activates and completes once with the same player-facing result.",
    ),
    "registration-and-lookup-logs": (
        [
            "canonical-clean",
            "canonical-mid-flow-reload",
            "canonical-completed-reload",
            "canonical-reinstall",
            "canonical-clean-replay",
            "source-edit-failure",
        ],
        "Retain a fresh four-file RED4ext/ArchiveXL/redscript log set from each of the six executions.",
        "All six log sets contain no cqa002 registration, depot-path, journal, localization, or condition error.",
    ),
}

EXPECTED_RUNS: tuple[tuple[str, str, str, str], ...] = (
    ("canonical-clean", "canonical-mode-2", "untouched-preinstall", "canonical-original"),
    ("canonical-mid-flow-reload", "canonical-mode-2", "mid-flow", "canonical-clean-derived"),
    ("canonical-completed-reload", "canonical-mode-2", "completed", "canonical-completed"),
    ("canonical-reinstall", "canonical-mode-2", "completed", "canonical-completed"),
    ("canonical-clean-replay", "canonical-mode-2", "untouched-preinstall", "canonical-original"),
    ("source-edit-failure", "source-edit-mode-1", "untouched-preinstall", "source-edit-original"),
)

EXPECTED_NODE_TYPES = {
    0: "questInputNodeDefinition",
    1: "questOutputNodeDefinition",
    10: "questConditionNodeDefinition",
    11: "questFactsDBManagerNodeDefinition",
    12: "questJournalNodeDefinition",
    13: "questJournalNodeDefinition",
    14: "questJournalNodeDefinition",
    15: "questPauseConditionNodeDefinition",
    16: "questPauseConditionNodeDefinition",
    17: "questConditionNodeDefinition",
    18: "questPauseConditionNodeDefinition",
    19: "questFactsDBManagerNodeDefinition",
    20: "questPauseConditionNodeDefinition",
    21: "questFactsDBManagerNodeDefinition",
    22: "questJournalNodeDefinition",
    23: "questJournalNodeDefinition",
    24: "questFactsDBManagerNodeDefinition",
    25: "questLogicalXorNodeDefinition",
    26: "questJournalNodeDefinition",
    27: "questFactsDBManagerNodeDefinition",
    28: "questJournalNodeDefinition",
}
EXPECTED_EDGES = frozenset(
    {
        (0, "Out", 10, "In"),
        (10, "False", 1, "In"),
        (10, "True", 11, "In"),
        (11, "Out", 12, "Active"),
        (12, "Out", 13, "Active"),
        (13, "Out", 14, "Active"),
        (14, "Out", 15, "In"),
        (14, "Out", 16, "In"),
        (14, "Out", 17, "In"),
        (17, "True", 18, "In"),
        (18, "Out", 19, "In"),
        (17, "False", 20, "In"),
        (20, "Out", 21, "In"),
        (15, "Out", 22, "Failed"),
        (22, "Out", 25, "In1"),
        (16, "Out", 23, "Succeeded"),
        (23, "Out", 24, "In"),
        (24, "Out", 25, "In2"),
        (25, "Out1", 26, "Succeeded"),
        (26, "Out", 27, "In"),
        (27, "Out", 28, "Succeeded"),
        (28, "Out", 1, "In"),
    }
)


class ValidationError(RuntimeError):
    """A Lab 2 repository invariant was not satisfied."""


@dataclass(frozen=True)
class ManifestInfo:
    depot_paths: tuple[str, ...]
    artifact_hashes: tuple[tuple[str, str], ...]
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
    require(isinstance(value, str) and value.strip(), f"{context}: expected a non-empty relative path")
    raw = value.replace("\\", "/")
    require(not raw.startswith("/") and ":" not in raw.split("/", 1)[0], f"{context}: absolute path is not allowed")
    require(all(part not in {"", ".", ".."} for part in raw.split("/")), f"{context}: unsafe path component")
    return PurePosixPath(raw).as_posix()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"{display(path)}: missing JSON file")
    require(path.stat().st_size <= 16 * 1024 * 1024, f"{display(path)}: JSON file is unexpectedly large")
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"{display(path)}: invalid UTF-8 JSON: {error}") from error
    require(isinstance(value, dict), f"{display(path)}: top-level JSON value must be an object")
    return value


def actual_files(root: Path) -> set[str]:
    require(root.is_dir(), f"{display(root)}: missing directory")
    return {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}


def retained_evidence_inventory() -> set[str]:
    """Return the acceptance-bound evidence files allowed in the checkpoint."""

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


def difference(expected: set[str] | frozenset[str], actual: set[str]) -> str:
    parts: list[str] = []
    if expected - actual:
        parts.append("missing " + ", ".join(sorted(expected - actual)))
    if actual - expected:
        parts.append("unexpected " + ", ".join(sorted(actual - expected)))
    return "; ".join(parts) or "no difference"


def run_git(*arguments: str) -> list[str]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(result.returncode == 0, f"git {' '.join(arguments)} failed: {result.stderr.strip()}")
    return [line for line in result.stdout.splitlines() if line]


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import {display(path)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def validate_inventories() -> None:
    retained_evidence = retained_evidence_inventory()
    completed_files = set(COMPLETED_FILES) | retained_evidence
    checkpoints = (
        (START, START_FILES, START_TEXT_FILES),
        (COMPLETED, completed_files, COMPLETED_TEXT_FILES),
    )
    for checkpoint, expected, text_files in checkpoints:
        actual = actual_files(checkpoint)
        require(actual == set(expected), f"{display(checkpoint)} inventory: {difference(expected, actual)}")
        for relative in sorted(text_files):
            path = checkpoint / relative
            payload = path.read_bytes()
            require(b"\r" not in payload, f"{display(path)}: text must use LF endings")
            try:
                payload.decode("utf-8")
            except UnicodeDecodeError as error:
                raise ValidationError(f"{display(path)}: text must be UTF-8: {error}") from error

    lab_files = set(LAB_FILES) | {f"completed/{path}" for path in retained_evidence}
    actual_lab = actual_files(LAB)
    require(actual_lab == lab_files, f"{display(LAB)} inventory: {difference(lab_files, actual_lab)}")
    for path in (LAB / "LICENSE.md", LAB / "README.md"):
        payload = path.read_bytes()
        require(b"\r" not in payload, f"{display(path)}: text must use LF endings")
        payload.decode("utf-8")

    pathspec = LAB.relative_to(ROOT).as_posix()
    expected_tracked = {(LAB / relative).relative_to(ROOT).as_posix() for relative in lab_files}
    tracked = set(run_git("ls-files", "--cached", "--", pathspec))
    require(tracked == expected_tracked, f"{display(LAB)} Git inventory: {difference(expected_tracked, tracked)}")
    untracked = run_git("ls-files", "--others", "--exclude-standard", "--", pathspec)
    require(not untracked, f"{display(LAB)} has untracked files: {', '.join(untracked)}")


def generated_raw_set(checkpoint: Path) -> set[str]:
    raw = checkpoint / "source" / "raw"
    return actual_files(raw)


def generate_into(root: Path, module_name: str) -> None:
    module = load_module(BUILD_SCRIPT, module_name)
    try:
        module.CHECKPOINTS = {"start": root / "start", "completed": root / "completed"}
        module.main()
    finally:
        sys.modules.pop(module_name, None)


def validate_generated_raw() -> None:
    expected = {f"{path}.json" for path in DEPOT_PATHS}
    with tempfile.TemporaryDirectory(prefix="cqa-lab02-raw-a-") as first_name, tempfile.TemporaryDirectory(
        prefix="cqa-lab02-raw-b-"
    ) as second_name:
        first = Path(first_name)
        second = Path(second_name)
        generate_into(first, "_cqa_build_lab02_sources_a")
        generate_into(second, "_cqa_build_lab02_sources_b")
        for checkpoint_name, checked_root in (("start", START), ("completed", COMPLETED)):
            first_checkpoint = first / checkpoint_name
            second_checkpoint = second / checkpoint_name
            first_set = generated_raw_set(first_checkpoint)
            second_set = generated_raw_set(second_checkpoint)
            require(first_set == expected, f"Lab 2 {checkpoint_name} generator inventory: {difference(expected, first_set)}")
            require(second_set == expected, f"Lab 2 {checkpoint_name} second generator inventory differs")
            for relative in sorted(expected):
                generated_a = first_checkpoint / "source" / "raw" / relative
                generated_b = second_checkpoint / "source" / "raw" / relative
                checked = checked_root / "source" / "raw" / relative
                require(
                    generated_a.read_bytes() == generated_b.read_bytes(),
                    f"Lab 2 {checkpoint_name} generator is not byte-deterministic for {relative}",
                )
                require(
                    generated_a.read_bytes() == checked.read_bytes(),
                    f"{display(checked)}: generated CR2W-JSON is stale",
                )


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
        set(value) == {
            "schema_version", "id", "title", "book_chapter", "baseline", "depot_paths",
            "persistent_facts", "evidence", "graph", "artifacts",
        },
        f"{display(MANIFEST)}: top-level schema changed",
    )
    require(value.get("schema_version") == 2, f"{display(MANIFEST)}: schema_version must be 2")
    require(value.get("id") == "cqa002" and value.get("title") == "Signal Race", f"{display(MANIFEST)}: Lab 2 identity changed")
    chapter = normalize_relative(value.get("book_chapter"), f"{display(MANIFEST)} book_chapter")
    require(chapter == "book/src/gates/lab-02.md" and (ROOT / chapter).is_file(), f"{display(MANIFEST)}: wrong or missing book chapter")
    require(value.get("baseline") == BASELINE, f"{display(MANIFEST)}: pinned baseline mismatch")

    raw_depot_paths = value.get("depot_paths")
    require(isinstance(raw_depot_paths, list), f"{display(MANIFEST)}: depot_paths must be a list")
    depot_paths = tuple(
        normalize_relative(path, f"{display(MANIFEST)} depot_paths[{index}]")
        for index, path in enumerate(raw_depot_paths)
    )
    require(depot_paths == DEPOT_PATHS, f"{display(MANIFEST)}: depot path order or inventory changed")
    require(value.get("persistent_facts") == list(FACTS), f"{display(MANIFEST)}: five-fact contract changed")

    evidence = value.get("evidence")
    require(isinstance(evidence, dict) and set(evidence) == {"structure", "runtime"}, f"{display(MANIFEST)}: invalid evidence object")
    require(
        evidence.get("structure") == {
            "status": "structurally-validated",
            "date": "2026-08-09",
            "method": "WolvenKit 8.19.0 deserialize and round-trip inspection",
        },
        f"{display(MANIFEST)}: structural evidence record changed",
    )
    runtime = evidence.get("runtime")
    require(
        isinstance(runtime, dict) and set(runtime) == {"status", "class", "date", "record"},
        f"{display(MANIFEST)}: invalid runtime evidence object",
    )
    runtime_status = runtime.get("status")
    runtime_class = runtime.get("class")
    runtime_date = runtime.get("date")
    require(runtime_status in {"pending", "passed", "failed"}, f"{display(MANIFEST)}: invalid runtime status")
    require(
        runtime_class == ("runtime-proven" if runtime_status == "passed" else "experimental"),
        f"{display(MANIFEST)}: runtime status and evidence class disagree",
    )
    if runtime_status == "pending":
        require(
            runtime_date is None or valid_observed_date(runtime_date),
            f"{display(MANIFEST)}: pending runtime date must be null or YYYY-MM-DD",
        )
    else:
        require(valid_observed_date(runtime_date), f"{display(MANIFEST)}: completed runtime evidence needs a YYYY-MM-DD date")
    runtime_record = normalize_relative(runtime.get("record"), f"{display(MANIFEST)} evidence.runtime.record")
    require(runtime_record == "runtime-acceptance.json", f"{display(MANIFEST)}: wrong runtime acceptance record")

    graph = value.get("graph")
    require(isinstance(graph, dict) and set(graph) == {"layout", "source_fingerprint"}, f"{display(MANIFEST)}: invalid graph object")
    layout = normalize_relative(graph.get("layout"), f"{display(MANIFEST)} graph.layout")
    require(layout == "assets/diagrams/lab-02/cqa002.questphase.layout.json", f"{display(MANIFEST)}: graph layout path changed")
    fingerprint = graph.get("source_fingerprint")
    require(valid_sha256(fingerprint, prefixed=True), f"{display(MANIFEST)}: invalid graph source fingerprint")

    artifacts = value.get("artifacts")
    require(isinstance(artifacts, dict) and set(artifacts) == {"algorithm", "files"}, f"{display(MANIFEST)}: invalid artifacts object")
    require(artifacts.get("algorithm") == "sha256", f"{display(MANIFEST)}: artifact algorithm must be sha256")
    raw_hashes = artifacts.get("files")
    require(isinstance(raw_hashes, dict), f"{display(MANIFEST)}: artifact files must be an object")
    normalized_hashes: dict[str, str] = {}
    for raw_path, digest in raw_hashes.items():
        relative = normalize_relative(raw_path, f"{display(MANIFEST)} artifact path")
        require(relative not in normalized_hashes, f"{display(MANIFEST)}: duplicate artifact path {relative}")
        require(valid_sha256(digest), f"{display(MANIFEST)}: invalid SHA-256 for {relative}")
        normalized_hashes[relative] = digest
    expected_hashed = set(COMPLETED_FILES) - {"README.md", "example.json"}
    require(set(normalized_hashes) == expected_hashed, f"{display(MANIFEST)} artifact inventory: {difference(expected_hashed, set(normalized_hashes))}")
    for relative, expected_digest in normalized_hashes.items():
        path = COMPLETED / relative
        actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual_digest == expected_digest, f"{display(path)}: SHA-256 mismatch; expected {expected_digest}, got {actual_digest}")

    return ManifestInfo(
        depot_paths=depot_paths,
        artifact_hashes=tuple(sorted(normalized_hashes.items())),
        graph_fingerprint=fingerprint,
        runtime_status=runtime_status,
        runtime_class=runtime_class,
        runtime_date=runtime_date,
    )


def validate_candidates(value: Any) -> dict[str, tuple[str | None, ...]]:
    require(isinstance(value, list), f"{display(ACCEPTANCE)}: candidates must be an array")
    expected = (
        ("canonical-mode-2", 2, True),
        ("source-edit-mode-1", 1, False),
    )
    require(
        [item.get("id") if isinstance(item, dict) else None for item in value]
        == [item[0] for item in expected],
        f"{display(ACCEPTANCE)}: exact two-candidate identity/order changed",
    )
    candidates: dict[str, tuple[str | None, ...]] = {}
    expected_installed = [normalize_relative(path, "installed path") for path in EXPECTED_INSTALLED_FILES]
    for candidate, (candidate_id, mode, canonical) in zip(value, expected, strict=True):
        require(
            isinstance(candidate, dict)
            and set(candidate) == {"id", "manifest", "source_state", "installed_files", "depot_paths"},
            f"{display(ACCEPTANCE)}:{candidate_id}: candidate shape changed",
        )
        require(candidate.get("manifest") == "example.json", f"{display(ACCEPTANCE)}:{candidate_id}: wrong manifest reference")
        require(
            candidate.get("source_state") == {
                "questphase_node_id": 11,
                "fact_name": "cqa002_test_mode",
                "set_exact_value": mode,
                "canonical": canonical,
            },
            f"{display(ACCEPTANCE)}:{candidate_id}: immutable source state changed",
        )
        installed = candidate.get("installed_files")
        require(isinstance(installed, list) and len(installed) == 2, f"{display(ACCEPTANCE)}:{candidate_id}: expected two installed files")
        installed_hashes: list[str | None] = []
        installed_paths: list[str] = []
        for index, item in enumerate(installed):
            require(
                isinstance(item, dict) and set(item) == {"path", "sha256"},
                f"{display(ACCEPTANCE)}:{candidate_id}: installed_files[{index}] shape changed",
            )
            installed_paths.append(
                normalize_relative(item.get("path"), f"{display(ACCEPTANCE)}:{candidate_id}: installed_files[{index}].path")
            )
            digest = item.get("sha256")
            require(
                digest is None or valid_sha256(digest),
                f"{display(ACCEPTANCE)}:{candidate_id}: invalid installed-file SHA-256",
            )
            installed_hashes.append(digest)
        require(installed_paths == expected_installed, f"{display(ACCEPTANCE)}:{candidate_id}: installed-file inventory changed")

        depot_paths = candidate.get("depot_paths")
        require(isinstance(depot_paths, list), f"{display(ACCEPTANCE)}:{candidate_id}: depot_paths must be an array")
        normalized_depots = [
            normalize_relative(path, f"{display(ACCEPTANCE)}:{candidate_id}: depot_paths[{index}]")
            for index, path in enumerate(depot_paths)
        ]
        require(normalized_depots == list(DEPOT_PATHS), f"{display(ACCEPTANCE)}:{candidate_id}: depot-path contract changed")
        candidates[candidate_id] = tuple(installed_hashes)
    return candidates


def validate_runs(value: Any) -> dict[str, dict[str, Any]]:
    require(isinstance(value, list), f"{display(ACCEPTANCE)}: runs must be an array")
    require(
        [item.get("id") if isinstance(item, dict) else None for item in value]
        == [item[0] for item in EXPECTED_RUNS],
        f"{display(ACCEPTANCE)}: exact six-run identity/order changed",
    )
    expected_log_paths = [normalize_relative(path, "runtime log path") for path in EXPECTED_LOGS]
    runs: dict[str, dict[str, Any]] = {}
    for run, (run_id, candidate_id, save_state, save_provenance) in zip(value, EXPECTED_RUNS, strict=True):
        require(
            isinstance(run, dict)
            and set(run) == {
                "id", "candidate_id", "save_state", "save_provenance", "performed_at", "tester",
                "observed_environment", "save", "logs",
            },
            f"{display(ACCEPTANCE)}:{run_id}: run shape changed",
        )
        require(
            run.get("candidate_id") == candidate_id
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
            isinstance(environment, dict) and set(environment) == set(REQUIRED_ENVIRONMENT),
            f"{display(ACCEPTANCE)}:{run_id}: observed-environment shape changed",
        )
        for key, observed in environment.items():
            require(
                observed is None or observed == REQUIRED_ENVIRONMENT[key],
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
        expected_created = save_state == "untouched-preinstall"
        require(
            created is None or created is expected_created,
            f"{display(ACCEPTANCE)}:{run_id}: created_before_first_install disagrees with save_state",
        )
        save_digest = save.get("sha256")
        require(save_digest is None or valid_sha256(save_digest), f"{display(ACCEPTANCE)}:{run_id}: invalid save SHA-256")

        logs = run.get("logs")
        require(isinstance(logs, list) and len(logs) == 4, f"{display(ACCEPTANCE)}:{run_id}: expected four logs")
        log_paths: list[str] = []
        for index, item in enumerate(logs):
            require(
                isinstance(item, dict) and set(item) == {"path", "sha256"},
                f"{display(ACCEPTANCE)}:{run_id}: logs[{index}] shape changed",
            )
            log_paths.append(normalize_relative(item.get("path"), f"{display(ACCEPTANCE)}:{run_id}: logs[{index}].path"))
            digest = item.get("sha256")
            require(digest is None or valid_sha256(digest), f"{display(ACCEPTANCE)}:{run_id}: invalid log SHA-256")
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
            evidence_type in {"screenshot", "video", "log", "save-metadata", "notes"},
            f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] has an invalid type",
        )
        reference = normalize_relative(
            item.get("reference"),
            f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}].reference",
        )
        require(reference.startswith("evidence/"), f"{display(ACCEPTANCE)}:{case_id}: evidence must stay below completed/evidence")
        require(reference not in references, f"{display(ACCEPTANCE)}:{case_id}: duplicate evidence reference {reference}")
        references.add(reference)
        digest = item.get("sha256")
        require(valid_sha256(digest), f"{display(ACCEPTANCE)}:{case_id}: evidence[{index}] needs a SHA-256")
        evidence_path = COMPLETED / reference
        require(evidence_path.is_file(), f"{display(evidence_path)}: retained evidence is missing")
        try:
            evidence_path.resolve().relative_to(COMPLETED.resolve())
        except ValueError as error:
            raise ValidationError(f"{display(evidence_path)}: evidence resolves outside the completed checkpoint") from error
        require(not evidence_path.is_symlink(), f"{display(evidence_path)}: retained evidence cannot be a symlink")
        require(
            evidence_path.name.lower() != "sav.dat" and evidence_path.suffix.lower() != ".dat",
            f"{display(evidence_path)}: private save binaries cannot be retained",
        )
        if evidence_type == "save-metadata":
            require(
                evidence_path.suffix.lower() in {".md", ".txt", ".json"},
                f"{display(evidence_path)}: save metadata must be sanitized text",
            )
        require(
            hashlib.sha256(evidence_path.read_bytes()).hexdigest() == digest,
            f"{display(evidence_path)}: retained evidence SHA-256 mismatch",
        )


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
        run.get("observed_environment") == REQUIRED_ENVIRONMENT,
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
    expected_created = run["save_state"] == "untouched-preinstall"
    require(
        save.get("created_before_first_install") is expected_created,
        f"{display(ACCEPTANCE)}:{run_id}: untouched saves must be pre-install and derived saves must not be",
    )
    require(
        all(valid_sha256(item.get("sha256")) for item in run["logs"]),
        f"{display(ACCEPTANCE)}:{run_id}: completed run needs four hash-bound logs",
    )
    return timestamp


def require_related_save_hash(runs: dict[str, dict[str, Any]], source_id: str, reuse_id: str) -> None:
    source_digest = runs[source_id]["save"].get("sha256")
    reuse_digest = runs[reuse_id]["save"].get("sha256")
    require(
        valid_sha256(source_digest) and valid_sha256(reuse_digest) and source_digest == reuse_digest,
        f"{display(ACCEPTANCE)}:{reuse_id}: save hash must match {source_id}",
    )


def validate_runtime_acceptance(info: ManifestInfo) -> None:
    value = load_json(ACCEPTANCE)
    require(
        set(value) == {
            "schema_version", "example_id", "status", "evidence_class", "required_environment",
            "candidates", "runs", "cases", "promotion_rule",
        },
        f"{display(ACCEPTANCE)}: top-level schema changed",
    )
    require(value.get("schema_version") == 3, f"{display(ACCEPTANCE)}: schema_version must be 3")
    require(value.get("example_id") == "cqa002", f"{display(ACCEPTANCE)}: wrong example_id")
    require(value.get("required_environment") == REQUIRED_ENVIRONMENT, f"{display(ACCEPTANCE)}: required environment differs from example.json")
    candidates = validate_candidates(value.get("candidates"))
    runs = validate_runs(value.get("runs"))

    cases = value.get("cases")
    require(isinstance(cases, list), f"{display(ACCEPTANCE)}: cases must be an array")
    require(
        [case.get("id") if isinstance(case, dict) else None for case in cases] == list(EXPECTED_CASES),
        f"{display(ACCEPTANCE)}: immutable acceptance-case identity/order changed",
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
            require(case.get("observed") is None and case.get("evidence") == [], f"{display(ACCEPTANCE)}:{case_id}: pending case cannot claim observations/evidence")
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
    require(value.get("status") == expected_status, f"{display(ACCEPTANCE)}: top-level status disagrees with required cases")
    require(value.get("evidence_class") == expected_class, f"{display(ACCEPTANCE)}: evidence_class disagrees with derived status")
    require(info.runtime_status == expected_status, f"{display(MANIFEST)}: runtime status disagrees with acceptance cases")
    require(info.runtime_class == expected_class, f"{display(MANIFEST)}: runtime evidence class disagrees with acceptance cases")

    completed_timestamps: dict[str, datetime] = {}
    for run_id in sorted(completed_run_ids):
        completed_timestamps[run_id] = validate_completed_run(run_id, runs[run_id], candidates)

    canonical_save = runs["canonical-clean"]["save"]
    edited_save = runs["source-edit-failure"]["save"]
    if canonical_save.get("label") is not None and edited_save.get("label") is not None:
        require(
            canonical_save["label"] != edited_save["label"],
            f"{display(ACCEPTANCE)}: canonical and source-edit clean saves need distinct labels",
        )
    if canonical_save.get("slot_directory") is not None and edited_save.get("slot_directory") is not None:
        require(
            canonical_save["slot_directory"] != edited_save["slot_directory"],
            f"{display(ACCEPTANCE)}: canonical and source-edit clean saves need distinct storage identities",
        )
    # Byte-identical pristine saves are valid; identity, not content, separates them.

    for source_id, reuse_id in (
        ("canonical-clean", "canonical-clean-replay"),
        ("canonical-completed-reload", "canonical-reinstall"),
    ):
        source_digest = runs[source_id]["save"].get("sha256")
        reuse_digest = runs[reuse_id]["save"].get("sha256")
        if source_digest is not None and reuse_digest is not None:
            require(
                source_digest == reuse_digest,
                f"{display(ACCEPTANCE)}:{reuse_id}: populated save hash must match {source_id}",
            )

    if "canonical-clean-replay" in completed_run_ids:
        require_related_save_hash(runs, "canonical-clean", "canonical-clean-replay")
    if "canonical-reinstall" in completed_run_ids:
        require_related_save_hash(runs, "canonical-completed-reload", "canonical-reinstall")

    expected_date = (
        max(timestamp.date().isoformat() for timestamp in completed_timestamps.values())
        if completed_timestamps
        else None
    )
    require(
        info.runtime_date == expected_date,
        f"{display(MANIFEST)}: runtime date must equal the latest completed referenced-run date {expected_date!r}",
    )
    require(value.get("promotion_rule") == PROMOTION_RULE, f"{display(ACCEPTANCE)}: promotion rule changed")


def marker_lines(path: Path) -> list[str]:
    require(path.is_file(), f"{display(path)}: missing reader-facing Lab 2 page")
    return [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("**Lab 2 runtime evidence:**")]


def validate_reader_status(info: ManifestInfo) -> None:
    expected_marker = {
        "pending": "**Lab 2 runtime evidence:** **Experimental** — pending.",
        "failed": "**Lab 2 runtime evidence:** **Experimental** — failed.",
        "passed": "**Lab 2 runtime evidence:** **Runtime-proven** — passed.",
    }[info.runtime_status]
    expected_date = info.runtime_date if info.runtime_date is not None else "Not yet recorded"
    date_row = f"| Runtime test date | {expected_date} |"
    book_pages = sorted(BOOK_GATES.glob("lab-02*.md"))
    expected_book_pages = {
        BOOK_GATES / "lab-02.md",
        BOOK_GATES / "lab-02-authoring.md",
        BOOK_GATES / "lab-02-test.md",
    }
    require(
        set(book_pages) == expected_book_pages,
        f"{display(BOOK_GATES)}: expected exactly lab-02.md, lab-02-authoring.md, and lab-02-test.md",
    )
    for page in book_pages:
        text = page.read_text(encoding="utf-8")
        require(
            marker_lines(page) == [expected_marker],
            f"{display(page)}: Lab 2 runtime evidence marker must be exactly {expected_marker!r}",
        )
        require(date_row in text, f"{display(page)}: runtime test date must be {expected_date!r}")

    status_pages = (
        ROOT / "README.md",
        ROOT / "HANDOFF.md",
        ROOT / "ROADMAP.md",
        ROOT / "book" / "src" / "introduction.md",
        BOOK_GATES / "index.md",
        LAB / "README.md",
        START / "README.md",
        COMPLETED / "README.md",
    )
    for page in status_pages:
        require(
            marker_lines(page) == [expected_marker],
            f"{display(page)}: missing, stale, or duplicate Lab 2 runtime evidence marker",
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
    result = value.get("HandleId") or value.get("HandleRefId")
    require(isinstance(result, str), "CR2W handle has no string ID")
    return result


def resolve(value: Any, handles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    identifier = handle_id(value)
    require(identifier in handles, f"unresolved CR2W handle {identifier}")
    return handles[identifier]


def validate_journal_and_localization() -> None:
    for relative in (
        "source/raw/mod/cqa/cqa002/journal/cqa002.journal.json",
        "source/raw/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json.json",
    ):
        require((START / relative).read_bytes() == (COMPLETED / relative).read_bytes(), f"Lab 2 checkpoints disagree on shared {relative}")

    journal_path = COMPLETED / "source/raw/mod/cqa/cqa002/journal/cqa002.journal.json"
    localization_path = COMPLETED / "source/raw/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json.json"
    journal = load_json(journal_path)
    localization = load_json(localization_path)

    handles: dict[str, dict[str, Any]] = {}
    collect_handles(journal, handles)
    root = journal.get("Data", {}).get("RootChunk", {})
    require(root.get("$type") == "gameJournalResource", f"{display(journal_path)}: wrong root type")
    root_entry = resolve(root.get("entry"), handles)
    require(root_entry.get("$type") == "gameJournalRootFolderEntry", f"{display(journal_path)}: missing journal root folder")
    require(
        root_entry.get("descriptor") == {
            "DepotPath": {"$type": "ResourcePath", "$storage": "string", "$value": "base\\journal\\descriptor.journaldesc"},
            "Flags": "Soft",
        },
        f"{display(journal_path)}: journal descriptor changed",
    )

    entries: dict[str, dict[str, Any]] = {}

    def visit(entry: dict[str, Any], parents: tuple[str, ...]) -> None:
        entry_id = entry.get("id")
        parts = parents
        if entry_id is not None:
            require(isinstance(entry_id, str) and entry_id, f"{display(journal_path)}: invalid journal entry id")
            parts = (*parents, entry_id)
            real_path = "/".join(parts)
            require(real_path not in entries, f"{display(journal_path)}: duplicate journal path {real_path}")
            entries[real_path] = entry
        children = entry.get("entries", [])
        require(isinstance(children, list), f"{display(journal_path)}: journal entries must be an array")
        for child in children:
            visit(resolve(child, handles), parts)

    visit(root_entry, ())
    expected_types = {
        "quests": "gameJournalPrimaryFolderEntry",
        "quests/minor_quest": "gameJournalFolderEntry",
        "quests/minor_quest/cqa002": "gameJournalQuest",
        "quests/minor_quest/cqa002/cqa002_01": "gameJournalQuestPhase",
        "quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_wait": "gameJournalQuestObjective",
        "quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_stable": "gameJournalQuestObjective",
    }
    require({path: entry.get("$type") for path, entry in entries.items()} == expected_types, f"{display(journal_path)}: exact journal tree changed")
    quest = entries["quests/minor_quest/cqa002"]
    required = entries["quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_wait"]
    optional = entries["quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_stable"]
    require(quest.get("title") == {"unk1": "0", "value": "cqa_cqa002_title"}, f"{display(journal_path)}: quest title localization key changed")
    require(required.get("description") == {"unk1": "0", "value": "cqa_cqa002_objective_wait"} and required.get("optional") == 0, f"{display(journal_path)}: required objective contract changed")
    require(optional.get("description") == {"unk1": "0", "value": "cqa_cqa002_objective_stable"} and optional.get("optional") == 1, f"{display(journal_path)}: optional objective/key contract changed")

    localization_root = localization.get("Data", {}).get("RootChunk", {})
    localization_handles: dict[str, dict[str, Any]] = {}
    collect_handles(localization, localization_handles)
    onscreens = resolve(localization_root.get("root"), localization_handles)
    require(onscreens.get("$type") == "localizationPersistenceOnScreenEntries", f"{display(localization_path)}: wrong onscreen root")
    expected_text = {
        "cqa_cqa002_title": "Signal Race",
        "cqa_cqa002_objective_wait": "Wait for the signal test to resolve.",
        "cqa_cqa002_objective_stable": "Keep the signal stable.",
    }
    localized: dict[str, str] = {}
    raw_entries = onscreens.get("entries")
    require(isinstance(raw_entries, list) and len(raw_entries) == 3, f"{display(localization_path)}: expected three onscreen entries")
    for index, entry in enumerate(raw_entries):
        require(
            isinstance(entry, dict)
            and set(entry) == {"$type", "femaleVariant", "maleVariant", "primaryKey", "secondaryKey"}
            and entry.get("$type") == "localizationPersistenceOnScreenEntry"
            and str(entry.get("primaryKey")) == "0"
            and entry.get("maleVariant") == "",
            f"{display(localization_path)}: invalid onscreen entry {index}",
        )
        key = entry.get("secondaryKey")
        value = entry.get("femaleVariant")
        require(isinstance(key, str) and key not in localized and isinstance(value, str), f"{display(localization_path)}: invalid or duplicate key at entry {index}")
        localized[key] = value
    require(localized == expected_text, f"{display(localization_path)}: exact localization lookup contract changed")


def expected_archive_xl_lines() -> list[str]:
    return [
        "quest:",
        "  phases:",
        "  - path: mod\\cqa\\cqa002\\phases\\cqa002.questphase",
        "    parent: base\\quest\\cyberpunk2077.quest",
        "",
        "journal:",
        "- mod\\cqa\\cqa002\\journal\\cqa002.journal",
        "",
        "localization:",
        "  onscreens:",
        "    en-us:",
        "    - mod\\cqa\\cqa002\\localization\\en-us\\onscreens\\cqa002.json",
    ]


def validate_project_and_resources() -> None:
    project_contract = (
        (START / "CQA_Lab02_SignalRace_Start.cpmodproj", "CQA Lab 02 Signal Race Start", "CQA_Lab02_SignalRace_Start"),
        (COMPLETED / "CQA_Lab02_SignalRace.cpmodproj", "CQA Lab 02 Signal Race", "CQA_Lab02_SignalRace"),
    )
    for project_path, expected_name, expected_mod_name in project_contract:
        try:
            root = ET.parse(project_path).getroot()
        except ET.ParseError as error:
            raise ValidationError(f"{display(project_path)}: invalid XML: {error}") from error
        require(root.tag == "CP77Mod", f"{display(project_path)}: wrong project root")
        require(root.findtext("Name") == expected_name and root.findtext("ModName") == expected_mod_name, f"{display(project_path)}: project identity changed")
        require(root.findtext("Version") == "0.1.0", f"{display(project_path)}: unexpected project version")

    for archive_xl in (
        START / "source/resources/CQA_Lab02_SignalRace_Start.archive.xl",
        COMPLETED / "source/resources/CQA_Lab02_SignalRace.archive.xl",
    ):
        lines = archive_xl.read_text(encoding="utf-8").splitlines()
        while lines and not lines[-1]:
            lines.pop()
        require(lines == expected_archive_xl_lines(), f"{display(archive_xl)}: exact ArchiveXL registration changed")

    pair_count = 0
    for checkpoint in (START, COMPLETED):
        for depot_path in DEPOT_PATHS:
            pair_count += 1
            cooked = checkpoint / "source" / "archive" / depot_path
            raw = checkpoint / "source" / "raw" / f"{depot_path}.json"
            source = load_json(raw)
            header = source.get("Header")
            data = source.get("Data")
            require(isinstance(header, dict) and isinstance(data, dict), f"{display(raw)}: missing Header/Data")
            require(
                header.get("WolvenKitVersion") == "8.19.0"
                and header.get("WKitJsonVersion") == "0.0.9"
                and header.get("GameVersion") == 2310
                and header.get("DataType") == "CR2W",
                f"{display(raw)}: CR2W review-source baseline changed",
            )
            archive_name = normalize_relative(header.get("ArchiveFileName"), f"{display(raw)} Header.ArchiveFileName")
            require(archive_name == depot_path, f"{display(raw)}: Header.ArchiveFileName does not match its depot path")
            suffix = next((candidate for candidate in EXPECTED_ROOT_TYPES if depot_path.endswith(candidate)), None)
            require(suffix is not None, f"{depot_path}: no expected root type")
            root_type = data.get("RootChunk", {}).get("$type")
            require(root_type == EXPECTED_ROOT_TYPES[suffix], f"{display(raw)}: wrong root type {root_type!r}")
            payload = cooked.read_bytes()
            require(payload.startswith(b"CR2W"), f"{display(cooked)}: missing CR2W magic")
            require(root_type.encode("ascii") in payload, f"{display(cooked)}: cooked string table does not contain {root_type}")
    require(pair_count == 6, "Lab 2 must contain exactly six CR2W source/cooked pairs")

    for depot_path in DEPOT_PATHS[1:]:
        start_cooked = START / "source" / "archive" / depot_path
        completed_cooked = COMPLETED / "source" / "archive" / depot_path
        require(start_cooked.read_bytes() == completed_cooked.read_bytes(), f"Lab 2 checkpoints disagree on shared cooked {depot_path}")


def cname(value: str) -> dict[str, str]:
    return {"$type": "CName", "$storage": "string", "$value": value}


def quest_source(checkpoint: Path) -> Path:
    return checkpoint / "source/raw/mod/cqa/cqa002/phases/cqa002.questphase.json"


def graph_nodes(source: dict[str, Any]) -> tuple[dict[int, dict[str, Any]], dict[str, dict[str, Any]]]:
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(source, handles)
    root = source.get("Data", {}).get("RootChunk", {})
    require(
        set(root) == {"$type", "cookingPlatform", "graph", "inplacePhases", "phasePrefabs"}
        and root.get("$type") == "questQuestPhaseResource"
        and root.get("cookingPlatform") == "PLATFORM_PC"
        and root.get("inplacePhases") == []
        and root.get("phasePrefabs") == [],
        "Lab 2 questphase root resource contract changed",
    )
    graph = resolve(root.get("graph"), handles)
    require(set(graph) == {"$type", "nodes"} and graph.get("$type") == "questGraphDefinition", "Lab 2 quest graph wrapper changed")
    wrappers = graph.get("nodes")
    require(isinstance(wrappers, list), "Lab 2 quest graph has no node array")
    nodes: dict[int, dict[str, Any]] = {}
    for wrapper in wrappers:
        node = resolve(wrapper, handles)
        node_id = node.get("id")
        require(isinstance(node_id, int) and node_id not in nodes, "Lab 2 quest graph has an invalid or duplicate node ID")
        nodes[node_id] = node
    return nodes, handles


def expected_sockets(node_id: int) -> list[tuple[str, str]]:
    red_type = EXPECTED_NODE_TYPES[node_id]
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
    if red_type == "questLogicalXorNodeDefinition":
        return [("CutDestination", "CutDestination"), ("In1", "Input"), ("In2", "Input"), ("Out1", "Output")]
    return [("CutDestination", "CutDestination"), ("In", "Input"), ("Out", "Output")]


def validate_node_shell(node_id: int, node: dict[str, Any], handles: dict[str, dict[str, Any]]) -> None:
    expected_type = EXPECTED_NODE_TYPES[node_id]
    require(node.get("$type") == expected_type, f"Lab 2 node {node_id}: expected {expected_type}, got {node.get('$type')!r}")
    sockets = node.get("sockets")
    require(isinstance(sockets, list), f"Lab 2 node {node_id}: sockets must be an array")
    resolved_sockets: list[tuple[str, str]] = []
    for socket_wrapper in sockets:
        socket = resolve(socket_wrapper, handles)
        require(set(socket) == {"$type", "connections", "name", "type"} and socket.get("$type") == "questSocketDefinition", f"Lab 2 node {node_id}: socket payload changed")
        name = socket.get("name")
        require(isinstance(name, dict) and name.get("$type") == "CName" and isinstance(name.get("$value"), str), f"Lab 2 node {node_id}: socket has an invalid CName")
        resolved_sockets.append((name["$value"], socket.get("type")))
    require(resolved_sockets == expected_sockets(node_id), f"Lab 2 node {node_id}: exact socket inventory changed: {resolved_sockets!r}")


def require_fact_condition(value: Any, handles: dict[str, dict[str, Any]], expected: tuple[str, str, int], context: str) -> None:
    condition = resolve(value, handles)
    require(set(condition) == {"$type", "type"} and condition.get("$type") == "questFactsDBCondition", f"{context}: expected questFactsDBCondition")
    comparison = resolve(condition.get("type"), handles)
    require(
        comparison == {
            "$type": "questVarComparison_ConditionType",
            "comparisonType": expected[1],
            "factName": expected[0],
            "value": expected[2],
        },
        f"{context}: fact comparison payload changed",
    )


def validate_graph_payloads(nodes: dict[int, dict[str, Any]], handles: dict[str, dict[str, Any]]) -> None:
    for node_id, node in nodes.items():
        validate_node_shell(node_id, node, handles)

    require(set(nodes[0]) == {"$type", "id", "sockets", "socketName"} and nodes[0].get("socketName") == cname("In1"), "Lab 2 node 0 input-interface payload changed")
    require(set(nodes[1]) == {"$type", "id", "sockets", "socketName", "type"} and nodes[1].get("socketName") == cname("Out1") and nodes[1].get("type") == "Terminating", "Lab 2 node 1 terminating-output payload changed")

    for node_id, expected in {
        10: ("cqa002_completed", "Equal", 0),
        15: ("cqa002_signal_failed", "Greater", 0),
        17: ("cqa002_test_mode", "Equal", 1),
    }.items():
        require(set(nodes[node_id]) == {"$type", "id", "sockets", "condition"}, f"Lab 2 node {node_id}: unexpected properties")
        require_fact_condition(nodes[node_id].get("condition"), handles, expected, f"Lab 2 node {node_id}")

    logical_node = nodes[16]
    require(set(logical_node) == {"$type", "id", "sockets", "condition"}, "Lab 2 node 16: unexpected properties")
    logical = resolve(logical_node.get("condition"), handles)
    require(set(logical) == {"$type", "conditions", "operation"} and logical.get("$type") == "questLogicalCondition" and logical.get("operation") == "AND", "Lab 2 node 16: logical AND payload changed")
    children = logical.get("conditions")
    require(isinstance(children, list) and len(children) == 2, "Lab 2 node 16: expected exactly two AND children")
    require_fact_condition(children[0], handles, ("cqa002_signal_stop", "Greater", 0), "Lab 2 node 16 child 0")
    require_fact_condition(children[1], handles, ("cqa002_test_mode", "Equal", 2), "Lab 2 node 16 child 1")

    for node_id, seconds in ((18, 30), (20, 120)):
        require(set(nodes[node_id]) == {"$type", "id", "sockets", "condition"}, f"Lab 2 node {node_id}: unexpected properties")
        condition = resolve(nodes[node_id].get("condition"), handles)
        require(set(condition) == {"$type", "type"} and condition.get("$type") == "questTimeCondition", f"Lab 2 node {node_id}: expected questTimeCondition")
        delay = resolve(condition.get("type"), handles)
        require(
            delay == {
                "$type": "questRealtimeDelay_ConditionType",
                "hours": 0,
                "miliseconds": 0,
                "minutes": 0,
                "seconds": seconds,
            },
            f"Lab 2 node {node_id}: realtime delay payload changed",
        )

    for node_id, fact_name, value in (
        (11, "cqa002_test_mode", 2),
        (19, "cqa002_signal_failed", 1),
        (21, "cqa002_signal_stop", 1),
        (24, "cqa002_signal_succeeded", 1),
        (27, "cqa002_completed", 1),
    ):
        require(set(nodes[node_id]) == {"$type", "id", "sockets", "type"}, f"Lab 2 node {node_id}: unexpected properties")
        node_type = resolve(nodes[node_id].get("type"), handles)
        require(
            node_type == {
                "$type": "questSetVar_NodeType",
                "factName": fact_name,
                "setExactValue": 1,
                "value": value,
            },
            f"Lab 2 node {node_id}: exact fact-writer payload changed",
        )

    quest_path = "quests/minor_quest/cqa002"
    required_path = "quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_wait"
    optional_path = "quests/minor_quest/cqa002/cqa002_01/cqa002_01_obj_stable"
    journal_paths = {
        12: (quest_path, "gameJournalQuest"),
        13: (required_path, "gameJournalQuestObjective"),
        14: (optional_path, "gameJournalQuestObjective"),
        22: (optional_path, "gameJournalQuestObjective"),
        23: (optional_path, "gameJournalQuestObjective"),
        26: (required_path, "gameJournalQuestObjective"),
        28: (quest_path, "gameJournalQuest"),
    }
    for node_id, (real_path, class_name) in journal_paths.items():
        require(set(nodes[node_id]) == {"$type", "id", "sockets", "type"}, f"Lab 2 node {node_id}: unexpected properties")
        node_type = resolve(nodes[node_id].get("type"), handles)
        require(
            set(node_type) == {"$type", "optional", "path", "sendNotification", "trackQuest", "version"}
            and node_type.get("$type") == "questJournalQuestEntry_NodeType"
            and node_type.get("optional") == 0
            and node_type.get("sendNotification") == 1
            and node_type.get("trackQuest") == 1
            and node_type.get("version") == "Initial",
            f"Lab 2 node {node_id}: journal-node presentation contract changed",
        )
        path = resolve(node_type.get("path"), handles)
        require(
            path == {
                "$type": "gameJournalPath",
                "className": cname(class_name),
                "editorPath": "",
                "fileEntryIndex": 2,
                "realPath": real_path,
            },
            f"Lab 2 node {node_id}: journal path/class payload changed",
        )

    require(
        set(nodes[25]) == {"$type", "id", "sockets", "inputSocketCount", "outputSocketCount"}
        and nodes[25].get("inputSocketCount") == 2
        and nodes[25].get("outputSocketCount") == 1,
        "Lab 2 node 25: XOR socket-count payload changed",
    )


def renderer_graph(path: Path) -> tuple[ModuleType, list[Any], list[Any]]:
    module_name = f"_cqa_render_lab02_{path.parent.name}"
    module = load_module(RENDER_SCRIPT, module_name)
    try:
        nodes, edges = module.parse_graph(load_json(path))
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module, nodes, edges


def validate_graph_semantics() -> None:
    start_source = load_json(quest_source(START))
    start_nodes, start_handles = graph_nodes(start_source)
    require(set(start_nodes) == {0, 1}, f"{display(quest_source(START))}: start graph must contain IDs 0 and 1 only")
    for node_id in (0, 1):
        validate_node_shell(node_id, start_nodes[node_id], start_handles)
    require(set(start_nodes[0]) == {"$type", "id", "sockets", "socketName"} and start_nodes[0].get("socketName") == cname("In1"), "Lab 2 start input payload changed")
    require(set(start_nodes[1]) == {"$type", "id", "sockets", "socketName", "type"} and start_nodes[1].get("socketName") == cname("Out1") and start_nodes[1].get("type") == "Terminating", "Lab 2 start output payload changed")

    start_module, rendered_start_nodes, rendered_start_edges = renderer_graph(quest_source(START))
    try:
        require(len(rendered_start_nodes) == 2, "Lab 2 start graph must have exactly 2 nodes")
        start_edges = [(edge.source, edge.source_socket, edge.destination, edge.destination_socket) for edge in rendered_start_edges]
        require(start_edges == [(0, "Out", 1, "In")], "Lab 2 start graph must have exactly edge 0.Out -> 1.In")
    finally:
        sys.modules.pop(start_module.__name__, None)

    completed_source = load_json(quest_source(COMPLETED))
    nodes, handles = graph_nodes(completed_source)
    require(set(nodes) == set(EXPECTED_NODE_TYPES), f"{display(quest_source(COMPLETED))}: exact 21-node ID inventory changed")
    validate_graph_payloads(nodes, handles)

    module, rendered_nodes, rendered_edges = renderer_graph(quest_source(COMPLETED))
    try:
        require(len(rendered_nodes) == 21, "Lab 2 completed graph must have exactly 21 nodes")
        edges = [(edge.source, edge.source_socket, edge.destination, edge.destination_socket) for edge in rendered_edges]
        require(len(edges) == 22 and len(set(edges)) == 22, "Lab 2 completed graph must have exactly 22 unique resolved edges")
        require(set(edges) == set(EXPECTED_EDGES), f"Lab 2 completed graph exact edge contract changed")
        connection_count = sum(1 for item in handles.values() if item.get("$type") == "graphGraphConnectionDefinition")
        require(connection_count == 22, "Lab 2 completed source must define exactly 22 graph connections")
    finally:
        sys.modules.pop(module.__name__, None)


def validate_graph_artifacts(info: ManifestInfo) -> None:
    missing = [display(path) for path in (LAYOUT, SVG) if not path.is_file()]
    require(not missing, "missing Lab 2 graph artifact(s): " + ", ".join(missing))
    source_relative = Path(
        "examples/lab-02-signal-race/completed/source/raw/mod/cqa/cqa002/phases/cqa002.questphase.json"
    )
    source = load_json(ROOT / source_relative)
    layout = load_json(LAYOUT)
    module = load_module(RENDER_SCRIPT, "_cqa_render_lab02_exact")
    try:
        nodes, edges = module.parse_graph(source)
        module.validate_layout(nodes, layout)
        fingerprint = module.fingerprint(nodes, edges)
        require(layout.get("source_fingerprint") == fingerprint, f"{display(LAYOUT)}: source fingerprint mismatch; actual {fingerprint}")
        require(info.graph_fingerprint == fingerprint, f"{display(MANIFEST)}: graph fingerprint does not match the completed source")
        expected_svg = module.render_svg(source_relative, nodes, edges, layout, fingerprint).encode("utf-8")
    finally:
        sys.modules.pop(module.__name__, None)
    require(SVG.read_bytes() == expected_svg, f"{display(SVG)}: generated exact SVG is stale")


def run_check(name: str, check: Callable[[], None]) -> bool:
    try:
        check()
    except Exception as error:
        print(f"[FAIL] {name}: {error}", file=sys.stderr)
        return False
    print(f"[ OK ] {name}")
    return True


def main() -> int:
    try:
        info = validate_manifest()
    except Exception as error:
        print(f"[FAIL] Lab 2 manifest and hashes: {error}", file=sys.stderr)
        return 1
    print("[ OK ] Lab 2 manifest and hashes")

    checks: tuple[tuple[str, Callable[[], None]], ...] = (
        ("Lab 2 exact inventories, Git tracking, and LF text", validate_inventories),
        ("Lab 2 generator byte determinism", validate_generated_raw),
        ("Lab 2 runtime-acceptance v3 promotion contract", lambda: validate_runtime_acceptance(info)),
        ("Lab 2 reader-facing evidence state", lambda: validate_reader_status(info)),
        ("Lab 2 journal and localization contract", validate_journal_and_localization),
        ("Lab 2 projects, ArchiveXL, and six CR2W pairs", validate_project_and_resources),
        ("Lab 2 exact start/completed graph semantics", validate_graph_semantics),
        ("Lab 2 graph fingerprint and exact SVG", lambda: validate_graph_artifacts(info)),
    )
    results = [run_check(name, check) for name, check in checks]
    passed = all(results)
    if passed:
        print("Lab 2 validation passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
