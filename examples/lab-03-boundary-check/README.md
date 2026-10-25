# Lab 3 — Boundary Check

**Lab 3 runtime evidence:** **Experimental** — pending.

This directory contains two incremental WolvenKit checkpoints for a small
world-integrated quest:

- `start`: the complete mod-owned world, journal, localization, and
  ArchiveXL scaffold with a terminating two-node questphase;
- `completed`: the same scaffold with the 16-node `cqa003` graph that marks a
  checkpoint, waits until the player is inside its reach volume, then waits
  until the player is outside its wider leave volume.

Both checkpoints use mod-owned resources and are **Structurally validated**
with WolvenKit `8.19.0`. Follow the lab test guide for world and save behavior.

Do not install both checkpoints together. They register the same depot paths.
