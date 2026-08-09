#!/usr/bin/env python3
"""Validate the Lab 5 community-backed scene example.

The default checks use only the standard library. Pass ``--wkit PATH`` to
repeat the WolvenKit 8.19.0 JSON/CR2W round trip. The package check invokes the
shared deterministic packager twice in temporary output directories.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import Any
from zipfile import ZipFile


sys.dont_write_bytecode = True
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import build_lab05_sources as source_builder  # noqa: E402
from validate_lab04 import (  # noqa: E402
    actual_files,
    cname_value,
    collect_handles,
    decode_outline,
    iter_objects,
    load_json,
    parsed_edges,
    phase_graph,
    require,
    resolve,
    resource_value,
    run_check,
    socket_contract,
)


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-05-first-contact"
START = LAB / "start"
COMPLETED = LAB / "completed"
BUILDER = ROOT / "scripts" / "build_lab05_sources.py"
DIAGRAM_BUILDER = ROOT / "scripts" / "build_lab05_diagrams.py"
PACKAGE_BUILDER = ROOT / "scripts" / "package_examples.py"
ASSETS = ROOT / "assets" / "diagrams" / "lab-05"
PUBLISHED = ROOT / "book" / "src" / "images" / "lab-05"
STATUS_PAGE_RELATIVES = (
    "README.md",
    "book/src/introduction.md",
    "book/src/communities/index.md",
    "book/src/communities/activation-readiness-and-acquisition.md",
    "book/src/communities/entries-phases-and-ai-spots.md",
    "book/src/communities/registries-and-areas.md",
    "book/src/communities/cleanup-and-character-safety.md",
    "book/src/scenes/index.md",
    "book/src/scenes/resource-anatomy.md",
    "book/src/scenes/actors-and-performers.md",
    "book/src/scenes/screenplay-sections-and-events.md",
    "book/src/scenes/one-spoken-line.md",
    "book/src/scenes/entry-exit-and-quest-handoff.md",
    "book/src/scenes/cleanup-and-save-state.md",
    "book/src/scenes/lab-05.md",
    "book/src/scenes/lab-05-authoring.md",
    "book/src/scenes/lab-05-test.md",
    "book/src/reference/evidence-version-matrix.md",
    "examples/lab-05-first-contact/README.md",
    "examples/lab-05-first-contact/start/README.md",
    "examples/lab-05-first-contact/completed/README.md",
)
STATUS_PAGES = tuple(ROOT / relative for relative in STATUS_PAGE_RELATIVES)
GATED_BOOK_RELATIVES = STATUS_PAGE_RELATIVES[2:17]
GATED_BOOK_PAGES = tuple(ROOT / relative for relative in GATED_BOOK_RELATIVES)
GATED_STATUS_NOTE = (
    "**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case "
    "matrix follow the synchronized marker above: pending or failed means "
    "**Experimental**; passed means **Runtime-proven**. Legacy evidence and "
    "out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load "
    "distinct full-slot copies of the named `seed-pre-scene-outside-setup` "
    "capture; those exact loads are in-matrix. Arbitrary or unlisted pre-scene "
    "states and active-line/interruption reload remain out-of-matrix."
)
STALE_GATED_STATUS_FRAGMENTS = (
    "| **Experimental** | The exact `cqa005`",
    "**Experimental:** the exact `cqa005`",
    "| Exact Lab 5 runtime status | **Experimental** — pending |",
    "all exact `cqa005` runtime claims remain **Experimental**",
    "The new `cqa005` combination remains **Experimental**",
    "Exact `cqa005` behavior remains **Experimental**",
    "Its behavior in the exact `cqa005` integration is **Experimental**",
    "All combined `cqa005` runtime behavior remains **Experimental**",
    "all combined runtime behavior remain **Experimental**",
    "eleven-case runtime matrix is still pending",
    "remain **Experimental** until all eleven hash-bound acceptance cases pass",
    "remain **Experimental** pending its retained eleven-case acceptance matrix",
    "Exact runtime behavior remains **Experimental** pending all eleven acceptance cases",
    "remain pending the Lab 5 acceptance record",
    "remain pending Lab 5",
    "remain pending its eleven-case acceptance matrix",
    "have not passed the pinned Lab 5 acceptance record",
    "pre-scene active-child reload",
    "save/reload while the child is active before scene start",
    "saving and reloading while the child is active before scene start",
    "both pre-scene save/reload rows",
)
DATE_PAGES = (
    ROOT / "book" / "src" / "scenes" / "lab-05.md",
    ROOT / "book" / "src" / "scenes" / "lab-05-authoring.md",
    ROOT / "book" / "src" / "scenes" / "lab-05-test.md",
)

BASELINE = {
    "cyberpunk_2077": "2.31a",
    "wolvenkit": "8.19.0",
    "archive_xl": "1.27.0",
    "red4ext": "1.30.0",
    "redscript": "0.5.31",
}

CR2W_PATHS = (
    source_builder.ROOT_PHASE_PATH,
    source_builder.CHILD_PHASE_PATH,
    source_builder.SCENE_PATH,
    source_builder.JOURNAL_PATH,
    source_builder.ONSCREEN_PATH,
    source_builder.SUBTITLES_PATH,
    source_builder.SUBTITLE_MAP_PATH,
    source_builder.VOICE_MAP_PATH,
    source_builder.BLOCK_PATH,
    source_builder.QUEST_SECTOR_PATH,
    source_builder.ALWAYS_SECTOR_PATH,
)
WEM_PATH = source_builder.VOICE_WEM_PATH
ROOT_TYPES = {
    CR2W_PATHS[0]: "questQuestPhaseResource",
    CR2W_PATHS[1]: "questQuestPhaseResource",
    CR2W_PATHS[2]: "scnSceneResource",
    CR2W_PATHS[3]: "gameJournalResource",
    CR2W_PATHS[4]: "JsonResource",
    CR2W_PATHS[5]: "JsonResource",
    CR2W_PATHS[6]: "JsonResource",
    CR2W_PATHS[7]: "JsonResource",
    CR2W_PATHS[8]: "worldStreamingBlock",
    CR2W_PATHS[9]: "worldStreamingSector",
    CR2W_PATHS[10]: "worldStreamingSector",
}
REGISTERED_PATHS = (
    CR2W_PATHS[0],
    CR2W_PATHS[3],
    CR2W_PATHS[4],
    CR2W_PATHS[6],
    CR2W_PATHS[7],
    CR2W_PATHS[8],
)

START_STATIC = {
    "CQA_Lab05_FirstContact_Start.cpmodproj",
    "README.md",
    "source/resources/CQA_Lab05_FirstContact_Start.archive.xl",
}
COMPLETED_STATIC = {
    "CQA_Lab05_FirstContact.cpmodproj",
    "README.md",
    "example.json",
    "runtime-acceptance.json",
    "source/resources/CQA_Lab05_FirstContact.archive.xl",
}
ASSET_FILES = {
    "cqa005.questphase.layout.json",
    "cqa005_contact.questphase.layout.json",
    "cqa005.root.questphase.svg",
    "cqa005.child.questphase.svg",
    "cqa005.scene.svg",
    "cqa005.community-identity.svg",
    "cqa005.resource-chain.svg",
    "cqa005.lifecycle.svg",
    "cqa005.trigger-volume-plan.svg",
}
PUBLISHED_FILES = {name for name in ASSET_FILES if name.endswith(".svg")}
VOICE_FILES = {
    "README.md",
    "provenance.json",
    "contact_i_85c3283507e7ef2f.wav",
}
WAV_SHA256 = "ca63bdebd64a1312f53a4fe04f381b97cd9b3e11c04c19b815a503b0b5a11110"
WEM_SHA256 = "0487ba1116d9c4fa9cfb25e825ad4ec35110195cf3953cb8bc67a16f5cbc657f"
EVIDENCE_TYPES = {"screenshot", "video", "log", "save-metadata", "notes"}
WINDOWS_RESERVED_NAMES = {
    "aux",
    "con",
    "nul",
    "prn",
    *(f"com{index}" for index in range(1, 10)),
    *(f"lpt{index}" for index in range(1, 10)),
}

ROOT_COMPLETED_TYPES = {
    0: "questInputNodeDefinition",
    1: "questOutputNodeDefinition",
    10: "questConditionNodeDefinition",
    11: "questJournalNodeDefinition",
    12: "questPhaseNodeDefinition",
    13: "questJournalNodeDefinition",
    14: "questFactsDBManagerNodeDefinition",
}
ROOT_COMPLETED_EDGES = {
    (0, "Out", 10, "In"),
    (10, "False", 1, "In"),
    (10, "True", 11, "Active"),
    (11, "Out", 12, "In1"),
    (12, "Out1", 13, "Succeeded"),
    (13, "Out", 14, "In"),
    (14, "Out", 1, "In"),
}
CHILD_COMPLETED_TYPES = {
    0: "questInputNodeDefinition",
    1: "questOutputNodeDefinition",
    10: "questJournalNodeDefinition",
    11: "questMappinManagerNodeDefinition",
    12: "questSpawnManagerNodeDefinition",
    13: "questPauseConditionNodeDefinition",
    14: "questPauseConditionNodeDefinition",
    15: "questCheckpointNodeDefinition",
    16: "questSceneNodeDefinition",
    17: "questJournalNodeDefinition",
    18: "questMappinManagerNodeDefinition",
    19: "questJournalNodeDefinition",
    20: "questPauseConditionNodeDefinition",
    21: "questSpawnManagerNodeDefinition",
    22: "questJournalNodeDefinition",
}
CHILD_COMPLETED_EDGES = {
    (0, "Out", 10, "Active"),
    (10, "Out", 11, "Active"),
    (11, "Out", 12, "In"),
    (12, "Out", 13, "In"),
    (13, "Out", 14, "In"),
    (14, "Out", 15, "In"),
    (15, "Out", 16, "start"),
    (16, "contact_done", 17, "Succeeded"),
    (17, "Out", 18, "Inactive"),
    (18, "Out", 19, "Active"),
    (19, "Out", 20, "In"),
    (20, "Out", 21, "In"),
    (21, "Out", 22, "Succeeded"),
    (22, "Out", 1, "In"),
}

SAVE_CAPTURE_CONTRACT = {
    "original-outside-setup": {
        "source_run_id": None,
        "parent_capture_id": None,
        "label": "CQA005 ORIGINAL OUTSIDE SETUP",
        "observable_state": "V is outside the cqa005 setup volume on the ordinary approach route, and this save has never loaded any CQA Lab 1–5 candidate.",
        "created_before_first_install": True,
    },
    "original-near-setup": {
        "source_run_id": None,
        "parent_capture_id": None,
        "label": "CQA005 ORIGINAL NEAR SETUP",
        "observable_state": "V is near but outside the cqa005 setup volume, and this separate save has never loaded any CQA Lab 1–5 candidate.",
        "created_before_first_install": True,
    },
    "seed-pre-scene-outside-setup": {
        "source_run_id": "clean-ordinary-passive-spawn",
        "parent_capture_id": "original-outside-setup",
        "label": "CQA005 SEED PRE SCENE OUTSIDE SETUP",
        "observable_state": "Meet is Active, its pin is Active, the child is active, the contact is spawned and passive, V is outside setup, checkpoint cqa005_first_contact has not executed, the scene has not started, and cqa005_completed is 0.",
        "created_before_first_install": False,
    },
    "seed-post-contact-inside-cleanup": {
        "source_run_id": "clean-ordinary-passive-spawn",
        "parent_capture_id": "seed-pre-scene-outside-setup",
        "label": "CQA005 SEED POST CONTACT INSIDE CLEANUP",
        "observable_state": "contact_done has returned, Meet is Succeeded, its pin is Inactive, Leave is Active, the child and contact are active, V is inside cleanup, and cqa005_completed is 0.",
        "created_before_first_install": False,
    },
    "seed-completed": {
        "source_run_id": "clean-ordinary-passive-spawn",
        "parent_capture_id": "seed-post-contact-inside-cleanup",
        "label": "CQA005 SEED COMPLETED",
        "observable_state": "Leave and the quest are Succeeded, the pin is Inactive, the contact is deactivated, the child and root have returned, and cqa005_completed is 1.",
        "created_before_first_install": False,
    },
}
CAPTURE_RUN_GROUPS = {
    "original-outside-setup": ("clean-ordinary-passive-spawn", "untouched-replay"),
    "original-near-setup": ("fast-arrival-race",),
    "seed-pre-scene-outside-setup": ("slow-contact-av-once", "named-exit-only", "stream-away-return"),
    "seed-post-contact-inside-cleanup": ("no-replay-inside-lifetime", "post-scene-reload", "cleanup-boundary-no-pop"),
    "seed-completed": ("completed-reload", "removal-isolation-diagnostic"),
}
RUN_CONTRACT = {
    "clean-ordinary-passive-spawn": ("untouched-preinstall-outside-setup", "canonical-original", "original-outside-setup"),
    "fast-arrival-race": ("untouched-preinstall-near-setup", "canonical-original", "original-near-setup"),
    "slow-contact-av-once": ("clean-derived-before-setup", "canonical-clean-derived", "seed-pre-scene-outside-setup"),
    "named-exit-only": ("clean-derived-before-scene", "canonical-clean-derived", "seed-pre-scene-outside-setup"),
    "no-replay-inside-lifetime": ("clean-derived-after-contact-inside-cleanup", "canonical-clean-derived", "seed-post-contact-inside-cleanup"),
    "post-scene-reload": ("contact-done-inside-cleanup", "canonical-clean-derived", "seed-post-contact-inside-cleanup"),
    "stream-away-return": ("child-active-before-setup", "canonical-clean-derived", "seed-pre-scene-outside-setup"),
    "cleanup-boundary-no-pop": ("contact-done-inside-cleanup", "canonical-clean-derived", "seed-post-contact-inside-cleanup"),
    "completed-reload": ("completed", "canonical-completed", "seed-completed"),
    "untouched-replay": ("untouched-preinstall-outside-setup", "canonical-original", "original-outside-setup"),
    "removal-isolation-diagnostic": ("completed-disposable-clone-before-removal", "canonical-completed-diagnostic-clone", "seed-completed"),
}

CASE_CONTRACT = {
    "clean-ordinary-passive-spawn": (
        "Install the canonical candidate, load a closed-game full-slot clone of the untouched outside-setup original, approach by ordinary movement, and continue the same unbroken route through ordinary completion while making the three named manual seed saves.",
        "The root and child activate once, the passive community contact appears through the community/AI-spot mapping, the meet objective and pin appear once without a spawn or NodeRef error, the ordinary route completes once, and exactly the pre-scene, post-contact, and completed seed captures are made at their frozen observable states.",
    ),
    "fast-arrival-race": (
        "Load a closed-game full-slot clone of the separate untouched near-setup original and enter immediately before waiting for streaming or spawn.",
        "The spawned-character wait resolves before the setup wait advances; the scene begins once only after the contact exists, with no missed trigger or deadlock.",
    ),
    "slow-contact-av-once": (
        "Load a byte-identical full-slot clone of the named pre-scene outside-setup seed, approach slowly, remain in range for the full scene, and do not skip or interrupt it.",
        "The exact subtitle `All clear. Keep moving.` and the hash-pinned WEM play once; the contact is acquired, the line does not duplicate, and lipsync/audio errors are absent from retained logs.",
    ),
    "named-exit-only": (
        "Load a byte-identical full-slot clone of the same named pre-scene outside-setup seed used by Cases 3 and 7, then observe ordinary completion; this is not a save between checkpoint node 15 and scene node 16.",
        "Only named exit `contact_done` advances the child to meet Succeeded; Default INT/RET remain unwired and no fallback continuation is observed.",
    ),
    "no-replay-inside-lifetime": (
        "Load a byte-identical full-slot clone of the named post-contact inside-cleanup seed, then cross the setup boundary or revisit the contact point before leaving cleanup.",
        "The scene, subtitle, and WEM do not replay during the same child lifetime; the leave objective remains the only active progression state.",
    ),
    "post-scene-reload": (
        "Without changing the installation, load a byte-identical full-slot clone of the named post-contact inside-cleanup seed.",
        "Meet stays succeeded, the pin stays inactive, leave stays active, the contact line does not replay, and crossing cleanup continues once.",
    ),
    "stream-away-return": (
        "Load a byte-identical full-slot clone of the named pre-scene outside-setup seed, travel by ordinary movement beyond the finite Quest descriptor box before entering setup, return, and finish.",
        "The community and child remain coherent across streaming; returning resolves the same NodeRefs and advances the scene exactly once without duplicate contact entries.",
    ),
    "cleanup-boundary-no-pop": (
        "Load a byte-identical full-slot clone of the named post-contact inside-cleanup seed, then walk outward continuously through the cleanup boundary more than 110 metres from the shared center.",
        "IsOutside resolves once, whole-community deactivation occurs only at cleanup, no visible contact pop occurs inside the cleanup volume, leave succeeds, and child Out1 returns once.",
    ),
    "completed-reload": (
        "With the same exact candidate installed, load a byte-identical full-slot clone of the named completed seed.",
        "cqa005_completed bypasses the child; objectives, pin, community, scene, subtitle, and WEM do not reactivate or replay.",
    ),
    "untouched-replay": (
        "With the canonical candidate still installed, load a byte-identical full-slot clone of the same untouched outside-setup original used by Case 1 and repeat the ordinary route.",
        "Spawn, acquisition, line, named exit, cleanup, child return, and root completion reproduce once with the same visible and logged behavior.",
    ),
    "removal-isolation-diagnostic": (
        "With the game closed, clone the named completed seed into the disposable execution slot, remove both exact candidate files before launching and loading that clone, and revisit the site without resetting any fact.",
        "No mod-owned resource remains mounted, no Lab 5 objective or pin reactivates, no cqa005 contact appears, fresh logs show no cqa005 registration, and the packaged fixture contains no TweakDB mutation or override.",
    ),
}
PROMOTION_RULE = (
    "Set status to passed and evidence_class to runtime-proven only when all "
    "eleven required cases pass and evidence binds the exact candidate build, "
    "both immutable original captures, all three manual Case-1 seed captures, "
    "every closed-game full-slot execution clone, exact versions, visible "
    "observations, the canonical WEM hash, and all four logs for the complete "
    "campaign. Structural round trips alone never promote the combined cqa005 "
    "fixture."
)


def raw_relative(depot_path: str) -> str:
    return "source/raw/" + depot_path.replace("\\", "/") + ".json"


def cooked_relative(depot_path: str) -> str:
    return "source/archive/" + depot_path.replace("\\", "/")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_sha256_value(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def parse_offset_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.utcoffset() is not None else None


def is_offset_timestamp(value: Any) -> bool:
    return parse_offset_timestamp(value) is not None


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
        cursor = cursor / part
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


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def retained_evidence_files() -> set[str]:
    record = load_json(COMPLETED / "runtime-acceptance.json")
    references: set[str] = set()
    for case_index, case in enumerate(record.get("cases", [])):
        evidence = case.get("evidence") if isinstance(case, dict) else None
        require(isinstance(evidence, list), f"acceptance case {case_index}: evidence must be an array")
        for evidence_index, item in enumerate(evidence):
            label = f"acceptance case {case_index} evidence {evidence_index}"
            require(
                isinstance(item, dict)
                and set(item) == {"type", "reference", "sha256"}
                and item["type"] in EVIDENCE_TYPES,
                f"{label}: expected exact type/reference/sha256 object",
            )
            reference = item["reference"]
            require(reference not in references, f"{label}: duplicate evidence reference {reference!r}")
            source = safe_evidence_path(reference, label=label)
            require(is_sha256_value(item["sha256"]), f"{label}: invalid lowercase SHA-256")
            require(sha256(source) == item["sha256"], f"{label}: retained evidence SHA-256 mismatch")
            if item["type"] == "save-metadata":
                require(source.suffix.casefold() in {".md", ".txt", ".json"}, f"{label}: save metadata must be sanitized text")
            references.add(reference)
    return references


def expected_checkpoint_files(*, completed: bool) -> set[str]:
    paired = {raw_relative(path) for path in CR2W_PATHS} | {
        cooked_relative(path) for path in CR2W_PATHS
    }
    paired.add(cooked_relative(WEM_PATH))
    return paired | (COMPLETED_STATIC | retained_evidence_files() if completed else START_STATIC)


def generate_into(root: Path, name: str) -> None:
    module = load_module(BUILDER, name)
    module.CHECKPOINTS = {"start": root / "start", "completed": root / "completed"}
    module.main()


def validate_inventories_and_generation() -> None:
    start_files = actual_files(START)
    completed_files = actual_files(COMPLETED)
    require(start_files == expected_checkpoint_files(completed=False), "Lab 5 start inventory changed")
    require(completed_files == expected_checkpoint_files(completed=True), "Lab 5 completed inventory changed")
    for checkpoint, files in ((START, start_files), (COMPLETED, completed_files)):
        require(
            not any(
                relative.casefold().startswith(("r6/tweaks/", "r6/scripts/"))
                or PurePosixPath(relative).suffix.casefold() in {".yaml", ".yml", ".reds"}
                for relative in files
            ),
            f"{checkpoint.name}: fixture introduced a TweakDB or script mutation source",
        )
    require(actual_files(LAB / "voice-source") == VOICE_FILES, "Lab 5 voice-source inventory changed")
    require(actual_files(ASSETS) == ASSET_FILES, "Lab 5 diagram-source inventory changed")
    require(actual_files(PUBLISHED) == PUBLISHED_FILES, "Lab 5 published-diagram inventory changed")

    with tempfile.TemporaryDirectory(prefix="cqa-lab05-a-") as first_dir, tempfile.TemporaryDirectory(prefix="cqa-lab05-b-") as second_dir:
        first = Path(first_dir)
        second = Path(second_dir)
        generate_into(first, "cqa_build_lab05_a")
        generate_into(second, "cqa_build_lab05_b")
        expected_raw = {f"{checkpoint}/{raw_relative(path)}" for checkpoint in ("start", "completed") for path in CR2W_PATHS}
        require(actual_files(first) == expected_raw == actual_files(second), "Lab 5 generator raw inventory changed")
        for relative in sorted(expected_raw):
            generated_a = first / relative
            generated_b = second / relative
            checked = LAB / relative
            require(generated_a.read_bytes() == generated_b.read_bytes(), f"{relative}: generation is nondeterministic")
            require(generated_a.read_bytes() == checked.read_bytes(), f"{relative}: checked source is stale")
            require(str(ROOT).encode() not in generated_a.read_bytes(), f"{relative}: generated source contains an absolute path")


def archive_xl_text() -> str:
    return """quest:
  phases:
  - path: mod\\cqa\\cqa005\\phases\\cqa005.questphase
    parent: base\\quest\\cyberpunk2077.quest

journal:
- mod\\cqa\\cqa005\\journal\\cqa005.journal

localization:
  onscreens:
    en-us:
    - mod\\cqa\\cqa005\\localization\\en-us\\onscreens\\cqa005_onscreens.json
  subtitles:
    en-us:
    - mod\\cqa\\cqa005\\localization\\en-us\\subtitles\\cqa005_subtitles_map.json
  vomaps:
    en-us:
    - mod\\cqa\\cqa005\\localization\\en-us\\vo\\cqa005_vo.json

streaming:
  blocks:
  - mod\\cqa\\cqa005\\world\\cqa005_first_contact.streamingblock
"""


def validate_projects_registration_and_pairs() -> None:
    for checkpoint, project_name, mod_name, archive_name in (
        (START, "CQA Lab 05 First Contact Start", "CQA_Lab05_FirstContact_Start", "CQA_Lab05_FirstContact_Start.archive.xl"),
        (COMPLETED, "CQA Lab 05 First Contact", "CQA_Lab05_FirstContact", "CQA_Lab05_FirstContact.archive.xl"),
    ):
        project = checkpoint / f"{mod_name}.cpmodproj"
        root = ET.parse(project).getroot()
        values = {child.tag: child.text for child in root}
        require(root.tag == "CP77Mod" and values.get("Name") == project_name and values.get("ModName") == mod_name, f"{project.name}: project identity changed")
        manifest = checkpoint / "source" / "resources" / archive_name
        content = manifest.read_text(encoding="utf-8")
        require(content == archive_xl_text(), f"{archive_name}: registration changed")
        require("vomaps:" in content and "voiceovers:" not in content, f"{archive_name}: VO registration key changed")
        for indirect in (CR2W_PATHS[1], CR2W_PATHS[2], CR2W_PATHS[5], WEM_PATH, CR2W_PATHS[9], CR2W_PATHS[10]):
            require(indirect not in content, f"{archive_name}: indirect resource was registered: {indirect}")

        for depot_path, root_type in ROOT_TYPES.items():
            raw = checkpoint / raw_relative(depot_path)
            cooked = checkpoint / cooked_relative(depot_path)
            source = load_json(raw)
            header = source["Header"]
            chunk = source["Data"]["RootChunk"]
            require(header.get("WolvenKitVersion") == "8.19.0" and header.get("WKitJsonVersion") == "0.0.9" and header.get("GameVersion") == 2310 and header.get("DataType") == "CR2W" and header.get("ArchiveFileName") == depot_path, f"{raw}: header/depot path changed")
            require(chunk.get("$type") == root_type, f"{raw}: root type changed")
            payload = cooked.read_bytes()
            require(payload.startswith(b"CR2W") and root_type.encode("ascii") in payload, f"{cooked}: cooked CR2W provenance changed")
            handles: dict[str, dict[str, Any]] = {}
            collect_handles(source, handles)
            for item in iter_objects(source):
                reference = item.get("HandleRefId")
                if reference is not None:
                    require(reference in handles, f"{raw}: unresolved handle {reference}")

    for changed_path in CR2W_PATHS[:3]:
        require((START / cooked_relative(changed_path)).read_bytes() != (COMPLETED / cooked_relative(changed_path)).read_bytes(), f"{changed_path}: start/completed resources must differ")
    for shared_path in CR2W_PATHS[3:]:
        require((START / cooked_relative(shared_path)).read_bytes() == (COMPLETED / cooked_relative(shared_path)).read_bytes(), f"{shared_path}: shared checkpoint resource drifted")


def expected_socket_names(red_type: str) -> list[tuple[str, str]]:
    contracts = {
        "questInputNodeDefinition": [("CutDestination", "CutDestination"), ("Out", "Output")],
        "questOutputNodeDefinition": [("CutDestination", "CutDestination"), ("In", "Input")],
        "questConditionNodeDefinition": [("CutDestination", "CutDestination"), ("In", "Input"), ("True", "Output"), ("False", "Output")],
        "questJournalNodeDefinition": [("CutDestination", "CutDestination"), ("Active", "Input"), ("Inactive", "Input"), ("Succeeded", "Input"), ("Failed", "Input"), ("Out", "Output")],
        "questMappinManagerNodeDefinition": [("CutDestination", "CutDestination"), ("Active", "Input"), ("Inactive", "Input"), ("Out", "Output")],
        "questPhaseNodeDefinition": [("CutDestination", "CutDestination"), ("In1", "Input"), ("Out1", "Output")],
        "questSceneNodeDefinition": [("CutDestination", "CutDestination"), ("start", "Input"), ("contact_done", "Output"), ("Default INT", "Output"), ("Default RET", "Output")],
    }
    return contracts.get(red_type, [("CutDestination", "CutDestination"), ("In", "Input"), ("Out", "Output")])


def validate_phase(path: Path, expected_types: dict[int, str], expected_edges: set[tuple[int, str, int, str]], prefabs: list[str]) -> tuple[dict[int, dict[str, Any]], dict[str, dict[str, Any]]]:
    source = load_json(path)
    root, nodes, handles = phase_graph(source)
    require({node_id: node["$type"] for node_id, node in nodes.items()} == expected_types, f"{path.name}: node contract changed")
    require(parsed_edges(path) == expected_edges, f"{path.name}: edge contract changed")
    require([item["prefabNodeRef"]["$value"] for item in root["phasePrefabs"]] == prefabs and root["inplacePhases"] == [], f"{path.name}: prefab scope changed")
    connection_count = 0
    for node_id, node in nodes.items():
        sockets = socket_contract(node, handles)
        require([(name, kind) for name, kind, _ in sockets] == expected_socket_names(node["$type"]), f"{path.name} node {node_id}: sockets changed")
        require(next(count for name, _, count in sockets if name == "CutDestination") == 0, f"{path.name} node {node_id}: CutDestination became wired")
        connection_count += sum(count for _, kind, count in sockets if kind == "Output")
    require(connection_count == len(expected_edges), f"{path.name}: duplicate or extra edge changed the graph")
    require(cname_value(nodes[0]["socketName"]) == "In1" and cname_value(nodes[1]["socketName"]) == "Out1" and nodes[1]["type"] == "Terminating", f"{path.name}: boundary names/types changed")
    return nodes, handles


def find_type(value: Any, red_type: str, handles: dict[str, dict[str, Any]]) -> dict[str, Any]:
    for item in iter_objects(value):
        identifier = item.get("HandleRefId", item.get("HandleId"))
        candidate = handles.get(identifier, item) if isinstance(identifier, str) else item
        if candidate.get("$type") == red_type:
            return candidate
    raise RuntimeError(f"missing {red_type}")


def require_journal_path(
    node: dict[str, Any],
    handles: dict[str, dict[str, Any]],
    *,
    real_path: str,
    class_name: str,
) -> None:
    path = find_type(node, "gameJournalPath", handles)
    require(
        path
        == {
            "$type": "gameJournalPath",
            "className": {"$type": "CName", "$storage": "string", "$value": class_name},
            "editorPath": "",
            "fileEntryIndex": 2,
            "realPath": real_path,
        },
        f"journal path contract changed: {real_path}",
    )


def validate_graphs() -> None:
    start_root_path = START / raw_relative(CR2W_PATHS[0])
    start_child_path = START / raw_relative(CR2W_PATHS[1])
    completed_root_path = COMPLETED / raw_relative(CR2W_PATHS[0])
    completed_child_path = COMPLETED / raw_relative(CR2W_PATHS[1])
    start_root, _ = validate_phase(start_root_path, {0: "questInputNodeDefinition", 1: "questOutputNodeDefinition", 13: "questPhaseNodeDefinition"}, {(0, "Out", 13, "In1"), (13, "Out1", 1, "In")}, [source_builder.PREFAB_LOCAL])
    start_child, _ = validate_phase(start_child_path, {0: "questInputNodeDefinition", 1: "questOutputNodeDefinition"}, {(0, "Out", 1, "In")}, [])
    require(not any(node["$type"] == "questSceneNodeDefinition" for node in (*start_root.values(), *start_child.values())), "start phase graphs invoke the scene shell")
    root_nodes, root_handles = validate_phase(completed_root_path, ROOT_COMPLETED_TYPES, ROOT_COMPLETED_EDGES, [source_builder.PREFAB_LOCAL])
    child_nodes, child_handles = validate_phase(completed_child_path, CHILD_COMPLETED_TYPES, CHILD_COMPLETED_EDGES, [])

    for node_id in (13, 12):
        node = start_root[node_id] if node_id == 13 else root_nodes[node_id]
        require(node["phaseGraph"] is None and node["phaseInstancePrefabs"] == [] and resource_value(node["phaseResource"]) == (source_builder.CHILD_PHASE_PATH, "Soft") and node["saveLock"] == 0 and node["unfreezingTriggerNodeRef"]["$value"] == "0", f"external phase node {node_id}: payload changed")
    comparison = find_type(root_nodes[10], "questVarComparison_ConditionType", root_handles)
    require(comparison == {"$type": "questVarComparison_ConditionType", "comparisonType": "Equal", "factName": "cqa005_completed", "value": 0}, "root completion guard changed")
    set_fact = find_type(root_nodes[14], "questSetVar_NodeType", root_handles)
    require(set_fact == {"$type": "questSetVar_NodeType", "factName": "cqa005_completed", "setExactValue": 1, "value": 1}, "root fact write changed")
    for node_id in (11, 13):
        journal_action = find_type(root_nodes[node_id], "questJournalQuestEntry_NodeType", root_handles)
        require(
            {key: journal_action[key] for key in ("optional", "sendNotification", "trackQuest", "version")}
            == {"optional": 0, "sendNotification": 1, "trackQuest": 1, "version": "Initial"},
            f"root journal node {node_id}: action flags changed",
        )
        require_journal_path(
            root_nodes[node_id],
            root_handles,
            real_path="quests/minor_quest/cqa005",
            class_name="gameJournalQuest",
        )
    require(
        (13, "Out", 14, "In") in ROOT_COMPLETED_EDGES
        and (14, "Out", 1, "In") in ROOT_COMPLETED_EDGES
        and (10, "False", 1, "In") in ROOT_COMPLETED_EDGES,
        "root fact/journal ordering contract changed",
    )

    activate = find_type(child_nodes[12], "questCommunityTemplate_NodeType", child_handles)
    deactivate = find_type(child_nodes[21], "questCommunityTemplate_NodeType", child_handles)
    require((activate["action"], cname_value(activate["communityEntryName"]), cname_value(activate["communityEntryPhaseName"]), activate["spawnerReference"]["$value"]) == ("Activate", "contact", "default", source_builder.COMMUNITY_LOCAL), "community activation changed")
    require((deactivate["action"], cname_value(deactivate["communityEntryName"]), cname_value(deactivate["communityEntryPhaseName"]), deactivate["spawnerReference"]["$value"]) == ("Deactivate", "None", "None", source_builder.COMMUNITY_LOCAL), "whole-community deactivation changed")
    spawned = find_type(child_nodes[13], "questCharacterSpawned_ConditionType", child_handles)
    comparison_params = resolve(spawned["comparisonParams"], child_handles)
    require(comparison_params == {"$type": "questComparisonParam", "comparisonType": "Greater", "count": 0, "entireCommunity": 1} and spawned["objectRef"]["reference"]["$value"] == source_builder.COMMUNITY_LOCAL, "spawn readiness condition changed")
    empty_activator = {
        "$type": "gameEntityReference",
        "dynamicEntityUniqueName": {"$type": "CName", "$storage": "string", "$value": "None"},
        "names": [],
        "reference": {"$type": "NodeRef", "$storage": "uint64", "$value": "0"},
        "sceneActorContextName": {"$type": "CName", "$storage": "string", "$value": "None"},
        "slotName": {"$type": "CName", "$storage": "string", "$value": "None"},
        "type": "EntityRef",
    }
    for node_id, trigger_ref, condition_type in ((14, source_builder.SETUP_LOCAL, "IsInside"), (20, source_builder.CLEANUP_LOCAL, "IsOutside")):
        condition = find_type(child_nodes[node_id], "questTriggerCondition", child_handles)
        require(condition["activatorRef"] == empty_activator and condition["isPlayerActivator"] == 1 and condition["triggerAreaRef"]["$value"] == trigger_ref and condition["type"] == condition_type, f"child trigger node {node_id} changed")
    require(child_nodes[15]["debugString"] == "cqa005_first_contact" and all(child_nodes[15][field] == 0 for field in ("endGameSave", "ignoreSaveLocks", "pointOfNoReturn", "retryOnFailure", "saveLock")), "checkpoint payload changed")
    for node_id, real_path in (
        (10, "quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_meet"),
        (17, "quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_meet"),
        (19, "quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_leave"),
        (22, "quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_leave"),
    ):
        journal_action = find_type(child_nodes[node_id], "questJournalQuestEntry_NodeType", child_handles)
        require(
            {key: journal_action[key] for key in ("optional", "sendNotification", "trackQuest", "version")}
            == {"optional": 0, "sendNotification": 1, "trackQuest": 1, "version": "Initial"},
            f"child journal node {node_id}: action flags changed",
        )
        require_journal_path(
            child_nodes[node_id],
            child_handles,
            real_path=real_path,
            class_name="gameJournalQuestObjective",
        )
    for node_id in (11, 18):
        require(child_nodes[node_id]["disablePreviousMappins"] == 0, f"mappin node {node_id}: disablePreviousMappins changed")
        require_journal_path(
            child_nodes[node_id],
            child_handles,
            real_path="quests/minor_quest/cqa005/cqa005_01/cqa005_01_obj_meet/cqa005_01_qmp_contact",
            class_name="gameJournalQuestMapPin",
        )
    scene_node = child_nodes[16]
    require(
        len(scene_node["sockets"]) == 5
        and resource_value(scene_node["sceneFile"])
        == ("mod\\cqa\\cqa005\\scenes\\cqa005_first_contact.scene", "Soft")
        and scene_node["sceneLocation"]
        == {
            "$type": "scnWorldMarker",
            "nodeRef": {"$type": "NodeRef", "$storage": "string", "$value": "#cqa005_sm_contact"},
            "tag": {"$type": "CName", "$storage": "string", "$value": "None"},
            "type": "NodeRef",
        }
        and scene_node["interruptionOperations"] == []
        and scene_node["notAllowedToBeFrozen"] == 0
        and scene_node["reapplyInterruptionOperationsAfterGameLoad"] == 0
        and scene_node["syncToMusic"] == 0,
        "quest scene node flags/marker contract changed",
    )


def scene_graph(root: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, dict[str, Any]]]:
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(root, handles)
    graph = resolve(root["sceneGraph"], handles)
    nodes = [resolve(item, handles) for item in graph["graph"]]
    return graph, nodes, handles


def scene_edges(nodes: list[dict[str, Any]]) -> list[tuple[int, int, int, int, int]]:
    result = []
    for node in nodes:
        source_id = int(node["nodeId"]["id"])
        for output in node.get("outputSockets", []):
            stamp = output["stamp"]
            for destination in output["destinations"]:
                target = destination["isockStamp"]
                result.append((source_id, int(stamp["name"]), int(destination["nodeId"]["id"]), int(target["name"]), int(target["ordinal"])))
    return result


def validate_scenes_and_localization() -> None:
    roots = {}
    for checkpoint in (START, COMPLETED):
        source = load_json(checkpoint / raw_relative(CR2W_PATHS[2]))
        root = source["Data"]["RootChunk"]
        root_handles: dict[str, dict[str, Any]] = {}
        collect_handles(root, root_handles)
        roots[checkpoint.name] = root
        require(root["version"] == 5 and root["cookingPlatform"] == "PLATFORM_PC" and root["sceneCategoryTag"] == "minorQuests", f"{checkpoint.name}: scene baseline changed")
        for field in ("effectDefinitions", "effectInstances", "executionTagEntries", "executionTags", "localMarkers", "notablePoints", "props", "referencePoints", "ridResources", "voInfo", "workspotInstances", "workspots"):
            require(root[field] == [], f"{checkpoint.name}: scene scaffold {field} changed")
        require("resouresReferences" in root and "resourcesReferences" not in root, f"{checkpoint.name}: serialized misspelling changed")
        require(len(root["actors"]) == len(root["playerActors"]) == 1, f"{checkpoint.name}: actor/player cardinality changed")
        actor = root["actors"][0]
        player = root["playerActors"][0]
        require(actor["actorId"]["id"] == 0 and actor["acquisitionPlan"] == "community" and actor["actorName"] == "contact" and actor["communityParams"]["reference"]["$value"] == source_builder.COMMUNITY_LOCAL and cname_value(actor["communityParams"]["entryName"]) == "contact", f"{checkpoint.name}: community actor changed")
        require(actor["communityParams"] == {"$type": "scnCommunityParams", "entryName": {"$type": "CName", "$storage": "string", "$value": "contact"}, "forceMaxVisibility": 0, "reference": {"$type": "NodeRef", "$storage": "string", "$value": "#cqa005_com_contact"}}, f"{checkpoint.name}: typed community acquisition params changed")
        require(player["actorId"]["id"] == 1 and player["acquisitionPlan"] == "findInContext" and player["playerName"] == "V" and player["findActorInContextParams"]["specRecordId"] == {"$type": "TweakDBID", "$storage": "string", "$value": "Character.Player_Puppet_Base"} and player["specCharacterRecordId"] == {"$type": "TweakDBID", "$storage": "string", "$value": "Character.Player_Puppet_Base"}, f"{checkpoint.name}: player actor/TweakDBID changed")
        require(actor["lipsyncAnimSet"] == {"$type": "scnLipsyncAnimSetSRRefId", "id": 0} and player["lipsyncAnimSet"] == {"$type": "scnLipsyncAnimSetSRRefId", "id": 0}, f"{checkpoint.name}: actor lipsync slots changed")
        performers = root["debugSymbols"]["performersDebugSymbols"]
        require([item["performerId"]["id"] for item in performers] == [1, 257] and performers[0]["entityRef"]["reference"]["$value"] == source_builder.COMMUNITY_LOCAL and [cname_value(item) for item in performers[0]["entityRef"]["names"]] == ["contact"] and performers[0]["entityRef"]["$type"] == "gameEntityReference" and performers[1]["entityRef"]["reference"]["$value"] == "#player" and performers[1]["entityRef"]["names"] == [], f"{checkpoint.name}: performer debug mapping changed")
        require(root["debugSymbols"]["$type"] == "scnDebugSymbols" and all(root["debugSymbols"][field] == [] for field in ("sceneEventsDebugSymbols", "sceneNodesDebugSymbols", "workspotsDebugSymbols")), f"{checkpoint.name}: typed debug scaffold changed")
        require(root["locStore"] == {"$type": "scnlocLocStoreEmbedded", "vdEntries": [], "vpEntries": []}, f"{checkpoint.name}: typed localization scaffold changed")
        lipsync = root["resouresReferences"]["lipsyncAnimSets"]
        resources = root["resouresReferences"]
        require(
            set(resources)
            == {
                "$type",
                "cinematicAnimNames",
                "cinematicAnimSets",
                "dynamicAnimNames",
                "dynamicAnimSets",
                "gameplayAnimNames",
                "gameplayAnimSets",
                "lipsyncAnimSets",
                "ridAnimationContainers",
                "ridAnimations",
                "ridAnimSets",
                "ridCameraAnimations",
                "ridCyberwareAnimSets",
                "ridDeformationAnimSets",
                "ridFacialAnimSets",
            }
            and resources["$type"] == "scnSRRefCollection"
            and all(resources[field] == [] for field in set(resources) - {"$type", "lipsyncAnimSets"}),
            f"{checkpoint.name}: typed scene resource scaffold changed",
        )
        require(len(lipsync) == 1 and lipsync[0]["$type"] == "scnLipsyncAnimSetSRRef" and resource_value(lipsync[0]["asyncRefLipsyncAnimSet"]) == ("base\\animations\\facial\\generic\\interactive_scene\\generic_facial_lipsync_gestures.anims", "Soft") and resource_value(lipsync[0]["lipsyncAnimSet"]) == ("0", "Default"), f"{checkpoint.name}: lipsync reference changed")
        require([(cname_value(item["name"]), item["nodeId"]["id"]) for item in root["entryPoints"]] == [("start", 1)] and [(cname_value(item["name"]), item["nodeId"]["id"]) for item in root["exitPoints"]] == [("contact_done", 3)], f"{checkpoint.name}: entry/exit changed")
        require(root["screenplayStore"]["$type"] == "scnscreenplayStore" and root["screenplayStore"]["options"] == [], f"{checkpoint.name}: typed screenplay scaffold changed")
        require(root["sceneSolutionHash"] == {"$type": "scnSceneSolutionHash", "sceneSolutionHash": {"$type": "scnSceneSolutionHashHash", "sceneSolutionHashDate": "14690332223362800506"}}, f"{checkpoint.name}: scene solution hash scaffold changed")
        scenarios = root["interruptionScenarios"]
        require(len(scenarios) == 1, f"{checkpoint.name}: interruption scenario count changed")
        scenario = scenarios[0]
        require(
            {key: scenario[key] for key in ("enabled", "forcePlayReturnLine", "interruptionSpammingSafeguard", "playingLinesBehavior", "playInterruptLine", "talkOnReturn")}
            == {"enabled": 1, "forcePlayReturnLine": 0, "interruptionSpammingSafeguard": 0, "playingLinesBehavior": "Default", "playInterruptLine": 1, "talkOnReturn": 1}
            and scenario["$type"] == "scnInterruptionScenario"
            and scenario["id"] == {"$type": "scnInterruptionScenarioId", "id": 0}
            and cname_value(scenario["name"]) == "Default"
            and cname_value(scenario["queueName"]) == "None"
            and scenario["postInterruptSignalFactCondition"] is None
            and scenario["postInterruptSignalTimeDelay"] == 0
            and scenario["postReturnSignalFactCondition"] is None
            and scenario["postReturnSignalTimeDelay"] == 0,
            f"{checkpoint.name}: interruption policy changed",
        )
        require(len(scenario["interruptConditions"]) == len(scenario["returnConditions"]) == 1, f"{checkpoint.name}: interruption condition cardinality changed")
        interrupt = resolve(scenario["interruptConditions"][0], root_handles)
        returned = resolve(scenario["returnConditions"][0], root_handles)
        require(
            interrupt
            == {
                "$type": "scnCheckSpeakersDistanceInterruptCondition",
                "params": {"$type": "scnCheckSpeakersDistanceInterruptConditionParams", "comparisonType": "Greater", "distance": 6},
            }
            and returned
            == {
                "$type": "scnCheckSpeakersDistanceReturnCondition",
                "params": {"$type": "scnCheckSpeakersDistanceReturnConditionParams", "comparisonType": "Less", "distance": 5},
            },
            f"{checkpoint.name}: interruption distance thresholds changed",
        )

    start_root = roots["start"]
    completed_root = roots["completed"]
    for key in set(start_root) - {"sceneGraph", "screenplayStore"}:
        require(start_root[key] == completed_root[key], f"scene shell differs between checkpoints at {key}")
    start_graph, start_nodes, _ = scene_graph(start_root)
    require([(node["nodeId"]["id"], node["$type"]) for node in start_nodes] == [(1, "scnStartNode"), (3, "scnEndNode")] and scene_edges(start_nodes) == [(1, 0, 3, 0, 0)], "start scene graph changed")
    require(all(node["ffStrategy"] == "automatic" for node in start_nodes), "start scene fast-forward strategy changed")
    require(start_graph["startNodes"] == [{"$type": "scnNodeId", "id": 1}] and start_graph["endNodes"] == [{"$type": "scnNodeId", "id": 3}] and start_nodes[1]["type"] == "Terminating", "start scene boundary bookkeeping changed")
    require(start_root["screenplayStore"] == {"$type": "scnscreenplayStore", "lines": [], "options": []}, "start screenplay must remain empty")

    graph, nodes, handles = scene_graph(completed_root)
    require([(node["nodeId"]["id"], node["$type"]) for node in nodes] == [(1, "scnStartNode"), (2, "scnSectionNode"), (4, "scnQuestNode"), (3, "scnEndNode")], "completed scene node order/types changed")
    require(all(node["ffStrategy"] == "automatic" for node in nodes), "completed scene fast-forward strategy changed")
    require(scene_edges(nodes) == [(1, 0, 2, 0, 0), (1, 0, 4, 0, 1), (2, 0, 3, 0, 0)], "completed scene edges/stamps changed")
    require(graph["startNodes"] == [{"$type": "scnNodeId", "id": 1}] and graph["endNodes"] == [{"$type": "scnNodeId", "id": 3}] and nodes[3]["type"] == "Terminating", "completed scene boundary bookkeeping changed")
    section = nodes[1]
    require(len(section["events"]) == 1 and len(section["outputSockets"]) == 2 and section["outputSockets"][1] == {"$type": "scnOutputSocket", "destinations": [], "stamp": {"$type": "scnOutputSocketStamp", "name": 1, "ordinal": 0}} and section["sectionDuration"] == {"$type": "scnSceneTime", "stu": 2998}, "section duration/event/cancel socket changed")
    require(section["actorBehaviors"] == [{"$type": "scnSectionInternalsActorBehavior", "actorId": {"$type": "scnActorId", "id": 0}, "behaviorMode": "OnlyIfAlive"}, {"$type": "scnSectionInternalsActorBehavior", "actorId": {"$type": "scnActorId", "id": 1}, "behaviorMode": "OnlyIfAlive"}], "section actor behavior policy changed")
    event = resolve(section["events"][0], handles)
    require(event["$type"] == "scnDialogLineEvent" and event["id"] == {"$type": "scnSceneEventId", "id": "8646165628675208917"} and event["duration"] == 2598 and event["startTime"] == 0 and event["screenplayLineId"] == {"$type": "scnscreenplayItemId", "id": 1} and event["type"] == "0" and event["visualStyle"] == "regular", "dialog event changed")
    require(event["additionalSpeakers"] == {"$type": "scnAdditionalSpeakers", "executionTag": 0, "role": "Full", "speakers": []} and event["executionTagFlags"] == 0 and event["scalingData"] is None and event["voParams"] == {"$type": "scnDialogLineVoParams", "alwaysUseBrainGender": 0, "customVoEvent": {"$type": "CName", "$storage": "string", "$value": "None"}, "disableHeadMovement": 0, "ignoreSpeakerIncapacitation": 0, "isHolocallSpeaker": 0, "voContext": "Vo_Context_Quest", "voExpression": "Vo_Expression_Spoken"}, "dialog event payload changed")
    ai_outer = nodes[2]
    require([cname_value(item) for item in ai_outer["isockMappings"]] == ["CutDestination", "In"] and [cname_value(item) for item in ai_outer["osockMappings"]] == ["Out"] and ai_outer["outputSockets"] == [{"$type": "scnOutputSocket", "destinations": [], "stamp": {"$type": "scnOutputSocketStamp", "name": 0, "ordinal": 0}}], "scene PuppetAI wrapper changed")
    ai_inner = resolve(ai_outer["questNode"], handles)
    require(ai_inner["$type"] == "questPuppetAIManagerNodeDefinition" and ai_inner["id"] == 4 and socket_contract(ai_inner, handles) == [("CutDestination", "CutDestination", 0), ("In", "Input", 0), ("Out", "Output", 0)] and len(ai_inner["entries"]) == 1 and ai_inner["entries"][0]["aiTier"] == "Cinematic" and ai_inner["entries"][0]["entityReference"]["reference"]["$value"] == source_builder.COMMUNITY_LOCAL, "scene PuppetAI payload changed")
    line = completed_root["screenplayStore"]["lines"]
    require(len(line) == 1 and line[0]["itemId"]["id"] == 1 and line[0]["locstringId"]["ruid"] == "9638591835734011695" and line[0]["speaker"]["id"] == 0 and line[0]["addressee"]["id"] == 1 and cname_value(line[0]["femaleLipsyncAnimationName"]) == "None" and cname_value(line[0]["maleLipsyncAnimationName"]) == "None" and line[0]["usage"] == {"$type": "scnscreenplayLineUsage", "playerGenderMask": {"$type": "scnGenderMask", "mask": 3}}, "screenplay line/lipsync/gender contract changed")

    subtitle = load_json(COMPLETED / raw_relative(CR2W_PATHS[5]))["Data"]["RootChunk"]["root"]["Data"]["entries"]
    require(subtitle == [{"$type": "localizationPersistenceSubtitleEntry", "femaleVariant": source_builder.CONTACT_LINE_TEXT, "maleVariant": source_builder.CONTACT_LINE_TEXT, "stringId": source_builder.CONTACT_LINE_RUID}], "subtitle entry changed")
    subtitle_map = load_json(COMPLETED / raw_relative(CR2W_PATHS[6]))["Data"]["RootChunk"]["root"]["Data"]["entries"]
    require(len(subtitle_map) == 1 and resource_value(subtitle_map[0]["subtitleFile"]) == (source_builder.SUBTITLES_PATH, "Soft") and cname_value(subtitle_map[0]["subtitleGroup"]) == "quest", "subtitle map changed")
    vo_map = load_json(COMPLETED / raw_relative(CR2W_PATHS[7]))["Data"]["RootChunk"]["root"]["Data"]["entries"]
    require(len(vo_map) == 1 and vo_map[0]["stringId"] == source_builder.CONTACT_LINE_RUID and resource_value(vo_map[0]["femaleResPath"]) == (WEM_PATH, "Soft") and resource_value(vo_map[0]["maleResPath"]) == (WEM_PATH, "Soft"), "voiceover map changed")


def validate_journal_and_onscreens() -> None:
    journal_resource = load_json(COMPLETED / raw_relative(CR2W_PATHS[3]))["Data"]["RootChunk"]
    handles: dict[str, dict[str, Any]] = {}
    collect_handles(journal_resource, handles)
    root = resolve(journal_resource["entry"], handles)
    require(root["$type"] == "gameJournalRootFolderEntry" and resource_value(root["descriptor"]) == ("base\\journal\\descriptor.journaldesc", "Soft") and len(root["entries"]) == 1, "journal root changed")
    quests = resolve(root["entries"][0], handles)
    minor = resolve(quests["entries"][0], handles)
    quest = resolve(minor["entries"][0], handles)
    phase = resolve(quest["entries"][0], handles)
    meet = resolve(phase["entries"][0], handles)
    leave = resolve(phase["entries"][1], handles)
    mappin = resolve(meet["entries"][0], handles)
    require(
        [(item["$type"], item["id"]) for item in (quests, minor, quest, phase, meet, mappin, leave)]
        == [
            ("gameJournalPrimaryFolderEntry", "quests"),
            ("gameJournalFolderEntry", "minor_quest"),
            ("gameJournalQuest", "cqa005"),
            ("gameJournalQuestPhase", "cqa005_01"),
            ("gameJournalQuestObjective", "cqa005_01_obj_meet"),
            ("gameJournalQuestMapPin", "cqa005_01_qmp_contact"),
            ("gameJournalQuestObjective", "cqa005_01_obj_leave"),
        ]
        and len(quests["entries"]) == len(minor["entries"]) == len(quest["entries"]) == 1
        and len(phase["entries"]) == 2
        and len(meet["entries"]) == 1
        and leave["entries"] == [],
        "cqa005 journal hierarchy/order changed",
    )
    require(
        quest["title"] == {"unk1": "0", "value": "cqa_cqa005_title"}
        and quest["type"] == "MinorQuest"
        and meet["description"] == {"unk1": "0", "value": "cqa_cqa005_objective_meet"}
        and leave["description"] == {"unk1": "0", "value": "cqa_cqa005_objective_leave"}
        and meet["optional"] == leave["optional"] == 0,
        "journal localization/objective payload changed",
    )
    require(
        mappin["enableGPS"] == 1
        and mappin["offset"] == {"$type": "Vector3", "X": 0, "Y": 0, "Z": 0.5}
        and mappin["reference"]["reference"] == {"$type": "NodeRef", "$storage": "string", "$value": "#cqa005_mp_contact"}
        and mappin["mappinData"]
        == {
            "$type": "gamemappinsMappinData",
            "active": 0,
            "debugCaption": "cqa_cqa005_mappin_contact",
            "localizedCaption": {"unk1": "0", "value": "cqa_cqa005_mappin_contact"},
            "mappinType": {"$type": "TweakDBID", "$storage": "string", "$value": "Mappins.QuestStaticMappinDefinition"},
            "scriptData": None,
            "variant": "DefaultQuestVariant",
            "visibleThroughWalls": 1,
        },
        "journal mappin payload changed",
    )

    onscreen_resource = load_json(COMPLETED / raw_relative(CR2W_PATHS[4]))["Data"]["RootChunk"]
    onscreen_handles: dict[str, dict[str, Any]] = {}
    collect_handles(onscreen_resource, onscreen_handles)
    onscreen = resolve(onscreen_resource["root"], onscreen_handles)
    expected_strings = [
        ("cqa_cqa005_title", "First Contact"),
        ("cqa_cqa005_objective_meet", "Meet the contact."),
        ("cqa_cqa005_objective_leave", "Leave the meeting area."),
        ("cqa_cqa005_mappin_contact", "First Contact"),
    ]
    require(
        onscreen["$type"] == "localizationPersistenceOnScreenEntries"
        and onscreen["entries"]
        == [
            {
                "$type": "localizationPersistenceOnScreenEntry",
                "femaleVariant": text,
                "maleVariant": "",
                "primaryKey": "0",
                "secondaryKey": key,
            }
            for key, text in expected_strings
        ],
        "cqa005 onscreen localization keys/text/order changed",
    )


def typed(root: Any, red_type: str) -> list[dict[str, Any]]:
    return [item for item in iter_objects(root) if item.get("$type") == red_type]


def require_placement(
    value: dict[str, Any],
    *,
    node_index: int,
    node_ref_value: str,
    node_ref_storage: str,
    position: tuple[float, float, float],
    yaw: float,
    maximum_distance: float,
    opaque_distance: float,
    uk10: int = 1024,
) -> None:
    vector4 = {"$type": "Vector4", "W": 0, "X": position[0], "Y": position[1], "Z": position[2]}
    vector3 = {"$type": "Vector3", "X": position[0], "Y": position[1], "Z": position[2]}
    require(
        set(value)
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
        }
        and value["Id"] == "0"
        and value["NodeIndex"] == node_index
        and value["Position"] == vector4
        and value["Pivot"] == vector3
        and value["Bounds"] == {"$type": "Box", "Max": vector4, "Min": vector4}
        and value["Scale"] == {"$type": "Vector3", "X": 1.0, "Y": 1.0, "Z": 1.0}
        and value["QuestPrefabRefHash"] == {"$type": "NodeRef", "$storage": node_ref_storage, "$value": node_ref_value}
        and value["UkHash1"] == {"$type": "NodeRef", "$storage": "uint64", "$value": "0"}
        and resource_value(value["CookedPrefabData"]) == ("0", "Default")
        and value["MaxStreamingDistance"] == maximum_distance
        and value["UkFloat1"] == opaque_distance
        and (value["Uk10"], value["Uk11"], value["Uk12"], value["Uk13"], value["Uk14"])
        == (uk10, 512, 0, "0", "0"),
        f"nodeData placement {node_index}: identity/transform metadata changed",
    )
    orientation = value["Orientation"]
    require(
        orientation["$type"] == "Quaternion"
        and orientation["i"] == orientation["j"] == 0
        and math.isclose(float(orientation["k"]), math.sin(math.radians(yaw) / 2), rel_tol=0, abs_tol=1e-15)
        and math.isclose(float(orientation["r"]), math.cos(math.radians(yaw) / 2), rel_tol=0, abs_tol=1e-15),
        f"nodeData placement {node_index}: yaw changed",
    )


def validate_world() -> None:
    quest = load_json(COMPLETED / raw_relative(CR2W_PATHS[9]))["Data"]["RootChunk"]
    always = load_json(COMPLETED / raw_relative(CR2W_PATHS[10]))["Data"]["RootChunk"]
    for root, category, level in ((quest, "Quest", 255), (always, "AlwaysLoaded", 1)):
        require(root["$type"] == "worldStreamingSector" and root["category"] == category and root["level"] == level and root["version"] == 62, f"{category} sector shell changed")
    expected_prefab = "$/mod/cqa/cqa005/#cqa005_pr_first_contact"
    expected_quest_refs = [
        f"{expected_prefab}/#cqa005_tr_setup",
        f"{expected_prefab}/#cqa005_tr_cleanup",
        f"{expected_prefab}/#cqa005_spot_contact",
        f"{expected_prefab}/#cqa005_com_contact",
    ]
    expected_always_refs = [
        f"{expected_prefab}/#cqa005_sm_contact",
        f"{expected_prefab}/#cqa005_mp_contact",
    ]
    quest_refs = [item["$value"] for item in quest["nodeRefs"]]
    always_refs = [item["$value"] for item in always["nodeRefs"]]
    require(quest_refs == expected_quest_refs, "Quest sector ownership changed")
    require(always_refs == expected_always_refs, "AlwaysLoaded marker ownership changed")
    expected_buffer_type = "WolvenKit.RED4.Archive.Buffer.worldNodeDataBuffer, WolvenKit.RED4, Version=8.19.0.0, Culture=neutral, PublicKeyToken=null"
    for sector, expected_count in ((quest, 4), (always, 3)):
        require(sector["nodeData"]["BufferId"] == "0" and sector["nodeData"]["Flags"] == 0 and sector["nodeData"]["Type"] == expected_buffer_type and len(sector["nodeData"]["Data"]) == expected_count, "world nodeData buffer contract changed")
    quest_handles: dict[str, dict[str, Any]] = {}
    collect_handles(quest, quest_handles)
    quest_nodes = [resolve(item, quest_handles) for item in quest["nodes"]]
    require([item["$type"] for item in quest_nodes] == ["worldTriggerAreaNode", "worldTriggerAreaNode", "worldAISpotNode", "worldCompiledCommunityAreaNode_Streamable"], "Quest sector node types changed")
    decode_outline(resolve(quest_nodes[0]["outline"], quest_handles), 25, 16, 12)
    decode_outline(resolve(quest_nodes[1]["outline"], quest_handles), 110, 20, 16)
    workspot = resolve(quest_nodes[2]["spot"], quest_handles)
    require(resource_value(workspot["resource"]) == ("base\\workspots\\common\\ground\\generic__stand_ground_cigarette__smoke__01.workspot", "Soft") and cname_value(quest_nodes[2]["debugName"]) == "{cqa005_spot_contact}", "AI workspot evidence path/name changed")
    area = quest_nodes[3]
    require(area["sourceObjectId"]["hash"] == "5948510988927765319" and cname_value(area["debugName"]) == "{cqa005_com_contact}", "community source object ID/name changed")
    area_data = resolve(area["area"], quest_handles)
    require(len(area_data["entriesData"]) == 1, "community area entry cardinality changed")
    area_entry = area_data["entriesData"][0]
    require(cname_value(area_entry["entryName"]) == "contact" and len(area_entry["phasesData"]) == 1, "community area entry name changed")
    area_phase = area_entry["phasesData"][0]
    require(cname_value(area_phase["entryPhaseName"]) == "default" and len(area_phase["timePeriodsData"]) == 1, "community area phase name changed")
    period_data = area_phase["timePeriodsData"][0]
    require(cname_value(period_data["periodName"]) == "Day" and period_data["isSequence"] == 0 and period_data["spotNodeIds"] == [{"$type": "worldGlobalNodeID", "hash": "15950783814303760596"}], "community area period/AI join changed")

    quest_placements = quest["nodeData"]["Data"]
    for index, ref, position, maximum_distance, opaque_distance in (
        (0, expected_quest_refs[0], (-1000.02, 1497.2208, 2.3), 320, 280),
        (1, expected_quest_refs[1], (-1000.02, 1497.2208, 0.3), 360, 320),
        (2, expected_quest_refs[2], (-1000.02, 1497.2208, 6.957), 320, 280),
        (3, expected_quest_refs[3], (-1000.02, 1497.2208, 6.957), 320, 280),
    ):
        require_placement(quest_placements[index], node_index=index, node_ref_value=ref, node_ref_storage="string", position=position, yaw=88.6, maximum_distance=maximum_distance, opaque_distance=opaque_distance)

    always_handles: dict[str, dict[str, Any]] = {}
    collect_handles(always, always_handles)
    always_nodes = [resolve(item, always_handles) for item in always["nodes"]]
    require([item["$type"] for item in always_nodes] == ["worldStaticMarkerNode", "worldStaticMarkerNode", "worldCommunityRegistryNode"], "AlwaysLoaded node types changed")
    require([cname_value(item["debugName"]) for item in always_nodes] == ["{cqa005_sm_contact}", "{cqa005_mp_contact}", "cqa005_contact_registry"], "AlwaysLoaded marker/registry names changed")
    registry = always_nodes[2]
    require(len(registry["communitiesData"]) == 1, "registry community cardinality changed")
    community = registry["communitiesData"][0]
    require(community["communityId"]["entityId"]["hash"] == "5948510988927765319" and len(community["entriesInitialState"]) == 1 and community["entriesInitialState"][0]["entryActiveOnStart"] == 0 and cname_value(community["entriesInitialState"][0]["entryName"]) == "contact" and cname_value(community["entriesInitialState"][0]["initialPhaseName"]) == "default", "registry initial state changed")
    template = resolve(community["template"], always_handles)
    require(len(template["entries"]) == 1, "community template entry cardinality changed")
    entry = resolve(template["entries"][0], always_handles)
    require(len(entry["phases"]) == 1, "community entry phase cardinality changed")
    phase = resolve(entry["phases"][0], always_handles)
    require(len(phase["timePeriods"]) == 1, "community phase time-period cardinality changed")
    period = phase["timePeriods"][0]
    require(entry["characterRecordId"]["$value"] == "Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa" and cname_value(entry["entryName"]) == "contact" and cname_value(phase["phaseName"]) == "default" and [cname_value(item) for item in phase["appearances"]] == ["default"], "community template changed")
    require(period["hour"] == "Day" and period["quantity"] == 1 and period["isSequence"] == 0 and period["spotNodeRefs"] == [{"$type": "NodeRef", "$storage": "string", "$value": expected_quest_refs[2]}], "community period/spot join changed")
    persistent = registry["workspotsPersistentData"]
    require(len(persistent) == 1 and persistent[0]["globalNodeId"]["hash"] == "15950783814303760596" and persistent[0]["isEnabled"] == 1 and persistent[0]["worldPosition"] == {"$type": "WorldPosition", "x": {"$type": "FixedPoint", "Bits": round(-1000.02 * 131072)}, "y": {"$type": "FixedPoint", "Bits": round(1497.2208 * 131072)}, "z": {"$type": "FixedPoint", "Bits": round(6.957 * 131072)}} and math.isclose(float(persistent[0]["yaw"]), 88.6), "persistent AI spot row changed")
    always_placements = always["nodeData"]["Data"]
    require_placement(always_placements[0], node_index=0, node_ref_value=expected_always_refs[0], node_ref_storage="string", position=(-1000.02, 1497.2208, 8.3), yaw=88.6, maximum_distance=360, opaque_distance=320)
    require_placement(always_placements[1], node_index=1, node_ref_value=expected_always_refs[1], node_ref_storage="string", position=(-1000.02, 1497.2208, 8.3), yaw=88.6, maximum_distance=360, opaque_distance=320)
    require_placement(always_placements[2], node_index=2, node_ref_value="6908684691797323855", node_ref_storage="uint64", position=(0, 0, 0), yaw=0, maximum_distance=17.320507, opaque_distance=100000000.0, uk10=32)

    emitted_refs = [expected_prefab, *quest_refs, *always_refs]
    emitted_hashes = [source_builder.node_ref_hash(ref) for ref in emitted_refs]
    require(emitted_hashes == [7886199184289800151, 6777129165529301919, 13742890428611163466, 15950783814303760596, 5948510988927765319, 13032711645120554624, 9647715025081619761] and all(emitted_hashes) and len(emitted_hashes) == len(set(emitted_hashes)), "emitted full NodeRef hashes changed, collided, or became zero")
    require(source_builder.node_ref_hash("$/mod/#;alias/#node") == source_builder.node_ref_hash("$/mod//node") == 11647479394447743018 and source_builder.node_ref_hash("#plain") == source_builder.node_ref_hash("plain") == 18252272687975150087, "RED4 alias-aware NodeRef hashing regressed")
    require(source_builder.COMMUNITY_SOURCE_ID == "5948510988927765319" and source_builder.AI_SPOT_GLOBAL_ID == "15950783814303760596" and source_builder.REGISTRY_NODE_ID == "6908684691797323855", "community identity constants changed")
    require(source_builder.REGISTRY_NODE_ID not in {str(value) for value in emitted_hashes} and source_builder.REGISTRY_NODE_ID not in always_refs, "registry placement identity leaked into emitted nodeRefs")

    block = load_json(COMPLETED / raw_relative(CR2W_PATHS[8]))["Data"]["RootChunk"]
    descriptors = block["descriptors"]
    require(block["$type"] == "worldStreamingBlock" and block["cookingPlatform"] == "PLATFORM_PC" and block["index"] == {"$type": "worldStreamingBlockIndex", "oup": "Base", "rldGridCell": 0} and len(descriptors) == 2, "streaming block shell changed")
    require([(item["category"], resource_value(item["data"])[0], item["level"]) for item in descriptors] == [("Quest", "mod\\cqa\\cqa005\\world\\cqa005_first_contact.streamingsector", 0), ("AlwaysLoaded", "mod\\cqa\\cqa005\\world\\cqa005_always_loaded.streamingsector", 1)], "streaming descriptor ownership changed")
    require(descriptors[0]["questPrefabNodeRef"] == {"$type": "NodeRef", "$storage": "string", "$value": expected_prefab} and descriptors[1]["questPrefabNodeRef"] == {"$type": "NodeRef", "$storage": "uint64", "$value": "0"}, "streaming prefab binding changed")
    max_float = 3.40282347e38
    for descriptor, minimum, maximum in (
        (descriptors[0], (-1300.02, 1197.2208, -291.7), (-700.02, 1797.2208, 308.3)),
        (descriptors[1], (-99999, -99999, -99999), (99999, 99999, 99999)),
    ):
        require(descriptor["$type"] == "worldStreamingSectorDescriptor" and descriptor["numNodeRanges"] == 1 and descriptor["variants"] == [] and descriptor["blockIndex"] == {"$type": "worldStreamingBlockIndex", "oup": "Base", "rldGridCell": 0} and descriptor["streamingBox"] == {"$type": "Box", "Max": {"$type": "Vector4", "W": max_float, "X": maximum[0], "Y": maximum[1], "Z": maximum[2]}, "Min": {"$type": "Vector4", "W": -max_float, "X": minimum[0], "Y": minimum[1], "Z": minimum[2]}}, "streaming descriptor bounds/scaffold changed")


def validate_audio() -> None:
    wav = LAB / "voice-source" / "contact_i_85c3283507e7ef2f.wav"
    require(wav.stat().st_size == 249160 and sha256(wav) == WAV_SHA256, "canonical WAV changed")
    for checkpoint in (START, COMPLETED):
        wem = checkpoint / cooked_relative(WEM_PATH)
        require(wem.stat().st_size == 21379 and sha256(wem) == WEM_SHA256, f"{checkpoint.name}: WEM changed")
    provenance = load_json(LAB / "voice-source" / "provenance.json")
    require(provenance["line"] == {"key": "cqa005_contact_line_0001", "text": "All clear. Keep moving.", "ruid": source_builder.CONTACT_LINE_RUID, "hex_ruid": "85c3283507e7ef2f"}, "voice line provenance changed")
    require(provenance["source"]["sha256"] == WAV_SHA256 and provenance["wem"]["sha256"] == WEM_SHA256 and provenance["wem"]["converter"] == "WwiseConsole 2025.1.7.9143 convert-external-source" and provenance["wem"]["byte_reproducible"] is False, "voice artifact provenance changed")
    require(provenance["license"] == "CC-BY-4.0" and provenance["redistributed_third_party_binaries"] == [], "voice artifact licensing/provenance boundary changed")
    readme = (LAB / "voice-source" / "README.md").read_text(encoding="utf-8")
    require("not claimed to be byte reproducible" in readme and "reader prerequisite" in readme, "voice evidence boundary changed")


def manifest_document() -> dict[str, Any]:
    acceptance = load_json(COMPLETED / "runtime-acceptance.json")
    checkpoint_files = {
        relative: sha256(COMPLETED / PurePosixPath(relative))
        for relative in sorted(actual_files(COMPLETED) - {"example.json"})
    }
    shared_names = {
        "LICENSE.md",
        "README.md",
        *(f"voice-source/{name}" for name in VOICE_FILES),
    }
    shared_files = {
        relative: sha256(LAB / PurePosixPath(relative))
        for relative in sorted(shared_names)
    }
    diagram_names = {
        f"assets/diagrams/lab-05/{name}" for name in ASSET_FILES
    }
    diagrams = {
        relative: sha256(ROOT / PurePosixPath(relative))
        for relative in sorted(diagram_names)
    }
    root_layout = load_json(ASSETS / "cqa005.questphase.layout.json")
    child_layout = load_json(ASSETS / "cqa005_contact.questphase.layout.json")
    return {
        "schema_version": 2,
        "id": "cqa005",
        "title": "First Contact",
        "book_chapter": "book/src/scenes/lab-05.md",
        "baseline": {"recorded": "2026-08-09", **BASELINE},
        "depot_paths": [*CR2W_PATHS, WEM_PATH],
        "registered_depot_paths": list(REGISTERED_PATHS),
        "persistent_facts": ["cqa005_completed"],
        "evidence": {
            "structure": {
                "status": "structurally-validated",
                "date": "2026-08-09",
                "method": (
                    "WolvenKit 8.19.0 deserialize and serialize "
                    "round-trip inspection"
                ),
                "resource_pairs": 22,
            },
            "runtime": {
                "status": acceptance["status"],
                "class": acceptance["evidence_class"],
                "date": acceptance["date"],
                "record": "runtime-acceptance.json",
            },
        },
        "graphs": {
            "root": {
                "layout": "assets/diagrams/lab-05/cqa005.questphase.layout.json",
                "source_fingerprint": root_layout["source_fingerprint"],
            },
            "child": {
                "layout": (
                    "assets/diagrams/lab-05/"
                    "cqa005_contact.questphase.layout.json"
                ),
                "source_fingerprint": child_layout["source_fingerprint"],
            },
            "scene": {
                "source": (
                    "examples/lab-05-first-contact/completed/source/raw/"
                    "mod/cqa/cqa005/scenes/cqa005_first_contact.scene.json"
                ),
                "nodes": 4,
                "edges": 3,
                "entry": "start",
                "exit": "contact_done",
            },
        },
        "audio": {
            "line_key": source_builder.CONTACT_LINE_KEY,
            "ruid": source_builder.CONTACT_LINE_RUID,
            "wav_sha256": WAV_SHA256,
            "wem_sha256": WEM_SHA256,
            "wwise_console": "2025.1.7.9143",
            "byte_reproducible_wem": False,
            "runtime": acceptance["evidence_class"],
            "provenance": "voice-source/provenance.json",
        },
        "artifacts": {
            "algorithm": "sha256",
            "checkpoint_files": checkpoint_files,
            "shared_files": shared_files,
            "diagrams": diagrams,
        },
    }


def write_manifest() -> None:
    destination = COMPLETED / "example.json"
    destination.write_text(
        json.dumps(manifest_document(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate_acceptance_manifest_and_diagrams() -> None:
    acceptance = load_json(COMPLETED / "runtime-acceptance.json")
    require(
        set(acceptance)
        == {
            "schema_version",
            "example_id",
            "status",
            "evidence_class",
            "date",
            "required_environment",
            "candidates",
            "save_captures",
            "runs",
            "cases",
            "promotion_rule",
        }
        and acceptance["schema_version"] == 4
        and acceptance["example_id"] == "cqa005"
        and acceptance["required_environment"] == BASELINE,
        "acceptance schema/example/environment changed",
    )
    runs = acceptance["runs"]
    cases = acceptance["cases"]
    expected_ids = list(RUN_CONTRACT)
    require(
        len(runs) == len(cases) == 11
        and [item["id"] for item in runs]
        == expected_ids
        == [item["id"] for item in cases],
        "acceptance run/case matrix changed",
    )
    case_statuses = [item["status"] for item in cases]
    require(all(value in {"pending", "passed", "failed"} for value in case_statuses), "acceptance case status changed")
    if "failed" in case_statuses:
        derived_status = "failed"
    elif set(case_statuses) == {"passed"}:
        derived_status = "passed"
    else:
        derived_status = "pending"
    status = acceptance["status"]
    expected_class = "runtime-proven" if derived_status == "passed" else "experimental"
    require(status == derived_status and acceptance["evidence_class"] == expected_class, "acceptance top status/evidence class disagree with required case results")
    recorded_date = acceptance["date"]
    if status == "pending":
        require(recorded_date is None, "pending acceptance must not have a date")
    else:
        require(isinstance(recorded_date, str), "failed/passed acceptance needs a recorded date")
        try:
            parsed_date = date.fromisoformat(recorded_date)
        except ValueError as error:
            raise RuntimeError("acceptance date must be canonical YYYY-MM-DD") from error
        require(parsed_date.isoformat() == recorded_date, "acceptance date must be canonical YYYY-MM-DD")

    candidates = acceptance["candidates"]
    require(len(candidates) == 1, "acceptance must bind one canonical candidate")
    candidate = candidates[0]
    require(set(candidate) == {"id", "manifest", "installed_files", "depot_paths"} and candidate["id"] == "canonical" and candidate["manifest"] == "example.json" and candidate["depot_paths"] == [*CR2W_PATHS, WEM_PATH], "acceptance candidate/depot inventory changed")
    installed = candidate["installed_files"]
    require(all(isinstance(item, dict) and set(item) == {"path", "sha256"} for item in installed) and [item["path"] for item in installed] == ["archive\\pc\\mod\\CQA_Lab05_FirstContact.archive", "archive\\pc\\mod\\CQA_Lab05_FirstContact.archive.xl"], "acceptance installed-file inventory/shape changed")
    installed_hashes = [item["sha256"] for item in installed]
    require(all(value is None for value in installed_hashes) or all(is_sha256_value(value) for value in installed_hashes), "candidate installed hashes must be wholly empty or wholly bound")
    if any(value in {"passed", "failed"} for value in case_statuses):
        require(all(is_sha256_value(value) for value in installed_hashes), "any completed execution requires both exact installed-file hashes")
    case_status_by_id = {item["id"]: item["status"] for item in cases}
    run_by_id = {item["id"]: item for item in runs}
    captures = acceptance["save_captures"]
    require(
        isinstance(captures, list)
        and [item["id"] for item in captures] == list(SAVE_CAPTURE_CONTRACT),
        "acceptance save-capture inventory changed",
    )
    capture_by_id = {item["id"]: item for item in captures}
    completed_capture_slots: dict[str, str] = {}
    completed_capture_hashes: dict[str, str] = {}
    capture_fields = {
        "id",
        "source_run_id",
        "parent_capture_id",
        "save_type",
        "label",
        "observable_state",
        "slot_directory",
        "artifact",
        "created_before_first_install",
        "sha256",
    }
    for capture in captures:
        capture_id = capture["id"]
        expected_capture = SAVE_CAPTURE_CONTRACT[capture_id]
        require(set(capture) == capture_fields, f"save capture {capture_id}: field set changed")
        require(
            capture["source_run_id"] == expected_capture["source_run_id"]
            and capture["parent_capture_id"] == expected_capture["parent_capture_id"]
            and capture["save_type"] == "manual-save"
            and capture["label"] == expected_capture["label"]
            and capture["observable_state"] == expected_capture["observable_state"]
            and capture["artifact"] == "sav.dat"
            and capture["created_before_first_install"]
            is expected_capture["created_before_first_install"],
            f"save capture {capture_id}: provenance/state contract changed",
        )
        slot_directory = capture["slot_directory"]
        digest = capture["sha256"]
        require(
            (slot_directory is None and digest is None)
            or (
                isinstance(slot_directory, str)
                and slot_directory.strip()
                and is_sha256_value(digest)
            ),
            f"save capture {capture_id}: slot/hash must be wholly empty or wholly bound",
        )
        if digest is not None:
            normalized_slot = slot_directory.strip().replace("/", "\\").rstrip("\\").casefold()
            require(normalized_slot, f"save capture {capture_id}: slot directory normalizes to empty")
            completed_capture_slots[capture_id] = normalized_slot
            completed_capture_hashes[capture_id] = digest
    require(
        len(completed_capture_slots) == len(set(completed_capture_slots.values())),
        "bound save captures must use distinct normalized slot directories",
    )
    require(
        len(completed_capture_hashes) == len(set(completed_capture_hashes.values())),
        "the five source captures represent distinct save states and must have distinct hashes",
    )
    require(
        tuple(
            capture_id
            for capture_id, contract in SAVE_CAPTURE_CONTRACT.items()
            if contract["source_run_id"] == "clean-ordinary-passive-spawn"
        )
        == (
            "seed-pre-scene-outside-setup",
            "seed-post-contact-inside-cleanup",
            "seed-completed",
        ),
        "Case 1 must own exactly the three frozen manual seed captures",
    )
    require(
        {
            capture_id: tuple(
                run_id
                for run_id, contract in RUN_CONTRACT.items()
                if contract[2] == capture_id
            )
            for capture_id in SAVE_CAPTURE_CONTRACT
        }
        == CAPTURE_RUN_GROUPS,
        "run-to-capture groups changed",
    )
    expected_logs = ["red4ext\\plugins\\ArchiveXL\\ArchiveXL.log", "red4ext\\logs\\red4ext.log", "red4ext\\logs\\game.log", "r6\\logs\\redscript_rCURRENT.log"]
    completed_timestamps: dict[str, datetime] = {}
    completed_log_bundles: dict[str, tuple[str, ...]] = {}
    completed_slot_directories: dict[str, str] = {}
    for run in runs:
        run_id = run["id"]
        require(set(run) == {"id", "candidate_id", "save_state", "save_provenance", "performed_at", "tester", "observed_environment", "save", "logs"}, f"acceptance run {run_id}: field set changed")
        expected_state, expected_provenance, expected_capture_id = RUN_CONTRACT[run_id]
        require(run["candidate_id"] == "canonical" and (run["save_state"], run["save_provenance"]) == (expected_state, expected_provenance), f"acceptance run {run_id}: candidate/save contract changed")
        require(all(isinstance(item, dict) and set(item) == {"path", "sha256"} for item in run["logs"]) and [item["path"] for item in run["logs"]] == expected_logs, f"acceptance run {run_id}: log inventory/shape changed")
        require(set(run["observed_environment"]) == set(BASELINE), f"acceptance run {run_id}: observed version slots changed")
        save = run["save"]
        capture_contract = SAVE_CAPTURE_CONTRACT[expected_capture_id]
        require(
            set(save)
            == {
                "label",
                "slot_directory",
                "artifact",
                "created_before_first_install",
                "capture_id",
                "source_run_id",
                "copy_scope",
                "game_closed_before_clone",
                "sha256",
            }
            and save["label"] == capture_contract["label"]
            and save["artifact"] == "sav.dat"
            and save["created_before_first_install"]
            is capture_contract["created_before_first_install"]
            and save["capture_id"] == expected_capture_id
            and save["source_run_id"] == capture_contract["source_run_id"]
            and save["copy_scope"] == "complete-slot-directory",
            f"acceptance run {run_id}: save lineage contract changed",
        )
        if case_status_by_id[run_id] == "pending":
            require(run["performed_at"] is None and run["tester"] is None and run["observed_environment"] == {key: None for key in BASELINE} and all(save[key] is None for key in ("slot_directory", "game_closed_before_clone", "sha256")) and all(item["sha256"] is None for item in run["logs"]), f"pending run {run_id}: execution slots must be empty")
        else:
            timestamp = parse_offset_timestamp(run["performed_at"])
            require(timestamp is not None and isinstance(run["tester"], str) and run["tester"].strip(), f"completed run {run_id}: execution identity/timestamp missing")
            require(run["observed_environment"] == BASELINE, f"completed run {run_id}: observed versions do not match baseline")
            require(isinstance(save["slot_directory"], str) and save["slot_directory"].strip() and save["game_closed_before_clone"] is True and is_sha256_value(save["sha256"]), f"completed run {run_id}: closed-game full-slot save clone evidence incomplete")
            capture = capture_by_id[expected_capture_id]
            require(is_sha256_value(capture["sha256"]) and save["sha256"] == capture["sha256"], f"completed run {run_id}: execution save must be byte-identical to capture {expected_capture_id}")
            require(all(is_sha256_value(item["sha256"]) for item in run["logs"]), f"completed run {run_id}: log hashes incomplete")
            completed_timestamps[run_id] = timestamp
            completed_log_bundles[run_id] = tuple(item["sha256"] for item in run["logs"])
            slot_directory = save["slot_directory"].strip().replace("/", "\\").rstrip("\\").casefold()
            require(slot_directory, f"completed run {run_id}: slot directory normalizes to empty")
            completed_slot_directories[run_id] = slot_directory
    require(len(completed_timestamps) == len(set(completed_timestamps.values())), "completed executions must use distinct performed_at instants")
    require(len(completed_log_bundles) == len(set(completed_log_bundles.values())), "completed executions must use distinct four-log hash bundles")
    require(len(completed_slot_directories) == len(set(completed_slot_directories.values())), "completed executions must use distinct save slot directories")
    require(
        set(completed_slot_directories.values()).isdisjoint(completed_capture_slots.values()),
        "execution clones must use slot directories distinct from all source captures",
    )
    if case_status_by_id["clean-ordinary-passive-spawn"] == "passed":
        require(
            all(
                capture_id in completed_capture_hashes
                for capture_id in (
                    "seed-pre-scene-outside-setup",
                    "seed-post-contact-inside-cleanup",
                    "seed-completed",
                )
            ),
            "passed Case 1 must bind all three manual seed captures",
        )
    for capture_id, capture in capture_by_id.items():
        source_run_id = capture["source_run_id"]
        if capture["sha256"] is not None and source_run_id is not None:
            require(source_run_id in completed_timestamps, f"save capture {capture_id}: source run is not completed")
    for run_id, timestamp in completed_timestamps.items():
        source_run_id = run_by_id[run_id]["save"]["source_run_id"]
        if source_run_id is not None:
            require(
                source_run_id in completed_timestamps
                and completed_timestamps[source_run_id] < timestamp,
                f"completed run {run_id}: source run must precede its execution clone",
            )
    if status in {"failed", "passed"}:
        latest_completed_date = max(completed_timestamps.values()).date().isoformat()
        require(recorded_date == latest_completed_date, "terminal acceptance date must equal the latest completed run date")

    for case in cases:
        case_id = case["id"]
        require(set(case) == {"id", "required", "status", "run_ids", "precondition", "expected", "observed", "evidence"}, f"acceptance case {case_id}: field set changed")
        expected_precondition, expected_outcome = CASE_CONTRACT[case_id]
        require(case["required"] is True and case["run_ids"] == [case_id] and case["precondition"] == expected_precondition and case["expected"] == expected_outcome and case["status"] in {"pending", "passed", "failed"}, f"acceptance case {case_id}: frozen contract changed")
        if case["status"] == "pending":
            require(case["observed"] is None and case["evidence"] == [], f"pending case {case_id}: result slots must be empty")
        else:
            require(isinstance(case["observed"], str) and case["observed"].strip() and isinstance(case["evidence"], list) and case["evidence"], f"completed case {case_id}: result evidence incomplete")
    retained_evidence_files()
    require(acceptance["promotion_rule"] == PROMOTION_RULE, "acceptance promotion rule changed")

    expected_marker = {
        "pending": "**Lab 5 runtime evidence:** **Experimental** — pending.",
        "failed": "**Lab 5 runtime evidence:** **Experimental** — failed.",
        "passed": "**Lab 5 runtime evidence:** **Runtime-proven** — passed.",
    }[status]
    marker_prefix = "**Lab 5 runtime evidence:**"
    test_page = ROOT / "book" / "src" / "scenes" / "lab-05-test.md"
    require(
        len(STATUS_PAGE_RELATIVES) == len(set(STATUS_PAGE_RELATIVES)) == 21,
        "Lab 5 runtime marker inventory must contain exactly 21 unique pages",
    )
    for page in STATUS_PAGES:
        marker_lines = [line for line in page.read_text(encoding="utf-8").splitlines() if line.startswith(marker_prefix)]
        require(marker_lines and marker_lines[0] == expected_marker, f"{page}: first Lab 5 runtime marker disagrees with acceptance")
        if page != test_page:
            require(marker_lines == [expected_marker], f"{page}: expected exactly one Lab 5 runtime marker")

    for page in GATED_BOOK_PAGES:
        content = page.read_text(encoding="utf-8")
        normalized = " ".join(content.split())
        require(
            normalized.count(GATED_STATUS_NOTE) == 1,
            f"{page}: expected exactly one canonical Lab 5 acceptance-gate note",
        )

    for page in STATUS_PAGES:
        content = page.read_text(encoding="utf-8")
        normalized = " ".join(content.split())
        require(
            "seed-pre-scene-outside-setup" in normalized
            or "named pre-scene seed load" in normalized,
            f"{page}: missing bounded Cases 3/4/7 pre-scene seed-load scope",
        )
        for stale_fragment in STALE_GATED_STATUS_FRAGMENTS:
            require(
                stale_fragment.casefold() not in normalized.casefold(),
                f"{page}: stale fixed acceptance-gated status text {stale_fragment!r}",
            )

    test_content = test_page.read_text(encoding="utf-8")
    require(
        "schema-version-4" in test_content
        and all(f"`{capture_id}`" in test_content for capture_id in SAVE_CAPTURE_CONTRACT),
        "Lab 5 test chapter must document schema v4 and all five source captures",
    )
    checklist_lines = [
        line
        for line in test_content.splitlines()
        if line.startswith("- [ ] `")
    ]
    expected_checklist_lines = [f"- [ ] `{relative}`" for relative in STATUS_PAGE_RELATIVES]
    require(
        checklist_lines == expected_checklist_lines,
        "Lab 5 test marker checklist must enumerate the exact 21-page marker inventory in order",
    )

    expected_date_row = f"| Runtime test date | {recorded_date} |" if recorded_date is not None else "| Runtime test date | Not yet recorded |"
    for page in DATE_PAGES:
        date_rows = [line for line in page.read_text(encoding="utf-8").splitlines() if line.startswith("| Runtime test date |")]
        require(date_rows == [expected_date_row], f"{page}: runtime test date row disagrees with acceptance")

    result = subprocess.run([sys.executable, "-B", str(DIAGRAM_BUILDER), "--check"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
    require(result.returncode == 0, f"Lab 5 diagrams stale:\n{result.stdout}{result.stderr}".rstrip())
    for name in PUBLISHED_FILES:
        require((ASSETS / name).read_bytes() == (PUBLISHED / name).read_bytes(), f"published {name} differs from source")
        content = (PUBLISHED / name).read_text(encoding="utf-8")
        evidence_label = "Runtime-proven" if expected_class == "runtime-proven" else "Experimental"
        require(evidence_label in content and status in content and "WolvenKit" not in content, f"{name}: evidence/status/screenshot boundary changed")

    manifest = load_json(COMPLETED / "example.json")
    require(manifest == manifest_document(), "example manifest differs from the complete derived contract")
    require(manifest["schema_version"] == 2 and manifest["id"] == "cqa005" and manifest["baseline"] == {"recorded": "2026-08-09", **BASELINE}, "example manifest identity/baseline changed")
    require(tuple(manifest["depot_paths"]) == (*CR2W_PATHS, WEM_PATH) and tuple(manifest["registered_depot_paths"]) == REGISTERED_PATHS, "example manifest depot inventories changed")
    require(manifest["evidence"]["structure"] == {"status": "structurally-validated", "date": "2026-08-09", "method": "WolvenKit 8.19.0 deserialize and serialize round-trip inspection", "resource_pairs": 22} and manifest["evidence"]["runtime"] == {"status": status, "class": expected_class, "date": recorded_date, "record": "runtime-acceptance.json"}, "example evidence metadata changed")
    for key, layout_name in (("root", "cqa005.questphase.layout.json"), ("child", "cqa005_contact.questphase.layout.json")):
        layout = load_json(ASSETS / layout_name)
        require(manifest["graphs"][key]["source_fingerprint"] == layout["source_fingerprint"], f"manifest {key} graph fingerprint drift")
    require(manifest["audio"]["wav_sha256"] == WAV_SHA256 and manifest["audio"]["wem_sha256"] == WEM_SHA256 and manifest["audio"]["wwise_console"] == "2025.1.7.9143" and manifest["audio"]["runtime"] == expected_class, "manifest audio provenance/runtime evidence changed")
    artifacts = manifest["artifacts"]
    require(artifacts["algorithm"] == "sha256", "manifest artifact algorithm changed")
    for relative, digest in artifacts["checkpoint_files"].items():
        require(sha256(COMPLETED / PurePosixPath(relative)) == digest, f"manifest checkpoint hash drift: {relative}")
    for relative, digest in artifacts["shared_files"].items():
        require(sha256(LAB / PurePosixPath(relative)) == digest, f"manifest shared hash drift: {relative}")
    for relative, digest in artifacts["diagrams"].items():
        require(sha256(ROOT / PurePosixPath(relative)) == digest, f"manifest diagram hash drift: {relative}")
    require(set(artifacts["checkpoint_files"]) == actual_files(COMPLETED) - {"example.json"}, "manifest checkpoint hash coverage changed")
    require(set(artifacts["shared_files"]) == {"LICENSE.md", "README.md", *(f"voice-source/{name}" for name in VOICE_FILES)}, "manifest shared hash coverage changed")
    require(set(artifacts["diagrams"]) == {f"assets/diagrams/lab-05/{name}" for name in ASSET_FILES}, "manifest diagram hash coverage changed")


def validate_packages() -> None:
    with tempfile.TemporaryDirectory(prefix="cqa-lab05-package-a-") as first_dir, tempfile.TemporaryDirectory(prefix="cqa-lab05-package-b-") as second_dir:
        first = Path(first_dir)
        second = Path(second_dir)
        for destination in (first, second):
            result = subprocess.run(
                [sys.executable, "-B", str(PACKAGE_BUILDER), "--output", str(destination)],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            require(result.returncode == 0, f"shared package builder failed:\n{result.stdout}{result.stderr}".rstrip())
        for name, root_name in (
            ("cqa-lab-05-start.zip", "CQA_Lab05_FirstContact_Start"),
            ("cqa-lab-05-completed.zip", "CQA_Lab05_FirstContact"),
        ):
            first_zip = first / name
            second_zip = second / name
            require(first_zip.read_bytes() == second_zip.read_bytes(), f"{name}: shared package generation is nondeterministic")
            with ZipFile(first_zip) as archive:
                names = set(archive.namelist())
                require(
                    {
                        f"{root_name}/voice-source/README.md",
                        f"{root_name}/voice-source/provenance.json",
                        f"{root_name}/voice-source/contact_i_85c3283507e7ef2f.wav",
                    }
                    <= names,
                    f"{name}: voice-source package contract changed",
                )


def run_wkit(wkit: Path) -> None:
    require(wkit.is_file(), f"WolvenKit CLI not found: {wkit}")
    version = subprocess.run([str(wkit), "--version"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8")
    require(version.returncode == 0 and version.stdout.strip() == "8.19.0", f"expected WolvenKit 8.19.0, got {version.stdout.strip()!r}")
    with tempfile.TemporaryDirectory(prefix="cqa-lab05-wkit-") as temporary:
        temp = Path(temporary)
        for checkpoint in (START, COMPLETED):
            cooked_out = temp / checkpoint.name / "cooked"
            json_out = temp / checkpoint.name / "json"
            cooked_out.mkdir(parents=True)
            json_out.mkdir(parents=True)
            cook = subprocess.run([str(wkit), "convert", "deserialize", str(checkpoint / "source" / "raw"), "-o", str(cooked_out), "-v", "Quiet"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", timeout=120)
            require(cook.returncode == 0, f"WolvenKit cook failed for {checkpoint.name}:\n{cook.stdout}{cook.stderr}".rstrip())
            require(len(list(cooked_out.iterdir())) == 11, f"{checkpoint.name}: WolvenKit cooked count changed")
            for depot_path in CR2W_PATHS:
                generated = cooked_out / Path(depot_path).name
                checked = checkpoint / cooked_relative(depot_path)
                require(generated.read_bytes() == checked.read_bytes(), f"WolvenKit cook drift: {checkpoint.name}/{depot_path}")
            serialize = subprocess.run([str(wkit), "convert", "serialize", str(cooked_out), "-o", str(json_out), "-v", "Quiet"], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", timeout=120)
            require(serialize.returncode == 0 and len(list(json_out.iterdir())) == 11, f"WolvenKit serialize failed for {checkpoint.name}:\n{serialize.stdout}{serialize.stderr}".rstrip())
            for depot_path, root_type in ROOT_TYPES.items():
                roundtrip = load_json(json_out / (Path(depot_path).name + ".json"))
                require(roundtrip["Header"]["WolvenKitVersion"] == "8.19.0" and roundtrip["Data"]["RootChunk"]["$type"] == root_type, f"WolvenKit round trip changed {checkpoint.name}/{depot_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wkit", type=Path, help="repeat the WolvenKit 8.19.0 cook/serialize round trip")
    parser.add_argument("--write-manifest", action="store_true", help="refresh the hash-bound Lab 5 example manifest")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.write_manifest:
        write_manifest()
    checks = [
        ("Lab 5 inventories and deterministic generation", validate_inventories_and_generation),
        ("Lab 5 projects, registration, and CR2W pairs", validate_projects_registration_and_pairs),
        ("Lab 5 root and external-child graphs", validate_graphs),
        ("Lab 5 scene and spoken localization", validate_scenes_and_localization),
        ("Lab 5 journal hierarchy and onscreen localization", validate_journal_and_onscreens),
        ("Lab 5 world/community identity", validate_world),
        ("Lab 5 voice artifact provenance", validate_audio),
        ("Lab 5 acceptance, manifest, and diagrams", validate_acceptance_manifest_and_diagrams),
        ("Lab 5 deterministic public packages", validate_packages),
    ]
    if args.wkit is not None:
        checks.append(("Lab 5 WolvenKit 8.19.0 cook and serialize round trip", lambda: run_wkit(args.wkit)))
    return 0 if all(run_check(name, function) for name, function in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
