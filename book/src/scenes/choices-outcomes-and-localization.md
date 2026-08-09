# Choices, outcomes, and scene-local localization

A scene choice joins four independent structures: the visible option in the
screenplay store, its embedded localization payload, an option row on a
`scnChoiceNode`, and one scene-graph output. A quest outcome is a fifth
structure. It becomes durable only when the scene reaches a named exit and the
calling questphase records the result.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Focused vanilla comparison | **Observed in vanilla** |
| New mod-owned choice or multi-exit scene | **Experimental** until its own runtime matrix passes |

> **Clean-save requirement:** scene state, quest checkpoints, journal entries,
> and result facts can survive a rebuild. Keep one untouched save from before
> the scene has ever started. Test each outcome from a closed-game copy of that
> same save, and use a new result-fact namespace when an older candidate may
> already have written state.

This guide teaches the native resource joins. It does not require a scene
generator, manifest, explorer, or custom compiler.

## The five ownership layers

```text
screenplayStore.options[]
  itemId + locstringId
          |
          +-> locStore.vdEntries[] -> vpeIndex -> locStore.vpEntries[]
          |
          `-> scnChoiceNodeOption.screenplayOptionId
                        |
                        v
             choice output socket ordinal
                        |
                        v
              section or branch graph
                        |
                        v
            scnEndNode + named exit point
                        |
                        v
       questSceneNodeDefinition output -> durable fact
```

| Layer | Native owner | What it identifies |
| --- | --- | --- |
| Screenplay option | `scnscreenplayChoiceOption` | One choice item and its `scnlocLocstringId` |
| Choice presentation | `scnChoiceNodeOption` | The choice item shown by one choice node, plus its conditions and interaction styling |
| Localized label | `scnlocLocStoreEmbedded` | Descriptor-to-payload lookup for the option locstring |
| Local branch | `scnChoiceNode.outputSockets` | Which scene node receives the selected option |
| Quest result | `scnExitPoint` and the calling quest scene node | Which named scene route the questphase receives |

The repeated small integers in these layers are not interchangeable. A
`scnscreenplayItemId`, a choice output ordinal, a `scnNodeId`, a
`scnlocLocstringId`, a `scnlocVariantId`, and a quest fact value occupy
different ID domains.

## A focused vanilla choice shape

Extract this scene from your own game installation and inspect choice node
`43`:

`base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene`

The installed Cyberpunk `2.31a` resource contains two options:

| Node `43` row | Screenplay item | Output stamp | First destination |
| --- | ---: | --- | ---: |
| Option `0` | `2` | name `0`, ordinal `0` | node `48` |
| Option `1` | `258` | name `0`, ordinal `1` | node `45` |

After those option outputs, the node retains six unconnected output sockets
with names `1` through `6`, each at ordinal `0`. The same option-count-plus-six
shape appears in the audited `mq003`, `mq007`, and `mq010` choices. This is
**Observed in vanilla** for those resources, not proof that every scene type,
game version, or special interaction must use the same padding.

Each node option points back to `screenplayStore.options`:

```text
scnChoiceNodeOption.screenplayOptionId = 2
    -> scnscreenplayChoiceOption.itemId = 2
    -> scnscreenplayChoiceOption.locstringId.ruid
```

`caption` on `scnChoiceNodeOption` is an editor-facing label in the inspected
resources. It is not the player-visible localization payload. Likewise,
`isSingleChoice` and `gameinteractionsChoiceTypeWrapper.properties` are
separate stored values. Do not derive optionality, progression importance,
color, or repeatability from either field alone. Copy those semantics from the
closest relevant vanilla choice and test the resulting interaction.

## Embedded choice localization

Spoken dialogue and choice labels use different ownership in the scene model:

| Content | Scene field | Text owner |
| --- | --- | --- |
| Spoken line | `screenplayStore.lines[].locstringId` | External subtitle resource; VO is a separate external map/WEM branch |
| Choice label | `screenplayStore.options[].locstringId` | The scene's embedded `scnlocLocStoreEmbedded` |

For one option, the embedded lookup is:

```text
screenplay option locstringId
  -> vdEntries[] row with the same locstringId and requested locale
       variantId
       vpeIndex
  -> vpEntries[vpeIndex]
       matching variantId
       content
```

Every descriptor in the four audited scene exports points at an in-range
payload whose `variantId` matches the descriptor. A descriptor's `vpeIndex` is
an array index, not a locstring ID or CR2W handle.

### Preserve observed ordering without inventing a universal rule

The focused exports at the four depot paths listed below have contiguous
`db_db`, `pl_pl`, and `en_us` descriptor blocks. Within each block,
`vdEntries` are sorted by the unsigned numeric value of `locstringId.ruid`.
That arrangement is **Observed in vanilla** in this corpus.

Do not sort decimal IDs as strings: `100` sorts before `20` lexically but
after it numerically. Preserve every value as an unsigned 64-bit number through
comparison and serialization.

Several `db_db` locstrings have two descriptors and two payloads, commonly one
blank and one source-text payload. Their relative payload order differs among
the audited scenes. Therefore:

- keep duplicate descriptors adjacent within their numeric locstring group;
- preserve the descriptor, `variantId`, `vpeIndex`, and payload relationship
  from the evidence-matched source shape;
- do not declare either blank-first or text-first a universal engine rule;
- do not replace the `db_db` block with `en_us` merely because the displayed
  language is English.

The exact required locale set for a newly authored scene, localization
fallback rules, and behavior with a missing descriptor remain
**Experimental** until tested in that package.

## Route a choice to a quest outcome

There are two useful scene designs:

```text
local conversation branch
Choice -> reply A --+
       -> reply B --+-> shared section -> one named exit

quest-significant branch
Choice -> accept section -> End A [accept]
       -> refuse section -> End B [refuse]
```

The first keeps narrative variation inside the scene. The second exposes a
result to the quest. For the second design, all of these names and IDs must
agree:

1. each option socket reaches the intended branch;
2. each branch reaches its own `scnEndNode`;
3. every End is present in `sceneGraph.endNodes`;
4. `exitPoints` maps a stable CName such as `accept` or `refuse` to that End;
5. the calling `questSceneNodeDefinition` has an output socket with the exact
   same name;
6. each quest output immediately writes the intended durable result fact;
7. shared continuation converges only after branch-owned effects are done.

A caption, locstring RUID, or option ordinal is not a quest output name. Do
not make a later phase rediscover the result from presentation state. See
[Branching, choices, and debriefs](../patterns/branching-choices-and-debriefs.md)
for fact and convergence design.

The single named-exit handoff in Lab 5 is **Structurally validated**. A retained
legacy archive with SHA-256
`1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC`
displayed its five intended meeting-choice labels and continued through its
recorded acceptance route; that bounded result is **Runtime-proven**. It does
not prove a general two-exit scene, every option, locale fallback, or behavior
after interruption.

## Manual WolvenKit authoring procedure

No downloadable choice checkpoint is claimed by this page. Use the Lab 5
project only as a **Structurally validated** v5 scene/quest handoff starting
point;
the added choice remains a new **Experimental** candidate.

1. In WolvenKit `8.19.0`, extract one evidence-matched vanilla `.scene` for
   inspection. Do not add the extracted resource to your mod or redistribute
   its complete CR2W or serialized export.
2. In a mod-owned v5 scene, allocate unique `scnscreenplayItemId` values for
   the options. The audited ordinary option pattern is `2 + 256n`; treat that
   as **Observed in vanilla**, not an unchecked license to collide with
   existing items.
3. Add one `scnscreenplayChoiceOption` per visible option. Set `itemId`, a full
   unsigned `locstringId.ruid`, and its usage fields deliberately.
4. Add the matching `scnChoiceNodeOption` rows. Match each
   `screenplayOptionId` to one screenplay option and copy the remaining option
   semantics from the closest compatible vanilla case.
5. Add one output stamped name `0` and ordinal `0..n-1` for each option. Add
   the six observed padding sockets only when the chosen compatible shape uses
   them. Connect every option output; leave padding sockets as the comparison
   does.
6. Populate `locStore.vdEntries` and `vpEntries`. Preserve typed IDs,
   locale-block structure, unsigned numeric ordering, duplicate descriptor
   relationships, `vpeIndex`, and matching payload `variantId` values.
7. Build each branch as ordinary scene nodes and sections. Decide whether it
   rejoins locally or reaches a distinct End and named exit.
8. If the quest consumes several exits, add exact matching output sockets to
   its `questSceneNodeDefinition` and write one durable result on each route.
9. Save, close, and reopen the scene. Convert it to focused CR2W JSON and
   inspect item joins, descriptor/payload joins, output stamps, graph edges,
   `endNodes`, and named exits. A clean WolvenKit round trip is
   **Structurally validated** evidence only.
10. Pack the normal WolvenKit project and inspect ArchiveXL/game logs before
    running the clean-save matrix.

Do not paste an entire choice node from an unrelated scene and leave its actor,
conditions, mappin, reminder, persistent-line, timing, or attachment data in
place. Those fields are part of the interaction contract even when they are
not visible in a graph diagram.

## Acceptance and lifecycle matrix

| Case | Required observation |
| --- | --- |
| Every option from the untouched pre-scene save | Correct label, branch, spoken response, named exit, and result fact |
| Optional branch then progression choice | Optional branch does not consume or duplicate the required progression choice |
| Save before the choice appears | Reload presents one coherent choice group and no stale label |
| Save after selection, before named exit | Reload resumes the selected branch without reopening another branch |
| Save immediately after named exit | Quest writes exactly one result and does not launch the scene again |
| Interrupt before selection | Return behavior is coherent and no result is written |
| Interrupt after selection | Branch and return behavior match the declared design; no other outcome fires |
| Missing-locale negative control | Deliberately recorded fallback behavior; never inferred from the editor caption |
| Completed-save reload | Choice, scene, reward, and branch-only effects do not repeat |
| Mod removal from a disposable save | No claim of cleanup unless active scene, quest, fact, and journal state are explicitly observed |

Active-scene saving may be restricted by the game. Record the nearest available
checkpoint instead of calling an unexecuted save case a pass. Multi-exit
interruption, return, active-branch reload, and localization fallback remain
**Experimental** until the exact candidate passes these cases.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Option row is present but label is blank | Screenplay option locstring, locale descriptor coverage, `vpeIndex`, descriptor/payload `variantId`, and block order |
| One option shows another option's text | Unsigned numeric sort, duplicate descriptor grouping, stale locStore payload, or an option pointing at the wrong locstring |
| Editor caption is correct but game text is wrong | Embedded locStore; `caption` is not the display source |
| Selecting option B follows branch A | Option array order, output name `0` ordinal, destination node, and stale active-scene save |
| Choice appears but cannot progress | Choice type/conditions, missing output edge, required persistent-line behavior, or a branch section that never ends |
| Scene reaches End but quest stalls | End missing from `endNodes`, missing/wrong `exitPoints` name, or quest scene-node socket mismatch |
| Correct scene branch, wrong later debrief | Durable result was not written immediately after the named output |
| Rebuild still shows old options | Save/checkpoint provenance, active scene state, archive replacement, and whether the game was fully restarted |

## Evidence boundary and research anchors

**Observed in vanilla:** the focused choice, socket, screenplay, and embedded
localization shapes described above were inspected in these installed
Cyberpunk `2.31a` resources:

- `base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene`
- `base\quest\minor_quests\mq003\scenes\mq003_03_orbital_pod.scene`
- `base\quest\minor_quests\mq007\scenes\mq007_01_gun_found.scene`
- `base\quest\minor_quests\mq010\scenes\mq010_02_barry_talk.scene`

Extract them from your own installation and record only focused fields. Do not
publish the extracted resources or complete serialized payloads.

**Structurally validated:** Lab 5 proves a v5 scene, typed empty embedded
locStore, and one named scene exit survive a WolvenKit `8.19.0` round trip. It
does not contain a choice.

**Runtime-proven:** the hash-bound legacy route above proves only its recorded
five labels and acceptance continuation in its recorded environment.

**Experimental:** every newly assembled choice, new embedded payload, general
multi-exit handoff, locale fallback, persistent-line behavior, interruption,
return, active-scene reload, and cleanup behavior remains experimental until
its own evidence record passes.

Previous: [Cleanup and save state](cleanup-and-save-state.md). Next: [External
VO, WEM, and lipsync](external-vo-wem-and-lipsync.md).
