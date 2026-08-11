# Actors, scenes, and lipsync

A scene-launch failure can occur before any subtitle, audio, or visualizer
appears. Diagnose actor readiness, acquisition identity, scene graph entry, and
indexed resource tables in that order.

## Locate the launch boundary

Record the last confirmed event and the first missing event:

```text
community Activate
  -> CharacterSpawned passed
  -> broad setup trigger passed
  -> scene node entered
  -> scene entry resolved
  -> actor acquisition
  -> section/event start
  -> subtitle / WEM
  -> named scene exit
```

If the game crashes before dialogue visualization and the crash follows the
scene launch trigger when that trigger moves, focus on scene initialization.
If bypassing the scene lets the world/community route continue, do not rebuild
the world sector first.

## Actor readiness workflow

For each required actor, compare all identity fields:

| Layer | Community actor | Player actor |
| --- | --- | --- |
| Spawn owner | Active community entry/phase | Existing player context |
| Quest readiness | `CharacterSpawned` condition on the same community target | Usually not a community-spawn gate |
| Scene acquisition | `community` with matching area/entry | `findInContext` with the intended player record |
| Scene actor ID | Actor-table key used by screenplay lines | Separate actor-table key |
| Performer ID | Section/event/debug-symbol performer | Must map to the correct actor |

Then test this order:

1. activate the community;
2. wait for `CharacterSpawned` on the exact community NodeRef/entry scope;
3. enter a broad setup boundary;
4. checkpoint if the tested pattern requires it;
5. start the scene;
6. let narrower scene conditions control approach beats.

A single fan-out that activates the community, waits, and starts the scene
does not enforce that order. Starting only at a narrow engage boundary can
also make several already-true scene conditions cascade in one tick.

Readiness and lipsync are independent. Legacy research repaired a
fast-approach readiness gap, yet a deterministic launch crash remained until
the lipsync table was corrected.

## Audit actor and performer joins

For every spoken line or section:

1. confirm the screenplay item's speaker and addressee are valid actor IDs;
2. confirm the section's actor behavior rows use the intended performer IDs;
3. confirm debug-symbol performer mappings agree with the actor table;
4. confirm a community actor's area NodeRef and entry name match the active
   registry entry exactly;
5. confirm the scene marker exists and the quest scene node uses the correct
   entry point CName;
6. confirm the quest expects an actual named scene exit, not a guessed `end`.

Actor ID, performer ID, screenplay item ID, localization RUID, event ID, and
CR2W handle ID are different domains. A numerically plausible reuse is not a
join.

## Audit lipsync cardinality

For each actor, record `lipsyncAnimSet.id`. Then inspect the cooked scene's
native `resouresReferences.lipsyncAnimSets` array:

```text
actor slot IDs: 0, 1
addressable rows after cooking: 1
result: invalid index 1
```

Require every selected index to be addressable. Two identical depot paths in
the authoring view may collapse to one import; inspect the round trip and
cooked imports, not only the source list.

The safest production correction is to provide the intended distinct, valid
NPC and V resources and prove both rows remain addressable after cooking. A
shared slot can isolate a cardinality fault, but it leaves facial and gesture
quality **Experimental** unless separately accepted.

## Reduce a crashing scene without losing causality

Use staged candidates, one change each:

1. Keep world/community flow and replace the scene invocation with direct
   phase continuation. If that passes, the earlier world path is not the
   immediate crash boundary.
2. Restore scene invocation with Start-to-End only. If it passes, root scene
   loading and entry/exit can work; actor readiness under full dialogue is not
   yet proved.
3. Restore one actor-acquired section without audio/choices.
4. Verify resource-table cardinalities and actor joins.
5. Restore the line and external localization/audio path.
6. Add choices, animation, interruption, and cleanup as separate surfaces.

Hash each candidate and reuse the same eligible starting-save lineage. Do not
call a bypass “fixed”; it only locates a boundary.

## Symptom routing

| Symptom | Inspect first |
| --- | --- |
| Actor never appears | Community registry/entry/phase, AI spot, activation, record/appearance namespace |
| Actor appears but scene waits forever | `CharacterSpawned` target/scope and scene acquisition entry |
| Crash exactly when scene launches | Actor table, performer joins, resource-reference indexes, graph entry |
| Slow approach works, fast approach fails | Readiness/order race and trigger cascade |
| Dialogue plays but actor is invisible | Character root/default appearance and requested community appearance |
| Scene exits immediately | Bypassed section or retained Start-to-End edge |
| Scene never returns to quest | Scene End/named exit and questphase output CName mismatch |
| No subtitle or audio but no crash | Continue with [Journal, localization, and audio](journal-localization-audio.md) |

Previous: [NodeRefs, streaming, and
placement](noderefs-streaming-placement.md). Next: [Journal, localization, and
audio](journal-localization-audio.md).
