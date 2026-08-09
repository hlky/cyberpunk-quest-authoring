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
7. [Lab 4: Handoff Point](lab-04.md) moves Lab 3's world activity into an
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

## Evidence boundary

**Lab 1 runtime evidence:** **Experimental** — pending.

**Lab 4 runtime evidence:** **Experimental** — pending.

| Claim | Evidence class | Scope |
| --- | --- | --- |
| A root-owned prefab can remain usable across external child phases whose own `phasePrefabs` arrays are empty | **Runtime-proven** | The retained GQT003 candidate completed four external children with one root declaration; archive SHA-256 `B082D157978347A126DAACB0A5404AF298B88E549731609D81D5A569CBA81FDF` |
| A vanilla root can declare a prefab while an external child uses nested world refs with an empty `phasePrefabs` array | **Observed in vanilla** | `sts_wat_nid_03.questphase` and `sts_wat_nid_03_openworld.questphase`; extract both from your own game |
| Lab 4's exact root, child, sockets, soft path, prefab lists, resources, and graphs serialize and round-trip | **Structurally validated** | WolvenKit `8.19.0`; see the synchronized lab marker |
| Lab 4 enters, resumes, streams, reloads, and completes as intended | **Experimental** | Pending the complete clean-save, hash-bound runtime matrix |

The retained GQT003 evidence was exported with WolvenKit `8.17.4`, WKit JSON
`0.0.9`, and `GameVersion 2310`, from research commit
`6e959d2149e664432eaff3b7d4905e8b1d342f2f`. It proves that exact native
arrangement and its tested lifecycle. It does not prove that every parent
automatically lends every prefab to every possible child.

Inline phases, non-zero `saveLock`, non-zero unfreezing refs, and wired cut
routes remain outside the beginner contract until isolated evidence supports
them.

Next: [Questphase resource anatomy](anatomy.md).
