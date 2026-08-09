# Root and child questphases

A root questphase is registered beneath the game's quest root. An external
child questphase is a separate archived resource invoked by a node in another
phase. They use the same CR2W resource type, but registration, ownership, and
interfaces differ.

## Root registration

ArchiveXL attaches a mod-owned root:

```yaml
quest:
  phases:
  - path: mod\cqa\cqa001\phases\cqa001.questphase
    parent: base\quest\cyberpunk2077.quest
```

The registration makes the resource reachable from the game's root quest
structure. It does not create journal or localization entries; those remain
separate registrations.

Register only the root phase. An external child must be present at its depot
path in the packed archive, but it is reached through the parent node's
`phaseResource`; it is not a second ArchiveXL root registration. Registering
every child beneath `base\quest\cyberpunk2077.quest` changes the composition
instead of satisfying the reference.

Lab 1 is a single root phase. Its input reaches the one-shot guard without a
location gate, so it can activate independently of player position. Lab 4
keeps one registered root and resolves its boundary activity as an external
child.

## Child-phase interface

A parent uses `questPhaseNodeDefinition` to refer to another questphase through
its soft `phaseResource`. Lab 4 uses this returning-child interface:

```text
parent questPhaseNodeDefinition
    phaseResource: mod\cqa\...\child.questphase
    input socket:  In1
    output socket: Out1

child questphase
    questInputNodeDefinition.socketName:  In1
    questOutputNodeDefinition.socketName: Out1
```

Socket names form the contract for this arrangement. The parent's `In1` maps
to the child's exposed input, and the child's `Out1` maps back to the parent
node's output.

The path and the socket contract solve different problems. A returning child
cannot hand control back through `Out1` when that socket is absent, misspelled,
or unconnected. Matching sockets cannot rescue a missing archived child
resource. This is not a rule that every external phase needs an output:
**Observed in vanilla**, the focused `sts_wat_nid_03` root also contains an
input-only external phase node. Its absence of `Out1` is a different lifecycle,
not an inherently defective resource.

Named outputs can represent distinct results, especially for scenes and later
branching phases. An output named `accepted` is not interchangeable with
`failed` merely because both terminate the child.

## Why create a child phase?

Use a child when it creates a meaningful ownership boundary:

- a reusable or independently testable activity;
- a lifecycle with its own setup and cleanup;
- a graph large enough to obscure the parent orchestration;
- a resource that owns specific world-prefab dependencies;
- a stage with named outcomes the parent must consume.

Do not create a child merely to hide one unexplained node. The book explains
the child's complete graph and every required external resource.

## Parent and child responsibilities

A useful split looks like:

```text
root
  -> decide whether the quest should run
  -> activate top-level journal state
  -> run child activity
  -> consume child outcome
  -> complete or choose the next child

child activity
  -> acquire or activate its dependencies
  -> wait for readiness
  -> perform the focused work
  -> clean up what it owns
  -> emit a named result
```

The parent should not assume that starting a child automatically creates its
community, scene, journal entries, or world objects. The child can coordinate
those resources only after they have been authored and registered.

Registration here means registration appropriate to the resource: the quest
root, journal tree, localization tables, and streaming block have their own
merge points. An external child questphase itself is archived and referenced
by `phaseResource`, not independently merged into the game quest root.

## Inline and external phases

A phase node can point to an external `phaseResource`; CR2W also has structures
for inline/inplace phase graphs. This book starts with external mod-owned
resources because their depot paths, ownership, downloads, and round-trip
inspection are explicit.

Do not generalize an inline vanilla shape into a reader template until its
inheritance, prefab, and save behavior have been isolated.

## Prefab dependencies

World-aware phases can declare quest-prefab dependencies:

- root `phasePrefabs` declares prefab roots owned by that phase composition;
  the usable scope can include external children invoked beneath the root;
- a phase node has a separate, node-local `phaseInstancePrefabs` array. Its
  presence is not evidence that a tool must duplicate the root declaration
  there.

**Runtime-proven:** in the retained GQT003 candidate, the root declared one
prefab while four external children declared `phasePrefabs: []`; the complete
recorded sequence used that root-owned scope successfully. This is bounded
evidence for that arrangement, not a claim that every prefab survives every
possible child, cut, stream, or save transition.

**Observed in vanilla:**
`base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03.questphase`
declares a prefab while its external
`sts_wat_nid_03_openworld.questphase` child has an empty declaration and uses
references beneath that prefab. The observation supports root-owned scope; it
does not replace a mod-owned runtime test.

Lab 4 uses the same explicit model: the root declares
`#cqa004_pr_handoff`, the child declares no prefab, and the parent phase node
does not duplicate the dependency in `phaseInstancePrefabs`. That exact
`cqa004` lifetime and save behavior remains **Experimental** until its
hash-bound runtime matrix passes.

Do not turn an authoring tool's convenience switch into an engine rule.
Research tooling may expose an `inherit_phase_prefabs` policy that copies or
propagates declarations while producing test resources. That remains tool
policy, not proof that native CR2W requires the copy. Inspect the emitted
`phasePrefabs`, `phaseInstancePrefabs`, and `phaseResource` values and validate
the resulting game-resource arrangement.

Lab 1 has empty prefab arrays because it contains no NodeRef. Lab 3 keeps its
reach/leave world activity in one root. Lab 4 moves that activity pattern into
an external child so the root-owned prefab scope and handoff are visible in a
small graph.

## Completion handoff

Completing the last internal action does not automatically advance the parent.
The child must reach its output, and the parent node's matching output must have
an outgoing connection.

Review both sides:

1. Does every intended child route reach an output?
2. Do the output names match the parent phase node?
3. Does every parent output lead somewhere intentional?
4. Do cut or failure routes clean up before handoff?

An orphaned `Out1` is a graph defect even when the child looks complete in
isolation.

`CutDestination` sockets are structurally present on the focused external
phase-node shape, but that does not establish their runtime interruption
semantics. Lab 4 deliberately leaves them unconnected and labels cut behavior
**Experimental** rather than inventing a safe cleanup recipe.

The [Questphases section](../questphases/index.md) continues with the exact
resource anatomy, interface properties, external-child fields, prefab
dependencies, and interruption review. [Lab 4: Handoff
Point](../questphases/lab-04.md) applies the model to downloadable start and
completed checkpoints.
