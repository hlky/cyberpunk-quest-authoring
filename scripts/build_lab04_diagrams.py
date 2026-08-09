#!/usr/bin/env python3
"""Build deterministic exact and conceptual SVGs for Lab 4.

The root and child graph figures are checked against their completed
CR2W-JSON sources before rendering. The resource and handoff figures are
tutorial-owned conceptual diagrams. Readers do not need this script.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from render_quest_graph import fingerprint, load_json, parse_graph  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-04-handoff-point" / "completed"
RAW_PHASES = LAB / "source" / "raw" / "mod" / "cqa" / "cqa004" / "phases"
ROOT_SOURCE = RAW_PHASES / "cqa004.questphase.json"
CHILD_SOURCE = RAW_PHASES / "cqa004_boundary.questphase.json"
ACCEPTANCE = LAB / "runtime-acceptance.json"
ASSET_DIR = ROOT / "assets" / "diagrams" / "lab-04"
PUBLISH_DIR = ROOT / "book" / "src" / "images" / "lab-04"


@dataclass(frozen=True)
class NodeSpec:
    quest_id: int
    title: str
    detail: str
    red_type: str
    category: str
    x: int
    y: int
    width: int
    height: int = 116


@dataclass(frozen=True)
class EdgeSpec:
    source: int
    source_socket: str
    destination: int
    destination_socket: str
    route: tuple[tuple[int, int], ...] = ()


ROOT_NODES = (
    NodeSpec(0, "Input", "In1", "questInputNodeDefinition", "boundary", 40, 145, 170),
    NodeSpec(1, "Output", "Terminating • Out1", "questOutputNodeDefinition", "boundary", 3590, 410, 210),
    NodeSpec(10, "Fact guard", "cqa004_completed == 0", "questConditionNodeDefinition", "gate", 260, 145, 280),
    NodeSpec(11, "Quest • Active", "cqa004", "questJournalNodeDefinition", "journal", 590, 145, 250),
    NodeSpec(12, "Phase • Active", "cqa004_01", "questJournalNodeDefinition", "journal", 890, 145, 250),
    NodeSpec(13, "External child", "cqa004_boundary.questphase", "questPhaseNodeDefinition", "phase", 1190, 145, 330),
    NodeSpec(14, "Confirmation • Active", "cqa004_01_obj_confirm", "questJournalNodeDefinition", "journal", 1570, 410, 310),
    NodeSpec(15, "Wait", "30 real-time seconds", "questPauseConditionNodeDefinition", "gate", 1930, 410, 280),
    NodeSpec(16, "Confirmation • Succeeded", "cqa004_01_obj_confirm", "questJournalNodeDefinition", "journal", 2260, 410, 320),
    NodeSpec(17, "Phase • Succeeded", "cqa004_01", "questJournalNodeDefinition", "journal", 2630, 410, 270),
    NodeSpec(18, "Set fact", "cqa004_completed = 1", "questFactsDBManagerNodeDefinition", "fact", 2950, 410, 260),
    NodeSpec(19, "Quest • Succeeded", "cqa004", "questJournalNodeDefinition", "journal", 3260, 410, 250),
)

ROOT_EDGES = (
    EdgeSpec(0, "Out", 10, "In"),
    EdgeSpec(10, "False", 1, "In", ((400, 710), (3590, 710))),
    EdgeSpec(10, "True", 11, "Active"),
    EdgeSpec(11, "Out", 12, "Active"),
    EdgeSpec(12, "Out", 13, "In1"),
    EdgeSpec(13, "Out1", 14, "Active", ((1355, 335), (1725, 335))),
    EdgeSpec(14, "Out", 15, "In"),
    EdgeSpec(15, "Out", 16, "Succeeded"),
    EdgeSpec(16, "Out", 17, "Succeeded"),
    EdgeSpec(17, "Out", 18, "In"),
    EdgeSpec(18, "Out", 19, "Succeeded"),
    EdgeSpec(19, "Out", 1, "In"),
)

CHILD_NODES = (
    NodeSpec(0, "Input", "In1", "questInputNodeDefinition", "boundary", 40, 150, 170),
    NodeSpec(1, "Output", "Terminating • Out1", "questOutputNodeDefinition", "boundary", 3110, 150, 210),
    NodeSpec(10, "Reach • Active", "cqa004_01_obj_reach", "questJournalNodeDefinition", "journal", 260, 150, 280),
    NodeSpec(11, "Mappin • Active", "disablePreviousMappins = 0", "questMappinManagerNodeDefinition", "journal", 590, 150, 290),
    NodeSpec(12, "Wait • IsInside", "#cqa004_tr_reach", "questPauseConditionNodeDefinition", "gate", 930, 150, 290),
    NodeSpec(13, "Mappin • Inactive", "disablePreviousMappins = 0", "questMappinManagerNodeDefinition", "journal", 1270, 150, 300),
    NodeSpec(14, "Reach • Succeeded", "cqa004_01_obj_reach", "questJournalNodeDefinition", "journal", 1620, 150, 290),
    NodeSpec(15, "Leave • Active", "cqa004_01_obj_leave", "questJournalNodeDefinition", "journal", 1960, 150, 280),
    NodeSpec(16, "Wait • IsOutside", "#cqa004_tr_leave", "questPauseConditionNodeDefinition", "gate", 2290, 150, 290),
    NodeSpec(17, "Leave • Succeeded", "cqa004_01_obj_leave", "questJournalNodeDefinition", "journal", 2630, 150, 300),
)

CHILD_EDGES = (
    EdgeSpec(0, "Out", 10, "Active"),
    EdgeSpec(10, "Out", 11, "Active"),
    EdgeSpec(11, "Out", 12, "In"),
    EdgeSpec(12, "Out", 13, "Inactive"),
    EdgeSpec(13, "Out", 14, "Succeeded"),
    EdgeSpec(14, "Out", 15, "Active"),
    EdgeSpec(15, "Out", 16, "In"),
    EdgeSpec(16, "Out", 17, "Succeeded"),
    EdgeSpec(17, "Out", 1, "In"),
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def evidence_label() -> str:
    record = load_json(ACCEPTANCE)
    status = record.get("status")
    evidence_class = record.get("evidence_class")
    expected = {
        "pending": "experimental",
        "failed": "experimental",
        "passed": "runtime-proven",
    }.get(status)
    if expected is None or evidence_class != expected:
        raise ValueError("Lab 4 acceptance status and evidence class disagree")
    return "Runtime-proven" if evidence_class == "runtime-proven" else "Experimental"


def graph_fingerprint(
    source: Path,
    nodes: tuple[NodeSpec, ...],
    edges: tuple[EdgeSpec, ...],
) -> str:
    parsed_nodes, parsed_edges = parse_graph(load_json(source))
    actual_nodes = tuple((node.quest_id, node.red_type) for node in parsed_nodes)
    expected_nodes = tuple((node.quest_id, node.red_type) for node in nodes)
    if actual_nodes != expected_nodes:
        raise ValueError(
            f"{source.name}: node contract changed: "
            f"expected {expected_nodes}, actual {actual_nodes}"
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
    expected_edges = tuple(
        sorted(
            (
                edge.source,
                edge.source_socket,
                edge.destination,
                edge.destination_socket,
            )
            for edge in edges
        )
    )
    if actual_edges != expected_edges:
        raise ValueError(
            f"{source.name}: edge contract changed: "
            f"expected {expected_edges}, actual {actual_edges}"
        )
    return fingerprint(parsed_nodes, parsed_edges)


STYLE = """    .bg { fill: #10151d; }
    .title { fill: #f7f9fc; font: 700 28px system-ui, sans-serif; }
    .subtitle { fill: #aeb8c8; font: 14px system-ui, sans-serif; }
    .badge { fill: #4a3200; stroke: #f5b942; stroke-width: 1.5; }
    .badge-text { fill: #ffd982; font: 700 14px system-ui, sans-serif; text-anchor: middle; }
    .edge { fill: none; stroke: #c9d1dc; stroke-width: 2.1; marker-end: url(#arrow); }
    .edge-label { fill: #e0e5ed; font: 12px ui-monospace, Consolas, monospace;
                  text-anchor: middle; paint-order: stroke; stroke: #10151d;
                  stroke-width: 5px; stroke-linejoin: round; }
    .node { stroke: #e6e9ef; stroke-width: 1.5; }
    .boundary { fill: #4b5563; }
    .gate { fill: #956600; }
    .journal { fill: #247a4b; }
    .phase { fill: #315f9a; }
    .fact { fill: #6d3ea0; }
    .node-id { fill: #f7f8fa; font: 12px ui-monospace, Consolas, monospace; }
    .node-title { fill: #ffffff; font: 700 16px system-ui, sans-serif; }
    .node-detail { fill: #f3f5f8; font: 12px ui-monospace, Consolas, monospace; }
    .node-type { fill: #d2d9e3; font: 10px ui-monospace, Consolas, monospace; }
    .panel { fill: #181f2a; stroke: #506078; stroke-width: 1.5; }
    .panel-blue { fill: #182b49; stroke: #78a9ff; stroke-width: 2; }
    .panel-green { fill: #173d38; stroke: #68d8c5; stroke-width: 2; }
    .panel-amber { fill: #493510; stroke: #f3be55; stroke-width: 2; }
    .panel-title { fill: #ffffff; font: 700 18px system-ui, sans-serif; }
    .label { fill: #f7f9fc; font: 600 14px system-ui, sans-serif; }
    .detail { fill: #dce2eb; font: 12px ui-monospace, Consolas, monospace; }
    .note { fill: #bac4d3; font: 13px system-ui, sans-serif; }
    .warn { fill: #ffd982; font: 600 13px system-ui, sans-serif; }
    .dashed { fill: none; stroke: #f3be55; stroke-width: 2; stroke-dasharray: 7 7; }
"""


def svg_open(
    width: int,
    height: int,
    title: str,
    description: str,
    metadata: dict[str, object],
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
        "<metadata>"
        + esc(json.dumps(metadata, sort_keys=True, separators=(",", ":")))
        + "</metadata>",
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#c9d1dc"/></marker>',
        "<style>",
        STYLE,
        "</style>",
        "</defs>",
        f'<rect class="bg" width="{width}" height="{height}"/>',
    ]


def text(
    x: float,
    y: float,
    value: object,
    css_class: str,
    *,
    anchor: str | None = None,
) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text class="{css_class}" x="{x:g}" y="{y:g}"{anchor_attr}>{esc(value)}</text>'


def box_edge(
    source: NodeSpec,
    destination: NodeSpec,
    route: tuple[tuple[int, int], ...],
) -> tuple[str, float, float]:
    start = (source.x + source.width, source.y + source.height / 2)
    end = (destination.x, destination.y + destination.height / 2)
    points = (start, *route, end)
    if route:
        path = " ".join(
            [f"M {points[0][0]:g} {points[0][1]:g}"]
            + [f"L {point[0]:g} {point[1]:g}" for point in points[1:]]
        )
        longest = max(
            zip(points, points[1:]),
            key=lambda pair: (pair[1][0] - pair[0][0]) ** 2
            + (pair[1][1] - pair[0][1]) ** 2,
        )
        label_x = (longest[0][0] + longest[1][0]) / 2
        label_y = (longest[0][1] + longest[1][1]) / 2 - 9
    else:
        delta = max(40.0, abs(end[0] - start[0]) * 0.38)
        path = (
            f"M {start[0]:g} {start[1]:g} "
            f"C {start[0] + delta:g} {start[1]:g}, "
            f"{end[0] - delta:g} {end[1]:g}, {end[0]:g} {end[1]:g}"
        )
        label_x = (start[0] + end[0]) / 2
        label_y = (start[1] + end[1]) / 2 - 10
    return path, label_x, label_y


def render_graph(
    title_value: str,
    subtitle: str,
    width: int,
    height: int,
    source: Path,
    nodes: tuple[NodeSpec, ...],
    edges: tuple[EdgeSpec, ...],
    source_fingerprint: str,
    evidence: str,
) -> str:
    description = (
        f"Exact {title_value} graph with {len(nodes)} nodes and {len(edges)} edges. "
        "Socket labels come from serialized graph connections. "
        f"Runtime evidence remains {evidence}."
    )
    parts = svg_open(
        width,
        height,
        title_value,
        description,
        {
            "source": source.relative_to(ROOT).as_posix(),
            "source_fingerprint": source_fingerprint,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "evidence_class": evidence,
        },
    )
    parts.extend(
        [
            text(40, 48, title_value, "title"),
            text(40, 77, subtitle, "subtitle"),
            f'<rect class="badge" x="{width - 230}" y="27" width="190" height="36" rx="18"/>',
            text(width - 135, 51, evidence, "badge-text"),
        ]
    )
    node_map = {node.quest_id: node for node in nodes}
    for edge in edges:
        path, label_x, label_y = box_edge(
            node_map[edge.source],
            node_map[edge.destination],
            edge.route,
        )
        parts.extend(
            [
                (
                    f'<g data-source="{edge.source}" '
                    f'data-source-socket="{esc(edge.source_socket)}" '
                    f'data-destination="{edge.destination}" '
                    f'data-destination-socket="{esc(edge.destination_socket)}">'
                ),
                f'<path class="edge" d="{path}"/>',
                text(
                    label_x,
                    label_y,
                    f"{edge.source_socket} → {edge.destination_socket}",
                    "edge-label",
                ),
                "</g>",
            ]
        )
    for node in nodes:
        parts.append(
            f'<g data-node-id="{node.quest_id}" data-node-type="{esc(node.red_type)}">'
        )
        if node.category == "gate":
            cut = 20
            points = (
                f"{node.x + cut},{node.y} {node.x + node.width - cut},{node.y} "
                f"{node.x + node.width},{node.y + node.height / 2:g} "
                f"{node.x + node.width - cut},{node.y + node.height} "
                f"{node.x + cut},{node.y + node.height} "
                f"{node.x},{node.y + node.height / 2:g}"
            )
            parts.append(f'<polygon class="node gate" points="{points}"/>')
        else:
            radius = node.height // 2 if node.category == "boundary" else 10
            parts.append(
                f'<rect class="node {node.category}" x="{node.x}" y="{node.y}" '
                f'width="{node.width}" height="{node.height}" rx="{radius}"/>'
            )
        parts.extend(
            [
                text(node.x + 14, node.y + 21, f"ID {node.quest_id}", "node-id"),
                text(node.x + 14, node.y + 48, node.title, "node-title"),
                text(node.x + 14, node.y + 74, node.detail, "node-detail"),
                text(node.x + 14, node.y + 99, node.red_type, "node-type"),
                "</g>",
            ]
        )
    parts.extend(
        [
            text(40, height - 35, "All CutDestination sockets are present and unwired.", "warn"),
            text(width - 40, height - 35, f"{evidence} — runtime acceptance pending", "note", anchor="end"),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def layout_json(
    title_value: str,
    width: int,
    height: int,
    nodes: Iterable[NodeSpec],
    edges: Iterable[EdgeSpec],
    source_fingerprint: str,
) -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "title": title_value,
            "source_fingerprint": source_fingerprint,
            "canvas": {"width": width, "height": height},
            "nodes": {
                str(node.quest_id): {
                    "x": node.x,
                    "y": node.y,
                    "width": node.width,
                    "height": node.height,
                }
                for node in nodes
            },
            "routes": {
                (
                    f"{edge.source}.{edge.source_socket}->"
                    f"{edge.destination}.{edge.destination_socket}"
                ): [list(point) for point in edge.route]
                for edge in edges
                if edge.route
            },
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def panel(parts: list[str], x: int, y: int, width: int, height: int, css: str, title_value: str, lines: tuple[str, ...]) -> None:
    parts.append(f'<rect class="{css}" x="{x}" y="{y}" width="{width}" height="{height}" rx="12"/>')
    parts.append(text(x + 18, y + 31, title_value, "panel-title"))
    for index, line in enumerate(lines):
        parts.append(text(x + 18, y + 61 + index * 22, line, "detail"))


def render_resource_chain(evidence: str) -> str:
    parts = svg_open(
        1580,
        720,
        "cqa004 external-phase resource chain",
        "ArchiveXL registers only the root phase. Its phase node resolves the archived child, which uses NodeRefs owned by the root prefab declaration and world resources.",
        {"evidence_class": evidence, "diagram": "conceptual-resource-chain"},
    )
    parts.extend(
        [
            text(40, 48, "cqa004 external-phase resource chain", "title"),
            text(40, 77, "Registration, archive lookup, phase scope, and world ownership are different relationships", "subtitle"),
        ]
    )
    panel(parts, 40, 125, 300, 150, "panel-blue", "ArchiveXL", ("register cqa004.questphase", "register journal + localization", "register streaming block", "DO NOT register child"))
    panel(parts, 410, 125, 330, 150, "panel-blue", "Root questphase", ("phasePrefabs: #cqa004_pr_handoff", "external phase node ID 13", "phaseInstancePrefabs: []"))
    panel(parts, 810, 125, 330, 150, "panel-amber", "External child", ("archived cqa004_boundary.questphase", "phasePrefabs: []", "terminating Out1"))
    panel(parts, 1210, 125, 330, 150, "panel-green", "Child graph lookups", ("#cqa004_mp_handoff", "#cqa004_tr_reach", "#cqa004_tr_leave"))
    panel(parts, 410, 410, 330, 160, "panel-green", "Streaming block", ("Quest descriptor binds", "$/mod/cqa/cqa004/", "#cqa004_pr_handoff"))
    panel(parts, 810, 410, 330, 160, "panel-green", "Quest sector", ("owns reach + leave triggers", "finite Quest descriptor", "Allen Street geometry"))
    panel(parts, 1210, 410, 330, 160, "panel-green", "AlwaysLoaded sector", ("owns static handoff marker", "separate sector category", "same full prefab subtree"))
    arrows = (
        (340, 200, 410, 200, "registered root"),
        (740, 200, 810, 200, "soft phaseResource"),
        (1140, 200, 1210, 200, "local NodeRefs"),
        (575, 275, 575, 410, "root prefab scope"),
        (740, 490, 810, 490, "descriptor data"),
        (1140, 490, 1210, 490, "separate owner"),
    )
    for x1, y1, x2, y2, label in arrows:
        parts.append(f'<path class="edge" d="M {x1} {y1} L {x2} {y2}"/>')
        parts.append(text((x1 + x2) / 2, (y1 + y2) / 2 - 10, label, "edge-label"))
    parts.extend(
        [
            text(40, 660, "Archived does not mean registered: the parent resolves the child by depot path.", "warn"),
            text(1540, 660, f"{evidence} — runtime behavior pending", "note", anchor="end"),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def render_handoff_contract(evidence: str) -> str:
    parts = svg_open(
        1500,
        720,
        "cqa004 terminating-child handoff contract",
        "Parent execution enters the phase node at In1, the child input is also named In1, the terminating child output Out1 returns through the parent phase node Out1, and CutDestination remains deliberately unwired.",
        {"evidence_class": evidence, "diagram": "conceptual-handoff-contract"},
    )
    parts.extend(
        [
            text(40, 48, "cqa004 terminating-child handoff contract", "title"),
            text(40, 77, "Exact socket names at the external phase boundary", "subtitle"),
        ]
    )
    panel(parts, 60, 145, 390, 260, "panel-blue", "Parent graph • phase node ID 13", ("input socket: In1", "output socket: Out1", "socket: CutDestination", "phaseGraph: null", "phaseResource: cqa004_boundary.questphase"))
    panel(parts, 550, 145, 390, 260, "panel-amber", "External child resource", ("questInput socketName: In1", "child work executes", "questOutput socketName: Out1", "questOutput type: Terminating", "phasePrefabs: []"))
    panel(parts, 1040, 145, 390, 260, "panel-blue", "Parent continuation", ("phase node Out1", "→ objective ID 14 Active", "→ 30-second confirmation", "→ completion path", "CutDestination has no edge"))
    parts.extend(
        [
            '<path class="edge" d="M 450 225 L 550 225"/>',
            text(500, 208, "In1 → In1", "edge-label"),
            '<path class="edge" d="M 940 305 L 1040 305"/>',
            text(990, 288, "Out1 → Out1", "edge-label"),
            '<path class="dashed" d="M 255 405 L 255 535 L 1235 535 L 1235 405"/>',
            text(745, 523, "CutDestination • present on nodes • deliberately unwired", "edge-label"),
            text(60, 590, "Structural contract: exact sockets and terminating output.", "label"),
            text(60, 618, "Runtime interpretation of CutDestination: Experimental; this lab creates no cut edge.", "warn"),
            text(1430, 665, f"{evidence} — parent/child runtime acceptance pending", "note", anchor="end"),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def outputs() -> dict[str, str]:
    evidence = evidence_label()
    root_fingerprint = graph_fingerprint(ROOT_SOURCE, ROOT_NODES, ROOT_EDGES)
    child_fingerprint = graph_fingerprint(CHILD_SOURCE, CHILD_NODES, CHILD_EDGES)
    return {
        "cqa004.questphase.layout.json": layout_json(
            "cqa004 Handoff Point root questphase",
            3840,
            790,
            ROOT_NODES,
            ROOT_EDGES,
            root_fingerprint,
        ),
        "cqa004.root.questphase.svg": render_graph(
            "cqa004 Handoff Point — root graph",
            "12 nodes • 12 edges • external child returns through 13.Out1",
            3840,
            790,
            ROOT_SOURCE,
            ROOT_NODES,
            ROOT_EDGES,
            root_fingerprint,
            evidence,
        ),
        "cqa004_boundary.questphase.layout.json": layout_json(
            "cqa004 Handoff Point external child questphase",
            3360,
            430,
            CHILD_NODES,
            CHILD_EDGES,
            child_fingerprint,
        ),
        "cqa004.child.questphase.svg": render_graph(
            "cqa004 Handoff Point — external child graph",
            "10 nodes • 9 edges • terminating Out1 returns to the parent",
            3360,
            430,
            CHILD_SOURCE,
            CHILD_NODES,
            CHILD_EDGES,
            child_fingerprint,
            evidence,
        ),
        "cqa004.resource-chain.svg": render_resource_chain(evidence),
        "cqa004.handoff-contract.svg": render_handoff_contract(evidence),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify checked diagram sources and published SVGs are current",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated = outputs()
    for name, content in generated.items():
        targets = [ASSET_DIR / name]
        if name.endswith(".svg"):
            targets.append(PUBLISH_DIR / name)
        for target in targets:
            if args.check:
                if not target.is_file() or target.read_text(encoding="utf-8") != content:
                    raise SystemExit(f"{target}: generated Lab 4 diagram is stale")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
