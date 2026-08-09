# Entry, exit, and quest handoff

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

The scene graph and the questphase graph meet through names, but they remain
different graph systems. First Contact exposes scene entry `start`, exposes
named scene exit `contact_done`, and gives a `questSceneNodeDefinition` sockets
with exactly those names.

## Canonical four-node scene

The completed scene has four scene-node IDs:

```text
                         +-> Section 2 -> End 3 [contact_done]
Start 1 -- one fan-out --+
                         +-> scnQuestNode 4 / PuppetAI [fire-and-forget]
```

Start uses one output socket with two destinations. The section controls the
line's duration and reaches End. The PuppetAI branch has no output destination,
so it is deliberately fire-and-forget and does not join the line branch before
the named exit.

The exact semantic edges and stamps are:

| Source node | Source output stamp | Destination | Destination input stamp |
| --- | --- | --- | --- |
| Start `1` | name `0`, ordinal `0` | Section `2` | name `0`, ordinal `0` |
| Start `1` | name `0`, ordinal `0` | PuppetAI wrapper `4` | name `0`, ordinal `1` |
| Section `2` normal | name `0`, ordinal `0` | End `3` | name `0`, ordinal `0` |
| Section `2` cancel | name `1`, ordinal `0` | no destination | — |
| PuppetAI wrapper `4` | name `0`, ordinal `0` | no destination | — |
| End `3` | no output sockets | — | — |

Do not turn the two Start destinations into two differently stamped outputs.
The fixture has one `0/0` fan-out. Likewise, the PuppetAI destination's
`0/1` is an input stamp, not the wrapper's output stamp.

The graph declares its boundary nodes independently of their appearance in
the `graph` array:

```text
startNodes: [scnNodeId(1)]
endNodes:   [scnNodeId(3)]

entryPoints:
  start -> scnNodeId(1)

exitPoints:
  contact_done -> scnNodeId(3)
```

`startNodes`/`endNodes` identify the graph's boundary nodes. `entryPoints` and
`exitPoints` publish named routes for callers. Preserve both layers; merely
naming an exit does not add End to `endNodes`, and merely listing End does not
publish `contact_done`.

## The scene-local PuppetAI node

Scene node `4` is an `scnQuestNode` wrapper around a
`questPuppetAIManagerNodeDefinition`, also with graph-local ID `4` in this
focused fixture. Its internal quest node has:

| Property | Value |
| --- | --- |
| Entry target | Contact entity reference beneath `#cqa005_com_contact` |
| `aiTier` | `Cinematic` |
| Quest sockets | `CutDestination`, `In`, `Out` |
| Wrapper `isockMappings` | `CutDestination`, `In` |
| Wrapper `osockMappings` | `Out` |
| Wrapper output destinations | none |

The wrapper's input ordinal `1` maps Start's destination to internal socket
`In`; ordinal `0` is the `CutDestination` mapping. This is why changing the
destination stamp from `0/1` to `0/0` is a semantic edit, not cosmetic graph
layout.

The branch requests the contact's `Cinematic` AI tier alongside the spoken
section. It neither ends the scene nor emits a completion signal. The section
branch alone reaches End `3`. Since no join waits for an AI output, treat this
arrangement as fire-and-forget and test teardown separately.

## Questphase scene node contract

The child questphase launches the archived scene through one
`questSceneNodeDefinition`. Its interface is exact:

| Socket | Socket type | First Contact connection |
| --- | --- | --- |
| `CutDestination` | `CutDestination` | Unconnected |
| `start` | `Input` | Connected from the child flow after actor readiness/setup |
| `contact_done` | `Output` | Connected to success-state and cleanup progression |
| `Default INT` | `Output` | Unconnected |
| `Default RET` | `Output` | Unconnected |

There is no output socket named `end`. The successful join is the exact
scene-exit name `contact_done`. Adding a questphase `end` output does not make
it match the scene's End node.

The decisive non-socket properties are:

```text
questSceneNodeDefinition
├── interruptionOperations: []
├── notAllowedToBeFrozen: 0
├── reapplyInterruptionOperationsAfterGameLoad: 0
├── syncToMusic: 0
├── sceneFile:
│   ├── DepotPath: mod\cqa\cqa005\scenes\cqa005_first_contact.scene
│   └── Flags: Soft
└── sceneLocation: scnWorldMarker
    └── nodeRef: #cqa005_sm_contact
```

The soft `sceneFile` is a depot reference to a `.scene` carried in the packed
archive. It is not an ArchiveXL root registration. ArchiveXL registers the
quest root and localization branches in this design; the active questphase
resolves the soft scene resource when execution reaches this node.

`sceneLocation` is a typed `scnWorldMarker`. Its local NodeRef must resolve
beneath the prefab scope available to the active phase composition. A valid
scene path cannot supply a missing marker, and a registered marker cannot
supply a missing scene. See [Quest prefabs and
NodeRefs](../world/quest-prefabs-and-noderefs.md).

Empty `interruptionOperations` and unconnected default interruption/return
outputs are exact boundaries for this small lab. They do not prove that a
larger quest can omit interruption handling, nor that `CutDestination` has
been runtime-validated.

## Start checkpoint boundary

The downloadable start checkpoint keeps a safe scene shell with only:

```text
Start 1 (output 0/0) -> End 3 (input 0/0)
```

It still declares `startNodes[1]`, `endNodes[3]`, entry `start`, and exit
`contact_done`. The root and child start quest graphs must not invoke that
scene node. The shell exists so the learner edits a native resource with its
actor/debug/localization/reference scaffold intact; it is not a playable
pre-completion shortcut.

## Evidence boundary

Comparable Start/Section/End and scene-local quest-node arrangements are
**Observed in vanilla** in the cited minor-quest scenes. The exact four nodes,
stamps, mappings, public entry/exit, scene-node sockets, soft path, and marker
are **Structurally validated** in First Contact. Resolution of
`#cqa005_sm_contact`, the exact `start` launch, `contact_done` return, and the
post-`contact_done` and completed reload paths named by the frozen Lab 5
campaign follow the synchronized marker above, as do the exact named
pre-scene seed loads in Cases 3, 4, and 7. Arbitrary or unlisted pre-scene
active-child states, active-line interruption/return or reload, and
`CutDestination` behavior remain **Experimental** and require separate runtime
records.

Previous: [Screenplay, sections, and
events](screenplay-sections-and-events.md). Next: [Author one spoken
line](one-spoken-line.md).
