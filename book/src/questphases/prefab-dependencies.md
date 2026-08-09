# Prefab dependencies

Quest-prefab dependencies connect a questphase's NodeRefs to world resources.
They are not required for graphs that never reference the world.

## Root-level dependencies

`questQuestPhaseResource.phasePrefabs` contains
`questQuestPrefabEntry` records:

```text
phasePrefabs:
  - questQuestPrefabEntry
      prefabNodeRef: #cqa..._pr_...
```

The supported ownership rule is:

> A questphase declares each quest-prefab root it uses directly.

“Uses directly” includes nodes in that resource whose journal/mappin, spawn,
scene, trigger, device, or other world behavior resolves a NodeRef beneath the
prefab root.

**Structurally validated:** Lab 1 has `phasePrefabs: []` because its
questphase has no NodeRef. Its journal resource contains default zero-valued
world fields, but the executable graph does not address a world object.

## Child resources own their dependencies

An external child is a separate `questQuestPhaseResource` with its own
`phasePrefabs` list. In the validated research shape:

- the parent lists prefab roots it uses directly;
- the child lists prefab roots it uses directly;
- the parent's `questPhaseNodeDefinition.phaseInstancePrefabs` can remain
  empty when the external child declares its own root dependencies.

Do not infer transitive inheritance. If both parent and child directly address
objects under the same prefab root, both resources declare that root.

```text
parent.questphase
  directly uses #quest_pr_root/... -> parent.phasePrefabs includes root
  invokes child.questphase

child.questphase
  directly uses #quest_pr_root/... -> child.phasePrefabs includes root
```

This duplication reflects direct ownership in two resources; it is not the
same as copying every child dependency into every ancestor.

## Phase-instance dependencies

`questPhaseNodeDefinition.phaseInstancePrefabs` is a second dependency
location associated with the phase-node activation shape, including inspected
inline-phase patterns. It is not interchangeable with the child resource's
root `phasePrefabs`.

The external-child examples used by this book keep
`phaseInstancePrefabs: []` and let each child resource declare what it uses.
Treat other arrangements as **Observed in vanilla** or **Experimental** until
their inline/external lifecycle has been isolated.

## A prefab entry does not create the world

Declaring a prefab root is one link in a longer reference chain. The world
resources must still provide the corresponding quest-prefab binding and child
NodeRefs.

Conceptually:

```text
questphase NodeRef
  -> declared quest prefab root
  -> world-side quest prefab binding
  -> registered child NodeRef
  -> concrete sector node or resource
```

A valid `phasePrefabs` entry cannot repair a misspelled child NodeRef, a
missing sector registration, or an absent world resource. Conversely, a world
object can exist while remaining unreachable from the phase because the
dependency was not declared.

## Review procedure

For each phase resource:

1. Inventory every non-zero NodeRef used by its nodes and payloads.
2. Group relative `#...` references by quest-prefab root.
3. Confirm each directly used root appears in `phasePrefabs`.
4. Confirm the world-side resources bind that root and register each child.
5. Inspect each external child independently.
6. Review `phaseInstancePrefabs` on phase nodes instead of assuming it inherits
   or replaces root dependencies.
7. Test activation and cleanup from a controlled save.

World-aware examples must retain depot paths and hashes for the mod-owned
resources. Vanilla comparisons should cite paths and teach extraction; they
must not redistribute extracted CR2W files.
