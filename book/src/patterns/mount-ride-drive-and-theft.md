# Mount, ride, drive, and theft

Vehicle objectives join a quest graph to an already authored vehicle. The
graph can wait for V or another character to mount it, assign a character to a
seat, observe the vehicle inside a trigger, update Journal presentation, and
preserve an outcome fact. It does not create the vehicle's community entry,
placement, driving AI, road route, or cleanup policy.

| Record | Value |
| --- | --- |
| Practical baseline | Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Vanilla inspection date | 2026-08-09 |
| Reduced-candidate provenance | Ghostline research commit `29066f7b76ad4b7435b3fa2a7c0b20ecea464b5e` |
| Exact legacy vehicle campaign | **Runtime-proven** only for archive SHA-256 `84BA33E902360BC4F1ED32A0865CE8B15C35D9442FD519CC6C3E85A06D1AE77B` at source commit `a24c341c1e2eca43f05a100f5776baba377b2260` |

The reduced mount, paired-ride, destination, and theft candidates are
**Structurally validated** at their recorded WolvenKit `8.17.4` research
boundary. Comparable shapes are **Observed in vanilla** in the depot paths
named below. The later hash-bound legacy candidate completed its exact
contact-mount, Patch-passenger, contact-arrival, designated-theft,
delivery-trigger, and final-cleanup route in game. That result does not promote
a newly authored vehicle lifecycle—or its untested reload, interruption, and
failure paths—to **Runtime-proven**.

## Name the vehicle before building the graph

A vehicle reference can use different identity domains. Record which one the
chosen node expects.

| Identity | Example consumer | What must exist |
| --- | --- | --- |
| Community NodeRef plus entry CName | `questCharacterMount_ConditionType`, `questAssignCharacter_NodeType`, a vehicle-as-activator trigger | A streamed community registry, vehicle entry, spawn set, and placement that resolve together |
| Direct world NodeRef | A trigger or condition whose `gameEntityReference.reference` names one placed vehicle | A stable placed entity in the owning prefab/sector scope |
| Player-vehicle TweakDB record | `questEnablePlayerVehicle_NodeType` | A player-vehicle record and the player-vehicle system; not an arbitrary world vehicle |
| Scene actor | Vehicle staging owned by a scene | A declared scene actor and scene-local acquisition contract |

Do not put a community NodeRef into `names`, an entry CName into `reference`,
or a TweakDB record into either field. See [Identifier
domains](../foundations/identifier-domains.md) and [Quest prefabs and
NodeRefs](../world/quest-prefabs-and-noderefs.md).

For a community-owned vehicle, a typical entity reference has this semantic
shape:

| Field | Value domain |
| --- | --- |
| `reference` | NodeRef of the community registry or compatible entity owner |
| `names` | one CName selecting the vehicle entry |
| `type` | `EntityRef` |
| `dynamicEntityUniqueName` | normally `None` unless that identity route was deliberately authored |

The same pair must be used by mount, assignment, arrival, and cleanup logic.
Changing only one consumer creates two apparently plausible identities for one
vehicle.

## Recipe: V enters a named vehicle

Use this shape when completion means that V mounts the designated vehicle. It
does not prove that V is the driver unless the role and seat contract require
that state.

```text
In1
  -> objective Active
  -> vehicle mappin Active
  -> wait: V OnMount designated vehicle
  -> objective Succeeded
  -> vehicle mappin Inactive
  -> Out1
```

The waiting node is a `questPauseConditionNodeDefinition` whose condition is a
`questCharacterCondition` carrying a
`questCharacterMount_ConditionType`.

| Mount field | Focused value | Meaning |
| --- | --- | --- |
| `condition` | `OnMount` | Wait for the mount event/state represented by this condition family |
| `childIsPlayer` | `1` | The mounted child is V |
| `parentRef` | the exact vehicle entity reference | The designated parent vehicle, not any nearby car |
| `anyParent` | `0` | Keep the parent bound to that reference |
| `anyChild` | `0` | Do not broaden the child match |
| `role` | choose deliberately | `Driver`, `Passenger`, or a tested neutral role must match the intended objective |
| `vehicleOrigin`, `vehicleType` | only broaden when intended | `Any` is not a substitute for the exact `parentRef` |

The focused reduced candidate used a neutral role while the vanilla driving
comparison contains role-aware variants. If the objective says “drive,” test
the driver-seat condition; a neutral mount condition can also succeed when V
enters as a passenger.

**Observed in vanilla:** extract
`base\quest\side_quests\sq004\phases\sq004_02_drive.questphase` and inspect
only its mount conditions, vehicle references, and nearby objective flow.
Those nodes remain bound to `sq004` identities and are not a copy-ready child
phase.

## Recipe: V rides with a contact

“Ride with” has two independent facts: the contact occupies the intended seat
and V occupies the same vehicle. A single mount wait cannot prove both, while
two latched signals do not automatically prove both remain true together.

```text
                 -> wait: V mounted as intended -----------\
In1 -> objective -> assign contact to vehicle seat          AND -> objective Succeeded -> Out1
                 -> wait: contact mounted as passenger ----/
```

1. Activate the objective.
2. Use `questVehicleNodeDefinition` with
   `questAssignCharacter_NodeType` to bind the contact to the vehicle and seat.
3. Fan out to one player mount condition and one contact mount condition.
4. Join them with `questLogicalAndNodeDefinition`; use two distinct input
   sockets.
5. Succeed the objective only after the join fires.

That graph-level AND is only a structurally valid signal join. Its
arrival-memory, unmount, cancellation, and reload semantics remain
**Experimental**. If the objective requires both actors to occupy the vehicle
at the same boundary, use one waiting `questLogicalCondition` whose AND tree
contains both current mount predicates, or immediately recheck both current
states before success. Retain an adversarial test where the first actor
unmounts before the second mounts; the ordinary passing GQT004 route does not
prove that ordering.

The assignment payload needs four identities plus explicit operation policy:

| Property | Owner |
| --- | --- |
| `characterRef.reference` | contact community NodeRef |
| `characterRef.names` | contact entry CName |
| `vehicleRef.reference` | vehicle community or entity NodeRef |
| `vehicleRef.names` | vehicle entry CName |
| `assign` | `1` to assign the contact; `0` is a clear/unassign operation, not an equivalent default |
| `isPlayer` | `0` when `characterRef` names the contact; `1` changes the subject to V |
| `slotName` | a seat slot supported by the vehicle, such as a tested passenger slot |
| `isInstant` | staging policy; the exact passing candidate used `1`, which is not a visible enter animation |

The exact passing GQT004 assignment used `assign: 1`, `isPlayer: 0`,
`isInstant: 1`, and `slotName: seat_front_right`. Those values prove that
candidate's Patch-passenger operation; they are not universal seat or staging
defaults.

Assignment is not readiness. Wait for the contact community and vehicle to be
streamed and spawned before issuing it, then retain the contact mount
condition. A fast approach can otherwise expose the same readiness class
described in [Activation, readiness, and
acquisition](../communities/activation-readiness-and-acquisition.md).

**Observed in vanilla:** compare the player/contact mount conditions and
`questAssignCharacter_NodeType` work in
`base\quest\side_quests\sq004\phases\sq004_02_drive.questphase`. The reduced
candidate proves only a structurally valid assignment plus two-way join; it
does not provide a road spline, driving command, scene, or interruption route.

## Recipe: drive a named vehicle into an area

The arrival trigger must observe the vehicle, not V. Reusing a player-area
condition completes when V crosses the boundary on foot.

```text
In1
  -> objective Active
  -> destination mappin Active
  -> wait: designated vehicle IsInside destination trigger
  -> objective Succeeded
  -> destination mappin Inactive
  -> set completion fact = 1
  -> Out1
```

Use a `questTriggerCondition` with:

| Field | Required contract |
| --- | --- |
| `triggerAreaRef` | NodeRef of the placed destination trigger |
| `activatorRef` | exact vehicle entity reference |
| `isPlayerActivator` | `0` |
| `type` | `IsInside` |

This is arrival, not delivery. If the vehicle must also stop, continue with
the speed condition in [Vehicle delivery, cleanup, chase, and
race](vehicle-delivery-cleanup-chase-race.md). If V must remain inside, add a
separate mount condition and join it explicitly.

## Recipe: record theft by mount

A minimal theft objective is the enter-vehicle recipe followed by a persistent
outcome fact:

```text
objective Active -> mappin Active -> V OnMount vehicle
  -> objective Succeeded -> mappin Inactive
  -> theft fact = 1 -> Out1
```

The fact records the quest's interpretation of the event. It does not change
vehicle ownership, player-garage availability, police response, lock state, or
despawn behavior. Those systems need separately authored and tested resources.

Use distinct facts for “mounted,” “delivered,” and “cleaned” when later logic
needs to diagnose partial progress. One overloaded completion fact makes
reload repair ambiguous.

**Runtime-proven:** `84BA33E9...` completed this exact sequence with its two
named community vehicles: V mounted the contact vehicle, Patch was assigned as
passenger, the contact vehicle reached its destination, V mounted the
designated theft vehicle, that vehicle reached its delivery trigger, and the
final player-vehicle cleanup ran. Its delivery child did not contain the
separate exact-zero speed wait, and the result does not prove another vehicle,
seat, owner, or cleanup operation.

## Manual WolvenKit composition order

1. Extract the cited `sq004_02_drive.questphase` from your own game and inspect
   only its mount, assignment, and vehicle-activator fields. Record its graph
   scope; do not copy the phase or its identities.
2. Author or select the vehicle's actual owner: community/spawn set, placed
   world entity, player-vehicle record, or scene. Give the mod-owned vehicle,
   contact, prefab, and NodeRefs unique identities.
3. Verify the vehicle and any contact resolve and become spawned before adding
   assignment or mount waits.
4. In the child phase, activate the intended objective and mappin, then add one
   `questPauseConditionNodeDefinition` per player/contact mount truth.
5. Bind every `gameEntityReference` with the exact community/world NodeRef and
   entry name expected by that condition. Choose the player role and passenger
   seat deliberately.
6. Add `questAssignCharacter_NodeType` only after readiness. When simultaneous
   occupation is required, prefer a Boolean condition tree or an explicit
   current-state recheck over a graph join that can remember old signals.
7. For arrival, place a destination trigger and bind the exact vehicle as its
   non-player activator. Keep vehicle arrival separate from player presence and
   stopped-delivery semantics.
8. Succeed presentation, remove mappins, and write distinct mount/arrival/theft
   facts before handing off to delivery or cleanup.
9. Reopen the phase and inspect handles, sockets, NodeRefs, entry names, seat
   slots, roles, and journal paths. Round-trip the mod-owned resources with
   WolvenKit `8.19.0`.
10. Pack one exact candidate and run the controlled cases below from separate
    copies of an untouched pre-install save.

## Presentation and lifecycle checklist

Before connecting the child phase, confirm:

- the objective and map-pin paths resolve to the intended entries and share
  the correct `fileEntryIndex`;
- the map pin points to the vehicle or destination that the condition uses;
- the parent phase owns every prefab needed to resolve vehicle, community, and
  trigger NodeRefs;
- the vehicle and contact have explicit activation and spawned-readiness
  gates;
- completion inactivates presentation without erasing facts needed for later
  stages;
- interruption says whether the contact unmounts, the vehicle remains, and
  the objective fails or becomes inactive;
- another child owns delivery, cleanup, or handoff instead of silently
  assuming it happened.

## Controlled runtime cases

Run these cases in separate save slots after the candidate is structurally
validated:

| Case | Start state | Expected observation |
| --- | --- | --- |
| Normal mount | Vehicle and contact not previously activated | Correct vehicle resolves; only the intended seat/state completes |
| Wrong vehicle | Another vehicle is beside the target | Mounting the other vehicle does not advance |
| Passenger versus driver | V changes seats before the wait | The declared role behaves exactly as documented |
| First actor unmounts early | Contact or V leaves before the other mount truth occurs | A simultaneous-occupancy objective does not complete from two historical signals |
| Fast approach | Load just outside streaming range and approach quickly | Readiness gates prevent lost assignment or mount waits |
| Reload before mount | Objective and mappin active | The same vehicle identity and wait resume |
| Reload after fact | Theft/arrival fact already `1` | Parent re-entry policy skips or resumes intentionally |
| Stream away and return | Vehicle remains quest-relevant | Community, entry, marker, and condition still resolve |
| Removal isolation | Candidate archive and loose registrations removed on a dedicated copy | No save-backed state is mistaken for installed content |

Vehicle and device state can be save-backed. Follow [Save state and clean
retests](../troubleshooting/save-state-clean-retests.md) before changing a
NodeRef or entry name and declaring the edit causal.

## Evidence boundary

| Claim | Evidence |
| --- | --- |
| Mount, paired-ride, arrival, and steal-by-mount reduced graphs serialize and round-trip at their recorded research boundary | **Structurally validated** in Ghostline commit `29066f7b76ad4b7435b3fa2a7c0b20ecea464b5e`; this is source evidence, not a reader tool |
| Comparable mount, assignment, and vehicle-route shapes exist in `sq004_02_drive` | **Observed in vanilla** on the cited depot path |
| The final GQT004 vehicle-lab route completed its exact six-stage mount/passenger/arrival/theft/delivery-trigger/final-cleanup sequence | **Runtime-proven** only for archive `84BA33E902360BC4F1ED32A0865CE8B15C35D9442FD519CC6C3E85A06D1AE77B` and the source/environment boundary above |
| A new mod-owned vehicle, contact, seats, triggers, reloads, and interruption behave as intended | **Experimental** until that exact arrangement passes retained in-game cases |

Continue with [Vehicle delivery, cleanup, chase, and
race](vehicle-delivery-cleanup-chase-race.md), [Triggers and
areas](../world/triggers-and-areas.md), and [Lifecycle, cleanup, and
evidence](../foundations/lifecycle-and-evidence.md).
