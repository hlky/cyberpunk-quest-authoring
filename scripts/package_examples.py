#!/usr/bin/env python3
"""Create deterministic downloadable ZIPs for tutorial checkpoints.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-01-one-shot"
CHECKPOINTS = {
    "cqa-lab-01-start.zip": (
        LAB / "start",
        "CQA_Lab01_OneShot_Start",
    ),
    "cqa-lab-01-completed.zip": (
        LAB / "completed",
        "CQA_Lab01_OneShot",
    ),
}
SHARED = (LAB / "LICENSE.md",)
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def add_file(archive: ZipFile, source: Path, target: str) -> None:
    info = ZipInfo(target, ZIP_TIMESTAMP)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, source.read_bytes())


def package(source: Path, root_name: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w") as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = path.relative_to(source).as_posix()
            add_file(archive, path, f"{root_name}/{relative}")
        for shared in SHARED:
            add_file(archive, shared, f"{root_name}/LICENSE.md")


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
    for name, (source, root_name) in CHECKPOINTS.items():
        package(source, root_name, args.output / name)


if __name__ == "__main__":
    main()
