# Location research

Safe location research produces a provenance record and a small mod-owned
fixture. It does not produce a folder of redistributed vanilla CR2W files. The
goal is to answer where a native object lives, which resources own it, how it
is addressed, and which observations still require an in-game test.

## Evidence and version boundary

This workflow keeps three ledgers:

| Ledger | Confidence label | What belongs in it |
| --- | --- | --- |
| Vanilla structure | **Observed in vanilla** | Exact depot path, focused property excerpt, node type, NodeRef, transform, and owner chain extracted from the researcher's installation |
| Mod-owned structure | **Structurally validated** | Round-trip, handle/reference checks, packed paths, block registration shape, and deterministic fixture fingerprints |
| Runtime behavior | **Runtime-proven** | Exact installed fixture, clean starting save, test route, visible behavior, reload cases, logs, and result |

An untested idea belongs under **Experimental**, even when every input was
copied accurately into research notes.

The retained reference extracts use WolvenKit JSON `0.0.9`, serialized by
WolvenKit `8.17.4`, with CR2W `GameVersion: 2310`. The practical authoring and
acceptance target is Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`,
ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`. Record the
versions actually used for every new extraction and test; do not silently
merge evidence from the two environments.

## Retained comparison paths

These depot paths form a focused research route. Extract them from your own
game with WolvenKit. Do not commit or distribute the extracted CR2W files.

| Depot path | Question it can answer |
| --- | --- |
| `base\worlds\03_night_city\_compiled\default\03_night_city.streamingworld` | Which global resources and compiled block list the native world root references |
| `base\worlds\03_night_city\_compiled\default\blocks\all.streamingblock` | Which descriptor points to a sector, with which category, level, box, and quest-prefab root |
| `base\worlds\03_night_city\_compiled\default\quest_606b61008df2ba6f.streamingsector` | How one focused Quest sector relates nodes, placements, NodeRefs, triggers, and a quest-prefab namespace |
| `base\worlds\03_night_city\_compiled\default\always_loaded_0.streamingsector` | How one AlwaysLoaded sector registers references and marker-related content without assuming compact array pairing |
| `base\worlds\03_night_city\_compiled\default\exterior_-17_22_0_0.streamingsector` | Where the vanilla Allen Street fast-travel terminal is placed and which entity template it uses |
| `base\worlds\03_night_city\_compiled\default\always_loaded_1.streamingsector` | Where that terminal's linked fast-travel destination marker is registered and placed |
| `base\localization\en-us\onscreens\onscreens.json` | Which player-facing English label is assigned to the terminal record's localization key |
| `base\quest\main_quests\part1\q108\phases\q108_06b_tower_mainframe.questphase` | How one vanilla phase declares prefab dependencies and uses local trigger, device, scene-marker, AI-spot, and spline references |
| `base\journal\cooked_journal.journal` | How quest mappins and their local world references are represented in the journal tree |
| `base\worlds\03_night_city\_compiled\default\exterior_19_-8_0_0.streamingsector` | How one placed laptop is linked to node data, an entity template, node-local instance data, and cooked prefab data |
| `base\worlds\03_night_city\_compiled\default\4fd0915183681e53.streamingsector_inplace` | What that placement's separate inplace resource embeds—and what it does not own |
| `base\gameplay\devices\drop_points\drop_point.ent` | Which components and local UI/navigation slots one drop-point template exposes |
| `base\worlds\03_night_city\_compiled\default\03_night_city.devices` | Whether a searched device identity appears in one global device registry |

Each row is a retained **Observed in vanilla** research target, not a complete
template or a guarantee that the same relationship applies to another
location.

## Start from the player-facing site

Before extracting resources, write down the intended behavior:

- safe and legal player access at the quest's intended time;
- on-foot and, if relevant, vehicle approach;
- approximate player/world coordinates and vertical level;
- nearby doors, elevators, interiors, restricted areas, traffic, and combat;
- a sensible marker and navigation endpoint;
- enough space for the trigger outline and its test approaches;
- expected behavior after fast travel and active-state reload, plus whether a
  completed-save reload stays inactive.

Take your own reference screenshots for private research if useful, but explain
the published model with coordinates, conceptual diagrams, property tables,
and mod-owned resources. Do not use WolvenKit graph screenshots as the chapter's
graph explanation.

## Boundary Check worked location record

Lab 3 centers its mod-owned marker and two trigger outlines on the outdoor
recycling-station cabinet row in Watson/Kabuki at
`(-1000.02, 1497.2208, 8.3)`.

**Observed in vanilla:** extracting
`base\worlds\03_night_city\_compiled\default\exterior_-17_22_0_0.streamingsector`
from your own game shows the fast-travel terminal entity at node index `1766`:

| Field | Focused value |
| --- | --- |
| TweakDB record | `FastTravelPoints.wat_kab_dataterm_12` |
| Full NodeRef | `$/03_night_city/c_watson/kabuki/kabuki_data_terminals_prefabW7DFTCQ/#wat_kab_dataterm_12/{kab_data_term_}12_prefabBARKVWA` |
| Entity template | `base\gameplay\devices\fast_travel\data_term_1.ent` |
| Entity position | `(-1064.30457, 1436.18298, 4.95000076)` |

Its point record resolves through the installed `r6\cache\tweakdb.bin` to
`displayName: LocKey#79217`; the English `onscreens.json` maps key `79217` to
`Allen Street`. The linked destination is **Observed in vanilla** at node
index `5757` in `always_loaded_1.streamingsector`:

| Field | Focused value |
| --- | --- |
| Marker NodeRef | `$/03_night_city/c_watson/kabuki/kabuki_data_terminals_prefabW7DFTCQ/#wat_kab_dataterm_12/#wat_kab_dataterm_12_tp` |
| Marker position | `(-1065.76489, 1435.83472, 4.94000006)` |

The entity is about 88.6 m and the linked marker about 89.95 m horizontally
southwest of the lab center. A calculation against the 20-sided 110 m leave
outline leaves about 18.8 m of directional margin at the marker; both Z values
lie within the outline's base `0.3` and height `16`. The next cataloged
terminal is about 131 m from the center and outside that outline. These are
structural observations and geometry calculations, not player-access evidence.
Do not redistribute either extracted sector or the extracted localization.

**Experimental:** confirm on the pinned game build that Allen Street is
unlockable and usable, that the public northeast route reaches the cabinet row,
that the row is independently recognizable without the quest pin, and that the
110 m trigger behaves as calculated. Lab 3's test protocol retains those as
runtime questions rather than promoting them from coordinates alone.

## Trace owners outward, then inward

Use two passes.

### Pass 1: world registration

```text
streamingworld.blockRefs
  -> streamingblock.descriptors
     -> descriptor.data
        -> streamingsector
           -> nodeData + nodes + nodeRefs
```

Record the descriptor index or distinguishing fields, sector depot path,
category, level, streaming box, and quest-prefab root. In the sector, locate
the placement by coordinate or full NodeRef, then record `NodeIndex`, node
type, transform, bounds, and `QuestPrefabRefHash`. Do not assume the three
sector arrays are parallel merely because one compact sample is.

### Pass 2: referenced behavior

Follow only the references needed for the behavior:

```text
trigger -> AreaShapeOutline buffer + notifier -> quest trigger condition
marker  -> journal mappin reference -> quest mappin manager
device  -> entity template + instanceData -> optional registry/persistence
```

For a quest-owned NodeRef, locate the phase prefab dependency and the exact
quest node or condition that consumes the local form. For a journal pin,
retain the narrow containing journal subtree and `gameJournalPath`, not the
entire cooked journal. For a device, separate the entity template, node-local
RedPackage, inplace resource, `.devices`, and `.psrep` questions.

## Keep a focused evidence record

A useful location record contains:

| Field | Example of the required precision |
| --- | --- |
| Observation date and game build | Exact build/storefront used for the in-game visit |
| WolvenKit version | Exact version used to extract and serialize the focused view |
| Depot provenance | Exact paths and archive source for every retained claim |
| World identity | Full NodeRef plus local form only where its resolution context is known |
| Placement | Position, quaternion or yaw, scale, pivot, bounds, and coordinate source |
| Resource chain | Root, block descriptor, sector, node-data row, node, template, and optional inplace/registry owners |
| Focused excerpt | Only decisive fields, with array indices or stable identifiers |
| Evidence label | One of the four exact confidence labels, attached to the bounded claim |
| Runtime case | Starting save, route, expected result, observed result, logs, and fixture hashes |

Hash mod-owned fixtures and generated diagrams. For vanilla resources, the
important public artifact is the depot path and extraction procedure; a hash
can help private provenance but does not grant redistribution rights.

## Turn observation into a mod-owned fixture

Do not copy the extracted sector and delete most of it. Create the smallest
mod-owned arrangement that expresses the researched relationship:

1. Choose a unique namespace, prefab root, and child NodeRefs.
2. Author a mod-owned sector with only the explained nodes.
3. Author a mod-owned block and register it through ArchiveXL.
4. Reference vanilla entity templates by depot path only when redistribution
   is unnecessary and the dependency is intentional.
5. Preserve opaque cooked values from a known-good mod-owned seed or editor
   output; do not invent meanings for `Uk*` properties.
6. Round-trip, validate, pack, and inventory the archive.
7. Test from a save made before any version of the fixture was installed.

Every supplied node and resource in a downloadable project must be explained.
The project is executable reference material, not a magic template.

## Separate the save from the archive

Facts, journal states, active objectives, tracker history, scenes, communities,
and device persistent state can survive an archive rebuild. A location edit can
appear to fix a static marker while the quest still follows an old checkpoint;
the two observations diagnose different owners.

Retain at least:

- one pre-install clean save;
- one save before the area or device first streams;
- one save before the initial reach crossing;
- one mid-objective save after reach while still inside the outer leave trigger;
- one completed-state save;
- a written reset procedure that names every save-backed variable it changes.

Never describe “set the completion fact back to zero” as a clean-save reset.
It does not clear journal, tracker, scene, community, or device state.

## Location acceptance matrix

| Case | Evidence sought |
| --- | --- |
| Approach from each practical direction | Streaming, collision, access, marker height, and trigger boundary |
| Approach from a different elevation | Vertical trigger coverage and endpoint placement |
| Start outside | Negative control for state conditions and premature UI |
| Save/reload before entry | Registration and quest-state restoration |
| After reach, save/reload inside the outer leave area | Active leave-state behavior and loaded target resolution |
| Stream away and return before reach | Visible continuity and lookup errors while the objective is active; no precise unload claim without instrumentation |
| Fast travel nearby | Separate load/route case; never substitute it for an ordinary crossing |
| Complete and reload | One-shot guard, journal cleanup, and persistent world/device state |
| Remove/reinstall on an old save | Demonstrates save contamination; it is not the primary acceptance route |

Capture visible player-facing evidence and logs. A successful coordinate
search, sector extraction, or static CR2W validation cannot prove navigation,
interaction, or reload behavior.

## Common failures

| Symptom | Likely research mistake |
| --- | --- |
| Correct coordinates, wrong sector | Multiple vertical/grid layers or a nearby composite prefab were conflated |
| `NodeIndex` resolves the wrong node | Placement row order was treated as array identity |
| Copied reference works only in vanilla | Its prefab root, variant, global registry, or save identity was an unstated dependency |
| Marker is visible but route ends badly | Visual anchor and traversable navigation endpoint were treated as the same point |
| Device appears but custom behavior is absent | Template, node-local package, registry, and persistence owners were collapsed into one assumption |
| Trigger looks correct in properties but fires as a square | The visible points were trusted instead of `AreaShapeOutline.buffer` |
| Result changes after reinstall | Save-backed facts, journal, checkpoints, or device state contaminated the comparison |
| Research folder is too large to review | Whole vanilla resources were retained instead of focused excerpts and a provenance table |

Previous: [Devices and persistence](devices-and-persistence.md). Next: [Lab 3:
Boundary Check](lab-03.md).
