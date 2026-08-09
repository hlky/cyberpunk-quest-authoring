# Root and child questphases

A root questphase is registered beneath the game's quest root. A child
questphase is invoked by a node in another phase. They use the same CR2W
resource type, but their ownership and interfaces differ.

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

Lab 1 is a single root phase. Its input reaches the one-shot guard without a
location gate, so it can activate independently of player position.

## Child-phase interface

A parent uses `questPhaseNodeDefinition` to refer to another questphase through
its `phaseResource`.

```text
parent questPhaseNodeDefinition
    phaseResource: mod\cqa\...\child.questphase
    input socket:  In1
    output socket: Out1

child questphase
    questInputNodeDefinition.socketName:  In1
    questOutputNodeDefinition.socketName: Out1
```

Socket names form the contract. The parent's `In1` must map to an exposed child
input, and the child's `Out1` must map back to the parent node's output.

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

## Inline and external phases

A phase node can point to an external `phaseResource`; CR2W also has structures
for inline/inplace phase graphs. This book starts with external mod-owned
resources because their depot paths, ownership, downloads, and round-trip
inspection are explicit.

Do not generalize an inline vanilla shape into a reader template until its
inheritance, prefab, and save behavior have been isolated.

## Prefab dependencies

World-aware phases can declare quest-prefab dependencies:

- root `phasePrefabs` describes prefab roots used directly by that questphase;
- a phase node's `phaseInstancePrefabs` applies to that phase-node activation
  shape.

**Structurally validated:** a child that declares its own root `phasePrefabs`
does not require the parent phase node to duplicate those entries merely
because it invokes the child. The parent still declares any prefab it uses
directly.

Lab 1 has empty prefab arrays because it contains no NodeRef. Lab 4 will add a
child boundary before world dependencies make that distinction harder to see.

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

The [Questphases section](../questphases/index.md) continues with the exact
resource anatomy, interface properties, external-child fields, prefab
dependencies, and interruption review.
