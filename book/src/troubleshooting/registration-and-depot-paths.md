# Registration and depot paths

Registration makes a root resource reachable. Packing makes a resource
available at a depot path. A working quest usually needs both, but not every
resource is registered in the same way.

## Evidence and version boundary

Use Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31` for the first-release
procedure.

**Structurally validated:** Labs 1–5 freeze their exact packed depot paths and
ArchiveXL registrations. Lab 4 registers its root questphase once while its
external child is only packed and reached through the parent's soft
`phaseResource`.

**Observed in vanilla:** the native parent path used by the labs is
`base\quest\cyberpunk2077.quest`. It is referenced, not redistributed. Vanilla
resource paths cited elsewhere in the book must likewise be extracted from the
reader's own installation.

Exact lab runtime behavior follows each lab's acceptance record. A clean
registration log is intermediate loader evidence; it does not promote any
quest route beyond the label already supported by that route's record.

## Separate the four edges

```text
archive payload path
        |
        +-> loose ArchiveXL configuration
                    |
                    +-> registered root
                              |
                              +-> native child/resource references
```

| Edge | Example owner | Failure |
| --- | --- | --- |
| Packed payload | `.archive` depot tree | Resource does not exist at the path requested |
| Loose configuration | `.archive.xl` beside the archive | ArchiveXL never sees the registration instructions |
| Root attachment | `quest.phases`, `journal`, `localization`, or `streaming.blocks` | Root system does not expose the mod resource |
| Nested resolution | `phaseResource`, subtitle map, block descriptor, or another CR2W reference | Root registers, but a child dependency fails later |

An external child questphase is not automatically another root. Registering
both parent and child can create two independent root attachments while still
leaving the parent's intended composition unproved.

## Diagnose a quest that never starts

1. Close the game and every framework process.
2. Inventory `archive\pc\mod` for every candidate-owned `.archive` and
   `.archive.xl`. Hash every intended and duplicate file before changing the
   live directory.
3. Move or disable every unintended live copy into a named quarantine outside
   all active mod/framework paths. Do not delete the preserved evidence.
4. Inventory `archive\pc\mod` again and require exactly the intended candidate
   pair, with no renamed or older copy that can still mount.
5. Hash the intended pair and compare it with the built candidate.
6. List the archive and confirm the exact root depot path appears once.
7. Extract that entry and compare its hash with WolvenKit project output.
8. Open the `.archive.xl` as text and compare its `path` character for
   character with the archive listing.
9. Launch to the load menu and preserve fresh RED4ext, ArchiveXL, game, and
   redscript logs.
10. Search for the candidate filename, resource path, and the first missing
   dependency. Record an error's full context rather than one line.
11. Only after registration is clean should you test the graph from a valid
   starting save.

Depot paths use backslashes in the canonical resources in this book. Do not
silently add a filesystem drive, project `source\archive` prefix, or game
install prefix to the virtual depot path.

## Diagnose a root that registers but stalls later

Trace the first external reference reached by execution:

| Symptom | Inspect next |
| --- | --- |
| Parent enters a phase node and stops | `phaseResource.DepotPath`, soft reference form, child archive entry, and child `In1` interface |
| Journal entries never render | Journal registration, full `gameJournalPath.realPath`, `fileEntryIndex`, and entry state socket |
| Text is blank | Correct localization registration class and exact secondary key or numeric RUID |
| World objective has no trigger/marker | Registered streaming block, descriptor sector path, prefab root, and child NodeRef chain |
| Scene starts but line has no text/audio | Subtitle-map and VO-map registrations plus their nested resource paths |

Do not add a second root registration to repair a missing nested path. Fix the
edge that owns that path.

## Compare registration classes

ArchiveXL configuration sections are not interchangeable:

| Responsibility | Registration surface used in the labs |
| --- | --- |
| Executable root questphase | `quest.phases` with mod path and vanilla parent |
| Journal tree | `journal` |
| Journal/UI text | `localization.onscreens` for the locale |
| Spoken subtitles | `localization.subtitles` for the locale |
| Spoken audio lookup | `localization.vomaps` for the locale |
| World loading | `streaming.blocks` |

A `.scene`, external child questphase, subtitle entries resource, VO WEM, or
streaming sector can be packed and reached through another registered resource
rather than registered as an independent root. Follow the ownership chain in
the relevant chapter.

## Stale-install control

A duplicate archive can make a removed resource appear to work. A duplicate
`.archive.xl` can register an old path while the current file is wrong. For an
isolation run:

- keep one exact candidate pair;
- keep only the pinned framework stack and explicitly required lab files;
- record unrelated mod inventory as absent rather than relying on memory;
- restart the game after any mounted-file change;
- hash installed bytes again before interpreting the result.

Changing the installed pair does not clean save-backed facts, journal state,
active nodes, scenes, communities, or devices. Use [Save state and clean
retests](save-state-clean-retests.md) before calling a registration correction
successful.

## Common false fixes

| False fix | Why it misleads |
| --- | --- |
| Register every CR2W as a root | Changes ownership and may start resources independently |
| Copy an extracted vanilla parent into the archive | Creates a global override and redistributes game content |
| Rename only the project file | Leaves ArchiveXL and nested ResourcePaths pointing at the old depot path |
| Edit the graph until a log error disappears | Registration occurs before the affected runtime branch |
| Test only an old completed save | Its guard can bypass the entire broken route |

Previous: [Serialization versus runtime](serialization-vs-runtime.md). Next:
[Handles, sockets, and resources](handles-sockets-resources.md).
