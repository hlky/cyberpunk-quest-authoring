#!/usr/bin/env python3
"""Build the deterministic Lab 3 SVG diagrams.

The exact engine graph is checked against the completed Lab 3 CR2W-JSON before
rendering.  The resource and trigger-volume figures are tutorial-owned
explanatory views of the same mod-owned resources.  Readers do not need this
script to author the resources in WolvenKit.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_quest_graph import fingerprint, load_json, parse_graph


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "examples"
    / "lab-03-boundary-check"
    / "completed"
    / "source"
    / "raw"
    / "mod"
    / "cqa"
    / "cqa003"
    / "phases"
    / "cqa003.questphase.json"
)
SOURCE_RELATIVE = SOURCE.relative_to(ROOT).as_posix()
MANIFEST = (
    ROOT
    / "examples"
    / "lab-03-boundary-check"
    / "completed"
    / "example.json"
)
ASSET_DIR = ROOT / "assets" / "diagrams" / "lab-03"
PUBLISH_DIR = ROOT / "book" / "src" / "images" / "lab-03"

QUESTPHASE_SVG = "cqa003.questphase.svg"
QUESTPHASE_LAYOUT = "cqa003.questphase.layout.json"
RESOURCE_CHAIN_SVG = "cqa003.resource-chain.svg"
TRIGGER_PLAN_SVG = "cqa003.trigger-volume-plan.svg"

PREFAB_LOCAL = "#cqa003_pr_boundary"
PREFAB_FULL = "$/mod/cqa/cqa003/#cqa003_pr_boundary"
REACH_LOCAL = "#cqa003_tr_reach"
LEAVE_LOCAL = "#cqa003_tr_leave"
MARKER_LOCAL = "#cqa003_mp_checkpoint"
CENTER_X = -1000.02
CENTER_Y = 1497.2208
REACH_RADIUS = 25
LEAVE_RADIUS = 110
REACH_HEIGHT = 12
LEAVE_HEIGHT = 16
REACH_BASE_Z = 2.3
LEAVE_BASE_Z = 0.3
REACH_POINT_COUNT = 16
LEAVE_POINT_COUNT = 20


@dataclass(frozen=True)
class GraphNodeSpec:
    quest_id: int
    title: str
    detail: str
    red_type: str
    category: str
    x: int
    y: int
    width: int
    height: int = 118


@dataclass(frozen=True)
class GraphEdgeSpec:
    source: int
    source_socket: str
    destination: int
    destination_socket: str
    path: str
    label_x: int
    label_y: int


@dataclass(frozen=True)
class RuntimeEvidence:
    status: str
    evidence_class: str
    runtime_date: str | None

    @property
    def display_class(self) -> str:
        return {
            "experimental": "Experimental",
            "runtime-proven": "Runtime-proven",
        }[self.evidence_class]

    @property
    def display_date(self) -> str:
        return self.runtime_date if self.runtime_date is not None else "Not yet recorded"

    @property
    def footer(self) -> str:
        return (
            f"{self.display_class} — runtime evidence {self.status}"
            f" • test date: {self.display_date}"
        )

    def metadata(self) -> dict[str, str | None]:
        return {
            "status": self.status,
            "class": self.evidence_class,
            "date": self.runtime_date,
        }


GRAPH_NODES = (
    GraphNodeSpec(0, "Input", "In1", "questInputNodeDefinition", "boundary", 40, 160, 180),
    GraphNodeSpec(1, "Output", "Terminating", "questOutputNodeDefinition", "boundary", 4690, 440, 180),
    GraphNodeSpec(10, "Fact guard", "cqa003_completed == 0", "questConditionNodeDefinition", "gate", 270, 160, 280),
    GraphNodeSpec(11, "Quest • Active", "cqa003", "questJournalNodeDefinition", "journal", 600, 160, 250),
    GraphNodeSpec(12, "Phase • Active", "cqa003_01", "questJournalNodeDefinition", "journal", 900, 160, 250),
    GraphNodeSpec(13, "Reach objective • Active", "cqa003_01_obj_reach", "questJournalNodeDefinition", "journal", 1200, 160, 300),
    GraphNodeSpec(14, "Mappin • Active", "disablePreviousMappins = 0", "questMappinManagerNodeDefinition", "journal", 1550, 160, 270),
    GraphNodeSpec(15, "Wait: IsInside reach", REACH_LOCAL, "questPauseConditionNodeDefinition", "gate", 1870, 160, 340),
    GraphNodeSpec(16, "Mappin • Inactive", "disablePreviousMappins = 0", "questMappinManagerNodeDefinition", "journal", 1870, 440, 280),
    GraphNodeSpec(17, "Reach objective • Succeeded", "cqa003_01_obj_reach", "questJournalNodeDefinition", "journal", 2200, 440, 310),
    GraphNodeSpec(18, "Leave objective • Active", "cqa003_01_obj_leave", "questJournalNodeDefinition", "journal", 2560, 440, 300),
    GraphNodeSpec(19, "Wait: IsOutside leave", LEAVE_LOCAL, "questPauseConditionNodeDefinition", "gate", 2910, 440, 350),
    GraphNodeSpec(20, "Leave objective • Succeeded", "cqa003_01_obj_leave", "questJournalNodeDefinition", "journal", 3310, 440, 310),
    GraphNodeSpec(21, "Phase • Succeeded", "cqa003_01", "questJournalNodeDefinition", "journal", 3670, 440, 280),
    GraphNodeSpec(22, "Set fact", "cqa003_completed = 1", "questFactsDBManagerNodeDefinition", "fact", 4000, 440, 310),
    GraphNodeSpec(23, "Quest • Succeeded", "cqa003", "questJournalNodeDefinition", "journal", 4360, 440, 280),
)


GRAPH_EDGES = (
    GraphEdgeSpec(0, "Out", 10, "In", "M 220 219 L 270 219", 245, 145),
    GraphEdgeSpec(10, "False", 1, "In", "M 410 278 L 410 780 L 4780 780 L 4780 558", 2595, 770),
    GraphEdgeSpec(10, "True", 11, "Active", "M 550 219 L 600 219", 575, 145),
    GraphEdgeSpec(11, "Out", 12, "Active", "M 850 219 L 900 219", 875, 145),
    GraphEdgeSpec(12, "Out", 13, "Active", "M 1150 219 L 1200 219", 1175, 145),
    GraphEdgeSpec(13, "Out", 14, "Active", "M 1500 219 L 1550 219", 1525, 145),
    GraphEdgeSpec(14, "Out", 15, "In", "M 1820 219 L 1870 219", 1845, 145),
    GraphEdgeSpec(15, "Out", 16, "Inactive", "M 2040 278 L 2040 440", 2130, 365),
    GraphEdgeSpec(16, "Out", 17, "Succeeded", "M 2150 499 L 2200 499", 2175, 425),
    GraphEdgeSpec(17, "Out", 18, "Active", "M 2510 499 L 2560 499", 2535, 425),
    GraphEdgeSpec(18, "Out", 19, "In", "M 2860 499 L 2910 499", 2885, 425),
    GraphEdgeSpec(19, "Out", 20, "Succeeded", "M 3260 499 L 3310 499", 3285, 425),
    GraphEdgeSpec(20, "Out", 21, "Succeeded", "M 3620 499 L 3670 499", 3645, 425),
    GraphEdgeSpec(21, "Out", 22, "In", "M 3950 499 L 4000 499", 3975, 425),
    GraphEdgeSpec(22, "Out", 23, "Succeeded", "M 4310 499 L 4360 499", 4335, 425),
    GraphEdgeSpec(23, "Out", 1, "In", "M 4640 499 L 4690 499", 4665, 425),
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text_element(
    x: float,
    y: float,
    value: object,
    css_class: str,
    *,
    anchor: str | None = None,
) -> str:
    anchor_attribute = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'<text class="{css_class}" x="{x:g}" y="{y:g}"'
        f"{anchor_attribute}>{esc(value)}</text>"
    )


def multiline_text(
    x: float,
    y: float,
    lines: Iterable[str],
    css_class: str,
    *,
    line_height: int = 21,
    anchor: str | None = None,
) -> list[str]:
    return [
        text_element(x, y + index * line_height, line, css_class, anchor=anchor)
        for index, line in enumerate(lines)
    ]


def metadata_element(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return f"<metadata>{esc(encoded)}</metadata>"


def svg_header(
    width: int,
    height: int,
    title: str,
    description: str,
    metadata: dict[str, object],
    style: str,
    markers: str,
) -> list[str]:
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!-- SPDX-License-Identifier: CC-BY-4.0 -->',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" '
            'role="img" aria-labelledby="svg-title svg-desc">'
        ),
        f'<title id="svg-title">{esc(title)}</title>',
        f'<desc id="svg-desc">{esc(description)}</desc>',
        metadata_element(metadata),
        "<defs>",
        markers,
        "<style>",
        style,
        "</style>",
        "</defs>",
    ]


COMMON_STYLE = """    .background { fill: #10151d; }
    .title { fill: #f7f9fc; font: 700 29px system-ui, sans-serif; }
    .subtitle { fill: #aeb8c8; font: 15px system-ui, sans-serif; }
    .badge { fill: #4a3200; stroke: #f5b942; stroke-width: 1.5; }
    .badge-text { fill: #ffd982; font: 700 14px system-ui, sans-serif; text-anchor: middle; }
    .panel { fill: #181f2a; stroke: #465266; stroke-width: 1.5; }
    .panel-title { fill: #f7f9fc; font: 700 18px system-ui, sans-serif; }
    .label { fill: #f7f9fc; font: 600 14px system-ui, sans-serif; }
    .detail { fill: #dce2eb; font: 12px ui-monospace, SFMono-Regular, Consolas, monospace; }
    .note { fill: #bac4d3; font: 13px system-ui, sans-serif; }
    .edge-label { fill: #d7dde7; font: 12px ui-monospace, SFMono-Regular, Consolas, monospace;
                  text-anchor: middle; paint-order: stroke; stroke: #10151d;
                  stroke-width: 5px; stroke-linejoin: round; }
"""


ARROW_MARKER = """<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M 0 0 L 10 5 L 0 10 z" fill="#c9d1dc"/>
</marker>"""


def load_runtime_evidence() -> RuntimeEvidence:
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Lab 3 completed manifest is missing: {MANIFEST}")
    manifest = load_json(MANIFEST)
    if manifest.get("id") != "cqa003":
        raise ValueError("Lab 3 completed manifest identity changed")
    evidence = manifest.get("evidence")
    runtime = evidence.get("runtime") if isinstance(evidence, dict) else None
    if not isinstance(runtime, dict):
        raise ValueError("Lab 3 completed manifest has no runtime evidence object")
    status = runtime.get("status")
    evidence_class = runtime.get("class")
    expected_class = {
        "pending": "experimental",
        "failed": "experimental",
        "passed": "runtime-proven",
    }.get(status)
    if expected_class is None or evidence_class != expected_class:
        raise ValueError("Lab 3 manifest runtime status and evidence class disagree")
    runtime_date = runtime.get("date")
    if runtime_date is not None:
        if not isinstance(runtime_date, str):
            raise ValueError("Lab 3 manifest runtime date must be null or YYYY-MM-DD")
        try:
            if date.fromisoformat(runtime_date).isoformat() != runtime_date:
                raise ValueError
        except ValueError as error:
            raise ValueError(
                "Lab 3 manifest runtime date must be null or YYYY-MM-DD"
            ) from error
    elif status != "pending":
        raise ValueError("Completed Lab 3 runtime evidence needs a date")
    return RuntimeEvidence(status, evidence_class, runtime_date)


def validate_graph_source() -> str:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Lab 3 completed graph source is missing: {SOURCE}")

    parsed_nodes, parsed_edges = parse_graph(load_json(SOURCE))
    expected_ids = tuple(node.quest_id for node in GRAPH_NODES)
    actual_ids = tuple(node.quest_id for node in parsed_nodes)
    if actual_ids != expected_ids:
        raise ValueError(
            "cqa003 completed graph node IDs changed: "
            f"expected {expected_ids}, actual {actual_ids}"
        )

    expected_types = {node.quest_id: node.red_type for node in GRAPH_NODES}
    actual_types = {node.quest_id: node.red_type for node in parsed_nodes}
    if actual_types != expected_types:
        raise ValueError(
            "cqa003 completed graph node types changed: "
            f"expected {expected_types}, actual {actual_types}"
        )

    expected_edges = tuple(
        (
            edge.source,
            edge.source_socket,
            edge.destination,
            edge.destination_socket,
        )
        for edge in GRAPH_EDGES
    )
    actual_edges = tuple(
        (
            edge.source,
            edge.source_socket,
            edge.destination,
            edge.destination_socket,
        )
        for edge in parsed_edges
    )
    if actual_edges != expected_edges:
        raise ValueError(
            "cqa003 completed graph edges changed: "
            f"expected {expected_edges}, actual {actual_edges}"
        )

    if len(parsed_nodes) != 16 or len(parsed_edges) != 16:
        raise ValueError("cqa003 completed graph must contain exactly 16 nodes and 16 edges")
    return fingerprint(parsed_nodes, parsed_edges)


def render_graph_svg(
    source_fingerprint: str, evidence: RuntimeEvidence
) -> str:
    style = COMMON_STYLE + """    .graph-edge { fill: none; stroke: #c9d1dc; stroke-width: 2.2; marker-end: url(#arrow); }
    .node-shape { stroke: #e6e9ef; stroke-width: 1.5; }
    .boundary { fill: #4b5563; }
    .gate { fill: #9a6700; }
    .fact { fill: #6d3ea0; }
    .journal { fill: #247a4b; }
    .node-id { fill: #f7f8fa; font: 12px ui-monospace, SFMono-Regular, Consolas, monospace; }
    .node-title { fill: #ffffff; font: 700 16px system-ui, sans-serif; }
    .node-detail { fill: #f3f5f8; font: 12px ui-monospace, SFMono-Regular, Consolas, monospace; }
    .node-type { fill: #d2d9e3; font: 10px ui-monospace, SFMono-Regular, Consolas, monospace; }
    .legend-shape { stroke: #e6e9ef; stroke-width: 1.3; }
"""
    description = (
        "Exact cqa003 Boundary Check quest graph with 16 nodes and 16 edges. "
        "The false one-shot guard exits immediately; the true path activates "
        "the reach objective and mappin, waits for IsInside, activates the leave "
        "objective, waits for IsOutside, records completion, and exits. "
        f"Diagram evidence state: {evidence.status}; runtime test date: "
        f"{evidence.display_date}."
    )
    parts = svg_header(
        4910,
        920,
        f"cqa003 Boundary Check exact quest graph — {evidence.display_class}",
        description,
        {
            "edge_count": 16,
            "node_count": 16,
            "source": SOURCE_RELATIVE,
            "source_fingerprint": source_fingerprint,
            "evidence": evidence.metadata(),
        },
        style,
        ARROW_MARKER,
    )
    parts.extend(
        [
            '<rect class="background" width="4910" height="920"/>',
            text_element(42, 49, "cqa003 Boundary Check — exact engine graph", "title"),
            text_element(
                42,
                79,
                "16 nodes • 16 edges • socket names are serialized graph connections",
                "subtitle",
            ),
            '<rect class="badge" x="4650" y="27" width="218" height="38" rx="19"/>',
            text_element(
                4759,
                52,
                f"cqa003 • {evidence.display_class}",
                "badge-text",
            ),
        ]
    )

    for edge in GRAPH_EDGES:
        label = f"{edge.source_socket} → {edge.destination_socket}"
        parts.extend(
            [
                (
                    '<g class="graph-edge-group" '
                    f'data-source="{edge.source}" data-source-socket="{esc(edge.source_socket)}" '
                    f'data-destination="{edge.destination}" '
                    f'data-destination-socket="{esc(edge.destination_socket)}">'
                ),
                (
                    f"<title>ID {edge.source} {esc(edge.source_socket)} to "
                    f"ID {edge.destination} {esc(edge.destination_socket)}</title>"
                ),
                f'<path class="graph-edge" d="{edge.path}"/>',
                text_element(edge.label_x, edge.label_y, label, "edge-label"),
                "</g>",
            ]
        )

    for node in GRAPH_NODES:
        accessible = f"ID {node.quest_id}, {node.title}, {node.detail}, {node.red_type}"
        parts.append(
            f'<g class="graph-node" data-node-id="{node.quest_id}" '
            f'data-node-type="{esc(node.red_type)}" aria-label="{esc(accessible)}">'
        )
        if node.category == "gate":
            cut = 22
            points = (
                f"{node.x + cut},{node.y} "
                f"{node.x + node.width - cut},{node.y} "
                f"{node.x + node.width},{node.y + node.height / 2:g} "
                f"{node.x + node.width - cut},{node.y + node.height} "
                f"{node.x + cut},{node.y + node.height} "
                f"{node.x},{node.y + node.height / 2:g}"
            )
            parts.append(f'<polygon class="node-shape gate" points="{points}"/>')
        else:
            radius = node.height // 2 if node.category == "boundary" else 10
            parts.append(
                f'<rect class="node-shape {node.category}" x="{node.x}" y="{node.y}" '
                f'width="{node.width}" height="{node.height}" rx="{radius}"/>'
            )
        parts.extend(
            [
                text_element(node.x + 14, node.y + 21, f"ID {node.quest_id}", "node-id"),
                text_element(node.x + 14, node.y + 49, node.title, "node-title"),
                text_element(node.x + 14, node.y + 75, node.detail, "node-detail"),
                text_element(node.x + 14, node.y + 101, node.red_type, "node-type"),
                "</g>",
            ]
        )

    parts.extend(
        [
            '<rect class="legend-shape boundary" x="42" y="844" width="42" height="24" rx="12"/>',
            text_element(96, 862, "boundary", "note"),
            '<polygon class="legend-shape gate" points="205,844 237,844 247,856 237,868 205,868 195,856"/>',
            text_element(259, 862, "condition / wait", "note"),
            '<rect class="legend-shape journal" x="407" y="844" width="42" height="24" rx="5"/>',
            text_element(461, 862, "journal / mappin", "note"),
            '<rect class="legend-shape fact" x="626" y="844" width="42" height="24" rx="5"/>',
            text_element(680, 862, "fact", "note"),
            '<path class="graph-edge" d="M 770 856 L 825 856"/>',
            text_element(842, 862, "normal execution", "note"),
            text_element(
                4868,
                862,
                evidence.footer,
                "note",
                anchor="end",
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def render_graph_layout(
    source_fingerprint: str, evidence: RuntimeEvidence
) -> str:
    layout = {
        "schema_version": 1,
        "title": (
            "cqa003 Boundary Check root questphase — "
            f"{evidence.display_class}"
        ),
        "source_fingerprint": source_fingerprint,
        "canvas": {"width": 4910, "height": 920},
        "nodes": {
            str(node.quest_id): {
                "x": node.x,
                "y": node.y,
                "width": node.width,
                "height": node.height,
            }
            for node in GRAPH_NODES
        },
        "routes": {
            "10.False->1.In": [[410, 780], [4780, 780], [4780, 558]],
        },
    }
    return json.dumps(layout, indent=2, ensure_ascii=False) + "\n"


def render_resource_chain_svg(evidence: RuntimeEvidence) -> str:
    style = COMMON_STYLE + """    .lookup-edge { fill: none; stroke: #d8dee9; stroke-width: 2.2; stroke-dasharray: 3 8;
                   stroke-linecap: round; marker-end: url(#arrow); }
    .quest-resource { fill: #293a63; stroke: #84a9ff; stroke-width: 2; }
    .world-resource { fill: #174f54; stroke: #62d7dc; stroke-width: 2; }
    .descriptor { fill: #233b46; stroke: #88ced2; stroke-width: 1.5; }
    .owned-node { fill: #255a55; stroke: #83e1cf; stroke-width: 1.5; }
    .resource-title { fill: #ffffff; font: 700 16px system-ui, sans-serif; }
    .resource-type { fill: #dce2eb; font: 12px ui-monospace, SFMono-Regular, Consolas, monospace; }
    .resource-value { fill: #f3f5f8; font: 11px ui-monospace, SFMono-Regular, Consolas, monospace; }
    .ownership-note { fill: #8ee6d9; font: 700 12px system-ui, sans-serif; letter-spacing: .04em; }
"""
    description = (
        "Resource ownership and NodeRef lookup chain for cqa003. "
        "The questphase phasePrefabs entry matches the Quest descriptor's prefab "
        "root, which resolves the quest sector containing reach and leave triggers. "
        "A separate AlwaysLoaded descriptor resolves the sector that owns the marker. "
        f"Diagram evidence state: {evidence.status}; runtime test date: "
        f"{evidence.display_date}."
    )
    parts = svg_header(
        1600,
        900,
        f"cqa003 resource ownership and reference chain — {evidence.display_class}",
        description,
        {
            "evidence": evidence.metadata(),
            "sources": [
                "mod/cqa/cqa003/phases/cqa003.questphase",
                "mod/cqa/cqa003/world/cqa003_boundary.streamingblock",
                "mod/cqa/cqa003/world/cqa003_boundary.streamingsector",
                "mod/cqa/cqa003/world/cqa003_always_loaded.streamingsector",
            ],
        },
        style,
        ARROW_MARKER,
    )
    parts.extend(
        [
            '<rect class="background" width="1600" height="900"/>',
            text_element(48, 52, "cqa003 resource ownership and reference chain", "title"),
            text_element(
                48,
                82,
                "Dotted arrows are resource or NodeRef lookups; nesting shows ownership.",
                "subtitle",
            ),
            '<rect class="badge" x="1340" y="29" width="212" height="38" rx="19"/>',
            text_element(
                1446,
                54,
                f"cqa003 • {evidence.display_class}",
                "badge-text",
            ),
            '<rect class="panel" x="28" y="110" width="1544" height="742" rx="16"/>',
            text_element(52, 142, "QUESTPHASE DEPENDENCY", "ownership-note"),
            '<rect class="quest-resource" x="52" y="230" width="360" height="210" rx="12"/>',
            text_element(76, 266, "questQuestPhaseResource", "resource-title"),
            *multiline_text(
                76,
                296,
                (
                    "phases\\cqa003.questphase",
                    "phasePrefabs[0].prefabNodeRef",
                    PREFAB_LOCAL,
                ),
                "resource-type",
                line_height=28,
            ),
            text_element(76, 409, "Declares dependency; does not place nodes", "note"),
            '<rect class="world-resource" x="470" y="145" width="500" height="625" rx="14"/>',
            text_element(494, 180, "worldStreamingBlock", "resource-title"),
            text_element(494, 205, "world\\cqa003_boundary.streamingblock", "resource-type"),
            text_element(494, 232, "OWNS TWO DESCRIPTORS", "ownership-note"),
            '<rect class="descriptor" x="500" y="258" width="440" height="205" rx="10"/>',
            text_element(522, 291, "Quest descriptor", "resource-title"),
            *multiline_text(
                522,
                320,
                (
                    "category: Quest",
                    "questPrefabNodeRef:",
                    PREFAB_FULL,
                    "data → cqa003_boundary.streamingsector",
                ),
                "resource-value",
                line_height=27,
            ),
            '<rect class="descriptor" x="500" y="520" width="440" height="180" rx="10"/>',
            text_element(522, 553, "AlwaysLoaded descriptor", "resource-title"),
            *multiline_text(
                522,
                582,
                (
                    "category: AlwaysLoaded",
                    "data →",
                    "cqa003_always_loaded.streamingsector",
                ),
                "resource-value",
                line_height=29,
            ),
            '<rect class="world-resource" x="1040" y="145" width="500" height="340" rx="14"/>',
            text_element(1064, 180, "Quest streaming sector", "resource-title"),
            text_element(1064, 205, "cqa003_boundary.streamingsector", "resource-type"),
            text_element(1064, 232, "OWNS PLACED TRIGGER NODES", "ownership-note"),
            '<rect class="owned-node" x="1070" y="260" width="210" height="175" rx="10"/>',
            text_element(1091, 294, "Reach trigger", "resource-title"),
            *multiline_text(
                1091,
                324,
                (REACH_LOCAL, "full child ref:", f"…/{REACH_LOCAL}", "r=25m • h=12m"),
                "resource-value",
                line_height=25,
            ),
            '<rect class="owned-node" x="1300" y="260" width="210" height="175" rx="10"/>',
            text_element(1321, 294, "Leave trigger", "resource-title"),
            *multiline_text(
                1321,
                324,
                (LEAVE_LOCAL, "full child ref:", f"…/{LEAVE_LOCAL}", "r=110m • h=16m"),
                "resource-value",
                line_height=25,
            ),
            '<rect class="world-resource" x="1040" y="520" width="500" height="210" rx="14"/>',
            text_element(1064, 555, "AlwaysLoaded streaming sector", "resource-title"),
            text_element(1064, 580, "cqa003_always_loaded.streamingsector", "resource-type"),
            text_element(1064, 608, "OWNS PLACED MARKER NODE", "ownership-note"),
            '<rect class="owned-node" x="1080" y="630" width="420" height="70" rx="10"/>',
            text_element(1102, 659, "Checkpoint marker", "resource-title"),
            text_element(1102, 684, f"{MARKER_LOCAL}  •  full child ref …/{MARKER_LOCAL}", "resource-value"),
            '<path class="lookup-edge" d="M 412 335 H 500"/>',
            text_element(456, 320, "prefab root", "edge-label"),
            '<path class="lookup-edge" d="M 940 360 H 1040"/>',
            text_element(990, 345, "resource path", "edge-label"),
            '<path class="lookup-edge" d="M 940 610 H 1040"/>',
            text_element(990, 595, "resource path", "edge-label"),
            text_element(
                52,
                818,
                "Matching the prefab root permits lookup; the sector still owns each concrete placed node.",
                "note",
            ),
            text_element(
                1540,
                818,
                evidence.footer,
                "note",
                anchor="end",
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def svg_polygon_points(
    center_x: float,
    center_y: float,
    radius: float,
    count: int,
) -> str:
    return " ".join(
        f"{center_x + math.cos(2 * math.pi * index / count) * radius:.3f},"
        f"{center_y + math.sin(2 * math.pi * index / count) * radius:.3f}"
        for index in range(count)
    )


def render_trigger_plan_svg(evidence: RuntimeEvidence) -> str:
    style = COMMON_STYLE + """    .leave-volume { fill: #174f54; fill-opacity: .32; stroke: #62d7dc; stroke-width: 3;
                    stroke-dasharray: 10 8; }
    .reach-volume { fill: #6b4a00; fill-opacity: .56; stroke: #f5b942; stroke-width: 3; }
    .center-line { fill: none; stroke: #9aa4b2; stroke-width: 1.5; stroke-dasharray: 4 6; }
    .player-path { fill: none; stroke: #f2f5f8; stroke-width: 4; stroke-linecap: round;
                   marker-end: url(#arrow); }
    .marker-pin { fill: #c35a91; stroke: #ffadd4; stroke-width: 2; }
    .step { fill: #293a63; stroke: #9cb8ff; stroke-width: 2; }
    .step-number { fill: #ffffff; font: 700 14px system-ui, sans-serif; text-anchor: middle; }
    .dimension { fill: none; stroke: #d8dee9; stroke-width: 1.5; marker-start: url(#dim-arrow);
                 marker-end: url(#dim-arrow); }
    .prism-line { stroke-width: 3; }
    .leave-line { stroke: #62d7dc; stroke-dasharray: 10 8; }
    .reach-line { stroke: #f5b942; }
    .volume-label { fill: #ffffff; font: 700 15px system-ui, sans-serif;
                    paint-order: stroke; stroke: #10151d; stroke-width: 4px; }
"""
    markers = ARROW_MARKER + """
<marker id="dim-arrow" viewBox="0 0 10 10" refX="5" refY="5"
        markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M 10 0 L 0 5 L 10 10" fill="none" stroke="#d8dee9" stroke-width="1.5"/>
</marker>"""
    description = (
        "Top-down and orthographic elevation views of the cqa003 concentric "
        "polygonal trigger prisms centered at x minus 1000.02 and y 1497.2208. "
        "The reach trigger is a 16-gon with circumradius 25 metres, base z 2.3, "
        "and height 12 metres; the leave trigger is a 20-gon with circumradius "
        "110 metres, base z 0.3, and height 16 metres. Both volume centers are "
        "at z 8.3. A marker sits at the common x and y center and a player path "
        "enters the reach volume before leaving the larger volume. "
        f"Diagram evidence state: {evidence.status}; runtime test date: "
        f"{evidence.display_date}."
    )
    parts = svg_header(
        1600,
        900,
        f"cqa003 polygonal trigger-volume plan — {evidence.display_class}",
        description,
        {
            "center": {"x": CENTER_X, "y": CENTER_Y},
            "leave": {
                "base_z": LEAVE_BASE_Z,
                "height_m": LEAVE_HEIGHT,
                "point_count": LEAVE_POINT_COUNT,
                "circumradius_m": LEAVE_RADIUS,
                "top_z": LEAVE_BASE_Z + LEAVE_HEIGHT,
            },
            "reach": {
                "base_z": REACH_BASE_Z,
                "height_m": REACH_HEIGHT,
                "point_count": REACH_POINT_COUNT,
                "circumradius_m": REACH_RADIUS,
                "top_z": REACH_BASE_Z + REACH_HEIGHT,
            },
            "evidence": evidence.metadata(),
        },
        style,
        markers,
    )
    parts.extend(
        [
            '<rect class="background" width="1600" height="900"/>',
            text_element(48, 52, "cqa003 trigger-volume plan", "title"),
            text_element(
                48,
                82,
                f"Concentric 16/20-gon prisms centered at ({CENTER_X}, {CENTER_Y}) • dimensions in metres",
                "subtitle",
            ),
            '<rect class="badge" x="1340" y="29" width="212" height="38" rx="19"/>',
            text_element(
                1446,
                54,
                f"cqa003 • {evidence.display_class}",
                "badge-text",
            ),
            '<rect class="panel" x="30" y="112" width="900" height="720" rx="16"/>',
            text_element(56, 148, "Top-down plan", "panel-title"),
            f'<polygon class="leave-volume" points="{svg_polygon_points(480, 470, 270, LEAVE_POINT_COUNT)}"/>',
            f'<polygon class="reach-volume" points="{svg_polygon_points(480, 470, 270 * REACH_RADIUS / LEAVE_RADIUS, REACH_POINT_COUNT)}"/>',
            '<path class="center-line" d="M 190 470 H 770 M 480 180 V 760"/>',
            '<path class="player-path" d="M 110 720 C 190 635 280 575 390 520 C 430 500 460 480 480 470 C 585 410 690 300 835 170"/>',
            '<circle class="step" cx="170" cy="655" r="15"/>',
            text_element(170, 660, "1", "step-number"),
            text_element(105, 684, "approach", "label"),
            '<circle class="step" cx="447" cy="487" r="15"/>',
            text_element(447, 492, "2", "step-number"),
            text_element(382, 545, "IsInside reach", "label"),
            '<circle class="step" cx="756" cy="241" r="15"/>',
            text_element(756, 246, "3", "step-number"),
            text_element(700, 215, "IsOutside leave", "label"),
            '<path class="marker-pin" d="M 480 427 C 458 427 446 444 446 461 C 446 487 480 516 480 516 C 480 516 514 487 514 461 C 514 444 502 427 480 427 Z"/>',
            '<circle cx="480" cy="461" r="9" fill="#10151d"/>',
            text_element(526, 451, "checkpoint marker", "label"),
            text_element(526, 474, "same X/Y center", "detail"),
            text_element(222, 184, "Leave trigger", "volume-label"),
            text_element(222, 207, "20-gon • circumradius 110m • dashed", "detail"),
            text_element(495, 360, "Reach trigger", "volume-label"),
            text_element(495, 383, "16-gon • circumradius 25m • solid", "detail"),
            '<path class="dimension" d="M 480 774 H 750"/>',
            text_element(615, 801, "110m radius", "edge-label"),
            text_element(
                56,
                814,
                "Player sequence: enter the 25m reach prism, then exit the 110m leave prism.",
                "note",
            ),
            '<rect class="panel" x="970" y="112" width="600" height="720" rx="16"/>',
            text_element(996, 148, "Orthographic elevation", "panel-title"),
            text_element(996, 174, "World-Z bases and tops • both centers at z = 8.3", "note"),
            '<path class="center-line" d="M 1020 510 H 1520"/>',
            '<rect class="leave-volume prism-line" x="1085" y="310" width="370" height="400"/>',
            '<rect class="reach-volume prism-line" x="1228" y="360" width="84" height="300"/>',
            '<path class="dimension" d="M 1490 310 V 710"/>',
            text_element(1512, 517, "h = 16m", "volume-label"),
            '<path class="dimension" d="M 1190 360 V 660"/>',
            text_element(1172, 517, "h = 12m", "volume-label", anchor="end"),
            text_element(1004, 250, "Leave prism", "volume-label"),
            text_element(1004, 274, "20-gon prism • circumradius 110m", "detail"),
            text_element(1004, 370, "Reach prism", "volume-label"),
            text_element(1004, 394, "16-gon prism • circumradius 25m", "detail"),
            text_element(1458, 304, "top z = 16.3", "detail"),
            text_element(1458, 730, "base z = 0.3", "detail"),
            text_element(1218, 354, "top z = 14.3", "detail", anchor="end"),
            text_element(1218, 680, "base z = 2.3", "detail", anchor="end"),
            text_element(1518, 505, "center z = 8.3", "detail", anchor="end"),
            text_element(1270, 785, "Orthographic resource geometry — not a terrain profile", "note", anchor="middle"),
            text_element(
                1540,
                818,
                evidence.footer,
                "note",
                anchor="end",
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def expected_outputs() -> tuple[dict[str, str], dict[str, str]]:
    source_fingerprint = validate_graph_source()
    evidence = load_runtime_evidence()
    svg_outputs = {
        QUESTPHASE_SVG: render_graph_svg(source_fingerprint, evidence),
        RESOURCE_CHAIN_SVG: render_resource_chain_svg(evidence),
        TRIGGER_PLAN_SVG: render_trigger_plan_svg(evidence),
    }
    asset_outputs = {
        QUESTPHASE_LAYOUT: render_graph_layout(source_fingerprint, evidence),
        **svg_outputs,
    }
    return asset_outputs, svg_outputs


def write_outputs(
    asset_outputs: dict[str, str], publish_outputs: dict[str, str]
) -> None:
    for directory, outputs in (
        (ASSET_DIR, asset_outputs),
        (PUBLISH_DIR, publish_outputs),
    ):
        directory.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            path = directory / name
            path.write_text(content, encoding="utf-8", newline="")


def check_outputs(
    asset_outputs: dict[str, str], publish_outputs: dict[str, str]
) -> None:
    stale: list[str] = []
    for directory, outputs in (
        (ASSET_DIR, asset_outputs),
        (PUBLISH_DIR, publish_outputs),
    ):
        for name, expected in outputs.items():
            path = directory / name
            if not path.is_file() or path.read_text(encoding="utf-8") != expected:
                stale.append(path.relative_to(ROOT).as_posix())
    if stale:
        raise SystemExit("stale or missing Lab 3 diagrams: " + ", ".join(stale))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that both diagram directories match a fresh deterministic render",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asset_outputs, publish_outputs = expected_outputs()
    if args.check:
        check_outputs(asset_outputs, publish_outputs)
        verb = "checked"
    else:
        write_outputs(asset_outputs, publish_outputs)
        verb = "wrote"

    print(
        f"{verb} {len(publish_outputs)} Lab 3 SVGs in each of 2 directories "
        f"plus {QUESTPHASE_LAYOUT} in assets"
    )
    for name, content in asset_outputs.items():
        print(f"  {name}: {len(content.encode('utf-8'))} bytes sha256:{sha256_text(content)}")


if __name__ == "__main__":
    main()
