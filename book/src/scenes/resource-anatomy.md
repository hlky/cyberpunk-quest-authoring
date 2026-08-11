# Scene resource anatomy

The First Contact scene is a native `.scene` CR2W resource rooted at
`scnSceneResource`. Its root records more than the visible node graph. Actor
acquisition, entry and exit names, screenplay data, localization storage,
referenced animation sets, interruption policy, debug symbols, and graph
metadata all belong beside the graph.

## The outer resource

This is the focused shape used by the completed checkpoint. Handle wrappers
and unrelated serialization metadata are omitted:

```text
scnSceneResource
├── version: 5
├── cookingPlatform: PLATFORM_PC
├── sceneCategoryTag: minorQuests
├── actors: [contact actor 0]
├── playerActors: [V actor 1]
├── entryPoints: [start -> node 1]
├── exitPoints: [contact_done -> node 3]
├── interruptionScenarios: [Default scenario 0]
├── screenplayStore: scnscreenplayStore
├── locStore: scnlocLocStoreEmbedded
├── resouresReferences: scnSRRefCollection
├── sceneGraph: scnSceneGraph
├── sceneSolutionHash: scnSceneSolutionHash
└── debugSymbols: scnDebugSymbols
```

`version: 5` is the scene-root version. It is not the outer WolvenKit JSON
format version or the CR2W header's game-version number. Likewise,
`PLATFORM_PC` is the cooking target and `minorQuests` is the category tag; they
do not register or launch the resource.

The serialized property is spelled exactly `resouresReferences`. The missing
second `c` is part of the native schema name. Correcting it to natural English
creates a different, unrecognized property in a hand-edited source.

## Typed stores and collections

Empty typed containers are still part of a sound minimal resource. This
focused WolvenKit-shaped excerpt shows the decisive types:

```json
{
  "locStore": {
    "$type": "scnlocLocStoreEmbedded",
    "vdEntries": [],
    "vpEntries": []
  },
  "resouresReferences": {
    "$type": "scnSRRefCollection",
    "lipsyncAnimSets": [
      {
        "$type": "scnLipsyncAnimSetSRRef",
        "asyncRefLipsyncAnimSet": {
          "DepotPath": "base\\animations\\facial\\generic\\interactive_scene\\generic_facial_lipsync_gestures.anims"
        }
      }
    ],
    "cinematicAnimNames": [],
    "cinematicAnimSets": [],
    "dynamicAnimNames": [],
    "dynamicAnimSets": [],
    "gameplayAnimNames": [],
    "gameplayAnimSets": [],
    "ridAnimations": []
  }
}
```

The full `scnSRRefCollection` in this checkpoint also retains typed empty
arrays for RID animation containers, animation sets, camera animations,
cyberware animation sets, deformation animation sets, and facial animation
sets. The root keeps empty `ridResources`, effects, props, markers, notable
points, reference points, VO-info, and workspot arrays. These values describe
the intentionally small scope; they are not invitations to delete the owning
properties indiscriminately.

The spoken line is externally localized, so `scnlocLocStoreEmbedded` remains
empty. That store becomes relevant for scene choices, not for the subtitle and
voice path taught here. See [Localization paths](../journal/localization-paths.md).

## Solution and debug data

The checkpoint retains the nested solution-hash types:

```text
sceneSolutionHash: scnSceneSolutionHash
└── sceneSolutionHash: scnSceneSolutionHashHash
    └── sceneSolutionHashDate: <unsigned value>
```

Treat `sceneSolutionHashDate` as scene metadata that must survive the authoring
and round-trip workflow. Do not use it as a screenplay, event, or content
identity, and do not claim that matching it proves runtime behavior.

`scnDebugSymbols` is also structured data. First Contact supplies two
`performersDebugSymbols` rows and explicit empty arrays for:

- `sceneEventsDebugSymbols`;
- `sceneNodesDebugSymbols`;
- `workspotsDebugSymbols`.

Debug rows do not acquire actors or connect graph nodes. They map editor-facing
performer information onto the native scene identities explained in [Actors
and performers](actors-and-performers.md).

## Default interruption scenario

First Contact includes one `scnInterruptionScenario`, not an omitted or null
policy:

| Property | Exact checkpoint value |
| --- | --- |
| `id` | `scnInterruptionScenarioId` `0` |
| `name` | `Default` |
| `enabled` | `1` |
| Interrupt condition | `scnCheckSpeakersDistanceInterruptCondition`; comparison `Greater`; distance `6` |
| Return condition | `scnCheckSpeakersDistanceReturnCondition`; comparison `Less`; distance `5` |
| `playInterruptLine` | `1` |
| `talkOnReturn` | `1` |
| `forcePlayReturnLine` | `0` |
| `playingLinesBehavior` | `Default` |

The unequal thresholds create a one-unit hysteresis band: the distance must
rise above 6 to interrupt and fall below 5 to return. Do not rewrite them as a
single equality test. The scenario's interrupt/return line policy is scene
behavior; it does not set a completion fact, choose the `contact_done` exit, or
deactivate a community. Those are separate handoff and cleanup operations.

The scenario shape and distance-condition families are **Observed in
vanilla**. The exact First Contact serialization is **Structurally validated**.
The supplied Lab 5 tests do not interrupt an active line or exercise
`CutDestination`. If your scene supports those paths, add explicit walk-out,
return, and reload cases rather than inferring their behavior from normal
playback.

## What to preserve in a focused comparison

When comparing a WolvenKit round trip, review semantic structure rather than
incidental handle allocation:

1. confirm the root type, `version`, platform, and category;
2. confirm every typed store and collection still has its native `$type`;
3. compare actor, performer, graph-node, entry, exit, screenplay, event, and
   locstring IDs in their own domains;
4. compare the lipsync array length with every actor's referenced slot;
5. compare both interruption conditions and their thresholds;
6. compare graph edges, output and input stamps, `startNodes`, and `endNodes`;
7. confirm the solution-hash and debug-symbol containers remain present.

A successful comparison is **Structurally validated** evidence. It does not
show that the marker resolves, the contact is ready, subtitles merge, audio
plays, or the exit returns to the questphase.

Previous: [Scenes](index.md). Next: [Actors and
performers](actors-and-performers.md).
