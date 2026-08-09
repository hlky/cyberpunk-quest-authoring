#!/usr/bin/env python3
"""Build deterministic exact and conceptual SVGs for Lab 5.

The phase figures are checked against the completed CR2W-JSON graphs before
rendering. The scene figure checks its native node/socket graph. The remaining
figures are tutorial-owned conceptual diagrams. Readers do not need this
script.

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
import build_lab05_sources as source_builder  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "examples" / "lab-05-first-contact" / "completed"
RAW = LAB / "source" / "raw" / "mod" / "cqa" / "cqa005"
ROOT_SOURCE = RAW / "phases" / "cqa005.questphase.json"
CHILD_SOURCE = RAW / "phases" / "cqa005_contact.questphase.json"
SCENE_SOURCE = RAW / "scenes" / "cqa005_first_contact.scene.json"
SUBTITLE_SOURCE = (
    RAW
    / "localization"
    / "en-us"
    / "subtitles"
    / "cqa005_subtitles.json.json"
)
QUEST_SECTOR_SOURCE = RAW / "world" / "cqa005_first_contact.streamingsector.json"
ALWAYS_SECTOR_SOURCE = RAW / "world" / "cqa005_always_loaded.streamingsector.json"
ACCEPTANCE = LAB / "runtime-acceptance.json"
ASSET_DIR = ROOT / "assets" / "diagrams" / "lab-05"
PUBLISH_DIR = ROOT / "book" / "src" / "images" / "lab-05"


@dataclass(frozen=True)
class NodeSpec:
    node_id: int
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
    NodeSpec(0, "Input", "In1", "questInputNodeDefinition", "boundary", 40, 140, 170),
    NodeSpec(1, "Output", "Terminating • Out1", "questOutputNodeDefinition", "boundary", 2300, 405, 210),
    NodeSpec(10, "Fact guard", "cqa005_completed == 0", "questConditionNodeDefinition", "gate", 260, 140, 280),
    NodeSpec(11, "Quest • Active", "cqa005", "questJournalNodeDefinition", "journal", 590, 140, 250),
    NodeSpec(12, "External child", "cqa005_contact.questphase", "questPhaseNodeDefinition", "phase", 890, 140, 330),
    NodeSpec(13, "Quest • Succeeded", "cqa005", "questJournalNodeDefinition", "journal", 1270, 405, 280),
    NodeSpec(14, "Set fact", "cqa005_completed = 1", "questFactsDBManagerNodeDefinition", "fact", 1600, 405, 280),
)

ROOT_EDGES = (
    EdgeSpec(0, "Out", 10, "In"),
    EdgeSpec(10, "False", 1, "In", ((400, 690), (2300, 690))),
    EdgeSpec(10, "True", 11, "Active"),
    EdgeSpec(11, "Out", 12, "In1"),
    EdgeSpec(12, "Out1", 13, "Succeeded", ((1055, 335), (1410, 335))),
    EdgeSpec(13, "Out", 14, "In"),
    EdgeSpec(14, "Out", 1, "In"),
)

CHILD_NODES = (
    NodeSpec(0, "Input", "In1", "questInputNodeDefinition", "boundary", 30, 140, 160),
    NodeSpec(1, "Output", "Terminating • Out1", "questOutputNodeDefinition", "boundary", 4480, 140, 200),
    NodeSpec(10, "Meet • Active", "cqa005_01_obj_meet", "questJournalNodeDefinition", "journal", 230, 140, 270),
    NodeSpec(11, "Mappin • Active", "#cqa005_mp_contact", "questMappinManagerNodeDefinition", "journal", 540, 140, 280),
    NodeSpec(12, "Community • Activate", "contact / default", "questSpawnManagerNodeDefinition", "community", 860, 140, 290),
    NodeSpec(13, "Character spawned", "entireCommunity > 0", "questPauseConditionNodeDefinition", "gate", 1190, 140, 300),
    NodeSpec(14, "Wait • IsInside", "#cqa005_tr_setup", "questPauseConditionNodeDefinition", "gate", 1530, 140, 280),
    NodeSpec(15, "Checkpoint", "cqa005_first_contact", "questCheckpointNodeDefinition", "action", 1850, 140, 270),
    NodeSpec(16, "Scene", "start → contact_done", "questSceneNodeDefinition", "scene", 2160, 140, 280),
    NodeSpec(17, "Meet • Succeeded", "cqa005_01_obj_meet", "questJournalNodeDefinition", "journal", 2480, 140, 290),
    NodeSpec(18, "Mappin • Inactive", "#cqa005_mp_contact", "questMappinManagerNodeDefinition", "journal", 2810, 140, 290),
    NodeSpec(19, "Leave • Active", "cqa005_01_obj_leave", "questJournalNodeDefinition", "journal", 3140, 140, 280),
    NodeSpec(20, "Wait • IsOutside", "#cqa005_tr_cleanup", "questPauseConditionNodeDefinition", "gate", 3460, 140, 290),
    NodeSpec(21, "Community • Deactivate", "whole / None / None", "questSpawnManagerNodeDefinition", "community", 3790, 140, 310),
    NodeSpec(22, "Leave • Succeeded", "cqa005_01_obj_leave", "questJournalNodeDefinition", "journal", 4140, 140, 300),
)

CHILD_EDGES = tuple(
    EdgeSpec(source, source_socket, destination, destination_socket)
    for source, source_socket, destination, destination_socket in (
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
    )
)


STYLE = """    .bg { fill: #10151d; }
    .title { fill: #f7f9fc; font: 700 28px system-ui, sans-serif; }
    .subtitle { fill: #aeb8c8; font: 14px system-ui, sans-serif; }
    .badge { fill: #4a3200; stroke: #f5b942; stroke-width: 1.5; }
    .badge-text { fill: #ffd982; font: 700 14px system-ui, sans-serif; text-anchor: middle; }
    .edge { fill: none; stroke: #c9d1dc; stroke-width: 2.1; marker-end: url(#arrow); }
    .edge-dashed { fill: none; stroke: #f3be55; stroke-width: 2; stroke-dasharray: 7 7; marker-end: url(#arrow); }
    .edge-label { fill: #e0e5ed; font: 12px ui-monospace, Consolas, monospace; text-anchor: middle; paint-order: stroke; stroke: #10151d; stroke-width: 5px; stroke-linejoin: round; }
    .node { stroke: #e6e9ef; stroke-width: 1.5; }
    .boundary { fill: #4b5563; }
    .gate { fill: #956600; }
    .journal { fill: #247a4b; }
    .phase { fill: #315f9a; }
    .fact { fill: #6d3ea0; }
    .community { fill: #8a4f22; }
    .scene { fill: #7b315e; }
    .action { fill: #315f78; }
    .node-id { fill: #f7f8fa; font: 12px ui-monospace, Consolas, monospace; }
    .node-title { fill: #ffffff; font: 700 16px system-ui, sans-serif; }
    .node-detail { fill: #f3f5f8; font: 12px ui-monospace, Consolas, monospace; }
    .node-type { fill: #d2d9e3; font: 10px ui-monospace, Consolas, monospace; }
    .panel { fill: #181f2a; stroke: #506078; stroke-width: 1.5; }
    .panel-blue { fill: #182b49; stroke: #78a9ff; stroke-width: 2; }
    .panel-green { fill: #173d38; stroke: #68d8c5; stroke-width: 2; }
    .panel-amber { fill: #493510; stroke: #f3be55; stroke-width: 2; }
    .panel-magenta { fill: #47203d; stroke: #e07abc; stroke-width: 2; }
    .panel-title { fill: #ffffff; font: 700 18px system-ui, sans-serif; }
    .label { fill: #f7f9fc; font: 600 14px system-ui, sans-serif; }
    .detail { fill: #dce2eb; font: 12px ui-monospace, Consolas, monospace; }
    .note { fill: #bac4d3; font: 13px system-ui, sans-serif; }
    .warn { fill: #ffd982; font: 600 13px system-ui, sans-serif; }
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def evidence_label() -> str:
    record = load_json(ACCEPTANCE)
    expected = {"pending": "experimental", "failed": "experimental", "passed": "runtime-proven"}.get(record.get("status"))
    if expected is None or record.get("evidence_class") != expected:
        raise ValueError("Lab 5 acceptance status and evidence class disagree")
    return "Runtime-proven" if expected == "runtime-proven" else "Experimental"


def acceptance_status() -> str:
    status = str(load_json(ACCEPTANCE).get("status"))
    if status not in {"pending", "failed", "passed"}:
        raise ValueError("Lab 5 acceptance status is invalid")
    return status


def svg_open(width: int, height: int, title: str, description: str, metadata: dict[str, object]) -> list[str]:
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!-- SPDX-License-Identifier: CC-BY-4.0 -->',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="svg-title svg-desc">',
        f'<title id="svg-title">{esc(title)}</title>',
        f'<desc id="svg-desc">{esc(description)}</desc>',
        "<metadata>" + esc(json.dumps(metadata, sort_keys=True, separators=(",", ":"))) + "</metadata>",
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#c9d1dc"/></marker>',
        "<style>",
        STYLE,
        "</style>",
        "</defs>",
        f'<rect class="bg" width="{width}" height="{height}"/>',
    ]


def text(x: float, y: float, value: object, css: str, *, anchor: str | None = None) -> str:
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text class="{css}" x="{x:g}" y="{y:g}"{anchor_attr}>{esc(value)}</text>'


def graph_fingerprint(source: Path, nodes: tuple[NodeSpec, ...], edges: tuple[EdgeSpec, ...]) -> str:
    parsed_nodes, parsed_edges = parse_graph(load_json(source))
    actual_nodes = tuple((node.quest_id, node.red_type) for node in parsed_nodes)
    expected_nodes = tuple((node.node_id, node.red_type) for node in nodes)
    if actual_nodes != expected_nodes:
        raise ValueError(f"{source.name}: node contract changed: {actual_nodes}")
    actual_edges = tuple((edge.source, edge.source_socket, edge.destination, edge.destination_socket) for edge in parsed_edges)
    expected_edges = tuple(sorted((edge.source, edge.source_socket, edge.destination, edge.destination_socket) for edge in edges))
    if actual_edges != expected_edges:
        raise ValueError(f"{source.name}: edge contract changed: {actual_edges}")
    return fingerprint(parsed_nodes, parsed_edges)


def layout_json(title: str, width: int, height: int, nodes: Iterable[NodeSpec], edges: Iterable[EdgeSpec], source_fingerprint: str) -> str:
    return json.dumps(
        {
            "schema_version": 1,
            "title": title,
            "source_fingerprint": source_fingerprint,
            "canvas": {"width": width, "height": height},
            "nodes": {str(node.node_id): {"x": node.x, "y": node.y, "width": node.width, "height": node.height} for node in nodes},
            "routes": {f"{edge.source}.{edge.source_socket}->{edge.destination}.{edge.destination_socket}": [list(point) for point in edge.route] for edge in edges if edge.route},
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"


def box_edge(source: NodeSpec, destination: NodeSpec, route: tuple[tuple[int, int], ...]) -> tuple[str, float, float]:
    start = (source.x + source.width, source.y + source.height / 2)
    end = (destination.x, destination.y + destination.height / 2)
    if route:
        points = (start, *route, end)
        path = " ".join([f"M {points[0][0]:g} {points[0][1]:g}"] + [f"L {point[0]:g} {point[1]:g}" for point in points[1:]])
        return path, (route[0][0] + route[-1][0]) / 2, route[0][1] - 9
    delta = max(40.0, abs(end[0] - start[0]) * 0.38)
    path = f"M {start[0]:g} {start[1]:g} C {start[0] + delta:g} {start[1]:g}, {end[0] - delta:g} {end[1]:g}, {end[0]:g} {end[1]:g}"
    return path, (start[0] + end[0]) / 2, (start[1] + end[1]) / 2 - 10


def render_graph(title: str, subtitle: str, width: int, height: int, source: Path, nodes: tuple[NodeSpec, ...], edges: tuple[EdgeSpec, ...], source_fingerprint: str, evidence: str, status: str) -> str:
    parts = svg_open(width, height, title, f"Exact graph with {len(nodes)} nodes and {len(edges)} edges. Runtime evidence remains {evidence}.", {"source": source.relative_to(ROOT).as_posix(), "source_fingerprint": source_fingerprint, "node_count": len(nodes), "edge_count": len(edges), "evidence_class": evidence})
    parts.extend([text(40, 48, title, "title"), text(40, 77, subtitle, "subtitle"), f'<rect class="badge" x="{width - 230}" y="27" width="190" height="36" rx="18"/>', text(width - 135, 51, evidence, "badge-text")])
    node_map = {node.node_id: node for node in nodes}
    for edge in edges:
        path, label_x, label_y = box_edge(node_map[edge.source], node_map[edge.destination], edge.route)
        parts.extend([f'<g data-source="{edge.source}" data-source-socket="{esc(edge.source_socket)}" data-destination="{edge.destination}" data-destination-socket="{esc(edge.destination_socket)}">', f'<path class="edge" d="{path}"/>', text(label_x, label_y, f"{edge.source_socket} → {edge.destination_socket}", "edge-label"), "</g>"])
    for node in nodes:
        parts.append(f'<g data-node-id="{node.node_id}" data-node-type="{esc(node.red_type)}">')
        if node.category == "gate":
            cut = 20
            points = f"{node.x + cut},{node.y} {node.x + node.width - cut},{node.y} {node.x + node.width},{node.y + node.height / 2:g} {node.x + node.width - cut},{node.y + node.height} {node.x + cut},{node.y + node.height} {node.x},{node.y + node.height / 2:g}"
            parts.append(f'<polygon class="node gate" points="{points}"/>')
        else:
            radius = node.height // 2 if node.category == "boundary" else 10
            parts.append(f'<rect class="node {node.category}" x="{node.x}" y="{node.y}" width="{node.width}" height="{node.height}" rx="{radius}"/>')
        parts.extend([text(node.x + 14, node.y + 21, f"ID {node.node_id}", "node-id"), text(node.x + 14, node.y + 48, node.title, "node-title"), text(node.x + 14, node.y + 74, node.detail, "node-detail"), text(node.x + 14, node.y + 99, node.red_type, "node-type"), "</g>"])
    parts.extend([text(40, height - 35, "All CutDestination sockets are present and unwired.", "warn"), text(width - 40, height - 35, f"{evidence} — runtime acceptance {status}", "note", anchor="end"), "</svg>"])
    return "\n".join(parts) + "\n"


def panel(parts: list[str], x: int, y: int, width: int, height: int, css: str, title: str, lines: tuple[str, ...]) -> None:
    parts.append(f'<rect class="{css}" x="{x}" y="{y}" width="{width}" height="{height}" rx="12"/>')
    parts.append(text(x + 18, y + 31, title, "panel-title"))
    for index, line in enumerate(lines):
        parts.append(text(x + 18, y + 61 + index * 22, line, "detail"))


def render_scene(evidence: str, status: str) -> str:
    scene = load_json(SCENE_SOURCE)["Data"]["RootChunk"]
    graph = scene["sceneGraph"]["Data"]
    nodes = graph["graph"]
    actual = [(node["Data"]["nodeId"]["id"], node["Data"]["$type"]) for node in nodes]
    expected = [(1, "scnStartNode"), (2, "scnSectionNode"), (4, "scnQuestNode"), (3, "scnEndNode")]
    if actual != expected:
        raise ValueError(f"scene graph changed: {actual}")
    start_destinations = nodes[0]["Data"]["outputSockets"][0]["destinations"]
    destinations = [(item["nodeId"]["id"], item["isockStamp"]["name"], item["isockStamp"]["ordinal"]) for item in start_destinations]
    if destinations != [(2, 0, 0), (4, 0, 1)]:
        raise ValueError(f"scene start fanout changed: {destinations}")
    if graph.get("startNodes") != [{"$type": "scnNodeId", "id": 1}] or graph.get("endNodes") != [{"$type": "scnNodeId", "id": 3}]:
        raise ValueError("scene startNodes/endNodes changed")
    section = nodes[1]["Data"]
    section_end = section["outputSockets"][0]
    section_cancel = section["outputSockets"][1]
    if (
        [(item["nodeId"]["id"], item["isockStamp"]["name"], item["isockStamp"]["ordinal"]) for item in section_end["destinations"]]
        != [(3, 0, 0)]
        or section_end["stamp"] != {"$type": "scnOutputSocketStamp", "name": 0, "ordinal": 0}
        or section_cancel != {"$type": "scnOutputSocket", "destinations": [], "stamp": {"$type": "scnOutputSocketStamp", "name": 1, "ordinal": 0}}
    ):
        raise ValueError("scene section output/cancel contract changed")
    if len(section["events"]) != 1:
        raise ValueError("scene dialog event count changed")
    event = section["events"][0]["Data"]
    if event["$type"] != "scnDialogLineEvent" or event["screenplayLineId"]["id"] != 1 or event["duration"] != 2598:
        raise ValueError("scene dialog event changed")
    line = scene["screenplayStore"]["lines"]
    if len(line) != 1 or line[0]["locstringId"]["ruid"] != "9638591835734011695" or line[0]["itemId"]["id"] != 1:
        raise ValueError("scene screenplay line changed")
    subtitle = load_json(SUBTITLE_SOURCE)["Data"]["RootChunk"]["root"]["Data"]["entries"]
    if len(subtitle) != 1 or subtitle[0]["stringId"] != "9638591835734011695" or subtitle[0]["femaleVariant"] != "All clear. Keep moving." or subtitle[0]["maleVariant"] != "All clear. Keep moving.":
        raise ValueError("displayed subtitle text/RUID changed")
    ai = nodes[2]["Data"]
    ai_inner = ai["questNode"]["Data"]
    if (
        ai_inner["$type"] != "questPuppetAIManagerNodeDefinition"
        or ai_inner["entries"][0]["aiTier"] != "Cinematic"
        or ai["outputSockets"] != [{"$type": "scnOutputSocket", "destinations": [], "stamp": {"$type": "scnOutputSocketStamp", "name": 0, "ordinal": 0}}]
    ):
        raise ValueError("scene PuppetAI contract changed")
    if nodes[3]["Data"].get("type") != "Terminating" or [(item["name"]["$value"], item["nodeId"]["id"]) for item in scene["exitPoints"]] != [("contact_done", 3)]:
        raise ValueError("scene terminating end/named exit changed")
    parts = svg_open(1540, 620, "cqa005 First Contact scene graph", "Exact completed scene graph: Start fans to a dialog section and a scene-local Puppet AI quest node; the section reaches the terminating end.", {"source": SCENE_SOURCE.relative_to(ROOT).as_posix(), "node_count": 4, "edge_count": 3, "evidence_class": evidence})
    parts.extend([text(40, 48, "cqa005 First Contact — scene graph", "title"), text(40, 77, "4 nodes • 3 edges • exact input socket ordinals", "subtitle")])
    panel(parts, 60, 155, 270, 180, "panel-blue", "Start • ID 1", ("startNodes: [1]", "output 0/0 fans out", "ffStrategy: automatic"))
    panel(parts, 470, 115, 340, 200, "panel-magenta", "Section • ID 2", ("one scnDialogLineEvent", "ruid 9638591835734011695", "All clear. Keep moving.", "output 0/0 → End 3"))
    panel(parts, 470, 355, 340, 180, "panel-amber", "scnQuestNode • ID 4", ("PuppetAIManager", "aiTier: Cinematic", "input socket 0/1", "output 0/0 empty"))
    panel(parts, 980, 155, 300, 180, "panel-green", "End • ID 3", ("type: Terminating", "endNodes: [3]", "exit: contact_done"))
    for x1, y1, x2, y2, label in ((330, 225, 470, 215, "0/0 → 0/0"), (330, 265, 470, 420, "0/0 → 0/1"), (810, 215, 980, 225, "0/0 → 0/0")):
        parts.append(f'<path class="edge" d="M {x1} {y1} L {x2} {y2}"/>')
        parts.append(text((x1 + x2) / 2, (y1 + y2) / 2 - 10, label, "edge-label"))
    parts.extend([text(60, 575, "The PuppetAI output is intentionally empty; no fourth edge is inferred.", "warn"), text(1480, 575, f"{evidence} — combined runtime {status}", "note", anchor="end"), "</svg>"])
    return "\n".join(parts) + "\n"


def render_panel_chain(title: str, subtitle: str, panels: tuple[tuple[str, tuple[str, ...], str], ...], arrows: tuple[str, ...], evidence: str, status: str, diagram: str) -> str:
    width = 1660
    parts = svg_open(width, 620, title, subtitle, {"diagram": diagram, "evidence_class": evidence})
    parts.extend([text(40, 48, title, "title"), text(40, 77, subtitle, "subtitle")])
    panel_width = 350
    gap = 45
    for index, (panel_title, lines, css) in enumerate(panels):
        x = 40 + index * (panel_width + gap)
        panel(parts, x, 155, panel_width, 240, css, panel_title, lines)
        if index < len(arrows):
            next_x = x + panel_width + gap
            parts.append(f'<path class="edge" d="M {x + panel_width} 275 L {next_x} 275"/>')
            parts.append(text((x + panel_width + next_x) / 2, 258, arrows[index], "edge-label"))
    parts.extend([text(40, 540, "Conceptual relationship diagram; exact values are listed in the panels.", "warn"), text(width - 40, 540, f"{evidence} — runtime integration {status}", "note", anchor="end"), "</svg>"])
    return "\n".join(parts) + "\n"


def render_community_identity(evidence: str, status: str) -> str:
    quest = load_json(QUEST_SECTOR_SOURCE)["Data"]["RootChunk"]
    always = load_json(ALWAYS_SECTOR_SOURCE)["Data"]["RootChunk"]
    area = quest["nodes"][3]["Data"]
    registry = always["nodes"][2]["Data"]
    registry_placement = always["nodeData"]["Data"][2]
    source_id = area["sourceObjectId"]["hash"]
    registry_id = registry_placement["QuestPrefabRefHash"]["$value"]
    spot_id = registry["workspotsPersistentData"][0]["globalNodeId"]["hash"]
    expected = (
        "5948510988927765319",
        "6908684691797323855",
        "15950783814303760596",
    )
    derived = (
        str(source_builder.node_ref_hash(source_builder.COMMUNITY_FULL)),
        str(source_builder.node_ref_hash(f"{source_builder.COMMUNITY_FULL}_registry")),
        str(source_builder.node_ref_hash(source_builder.AI_SPOT_FULL)),
    )
    if (source_id, registry_id, spot_id) != expected or derived != expected:
        raise ValueError(
            "displayed community source/registry/AI spot identities changed"
        )
    if (
        quest["nodeRefs"][3]["$value"] != source_builder.COMMUNITY_FULL
        or registry["communitiesData"][0]["communityId"]["entityId"]["hash"]
        != source_id
        or len({source_id, registry_id, spot_id}) != 3
    ):
        raise ValueError("displayed community identity joins changed")
    return render_panel_chain(
        "cqa005 community identity domains",
        "NodeRefs, source object IDs, registry IDs, and AI spot IDs are related but not interchangeable",
        (
            ("Community NodeRef", ("#cqa005_com_contact", "full prefab subtree", "RED4 hash: 5948510988927765319"), "panel-blue"),
            ("Community source", ("sourceObjectId", "5948510988927765319", "hash of community full ref"), "panel-green"),
            ("Registry node", ("QuestPrefabRefHash", "6908684691797323855", "hash of full ref + _registry"), "panel-amber"),
            ("AI spot", ("worldGlobalNodeID", "15950783814303760596", "hash of AI spot full ref"), "panel-magenta"),
        ),
        ("resolves", "registry owns", "entry maps"),
        evidence,
        status,
        "conceptual-community-identity",
    )


def render_resource_chain(evidence: str, status: str) -> str:
    return render_panel_chain(
        "cqa005 First Contact resource chain",
        "Registration, archive resolution, localization, audio, and world ownership",
        (
            ("ArchiveXL", ("register root phase", "journal + 3 localization maps", "register streaming block", "do not register child"), "panel-blue"),
            ("Quest resources", ("root owns prefab", "external child archived", "child invokes .scene", "scene exits contact_done"), "panel-green"),
            ("Scene + localization", ("ruid → subtitle entry", "ruid → VO map", "VO map → mod-owned WEM", "same shell in both checkpoints"), "panel-magenta"),
            ("World resources", ("Quest sector: triggers/community", "AlwaysLoaded: markers/registry", "block binds prefab root", "Allen Street geometry"), "panel-amber"),
        ),
        ("mounts", "soft references", "shares NodeRefs"),
        evidence,
        status,
        "conceptual-resource-chain",
    )


def render_lifecycle(evidence: str, status: str) -> str:
    return render_panel_chain(
        "cqa005 First Contact lifecycle",
        "The child owns setup, acquisition, conversation, and cleanup; the root owns one-shot completion",
        (
            ("Root guard", ("cqa005_completed == 0", "False → terminating output", "True → quest Active"), "panel-blue"),
            ("Child setup", ("meet Active + mappin Active", "community Activate", "wait entireCommunity > 0", "wait IsInside setup"), "panel-green"),
            ("Contact", ("checkpoint", "scene start", "contact_done", "meet Succeeded"), "panel-magenta"),
            ("Cleanup + return", ("mappin Inactive", "leave Active / IsOutside", "community Deactivate whole", "root succeeds + fact=1"), "panel-amber"),
        ),
        ("True", "inside", "outside / Out1"),
        evidence,
        status,
        "conceptual-lifecycle",
    )


def render_trigger_plan(evidence: str, status: str) -> str:
    parts = svg_open(1240, 760, "cqa005 trigger-volume plan", "Top-down conceptual plan of the nested setup and cleanup trigger volumes around the Allen Street contact.", {"diagram": "conceptual-trigger-volume-plan", "evidence_class": evidence})
    parts.extend([text(40, 48, "cqa005 trigger-volume plan", "title"), text(40, 77, "Allen Street • shared center X -1000.02 / Y 1497.2208", "subtitle")])
    parts.extend(['<circle cx="420" cy="390" r="270" fill="#493510" fill-opacity="0.45" stroke="#f3be55" stroke-width="3"/>', '<circle cx="420" cy="390" r="85" fill="#182b49" fill-opacity="0.8" stroke="#78a9ff" stroke-width="3"/>', '<circle cx="420" cy="390" r="10" fill="#e07abc"/>'])
    parts.extend([text(420, 135, "cleanup • radius 110 • IsOutside", "label", anchor="middle"), text(420, 325, "setup • radius 25", "label", anchor="middle"), text(420, 420, "contact / AI spot / scene marker", "detail", anchor="middle")])
    panel(parts, 760, 160, 400, 310, "panel-green", "Exact serialized plan", ("setup: 16-point outline", "setup Z 2.3 • height 12", "cleanup: 20-point outline", "cleanup Z 0.3 • height 16", "contact Z 6.957 • yaw 88.6", "scene + mappin markers AlwaysLoaded"))
    parts.extend([text(760, 525, "The circles explain nesting; the CR2W stores polygon outlines.", "warn"), text(1180, 700, f"{evidence} — placement runtime {status}", "note", anchor="end"), "</svg>"])
    return "\n".join(parts) + "\n"


def outputs() -> dict[str, str]:
    evidence = evidence_label()
    status = acceptance_status()
    root_fingerprint = graph_fingerprint(ROOT_SOURCE, ROOT_NODES, ROOT_EDGES)
    child_fingerprint = graph_fingerprint(CHILD_SOURCE, CHILD_NODES, CHILD_EDGES)
    return {
        "cqa005.questphase.layout.json": layout_json("cqa005 First Contact root questphase", 2550, 780, ROOT_NODES, ROOT_EDGES, root_fingerprint),
        "cqa005.root.questphase.svg": render_graph("cqa005 First Contact — root graph", "7 nodes • 7 edges • root owns one-shot completion", 2550, 780, ROOT_SOURCE, ROOT_NODES, ROOT_EDGES, root_fingerprint, evidence, status),
        "cqa005_contact.questphase.layout.json": layout_json("cqa005 First Contact external child questphase", 4720, 430, CHILD_NODES, CHILD_EDGES, child_fingerprint),
        "cqa005.child.questphase.svg": render_graph("cqa005 First Contact — external child graph", "15 nodes • 14 edges • spawn, scene, cleanup, terminating return", 4720, 430, CHILD_SOURCE, CHILD_NODES, CHILD_EDGES, child_fingerprint, evidence, status),
        "cqa005.scene.svg": render_scene(evidence, status),
        "cqa005.community-identity.svg": render_community_identity(evidence, status),
        "cqa005.resource-chain.svg": render_resource_chain(evidence, status),
        "cqa005.lifecycle.svg": render_lifecycle(evidence, status),
        "cqa005.trigger-volume-plan.svg": render_trigger_plan(evidence, status),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify checked diagram outputs are current")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for name, content in outputs().items():
        targets = [ASSET_DIR / name]
        if name.endswith(".svg"):
            targets.append(PUBLISH_DIR / name)
        for target in targets:
            if args.check:
                if not target.is_file() or target.read_text(encoding="utf-8") != content:
                    raise SystemExit(f"{target}: generated Lab 5 diagram is stale")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
