# Delays, facts, and persistence boundaries

A delay in a questphase is a condition payload, normally held by a Pause
Condition node. It gates the route that entered it; it does not schedule a
complete quest action by itself. The nodes after the delay still own the
journal update, fact write, scene start, or other effect.

This distinction matters when saves, time skips, and re-entry are involved.
The serialized resource describes the delay and its wiring, while only runtime
tests can establish how its active state survives interruption.

## Pinned acceptance environment

| Component | Version |
| --- | --- |
| Cyberpunk 2077 for Windows | `2.31a` (GOG) |
| WolvenKit | `8.19.0` |
| ArchiveXL | `1.27.0` |
| RED4ext | `1.30.0` |
| redscript | `0.5.31` |

Review date: **2026-08-09**.

The book-owned Lab 2 CR2W resources are **Structurally validated** by cooking
and serializing them back with WolvenKit `8.19.0`. The other values pin the
environment required by the future runtime acceptance run; they have not yet
been exercised together for Lab 2. Timing and reload behavior therefore remain
**Experimental** until the dedicated record passes.

## Realtime delay payload

`questTimeCondition` wraps a concrete time condition. The realtime form is
`questRealtimeDelay_ConditionType`:

| Property | Role |
| --- | --- |
| `hours` | Whole realtime hours |
| `minutes` | Whole realtime minutes |
| `seconds` | Whole realtime seconds |
| `miliseconds` | Millisecond remainder; the native field is misspelled |

Keep the spelling `miliseconds` in the native property tree. Correcting it to
English creates the wrong field in raw representations.

**Observed in vanilla:** nested Pause Condition node 71 in
`base\open_world\street_stories\westbrook\japantown\sts_wbr_jpn_03\phase\sts_wbr_jpn_03_streetstory.questphase`
holds a two-second realtime delay.

Lab 2 uses 30- and 120-second realtime waits so the intermediate objective
state is observable and a tester can make a mid-flow save. The WolvenKit
round-trip proves their resource shape; it does not yet prove what the clock
does in a pause menu, loading screen, or save/reload.

## Game-time delay payload

`questGameTimeDelay_ConditionType` stores game-world duration fields:

| Property | Role |
| --- | --- |
| `days` | Whole game-time days |
| `hours` | Whole game-time hours |
| `minutes` | Whole game-time minutes |
| `seconds` | Whole game-time seconds |

**Observed in vanilla:** the following depot resources contain long game-time
waits:

| Depot path | Observed payload |
| --- | --- |
| `base\quest\side_quests\sq011\phases\sq011_concert.questphase` | 23 hours |
| `base\quest\side_quests\sq011\phases\sq011_follow_up.questphase` | 3 days |
| same follow-up phase | 5 hours |

Those observations establish the payloads, not every clock rule. The contact,
message, or scene seen after an SQ011 delay is downstream behavior and should
not be attributed to the time condition itself.

## Choose the clock deliberately

Use a realtime delay when the authored meaning is a short wall-clock beat such
as debouncing a transition or allowing a presentation step to breathe. Use a
game-time delay when the fiction depends on Night City time passing.

Do not choose solely by duration. A ten-second game-time wait and a ten-second
realtime wait ask different runtime questions:

| Interruption | Realtime question | Game-time question |
| --- | --- | --- |
| Pause menu | Does wall-clock progress continue? | Does game time stop? |
| Time skip | Is the wait unaffected? | Can the target be crossed immediately? |
| Fast travel | Does loading count? | Does travel advance the target? |
| Save/load | Is elapsed duration restored or restarted? | Is the target timestamp restored? |
| Process restart | Is active condition state serialized? | Is the target reconstructed? |

All answers in that table are **Experimental** until tested on the pinned
build. Enum names and vanilla serialization do not settle them.

## Facts are durable design state, not Boolean variables

`questFactsDBCondition` compares a named fact's signed integer value. Facts are
often used as zero/nonzero flags, but their native model is an integer:

```text
cqa002_completed Equal 0
cqa002_test_mode Equal 2
cqa002_signal_failed Greater 0
```

The comparison operators represented in retained resources include `Equal`,
`NotEqual`, `Greater`, `GreaterOrEqual`, `Less`, and `LessOrEqual`.

A fact can make a delayed route re-entry-safe only if the graph checks and
writes it at the right boundaries. The fact's persistence does not magically
cancel an active listener or undo a side effect that already ran.

## One-shot entry guard

Place a completed guard before the first player-facing or save-backed effect:

```text
Input
  -> Condition(completed == 0)
       False -> terminating Output
       True  -> first-run route
```

Write the completion fact before, or in a tightly controlled sequence with,
the final visible completion transition. Then make the False route terminate
without reactivating journal entries, starting scenes, or spawning world
content.

Use different facts when “started” and “completed” have different meanings.
One fact cannot distinguish a partially completed run from a never-started run.

This pattern is **Structurally validated** in the book's labs. Re-entry and
reinstall behavior remain **Experimental** until the exact completed save and
installed payload are hash-bound to a passing runtime record.

## Clean-save rule

Facts, journal state, active quest nodes, scene state, communities, and device
persistent state can all be save-backed. A save made after an earlier build was
installed is not a clean first-run test, even when the archive has since been
removed.

For every practical delay or one-shot test, retain:

1. one untouched save created before the candidate was first installed;
2. one save made while the delay or listener is active;
3. one save made after completion;
4. the exact installed archive and registration file;
5. exact game/mod versions and fresh logs;
6. hashes for all retained evidence.

Never reuse the mid-flow or completed save as the clean replay baseline.

## Minimum timer acceptance matrix

| Case | What to record |
| --- | --- |
| Uninterrupted | Earliest and observed completion time |
| Pause menu | Whether the target advances while paused |
| Save during wait | Remaining time or restart behavior after reload |
| Process restart | Same observation after closing the game completely |
| Time skip | Whether a game-time target is crossed and emitted once |
| Fast travel | Loading/travel effect on both clock and output |
| Completed reload | No second journal activation or delayed output |
| Clean replay | Same first-run result from the untouched save |

Record what happened; do not normalize a surprising result into the behavior
you expected. See [Lab 2 test protocol](lab-02-test.md) for the concrete
two-route version of this matrix.

Even a fully passing Lab 2 record promotes only its listed uninterrupted,
mid-flow reload, completed reload/reinstall, and clean-replay cases. It does
not promote pause-menu, full process-restart, time-skip, fast-travel,
simultaneous-arrival, or late-second-XOR-input behavior; those rows remain
**Experimental** until a future fixture exercises them explicitly.
