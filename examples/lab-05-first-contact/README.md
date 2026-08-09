# Lab 5 — First Contact

**Lab 5 runtime evidence:** **Experimental** — pending.

This directory contains two incremental WolvenKit checkpoints for a compact
community-backed contact scene:

- `start`: a registered root that passes through an archived child, while the
  child and scene are deliberately inert structural shells;
- `completed`: the same resource inventory with passive community activation,
  spawned-character and trigger waits, a one-line scene, named scene exit,
  cleanup, and root-owned one-shot completion.

Each checkpoint contains exactly eleven mod-owned CR2W resources and one
archived WEM. The source WAV and its provenance record live once under
`voice-source`, outside either WolvenKit project's `source` tree. The
deterministic download packager copies that shared provenance directory under
each ZIP's project root without making it part of the game archive.

ArchiveXL registers only the root phase, journal, onscreen table, subtitle map,
voiceover map, and streaming block. The child phase, scene, subtitle entries,
WEM, and two sectors remain archived dependencies resolved through those
registered roots.

Combined `cqa005` behavior covered by the frozen eleven-case campaign follows
the synchronized marker above. Structural validation means WolvenKit 8.19.0
accepted and serialized all twenty-two CR2W pairs; by itself it does not prove
spawning, ordinary scene playback, subtitle or audio lookup, named-exit
continuation, stream-away/return, cleanup, post-`contact_done` reload, or
completed reload. The gate includes the exact named pre-scene seed loads in
Cases 3, 4, and 7. Active-line interruption or `CutDestination`, arbitrary or
unlisted pre-scene active-child states, and facial/workspot-animation quality
remain **Experimental** outside that campaign.

The schema-version-4 campaign binds five manual source captures: two untouched
originals plus the pre-scene, post-contact, and completed seeds made during
Case 1's continuous ordinary route. Every execution uses a closed-game copy of
the complete source slot, and all runs that reference one capture must retain
its exact `sav.dat` hash.

Do not install both checkpoints together. They own the same depot paths.
