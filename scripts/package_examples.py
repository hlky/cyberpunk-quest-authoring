#!/usr/bin/env python3
"""Create deterministic downloadable ZIPs for tutorial checkpoints.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-01-one-shot"
START_FILES = (
    "CQA_Lab01_OneShot_Start.cpmodproj",
    "README.md",
)
START_TEXT_FILES = frozenset(START_FILES)
COMPLETED_FILES = (
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
        LAB / "completed",
        "CQA_Lab01_OneShot",
        COMPLETED_FILES,
        COMPLETED_TEXT_FILES,
    ),
}
SHARED = (LAB / "LICENSE.md",)
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)
ZIP_CREATE_SYSTEM = 3  # Unix: keeps host OS out of the archive metadata.
ZIP_VERSION = 20
ZIP_MODE = 0o100644
ZIP_COMPRESSION_LEVEL = 9


def file_bytes(source: Path, *, text: bool) -> bytes:
    payload = source.read_bytes()
    if not text:
        return payload
    normalized = payload.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return normalized.encode("utf-8")


def add_file(archive: ZipFile, source: Path, target: str, *, text: bool) -> None:
    info = ZipInfo(target, ZIP_TIMESTAMP)
    info.create_system = ZIP_CREATE_SYSTEM
    info.create_version = ZIP_VERSION
    info.extract_version = ZIP_VERSION
    info.reserved = 0
    info.flag_bits = 0
    info.compress_type = ZIP_DEFLATED
    info.volume = 0
    info.internal_attr = 0
    info.external_attr = ZIP_MODE << 16
    info.extra = b""
    info.comment = b""
    archive.writestr(
        info,
        file_bytes(source, text=text),
        compress_type=ZIP_DEFLATED,
        compresslevel=ZIP_COMPRESSION_LEVEL,
    )


def entries(
    source: Path,
    root_name: str,
    expected_files: tuple[str, ...],
    text_files: frozenset[str],
) -> list[tuple[str, Path, bool]]:
    actual_files = {
        path.relative_to(source).as_posix()
        for path in source.rglob("*")
        if path.is_file()
    }
    expected = set(expected_files)
    if actual_files != expected:
        missing = sorted(expected - actual_files)
        unexpected = sorted(actual_files - expected)
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if unexpected:
            details.append("unexpected: " + ", ".join(unexpected))
        raise ValueError(f"{source}: checkpoint inventory mismatch ({'; '.join(details)})")
    if not text_files <= expected:
        raise ValueError(f"{source}: text inventory is not a subset of checkpoint files")

    result = [
        (f"{root_name}/{relative}", source / Path(*PurePosixPath(relative).parts), relative in text_files)
        for relative in expected_files
    ]
    result.extend((f"{root_name}/LICENSE.md", shared, True) for shared in SHARED)
    result.sort(key=lambda entry: entry[0])

    targets = [target for target, _, _ in result]
    if len(targets) != len(set(targets)):
        raise ValueError(f"{source}: duplicate ZIP entry")
    return result


def package(
    source: Path,
    root_name: str,
    expected_files: tuple[str, ...],
    text_files: frozenset[str],
    destination: Path,
) -> None:
    prepared_entries = entries(source, root_name, expected_files, text_files)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
        delete=False,
    ) as temporary_file:
        temporary_path = Path(temporary_file.name)
    try:
        with ZipFile(
            temporary_path,
            "w",
            compression=ZIP_DEFLATED,
            compresslevel=ZIP_COMPRESSION_LEVEL,
            strict_timestamps=True,
        ) as archive:
            for target, path, is_text in prepared_entries:
                add_file(archive, path, target, text=is_text)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "book" / "site" / "downloads",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for name, (source, root_name, expected_files, text_files) in CHECKPOINTS.items():
        package(source, root_name, expected_files, text_files, args.output / name)


if __name__ == "__main__":
    main()
