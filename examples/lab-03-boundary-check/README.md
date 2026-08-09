# Lab 3 — Boundary Check

**Lab 3 runtime evidence:** **Experimental** — pending.

This directory contains two incremental WolvenKit checkpoints for a small
world-integrated quest:

- `start`: the complete mod-owned world, journal, localization, and
  ArchiveXL scaffold with a terminating two-node questphase;
- `completed`: the same scaffold with the 16-node `cqa003` graph that marks a
  checkpoint, waits until the player is inside its reach volume, then waits
  until the player is outside its wider leave volume.

Both checkpoints use only mod-owned resources. They inherit a test location
and trigger geometry from earlier Ghostline research, but that provenance does
not prove this new resource set in game. The cooked resources are
**Structurally validated** with WolvenKit 8.19.0; all `cqa003` mounting,
streaming, marker, trigger, navigation, and save behavior remains
**Experimental** until `runtime-acceptance.json` is completed.

Do not install both checkpoints together. They register the same depot paths.
