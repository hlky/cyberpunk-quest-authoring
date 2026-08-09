# Serialization versus runtime validity

A successful save, conversion, or archive build is an intermediate result.
The game can receive a readable CR2W whose graph is smaller than the authored
graph, whose nested values are stale, or whose external references cannot
resolve.

## Evidence and version boundary

Run the current procedure with Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit
`8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`.

**Structurally validated:** the five tutorial labs compare mod-owned authored
resources with WolvenKit round trips, exact graph/resource contracts, archive
manifests, and extracted package contents. Those checks prove retained
structure, not in-game behavior.

**Structurally validated:** a retained legacy vehicle-lab investigation at
research commit `a24c341c1e2eca43f05a100f5776baba377b2260` showed a writer
returning success while omitting three phase nodes, one vehicle assignment
node, two spawn-set mappings, and later several bound scalar values.

**Runtime-proven:** candidate archive
`355C442781509F69B61745AF0889CDD32EEA825BA0E480AAD97A8DAF2CCE90BE`
crashed reproducibly while loading a save. WolvenKit-rebuilt topology produced
candidate
`BA94F1F88E91DA2E5C1E15D956E1AE867048029F4894C65F0A7B6DA6403436C1`,
which loaded without that crash but still lacked the intended journal and
vehicles. These are bounded runtime observations, not a successful route.

**Experimental:** a later round trip exposed literal placeholder scalars and
led to candidate
`B5C9527AEAC233D3D9885B276E4898EE67114CA0FBDE3A7EBC57413EC06AB04A`.
No retained successful runtime result is bound to that candidate. The complete
legacy sequence supports the validation method, not WolvenKit `8.19.0`, the
current labs, or a claim that the final candidate worked in game.

## Recognize the misleading success

| Symptom | Likely boundary | Decisive test |
| --- | --- | --- |
| Converter exits zero but nodes are missing | CR2W object-graph/topology write | Serialize the produced binary back and compare semantic node counts and edges |
| Graph shape matches but a path is still a template token | Nested scalar write | Search the round trip for unexpected placeholders and compare decisive properties |
| Archive packs but root never starts | Registration or depot path | List/extract the archive, then inspect ArchiveXL registration logs |
| ArchiveXL registers everything but load crashes | Native resource content or runtime lookup | Reduce to the earliest activation boundary; inspect scene/world/resource cardinalities |
| Behavior differs after reinstalling identical bytes | Save-backed state | Compare a pre-install original with a completed or contaminated save |

Do not diagnose from the last visible symptom alone. A journal objective that
never appears can be caused by an omitted node, a stale journal path, failed
registration, or a saved branch that already passed the activation node.

## Compare meaning, not bytes

An intentional CR2W edit can legitimately change handle allocation, import
order, or other serialization details. A useful round-trip comparison freezes
the semantic contract instead:

- root type and version;
- graph node types and graph-local IDs;
- input/output/cut socket names and roles;
- every source-socket to destination-socket edge;
- decisive nested conditions, operations, paths, names, and numeric IDs;
- resource-reference array lengths and every referenced index;
- world registries, NodeRefs, placements, and typed buffer rows;
- journal paths and `fileEntryIndex` values;
- absence of unrequested placeholder strings.

For a nine-node authored graph, a readable six-node round trip is a failed
write. It must not be packaged merely because both files begin with a CR2W
header.

## Run the boundary test

1. Save the resource in WolvenKit and close its editor tab so the binary on
   disk is final.
2. Convert or serialize that binary to an isolated review directory.
3. Compare it with the authored inventory. Start with counts, type sets,
   sockets, edges, and decisive values rather than a full textual diff.
4. Reopen the binary in WolvenKit and inspect the same nodes and nested
   properties.
5. Pack only after the focused comparison passes.
6. List and extract the candidate archive to a new directory.
7. Hash each extracted payload against the project output and record the
   candidate archive hash.
8. Install that exact candidate and confirm the installed hash still matches.

If a tool cannot represent an edit, the safe result is a clear failure. Do not
keep an output that silently retained a template's smaller array or older
scalar.

## Narrow the fix

When the round trip is wrong:

1. Return to the last structurally correct resource.
2. Recreate only the first missing object or value in WolvenKit.
3. Save and round-trip immediately.
4. Verify all existing topology as well as the new edit.
5. Delete the rejected candidate from install staging so it cannot be mounted
   accidentally.

When the round trip is correct but runtime still fails, stop editing the
serializer boundary. Move to registration, references, lifecycle ordering, or
save state according to the earliest observed failure.

## Claims after a correction

| Result | Supported label |
| --- | --- |
| Binary round trip and semantic checks pass | **Structurally validated** |
| Same shape exists in a cited vanilla resource | **Observed in vanilla** |
| Exact hash-bound candidate passes the defined game route | **Runtime-proven** |
| Candidate is unplayed, reload cases are incomplete, or several variables changed | **Experimental** for those runtime claims |

A non-crashing load alone does not prove journal presentation, cleanup,
reload, or replay. Promote only the cases actually exercised.

Previous: [Troubleshooting](index.md). Next: [Registration and depot
paths](registration-and-depot-paths.md).
