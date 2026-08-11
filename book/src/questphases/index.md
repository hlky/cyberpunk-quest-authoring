# Questphases

A questphase is an executable quest graph stored as a
`questQuestPhaseResource`. It coordinates progression; it does not replace the
resources that own journal content, localized text, scenes, communities, or
world objects.

This section turns the [root-and-child model](../foundations/phase-composition.md)
into exact native resource contracts:

1. [Resource anatomy](anatomy.md) identifies the CR2W root, graph, nodes,
   sockets, external references, and dependency lists.
2. [Registering a root](root-registration.md) separates ArchiveXL root
   attachment from normal depot-resource resolution.
3. [Inputs and outputs](inputs-and-outputs.md) separates a phase interface from
   the sockets used inside its graph.
4. [Calling child phases](child-phases.md) documents
   `questPhaseNodeDefinition` and the parent/child handoff.
5. [Prefab dependencies](prefab-dependencies.md) explains root-owned prefab
   scope, `phasePrefabs`, and `phaseInstancePrefabs` without inventing a
   universal inheritance rule.
6. [Completion and interruption](completion-and-cut.md) reviews terminating
   outputs, parent continuation, re-entry, and cut obligations.
7. [Complex cleanup, interruption, and
   cancellation](cleanup-interruption-and-cancellation.md) expands those
   obligations into an owner ledger for scenes, communities, AI, devices,
   markers, vehicles, monitors, and durable state.
8. [Lab 4: Handoff Point](lab-04.md) moves Lab 3's world activity into an
   external child and makes the boundary inspectable.

The practical pages target the exact
[first-release version set](../reference/tested-versions.md): Cyberpunk 2077
`2.31a` for Windows (GOG; public patch `2.31`), WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31`.

## What belongs in a questphase?

A questphase owns execution order and orchestration. Its nodes can change a
fact, update a journal entry, wait for a condition, invoke a child phase, or
coordinate another native resource.

The referenced resource remains authoritative:

| Concern | Authoritative owner | Questphase role |
| --- | --- | --- |
| Quest and objective hierarchy | Journal resource | Change entry state through a typed journal path |
| Player-facing text | Localization resource | Trigger the state that presents it |
| Dialogue and cinematic timing | Scene resource | Launch the scene and receive an outcome |
| Community, trigger, or marker | World resource | Refer to it through a NodeRef and manage its lifecycle |
| Durable progression | Save-backed fact or journal state | Read or write it at deliberate boundaries |

That distinction is visible in [Lab 1](../start-here/lab-01.md): the phase
contains no title text and no location. Lab 4 adds an external child, but that
child still does not contain trigger geometry or journal strings. It refers to
the world and journal resources that own them.

## The composition boundary

Lab 4 uses one registered root and one externally resolved child:

```text
ArchiveXL quest.phases
  -> cqa004.questphase                         registered root
       phasePrefabs: [#cqa004_pr_handoff]
       questPhaseNodeDefinition
         phaseResource (Soft)
           -> cqa004_boundary.questphase       archived child, not registered
                phasePrefabs: []
                In1 ... Out1
       Out1 from child -> parent continuation
```

Registration answers how the root becomes reachable. `phaseResource` answers
which child the parent loads. The archive must contain both files at their
exact depot paths, but only the root appears under ArchiveXL `quest.phases`.
