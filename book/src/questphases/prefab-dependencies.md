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

For the book's mod-owned examples, the conservative authoring convention is:

> Declare a quest-prefab root on the root questphase that activates the
> world-aware flow. When an independently registered external child directly
> uses the same root, duplicate the declaration only as an explicit
> compatibility choice and test that exact arrangement.

This is a supported convention for the examples, not a universal native
ownership law. A retained vanilla external child directly uses trigger
NodeRefs while its own root `phasePrefabs` is empty; its parent root declares
the prefab. That is **Observed in vanilla**, but the inheritance and activation
lifetime responsible for it have not been isolated.

**Structurally validated:** Lab 1 has `phasePrefabs: []` because its
questphase has no NodeRef. Its journal resource contains default zero-valued
world fields, but the executable graph does not address a world object.

## External-child dependency boundary

An external child is a separate `questQuestPhaseResource` with its own
`phasePrefabs` list. Inspected resources show more than one arrangement:

- a mod-owned research shape duplicates a directly used root on parent and
  child;
- a retained vanilla street-story root declares the prefab while its external
  open-world child has empty root `phasePrefabs` and still uses nested trigger
  NodeRefs;
- the inspected phase nodes in that vanilla pair have empty
  `phaseInstancePrefabs`.

These observations disprove mandatory child duplication, but they do not prove
a general transitive-inheritance rule. Treat both omission and duplication as
lifecycle-sensitive until the exact root/child activation shape is tested.

```text
root.questphase
  phasePrefabs includes #quest_pr_root
  invokes child.questphase

child.questphase
  directly uses #quest_pr_root/...
  phasePrefabs may be empty or may duplicate the root in inspected shapes
```

When using duplication as the book's conservative mod convention, record it
as a deliberate tested choice. Do not copy every child dependency into every
ancestor without understanding which phase activates the world-aware flow.

## Phase-instance dependencies

`questPhaseNodeDefinition.phaseInstancePrefabs` is a second dependency
location associated with the phase-node activation shape, including inspected
inline-phase patterns. It is not interchangeable with the child resource's
root `phasePrefabs`.

The inspected external-child examples keep `phaseInstancePrefabs: []`, but
their root-level declarations differ as described above. Treat any claimed
relationship among root `phasePrefabs`, node `phaseInstancePrefabs`, and
external-child lifetime as **Experimental** until that arrangement is isolated.

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
2. Group local `#...` references by the root that gives them context.
3. Inventory root `phasePrefabs` and node `phaseInstancePrefabs` without
   assuming either collection automatically owns every direct use.
4. Confirm the world-side resources bind the intended root and register each
   child.
5. Inspect each external child independently and record whether its root
   declaration is present, duplicated, or omitted.
6. Choose a deliberate arrangement, keep it stable for the candidate, and do
   not infer transitive inheritance from one successful lookup.
7. Test activation, unload/reload, and cleanup from a controlled save.

World-aware examples must retain depot paths and hashes for the mod-owned
resources. Vanilla comparisons should cite paths and teach extraction; they
must not redistribute extracted CR2W files.
