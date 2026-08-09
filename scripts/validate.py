#!/usr/bin/env python3
"""Validate generated documentation artifacts and tutorial example projects.

The validator deliberately uses only the Python standard library. It parses
JSON only from the checked manifest, layout, and expected CR2W-JSON paths; a
cooked resource named ``*.json`` is treated as binary, never as JSON.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from types import ModuleType
from collections.abc import Iterator
from typing import Any, Callable
from urllib.parse import unquote
from zipfile import ZIP_DEFLATED, ZipFile


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
BOOK_SRC = ROOT / "book" / "src"
SUMMARY = BOOK_SRC / "SUMMARY.md"
LAB = ROOT / "examples" / "lab-01-one-shot"
COMPLETED = LAB / "completed"
SOURCE_ROOT = COMPLETED / "source"
ARCHIVE_ROOT = SOURCE_ROOT / "archive"
RAW_ROOT = SOURCE_ROOT / "raw"
ARCHIVE_XL = SOURCE_ROOT / "resources" / "CQA_Lab01_OneShot.archive.xl"
MANIFEST = COMPLETED / "example.json"
ACCEPTANCE = COMPLETED / "runtime-acceptance.json"
LAYOUT = ROOT / "assets" / "diagrams" / "lab-01" / "cqa001.questphase.layout.json"
SVG = ROOT / "book" / "src" / "images" / "lab-01" / "cqa001.questphase.svg"
LAB_STATUS_PAGES = (
    ROOT / "README.md",
    ROOT / "HANDOFF.md",
    ROOT / "ROADMAP.md",
    ROOT / "examples" / "lab-01-one-shot" / "README.md",
    ROOT / "examples" / "lab-01-one-shot" / "completed" / "README.md",
    ROOT / "book" / "src" / "introduction.md",
    ROOT / "book" / "src" / "start-here" / "index.md",
    ROOT / "book" / "src" / "start-here" / "lab-01.md",
    ROOT / "book" / "src" / "start-here" / "lab-01-authoring.md",
    ROOT / "book" / "src" / "start-here" / "install-and-test.md",
    ROOT / "book" / "src" / "questphases" / "index.md",
    ROOT / "book" / "src" / "journal" / "index.md",
    ROOT / "book" / "src" / "journal" / "trees-and-paths.md",
    ROOT / "book" / "src" / "journal" / "quest-state.md",
    ROOT / "book" / "src" / "journal" / "localization-paths.md",
    ROOT / "book" / "src" / "journal" / "rewards-and-completion.md",
)
LAB_PRACTICAL_PAGES = (
    ROOT / "book" / "src" / "start-here" / "lab-01.md",
    ROOT / "book" / "src" / "start-here" / "lab-01-authoring.md",
    ROOT / "book" / "src" / "start-here" / "install-and-test.md",
)
QUEST_SOURCE_RELPATH = Path(
    "examples/lab-01-one-shot/completed/source/raw/"
    "mod/cqa/cqa001/phases/cqa001.questphase.json"
)
QUEST_RAW = ROOT / QUEST_SOURCE_RELPATH
JOURNAL_RAW = (
    COMPLETED
    / "source"
    / "raw"
    / "mod"
    / "cqa"
    / "cqa001"
    / "journal"
    / "cqa001.journal.json"
)
LOCALIZATION_RAW = (
    COMPLETED
    / "source"
    / "raw"
    / "mod"
    / "cqa"
    / "cqa001"
    / "localization"
    / "en-us"
    / "onscreens"
    / "cqa001.json.json"
)
BUILD_SCRIPT = ROOT / "scripts" / "build_lab01_sources.py"
RENDER_SCRIPT = ROOT / "scripts" / "render_quest_graph.py"
PACKAGE_SCRIPT = ROOT / "scripts" / "package_examples.py"
LAB02_VALIDATOR = ROOT / "scripts" / "validate_lab02.py"
LAB03_VALIDATOR = ROOT / "scripts" / "validate_lab03.py"
SHARED_LICENSE = LAB / "LICENSE.md"
JSON_SIZE_LIMIT = 16 * 1024 * 1024
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)
ZIP_CREATE_SYSTEM = 3
ZIP_VERSION = 20
ZIP_MODE = 0o100644

EXPECTED_DEPOT_PATHS = frozenset(
    {
        "mod/cqa/cqa001/journal/cqa001.journal",
        "mod/cqa/cqa001/localization/en-us/onscreens/cqa001.json",
        "mod/cqa/cqa001/phases/cqa001.questphase",
    }
)
EXPECTED_ACCEPTANCE_CASES = {
    "clean-save-activation": {
        "precondition": "Load a save created before cqa001 was ever installed.",
        "expected": "First Signal and Wait for the signal. activate once without a manual trigger.",
    },
    "realtime-delay": {
        "precondition": "Measure wall-clock time from objective activation without pausing the game.",
        "expected": "The objective does not succeed before ten real-time seconds and then advances once.",
    },
    "journal-completion": {
        "precondition": "Let the first-run path finish without interruption.",
        "expected": "The objective and quest both show succeeded state, and no localization key is blank.",
    },
    "mid-flow-reload": {
        "precondition": "Save while the delay is active, reload that save, and record whether elapsed time resumes or restarts.",
        "expected": "Reloading neither duplicates journal activation nor blocks completion; timer behavior is recorded explicitly.",
    },
    "completed-save-reload": {
        "precondition": "Save after completion and reload without changing the installation.",
        "expected": "The cqa001_completed guard takes the false route and the quest does not reactivate.",
    },
    "completed-save-reinstall": {
        "precondition": "Remove and reinstall the identical candidate, then load the completed save.",
        "expected": "The quest remains completed and does not create a second activation.",
    },
    "clean-replay": {
        "precondition": "Reload the original untouched pre-install save with the identical candidate still installed.",
        "expected": "The first-run route activates and completes once with the same player-facing result.",
    },
    "registration-and-lookup-logs": {
        "precondition": "Retain fresh RED4ext and ArchiveXL logs from the clean-save run.",
        "expected": "The logs contain no cqa001 registration, depot-path, journal, or localization lookup error.",
    },
}
EXPECTED_INSTALLED_FILES = frozenset(
    {
        "archive/pc/mod/CQA_Lab01_OneShot.archive",
        "archive/pc/mod/CQA_Lab01_OneShot.archive.xl",
    }
)
EXPECTED_RUNTIME_LOGS = frozenset(
    {
        "red4ext/plugins/ArchiveXL/ArchiveXL.log",
        "red4ext/logs/red4ext.log",
        "red4ext/logs/game.log",
        "r6/logs/redscript_rCURRENT.log",
    }
)
EXPECTED_PROMOTION_RULE = (
    "Set status to passed and evidence_class to runtime-proven only when every required case passes and the run "
    "binds both installed payloads, the pre-install save, exact versions, and all four retained logs to hashes."
)
START_FILES = frozenset(
    {
        "CQA_Lab01_OneShot_Start.cpmodproj",
        "README.md",
    }
)
START_TEXT_FILES = START_FILES
COMPLETED_FILES = frozenset(
    {
        "CQA_Lab01_OneShot.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        "source/archive/mod/cqa/cqa001/journal/cqa001.journal",
        "source/archive/mod/cqa/cqa001/localization/en-us/onscreens/cqa001.json",
        "source/archive/mod/cqa/cqa001/phases/cqa001.questphase",
        "source/raw/mod/cqa/cqa001/journal/cqa001.journal.json",
        "source/raw/mod/cqa/cqa001/localization/en-us/onscreens/cqa001.json.json",
        "source/raw/mod/cqa/cqa001/phases/cqa001.questphase.json",
        "source/resources/CQA_Lab01_OneShot.archive.xl",
    }
)
COMPLETED_TEXT_FILES = frozenset(
    {
        "CQA_Lab01_OneShot.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        "source/raw/mod/cqa/cqa001/journal/cqa001.journal.json",
        "source/raw/mod/cqa/cqa001/localization/en-us/onscreens/cqa001.json.json",
        "source/raw/mod/cqa/cqa001/phases/cqa001.questphase.json",
        "source/resources/CQA_Lab01_OneShot.archive.xl",
    }
)
CHECKPOINTS = {
    "cqa-lab-01-start.zip": (
        LAB / "start",
        "CQA_Lab01_OneShot_Start",
        START_FILES,
        START_TEXT_FILES,
    ),
    "cqa-lab-01-completed.zip": (
        COMPLETED,
        "CQA_Lab01_OneShot",
        COMPLETED_FILES,
        COMPLETED_TEXT_FILES,
    ),
}
GENERATED_DOWNLOAD_NAMES = frozenset(
    {
        "cqa-lab-01-start.zip",
        "cqa-lab-01-completed.zip",
        "cqa-lab-02-start.zip",
        "cqa-lab-02-completed.zip",
        "cqa-lab-03-start.zip",
        "cqa-lab-03-completed.zip",
    }
)

EXPECTED_ROOT_TYPES = {
    ".journal": "gameJournalResource",
    ".questphase": "questQuestPhaseResource",
    ".json": "JsonResource",
}
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_FENCE_PATTERN = re.compile(r"^\s*(`{3,}|~{3,})")
MARKDOWN_HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")


class ValidationError(RuntimeError):
    """A repository invariant was not satisfied."""


@dataclass(frozen=True)
class ManifestInfo:
    depot_paths: tuple[str, ...]
    baseline: tuple[tuple[str, str], ...]
    artifact_hashes: tuple[tuple[str, str], ...]
    acceptance_record: str
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


def normalize_relative(value: Any, label: str) -> str:
    require(isinstance(value, str) and value != "", f"{label}: expected a path string")
    normalized = value.replace("\\", "/")
    parts = normalized.split("/")
    require(
        not normalized.startswith("/")
        and not normalized.endswith("/")
        and ":" not in parts[0]
        and all(part not in ("", ".", "..") for part in parts),
        f"{label}: unsafe or non-normal relative path {value!r}",
    )
    return PurePosixPath(*parts).as_posix()


def depot_file(root: Path, depot_path: str) -> Path:
    return root.joinpath(*PurePosixPath(depot_path).parts)


def raw_depot_file(depot_path: str) -> Path:
    parts = list(PurePosixPath(depot_path).parts)
    parts[-1] += ".json"
    return RAW_ROOT.joinpath(*parts)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def json_path_is_allowed(path: Path) -> bool:
    resolved = path.resolve(strict=False)
    if resolved in {
        MANIFEST.resolve(strict=False),
        ACCEPTANCE.resolve(strict=False),
        LAYOUT.resolve(strict=False),
    }:
        return True
    try:
        resolved.relative_to(RAW_ROOT.resolve(strict=False))
        return True
    except ValueError:
        return False


def load_json(path: Path) -> dict[str, Any]:
    require(json_path_is_allowed(path), f"{display(path)}: JSON path is outside the allowlist")
    require(path.is_file(), f"{display(path)}: missing JSON file")
    resolved = path.resolve(strict=True)
    require(json_path_is_allowed(resolved), f"{display(path)}: JSON symlink escapes its allowed root")
    payload = resolved.read_bytes()
    require(
        len(payload) <= JSON_SIZE_LIMIT,
        f"{display(path)}: JSON exceeds the {JSON_SIZE_LIMIT}-byte safety limit",
    )
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"{display(path)}: invalid UTF-8 JSON: {error}") from error
    require(isinstance(value, dict), f"{display(path)}: expected a JSON object")
    return value


def validate_manifest() -> ManifestInfo:
    value = load_json(MANIFEST)
    require(value.get("schema_version") == 2, f"{display(MANIFEST)}: unsupported schema_version")
    require(value.get("id") == "cqa001", f"{display(MANIFEST)}: unexpected example id")
    require(value.get("title") == "First Signal", f"{display(MANIFEST)}: unexpected example title")
    require(
        value.get("persistent_facts") == ["cqa001_completed"],
        f"{display(MANIFEST)}: persistent fact inventory mismatch",
    )

    raw_paths = value.get("depot_paths")
    require(isinstance(raw_paths, list) and raw_paths, f"{display(MANIFEST)}: depot_paths must be a non-empty list")
    depot_paths = tuple(
        normalize_relative(path, f"{display(MANIFEST)} depot_paths[{index}]")
        for index, path in enumerate(raw_paths)
    )
    require(len(depot_paths) == len(set(depot_paths)), f"{display(MANIFEST)}: duplicate depot path")
    require(
        set(depot_paths) == EXPECTED_DEPOT_PATHS,
        f"{display(MANIFEST)}: Lab 1 depot inventory mismatch: "
        + describe_set_difference(set(EXPECTED_DEPOT_PATHS), set(depot_paths)),
    )

    chapter = normalize_relative(value.get("book_chapter"), f"{display(MANIFEST)} book_chapter")
    require((ROOT / chapter).is_file(), f"{display(MANIFEST)}: missing book_chapter {chapter}")

    baseline = value.get("baseline")
    expected_baseline = {
        "recorded": "2026-08-09",
        "cyberpunk_2077": "2.31a",
        "wolvenkit": "8.19.0",
        "archive_xl": "1.27.0",
        "red4ext": "1.30.0",
        "redscript": "0.5.31",
    }
    require(baseline == expected_baseline, f"{display(MANIFEST)}: pinned baseline mismatch")

    evidence = value.get("evidence")
    require(isinstance(evidence, dict), f"{display(MANIFEST)}: missing evidence object")
    structure = evidence.get("structure")
    runtime = evidence.get("runtime")
    expected_structure = {
        "status": "structurally-validated",
        "date": "2026-07-27",
        "method": "WolvenKit 8.19.0 deserialize and round-trip inspection",
    }
    require(structure == expected_structure, f"{display(MANIFEST)}: invalid structural evidence record")
    require(isinstance(runtime, dict), f"{display(MANIFEST)}: missing runtime evidence state")
    runtime_status = runtime.get("status")
    runtime_class = runtime.get("class")
    runtime_date = runtime.get("date")
    require(runtime_status in {"pending", "passed", "failed"}, f"{display(MANIFEST)}: invalid runtime status")
    require(
        runtime_class == ("runtime-proven" if runtime_status == "passed" else "experimental"),
        f"{display(MANIFEST)}: runtime status and evidence class disagree",
    )
    if runtime_status == "pending":
        require(runtime_date is None, f"{display(MANIFEST)}: pending runtime evidence cannot have a test date")
    else:
        require(
            valid_observed_date(runtime_date),
            f"{display(MANIFEST)}: completed runtime evidence needs a YYYY-MM-DD date",
        )
    acceptance_record = normalize_relative(runtime.get("record"), f"{display(MANIFEST)} runtime record")
    require(acceptance_record == "runtime-acceptance.json", f"{display(MANIFEST)}: unexpected runtime record")

    graph = value.get("graph")
    require(isinstance(graph, dict), f"{display(MANIFEST)}: missing graph object")
    graph_layout = normalize_relative(graph.get("layout"), f"{display(MANIFEST)} graph layout")
    require((ROOT / graph_layout).resolve() == LAYOUT.resolve(), f"{display(MANIFEST)}: wrong graph layout")
    graph_fingerprint = graph.get("source_fingerprint")
    require(
        isinstance(graph_fingerprint, str)
        and graph_fingerprint.startswith("sha256:")
        and len(graph_fingerprint) == 71
        and all(character in "0123456789abcdef" for character in graph_fingerprint[7:]),
        f"{display(MANIFEST)}: invalid graph fingerprint",
    )

    artifacts = value.get("artifacts")
    require(
        isinstance(artifacts, dict) and artifacts.get("algorithm") == "sha256",
        f"{display(MANIFEST)}: unsupported artifact hash configuration",
    )
    raw_hashes = artifacts.get("files")
    require(isinstance(raw_hashes, dict), f"{display(MANIFEST)}: missing artifact hash map")
    expected_hashed = set(COMPLETED_FILES) - {"README.md", "example.json"}
    artifact_hashes: list[tuple[str, str]] = []
    for raw_path, digest in raw_hashes.items():
        artifact_path = normalize_relative(raw_path, f"{display(MANIFEST)} artifact path")
        require(
            isinstance(digest, str)
            and len(digest) == 64
            and all(character in "0123456789abcdef" for character in digest),
            f"{display(MANIFEST)}: invalid SHA-256 for {artifact_path}",
        )
        artifact_hashes.append((artifact_path, digest))
    require(
        {path for path, _ in artifact_hashes} == expected_hashed,
        f"{display(MANIFEST)} artifact inventory: "
        + describe_set_difference(expected_hashed, {path for path, _ in artifact_hashes}),
    )

    return ManifestInfo(
        depot_paths=depot_paths,
        baseline=tuple(sorted(expected_baseline.items())),
        artifact_hashes=tuple(sorted(artifact_hashes)),
        acceptance_record=acceptance_record,
        graph_fingerprint=graph_fingerprint,
        runtime_status=runtime_status,
        runtime_class=runtime_class,
        runtime_date=runtime_date,
    )


def actual_files(root: Path) -> set[str]:
    require(root.is_dir(), f"{display(root)}: missing directory")
    result: set[str] = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), f"{display(path)}: symlinks are not allowed in generated sources")
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
    return result


def describe_set_difference(expected: set[str], actual: set[str]) -> str:
    parts: list[str] = []
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing:
        parts.append("missing: " + ", ".join(missing))
    if unexpected:
        parts.append("unexpected: " + ", ".join(unexpected))
    return "; ".join(parts)


def run_git(*arguments: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except OSError as error:
        raise ValidationError(f"could not run git: {error}") from error
    require(result.returncode == 0, f"git {' '.join(arguments)} failed: {result.stderr.strip()}")
    return [line for line in result.stdout.splitlines() if line]


def validate_source_tree(info: ManifestInfo) -> None:
    expected_archive = set(info.depot_paths)
    expected_raw = {f"{path}.json" for path in info.depot_paths}
    require(
        actual_files(ARCHIVE_ROOT) == expected_archive,
        f"{display(ARCHIVE_ROOT)}: "
        + describe_set_difference(expected_archive, actual_files(ARCHIVE_ROOT)),
    )
    require(
        actual_files(RAW_ROOT) == expected_raw,
        f"{display(RAW_ROOT)}: " + describe_set_difference(expected_raw, actual_files(RAW_ROOT)),
    )

    expected_source = {
        *(f"archive/{path}" for path in expected_archive),
        *(f"raw/{path}" for path in expected_raw),
        "resources/CQA_Lab01_OneShot.archive.xl",
    }
    actual_source = actual_files(SOURCE_ROOT)
    require(
        actual_source == expected_source,
        f"{display(SOURCE_ROOT)}: " + describe_set_difference(expected_source, actual_source),
    )

    source_pathspec = SOURCE_ROOT.relative_to(ROOT).as_posix()
    tracked = set(run_git("ls-files", "--cached", "--", source_pathspec))
    expected_tracked = {
        (SOURCE_ROOT / path).relative_to(ROOT).as_posix() for path in expected_source
    }
    require(
        expected_tracked <= tracked,
        "generated source files are not tracked: " + ", ".join(sorted(expected_tracked - tracked)),
    )
    untracked = run_git("ls-files", "--others", "--exclude-standard", "--", source_pathspec)
    require(not untracked, "untracked generated source files: " + ", ".join(untracked))


def validate_checkpoint_inventories() -> None:
    for _, (checkpoint, _, expected_files, text_files) in CHECKPOINTS.items():
        actual = actual_files(checkpoint)
        require(
            actual == set(expected_files),
            f"{display(checkpoint)}: "
            + describe_set_difference(set(expected_files), actual),
        )

        pathspec = checkpoint.relative_to(ROOT).as_posix()
        tracked = set(run_git("ls-files", "--cached", "--", pathspec))
        expected_tracked = {
            (checkpoint / relative).relative_to(ROOT).as_posix()
            for relative in expected_files
        }
        require(
            tracked == expected_tracked,
            f"{display(checkpoint)} Git inventory: "
            + describe_set_difference(expected_tracked, tracked),
        )
        untracked = run_git("ls-files", "--others", "--exclude-standard", "--", pathspec)
        require(
            not untracked,
            f"{display(checkpoint)} has untracked files: " + ", ".join(untracked),
        )

        require(set(text_files) <= set(expected_files), f"{display(checkpoint)}: invalid text inventory")
        for relative in sorted(text_files):
            require(
                b"\r" not in (checkpoint / relative).read_bytes(),
                f"{display(checkpoint / relative)}: text must use LF endings",
            )

    require(
        b"\r" not in SHARED_LICENSE.read_bytes(),
        f"{display(SHARED_LICENSE)}: text must use LF endings",
    )


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"could not load {display(path)}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def validate_generated_raw(info: ManifestInfo) -> None:
    expected = {f"{path}.json" for path in info.depot_paths}
    with tempfile.TemporaryDirectory(prefix="cqa-lab01-raw-") as temporary:
        generated_root = Path(temporary) / "raw"
        module = load_module(BUILD_SCRIPT, "_cqa_build_lab01_sources")
        try:
            module.RAW_ROOT = generated_root / "mod" / "cqa" / "cqa001"
            module.main()
        finally:
            sys.modules.pop(module.__name__, None)

        actual = actual_files(generated_root)
        require(
            actual == expected,
            "Lab 1 generator output set differs from the manifest: "
            + describe_set_difference(expected, actual),
        )
        stale = [
            path
            for path in sorted(expected)
            if (generated_root / path).read_bytes() != (RAW_ROOT / path).read_bytes()
        ]
        require(not stale, "generated Lab 1 CR2W-JSON is stale: " + ", ".join(stale))


def valid_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def valid_observed_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or "T" not in value:
        return False
    try:
        observed = datetime.fromisoformat(value)
    except ValueError:
        return False
    return observed.tzinfo is not None and observed.utcoffset() is not None


def valid_observed_date(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        observed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return observed.strftime("%Y-%m-%d") == value


def validate_evidence_record(info: ManifestInfo) -> None:
    for relative, expected_digest in info.artifact_hashes:
        path = COMPLETED / relative
        require(path.is_file(), f"{display(path)}: hashed artifact is missing")
        actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            actual_digest == expected_digest,
            f"{display(path)}: SHA-256 mismatch; expected {expected_digest}, got {actual_digest}",
        )

    record_path = COMPLETED / info.acceptance_record
    require(record_path.resolve() == ACCEPTANCE.resolve(), f"{display(record_path)}: unexpected acceptance path")
    record = load_json(record_path)
    require(record.get("schema_version") == 2, f"{display(record_path)}: unsupported schema_version")
    require(record.get("example_id") == "cqa001", f"{display(record_path)}: wrong example_id")
    require(record.get("status") == info.runtime_status, f"{display(record_path)}: status disagrees with manifest")
    require(
        record.get("evidence_class") == info.runtime_class,
        f"{display(record_path)}: evidence_class disagrees with manifest",
    )

    expected_environment = dict(info.baseline)
    expected_environment.pop("recorded")
    require(
        record.get("required_environment") == expected_environment,
        f"{display(record_path)}: required environment disagrees with manifest",
    )

    candidate = record.get("candidate")
    require(isinstance(candidate, dict), f"{display(record_path)}: missing candidate object")
    require(candidate.get("manifest") == "example.json", f"{display(record_path)}: wrong manifest reference")
    installed_files = candidate.get("installed_files")
    require(
        isinstance(installed_files, list),
        f"{display(record_path)}: candidate installed_files must be a list",
    )
    installed_hashes: list[str | None] = []
    installed_paths: set[str] = set()
    for index, item in enumerate(installed_files):
        require(
            isinstance(item, dict),
            f"{display(record_path)}: installed_files[{index}] must be an object",
        )
        installed_path = normalize_relative(
            item.get("path"),
            f"{display(record_path)} installed_files[{index}].path",
        )
        require(
            installed_path not in installed_paths,
            f"{display(record_path)}: duplicate installed file {installed_path}",
        )
        installed_paths.add(installed_path)
        digest = item.get("sha256")
        require(
            digest is None or valid_sha256(digest),
            f"{display(record_path)}: invalid installed-file SHA-256 for {installed_path}",
        )
        installed_hashes.append(digest)
    require(
        installed_paths == EXPECTED_INSTALLED_FILES,
        f"{display(record_path)} installed files: "
        + describe_set_difference(EXPECTED_INSTALLED_FILES, installed_paths),
    )
    candidate_paths = candidate.get("depot_paths")
    require(isinstance(candidate_paths, list), f"{display(record_path)}: candidate depot_paths must be a list")
    normalized_candidate_paths = {
        normalize_relative(path, f"{display(record_path)} candidate depot path")
        for path in candidate_paths
    }
    require(
        len(candidate_paths) == len(normalized_candidate_paths),
        f"{display(record_path)}: duplicate candidate depot path",
    )
    require(
        normalized_candidate_paths == set(info.depot_paths),
        f"{display(record_path)}: candidate depot paths disagree with manifest",
    )

    cases = record.get("cases")
    require(isinstance(cases, list) and cases, f"{display(record_path)}: cases must be a non-empty list")
    seen_case_ids: set[str] = set()
    required_statuses: list[str] = []
    for index, case in enumerate(cases):
        require(isinstance(case, dict), f"{display(record_path)}: cases[{index}] must be an object")
        case_id = case.get("id")
        require(isinstance(case_id, str) and case_id, f"{display(record_path)}: cases[{index}] has no id")
        require(case_id not in seen_case_ids, f"{display(record_path)}: duplicate case id {case_id}")
        seen_case_ids.add(case_id)
        require(
            case_id in EXPECTED_ACCEPTANCE_CASES,
            f"{display(record_path)}: unexpected acceptance case {case_id}",
        )
        expected_case = EXPECTED_ACCEPTANCE_CASES[case_id]
        status = case.get("status")
        require(status in {"pending", "passed", "failed", "not-applicable"}, f"{display(record_path)}:{case_id}: invalid status")
        require(isinstance(case.get("required"), bool), f"{display(record_path)}:{case_id}: required must be Boolean")
        require(case.get("precondition") == expected_case["precondition"], f"{display(record_path)}:{case_id}: precondition changed")
        require(case.get("expected") == expected_case["expected"], f"{display(record_path)}:{case_id}: expected result changed")
        evidence = case.get("evidence")
        require(isinstance(evidence, list), f"{display(record_path)}:{case_id}: evidence must be a list")
        for evidence_index, evidence_item in enumerate(evidence):
            require(
                isinstance(evidence_item, dict),
                f"{display(record_path)}:{case_id}: evidence[{evidence_index}] must be an object",
            )
            require(
                evidence_item.get("type") in {"screenshot", "video", "log", "save-metadata", "notes"},
                f"{display(record_path)}:{case_id}: evidence[{evidence_index}] has an invalid type",
            )
            evidence_reference = normalize_relative(
                evidence_item.get("reference"),
                f"{display(record_path)}:{case_id}: evidence[{evidence_index}].reference",
            )
            require(
                evidence_reference.startswith("evidence/"),
                f"{display(record_path)}:{case_id}: evidence must be retained below evidence/",
            )
            require(
                valid_sha256(evidence_item.get("sha256")),
                f"{display(record_path)}:{case_id}: evidence[{evidence_index}] needs a SHA-256",
            )
            evidence_path = COMPLETED / evidence_reference
            require(evidence_path.is_file(), f"{display(evidence_path)}: retained evidence is missing")
            require(
                evidence_path.name.lower() != "sav.dat" and evidence_path.suffix.lower() != ".dat",
                f"{display(evidence_path)}: private save binaries cannot be retained as evidence",
            )
            if evidence_item["type"] == "save-metadata":
                require(
                    evidence_path.suffix.lower() in {".md", ".txt", ".json"},
                    f"{display(evidence_path)}: save-metadata evidence must be sanitized text",
                )
            require(
                hashlib.sha256(evidence_path.read_bytes()).hexdigest() == evidence_item["sha256"],
                f"{display(evidence_path)}: retained evidence SHA-256 mismatch",
            )
        if status in {"passed", "failed"}:
            require(
                isinstance(case.get("observed"), str) and case.get("observed").strip() and evidence,
                f"{display(record_path)}:{case_id}: a completed case needs an observation and evidence",
            )
        if case["required"]:
            require(status != "not-applicable", f"{display(record_path)}:{case_id}: required case cannot be not-applicable")
            required_statuses.append(status)

    require(
        seen_case_ids == set(EXPECTED_ACCEPTANCE_CASES),
        f"{display(record_path)} acceptance cases: "
        + describe_set_difference(set(EXPECTED_ACCEPTANCE_CASES), seen_case_ids),
    )
    require(
        len(required_statuses) == len(EXPECTED_ACCEPTANCE_CASES),
        f"{display(record_path)}: every Lab 1 acceptance case must remain required",
    )

    if any(status == "failed" for status in required_statuses):
        expected_runtime_status = "failed"
    elif all(status == "passed" for status in required_statuses):
        expected_runtime_status = "passed"
    else:
        expected_runtime_status = "pending"
    require(
        info.runtime_status == expected_runtime_status,
        f"{display(record_path)}: overall status disagrees with required case results",
    )

    run = record.get("run")
    require(isinstance(run, dict), f"{display(record_path)}: missing run provenance")
    require(
        run.get("performed_at") is None or valid_observed_timestamp(run.get("performed_at")),
        f"{display(record_path)}: performed_at must be an ISO 8601 timestamp with a UTC offset",
    )
    require(
        run.get("tester") is None or isinstance(run.get("tester"), str),
        f"{display(record_path)}: tester must be a string or null",
    )
    observed_environment = run.get("observed_environment")
    require(isinstance(observed_environment, dict), f"{display(record_path)}: missing observed environment")
    require(
        set(observed_environment) == set(expected_environment),
        f"{display(record_path)}: observed environment fields disagree with the required environment",
    )
    require(
        all(value is None or isinstance(value, str) for value in observed_environment.values()),
        f"{display(record_path)}: observed environment values must be strings or null",
    )
    logs = run.get("logs")
    require(isinstance(logs, list), f"{display(record_path)}: logs must be a list")
    log_paths: set[str] = set()
    log_hashes: list[str | None] = []
    for index, item in enumerate(logs):
        require(isinstance(item, dict), f"{display(record_path)}: logs[{index}] must be an object")
        log_path = normalize_relative(item.get("path"), f"{display(record_path)} logs[{index}].path")
        require(log_path not in log_paths, f"{display(record_path)}: duplicate log path {log_path}")
        log_paths.add(log_path)
        digest = item.get("sha256")
        require(
            digest is None or valid_sha256(digest),
            f"{display(record_path)}: invalid log SHA-256 for {log_path}",
        )
        log_hashes.append(digest)
    require(
        log_paths == EXPECTED_RUNTIME_LOGS,
        f"{display(record_path)} runtime logs: "
        + describe_set_difference(EXPECTED_RUNTIME_LOGS, log_paths),
    )

    has_completed_case = any(status in {"passed", "failed"} for status in required_statuses)
    if has_completed_case:
        require(
            all(valid_sha256(digest) for digest in installed_hashes),
            f"{display(record_path)}: completed run needs both installed payload SHA-256 values",
        )
        require(valid_observed_timestamp(run.get("performed_at")), f"{display(record_path)}: completed run needs performed_at")
        require(
            isinstance(run.get("tester"), str) and run["tester"].strip(),
            f"{display(record_path)}: completed run needs tester",
        )
        require(
            observed_environment == expected_environment,
            f"{display(record_path)}: completed run uses the wrong observed environment",
        )
        save = run.get("save")
        require(
            isinstance(save, dict)
            and isinstance(save.get("label"), str)
            and save["label"].strip()
            and isinstance(save.get("slot_directory"), str)
            and save["slot_directory"].strip()
            and save.get("artifact") == "sav.dat"
            and save.get("created_before_first_install") is True
            and valid_sha256(save.get("sha256")),
            f"{display(record_path)}: completed run needs a hash-bound pre-install save",
        )
        require(
            all(valid_sha256(digest) for digest in log_hashes),
            f"{display(record_path)}: completed run needs hash-bound logs",
        )
        if info.runtime_status in {"passed", "failed"}:
            require(
                info.runtime_date == datetime.fromisoformat(run["performed_at"]).date().isoformat(),
                f"{display(record_path)}: manifest runtime date disagrees with performed_at",
            )

    require(record.get("promotion_rule") == EXPECTED_PROMOTION_RULE, f"{display(record_path)}: promotion rule changed")


def validate_reader_evidence_status(info: ManifestInfo) -> None:
    expected_status_line = {
        "pending": "**Lab 1 runtime evidence:** **Experimental** — pending.",
        "failed": "**Lab 1 runtime evidence:** **Experimental** — failed.",
        "passed": "**Lab 1 runtime evidence:** **Runtime-proven** — passed.",
    }[info.runtime_status]
    for page in LAB_STATUS_PAGES:
        status_lines = [
            line
            for line in page.read_text(encoding="utf-8").splitlines()
            if line.startswith("**Lab 1 runtime evidence:**")
        ]
        require(
            status_lines == [expected_status_line],
            f"{display(page)}: dedicated Lab 1 runtime evidence marker disagrees with the manifest",
        )

    expected_date = info.runtime_date if info.runtime_date is not None else "Not yet recorded"
    date_row = f"| Runtime test date | {expected_date} |"
    for page in LAB_PRACTICAL_PAGES:
        require(
            date_row in page.read_text(encoding="utf-8"),
            f"{display(page)}: runtime test date disagrees with the manifest",
        )


def markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<"):
        end = target.find(">")
        require(end > 1, f"invalid angle-bracket Markdown target {raw_target!r}")
        return target[1:end]
    return target.split(maxsplit=1)[0]


def markdown_visible_text(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    visible: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line in text.splitlines():
        match = MARKDOWN_FENCE_PATTERN.match(line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = None
                fence_length = 0
            continue
        if fence_char is None:
            visible.append(line)
    require(fence_char is None, "unterminated Markdown code fence")
    return "\n".join(visible)


def markdown_heading_ids(text: str) -> set[str]:
    counts: dict[str, int] = {}
    heading_ids: set[str] = set()
    for line in markdown_visible_text(text).splitlines():
        match = MARKDOWN_HEADING_PATTERN.match(line)
        if not match:
            continue
        heading = re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
        heading = re.sub(r"<[^>]*>", "", heading)
        heading = re.sub(r"[^\w\-\s]", "", heading, flags=re.UNICODE)
        base = re.sub(r"\s+", "-", heading.strip().lower())
        if not base:
            continue
        duplicate_index = counts.get(base, 0)
        counts[base] = duplicate_index + 1
        heading_ids.add(base if duplicate_index == 0 else f"{base}-{duplicate_index}")
    return heading_ids


def validate_book_links_and_summary() -> None:
    summary_text = markdown_visible_text(SUMMARY.read_text(encoding="utf-8"))
    raw_summary_targets = [
        markdown_target(match.group(1))
        for match in MARKDOWN_LINK_PATTERN.finditer(summary_text)
    ]
    summary_targets = [target for target in raw_summary_targets if target.split("#", 1)[0].endswith(".md")]
    normalized_summary: list[str] = []
    for target in summary_targets:
        path_only = target.split("#", 1)[0]
        require(
            not path_only.startswith("/")
            and "\\" not in path_only
            and ":" not in path_only.split("/", 1)[0]
            and all(part not in {"", ".", ".."} for part in path_only.split("/")),
            f"{display(SUMMARY)}: unsafe chapter target {target!r}",
        )
        normalized = PurePosixPath(path_only).as_posix()
        require((BOOK_SRC / normalized).is_file(), f"{display(SUMMARY)}: missing chapter {normalized}")
        normalized_summary.append(normalized)

    require(
        len(normalized_summary) == len(set(normalized_summary)),
        f"{display(SUMMARY)}: duplicate chapter target",
    )
    actual_pages = {
        path.relative_to(BOOK_SRC).as_posix()
        for path in BOOK_SRC.rglob("*.md")
        if path.resolve() != SUMMARY.resolve()
    }
    require(
        set(normalized_summary) == actual_pages,
        f"{display(SUMMARY)} chapter coverage: "
        + describe_set_difference(actual_pages, set(normalized_summary)),
    )

    generated_downloads = {
        f"downloads/{name}" for name in GENERATED_DOWNLOAD_NAMES
    }
    heading_cache: dict[Path, set[str]] = {}
    for page in sorted(BOOK_SRC.rglob("*.md")):
        visible_text = markdown_visible_text(page.read_text(encoding="utf-8"))
        for match in MARKDOWN_LINK_PATTERN.finditer(visible_text):
            target = markdown_target(match.group(1))
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
                require(
                    target.startswith(("https://", "http://", "mailto:")),
                    f"{display(page)}: unsupported link scheme in {target!r}",
                )
                continue
            target_without_query = target.split("?", 1)[0]
            path_only, separator, fragment = target_without_query.partition("#")
            require(not path_only.startswith(("/", "\\")), f"{display(page)}: absolute local link {target!r}")
            require("\\" not in path_only, f"{display(page)}: local Markdown link must use forward slashes: {target!r}")
            resolved = page.resolve() if not path_only else (
                page.parent / Path(*PurePosixPath(path_only).parts)
            ).resolve()
            try:
                relative = resolved.relative_to(BOOK_SRC.resolve()).as_posix()
            except ValueError as error:
                raise ValidationError(f"{display(page)}: local link escapes book/src: {target!r}") from error
            if relative in generated_downloads:
                continue
            require(resolved.is_file(), f"{display(page)}: missing local link target {target!r}")
            if separator and resolved.suffix.lower() == ".md":
                if resolved not in heading_cache:
                    heading_cache[resolved] = markdown_heading_ids(
                        resolved.read_text(encoding="utf-8")
                    )
                decoded_fragment = unquote(fragment)
                require(
                    decoded_fragment in heading_cache[resolved],
                    f"{display(page)}: missing Markdown heading #{decoded_fragment} in {display(resolved)}",
                )


def iter_json_objects(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_json_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_json_objects(child)


def validate_lab01_journal_contract() -> None:
    journal = load_json(JOURNAL_RAW)
    quest = load_json(QUEST_RAW)
    localization = load_json(LOCALIZATION_RAW)

    root = journal["Data"]["RootChunk"]
    require(root.get("$type") == "gameJournalResource", f"{display(JOURNAL_RAW)}: wrong root type")
    root_entry = root.get("entry", {}).get("Data")
    require(
        isinstance(root_entry, dict) and root_entry.get("$type") == "gameJournalRootFolderEntry",
        f"{display(JOURNAL_RAW)}: missing root folder entry",
    )
    descriptor = root_entry.get("descriptor", {})
    require(
        descriptor.get("DepotPath", {}).get("$value") == "base\\journal\\descriptor.journaldesc"
        and descriptor.get("Flags") == "Soft",
        f"{display(JOURNAL_RAW)}: descriptor contract changed",
    )

    journal_entries: dict[str, str] = {}
    journal_entry_objects: dict[str, dict[str, Any]] = {}

    def visit_entry(entry: Any, parent_parts: tuple[str, ...]) -> None:
        require(isinstance(entry, dict), f"{display(JOURNAL_RAW)}: journal entry must be an object")
        entry_id = entry.get("id")
        parts = parent_parts
        if entry_id is not None:
            require(isinstance(entry_id, str) and entry_id, f"{display(JOURNAL_RAW)}: invalid journal entry id")
            parts = (*parent_parts, entry_id)
            real_path = "/".join(parts)
            require(real_path not in journal_entries, f"{display(JOURNAL_RAW)}: duplicate journal path {real_path}")
            journal_entries[real_path] = entry.get("$type")
            journal_entry_objects[real_path] = entry
        children = entry.get("entries", [])
        require(isinstance(children, list), f"{display(JOURNAL_RAW)}: entries must be an array")
        for child in children:
            require(
                isinstance(child, dict) and isinstance(child.get("Data"), dict),
                f"{display(JOURNAL_RAW)}: journal child must be a populated handle",
            )
            visit_entry(child["Data"], parts)

    visit_entry(root_entry, ())
    expected_entries = {
        "quests": "gameJournalPrimaryFolderEntry",
        "quests/minor_quest": "gameJournalFolderEntry",
        "quests/minor_quest/cqa001": "gameJournalQuest",
        "quests/minor_quest/cqa001/cqa001_01": "gameJournalQuestPhase",
        "quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait": "gameJournalQuestObjective",
    }
    require(journal_entries == expected_entries, f"{display(JOURNAL_RAW)}: Lab 1 journal tree changed")

    quest_entry = journal_entry_objects["quests/minor_quest/cqa001"]
    objective_entry = journal_entry_objects[
        "quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait"
    ]
    require(
        quest_entry.get("title") == {"unk1": "0", "value": "cqa_cqa001_title"},
        f"{display(JOURNAL_RAW)}: quest title localization join changed",
    )
    require(
        objective_entry.get("description")
        == {"unk1": "0", "value": "cqa_cqa001_objective_wait"},
        f"{display(JOURNAL_RAW)}: objective localization join changed",
    )

    journal_nodes = [
        item
        for item in iter_json_objects(quest)
        if item.get("$type") == "questJournalNodeDefinition"
        and item.get("type", {}).get("Data", {}).get("$type")
        == "questJournalQuestEntry_NodeType"
    ]
    require(len(journal_nodes) == 4, f"{display(QUEST_RAW)}: expected four journal nodes")
    nodes_by_id = {node.get("id"): node for node in journal_nodes}
    expected_node_paths = {
        11: ("quests/minor_quest/cqa001", "gameJournalQuest"),
        12: (
            "quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait",
            "gameJournalQuestObjective",
        ),
        14: (
            "quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait",
            "gameJournalQuestObjective",
        ),
        16: ("quests/minor_quest/cqa001", "gameJournalQuest"),
    }
    require(
        set(nodes_by_id) == set(expected_node_paths),
        f"{display(QUEST_RAW)}: journal node ID inventory changed",
    )
    for node_id, (expected_path, expected_class) in expected_node_paths.items():
        node_type = nodes_by_id[node_id]["type"]["Data"]
        require(
            node_type.get("optional") == 0
            and node_type.get("sendNotification") == 1
            and node_type.get("trackQuest") == 1
            and node_type.get("version") == "Initial",
            f"{display(QUEST_RAW)}: journal node {node_id} presentation contract changed",
        )
        path = node_type.get("path", {}).get("Data")
        require(
            isinstance(path, dict) and path.get("$type") == "gameJournalPath",
            f"{display(QUEST_RAW)}: journal node {node_id} has no gameJournalPath",
        )
        real_path = path.get("realPath")
        class_name = path.get("className", {}).get("$value")
        require(
            real_path == expected_path
            and class_name == expected_class
            and journal_entries.get(real_path) == class_name
            and path.get("editorPath") == "",
            f"{display(QUEST_RAW)}: journal node {node_id} path/class does not resolve",
        )
        parts = real_path.split("/")
        file_entry_index = path.get("fileEntryIndex")
        require(file_entry_index == 2, f"{display(QUEST_RAW)}: Lab 1 journal fileEntryIndex must be 2")
        containing_path = "/".join(parts[: file_entry_index + 1])
        require(
            journal_entries.get(containing_path) == "gameJournalQuest",
            f"{display(QUEST_RAW)}: fileEntryIndex does not identify the containing quest",
        )

    journal_keys = {
        item["value"]
        for item in iter_json_objects(journal)
        if "unk1" in item and isinstance(item.get("value"), str) and item["value"]
    }
    expected_text = {
        "cqa_cqa001_title": "First Signal",
        "cqa_cqa001_objective_wait": "Wait for the signal.",
    }
    require(journal_keys == set(expected_text), f"{display(JOURNAL_RAW)}: localization key inventory changed")

    localization_root = localization["Data"]["RootChunk"].get("root", {}).get("Data")
    require(
        isinstance(localization_root, dict)
        and localization_root.get("$type") == "localizationPersistenceOnScreenEntries",
        f"{display(LOCALIZATION_RAW)}: wrong onscreen localization root",
    )
    localized_entries = localization_root.get("entries")
    require(isinstance(localized_entries, list), f"{display(LOCALIZATION_RAW)}: missing localization entries")
    localized_text: dict[str, str] = {}
    for index, entry in enumerate(localized_entries):
        require(
            isinstance(entry, dict)
            and entry.get("$type") == "localizationPersistenceOnScreenEntry"
            and str(entry.get("primaryKey")) == "0"
            and entry.get("maleVariant") == "",
            f"{display(LOCALIZATION_RAW)}: invalid onscreen entry {index}",
        )
        key = entry.get("secondaryKey")
        value = entry.get("femaleVariant")
        require(
            isinstance(key, str) and key and isinstance(value, str) and value and key not in localized_text,
            f"{display(LOCALIZATION_RAW)}: invalid or duplicate onscreen key at entry {index}",
        )
        localized_text[key] = value
    require(localized_text == expected_text, f"{display(LOCALIZATION_RAW)}: journal text lookup contract changed")


def parse_archive_xl(
    path: Path,
) -> tuple[list[tuple[str, str]], set[str], set[str]]:
    phases: list[list[str | None]] = []
    journal: list[str] = []
    localization: list[str] = []
    section: str | None = None
    seen_headers: set[str] = set()
    saw_phase_list = False
    saw_onscreens = False
    saw_locale = False

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        require("\t" not in raw_line, f"{display(path)}:{line_number}: tabs are not allowed")
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))

        if indent == 0 and stripped in {"quest:", "journal:", "localization:"}:
            section = stripped[:-1]
            require(section not in seen_headers, f"{display(path)}:{line_number}: duplicate {section} section")
            seen_headers.add(section)
            continue

        if section == "quest" and indent == 2 and stripped == "phases:":
            require(not saw_phase_list, f"{display(path)}:{line_number}: duplicate phases list")
            saw_phase_list = True
            continue
        if section == "quest" and indent == 2 and stripped.startswith("- path:"):
            require(saw_phase_list, f"{display(path)}:{line_number}: quest path is outside phases")
            require(
                not phases or phases[-1][1] is not None,
                f"{display(path)}:{line_number}: preceding quest phase has no parent",
            )
            phase_path = normalize_relative(
                stripped.removeprefix("- path:").strip(),
                f"{display(path)}:{line_number}",
            )
            phases.append([phase_path, None])
            continue
        elif section == "quest" and indent == 4 and stripped.startswith("parent:"):
            require(phases and phases[-1][1] is None, f"{display(path)}:{line_number}: parent has no phase")
            phases[-1][1] = normalize_relative(
                stripped.removeprefix("parent:").strip(),
                f"{display(path)}:{line_number}",
            )
            continue
        elif section == "journal" and indent == 0 and stripped.startswith("- "):
            journal.append(
                normalize_relative(
                    stripped.removeprefix("- ").strip(),
                    f"{display(path)}:{line_number}",
                )
            )
            continue
        elif section == "localization" and indent == 2 and stripped == "onscreens:":
            require(not saw_onscreens, f"{display(path)}:{line_number}: duplicate onscreens section")
            saw_onscreens = True
            continue
        elif section == "localization" and indent == 4 and stripped == "en-us:":
            require(saw_onscreens, f"{display(path)}:{line_number}: en-us is outside onscreens")
            require(not saw_locale, f"{display(path)}:{line_number}: duplicate en-us section")
            saw_locale = True
            continue
        elif section == "localization" and indent == 4 and stripped.startswith("- "):
            require(saw_locale, f"{display(path)}:{line_number}: localization path is outside en-us")
            localization.append(
                normalize_relative(
                    stripped.removeprefix("- ").strip(),
                    f"{display(path)}:{line_number}",
                )
            )
            continue
        else:
            raise ValidationError(f"{display(path)}:{line_number}: unsupported ArchiveXL shape: {stripped!r}")

    require(
        seen_headers == {"quest", "journal", "localization"},
        f"{display(path)}: expected quest, journal, and localization sections",
    )
    require(saw_phase_list and phases, f"{display(path)}: missing quest phases list")
    require(all(parent is not None for _, parent in phases), f"{display(path)}: quest phase has no parent")
    require(saw_onscreens and saw_locale, f"{display(path)}: missing localization/onscreens/en-us nesting")
    phase_pairs = [(phase, parent) for phase, parent in phases if parent is not None]
    phase_paths = [phase for phase, _ in phase_pairs]
    require(len(phase_paths) == len(set(phase_paths)), f"{display(path)}: duplicate quest phase")
    require(len(journal) == len(set(journal)), f"{display(path)}: duplicate journal registration")
    require(len(localization) == len(set(localization)), f"{display(path)}: duplicate localization registration")
    return phase_pairs, set(journal), set(localization)


def validate_archive_xl(info: ManifestInfo) -> None:
    require(ARCHIVE_XL.is_file(), f"{display(ARCHIVE_XL)}: missing ArchiveXL registration")
    phases, journal, localization = parse_archive_xl(ARCHIVE_XL)
    expected_phases = {path for path in info.depot_paths if path.endswith(".questphase")}
    expected_journal = {path for path in info.depot_paths if path.endswith(".journal")}
    expected_localization = {path for path in info.depot_paths if path.endswith(".json")}
    require(
        {phase for phase, _ in phases} == expected_phases,
        f"{display(ARCHIVE_XL)} quest phases and example.json disagree: "
        + describe_set_difference(expected_phases, {phase for phase, _ in phases}),
    )
    require(
        journal == expected_journal,
        f"{display(ARCHIVE_XL)} journal section and example.json disagree: "
        + describe_set_difference(expected_journal, journal),
    )
    require(
        localization == expected_localization,
        f"{display(ARCHIVE_XL)} localization section and example.json disagree: "
        + describe_set_difference(expected_localization, localization),
    )
    require(
        all(parent == "base/quest/cyberpunk2077.quest" for _, parent in phases),
        f"{display(ARCHIVE_XL)}: Lab 1 phase must attach to base/quest/cyberpunk2077.quest",
    )


def validate_cr2w_pairs(info: ManifestInfo) -> None:
    for depot_path in info.depot_paths:
        binary_path = depot_file(ARCHIVE_ROOT, depot_path)
        raw_path = raw_depot_file(depot_path)
        payload = binary_path.read_bytes()
        require(payload.startswith(b"CR2W"), f"{display(binary_path)}: missing CR2W magic")

        source = load_json(raw_path)
        header = source.get("Header")
        data = source.get("Data")
        require(isinstance(header, dict) and isinstance(data, dict), f"{display(raw_path)}: missing Header/Data objects")
        require(header.get("DataType") == "CR2W", f"{display(raw_path)}: Header.DataType is not CR2W")
        archive_name = normalize_relative(header.get("ArchiveFileName"), f"{display(raw_path)} Header.ArchiveFileName")
        require(archive_name == depot_path, f"{display(raw_path)}: ArchiveFileName does not match example.json")

        root_chunk = data.get("RootChunk")
        require(isinstance(root_chunk, dict), f"{display(raw_path)}: missing Data.RootChunk")
        root_type = root_chunk.get("$type")
        suffix = next((item for item in EXPECTED_ROOT_TYPES if depot_path.endswith(item)), None)
        require(suffix is not None, f"{depot_path}: no expected resource type is defined")
        require(
            root_type == EXPECTED_ROOT_TYPES[suffix],
            f"{display(raw_path)}: expected root type {EXPECTED_ROOT_TYPES[suffix]!r}, got {root_type!r}",
        )
        require(
            root_type.encode("ascii") in payload,
            f"{display(binary_path)}: cooked string table does not contain raw root type {root_type!r}",
        )


def validate_graph(info: ManifestInfo) -> None:
    source = load_json(ROOT / QUEST_SOURCE_RELPATH)
    layout = load_json(LAYOUT)
    module = load_module(RENDER_SCRIPT, "_cqa_render_quest_graph")
    try:
        nodes, edges = module.parse_graph(source)
        module.validate_layout(nodes, layout, edges)
        actual_fingerprint = module.fingerprint(nodes, edges)
        require(
            layout.get("source_fingerprint") == actual_fingerprint,
            f"{display(LAYOUT)}: source fingerprint mismatch; actual {actual_fingerprint}",
        )
        require(
            info.graph_fingerprint == actual_fingerprint,
            f"{display(MANIFEST)}: graph fingerprint does not match the source",
        )
        generated_svg = module.render_svg(
            QUEST_SOURCE_RELPATH,
            nodes,
            edges,
            layout,
            actual_fingerprint,
        ).encode("utf-8")
    finally:
        sys.modules.pop(module.__name__, None)
    require(SVG.is_file(), f"{display(SVG)}: missing SVG")
    require(SVG.read_bytes() == generated_svg, f"{display(SVG)}: generated SVG is stale")


def run_packager(output: Path) -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, str(PACKAGE_SCRIPT), "--output", str(output)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(
        result.returncode == 0,
        f"package_examples.py failed:\n{result.stdout}{result.stderr}".rstrip(),
    )


def expected_zip_entries(
    source: Path,
    root_name: str,
    expected_files: frozenset[str],
    license_path: Path,
) -> dict[str, bytes]:
    result = {
        f"{root_name}/{relative}": (source / relative).read_bytes()
        for relative in expected_files
    }
    license_name = f"{root_name}/LICENSE.md"
    require(license_name not in result, f"{display(source)}: LICENSE.md collides with shared ZIP entry")
    result[license_name] = license_path.read_bytes()
    return result


def validate_zip(
    path: Path,
    source: Path,
    root_name: str,
    expected_files: frozenset[str],
    license_path: Path,
) -> None:
    expected = expected_zip_entries(source, root_name, expected_files, license_path)
    with ZipFile(path) as archive:
        require(archive.comment == b"", f"{path.name}: unexpected archive comment")
        require(archive.testzip() is None, f"{path.name}: CRC check failed")
        infos = archive.infolist()
        names = [info.filename for info in infos]
        require(names == sorted(expected), f"{path.name}: entry order or set is not canonical")
        require(len(names) == len(set(names)), f"{path.name}: duplicate entry")
        for info in infos:
            require("\\" not in info.filename, f"{path.name}: non-POSIX entry {info.filename!r}")
            require(info.date_time == ZIP_TIMESTAMP, f"{path.name}:{info.filename}: timestamp drift")
            require(info.create_system == ZIP_CREATE_SYSTEM, f"{path.name}:{info.filename}: create_system drift")
            require(info.create_version == ZIP_VERSION, f"{path.name}:{info.filename}: create_version drift")
            require(info.extract_version == ZIP_VERSION, f"{path.name}:{info.filename}: extract_version drift")
            require(info.flag_bits == 0, f"{path.name}:{info.filename}: flag_bits drift")
            require(info.compress_type == ZIP_DEFLATED, f"{path.name}:{info.filename}: compression drift")
            require(info.volume == 0, f"{path.name}:{info.filename}: volume drift")
            require(info.internal_attr == 0, f"{path.name}:{info.filename}: internal_attr drift")
            require(info.external_attr == ZIP_MODE << 16, f"{path.name}:{info.filename}: permissions drift")
            require(info.extra == b"", f"{path.name}:{info.filename}: unexpected extra metadata")
            require(info.comment == b"", f"{path.name}:{info.filename}: unexpected entry comment")
            require(archive.read(info) == expected[info.filename], f"{path.name}:{info.filename}: content mismatch")


def validate_packages() -> None:
    with tempfile.TemporaryDirectory(prefix="cqa-zips-a-") as first_directory, tempfile.TemporaryDirectory(
        prefix="cqa-zips-b-"
    ) as second_directory:
        first = Path(first_directory)
        second = Path(second_directory)
        packager = load_module(PACKAGE_SCRIPT, "cqa_package_examples_atomic_check")

        evidence_fixture = first / "lab02-evidence-fixture"
        evidence_path = evidence_fixture / "completed" / "evidence" / "run-note.md"
        evidence_path.parent.mkdir(parents=True)
        evidence_path.write_text("sanitized evidence\n", encoding="utf-8", newline="\n")
        evidence_record = evidence_fixture / "completed" / "runtime-acceptance.json"
        evidence_record.write_text(
            json.dumps(
                {
                    "cases": [
                        {"evidence": [{"reference": "evidence/run-note.md"}]},
                    ]
                }
            ),
            encoding="utf-8",
            newline="\n",
        )
        original_lab02 = packager.LAB02
        try:
            packager.LAB02 = evidence_fixture
            require(
                packager.lab02_retained_evidence_files() == ("evidence/run-note.md",),
                "package_examples.py did not admit acceptance-bound Lab 2 evidence",
            )
            evidence_record.write_text(
                json.dumps(
                    {
                        "cases": [
                            {"evidence": [{"reference": "../private-save.dat"}]},
                        ]
                    }
                ),
                encoding="utf-8",
                newline="\n",
            )
            try:
                packager.lab02_retained_evidence_files()
            except ValueError:
                pass
            else:
                raise ValidationError("package_examples.py accepted an unsafe evidence path")
        finally:
            packager.LAB02 = original_lab02

        evidence_record.write_text(
            json.dumps(
                {
                    "cases": [
                        {"evidence": [{"reference": "evidence/run-note.md"}]},
                    ]
                }
            ),
            encoding="utf-8",
            newline="\n",
        )
        original_lab03 = packager.LAB03
        try:
            packager.LAB03 = evidence_fixture
            require(
                packager.lab03_retained_evidence_files() == ("evidence/run-note.md",),
                "package_examples.py did not admit acceptance-bound Lab 3 evidence",
            )
            evidence_record.write_text(
                json.dumps(
                    {
                        "cases": [
                            {"evidence": [{"reference": "../private-save.dat"}]},
                        ]
                    }
                ),
                encoding="utf-8",
                newline="\n",
            )
            try:
                packager.lab03_retained_evidence_files()
            except ValueError:
                pass
            else:
                raise ValidationError("package_examples.py accepted an unsafe Lab 3 evidence path")
        finally:
            packager.LAB03 = original_lab03

        preserved = first / "preserved.zip"
        sentinel = b"previous valid download"
        preserved.write_bytes(sentinel)
        try:
            packager.package(
                LAB / "start",
                "Invalid",
                ("missing.file",),
                frozenset(),
                SHARED_LICENSE,
                preserved,
            )
        except ValueError:
            pass
        else:
            raise ValidationError("package_examples.py accepted an invalid checkpoint inventory")
        require(
            preserved.read_bytes() == sentinel,
            "package_examples.py changed the destination after inventory validation failed",
        )
        run_packager(first)
        run_packager(second)
        for name, (
            source,
            root_name,
            expected_files,
            _,
            license_path,
        ) in packager.CHECKPOINTS.items():
            first_zip = first / name
            second_zip = second / name
            require(first_zip.is_file() and second_zip.is_file(), f"package_examples.py did not create {name}")
            validate_zip(
                first_zip,
                source,
                root_name,
                frozenset(expected_files),
                license_path,
            )
            require(
                first_zip.read_bytes() == second_zip.read_bytes(),
                f"{name}: two clean packaging runs differ",
            )


def validate_lab02() -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, str(LAB02_VALIDATOR)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(
        result.returncode == 0,
        f"validate_lab02.py failed:\n{result.stdout}{result.stderr}".rstrip(),
    )


def validate_lab03() -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, str(LAB03_VALIDATOR)],
        cwd=ROOT,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    require(
        result.returncode == 0,
        f"validate_lab03.py failed:\n{result.stdout}{result.stderr}".rstrip(),
    )


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
        print(f"[FAIL] Lab 1 manifest: {error}", file=sys.stderr)
        return 1
    print("[ OK ] Lab 1 manifest")

    checks: tuple[tuple[str, Callable[[], None]], ...] = (
        ("generated Lab 1 CR2W-JSON", lambda: validate_generated_raw(info)),
        ("Lab 1 source file set and Git tracking", lambda: validate_source_tree(info)),
        ("Lab 1 checkpoint inventories and line endings", validate_checkpoint_inventories),
        ("Lab 1 hashes and runtime acceptance", lambda: validate_evidence_record(info)),
        ("Lab 1 reader-facing evidence status", lambda: validate_reader_evidence_status(info)),
        ("book links and SUMMARY coverage", validate_book_links_and_summary),
        ("Lab 1 journal and localization lookups", validate_lab01_journal_contract),
        ("example.json and ArchiveXL registrations", lambda: validate_archive_xl(info)),
        ("cooked CR2W and review-source provenance", lambda: validate_cr2w_pairs(info)),
        ("Lab 1 graph fingerprint and exact SVG", lambda: validate_graph(info)),
        ("Lab 2 project, evidence, semantics, and graph", validate_lab02),
        ("Lab 3 project, world resources, evidence, and graph", validate_lab03),
        ("deterministic example ZIPs", validate_packages),
    )
    results = [run_check(name, check) for name, check in checks]
    passed = all(results)
    if passed:
        print("Validation passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
