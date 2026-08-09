# Complex cleanup, interruption, and cancellation

Complex cleanup is not one final node. It is a protocol among graph routes and
the resources they activated: scenes, communities, AI, workspots, devices,
markers, vehicles, inventory, journal state, and save-backed progress.

Use this chapter when an activity has more than one live owner or more than one
way to end. Its goal is a teardown design in which every outcome records its
meaning, stops or neutralizes outstanding work, releases each resource through
its actual owner, and returns through an explicit phase interface.

```text
success / failure / player cancel / interruption
  -> choose and persist one outcome
  -> stop new state-changing work
  -> let active consumers reach a safe release boundary
  -> retire presentation
  -> run owner-specific teardown
  -> confirm cleanup handoff
  -> write terminal state and terminate the owning route
```

There is no established native "clean up everything" operation. A cut edge,
phase output, scene end, community deactivation, or vehicle command handles
only its own bounded contract.

## Evidence and tested boundary

Practical review on this page targets Cyberpunk 2077 Windows GOG `2.31a`,
WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, and redscript
`0.5.31`.

| Label | Bounded claim |
| --- | --- |
| **Observed in vanilla** | The cited resources expose explicit cut-to-target wiring, delayed community deactivation, scene/quest boundaries, and a player-vehicle operation in their own contexts. These are examples of separate owners, not one reusable teardown graph. |
| **Structurally validated** | The checked labs serialize named scene and child outputs, journal/mappin transitions, spawn-manager actions, completion facts, and unwired `CutDestination` sockets in deliberate order. This proves graph shape, not interrupted runtime recovery. |
| **Runtime-proven** | Retained archive `DE2A28EF7F7D8D20B4FADF3B97BD0B96BB420FED8456AC0D57E9987B00ACFB2A` deactivated surviving actors after one leave-area boundary. Archive `84BA33E902360BC4F1ED32A0865CE8B15C35D9442FD519CC6C3E85A06D1AE77B` completed one exact six-stage vehicle route and its final player-vehicle cleanup. The separate partial results below expose two unsafe handoffs. None represents the pinned practical baseline. |
| **Experimental** | General cut semantics, active-scene cancellation, arbitrary monitor teardown, mixed-owner cleanup, command idempotency, and every newly authored interruption/reload policy remain unproved until their own hash-bound matrix passes. |

Extract these focused comparisons from your own installation rather than
copying their complete resources:

```text
base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase
base\quest\minor_quests\mq003\phases\mq003_homeless.questphase
base\quest\minor_quests\mq003\scenes\mq003_01_homeless.scene
base\quest\side_quests\sq031\phases\sq031_porsche.questphase
base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_03\phases\sts_wat_nid_03_gameplay.questphase
```

## Name the exit before choosing the cleanup

Different endings require different state and sometimes different release
orders:

| Exit class | What produces it | Required durable distinction |
| --- | --- | --- |
| Normal success | Authoritative activity result | Success or branch outcome, written before destructive teardown |
| Authored failure | Death, target loss, timeout, combat state, or explicit failure fact | Failure reason and retry/terminal policy |
| Player cancellation | A supported prompt/UI/workspot/scene exit | Whether the activity remains active, resets, or terminates |
| Scene interruption and return | Scene interruption scenario plus quest wrapper outputs | Interrupted is not completed; return and terminal interruption need separate handling |
| Graph cut | `questCutControlNodeDefinition.CutSource` targeting named `CutDestination` sockets | Which routes are cut, whether the cut is permanent, and which cleanup route now owns them |
| Streaming transition | Player leaves a streamed owner while graph/save state remains active | Reacquire, remain inactive, or fail according to an explicit policy |
| Mod removal or upgrade | Archive changes while save-backed state remains | Migration/removal behavior, never inferred from a clean install |

Do not converge these exits before recording their meaning. If success and
cancel both reach cleanup with no discriminator, a save taken during teardown
cannot know which presentation, retry, or terminal state to restore.

## Build an owner ledger

Before drawing edges, list every resource that may be active and the exact
operation that acquired it:

| Active concern | Acquisition boundary | Release question |
| --- | --- | --- |
| Parallel Pause Condition or delay | Split from a main route | Can a late signal remain harmless, or must a tested cut target it? |
| Journal objective/description/mappin | Journal or Mappin Manager state change | Which terminal state is correct for each outcome? |
| Scene | `questSceneNodeDefinition` input and scene entry | Which named normal, interruption, return, or failure output proves release? |
| Community actor or vehicle | Spawn Manager activation/phase action | Are scene, AI, workspot, combat, carry, or seat owners finished before deactivation? |
| Gameplay AI / follower role | AI manager command | Which later command or owner transfer ends that role safely? |
| Device interaction | Controller eligibility, player prompt, UI/workspot, or quest command | Preserve, restore, disconnect, or leave native state—which is evidenced? |
| World marker/trigger | Sector placement plus quest/journal activation | Retire the pin/presentation; do not mistake streaming for graph cancellation |
| Player-vehicle record | Player-vehicle system operation | Is the exact vehicle record and `questEnablePlayerVehicle_NodeType` context applicable? |
| Placed world vehicle | Sector, prefab, community, or scene | Which of those owners, not a guessed player-vehicle command, releases it? |
| Inventory/reward | Item or reward manager write | Is the write before or after commitment, and can any route repeat it? |
| Durable fact | Facts DB write and save | Does it mean outcome chosen, cleanup started, cleanup finished, or quest terminal? |

Give each row one cleanup owner. Shared responsibility is usually an
unresolved handoff: the scene assumes the quest will retain an actor while the
quest assumes scene End already released it.

## Separate selection, quiescence, release, and finalization

A robust teardown has four boundaries.

### 1. Select one outcome

The winning branch records its outcome before it reaches shared teardown:

```text
success signal -> set activity_outcome = success --+
failure signal -> set activity_outcome = failure --+-> cleanup entry
cancel signal  -> set activity_outcome = cancel  --+
```

Use facts, journal states, or explicit named outputs that the owning design can
read after reload. Do not award, remove an item, or mark the whole quest
complete merely to create a discriminator.

An XOR-shaped convergence is not proof that losing producers were cancelled.
Every late route must either be harmless after the outcome write or be the
target of a separately accepted cut topology.

### 2. Quiesce producers and consumers

Stop new state-changing work before removing the resources it addresses:

- make losing monitor outputs bypass journal, fact, reward, and world writes;
- wait for a scene's intended named outcome rather than assuming section End
  released every performer;
- end or transfer follower, patrol, combat, workspot, carry, and seat roles;
- finish or explicitly interrupt device UI/personal-link/workspot ownership;
- stop spawning new waves before deactivating the encounter;
- decide how an active timer or delay behaves after the outcome is sealed.

Quiescence can be logical rather than destructive. A listener that remains
active but cannot mutate state may be safer than an unproved cut operation.

### 3. Release owner-specific transients

Retire each resource through the system that owns it:

```text
journal/mappin owner  -> outcome-specific state + pin inactive
scene owner           -> named exit / accepted interruption contract
AI/workspot owner     -> explicit handoff or release command
community owner       -> Spawn Manager Deactivate at safe boundary
device owner          -> evidenced final controller/disconnect policy
vehicle owner         -> source-specific deactivation or vehicle-system action
world owner           -> leave placement to streaming unless a resource-specific action exists
```

The order may differ by branch. A failed combat encounter may need to stop
waves before actor deactivation; a successful meeting may need the named scene
exit, journal write, outer-area exit, and only then community deactivation.

### 4. Confirm handoff and finalize

Return from a cleanup child through a named output such as `cleanup_done`, then
let the parent write the terminal one-shot state and terminate. The output
proves only that the graph issued its cleanup sequence. Runtime observation
must still prove that actors, UI, vehicles, markers, and persistent state match
the intended result.

```text
child cleanup_done
  -> parent receives matching socket
  -> terminal journal state
  -> completion fact
  -> root output
```

Write no required state after a terminating output; that route is unreachable.
Also avoid writing the parent's terminal fact before the child can finish its
teardown, unless re-entry intentionally bypasses cleanup and that policy is
tested.

## Cut stops a graph target, not its world consequences

`questCutControlNodeDefinition` exposes ordinary flow plus `CutSource`.
Targets such as Pause Conditions expose `CutDestination`. The Cut Control also
serializes a `permanent` field.

**Observed in vanilla:** in the cited `ma_wat_nid_15_phase.questphase`, Cut
Control node `236` has a `CutSource` edge to character-killed listener node
`225` at its `CutDestination`. Across the retained corpus, cut edges commonly
target Pause Conditions. This establishes explicit target wiring.

It does not establish that a cut:

- rolls back a fact or journal write already emitted;
- deactivates a community or removes a marker;
- stops a scene, AI command, vehicle, or device unless that exact target and
  consequence are separately evidenced;
- emits the target's ordinary output;
- survives reload or permits re-entry in a particular way;
- is reversible when `permanent` is false or irreversible when true.

Those semantics remain **Experimental**. If a late listener is cheap, make its
post-outcome edge harmless. If it must be cut, isolate the listener and Cut
Control in a mod-owned fixture and test both arrival orders, simultaneous
signals, reload with both armed, and re-entry.

## Resource-specific cleanup rules

### Scenes

A scene section's normal/cancel socket, an `scnEndNode`, a public named exit,
the quest wrapper's `Default INT`/`Default RET`, and a quest
`CutDestination` are different interfaces. None implies community
deactivation or quest completion.

For a normal route, wait for the exact named scene output before advancing the
outcome and releasing actors. For interruption, decide whether the scene may
return, terminates into a named failure/cancel outcome, or remains unsupported.
Active-line interruption and cut behavior in the current lab remain
**Experimental**; do not silently route their unwired sockets into success.

See [Cleanup and save state](../scenes/cleanup-and-save-state.md) for the scene
boundary matrix.

### Actors, communities, AI, and workspots

`questSpawnManagerNodeDefinition` can carry an action whose
`questCommunityTemplate_NodeType` requests `Deactivate`. Its outgoing graph
edge proves command issuance, not immediate disappearance.

**Observed in vanilla:** the cited `mq003_homeless.questphase` changes named
community phases and deactivates community-backed actors later in its
lifecycle. **Runtime-proven:** `DE2A28EF...` showed surviving-actor
deactivation after its exact leave-area boundary.

Deactivate only after scenes, AI, workspots, combat, carry, and vehicle seats
no longer need the actor. A timer alone is not a safe-release proof. Use a
measured outer boundary or another authoritative state, and test dead,
unconscious, missing, combat-active, streamed-out, and reloaded variants when
the design supports them.

Early role release has a concrete warning. Archive
`3EB9FCB4DBD1CA8BA6730C02CDF81B8A89B855C75372FFF8927DC66F0423D597`
advanced through three escort gates, then cleared its follower role too early;
the persistent target walked back toward the original AI spot as the hold
began. That partial result is **Runtime-proven** for that archive only. It does
not define a universal safe follower-clear command or timing rule.

See [Cleanup and character safety](../communities/cleanup-and-character-safety.md)
for actor-specific acceptance cases.

### World markers, triggers, and streamed placements

Retire a quest mappin through its journal or Mappin Manager owner. A trigger is
world geometry observed by a condition; completing the condition does not
delete the trigger, and streaming it out does not cancel every graph listener
that referenced it.

Placed world objects normally remain owned by their sector/prefab and stream
according to that owner. Do not invent a generic despawn step for a trigger,
marker, or prop. Instead, disable the player-facing state the quest activated,
make remaining observers harmless, and test stream-away/return after every
supported outcome.

### Devices

Device cleanup is an authored final-state policy, not a universal reset. The
device may need to preserve an open/unlocked/completed state, restore an
evidence-matched state, disconnect a personal link, or remain under its native
world owner.

Changing the archive does not clear device persistent state already retained
by the save. Use a fresh identity or a save that never streamed it when testing
package or controller changes. See [Advanced devices, interactions, and
persistent state](../world/advanced-devices-and-interactions.md).

### Vehicles

Choose cleanup from the vehicle's acquisition owner:

| Vehicle origin | Cleanup owner to investigate |
| --- | --- |
| Community/spawn-set vehicle | Community entry/phase and the actors/seats still using it |
| Placed world vehicle | Sector/prefab and any resource-specific quest operation |
| Player-vehicle record | Player-vehicle system and exact record state |
| Scene-staged vehicle | Scene exit plus quest handoff, occupants, and post-scene visibility |

The cited `sq031_porsche.questphase` is an **Observed in vanilla** context for
`questEnablePlayerVehicle_NodeType`, whose serialized payload includes a
vehicle record string and `enable`, `despawn`, and
`makePlayerActiveVehicle`. It is not a generic world-entity despawner.

Two retained candidates show why ownership matters:

- archive `707CA5603E84D802B11400CF98761624A1B9156E56BF6752B695C30AA29B5D19`
  had a separate theft vehicle disappear exactly at an intermediate
  contact-vehicle cleanup handoff while both custom player-vehicle records had
  live instances;
- archive `84BA33E9...` removed that intermediate cleanup and completed its
  exact six-stage route with a dedicated final player-vehicle cleanup.

Both observations are **Runtime-proven** only for their own archive and route.
They do not prove the cause of the failure or a generic vehicle-cleanup recipe.

### Journal, inventory, facts, and rewards

These writes are not visual cleanup; they are the durable meaning of the
outcome. Order them deliberately:

1. record the branch outcome;
2. update the objective, description, or pin whose promise is now resolved;
3. run safe resource teardown;
4. return through the cleanup owner's output;
5. write the terminal one-shot fact and quest state at the owning parent;
6. grant or remove inventory exactly once at its commitment boundary.

Failure and cancellation branches should not inherit success rewards or item
removal merely because they converge on common cleanup.

## Design cleanup as an idempotent protocol

Reload can resume between any two reachable graph writes. A cleanup protocol
should therefore distinguish at least:

```text
outcome_chosen
cleanup_started
cleanup_finished
activity_terminal
```

These may be explicit facts, journal states, or graph checkpoints rather than
four literal fact names. The distinction matters more than the storage form.

Do not assume a cleanup command is idempotent. If a save can occur after the
command was issued but before `cleanup_finished`, test whether reload repeats
it, skips it, or restores the graph after it. A guard can prevent a second
quest-side emission, but it cannot prove what the device, actor, scene, or
vehicle already persisted.

An upgrade/removal path is a separate policy. A completion fact can prevent
new activation, but it cannot erase an active scene, old controller state,
community phase, vehicle instance, or journal state retained in a save.

## Author and inspect the teardown in WolvenKit

1. Duplicate a mod-owned test project and assign a fresh candidate identity.
   Do not edit an installed lab or copy a complete vanilla phase.
2. Draw the owner ledger before editing the graph. Include every parallel
   listener, delay, scene, actor, AI/workspot, marker, device, vehicle,
   inventory write, journal entry, and fact.
3. Give success, failure, cancel, timeout, and interruption distinct incoming
   routes. Write their discriminator before shared cleanup.
4. For every independent listener, either gate all late writes on the chosen
   outcome or add a Cut Control only after the exact target behavior has an
   acceptance plan.
5. Wire scene normal and supported interruption outputs explicitly. Leave
   unsupported `Default INT`, `Default RET`, and `CutDestination` routes
   visibly unwired and label them **Experimental**.
6. Release AI, workspot, carry, and seat ownership before community
   deactivation. Use a measured safe boundary where visible disappearance
   matters.
7. Retire objectives and mappins according to each outcome. Do not let common
   cleanup overwrite a deliberate `Failed`, `Succeeded`, or resumable state.
8. Apply device and vehicle operations only to the exact controller/record and
   owner class for which the experiment has evidence.
9. End a cleanup child with a named output and connect the matching parent
   socket. Put the parent's terminal write before its output and after the
   child handoff.
10. Save, close, reopen, and serialize every affected CR2W. Review concrete
    node types, socket classes, edges, NodeRefs, controller/record values,
    action arrays, output names, and the order of all durable writes.
11. Cook, pack, extract, and hash the exact mod-owned payload. Keep the archive
    inventory with the acceptance record.

The existing labs demonstrate smaller ownership boundaries. Combining their
shapes into a mixed scene/actor/device/vehicle teardown creates a new
**Experimental** candidate; structural validity does not inherit runtime
results from its parts.

## Clean-save, interruption, and reload matrix

Begin positive identity/topology testing from an untouched save created before
the candidate was ever installed. Clone complete save slots only while the
game is closed. Bind every row to the same archive hash unless the row is an
explicit upgrade/removal case.

| Case | Required observation |
| --- | --- |
| Normal success | One outcome is written; presentation retires; every owner releases in order; terminal state occurs once |
| Each authored failure | Failure reason survives cleanup and reload; no success reward, item removal, or objective state leaks in |
| Player cancellation | Retry or terminal-cancel policy is exact; UI/workspot/scene state releases; no irreversible success write occurs |
| Monitor wins | Losing main-route signal cannot mutate state later |
| Main route wins | Losing monitor remains harmless or the tested cut handles it |
| Near-simultaneous signals | The observed result matches the only ordering on which the design relies |
| Save with all listeners armed | Reload restores or neutralizes each route without duplicate outcome writes |
| Save after outcome, before teardown | Reload resumes the correct cleanup branch and does not re-run activity success |
| Save after each owner release | Remaining owners finish; already released resources do not duplicate, vanish incorrectly, or regain ownership |
| Active scene interruption/return | Supported path retains actor and progression; unsupported path remains recorded as **Experimental** |
| Combat/death during cleanup | Actor, AI, wave, and deactivation policy reaches an intentional result |
| Vehicle occupied during cleanup | Occupants, seats, player control, and vehicle lifetime remain coherent |
| Device operation active during cleanup | UI/personal link/workspot and controller reach the authored final state |
| Stream away and return | No stale pin, duplicate spawn, restarted scene, repeated reward, or rearmed terminal listener |
| Completed-save reload | Root guard bypasses activity; cleanup does not replay; world/save state matches the claim |
| Upgrade/removal copy | Lingering save-backed state is documented and not misreported as clean-install behavior |
| Second untouched save | The exact candidate reproduces without inherited facts, journal, graph, scene, community, device, or vehicle state |

If the game forbids saving at a boundary, record that limitation and test the
nearest supported checkpoint. An unexercised row remains **Experimental**.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Success and failure both write | Outcome discriminator placement, late listener gates, and convergence before state writes |
| Quest ends but marker/actor/vehicle remains | Phase output occurred before owner-specific teardown or targeted the wrong owner class |
| Actor disappears during dialogue/combat | Community deactivation precedes scene/AI/workspot/combat release |
| Scene ends but quest does not continue | Named exit, quest-wrapper output, child socket, and parent continuation are separate boundaries |
| Reload repeats reward or item removal | Commitment write is reachable twice or terminal/re-entry guard is too late |
| Reload skips required cleanup | Terminal fact was written before cleanup handoff or active graph resumed on the bypass path |
| Cut route produces an unexpected ordinary output | The design assumed unproved cut semantics; isolate and retain the exact target behavior |
| Vehicle disappears at another vehicle's cleanup | Wrong acquisition owner or record domain; inspect cross-vehicle state and intermediate child handoff |
| Device returns to an old state | Reused persistent identity or save-backed controller state, not merely the current archive payload |
| Stream return duplicates the encounter | Activation/re-entry guard, community/scene state, and late monitor remain independently live |

Previous: [Completion and interruption](completion-and-cut.md). Next: [Lab 4:
Handoff Point](lab-04.md).
