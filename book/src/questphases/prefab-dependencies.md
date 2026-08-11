# Prefab dependencies

Quest-prefab dependencies give quest graph NodeRefs a world-side scope. They
are not required for graphs that never reference the world, and their native
lifecycle cannot be reduced to “duplicate every direct use.”

## Root-owned scope

`questQuestPhaseResource.phasePrefabs` contains
`questQuestPrefabEntry` records:

```text
phasePrefabs:
  - questQuestPrefabEntry
      prefabNodeRef: #cqa004_pr_handoff
```

Lab 4 declares that entry on the registered root only:

```text
cqa004.questphase
  phasePrefabs: [#cqa004_pr_handoff]
  invokes cqa004_boundary.questphase

cqa004_boundary.questphase
  phasePrefabs: []
  uses #cqa004_tr_reach and #cqa004_tr_leave
```

The root declaration can own the world scope used by an active external child.
It is therefore too narrow to define `phasePrefabs` as “only roots directly
used by nodes in this file.”

The supported statement is more precise:

> A prefab declared by a composition root can remain available to external
> children in tested native arrangements. The exact root, child, and activation
> lifetime are part of the evidence.

That supports Lab 4's design without claiming universal transitive
inheritance.

## Why the root-only arrangement is supported

### Runtime-proven research fixture

**Runtime-proven:** a retained mod-owned GQT003 candidate completed its full
activity sequence across four external child phases while only its root
declared `#gqt003_pr_extract_and_hold`. Every child's `phasePrefabs` list was
empty.

The exact candidate identity is retained in [Lab status and research
provenance](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence).

The composition used this root and four external child depot resources:

```text
mod\gqt003_extract_and_hold\phases\gqt003_extract_and_hold.questphase
  -> mod\gqt003\phases\gqt003_reach_extraction_relay.questphase
  -> mod\gqt003\phases\gqt003_release_patch.questphase
  -> mod\gqt003\phases\gqt003_escort_patch.questphase
  -> mod\gqt003\phases\gqt003_defend_patch.questphase
```

The retained snapshot used WolvenKit `8.17.4`, WKit JSON `0.0.9`, and
`GameVersion 2310`; treat it as a bounded precedent rather than a current lab.

That run proves root-owned scope remained usable across those four exact
children and stage handoffs. It does not isolate active-child unload/reload or
wired-cut behavior, and it does not turn a generator's dependency policy into
an engine law.

### Vanilla comparison

**Observed in vanilla:** extract these resources from your own game:

```text
base\open_world\street_stories\watson\northside_industrial_district\
  sts_wat_nid_03\phases\sts_wat_nid_03.questphase

base\open_world\street_stories\watson\northside_industrial_district\
  sts_wat_nid_03\phases\sts_wat_nid_03_openworld.questphase
```

The inspected parent declares `#sts_wat_nid_03_streetstory`. Its external
open-world child has `phasePrefabs: []`, while the child graph uses nested refs
under that prefab. The invoking phase node also has
`phaseInstancePrefabs: []`.

This is comparative evidence for the serialized shape. Do not redistribute
the extracted CR2W resources, and do not treat observation alone as a runtime
test of Lab 4.

### Lab 4 candidate

**Structurally validated:** the completed Lab 4 parent contains exactly one
root entry, the child contains zero, and phase node `13` contains zero
instance-prefab entries. Both phase resources cook and round-trip with
WolvenKit `8.19.0`.

**Experimental:** mounting, child-time NodeRef resolution, streaming away and
back, save/reload, and the eventual parent handoff remain pending until every
Lab 4 runtime case passes.

## Tooling policy is not a native field

Some generators expose a policy named `inherit_phase_prefabs` or otherwise
copy declarations into generated children. That option is a tool's authoring
policy. There is no native CR2W property with that name.

Judge the emitted native fields instead:

| Native location | Lab 4 value |
| --- | --- |
| Parent root `phasePrefabs` | `[#cqa004_pr_handoff]` |
| Child root `phasePrefabs` | `[]` |
| Parent phase node `phaseInstancePrefabs` | `[]` |

An earlier GQT004 research diagnosis blamed a failing candidate on a missing
child prefab declaration. Later controlled evidence disproved that theory. Do
not cite that discarded diagnosis as proof that duplication is mandatory.

## Duplication changes the candidate

An external child is a separate `questQuestPhaseResource`, so it can serialize
its own `phasePrefabs` list. Adding the same root there is not a harmless
annotation: it changes the activation arrangement that must be tested.

Use one deliberate shape:

- root-only declaration when evidence and desired lifetime match Lab 4;
- duplicated declaration only when the exact duplicate arrangement has an
  identified lifecycle reason and its own runtime evidence.

Do not copy every child dependency into every ancestor, and do not duplicate a
root merely because the child graph contains a local `#...` NodeRef.

## Phase-instance dependencies are separate

`questPhaseNodeDefinition.phaseInstancePrefabs` is a second native dependency
location associated with the phase-node instance. It is not interchangeable
with either resource root's `phasePrefabs` array.

The focused external-child examples used by this section keep
`phaseInstancePrefabs: []`. Other arrangements, including inline phases, need
separate evidence. Do not infer a universal precedence or fallback order among
the three lists.

## A prefab entry does not create the world

Declaring a prefab root is one link in a longer reference chain. Lab 4 uses:

```text
root phasePrefabs: #cqa004_pr_handoff
  -> world-side full root: $/mod/cqa/cqa004/#cqa004_pr_handoff
     -> Quest sector child refs:
          #cqa004_tr_reach
          #cqa004_tr_leave
     -> AlwaysLoaded sector child ref:
          #cqa004_mp_handoff
```

The streaming block and sectors still have to provide the binding, nodeRefs,
placements, and descriptors. A valid root entry cannot repair a misspelled
child ref, missing sector registration, or absent world resource. Conversely,
a world object can exist while remaining unreachable from the phase.

## Review procedure

For a composed phase tree:

1. Inventory every non-zero NodeRef used by every phase resource.
2. Group local `#...` refs by the full root that gives them context.
3. Inventory each resource root's `phasePrefabs` and each invoking node's
   `phaseInstancePrefabs` separately.
4. Identify the composition root and the intended prefab activation lifetime.
5. Confirm the world-side resources bind the same full root and child refs.
6. Record whether each external child declares, duplicates, or omits the root.
7. Cite runtime evidence for the exact arrangement; do not infer a general
   inheritance rule from one success.
8. Test active-child reload, stream-away/return, normal completion, and cleanup
   from a controlled save.

World-aware examples retain depot paths and hashes for mod-owned resources.
Vanilla comparisons cite paths and teach extraction; they never redistribute
extracted CR2W files.

Previous: [Calling child phases](child-phases.md). Next: [Completion and
interruption](completion-and-cut.md).
