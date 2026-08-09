# Calling child phases

A parent invokes an external child questphase with
`questPhaseNodeDefinition`. The node is both a depot-resource reference and
the parent side of the child's interface.

## External child shape

Lab 4 uses this exact focused shape:

```text
questPhaseNodeDefinition
├── id: 13
├── sockets
│   ├── CutDestination     unwired
│   ├── In1                parent enters here
│   └── Out1               child returns here
├── phaseGraph: null
├── phaseInstancePrefabs: []
├── phaseResource:
│   ├── DepotPath: mod\cqa\cqa004\phases\cqa004_boundary.questphase
│   └── Flags: Soft
├── saveLock: 0
└── unfreezingTriggerNodeRef: 0
```

| Property | Supported interpretation |
| --- | --- |
| `phaseResource` | Soft depot reference to the external child resource |
| `phaseGraph` | Inline graph slot; null in this external-child shape |
| `phaseInstancePrefabs` | Prefab list on this phase-node instance; empty here |
| `saveLock` | Exact serialized value `0`; broader behavior is not generalized |
| `unfreezingTriggerNodeRef` | Exact zero NodeRef; advanced behavior is not isolated |

Do not copy non-zero values for the final two fields from a large vanilla
quest without isolating their activation and save semantics.

## The child is archived, not independently registered

The root and child are separate CR2W files and both must appear in the packed
archive:

```text
mod\cqa\cqa004\phases\cqa004.questphase
mod\cqa\cqa004\phases\cqa004_boundary.questphase
```

Only the first appears under ArchiveXL `quest.phases`. The second is resolved
when the parent phase node follows `phaseResource`.

This distinction prevents two different ownership models from being
confused:

- **root registration** attaches a new composition root under
  `base\quest\cyberpunk2077.quest`;
- **external resolution** loads a child because an executing parent names its
  depot path.

If the child is missing from the archive, registration of the parent can still
look correct. If the child is separately registered, the files may load while
the intended one-root ownership model has already been changed.

## The interface must match

The parent and child meet at names, not at graph IDs:

```text
parent cqa004.questphase
  [13] questPhaseNodeDefinition
    In1  -> child questInputNodeDefinition.socketName "In1"
    Out1 <- child questOutputNodeDefinition.socketName "Out1"

child cqa004_boundary.questphase
  [0] Input socketName In1
    Out -> reach/leave activity -> In
  [1] Output socketName Out1, type Terminating
```

Matching only the file path is insufficient. The parent node, child input, and
child output must agree on the interface names, and the child route must
actually reach its output.

## Parent and child ownership

Split at a lifecycle boundary, not an arbitrary node count. Lab 4 makes the
division concrete:

| Root parent owns | Boundary child owns |
| --- | --- |
| Completion guard | Reach and leave objective states |
| Quest and phase activation | Checkpoint pin activation/inactivation |
| Root `phasePrefabs` declaration | Direct `#cqa004_tr_reach` and `#cqa004_tr_leave` use |
| Starting the child | Waiting for current inside/outside state |
| Interpreting returned `Out1` | Returning `Out1` after leave succeeds |
| 30-second handoff confirmation | No post-return work |
| Completion fact and final quest state | No final quest completion |

The ownership table is a deliberate design, not a file-format restriction. It
makes the active child interval and the parent-only continuation visible for
save/reload testing.

## Exact handoff sequence

![Handoff Point parent-child contract](../images/lab-04/cqa004.handoff-contract.svg)

```text
parent [12] phase Active
  -> parent [13].In1
     -> child [0] socketName In1
        -> reach objective and pin
        -> IsInside reach
        -> retire pin, succeed reach, activate leave
        -> IsOutside leave
        -> succeed leave
        -> child [1] terminating socketName Out1
     -> parent [13].Out1
  -> parent [14] confirmation objective Active
```

The active confirmation objective is the visible proof that normal child
return reached parent-only work. Thirty realtime seconds later, the parent
succeeds that objective, phase, completion fact, and quest.

If the child never reaches output `1`, parent node `13` never emits its normal
`Out1`. If `13.Out1` is orphaned, the child can finish without advancing the
larger quest. The diagram also keeps `CutDestination` visible but unwired; it
is not a hidden normal-return edge.

## Root-owned prefab scope can cross this boundary

Lab 4's parent root declares `#cqa004_pr_handoff`. The child directly uses
nested trigger NodeRefs while its own `phasePrefabs` and the parent node's
`phaseInstancePrefabs` are empty.

That shape is not based on an assumed compiler inheritance feature:

- an exact mod-owned four-child fixture is **Runtime-proven** with only its
  root declaration;
- a comparable root/child arrangement is **Observed in vanilla**;
- Lab 4's exact resources are **Structurally validated**;
- Lab 4 runtime behavior remains **Experimental** until its matrix passes.

See [Prefab dependencies](prefab-dependencies.md) for the evidence limits.

## External before inline

CR2W supports `phaseGraph` and `inplacePhases`, but this book begins with
external mod-owned child resources because they provide:

- an explicit depot path;
- an independently inspectable graph;
- a clear archive manifest entry;
- a focused parent/child diff;
- separate exact SVGs and structural fingerprints.

`phaseGraph: null` is therefore the documented external-child shape, not a
claim that the field must always be null. Inline phase activation, dependency
scope, save behavior, and interruption need their own isolated evidence.

## Validation

Before runtime testing:

1. Confirm the parent `phaseResource.DepotPath` matches the archived child.
2. Confirm the child is absent from ArchiveXL `quest.phases`.
3. Confirm both roots are `questQuestPhaseResource`.
4. Confirm external parent node `phaseGraph` is null and
   `phaseInstancePrefabs` is empty.
5. Match every parent input and output name to a child interface node.
6. Confirm each intended child route reaches an output.
7. Confirm each returned parent output has a continuation.
8. Inventory root and child prefab declarations separately.
9. Confirm no ordinary edge uses `CutDestination` in the unwired lab.
10. Round-trip parent and child independently.

Then test entry, reload before and during the child, streaming away and back
while it is active, reload after return, and completed re-entry. One normal
handoff does not establish save or cut safety.

Previous: [Inputs and outputs](inputs-and-outputs.md). Next: [Prefab
dependencies](prefab-dependencies.md).
