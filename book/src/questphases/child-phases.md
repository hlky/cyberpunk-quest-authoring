# Calling child phases

A parent invokes an external child questphase with
`questPhaseNodeDefinition`. The node is both a resource reference and the
parent side of the child's interface.

## External child shape

This focused shape is structurally validated in the research fixtures:

```text
questPhaseNodeDefinition
├── id: 10
├── sockets
│   ├── CutDestination
│   ├── In1
│   └── Out1
├── phaseGraph: null
├── phaseInstancePrefabs: []
├── phaseResource:
│   └── mod\...\child.questphase  (Soft)
├── saveLock: 0
└── unfreezingTriggerNodeRef: 0
```

| Property | Supported interpretation |
| --- | --- |
| `phaseResource` | Soft depot reference to the external child resource |
| `phaseGraph` | Inline graph slot; null in this external-child shape |
| `phaseInstancePrefabs` | Prefab activation list on this phase-node instance |
| `saveLock` | Present as `0` in the inspected shape; behavior is not generalized here |
| `unfreezingTriggerNodeRef` | Zero in the inspected shape; advanced behavior is not yet isolated |

Do not copy a non-zero value for the last two fields from a large vanilla
quest without first isolating its save and activation semantics.

## The interface must match

The parent and child are separate CR2W resources:

```text
parent
  questPhaseNodeDefinition
    In1  -> child questInputNodeDefinition.socketName "In1"
    Out1 <- child questOutputNodeDefinition.socketName "Out1"
```

The child still contains ordinary internal sockets:

```text
questInputNodeDefinition
  socketName: In1
  Out -> first child action

last child action
  -> In
questOutputNodeDefinition
  socketName: Out1
  type: Terminating
```

Matching only the file path is insufficient. The parent node, child input, and
child output must agree on the interface names.

## Parent and child ownership

Split at a lifecycle boundary, not an arbitrary node count.

| Parent usually owns | Child usually owns |
| --- | --- |
| Overall progression and ordering | One focused activity |
| Deciding which activity starts | Readiness checks specific to that activity |
| Interpreting the child's outcome | Local objective and presentation changes |
| Cross-activity persistent state | Local world dependencies and cleanup |
| Final quest completion | Returning a named result |

For example, a meeting child can activate its community, wait for readiness,
launch its scene, handle the scene outcome, clean up its local markers, and
return `accepted` or `declined`. The parent decides which later questphase
follows that result.

This is an ownership convention, not a restriction imposed by the file
format. Use it because it makes save, interruption, and cleanup responsibilities
reviewable.

## Handoff sequence

```text
parent reaches phase node In1
  -> external child enters through socketName In1
  -> child performs its internal graph
  -> child reaches terminating output socketName Out1
  -> parent phase node emits Out1
  -> parent continuation runs
```

If the child never reaches an output, the parent does not receive that normal
handoff. If the parent `Out1` is orphaned, the child may finish without
advancing the larger quest.

## External before inline

CR2W supports `phaseGraph` and `inplacePhases`, but this book begins with
external mod-owned child resources because they provide:

- an explicit depot path;
- an independently inspectable graph;
- clear dependency ownership;
- a separate WolvenKit project resource;
- a focused archive and hash record.

Inline phase behavior, inheritance, save behavior, and prefab activation need
their own isolated evidence. A null `phaseGraph` is therefore the documented
external-child shape, not a claim that the field must always be null.

## Validation

Before runtime testing:

1. Confirm the parent `phaseResource.DepotPath` matches the archived child.
2. Confirm the child root type is `questQuestPhaseResource`.
3. Match every parent input and output name to a child interface node.
4. Confirm each intended child route reaches an output.
5. Confirm each returned parent output has a continuation.
6. Review dependencies on the resource that directly uses them.
7. Round-trip parent and child independently.

Then test entry, every outcome, reload while the child is active, and the
intended interruption route. One successful normal handoff does not establish
save or cut safety.
