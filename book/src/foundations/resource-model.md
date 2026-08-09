# Resources and ownership

A questphase is a coordinator. It can change facts and journal state, wait on
conditions, start scenes, refer to world objects, and run child phases. It does
not make the referenced journal entry, scene, actor, trigger, or localized text
exist.

That distinction is the first debugging tool: when a lookup fails, identify the
resource that owns the missing thing before changing the graph that refers to
it.

## The resource layers

| Layer | Typical resources | Owns |
| --- | --- | --- |
| Quest control | `.questphase` | Execution flow, conditions, journal operations, facts, child-phase and scene handoff |
| Journal and UI | `.journal` | Quest, phase, objective, description, message, file, and map-pin entries |
| Localization | onscreen JSON resources, subtitle maps, VO maps, embedded scene `locStore` | Player-facing text through separate lookup systems |
| Scenes | `.scene`, lipsync and animation references | Dialogue, choices, performers, timed events, entry points, and named exits |
| World | streaming blocks, streaming sectors, inplace resources, `.devices` | Triggers, markers, communities, AI spots, devices, and NodeRef registration |
| Characters | `.ent`, `.app`, TweakDB records, community entries | Entity composition, appearances, gameplay records, and spawned identities |
| Framework registration | ArchiveXL and related loose configuration | Merging or registering mod-owned resources with game roots |

One player-facing beat can cross several rows. “Reach the marker and talk to a
contact” needs at least a questphase, journal entries, localization, world
markers and triggers, a community, and a scene. No one row silently supplies
the others.

## Depot paths

A depot path is the resource's address inside the game's virtual resource
space:

```text
mod\cqa\cqa001\phases\cqa001.questphase
```

The same address appears in several contexts:

- as a file beneath a WolvenKit project's `source\archive`;
- as a `ResourcePath` value inside another CR2W resource;
- as an ArchiveXL registration path;
- as a path printed in packing or runtime logs.

Use the spelling and backslashes shown by WolvenKit. A Windows filesystem path
such as `H:\mods\...` is not a depot path and must never be serialized as the
resource address.

The `mod\cqa\...` prefix means that the example owns the resource. A reference
to `base\quest\cyberpunk2077.quest` points to a vanilla resource; it does not
copy that resource into the project.

## Ownership versus reference

Owning and referring are different:

```text
cqa001.questphase
    refers to journal path quests/minor_quest/cqa001

cqa001.journal
    owns the cqa001 journal entry

cqa001 journal entry
    refers to localization key cqa_cqa001_title

cqa001 onscreen localization
    owns the English text First Signal
```

Changing the questphase cannot repair a missing localization key. Changing the
localization resource cannot activate an objective. Follow the lookup to its
owner.

## WolvenKit project layers

The examples use this source layout:

```text
source/
├── archive/      CR2W resources at their intended depot paths
├── raw/          serialized review artifacts for mod-owned CR2W resources
└── resources/    loose ArchiveXL and other framework configuration
```

`source\archive` and `source\resources` have different installation
destinations. Packing the CR2W tree does not automatically prove that the loose
ArchiveXL file was staged, and seeing a valid `.archive` does not prove that
the root questphase was registered.

The `source\raw` copies support review, round trips, and deterministic diagrams.
They are documentation-author artifacts, not an instruction to make raw JSON
editing the beginner workflow.

## Lab 1 ownership map

Lab 1 deliberately stops at three native resources:

| Outcome | Owner |
| --- | --- |
| Run once, wait, and finish | `cqa001.questphase` |
| Define the quest and objective | `cqa001.journal` |
| Display “First Signal” and “Wait for the signal.” | `cqa001` onscreen localization |
| Attach all three to game roots | `CQA_Lab01_OneShot.archive.xl` |

It has no world resource. That is why player position is irrelevant to Lab 1.

## Diagnostic questions

When a feature is absent, ask in this order:

1. Does the owning resource exist at the exact depot path?
2. Was that resource packed or staged in the correct installation layer?
3. Was it registered or merged where required?
4. Does the referring resource use the correct identifier domain?
5. Does runtime state permit this resource to activate now?

A graph edit belongs at step five only when the first four answers are already
known.
