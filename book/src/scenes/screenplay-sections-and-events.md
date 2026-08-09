# Screenplay, sections, and events

**Lab 5 runtime evidence:** **Experimental** — pending.

**Acceptance gate:** Exact `cqa005` claims covered by the frozen eleven-case
matrix follow the synchronized marker above: pending or failed means
**Experimental**; passed means **Runtime-proven**. Legacy evidence and
out-of-matrix claims retain their own labels. Cases 3, 4, and 7 load distinct
full-slot copies of the named `seed-pre-scene-outside-setup` capture; those
exact loads are in-matrix. Arbitrary or unlisted pre-scene states and
active-line/interruption reload remain out-of-matrix.

One spoken line spans three native objects. The screenplay item says who speaks
and which localization ID to resolve. A timed event schedules that item. A
section owns the event and determines when graph flow can leave.

```text
screenplayStore.lines[0]
  scnscreenplayDialogLine item 1
          ^
          | screenplayLineId 1
  scnDialogLineEvent, start 0, duration 2598 ms
          |
          v
  scnSectionNode 2, sectionDuration 2998 ms
```

Removing any layer produces a different resource: a screenplay row alone is
not scheduled, an event with an unresolved item ID has no line definition, and
a section duration that ends too early can cut off its event.

## The screenplay line

First Contact's `scnscreenplayStore.lines` contains exactly one
`scnscreenplayDialogLine`; its `options` array is empty:

```json
{
  "$type": "scnscreenplayDialogLine",
  "itemId": { "$type": "scnscreenplayItemId", "id": 1 },
  "speaker": { "$type": "scnActorId", "id": 0 },
  "addressee": { "$type": "scnActorId", "id": 1 },
  "locstringId": {
    "$type": "scnlocLocstringId",
    "ruid": "9638591835734011695"
  },
  "usage": {
    "$type": "scnscreenplayLineUsage",
    "playerGenderMask": { "$type": "scnGenderMask", "mask": 3 }
  }
}
```

Actor `0` is the contact and actor `1` is V. Gender mask `3` is the exact
line-usage value in this checkpoint. It sits beside male and female lipsync
animation names set to `None`; it does not select the subtitle resource or
replace the actor definitions.

The line stores no English sentence. Its RUID
`9638591835734011695` resolves to `All clear. Keep moving.` through external
subtitle and VO resources. Consequently the scene's
`scnlocLocStoreEmbedded` can remain typed and empty. Embedded locStore payloads
are for scene-owned localized data such as choice labels, not this line's
external spoken-text path.

## The timed line event

Section node `2` contains exactly one handled `scnDialogLineEvent`:

| Property | Exact value |
| --- | --- |
| `screenplayLineId` | `scnscreenplayItemId` `1` |
| `id` | `scnSceneEventId` `8646165628675208917` |
| `startTime` | `0` |
| `duration` | `2598` ms |
| `visualStyle` | `regular` |
| `voContext` | `Vo_Context_Quest` |
| `voExpression` | `Vo_Expression_Spoken` |
| `additionalSpeakers.speakers` | `[]` |

The event points to screenplay item `1`; it does not point directly to the
locstring. Event ID `8646165628675208917` and locstring RUID
`9638591835734011695` are intentionally different unsigned identifiers. Keep
both as unsigned decimal values through tooling and comparison. Do not derive
one from the other, reuse a graph node ID, or truncate either to 32 bits.

The event duration is aligned to the supplied audio's measured duration for
this fixture. It is not inferred from subtitle character count.

## The section

`scnSectionNode` `2` owns the event and two output sockets:

```text
Section 2
├── actorBehaviors
│   ├── actor 0: OnlyIfAlive
│   └── actor 1: OnlyIfAlive
├── events
│   └── DialogLineEvent: item 1, 2598 ms
├── sectionDuration: scnSceneTime(stu = 2998)
├── output stamp name 0 / ordinal 0 -> End 3 input 0 / 0
└── output stamp name 1 / ordinal 0 -> no destination
```

For First Contact, the section-duration contract is:

```text
2598 ms line duration + 400 ms tail = 2998 ms section duration
```

The 400 ms tail is a deliberate lab value that lets the line finish before the
section reaches End. It is not claimed as a universal engine constant. For
multiple or overlapping events, calculate the latest event end and add an
appropriate tested tail instead of adding 400 ms blindly to every line.

Output stamp `0/0` is the normal completed route. Output stamp `1/0` is an
explicit cancel-shaped socket with no destination in this minimal scene. A
named quest exit is attached to End node `3`, not to the screenplay line or
event itself.

## Keep the ID domains separate

| Typed domain | First Contact value | Identifies |
| --- | ---: | --- |
| `scnActorId` | `0`, `1` | Contact and V |
| `scnPerformerId` | `1`, `257` | Debug performer symbols |
| `scnNodeId` | `1`, `2`, `3`, `4` | Start, Section, End, PuppetAI wrapper |
| `scnscreenplayItemId` | `1` | The line definition and event-to-line join |
| `scnSceneEventId` | `8646165628675208917` | The timed event instance |
| `scnlocLocstringId` | `9638591835734011695` | External subtitle and voice lookup |
| `scnLipsyncAnimSetSRRefId` | `0` | Index into the lipsync resource-reference array |

The repeated integer `1` across several rows is coincidence plus a deliberately
small fixture. See [Identifier domains](../foundations/identifier-domains.md)
before comparing raw exports.

## Evidence boundary

The screenplay-item/event/section layering, typed IDs, external spoken-line
localization, and comparable section graph arrangements are **Observed in
vanilla** at the cited `mq003`, `mq007`, and `mq010` paths. The exact First
Contact one-line section, ID joins, and `2598 + 400 = 2998` timing are
**Structurally validated**. Ordinary playback, exact subtitle/WEM lookup,
performer acquisition through the line, and normal completion in the exact
`cqa005` package follow the synchronized marker above. Per-frame timing,
facial/animation quality, active-line interruption and return, and
`CutDestination` behavior remain **Experimental** outside that campaign.

Previous: [Actors and performers](actors-and-performers.md). Next: [Entry,
exit, and quest handoff](entry-exit-and-quest-handoff.md).
