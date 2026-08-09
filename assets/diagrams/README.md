# Diagram sources

This directory is reserved for source files and exported assets used to explain
quest graphs.

Prefer deterministic, reviewable sources such as Mermaid or generated SVG.
Every diagram should have a textual explanation and should follow the visual
grammar in [`../../STYLE.md`](../../STYLE.md). Raw WolvenKit graph screenshots
are not the primary teaching format.

Exact graph figures use WolvenKit CR2W-JSON as their structural source and a
layout-only JSON file in this directory. The renderer records and checks a
structural SHA-256 fingerprint so a changed example cannot silently retain a
stale figure.
