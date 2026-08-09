# Entries, phases, and AI spots

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

A community entry answers three different questions:

```text
Who can spawn?        characterRecordId
In which authored mode? phaseName + appearance + time period
Where can they act?   spotNodeRefs -> worldAISpotNode -> workspot resource
```

Keeping those questions separate makes failures diagnosable. Changing the
character record does not move the spot. Moving the spot does not change the
appearance. Activating an entry with the wrong phase name does not fall back to
a similarly named workspot.

## Evidence boundary

**Observed in vanilla:** extract this focused template from your own game:

```text
base\open_world\minor_activities\westbrook\japantown\
  ma_wbr_jpn_13\community\ma_wbr_jpn_013_claws_com.community
```

It contains three `communitySpawnEntry` objects. Each entry has a character
record, entry name, phase `A`, appearance `default`, one `Day` time period,
quantity `1`, and one spot NodeRef. This observation proves that serialized
shape in that resource; it does not make its entries, spot names, phase name,
or schedule universal.

**Runtime-proven:** legacy fixture only. Archive
`2C5179349DBD1AFF5A5A01123F83FF1DC76D8D91E45FE946CEA4DCAF0166BF80`
spawned all three configured generic Tyger Claw entries at the retained cache
site. Its exact character/spot recommendation is bounded further in [Cleanup
and character safety](cleanup-and-character-safety.md).

**Acceptance-gated:** the exact `cqa005` entry name, phase, appearance, spot
placement, spawn, scene join, ordinary lifecycle, post-`contact_done` reload,
completed reload, and the named pre-scene seed loads in Cases 3, 4, and 7
follow the synchronized marker above. Workspot/cigarette animation quality,
combat or interruption behavior, arbitrary/unlisted pre-scene states, and
active-line/interruption reload remain **Experimental** out-of-matrix claims.

## Registry-side entry shape

In the retained registry item, template data has this focused shape:

```text
communityCommunityTemplateData
  entries[]
    communitySpawnEntry
      characterRecordId: TweakDBID
      entryName: CName
      phases[]
        communitySpawnPhase
          phaseName: CName
          appearances[]: CName
          timePeriods[]
            communityPhaseTimePeriod
              hour: CName-like period selector
              isSequence: Bool
              quantity: Int32
              spotNodeRefs[]: NodeRef
```

The important properties are:

| Property | Meaning in the inspected shape |
| --- | --- |
| `characterRecordId` | TweakDB record used to create the actor. It can lead to an entity template, appearances, gameplay packages, faction data, and other dependencies; it is not a world identity. |
| `entryName` | Community-local name used by activation and scene acquisition. It is a `CName`, not the actor's display name. |
| `phaseName` | Community-local mode selected by initial state or a Spawn Manager action. |
| `appearances` | Names the spawn phase can request from the selected character/template chain. |
| `hour` | Selects the authored time-period row. `Day` in one fixture is not a rule that communities only work during daytime. |
| `isSequence` | Tells this period whether its spot list represents sequenced use in the inspected model. |
| `quantity` | Requested quantity for that period; it is not a readiness timeout or scene performer count. |
| `spotNodeRefs` | Full or context-valid world references to AI spots. |

`entryActiveOnStart`, stored under the registry item's initial state rather
than the spawn entry itself, decides whether quest logic begins with that entry
active. For a controlled quest contact, `false` plus an explicit activation
edge gives the graph a reviewable owner.

## Area-side mirror

The compiled area does not repeat the character record. It repeats the
topology needed to bind the entry/phase/time period to placed spot identities:

| Registry template | Compiled area |
| --- | --- |
| `communitySpawnEntry.entryName` | `communityCommunityEntrySpotsData.entryName` |
| `communitySpawnPhase.phaseName` | `communityCommunityEntryPhaseSpotsData.entryPhaseName` |
| `communityPhaseTimePeriod.hour` | `communityCommunityEntryPhaseTimePeriodData.periodName` |
| `communityPhaseTimePeriod.isSequence` | `communityCommunityEntryPhaseTimePeriodData.isSequence` |
| `communityPhaseTimePeriod.spotNodeRefs` | `communityCommunityEntryPhaseTimePeriodData.spotNodeIds` |

The values describe the same intended route through different serialized
types. A valid character entry with a stale area mirror can activate but never
obtain its intended spot.

When reviewing serialized sectors, do not pair rows merely because they are
adjacent. Follow the entry name, phase name, full spot NodeRef, world-global
spot ID, and sector `NodeIndex`. Later source snapshots can reorder nodes or
change a workspot without changing a nearby debug string.

## `worldAISpotNode` owns the placed activity

The AI spot is a concrete world node. Its decisive focused structure is:

```text
worldAISpotNode
  isWorkspotInfinite
  isWorkspotStatic
  lookAtTarget
  spot -> AIActionSpot
    resource -> ResourcePath to .workspot
    snapToGround
    useClippingSpace
```

The sector's `nodeData` owns its transform and binds the concrete node to the
registered NodeRef. The `worldAISpotNode` owns the activity configuration. A
workspot resource supplies animation/behavior data; it does not supply the
world position.

| Concern | Owner |
| --- | --- |
| World position and orientation | The spot node's matching `nodeData` placement |
| Quest-prefab child identity | Full/local NodeRef chain and `QuestPrefabRefHash` |
| Workspot behavior | `AIActionSpot.resource` depot path |
| Finite versus continuing use | `isWorkspotInfinite` together with the community period design |
| Ordered movement between spots | A validated sequence using `isSequence`, multiple spot identities, and compatible AI behavior |
| Actor selection | `communitySpawnEntry.characterRecordId` |

Do not introduce a patrol merely by adding two points. Sequenced workspots,
AI roles, navigation, interruption, combat, and cleanup are separate runtime
surfaces. A single stationary contact spot is the smaller Lab 5 search surface.

## Character record, entity, and appearance are separate

The community stores a `TweakDBID`, for example:

```text
Character.jpn_tyger_claws_biker2_ranged2_copperhead_wa
```

That record is not an `.ent` depot path. It can refer onward to a character
entity template and other gameplay records. The spawn phase's appearance
`CName` must be valid for the selected template chain. An appearance name that
worked for a different record is not inherited because both entries say
`default`.

For a first contact fixture, prefer a generic population/combat record whose
bounded spawn behavior is retained over a story-unique character record. This
reduces conflict with vanilla quest ownership, but it does not make every
appearance, faction, voice, or AI behavior appropriate. Inspect the selected
record and verify the actor in game.

## Choosing a workspot

Choose a workspot from evidence tied to the exact record and candidate, then
validate it at the new placement. Check:

1. the resource exists at the exact depot path;
2. the spot transform leaves enough clearance for the actor;
3. the surface is reachable and supports the intended ground contact;
4. the actor does not clip into walls, props, or the player approach lane;
5. the broad setup route streams the area before the scene needs the actor;
6. each named pre-scene seed load in Cases 3, 4, and 7 reacquires the same
   passive contact without duplication;
7. normal exit, post-`contact_done` reload, completed reload, and delayed
   deactivation do not leave the actor stuck in the workspot.

A workspot proven at one transform is not a navmesh guarantee at another. The
later
`base\workspots\common\ground\generic__stand_ground__guard__02.workspot`
source/runtime lineage belongs to a different retained candidate and is not
the workspot byte-bound to archive `2C517934...`. Separate
`base\workspots\patrolling\guard_stand.workspot` research likewise does not
replace the exact `cqa005` contact spot.

## Common failures

| Symptom | Inspect first |
| --- | --- |
| Entry activates but uses the wrong actor | `characterRecordId`, entry name, registry item, and saved activation history |
| Actor is invisible or malformed | Requested appearance, record-to-entity path, dependencies, and expansion requirements |
| Actor appears at an unexpected sibling spot | Registry `spotNodeRefs`, area `spotNodeIds`, and world-global ID uniqueness |
| Actor clips or faces away | Spot `nodeData` position/orientation, workspot semantics, clearance, and navmesh |
| Sequence never advances | `isSequence`, finite/infinite settings, spot ordering, AI behavior, and navigation evidence |
| Scene asks for an entry that exists only in another community | Scene community reference and entry `CName`; entry names are community-local |

Next: [Activation, readiness, and
acquisition](activation-readiness-and-acquisition.md).
