# Labs at a glance

The five labs form one progression from a registered root questphase to a
community-backed spoken scene. Each lab is a complete, mod-owned WolvenKit
project with a start checkpoint, a completed checkpoint, an exact structural
contract, and a separate runtime-acceptance record.

Use the title, namespace, and project name in this table consistently. `Lab 1`
is the reader-facing number; `cqa001` is its resource namespace;
`CQA_Lab01_OneShot` is its completed WolvenKit and installed-file stem. Those
three names belong to different domains and are not interchangeable.

## Reading sequence

| Lab | Canonical title and namespace | Primary boundary | Build and test |
| --- | --- | --- | --- |
| 1 | **First Signal** · `cqa001` | Root registration, journal state, real-time delay, one-shot fact | [Overview](../start-here/lab-01.md) · [Author](../start-here/lab-01-authoring.md) · [Test](../start-here/install-and-test.md) |
| 2 | **Signal Race** · `cqa002` | Immediate selection, pause conditions, parallel listeners, XOR-shaped convergence | [Overview](../gates/lab-02.md) · [Author](../gates/lab-02-authoring.md) · [Test](../gates/lab-02-test.md) |
| 3 | **Boundary Check** · `cqa003` | Streaming block/sector ownership, NodeRefs, marker, nested trigger volumes | [Overview](../world/lab-03.md) · [Author](../world/lab-03-authoring.md) · [Test](../world/lab-03-test.md) |
| 4 | **Handoff Point** · `cqa004` | Registered root, archive-resolved external child, `In1`/`Out1` handoff | [Overview](../questphases/lab-04.md) · [Author](../questphases/lab-04-authoring.md) · [Test](../questphases/lab-04-test.md) |
| 5 | **First Contact** · `cqa005` | Community lifecycle, actor acquisition, one-line scene, named exit, cleanup | [Overview](../scenes/lab-05.md) · [Author](../scenes/lab-05-authoring.md) · [Test](../scenes/lab-05-test.md) |

The topical table of contents places each lab beside the system it teaches, so
Lab 4 appears under Questphases before the later-numbered topical sections. The
table above is the canonical **practical** sequence.

## Checkpoint identity

| Lab | Completed project/file stem | Start ZIP | Completed ZIP |
| --- | --- | --- | --- |
| 1 | `CQA_Lab01_OneShot` | [Download](../downloads/cqa-lab-01-start.zip) | [Download](../downloads/cqa-lab-01-completed.zip) |
| 2 | `CQA_Lab02_SignalRace` | [Download](../downloads/cqa-lab-02-start.zip) | [Download](../downloads/cqa-lab-02-completed.zip) |
| 3 | `CQA_Lab03_BoundaryCheck` | [Download](../downloads/cqa-lab-03-start.zip) | [Download](../downloads/cqa-lab-03-completed.zip) |
| 4 | `CQA_Lab04_HandoffPoint` | [Download](../downloads/cqa-lab-04-start.zip) | [Download](../downloads/cqa-lab-04-completed.zip) |
| 5 | `CQA_Lab05_FirstContact` | [Download](../downloads/cqa-lab-05-start.zip) | [Download](../downloads/cqa-lab-05-completed.zip) |

A start and completed checkpoint for the same lab own the same depot paths.
They are alternative source states, not two mods to install together. Lab 2's
edited timing variant is another separately hash-bound candidate. Install only
the candidate named by the current test case, with the game and framework
processes closed.

## What every evidence label means here

All five completed checkpoint structures have passed the repository's exact
source, graph, package, and WolvenKit `8.19.0` round-trip gates. That supports
**Structurally validated** claims about the resources and their serialized
relationships. It does not by itself prove mounting, presentation, timing,
streaming, scene playback, cleanup, or reload behavior.

The dedicated marker on each linked lab page mirrors that lab's canonical
runtime-acceptance record:

- a pending or failed campaign leaves its in-game claims **Experimental**;
- a complete passing campaign promotes only the exact hash-bound cases it
  records to **Runtime-proven**;
- a comparable base-game extract may support **Observed in vanilla**, but does
  not prove the mod-owned candidate;
- legacy Ghostline results remain evidence for their named historical
  candidate and version record, not an automatic promotion of a lab.

Do not rewrite a label from memory. Follow the lab marker and its test page.

## Shared practical baseline

The practical guides use Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`. See [Tested
versions](tested-versions.md) for roles and boundaries. Every runtime campaign
also requires the clean-save and candidate-isolation rules in its own test
page; sharing a tool version does not make two save histories equivalent.

Next: [Glossary](glossary.md).
