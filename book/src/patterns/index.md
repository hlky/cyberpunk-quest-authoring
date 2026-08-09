# Gameplay patterns

This cookbook composes the native quest, journal, scene, community, world,
device, character, and vehicle systems taught earlier. Start from the player
behavior you want, then follow the resource owners all the way through
activation, a durable completion signal, and cleanup.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Research input | Focused vanilla resources and hash-bound legacy candidates retained in Ghostline history; Ghostline is not a reader dependency |
| Default status for a new composition | **Experimental** until that exact package passes a retained, version-bound, clean-save matrix |

## Choose the owning systems

| Desired behavior | Primary guide | Systems that must agree |
| --- | --- | --- |
| Send a text, offer a reply, or start a call | [Messages, calls, and conversations](messages-calls-and-conversations.md) | Journal, localization, phone state, and optionally scene/audio |
| Turn a choice into later content | [Branching, choices, and debriefs](branching-choices-and-debriefs.md) | Choice owner, facts, gates, journal, and downstream phases |
| Reach, leave, interact, hack, plant, or deposit | [Areas, devices, and hacking](areas-devices-and-hacking.md) | World placement, NodeRefs, controller state, quest logic, and save identity |
| Acquire an item, read a shard/file, or scan a clue | [Items, shards, files, and scans](items-shards-files-and-scans.md) | TweakDB or journal content, localization, inventory/scan producer, and quest observer |
| Place an actor or expose a device interaction | [Workspots and interactions](workspots-and-interactions.md) | Community or entity template, world placement, workspot, controller, and quest lifecycle |
| Open, close, lock, or expose a world door | [Doors are device contracts](workspots-and-interactions.md#doors-are-device-contracts) | Door entity/controller, NodeRef, supported action, interaction policy, navigation, and persistent state |
| Wait in real time, game time, or for a time period | [Delays, facts, and persistence](../gates/delays-and-persistence.md) | Clock domain, wait semantics, durable facts, reload, and re-entry policy |
| Meet or coordinate a named NPC | [NPC interaction and meetings](npc-interaction-and-meetings.md) | Community identity, readiness, acquisition, scene or interaction, and cleanup |
| Monitor stealth, run combat, plant, or destroy | [Stealth, combat, and destruction](stealth-combat-and-destruction.md) | Parallel monitors, encounter owner, device/target capability, outcomes, and cleanup |
| Release, escort, defend, carry, or place an NPC | [Rescue, escort, defend, and carry](rescue-escort-defend-and-carry.md) | Actor ownership, AI roles, ordered volumes, combat/carry state, and terminal cleanup |
| Mount, ride in, drive, or steal a vehicle | [Mount, ride, drive, and theft](mount-ride-drive-and-theft.md) | Vehicle identity, seat roles, mount conditions, route volumes, and lifecycle policy |
| Deliver, remove, chase with, or race a vehicle | [Vehicle delivery, cleanup, chase, and race](vehicle-delivery-cleanup-chase-race.md) | Vehicle state, trigger/speed observations, AI route or race systems, restrictions, and cleanup |
| Resolve an outcome, debrief, reward, and finish | [Rewards, switches, and outcomes](rewards-switches-and-outcomes.md) | Durable outcome, switch/branch, presentation, reward record, journal state, and termination |

These guides deliberately overlap at system boundaries. A plant objective, for
example, uses both the device recipe and the stealth/combat lifecycle; a
vehicle delivery may finish through the outcome/reward recipe. Follow both
guides instead of treating either page as a complete quest template.

## What each recipe supplies

Each page supplies:

- a resource and ownership checklist;
- a conceptual flow and the decisive native node or condition shapes;
- a manual WolvenKit composition order;
- named vanilla depot paths to extract from your own installation;
- exact evidence labels and boundaries for retained research;
- clean-save, reload, interruption, and cleanup cases appropriate to the
  pattern;
- failure isolation and links back to the foundational chapters.

It does not supply a universal drop-in graph, generate missing assets, or make
one vanilla node portable outside its original identities. The pages do not
redistribute extracted CR2Ws. Downloadable Labs 1–5 remain the executable
incremental reference projects; these broader recipes explain patterns whose
new combinations usually still require their own runtime campaign.

## Read in dependency order

For a multi-system quest, a reliable order is:

1. define durable facts, journal states, outcomes, and one-shot policy;
2. inventory every world, device, community, character, scene, item, and
   vehicle owner;
3. prove placement, NodeRefs, streaming bounds, identity joins, and readiness;
4. compose the smallest activity path and its authoritative completion signal;
5. add optional monitors, branching, presentation, rewards, and cleanup;
6. test each branch on an untouched save, then repeat save/load, stream return,
   interruption, failure, removal, and replay cases that can expose persistence.

Do not begin with presentation polish. A subtitle, prompt, mappin, or objective
can appear while the producing device, actor, vehicle, or condition is still
wrong.

## Evidence does not compose automatically

The four labels apply to the exact statement beside them:

- **Runtime-proven** means the bounded result was observed in game for the
  named retained arrangement and archive hash.
- **Structurally validated** means the resource serialized, round-tripped, or
  passed an explicit structural contract; it is not runtime proof.
- **Observed in vanilla** means the named extracted resource contains the
  focused shape under discussion; it is not a reusable template.
- **Experimental** is the correct status for intended behavior without a
  retained passing runtime result.

Evidence from two separate candidates does not prove their combination. A
runtime-proven meeting plus a runtime-proven device action still leaves the new
meeting-with-device quest **Experimental** until that exact composition passes.
Use the [evidence and version matrix](../reference/evidence-version-matrix.md)
and [vanilla depot-path index](../reference/vanilla-depot-paths.md) to audit the
source and environment boundary behind a claim.

## Clean-save rule

Facts, journal entries, scenes, communities, device persistent state, and some
world or vehicle state can survive ordinary reloads. When a test changes any
of those identities, close the game, install the exact candidate, and begin
from a save created before that candidate was installed or streamed. Record
the save lineage, package hash, tool/game versions, route, expected state, and
observed state. A successful run on a contaminated save is diagnostic
information, not clean-save evidence.

When a recipe has only structural or vanilla evidence, continue authoring with
that label and use its acceptance matrix to create the missing evidence. Do
not promote the intended behavior by analogy.
