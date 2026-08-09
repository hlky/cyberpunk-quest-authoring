# Questphases

A questphase is an executable quest graph stored as a
`questQuestPhaseResource`. It coordinates progression; it does not replace the
resources that own journal content, localized text, scenes, or world objects.

This section turns the [root-and-child model](../foundations/phase-composition.md)
into exact resource contracts:

1. [Resource anatomy](anatomy.md) identifies the CR2W root, graph, nodes,
   sockets, and dependency lists.
2. [Registering a root](root-registration.md) explains how ArchiveXL attaches a
   mod-owned phase to the game's root quest structure.
3. [Inputs and outputs](inputs-and-outputs.md) separates the phase interface
   from the sockets used inside the graph.
4. [Calling child phases](child-phases.md) documents
   `questPhaseNodeDefinition` and the parent/child handoff.
5. [Prefab dependencies](prefab-dependencies.md) explains `phasePrefabs`,
   `phaseInstancePrefabs`, and direct world-reference ownership.
6. [Completion and interruption](completion-and-cut.md) reviews terminating
   outputs, named outcomes, re-entry, and cut obligations.

The exact property shapes and practical procedures target the
[first-release version set](../reference/tested-versions.md): Cyberpunk 2077
2.31a, WolvenKit 8.19.0, ArchiveXL 1.27.0, RED4ext 1.30.0, and redscript
0.5.31.

## What belongs in a questphase?

A questphase owns execution order and orchestration. Its nodes can change a
fact, update a journal entry, wait for a condition, invoke a child phase, or
coordinate another native resource.

The referenced resource remains authoritative:

| Concern | Authoritative owner | Questphase role |
| --- | --- | --- |
| Quest and objective hierarchy | Journal resource | Change entry state through a journal path |
| Player-facing text | Localization resource | Trigger the state that presents it |
| Dialogue and cinematic timing | Scene resource | Launch the scene and receive an outcome |
| Community, trigger, or marker | World resource | Refer to it through a NodeRef and manage its lifecycle |
| Durable progression | Save-backed fact or journal state | Read or write it at deliberate boundaries |

That distinction is visible in [Lab 1](../start-here/lab-01.md): the
questphase contains no title text and no location. It changes a journal
resource and a fact, then terminates.

## Evidence boundary

**Lab 1 runtime evidence:** **Experimental** — pending.

The supplied Lab 1 phase is **Structurally validated** with WolvenKit 8.19.0:
its binary resources deserialize, round-trip, and pack. The dedicated marker
above mirrors the eight-case, hash-bound runtime-acceptance record.

External child phases and prefab ownership are supported by isolated research
fixtures and vanilla comparison, but this section does not promote untested
fields into beginner defaults. In particular, inline phases, `saveLock`, and
unfreezing triggers are named where they appear and left unexplained where
their behavior has not been isolated.
