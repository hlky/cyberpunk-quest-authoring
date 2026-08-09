# Activation, readiness, and acquisition

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

Community activation, actor readiness, player approach, and scene acquisition
are four separate runtime events. Connecting them in that order prevents the
scene from racing the world streamer:

```text
questSpawnManager Activate
  -> questCharacterSpawned condition
  -> broad setup-area condition
  -> scene start
  -> scnActorDef community acquisition
```

The first node requests a state change. The second observes materialization.
The third gives world and scene setup an approach boundary. The fourth asks an
already-running scene to bind a performer to the available community entry.
None substitutes for another.

## Evidence boundary

**Observed in vanilla:** extract these resources from your own game:

```text
base\quest\minor_quests\mq003\mq003_orbitals.questphase
base\quest\minor_quests\mq003\phases\mq003_homeless.questphase
base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene
```

Together, they show the useful lifecycle division: whole-community activation,
a spawned-character readiness condition, a child activity phase, and scene
actors acquired from named community entries. The scene keeps narrower
awareness and engagement work inside an already-started scene rather than
using the narrowest approach boundary as its launch point.

**Runtime-proven:** legacy fixture only. Archive
`87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D`
completed its phone, travel, approach, dialogue, acceptance, and cache-objective
route after the retained community readiness and scene-acquisition join. That
result proves only the installed historical fixture represented by the hash.
It used a unique story character for isolation and is not current authoring
guidance.

**Structurally validated:** retained resources at commit
`68f311c8f2511aeba679b76a68062ef5e446aaa0` serialize the node and actor fields
described below. The commit is legacy research, not the book's pinned baseline
and not evidence that a regenerated package behaves identically.

**Acceptance-gated:** the exact `cqa005` community action, readiness condition,
broad-setup join, scene acquisition, ordinary route, post-`contact_done`
reload, completed reload, and the exact named pre-scene seed loads in Cases 3,
4, and 7 follow the synchronized marker above. Arbitrary or unlisted
pre-scene active-child states remain **Experimental** independently of that
marker.

## `Activate` requests community state

A questphase uses `questSpawnManagerNodeDefinition`. Its `actions` array can
contain a `questSpawnManagerNodeActionEntry` whose typed payload is
`questCommunityTemplate_NodeType`:

```text
questSpawnManagerNodeDefinition
  actions[]
    questSpawnManagerNodeActionEntry
      type -> questCommunityTemplate_NodeType
        action: Activate
        spawnerReference: NodeRef
        communityEntryName: CName
        communityEntryPhaseName: CName
```

`spawnerReference` must resolve to the intended community source. The two
`CName` fields decide whether the command addresses a named entry/phase or the
broader community operation used by the inspected vanilla pattern.

In serialized data, `None` is a real authored `CName` token. It is not a
missing JSON property, `null`, an empty string, or permission to omit the
field. In the observed `mq003` whole-community action and retained legacy
fixture, the broad form is conventionally described as `Activate None/None`.
A focused action instead supplies the exact community-local entry and phase
names.

Choose scope deliberately:

| Action scope | Use when | Review risk |
| --- | --- | --- |
| Whole community (`None` / `None`) | The lifecycle owner intentionally brings the configured community into its active state | It may activate more entries than the scene needs |
| Named entry and phase | One entry must move to one explicit authored phase | A spelling mismatch can leave the intended actor inactive |

An `Out` edge from the Spawn Manager says the command was issued. It does not
prove the streamed area is present, a spot is available, an entity was
constructed, or a scene can acquire that entity.

## `CharacterSpawned` observes readiness

The focused retained condition shape is:

```text
questPauseConditionNodeDefinition
  condition -> questCharacterCondition
    type -> questCharacterSpawned_ConditionType
      objectRef.reference: NodeRef
      comparisonParams
        comparisonType: Greater
        count: 0
        entireCommunity: 1
```

Read this payload literally. With `Greater`, count `0`, and
`entireCommunity: 1`, the condition asks whether the spawned count evaluated
at community scope is greater than zero. It does not mean "every configured
actor is ready." For a one-entry contact, that distinction is small. For a
three-entry encounter, it is decisive.

The `objectRef.reference` must target the same community intended by the
activation action. Do not substitute the registry node's world-global ID, the
AI spot NodeRef, the entry `CName`, or the character `TweakDBID`. Those belong
to different identity domains.

If a scene requires several specific performers, prove every required actor
instead of treating aggregate `> 0` as enough. Parallel actor- or entry-scoped
spawn waits converging on an explicit `And` rendezvous make that requirement
visible in the graph. This follows from the comparison semantics; it is not a
claim that every vanilla multi-actor scene uses that exact graph. Check a
vanilla resource with the same actor count and lifecycle before treating the
arrangement as a reusable precedent. For the single-entry `cqa005` contact,
the final condition and join follow the synchronized marker above.

## Broad setup is an approach boundary

Readiness answers whether the actor exists. It does not answer whether V has
approached through a useful streaming corridor or whether scene setup has had
time to establish its state.

Use a generous outer trigger as the scene-start boundary after readiness:

```text
Activate issued
  -> spawned readiness true
  -> V enters broad setup area
  -> checkpoint if the phase owns one
  -> start scene at its named input
```

The exact radius is location-specific. It must be supported by measured
approach routes, streaming distance, sight lines, and the scene's intended
staging. A number retained from another location is not evidence for the new
one. See [Triggers and areas](../world/triggers-and-areas.md) for volume and
edge semantics.

Keep narrower mood, awareness, greeting, or interaction gates inside the
already-running scene when that is the intended presentation. If the scene is
launched only after the narrowest gate is true, all earlier setup conditions
may already be satisfied on its first update. That can collapse setup, AI
ownership, and opening dialogue into one startup tick.

The broad setup edge is not another spawn command. It is a sequencing and
streaming boundary between the readiness proof and scene initialization.

## The scene acquires; it does not spawn

A community-backed scene actor uses this focused shape:

```text
scnActorDef
  acquisitionPlan: community
  actorId: scnActorId
  actorName
  communityParams -> scnCommunityParams
    reference: NodeRef
    entryName: CName
```

The fields cross three contracts:

| Field | Contract |
| --- | --- |
| `acquisitionPlan: community` | Tells the scene to bind through the community system rather than spawn/despawn or context lookup |
| `communityParams.reference` | Names the community source the quest activated and waited for |
| `communityParams.entryName` | Selects the community-local entry the performer represents |
| `actorId` | Supplies the scene-local performer identity used by sections and events |
| `actorName` | Supplies scene authoring/debug context; it is not the community join key |

The scene's `entryName` must exactly match the registry template entry and the
compiled area's entry mirror. The reference must resolve in the scene's
NodeRef context to the same community used by the questphase. A character can
be visible in the world while acquisition still fails because either join is
wrong.

Scene acquisition also does not transfer permanent ownership. The quest still
owns activation and cleanup; the scene owns the actor only for the performance
window. Let the scene produce a named outcome before the quest advances to
cleanup. The [Scenes](../scenes/index.md) section owns the screenplay,
performer, entry-point, and exit details.

## Authoring and review procedure

For one community-backed contact:

1. Confirm the registry item and streamed area use the intended community
   identity and that the area can stream on every supported approach.
2. Add a Spawn Manager action using the community source NodeRef and chosen
   whole-community or named-entry scope.
3. Add a separate `CharacterSpawned` pause condition. Inspect the comparison,
   count, `entireCommunity`, and object reference rather than relying on the
   node caption.
4. Route readiness to a broad setup-area condition. Do not duplicate the
   activation action on every approach branch.
5. Start the scene through the exact named input after readiness and setup are
   both satisfied.
6. Set every community-backed `scnActorDef` to `acquisitionPlan: community`
   with the matching community reference and entry `CName`.
7. Route each named scene outcome back into explicit quest progression before
   scheduling cleanup.

For multiple required performers, repeat step 3 at the necessary scope and
join the waits explicitly. Do not infer "all ready" from a single `> 0`
community count.

## Acceptance matrix

Test the complete join in game, not only in WolvenKit:

This authoring matrix is broader than the frozen Lab 5 promotion campaign.
The exact `seed-pre-scene-outside-setup` loads and routes for Cases 3, 4, and 7
inherit the synchronized marker, as does Case 2's separate near-site original
load. Generic fast-travel arrival, arbitrary pre-scene save points or states,
active-line/interruption reload, and alternate named outcomes are supplemental
**Experimental** probes until separately retained evidence proves them.

| Route | Required observation |
| --- | --- |
| Case 1: outside original clone, ordinary approach | Actor materializes before scene acquisition; setup occurs once |
| Case 2: separate `original-near-setup` clone, immediate entry | Spawned readiness still wins the race before setup advances |
| Cases 3/4/7: distinct clones of `seed-pre-scene-outside-setup` | The exact saved child/contact state reacquires; Cases 3/4 start once and Case 7 survives its specified stream-away/return route |
| Case 9: `seed-completed` clone | No duplicate scene start or accidentally reactivated contact |
| Supplemental: generic fast travel, then approach | Same ordering; no start-time acquisition failure |
| Supplemental: arbitrary pre-scene save point, then load | No stale activation or skipped readiness edge; result does not promote the frozen cases |
| Supplemental: complete alternate named outcomes | Each route writes the intended durable progression before cleanup |

Record the installed archive SHA-256, starting save, approach route, game and
tool versions, exact first and last visible behavior, and any crash or log
artifact. A successful CR2W round trip is **Structurally validated**; it is not
a runtime result.

## Common failures

| Symptom | Likely contract failure |
| --- | --- |
| Spawn Manager completes but no actor appears | Activation is only a request; inspect streaming, entry/phase names, area/registry join, spot, and character record |
| Readiness gate opens with only one of several actors present | Aggregate `Greater 0` was mistaken for an all-performers condition |
| Readiness never opens | Wrong reference/scope, inactive entry, unavailable spot, bad area placement, or dirty save |
| Scene starts as V crosses the innermost trigger and immediately misbehaves | Broad setup and narrow engage boundaries were collapsed |
| Actor is visible but scene has no performer | Wrong acquisition plan, community reference, entry name, or scene start context |
| Scene restarts on return | Completion state did not gate the setup/start path |

Next: [Cleanup and character safety](cleanup-and-character-safety.md).
