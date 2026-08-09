#!/usr/bin/env python3
"""Render an exact quest graph from WolvenKit CR2W-JSON.

The CR2W-JSON owns nodes, sockets, edges, and decisive values. A companion
layout file owns only canvas geometry and node boxes.

SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


Json = dict[str, Any]


@dataclass(frozen=True)
class Node:
    quest_id: int
    red_type: str
    sockets: tuple[tuple[str, str, str], ...]
    title: str
    detail: str
    category: str


@dataclass(frozen=True)
class Edge:
    source: int
    source_socket: str
    destination: int
    destination_socket: str


def load_json(path: Path) -> Json:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def collect_handles(value: Any, result: dict[str, Json]) -> None:
    if isinstance(value, dict):
        handle_id = value.get("HandleId")
        data = value.get("Data")
        if isinstance(handle_id, str) and isinstance(data, dict):
            result[handle_id] = data
        for child in value.values():
            collect_handles(child, result)
    elif isinstance(value, list):
        for child in value:
            collect_handles(child, result)


def handle_id(value: Any) -> str:
    if not isinstance(value, dict):
        raise ValueError("expected a handle object")
    result = value.get("HandleId") or value.get("HandleRefId")
    if not isinstance(result, str):
        raise ValueError("handle object has no string ID")
    return result


def resolve(value: Any, handles: dict[str, Json]) -> Json:
    return handles[handle_id(value)]


def cname(value: Any) -> str:
    if isinstance(value, dict):
        raw = value.get("$value")
        if isinstance(raw, str):
            return raw
    return ""


def find_typed(
    value: Any,
    target_type: str,
    handles: dict[str, Json],
    visited: set[str] | None = None,
) -> Json | None:
    if visited is None:
        visited = set()
    if isinstance(value, dict):
        if value.get("$type") == target_type:
            return value
        if "HandleId" in value or "HandleRefId" in value:
            current_handle = handle_id(value)
            if current_handle not in visited:
                visited.add(current_handle)
                found = find_typed(
                    resolve(value, handles), target_type, handles, visited
                )
                if found is not None:
                    return found
        for key, child in value.items():
            if key not in {"HandleId", "HandleRefId"}:
                found = find_typed(child, target_type, handles, visited)
                if found is not None:
                    return found
    elif isinstance(value, list):
        for child in value:
            found = find_typed(child, target_type, handles, visited)
            if found is not None:
                return found
    return None


def compare_symbol(value: str) -> str:
    return {
        "Equal": "==",
        "NotEqual": "!=",
        "Greater": ">",
        "GreaterOrEqual": ">=",
        "Less": "<",
        "LessOrEqual": "<=",
    }.get(value, value)


def node_presentation(data: Json, handles: dict[str, Json]) -> tuple[str, str, str]:
    red_type = str(data.get("$type", "Unknown"))
    if red_type == "questInputNodeDefinition":
        return "Input", cname(data.get("socketName")), "boundary"
    if red_type == "questOutputNodeDefinition":
        return "Terminate", str(data.get("type", "Output")), "boundary"
    if red_type == "questConditionNodeDefinition":
        comparison = find_typed(
            data.get("condition"), "questVarComparison_ConditionType", handles
        )
        if comparison:
            detail = (
                f"{comparison.get('factName', '?')} "
                f"{compare_symbol(str(comparison.get('comparisonType', '?')))} "
                f"{comparison.get('value', '?')}"
            )
        else:
            detail = "evaluate condition now"
        return "One-shot guard", detail, "gate"
    if red_type == "questPauseConditionNodeDefinition":
        delay = find_typed(
            data.get("condition"), "questRealtimeDelay_ConditionType", handles
        )
        if delay:
            seconds = int(delay.get("seconds", 0))
            minutes = int(delay.get("minutes", 0))
            hours = int(delay.get("hours", 0))
            total = seconds + 60 * minutes + 3600 * hours
            return "Wait", f"{total} real-time seconds", "gate"
        return "Wait", "until condition becomes true", "gate"
    if red_type == "questJournalNodeDefinition":
        path = find_typed(data.get("type"), "gameJournalPath", handles)
        real_path = str(path.get("realPath", "?")) if path else "?"
        return "Journal state", real_path.rsplit("/", 1)[-1], "journal"
    if red_type == "questFactsDBManagerNodeDefinition":
        fact = find_typed(data.get("type"), "questSetVar_NodeType", handles)
        if fact:
            return (
                "Set fact",
                f"{fact.get('factName', '?')} = {fact.get('value', '?')}",
                "fact",
            )
        return "Fact operation", "FactsDBManager", "fact"
    label = red_type.removeprefix("quest").removesuffix("NodeDefinition")
    return label, red_type, "action"


def parse_graph(source: Json) -> tuple[list[Node], list[Edge]]:
    handles: dict[str, Json] = {}
    collect_handles(source, handles)
    root = source.get("Data", {}).get("RootChunk", {})
    if root.get("$type") != "questQuestPhaseResource":
        raise ValueError("source root is not questQuestPhaseResource")
    graph = resolve(root["graph"], handles)
    wrappers = graph.get("nodes")
    if not isinstance(wrappers, list):
        raise ValueError("quest graph has no node list")

    nodes: list[Node] = []
    socket_owner: dict[str, tuple[int, str, str]] = {}
    for wrapper in wrappers:
        data = resolve(wrapper, handles)
        quest_id = data.get("id")
        if not isinstance(quest_id, int):
            raise ValueError("quest node has no numeric id")
        sockets: list[tuple[str, str, str]] = []
        for socket_wrapper in data.get("sockets", []):
            socket_id = handle_id(socket_wrapper)
            socket_data = resolve(socket_wrapper, handles)
            socket_name = cname(socket_data.get("name"))
            socket_type = str(socket_data.get("type", ""))
            sockets.append((socket_id, socket_name, socket_type))
            socket_owner[socket_id] = (quest_id, socket_name, socket_type)
        title, detail, category = node_presentation(data, handles)
        nodes.append(
            Node(
                quest_id=quest_id,
                red_type=str(data.get("$type", "Unknown")),
                sockets=tuple(sockets),
                title=title,
                detail=detail,
                category=category,
            )
        )

    edges: list[Edge] = []
    for connection_id, data in handles.items():
        if data.get("$type") != "graphGraphConnectionDefinition":
            continue
        source_id = handle_id(data["source"])
        destination_id = handle_id(data["destination"])
        if source_id not in socket_owner or destination_id not in socket_owner:
            raise ValueError(f"connection {connection_id} uses an unknown socket")
        source_node, source_name, _ = socket_owner[source_id]
        destination_node, destination_name, _ = socket_owner[destination_id]
        edges.append(Edge(source_node, source_name, destination_node, destination_name))

    nodes.sort(key=lambda item: item.quest_id)
    edges.sort(
        key=lambda item: (
            item.source,
            item.source_socket,
            item.destination,
            item.destination_socket,
        )
    )
    return nodes, edges


def canonical_structure(nodes: Iterable[Node], edges: Iterable[Edge]) -> Json:
    return {
        "nodes": [
            {
                "id": node.quest_id,
                "type": node.red_type,
                "sockets": [
                    {"name": name, "type": socket_type}
                    for _, name, socket_type in node.sockets
                ],
                "detail": node.detail,
            }
            for node in nodes
        ],
        "edges": [
            {
                "source": edge.source,
                "source_socket": edge.source_socket,
                "destination": edge.destination,
                "destination_socket": edge.destination_socket,
            }
            for edge in edges
        ],
    }


def fingerprint(nodes: Iterable[Node], edges: Iterable[Edge]) -> str:
    canonical = json.dumps(
        canonical_structure(nodes, edges),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


def update_fingerprint(path: Path, layout: Json, actual: str) -> None:
    layout["source_fingerprint"] = actual
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(layout, indent=2, ensure_ascii=False) + "\n")


def validate_layout(nodes: Iterable[Node], layout: Json) -> None:
    allowed_top = {
        "schema_version",
        "title",
        "source_fingerprint",
        "canvas",
        "nodes",
    }
    unexpected_top = set(layout) - allowed_top
    if unexpected_top:
        raise ValueError(f"layout contains non-layout fields: {sorted(unexpected_top)}")
    raw_nodes = layout.get("nodes")
    if not isinstance(raw_nodes, dict):
        raise ValueError("layout has no node geometry map")
    graph_ids = {str(node.quest_id) for node in nodes}
    layout_ids = set(raw_nodes)
    if graph_ids != layout_ids:
        raise ValueError(
            "layout node IDs do not match graph node IDs: "
            f"missing={sorted(graph_ids - layout_ids)}, "
            f"extra={sorted(layout_ids - graph_ids)}"
        )
    allowed_geometry = {"x", "y", "width", "height"}
    for node_id, geometry in raw_nodes.items():
        if not isinstance(geometry, dict):
            raise ValueError(f"layout node {node_id} is not an object")
        unexpected = set(geometry) - allowed_geometry
        if unexpected:
            raise ValueError(
                f"layout node {node_id} contains non-geometry fields: "
                f"{sorted(unexpected)}"
            )
        if not {"x", "y"} <= set(geometry):
            raise ValueError(f"layout node {node_id} requires x and y")


def svg_text(x: float, y: float, value: str, css_class: str) -> str:
    return f'<text x="{x:g}" y="{y:g}" class="{css_class}">{html.escape(value)}</text>'


def box(layout: Json, node_id: int) -> tuple[float, float, float, float]:
    raw = layout.get("nodes", {}).get(str(node_id))
    if not isinstance(raw, dict):
        raise ValueError(f"layout is missing node {node_id}")
    return (
        float(raw["x"]),
        float(raw["y"]),
        float(raw.get("width", 220)),
        float(raw.get("height", 92)),
    )


def edge_points(
    source_box: tuple[float, float, float, float],
    destination_box: tuple[float, float, float, float],
) -> tuple[tuple[float, float], tuple[float, float]]:
    sx, sy, sw, sh = source_box
    dx, dy, dw, dh = destination_box
    source_center = (sx + sw / 2, sy + sh / 2)
    destination_center = (dx + dw / 2, dy + dh / 2)
    if abs(source_center[0] - destination_center[0]) < 1:
        if destination_center[1] >= source_center[1]:
            return (source_center[0], sy + sh), (destination_center[0], dy)
        return (source_center[0], sy), (destination_center[0], dy + dh)
    if destination_center[0] > source_center[0]:
        return (sx + sw, source_center[1]), (dx, destination_center[1])
    return (sx, source_center[1]), (dx + dw, destination_center[1])


def render_svg(
    source_path: Path,
    nodes: list[Node],
    edges: list[Edge],
    layout: Json,
    actual_fingerprint: str,
) -> str:
    canvas = layout.get("canvas", {})
    width = int(canvas.get("width", 1400))
    height = int(canvas.get("height", 520))
    title = str(layout.get("title", source_path.stem))
    boxes = {node.quest_id: box(layout, node.quest_id) for node in nodes}

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-labelledby="svg-title svg-desc">'
        ),
        f'<title id="svg-title">{html.escape(title)}</title>',
        (
            '<desc id="svg-desc">Exact quest graph rendered from '
            f"{html.escape(source_path.name)}. Fingerprint "
            f"{html.escape(actual_fingerprint)}.</desc>"
        ),
        "<metadata>"
        + html.escape(
            json.dumps(
                {
                    "source": source_path.as_posix(),
                    "source_fingerprint": actual_fingerprint,
                },
                sort_keys=True,
            )
        )
        + "</metadata>",
        """<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#9aa4b2"/>
  </marker>
  <style>
    .background { fill: #11151c; }
    .edge { fill: none; stroke: #9aa4b2; stroke-width: 2; marker-end: url(#arrow); }
    .edge-label { fill: #d7dde7; font: 12px ui-monospace, Consolas, monospace;
                  text-anchor: middle; paint-order: stroke; stroke: #11151c;
                  stroke-width: 4px; stroke-linejoin: round; }
    .node { stroke: #e6e9ef; stroke-width: 1.5; }
    .boundary { fill: #4b5563; }
    .gate { fill: #9a6700; }
    .fact { fill: #6d3ea0; }
    .journal { fill: #247a4b; }
    .action { fill: #28699c; }
    .node-id { fill: #f7f8fa; font: 12px ui-monospace, Consolas, monospace; }
    .node-title { fill: white; font: 600 16px system-ui, sans-serif; }
    .node-detail { fill: #f3f5f8; font: 12px ui-monospace, Consolas, monospace; }
  </style>
</defs>""",
        f'<rect class="background" width="{width}" height="{height}"/>',
    ]

    for edge in edges:
        source_box = boxes[edge.source]
        destination_box = boxes[edge.destination]
        start, end = edge_points(source_box, destination_box)
        delta = max(45.0, abs(end[0] - start[0]) * 0.4)
        if abs(end[1] - start[1]) < 1:
            path = f"M {start[0]:g} {start[1]:g} L {end[0]:g} {end[1]:g}"
        elif abs(end[0] - start[0]) < 1:
            path = (
                f"M {start[0]:g} {start[1]:g} "
                f"C {start[0] + 70:g} {start[1]:g}, "
                f"{end[0] + 70:g} {end[1]:g}, {end[0]:g} {end[1]:g}"
            )
        elif end[0] > start[0]:
            path = (
                f"M {start[0]:g} {start[1]:g} "
                f"C {start[0] + delta:g} {start[1]:g}, "
                f"{end[0] - delta:g} {end[1]:g}, {end[0]:g} {end[1]:g}"
            )
        else:
            path = (
                f"M {start[0]:g} {start[1]:g} "
                f"C {start[0] - delta:g} {start[1]:g}, "
                f"{end[0] + delta:g} {end[1]:g}, {end[0]:g} {end[1]:g}"
            )
        parts.append(f'<path class="edge" d="{path}"/>')
        label = f"{edge.source_socket} → {edge.destination_socket}"
        label_x = (start[0] + end[0]) / 2
        if abs(end[1] - start[1]) < 1:
            label_y = min(source_box[1], destination_box[1]) - 10
        else:
            label_y = (start[1] + end[1]) / 2 - 8
        parts.append(svg_text(label_x, label_y, label, "edge-label"))

    for node in nodes:
        x, y, width_box, height_box = boxes[node.quest_id]
        tooltip = f"{node.red_type}: {node.detail}"
        parts.append(f'<g aria-label="{html.escape(tooltip)}">')
        if node.category == "gate":
            cut = 16
            points = (
                f"{x + cut:g},{y:g} {x + width_box - cut:g},{y:g} "
                f"{x + width_box:g},{y + height_box / 2:g} "
                f"{x + width_box - cut:g},{y + height_box:g} "
                f"{x + cut:g},{y + height_box:g} "
                f"{x:g},{y + height_box / 2:g}"
            )
            parts.append(f'<polygon class="node {node.category}" points="{points}"/>')
        else:
            parts.append(
                f'<rect class="node {node.category}" x="{x:g}" y="{y:g}" '
                f'width="{width_box:g}" height="{height_box:g}" rx="10"/>'
            )
        parts.append(svg_text(x + 14, y + 21, f"ID {node.quest_id}", "node-id"))
        parts.append(svg_text(x + 14, y + 47, node.title, "node-title"))
        parts.append(svg_text(x + 14, y + 70, node.detail, "node-detail"))
        parts.append("</g>")

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("layout", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--update-fingerprint",
        action="store_true",
        help="replace the layout's recorded fingerprint before rendering",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that the existing SVG exactly matches a fresh render",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = load_json(args.source)
    layout = load_json(args.layout)
    nodes, edges = parse_graph(source)
    validate_layout(nodes, layout)
    actual = fingerprint(nodes, edges)
    if args.update_fingerprint:
        update_fingerprint(args.layout, layout, actual)
    recorded = layout.get("source_fingerprint")
    if recorded != actual:
        raise SystemExit(
            f"source fingerprint mismatch: recorded {recorded!r}, actual {actual!r}"
        )
    svg = render_svg(args.source, nodes, edges, layout, actual)
    if args.check:
        existing = args.output.read_text(encoding="utf-8")
        if existing != svg:
            raise SystemExit(f"{args.output}: generated SVG is stale")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(svg)


if __name__ == "__main__":
    main()
