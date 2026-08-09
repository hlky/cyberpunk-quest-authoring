#!/usr/bin/env python3
"""Validate generated documentation artifacts and Lab 1 example projects.

The validator deliberately uses only the Python standard library. It parses
JSON only from the checked manifest, layout, and expected CR2W-JSON paths; a
cooked resource named ``*.json`` is treated as binary, never as JSON.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any, Callable
from zipfile import ZIP_DEFLATED, ZipFile


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-01-one-shot"
COMPLETED = LAB / "completed"
SOURCE_ROOT = COMPLETED / "source"
ARCHIVE_ROOT = SOURCE_ROOT / "archive"
RAW_ROOT = SOURCE_ROOT / "raw"
ARCHIVE_XL = SOURCE_ROOT / "resources" / "CQA_Lab01_OneShot.archive.xl"
MANIFEST = COMPLETED / "example.json"
LAYOUT = ROOT / "assets" / "diagrams" / "lab-01" / "cqa001.questphase.layout.json"
SVG = ROOT / "book" / "src" / "images" / "lab-01" / "cqa001.questphase.svg"
QUEST_SOURCE_RELPATH = Path(
    "examples/lab-01-one-shot/completed/source/raw/"
    "mod/cqa/cqa001/phases/cqa001.questphase.json"
)
BUILD_SCRIPT = ROOT / "scripts" / "build_lab01_sources.py"
RENDER_SCRIPT = ROOT / "scripts" / "render_quest_graph.py"
PACKAGE_SCRIPT = ROOT / "scripts" / "package_examples.py"
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

EXPECTED_ROOT_TYPES = {
    ".journal": "gameJournalResource",
    ".questphase": "questQuestPhaseResource",
    ".json": "JsonResource",
}


class ValidationError(RuntimeError):
    """A repository invariant was not satisfied."""


@dataclass(frozen=True)
class ManifestInfo:
    depot_paths: tuple[str, ...]


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
    if resolved in {MANIFEST.resolve(strict=False), LAYOUT.resolve(strict=False)}:
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
    require(value.get("schema_version") == 1, f"{display(MANIFEST)}: unsupported schema_version")

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
    return ManifestInfo(depot_paths=depot_paths)


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


def validate_graph() -> None:
    source = load_json(ROOT / QUEST_SOURCE_RELPATH)
    layout = load_json(LAYOUT)
    module = load_module(RENDER_SCRIPT, "_cqa_render_quest_graph")
    try:
        nodes, edges = module.parse_graph(source)
        module.validate_layout(nodes, layout)
        actual_fingerprint = module.fingerprint(nodes, edges)
        require(
            layout.get("source_fingerprint") == actual_fingerprint,
            f"{display(LAYOUT)}: source fingerprint mismatch; actual {actual_fingerprint}",
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
) -> dict[str, bytes]:
    result = {
        f"{root_name}/{relative}": (source / relative).read_bytes()
        for relative in expected_files
    }
    license_name = f"{root_name}/LICENSE.md"
    require(license_name not in result, f"{display(source)}: LICENSE.md collides with shared ZIP entry")
    result[license_name] = SHARED_LICENSE.read_bytes()
    return result


def validate_zip(
    path: Path,
    source: Path,
    root_name: str,
    expected_files: frozenset[str],
) -> None:
    expected = expected_zip_entries(source, root_name, expected_files)
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
        run_packager(first)
        run_packager(second)
        for name, (source, root_name, expected_files, _) in CHECKPOINTS.items():
            first_zip = first / name
            second_zip = second / name
            require(first_zip.is_file() and second_zip.is_file(), f"package_examples.py did not create {name}")
            validate_zip(first_zip, source, root_name, expected_files)
            require(
                first_zip.read_bytes() == second_zip.read_bytes(),
                f"{name}: two clean packaging runs differ",
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
        ("example.json and ArchiveXL registrations", lambda: validate_archive_xl(info)),
        ("cooked CR2W and review-source provenance", lambda: validate_cr2w_pairs(info)),
        ("Lab 1 graph fingerprint and exact SVG", validate_graph),
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
