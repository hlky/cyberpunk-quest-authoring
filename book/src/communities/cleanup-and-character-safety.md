# Cleanup and character safety

Community cleanup is a quest-owned lifecycle transition, not the last line of
a scene. Preserve the actor until the scene has exited, its outcome has been
consumed, the relevant journal or branch state has advanced, and V has left a
generous cleanup area:

```text
scene named exit
  -> consume outcome in questphase
  -> advance outcome-specific journal or branch state
  -> wait until V exits cleanup area
  -> questSpawnManager Deactivate
  -> complete cleanup branch
  -> write terminal one-shot state where the owning phase requires it
```

This ordering protects the scene, AI, and workspot from losing their actor
while they may still own it. It also gives reload tests an explicit durable
state to resume from.

## `Deactivate` is a command, not a disappearance proof

Cleanup uses the same Spawn Manager family as activation:

```text
questSpawnManagerNodeDefinition
  actions[]
    questSpawnManagerNodeActionEntry
      type -> questCommunityTemplate_NodeType
        action: Deactivate
        spawnerReference: NodeRef
        communityEntryName: CName
        communityEntryPhaseName: CName
```

The action scope matters just as it does for `Activate`. A whole-community
deactivation intentionally uses the broad `None` / `None` scope seen in the
inspected pattern; a targeted action must name the exact entry and phase
contract expected by that resource.

The Spawn Manager's outgoing edge establishes graph progression after issuing
the command. It does not prove that the actor vanished during the same frame.
Streaming, AI, scene, combat, workspot, and engine lifecycle rules can affect
when the actor is released. Runtime acceptance must observe both the graph
outcome and the world result.

## Delay cleanup past every active owner

Do not deactivate while any of these can still be true:

- the scene has not reached a named exit;
- a screenplay or section event still references the performer;
- AI or a workspot still owns the actor for immediate presentation;
- combat is active or the actor is reacting to damage;
- the player remains close enough to watch or interact with the actor;
- durable quest/journal progression has not been written;
- a reload could resume before the cleanup branch knows which outcome won.

A simple safe pattern is an outer cleanup trigger whose `Exited` edge becomes
eligible only after the named scene outcome and progression writes. Choose the
volume from measured routes and sight lines. It should be generous enough that
normal departures release presentation ownership before the deactivation
request, but not so broad that the cleanup branch never runs during a typical
playthrough.

Do not use a timer alone as proof of safety. A player can pause, enter combat,
save/reload, or remain beside the actor longer than the assumed duration. A
spatial exit combined with explicit quest state describes the actual
requirement more clearly.

## Advance the outcome before cleanup; finish terminal state afterward

The community is presentation/runtime state. Journal and branch state make the
scene outcome explicit before cleanup, while the owning parent can reserve its
terminal one-shot fact until cleanup has completed.

For every scene outcome:

1. route the named scene output into the questphase;
2. write any outcome or choice fact the branch actually owns;
3. advance or close the applicable journal objective so cleanup does not erase
   the only visible result;
4. converge only branches that have equivalent cleanup requirements;
5. wait for the safe spatial exit;
6. issue the intended `Deactivate` action;
7. complete the child/root branch according to its explicit output contract;
8. write the terminal completion fact at the point defined by that owner.

If cleanup runs before the outcome-specific state, a save can retain an absent
actor without retaining the progression needed to resume the encounter. Do
not infer that every fact must therefore precede cleanup. In exact `cqa005`,
the scene output succeeds the meet objective, retires the pin, and activates
the leave objective before the outer wait; deactivation and leave success then
return the child, and the root writes `cqa005_completed` afterward. That order
is the candidate's explicit ownership contract.

Community activation, scenes, facts, journal entries, and persistent actor
state are save-backed surfaces. Use a clean pre-activation save after changing
their identities or topology. See [Persistent state](../foundations/persistent-state.md)
and [Quest state](../journal/quest-state.md).

## Do not borrow a unique story character

A story-unique character record may already be owned by vanilla quest logic,
availability facts, appearances, phone/scene systems, or persistent save state.
Reusing it for a convenient contact can create conflicts that a clean CR2W
round trip cannot reveal:

- the character may be unavailable, dead, hidden, or in another phase;
- a vanilla scene may acquire or reposition the same identity;
- save state may retain an appearance or attitude inappropriate for the mod;
- deactivating the mod community can interfere with another lifecycle owner;
- a test save can make the character appear reliable when a different save
  legitimately cannot provide it.

The [retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
used `Character.Judy` to isolate a failing scene/community path. That bounded
result is **Runtime-proven** for the legacy fixture only. It is evidence that
the tested lifecycle once completed; it is not a recommendation to author new
content around Judy or any other unique story character.

## Bounded generic-character starting point

For the Lab 5 stationary contact, use this pair as the evidence-backed
starting point:

```text
Character record:
  Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa

Workspot resource:
  base\workspots\common\ground\generic__stand_ground_cigarette__smoke__01.workspot
```

Why this pair is preferred:

- the character is a generic Tyger Claw record, reducing unique-story
  ownership risk;
- the extracted vanilla community at
  `base\open_world\minor_activities\westbrook\japantown\ma_wbr_jpn_13\community\ma_wbr_jpn_013_claws_com.community`
  supplies **Observed in vanilla** evidence for the record's use in a native
  community entry;
- the [retained candidate files](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
  bind that entry, its spot identity, and the cigarette workspot, and the
  legacy fixture spawned all three configured guards. The spawn result is
  **Runtime-proven** only for that hash-bound fixture and placement.

This is not a promise that the actor will stand safely at a new transform,
provide an appropriate voice, remain passive, acquire into a new scene, or
clean up correctly. Lab 5 tests ordinary passivity, acquisition, and cleanup
for its supplied contact. Voice casting, workspot and facial-animation quality,
combat, and interruption need their own checks.

## How to verify workspot mappings

When retained sources disagree, prefer evidence bound to the installed runtime
artifact:

```text
hash-bound archive bytes + runtime observation
  > byte-identical extracted/serialized resource joins
  > synchronized source at the tested commit
  > later or squashed source snapshot
  > array order, debug-name proximity, or memory
```

The [retained archive](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
and its typed entry-to-spot joins support the cigarette workspot above. A later
source-only snapshot named a different
standing workspot, but it is not byte-bound to that runtime archive and does
not supersede the archive-bound mapping.

The later
`base\workspots\common\ground\generic__stand_ground__guard__02.workspot`
appears in a different source/runtime lineage; it is not the retained
stationary-contact mapping. Separate
`base\workspots\patrolling\guard_stand.workspot` evidence belongs to a
finite-patrol candidate and is not a universal guard workspot. Always follow
the typed entry name -> registry `spotNodeRefs` -> area `spotNodeIds` ->
concrete `worldAISpotNode` resource path, rather than pairing nearby
serialized arrays or debug strings.

## Interruption and combat policy

A community-backed contact needs an authored answer for interruption. At
minimum, decide what happens if V attacks, draws police or gang combat into the
area, leaves during the scene, or reloads while the actor is active.

Do not make "deactivate immediately" the generic interruption response. An
actor disappearing during combat or while scene code holds a performer can be
more damaging than leaving the actor present until a safe terminal edge.
Instead, route interruption to a named scene/quest outcome where possible,
write durable state, release scene ownership, then reuse the delayed cleanup
branch.

The generic record already carries gameplay and faction behavior. It is not a
neutral dialogue mannequin. Attitude, combat target, voice, facial animation,
appearance, and invulnerability are separate authoring decisions requiring
their own evidence and acceptance tests.

## Clean-save acceptance matrix

Use a clean save made before the community was ever activated for the first
identity/topology test. Then cover all lifecycle boundaries:

This design matrix is broader than the supplied Lab 5 cases. The generic
pre-scene row below means any arbitrary or unlisted active-child save point;
active-scene reload, alternate outcomes, interruption, and combat require
additional testing if your quest uses them.

| Starting point | Action | Required observation |
| --- | --- | --- |
| Clean pre-activation save | Approach, complete normal outcome, leave cleanup area | Actor remains through named scene exit; progression writes; cleanup issues once |
| Clean pre-activation save | Approach, choose every alternate outcome, leave | Each branch records its own durable result before shared cleanup |
| Named `seed-pre-scene-outside-setup` (Cases 3/4/7) | Load a distinct byte-identical clone, then follow the frozen case route | Exact readiness/acquisition state resumes without a duplicate actor; the named case completes as specified |
| Arbitrary/unlisted active actor before scene | Save/load at another point, then enter broad setup area | Supplemental: readiness/acquisition resumes without duplicate actor or scene |
| During scene at a supported save point | Save/reload and finish | Performer remains coherent; named outcome still reaches progression |
| Named `seed-post-contact-inside-cleanup` (Cases 5/6/8) | Load a distinct byte-identical clone, then follow the frozen case route | Progression is retained and delayed deactivation occurs once |
| Named `seed-completed` (Cases 9/11) | Load a distinct byte-identical clone under the case-specific installation | Scene does not restart and no stale contact reactivates |
| Active contact | Trigger intended interruption/combat cases | No mid-owner disappearance, deadlock, duplicate actor, or lost outcome |

For each run, record the installed archive hash, starting save, route, chosen
outcome, first/last visible actor state, journal/fact state, and behavior after
reload and revisit. A later run against a different archive cannot silently
inherit the earlier result.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Actor disappears before the scene finishes | Deactivate edge, named-exit routing, workspot/AI ownership, and cleanup trigger polarity |
| Actor remains forever after completion | Whether the cleanup-area `Exited` edge was armed, action scope/reference, and saved branch state |
| Scene restarts although the actor was removed | Durable completion fact/journal gate and setup/start path |
| Different saves produce different actor availability | Unique-character ownership, old community activation, scene state, death/appearance state, and starting-save provenance |
| Actor spawns but behaves like a hostile gang member | Character record packages, faction/attitude logic, AI commands, and interruption policy |
| Workspot evidence appears contradictory | Installed archive hash, typed spot joins, source-to-binary synchronization, and whether the candidate was stationary or patrolling |

Return to [Communities and characters](index.md).
