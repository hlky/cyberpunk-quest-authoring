#!/usr/bin/env python3
"""Create deterministic downloadable ZIPs for tutorial checkpoints.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
LAB01 = ROOT / "examples" / "lab-01-one-shot"
LAB02 = ROOT / "examples" / "lab-02-signal-race"
LAB03 = ROOT / "examples" / "lab-03-boundary-check"
LAB04 = ROOT / "examples" / "lab-04-handoff-point"
LAB05 = ROOT / "examples" / "lab-05-first-contact"


def lab02_retained_evidence_files() -> tuple[str, ...]:
    """Return only acceptance-record evidence paths safe to ship in Lab 2."""

    record_path = LAB02 / "completed" / "runtime-acceptance.json"
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read Lab 2 acceptance record: {error}") from error

    cases = record.get("cases") if isinstance(record, dict) else None
    if not isinstance(cases, list):
        raise ValueError("Lab 2 acceptance record cases must be an array")

    references: set[str] = set()
    for case_index, case in enumerate(cases):
        evidence = case.get("evidence") if isinstance(case, dict) else None
        if not isinstance(evidence, list):
            raise ValueError(f"Lab 2 case {case_index} evidence must be an array")
        for evidence_index, item in enumerate(evidence):
            reference = item.get("reference") if isinstance(item, dict) else None
            if not isinstance(reference, str) or not reference:
                raise ValueError(
                    f"Lab 2 case {case_index} evidence {evidence_index} needs a reference"
                )
            relative = PurePosixPath(reference)
            if (
                reference != relative.as_posix()
                or relative.is_absolute()
                or "\\" in reference
                or len(relative.parts) < 2
                or relative.parts[0] != "evidence"
                or any(part in {"", ".", ".."} for part in relative.parts)
            ):
                raise ValueError(f"unsafe Lab 2 evidence path: {reference!r}")
            source = LAB02 / "completed" / Path(*relative.parts)
            if not source.is_file() or source.is_symlink():
                raise ValueError(f"missing or linked Lab 2 evidence file: {reference}")
            references.add(reference)
    return tuple(sorted(references))


def lab03_retained_evidence_files() -> tuple[str, ...]:
    """Return only acceptance-record evidence paths safe to ship in Lab 3."""

    record_path = LAB03 / "completed" / "runtime-acceptance.json"
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read Lab 3 acceptance record: {error}") from error

    cases = record.get("cases") if isinstance(record, dict) else None
    if not isinstance(cases, list):
        raise ValueError("Lab 3 acceptance record cases must be an array")

    references: set[str] = set()
    for case_index, case in enumerate(cases):
        evidence = case.get("evidence") if isinstance(case, dict) else None
        if not isinstance(evidence, list):
            raise ValueError(f"Lab 3 case {case_index} evidence must be an array")
        for evidence_index, item in enumerate(evidence):
            reference = item.get("reference") if isinstance(item, dict) else None
            if not isinstance(reference, str) or not reference:
                raise ValueError(
                    f"Lab 3 case {case_index} evidence {evidence_index} needs a reference"
                )
            relative = PurePosixPath(reference)
            if (
                reference != relative.as_posix()
                or relative.is_absolute()
                or "\\" in reference
                or len(relative.parts) < 2
                or relative.parts[0] != "evidence"
                or any(part in {"", ".", ".."} for part in relative.parts)
            ):
                raise ValueError(f"unsafe Lab 3 evidence path: {reference!r}")
            source = LAB03 / "completed" / Path(*relative.parts)
            if not source.is_file() or source.is_symlink():
                raise ValueError(f"missing or linked Lab 3 evidence file: {reference}")
            references.add(reference)
    return tuple(sorted(references))


def lab04_retained_evidence_files() -> tuple[str, ...]:
    """Return only acceptance-record evidence paths safe to ship in Lab 4."""

    record_path = LAB04 / "completed" / "runtime-acceptance.json"
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read Lab 4 acceptance record: {error}") from error

    cases = record.get("cases") if isinstance(record, dict) else None
    if not isinstance(cases, list):
        raise ValueError("Lab 4 acceptance record cases must be an array")

    references: set[str] = set()
    for case_index, case in enumerate(cases):
        evidence = case.get("evidence") if isinstance(case, dict) else None
        if not isinstance(evidence, list):
            raise ValueError(f"Lab 4 case {case_index} evidence must be an array")
        for evidence_index, item in enumerate(evidence):
            reference = item.get("reference") if isinstance(item, dict) else None
            if not isinstance(reference, str) or not reference:
                raise ValueError(
                    f"Lab 4 case {case_index} evidence {evidence_index} needs a reference"
                )
            relative = PurePosixPath(reference)
            if (
                reference != relative.as_posix()
                or relative.is_absolute()
                or "\\" in reference
                or len(relative.parts) < 2
                or relative.parts[0] != "evidence"
                or any(part in {"", ".", ".."} for part in relative.parts)
            ):
                raise ValueError(f"unsafe Lab 4 evidence path: {reference!r}")
            source = LAB04 / "completed" / Path(*relative.parts)
            if not source.is_file() or source.is_symlink():
                raise ValueError(f"missing or linked Lab 4 evidence file: {reference}")
            references.add(reference)
    return tuple(sorted(references))


def lab05_retained_evidence_files() -> tuple[str, ...]:
    """Return only acceptance-record evidence paths safe to ship in Lab 5."""

    record_path = LAB05 / "completed" / "runtime-acceptance.json"
    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read Lab 5 acceptance record: {error}") from error

    cases = record.get("cases") if isinstance(record, dict) else None
    if not isinstance(cases, list):
        raise ValueError("Lab 5 acceptance record cases must be an array")

    references: set[str] = set()
    for case_index, case in enumerate(cases):
        evidence = case.get("evidence") if isinstance(case, dict) else None
        if not isinstance(evidence, list):
            raise ValueError(f"Lab 5 case {case_index} evidence must be an array")
        for evidence_index, item in enumerate(evidence):
            reference = item.get("reference") if isinstance(item, dict) else None
            if not isinstance(reference, str) or not reference:
                raise ValueError(
                    f"Lab 5 case {case_index} evidence {evidence_index} needs a reference"
                )
            relative = PurePosixPath(reference)
            if (
                reference != relative.as_posix()
                or relative.is_absolute()
                or "\\" in reference
                or len(relative.parts) < 2
                or relative.parts[0] != "evidence"
                or any(part in {"", ".", ".."} for part in relative.parts)
            ):
                raise ValueError(f"unsafe Lab 5 evidence path: {reference!r}")
            source = LAB05 / "completed" / Path(*relative.parts)
            if not source.is_file() or source.is_symlink():
                raise ValueError(f"missing or linked Lab 5 evidence file: {reference}")
            references.add(reference)
    return tuple(sorted(references))

LAB01_START_FILES = (
    "CQA_Lab01_OneShot_Start.cpmodproj",
    "README.md",
)
LAB01_START_TEXT_FILES = frozenset(LAB01_START_FILES)
LAB01_COMPLETED_FILES = (
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
LAB01_COMPLETED_TEXT_FILES = frozenset(
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

LAB02_START_FILES = (
    "CQA_Lab02_SignalRace_Start.cpmodproj",
    "README.md",
    "source/archive/mod/cqa/cqa002/journal/cqa002.journal",
    "source/archive/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json",
    "source/archive/mod/cqa/cqa002/phases/cqa002.questphase",
    "source/raw/mod/cqa/cqa002/journal/cqa002.journal.json",
    "source/raw/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json.json",
    "source/raw/mod/cqa/cqa002/phases/cqa002.questphase.json",
    "source/resources/CQA_Lab02_SignalRace_Start.archive.xl",
)
LAB02_START_TEXT_FILES = frozenset(
    {
        "CQA_Lab02_SignalRace_Start.cpmodproj",
        "README.md",
        "source/raw/mod/cqa/cqa002/journal/cqa002.journal.json",
        "source/raw/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json.json",
        "source/raw/mod/cqa/cqa002/phases/cqa002.questphase.json",
        "source/resources/CQA_Lab02_SignalRace_Start.archive.xl",
    }
)
LAB02_COMPLETED_BASE_FILES = (
    "CQA_Lab02_SignalRace.cpmodproj",
    "README.md",
    "example.json",
    "runtime-acceptance.json",
    "source/archive/mod/cqa/cqa002/journal/cqa002.journal",
    "source/archive/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json",
    "source/archive/mod/cqa/cqa002/phases/cqa002.questphase",
    "source/raw/mod/cqa/cqa002/journal/cqa002.journal.json",
    "source/raw/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json.json",
    "source/raw/mod/cqa/cqa002/phases/cqa002.questphase.json",
    "source/resources/CQA_Lab02_SignalRace.archive.xl",
)
LAB02_COMPLETED_FILES = (
    *LAB02_COMPLETED_BASE_FILES,
    *lab02_retained_evidence_files(),
)
LAB02_COMPLETED_TEXT_FILES = frozenset(
    {
        "CQA_Lab02_SignalRace.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        "source/raw/mod/cqa/cqa002/journal/cqa002.journal.json",
        "source/raw/mod/cqa/cqa002/localization/en-us/onscreens/cqa002.json.json",
        "source/raw/mod/cqa/cqa002/phases/cqa002.questphase.json",
        "source/resources/CQA_Lab02_SignalRace.archive.xl",
    }
)

LAB03_START_FILES = (
    "CQA_Lab03_BoundaryCheck_Start.cpmodproj",
    "README.md",
    "source/archive/mod/cqa/cqa003/journal/cqa003.journal",
    "source/archive/mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json",
    "source/archive/mod/cqa/cqa003/phases/cqa003.questphase",
    "source/archive/mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector",
    "source/archive/mod/cqa/cqa003/world/cqa003_boundary.streamingblock",
    "source/archive/mod/cqa/cqa003/world/cqa003_boundary.streamingsector",
    "source/raw/mod/cqa/cqa003/journal/cqa003.journal.json",
    "source/raw/mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json.json",
    "source/raw/mod/cqa/cqa003/phases/cqa003.questphase.json",
    "source/raw/mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector.json",
    "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingblock.json",
    "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingsector.json",
    "source/resources/CQA_Lab03_BoundaryCheck_Start.archive.xl",
)
LAB03_START_TEXT_FILES = frozenset(
    {
        "CQA_Lab03_BoundaryCheck_Start.cpmodproj",
        "README.md",
        "source/raw/mod/cqa/cqa003/journal/cqa003.journal.json",
        "source/raw/mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json.json",
        "source/raw/mod/cqa/cqa003/phases/cqa003.questphase.json",
        "source/raw/mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector.json",
        "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingblock.json",
        "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingsector.json",
        "source/resources/CQA_Lab03_BoundaryCheck_Start.archive.xl",
    }
)
LAB03_COMPLETED_BASE_FILES = (
    "CQA_Lab03_BoundaryCheck.cpmodproj",
    "README.md",
    "example.json",
    "runtime-acceptance.json",
    "source/archive/mod/cqa/cqa003/journal/cqa003.journal",
    "source/archive/mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json",
    "source/archive/mod/cqa/cqa003/phases/cqa003.questphase",
    "source/archive/mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector",
    "source/archive/mod/cqa/cqa003/world/cqa003_boundary.streamingblock",
    "source/archive/mod/cqa/cqa003/world/cqa003_boundary.streamingsector",
    "source/raw/mod/cqa/cqa003/journal/cqa003.journal.json",
    "source/raw/mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json.json",
    "source/raw/mod/cqa/cqa003/phases/cqa003.questphase.json",
    "source/raw/mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector.json",
    "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingblock.json",
    "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingsector.json",
    "source/resources/CQA_Lab03_BoundaryCheck.archive.xl",
)
LAB03_COMPLETED_FILES = (
    *LAB03_COMPLETED_BASE_FILES,
    *lab03_retained_evidence_files(),
)
LAB03_COMPLETED_TEXT_FILES = frozenset(
    {
        "CQA_Lab03_BoundaryCheck.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        "source/raw/mod/cqa/cqa003/journal/cqa003.journal.json",
        "source/raw/mod/cqa/cqa003/localization/en-us/onscreens/cqa003.json.json",
        "source/raw/mod/cqa/cqa003/phases/cqa003.questphase.json",
        "source/raw/mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector.json",
        "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingblock.json",
        "source/raw/mod/cqa/cqa003/world/cqa003_boundary.streamingsector.json",
        "source/resources/CQA_Lab03_BoundaryCheck.archive.xl",
    }
)

LAB04_START_FILES = (
    "CQA_Lab04_HandoffPoint_Start.cpmodproj",
    "README.md",
    "source/archive/mod/cqa/cqa004/journal/cqa004.journal",
    "source/archive/mod/cqa/cqa004/localization/en-us/onscreens/cqa004.json",
    "source/archive/mod/cqa/cqa004/phases/cqa004.questphase",
    "source/archive/mod/cqa/cqa004/phases/cqa004_boundary.questphase",
    "source/archive/mod/cqa/cqa004/world/cqa004_always_loaded.streamingsector",
    "source/archive/mod/cqa/cqa004/world/cqa004_handoff.streamingblock",
    "source/archive/mod/cqa/cqa004/world/cqa004_handoff.streamingsector",
    "source/raw/mod/cqa/cqa004/journal/cqa004.journal.json",
    "source/raw/mod/cqa/cqa004/localization/en-us/onscreens/cqa004.json.json",
    "source/raw/mod/cqa/cqa004/phases/cqa004.questphase.json",
    "source/raw/mod/cqa/cqa004/phases/cqa004_boundary.questphase.json",
    "source/raw/mod/cqa/cqa004/world/cqa004_always_loaded.streamingsector.json",
    "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingblock.json",
    "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingsector.json",
    "source/resources/CQA_Lab04_HandoffPoint_Start.archive.xl",
)
LAB04_START_TEXT_FILES = frozenset(
    {
        "CQA_Lab04_HandoffPoint_Start.cpmodproj",
        "README.md",
        "source/raw/mod/cqa/cqa004/journal/cqa004.journal.json",
        "source/raw/mod/cqa/cqa004/localization/en-us/onscreens/cqa004.json.json",
        "source/raw/mod/cqa/cqa004/phases/cqa004.questphase.json",
        "source/raw/mod/cqa/cqa004/phases/cqa004_boundary.questphase.json",
        "source/raw/mod/cqa/cqa004/world/cqa004_always_loaded.streamingsector.json",
        "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingblock.json",
        "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingsector.json",
        "source/resources/CQA_Lab04_HandoffPoint_Start.archive.xl",
    }
)
LAB04_COMPLETED_BASE_FILES = (
    "CQA_Lab04_HandoffPoint.cpmodproj",
    "README.md",
    "example.json",
    "runtime-acceptance.json",
    "source/archive/mod/cqa/cqa004/journal/cqa004.journal",
    "source/archive/mod/cqa/cqa004/localization/en-us/onscreens/cqa004.json",
    "source/archive/mod/cqa/cqa004/phases/cqa004.questphase",
    "source/archive/mod/cqa/cqa004/phases/cqa004_boundary.questphase",
    "source/archive/mod/cqa/cqa004/world/cqa004_always_loaded.streamingsector",
    "source/archive/mod/cqa/cqa004/world/cqa004_handoff.streamingblock",
    "source/archive/mod/cqa/cqa004/world/cqa004_handoff.streamingsector",
    "source/raw/mod/cqa/cqa004/journal/cqa004.journal.json",
    "source/raw/mod/cqa/cqa004/localization/en-us/onscreens/cqa004.json.json",
    "source/raw/mod/cqa/cqa004/phases/cqa004.questphase.json",
    "source/raw/mod/cqa/cqa004/phases/cqa004_boundary.questphase.json",
    "source/raw/mod/cqa/cqa004/world/cqa004_always_loaded.streamingsector.json",
    "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingblock.json",
    "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingsector.json",
    "source/resources/CQA_Lab04_HandoffPoint.archive.xl",
)
LAB04_COMPLETED_FILES = (
    *LAB04_COMPLETED_BASE_FILES,
    *lab04_retained_evidence_files(),
)
LAB04_COMPLETED_TEXT_FILES = frozenset(
    {
        "CQA_Lab04_HandoffPoint.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        "source/raw/mod/cqa/cqa004/journal/cqa004.journal.json",
        "source/raw/mod/cqa/cqa004/localization/en-us/onscreens/cqa004.json.json",
        "source/raw/mod/cqa/cqa004/phases/cqa004.questphase.json",
        "source/raw/mod/cqa/cqa004/phases/cqa004_boundary.questphase.json",
        "source/raw/mod/cqa/cqa004/world/cqa004_always_loaded.streamingsector.json",
        "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingblock.json",
        "source/raw/mod/cqa/cqa004/world/cqa004_handoff.streamingsector.json",
        "source/resources/CQA_Lab04_HandoffPoint.archive.xl",
    }
)

LAB05_START_FILES = (
    "CQA_Lab05_FirstContact_Start.cpmodproj",
    "README.md",
    "source/archive/mod/cqa/cqa005/journal/cqa005.journal",
    "source/archive/mod/cqa/cqa005/localization/en-us/onscreens/cqa005_onscreens.json",
    "source/archive/mod/cqa/cqa005/localization/en-us/subtitles/cqa005_subtitles.json",
    "source/archive/mod/cqa/cqa005/localization/en-us/subtitles/cqa005_subtitles_map.json",
    "source/archive/mod/cqa/cqa005/localization/en-us/vo/contact_i_85c3283507e7ef2f.wem",
    "source/archive/mod/cqa/cqa005/localization/en-us/vo/cqa005_vo.json",
    "source/archive/mod/cqa/cqa005/phases/cqa005.questphase",
    "source/archive/mod/cqa/cqa005/phases/cqa005_contact.questphase",
    "source/archive/mod/cqa/cqa005/scenes/cqa005_first_contact.scene",
    "source/archive/mod/cqa/cqa005/world/cqa005_always_loaded.streamingsector",
    "source/archive/mod/cqa/cqa005/world/cqa005_first_contact.streamingblock",
    "source/archive/mod/cqa/cqa005/world/cqa005_first_contact.streamingsector",
    "source/raw/mod/cqa/cqa005/journal/cqa005.journal.json",
    "source/raw/mod/cqa/cqa005/localization/en-us/onscreens/cqa005_onscreens.json.json",
    "source/raw/mod/cqa/cqa005/localization/en-us/subtitles/cqa005_subtitles.json.json",
    "source/raw/mod/cqa/cqa005/localization/en-us/subtitles/cqa005_subtitles_map.json.json",
    "source/raw/mod/cqa/cqa005/localization/en-us/vo/cqa005_vo.json.json",
    "source/raw/mod/cqa/cqa005/phases/cqa005.questphase.json",
    "source/raw/mod/cqa/cqa005/phases/cqa005_contact.questphase.json",
    "source/raw/mod/cqa/cqa005/scenes/cqa005_first_contact.scene.json",
    "source/raw/mod/cqa/cqa005/world/cqa005_always_loaded.streamingsector.json",
    "source/raw/mod/cqa/cqa005/world/cqa005_first_contact.streamingblock.json",
    "source/raw/mod/cqa/cqa005/world/cqa005_first_contact.streamingsector.json",
    "source/resources/CQA_Lab05_FirstContact_Start.archive.xl",
)
LAB05_START_TEXT_FILES = frozenset(
    {
        "CQA_Lab05_FirstContact_Start.cpmodproj",
        "README.md",
        "source/raw/mod/cqa/cqa005/journal/cqa005.journal.json",
        "source/raw/mod/cqa/cqa005/localization/en-us/onscreens/cqa005_onscreens.json.json",
        "source/raw/mod/cqa/cqa005/localization/en-us/subtitles/cqa005_subtitles.json.json",
        "source/raw/mod/cqa/cqa005/localization/en-us/subtitles/cqa005_subtitles_map.json.json",
        "source/raw/mod/cqa/cqa005/localization/en-us/vo/cqa005_vo.json.json",
        "source/raw/mod/cqa/cqa005/phases/cqa005.questphase.json",
        "source/raw/mod/cqa/cqa005/phases/cqa005_contact.questphase.json",
        "source/raw/mod/cqa/cqa005/scenes/cqa005_first_contact.scene.json",
        "source/raw/mod/cqa/cqa005/world/cqa005_always_loaded.streamingsector.json",
        "source/raw/mod/cqa/cqa005/world/cqa005_first_contact.streamingblock.json",
        "source/raw/mod/cqa/cqa005/world/cqa005_first_contact.streamingsector.json",
        "source/resources/CQA_Lab05_FirstContact_Start.archive.xl",
    }
)
LAB05_COMPLETED_BASE_FILES = (
    "CQA_Lab05_FirstContact.cpmodproj",
    "README.md",
    "example.json",
    "runtime-acceptance.json",
    *LAB05_START_FILES[2:-1],
    "source/resources/CQA_Lab05_FirstContact.archive.xl",
)
LAB05_COMPLETED_FILES = (
    *LAB05_COMPLETED_BASE_FILES,
    *lab05_retained_evidence_files(),
)
LAB05_COMPLETED_TEXT_FILES = frozenset(
    {
        "CQA_Lab05_FirstContact.cpmodproj",
        "README.md",
        "example.json",
        "runtime-acceptance.json",
        *LAB05_START_TEXT_FILES.difference(
            {
                "CQA_Lab05_FirstContact_Start.cpmodproj",
                "README.md",
                "source/resources/CQA_Lab05_FirstContact_Start.archive.xl",
            }
        ),
        "source/resources/CQA_Lab05_FirstContact.archive.xl",
    }
)
LAB05_VOICE_SOURCE_ENTRIES = (
    (LAB05 / "voice-source" / "README.md", "voice-source/README.md", True),
    (
        LAB05 / "voice-source" / "contact_i_85c3283507e7ef2f.wav",
        "voice-source/contact_i_85c3283507e7ef2f.wav",
        False,
    ),
    (LAB05 / "voice-source" / "provenance.json", "voice-source/provenance.json", True),
)

CHECKPOINTS = {
    "cqa-lab-01-start.zip": (
        LAB01 / "start",
        "CQA_Lab01_OneShot_Start",
        LAB01_START_FILES,
        LAB01_START_TEXT_FILES,
        LAB01 / "LICENSE.md",
        (),
    ),
    "cqa-lab-01-completed.zip": (
        LAB01 / "completed",
        "CQA_Lab01_OneShot",
        LAB01_COMPLETED_FILES,
        LAB01_COMPLETED_TEXT_FILES,
        LAB01 / "LICENSE.md",
        (),
    ),
    "cqa-lab-02-start.zip": (
        LAB02 / "start",
        "CQA_Lab02_SignalRace_Start",
        LAB02_START_FILES,
        LAB02_START_TEXT_FILES,
        LAB02 / "LICENSE.md",
        (),
    ),
    "cqa-lab-02-completed.zip": (
        LAB02 / "completed",
        "CQA_Lab02_SignalRace",
        LAB02_COMPLETED_FILES,
        LAB02_COMPLETED_TEXT_FILES,
        LAB02 / "LICENSE.md",
        (),
    ),
    "cqa-lab-03-start.zip": (
        LAB03 / "start",
        "CQA_Lab03_BoundaryCheck_Start",
        LAB03_START_FILES,
        LAB03_START_TEXT_FILES,
        LAB03 / "LICENSE.md",
        (),
    ),
    "cqa-lab-03-completed.zip": (
        LAB03 / "completed",
        "CQA_Lab03_BoundaryCheck",
        LAB03_COMPLETED_FILES,
        LAB03_COMPLETED_TEXT_FILES,
        LAB03 / "LICENSE.md",
        (),
    ),
    "cqa-lab-04-start.zip": (
        LAB04 / "start",
        "CQA_Lab04_HandoffPoint_Start",
        LAB04_START_FILES,
        LAB04_START_TEXT_FILES,
        LAB04 / "LICENSE.md",
        (),
    ),
    "cqa-lab-04-completed.zip": (
        LAB04 / "completed",
        "CQA_Lab04_HandoffPoint",
        LAB04_COMPLETED_FILES,
        LAB04_COMPLETED_TEXT_FILES,
        LAB04 / "LICENSE.md",
        (),
    ),
    "cqa-lab-05-start.zip": (
        LAB05 / "start",
        "CQA_Lab05_FirstContact_Start",
        LAB05_START_FILES,
        LAB05_START_TEXT_FILES,
        LAB05 / "LICENSE.md",
        LAB05_VOICE_SOURCE_ENTRIES,
    ),
    "cqa-lab-05-completed.zip": (
        LAB05 / "completed",
        "CQA_Lab05_FirstContact",
        LAB05_COMPLETED_FILES,
        LAB05_COMPLETED_TEXT_FILES,
        LAB05 / "LICENSE.md",
        LAB05_VOICE_SOURCE_ENTRIES,
    ),
}
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
    license_path: Path,
    extra_entries: tuple[tuple[Path, str, bool], ...] = (),
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
    for extra_source, relative, is_text in extra_entries:
        posix_relative = PurePosixPath(relative)
        if (
            relative != posix_relative.as_posix()
            or posix_relative.is_absolute()
            or "\\" in relative
            or any(part in {"", ".", ".."} for part in posix_relative.parts)
        ):
            raise ValueError(f"unsafe extra ZIP path: {relative!r}")
        if not extra_source.is_file() or extra_source.is_symlink():
            raise ValueError(f"missing or linked extra ZIP source: {extra_source}")
        result.append((f"{root_name}/{relative}", extra_source, is_text))
    if not license_path.is_file():
        raise ValueError(f"{license_path}: shared checkpoint license is missing")
    result.append((f"{root_name}/LICENSE.md", license_path, True))
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
    license_path: Path,
    destination: Path,
    extra_entries: tuple[tuple[Path, str, bool], ...] = (),
) -> None:
    prepared_entries = entries(
        source,
        root_name,
        expected_files,
        text_files,
        license_path,
        extra_entries,
    )
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
    for name, (
        source,
        root_name,
        expected_files,
        text_files,
        license_path,
        extra_entries,
    ) in CHECKPOINTS.items():
        package(
            source,
            root_name,
            expected_files,
            text_files,
            license_path,
            args.output / name,
            extra_entries,
        )


if __name__ == "__main__":
    main()
