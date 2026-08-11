# Vehicle delivery, cleanup, chase, and race

Delivery is a small condition chain. Cleanup is an ownership decision. Chases
and races are large authored systems with vehicles, occupants, splines,
world-space gates, UI, recovery, and failure handling. Treating all four as
“vehicle nodes” hides the boundaries most likely to break.

Tested with Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`,
RED4ext `1.30.0`, and redscript `0.5.31`. See [Tested
versions](../reference/tested-versions.md). The stopped-delivery chain below is
a new composition and needs its own in-game test.

## Recipe: record arrival, then a later stop

A focused delivery child waits for the exact vehicle to enter the destination,
then waits for that same vehicle to stop:

```text
In1
  -> objective Active
  -> wait: designated vehicle IsInside destination trigger
  -> wait: designated vehicle speed == 0
  -> objective Succeeded
  -> Out1
```

The first wait is a `questPauseConditionNodeDefinition` containing a
`questTriggerCondition`. Its `activatorRef` is the vehicle,
`isPlayerActivator` is `0`, `triggerAreaRef` is the destination NodeRef, and
`type` is `IsInside`.

The second wait contains `questVehicleCondition` with
`questVehicleSpeed_ConditionType`:

| Field | Focused value |
| --- | --- |
| `vehicleRef` | the same exact entity reference used by the trigger |
| `comparisonType` | `CT_EQUAL` in the reduced candidate |
| `speed` | `0` |

This sequential topology proves only “the vehicle entered earlier and stopped
later.” Once `IsInside` emits, that wait is retired. The vehicle can leave the
destination and satisfy the speed wait somewhere else. Do not read this graph
as “stopped inside,” or `speed == 0` as “parked correctly.” It also does not
prove orientation, damage state, engine state, whether V exited, or whether the
vehicle belongs to the intended delivery stage.

### Require stopped and inside at the same boundary

When simultaneous containment is the promise, author one waiting predicate
whose Boolean tree requires both current states:

```text
PauseCondition
  questLogicalCondition AND
    |-> questTriggerCondition: exact vehicle IsInside destination
    `-> questVehicleCondition: same vehicle speed == 0
```

Alternatively, re-evaluate `IsInside` immediately after the speed wait and
route false back to the arrival/stop cycle. A graph-level AND that merely
remembers two earlier signals has the same temporal defect as the sequential
chain. The mixed stopped-inside predicate is **Experimental** in this book: its
exact already-true, exit/re-entry, reload, and event-order behavior needs a
retained candidate before promotion.

**Observed in vanilla:** inspect
`base\quest\side_quests\sq004\phases\sq004_02_drive.questphase` for an exact
vehicle `activatorRef` in `IsInside` triggers and a
`questVehicleSpeed_ConditionType` using `CT_LESS_EQUAL` with speed `2` for that
vehicle. This is a close low-speed precedent, not the candidate's exact
`CT_EQUAL`/`0` pair. As a second contrast,
`base\open_world\street_stories\watson\northside_industrial_district\sts_wat_nid_02\phases\sts_wat_nid_02_gameplay.questphase`
contains `CT_NOT_EQUAL`/`0` for its van while its nearby triggers are
player-activated. Do not merge those separate observations into one vanilla
delivery chain.

The reduced four-node sequential chain is **Structurally validated** at its
recorded WolvenKit `8.17.4` research boundary. Its intended stopped-inside
meaning is **Experimental** because the topology does not enforce that meaning.

The final GQT004 runtime route is not evidence for this exact stopped chain.
Its `drive_to` delivery child observed the designated vehicle entering the
destination trigger and did not contain the separate `CT_EQUAL`/`0` speed
wait.

## Separate delivery from handoff

Most delivery stories need more than the condition chain:

```text
vehicle satisfies the exact delivery predicate
  -> capture delivery fact
  -> ask V to exit, if required
  -> transfer or lock vehicle, if authored
  -> run recipient scene or message
  -> settle reward/outcome
  -> remove marker
  -> perform owner-specific cleanup
```

Each arrow is a separate claim. In particular, a recipient scene does not
transfer ownership, and a completion fact does not despawn the vehicle. Keep
the objective active until the last player-facing requirement that its text
actually promises.

## Cleanup starts with ownership

Choose cleanup from the way the vehicle entered the activity.

| Vehicle source | Likely owner | Safe question to answer |
| --- | --- | --- |
| Community/spawn-set vehicle | Community and its world placement | Which phase deactivates the entry or community, and after what distance/readiness gate? |
| Placed world vehicle | Sector/prefab plus quest lifecycle | Should it persist, stream naturally, or receive a resource-specific disable path? |
| Player-vehicle record | Player-vehicle system | Is `questEnablePlayerVehicle_NodeType` valid for this exact TweakDB record and state? |
| Scene-staged vehicle | Scene plus surrounding quest | Which exit owns unmount, visibility, and post-scene handoff? |

`questEnablePlayerVehicle_NodeType` is not a generic world-entity despawner.
GQT004 originally put an `sq031_porsche`-style player-record operation in an
intermediate contact-cleanup child. The **Runtime-proven** partial result for
a [retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
is that the separately authored theft vehicle existed during the contact drive
but disappeared exactly at that cleanup handoff while both custom
player-vehicle records had live instances. It does not establish a universal
cause.

The later fact-only intermediate child also failed: a
[retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
reached that child, did not hand off, and lost the theft vehicle as the child
was entered. That bounded failure is **Runtime-proven** for its own hash; a
generic fact-only-child rule is not. The passing six-stage route removed the
intermediate cleanup entirely. Its dedicated final child targeted the exact
`Vehicle.GhostlineGQT004Theft` player-vehicle record and ran on the
[retained route](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence).
That is **Runtime-proven** only for that record, ordering,
and archive; it is not generic community/world-vehicle cleanup.

**Observed in vanilla:** extract
`base\quest\side_quests\sq031\phases\sq031_porsche.questphase` and inspect the
exact `questEnablePlayerVehicle_NodeType` context, record domain, incoming
state, and following nodes. Do not substitute a community entry or world
NodeRef for its vehicle record.

For community actors and vehicles, begin with [Cleanup and character
safety](../communities/cleanup-and-character-safety.md): stop dependent work,
deactivate at a safe boundary, and retest stream-away/return. Precise cleanup
for a newly authored vehicle remains **Experimental** until the exact owner and
save behavior pass in game.

## Chase is a coordinated encounter

There is no retained generic chase child in this book or its research input.
A chase needs at least:

- spawned vehicles and occupants with consistent community/entry identities;
- seat assignment and spawned-readiness gates;
- movement or combat AI with a target and recovery policy;
- start, success, lost-target, damage, death, and interruption signals;
- streaming coverage along the route;
- player-facing objectives and mappins that survive detours and reloads;
- cleanup for every vehicle, occupant, monitor, and restriction.

**Observed in vanilla:** the installed
`base\open_world\street_stories\badlands\inland_avenue\sts_bls_ina_07\phases\sts_bls_ina_07_gpl.questphase`
contains named chase facts, multiple `questVehicleNodeDefinition` assignment
operations that bind occupants to vehicle seats, AI patrol roles, and
conditions for lost/route state. That observation is evidence of a composite,
not an isolated reusable chase recipe.

Use the vanilla phase as a question map:

1. Which resource spawns each pursuer vehicle and occupant?
2. Which node assigns each character to which seat?
3. Which AI command begins movement or combat?
4. Which facts distinguish route and lost-target states?
5. Which branch owns success, failure, and cleanup?

If those answers span several external phases or world resources, preserve the
split. Collapsing them into one guessed child discards lifecycle ownership.

## Race is a subsystem, not a trigger loop

**Observed in vanilla:** the installed
`base\quest\side_quests\sq024\phases\sq024_05_the_big_race.questphase`
contains all of the following focused shapes:

| Shape | Native type or reference |
| --- | --- |
| Start and stop the race subsystem | `questStartRace_NodeType`, `questStopRace_NodeType` |
| Return/recovery route | `questGoBackToRace_NodeType` plus player-facing restriction/objective state |
| Competitor movement | `questvehicleRacingParams` on vehicle command nodes |
| Course ownership | spline NodeRefs, including a race-specific spline in that phase |
| Opponent behavior | racing parameters, target refs, precision, push-aside, and rubber-banding policy |
| Player/vehicle state | mount and spawned conditions plus camera and gameplay restrictions |
| Progress and outcome | checkpoint resources/facts, `VehicleRaceQuestEvent`, Journal state, and finish/stop logic |

That phase also coordinates scenes, communities, race crowds, competitors,
player-vehicle selection, and recovery. A row in the table is not sufficient
on its own.

A safe authoring decomposition is:

```text
course/world assets
  -> competitor and player-vehicle readiness
  -> pre-race scene and restrictions
  -> start-race operation
  -> checkpoint/progress subsystem + opponent movement
  -> finish, leave-course, damage, and interruption branches
  -> stop-race operation
  -> restore restrictions, settle outcome, clean every dependency
```

For a new race, first document the course spline and checkpoint owner, then one
competitor's complete lifecycle, then the player recovery route. Do not claim
a generic recipe until that reduced arrangement survives leaving the course,
reloading mid-race, losing or destroying a competitor, finishing, and replay
isolation.

## Manual WolvenKit composition order

1. Choose one bounded activity: stopped delivery, owner-specific cleanup,
   chase research, or race research. Do not start by combining all four.
2. Extract only the relevant current-game comparison phase named above and
   record each inspected node's containing graph, identities, decisive fields,
   and surrounding lifecycle.
3. Author the mod-owned vehicle, occupants, trigger/spline/checkpoint assets,
   community/world ownership, journal entries, and unique NodeRefs before the
   quest child.
4. For arrival-only delivery, bind the destination wait to the exact vehicle as
   a non-player activator. For stopped-inside delivery, require current trigger
   and speed state in one Boolean predicate or a deliberate recheck loop; do
   not use two latched historical signals as simultaneous truth.
5. For cleanup, identify whether the target belongs to a community, world
   placement, player-vehicle record, or scene. Use only an operation whose
   identity domain matches that owner.
6. For a chase, prove both vehicles and occupants spawned before seat
   assignment or AI; give success, lost-target, failure, stop, and cleanup
   routes explicit outputs.
7. For a race, reduce the cited subsystem to one course and competitor while
   preserving start/stop, checkpoint, recovery, restriction, and cleanup
   ownership. Keep the result **Experimental**.
8. Reopen every mod-owned phase and inspect handles, sockets, vehicle refs,
   entry names, trigger refs, comparisons, facts, and terminal outputs.
   Round-trip the resources with WolvenKit `8.19.0`.
9. Pack and hash one candidate. Run delivery/cleanup or chase/race cases from
   separate copies of an untouched pre-install save, retaining fresh logs and
   state captures.
10. Promote only the exact observed result. Keep stopped delivery, generic
    cleanup, reload/interruption, chase, and race **Experimental** unless their
    own retained matrices pass.

## Failure patterns

| Symptom | First boundary to isolate |
| --- | --- |
| Delivery completes when V walks in | `isPlayerActivator` or an empty/wrong `activatorRef` |
| Correct vehicle enters but never completes | Vehicle identity differs between trigger and speed condition, or exact-zero semantics never become true |
| Contact/occupants vanish during route | Community activation, streaming coverage, or assignment before spawned readiness |
| Cleanup removes the wrong vehicle | Player-record operation used for a community/world vehicle, or broad cleanup shares one owner |
| Chase starts but cannot finish | Lost-target/success/stop monitors do not converge or one route never releases the parent |
| Race UI or restrictions remain | Stop/restore cleanup is reachable only from the normal finish branch |
| Reload duplicates opponents or checkpoints | Save-backed stage facts and activation guards do not distinguish resume from restart |

Use [NodeRefs, streaming, and
placement](../troubleshooting/noderefs-streaming-placement.md), [Handles,
sockets, and resource
references](../troubleshooting/handles-sockets-resources.md), and [Controlled
isolation and evidence](../troubleshooting/controlled-isolation-evidence.md)
to reduce the failure before changing several systems at once.

## Acceptance matrices

For a simultaneous stopped-inside delivery and its cleanup, retain at least:

| Case | Required result |
| --- | --- |
| Wrong vehicle enters destination | No progress |
| Correct vehicle passes through without stopping | Delivery remains incomplete |
| Correct vehicle enters, leaves, then stops outside | No progress; the sequential structural control should expose its false positive here |
| Correct vehicle stops inside | Delivery succeeds exactly once |
| Reload while inside but moving | The stopped wait resumes without replaying earlier one-shot work |
| Reload after delivery before cleanup | Handoff and cleanup resume intentionally |
| Stream away after cleanup | No unintended respawn or remaining marker |
| Clean-save replay and removal isolation | No old vehicle/device/community state is mistaken for the candidate |

For a chase or race, add route departure, catch-up/recovery, competitor death or
destruction, mid-route reload, normal finish, failure, interruption, and
post-completion replay. Record vehicle/occupant counts and every restored
restriction, not only the final quest fact.
