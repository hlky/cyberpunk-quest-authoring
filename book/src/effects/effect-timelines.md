# Effect timelines

A `.effect` resource schedules presentation. Its length is not the duration of
the gameplay status that requested it. A six-second status can keep a short
visual loop active, then let an outro play when the loop breaks.

Use the [custom-effects toolchain](index.md#tools-and-versions) and begin with
one particle track before building an animated sequence.

## Read the timeline resource

**Observed in vanilla:** inspect
`base\fx\player\p_hacking_glitch\p_hacking_glitch_low.effect` in WolvenKit.
The root type is `worldEffect`.

| Property or type | Owns |
| --- | --- |
| `worldEffect.length` | Total authored timeline length, including the outro |
| `trackRoot` → `effectTrackGroup` | Collection of tracks |
| `effectTrack.items` | Handled timeline items |
| `worldEffect.events` | References to the same item objects used by tracks |
| `effectTrackItemParticles` | A timed particle resource invocation |
| `effectTrackItemLoopMarker` | The timeline's loop-marker item |
| `effectLoops[]` → `effectLoopData` | Loop start/end times |
| `effectTrackItemSound` | A timed audio event request |

Do not create unrelated copies of an event in the track and root event list.
They must reference the same object. Keep CR2W handles separate from the
event's unsigned `ruid`.

## Separate the three clocks

| Clock | Example | Setting |
| --- | --- | --- |
| Gameplay duration | Six seconds of an optics status | TweakDB duration record |
| Presentation timeline | Intro, repeating motion, outro | `.effect` times and loop range |
| Particle lifetime | How long one spawned frame survives | Authored and compiled `.particle` simulation |

For a short animated effect, this is a useful starting layout:

```text
timeline seconds: 0        0.2                     1.0          1.6
                 | intro  |  repeating motion      |  outro     |
                          +-----------------------+
                          loop range

status active -> presentation repeats the loop
normal stop   -> break loop -> finite outro -> finished
```

The intro is outside the loop. The outro and any one-shot exit sound are also
outside it. Setting `worldEffect.length` to six seconds would instead change
the presentation layout; it would not configure a six-second gameplay status.

## Author one particle track in WolvenKit

1. Create or open a mod-owned `.effect` with a `worldEffect` root and PC
   cooking target. Inspect the reference's group, track, and event types.
2. Add an `effectTrack` beneath the root group. Add a handled
   `effectTrackItemParticles` to its `items` array.
3. Set `particleSystem` to the exact archived `.particle` depot path.
4. Set `timeBegin` and `timeDuration`. These timeline values use seconds;
   do not copy millisecond values from a scene dialog event.
5. Give the item a unique `ruid`. Add the matching object reference to the
   root `events` array rather than constructing another item with the same ID.
6. Inspect `alpha`, `emissionScale`, `size`, and `velocity`. The constant-value
   setup uses `effectEffectParameterEvaluatorFloat` with a
   `CEvaluatorFloatConst` evaluator of `1.0` for each. A zero alpha or emission
   scale can hide otherwise valid particles.
7. Set the root length to cover the item, save, and reopen it. Check the track,
   item reference, particle path, evaluators, and RUID.
8. Bind the event to a placement in the
   [entity descriptor](entity-spawners-and-status-effects.md#bind-events-to-a-placement).

For the first game check, use a single visible track and verify removal. A
timeline item ending does not establish that an incompatible long-lived
particle disappears with it.

## Add the loop and outro

1. Put intro tracks before `0.2` seconds.
2. Add a loop marker beginning at `0.2`, lasting `0.8` seconds.
3. Set the corresponding `effectLoopData.startTime` to `0.2` and `endTime`
   to `1.0`. Keep the marker and loop table consistent.
4. Place the motion tracks entirely within that interval.
5. Put finite outro tracks at or after `1.0`. Set the root length to the
   latest outro event's end.
6. Test normal expiry, early removal, and reapplication. Normal loop break and
   an immediate effect stop can produce different cleanup behavior.

Loop-break, immediate-stop, and overlapping reapplication behavior are
**Experimental** for a new effect. Design the gameplay owner to use the
intended stop route, then test that route explicitly.

## Animate images with tracks

Motion can be drawn into a sequence of original texture frames. Each frame
has a particle resource, and the effect timeline selects them in order. This
is texture animation; scattered pixels drawn into successive frames are not
independent physics particles.

For eight motion frames over `0.8` seconds:

| Frame | Begin | Duration | End |
| --- | ---: | ---: | ---: |
| `hold_00` | `0.2` | `0.1` | `0.3` |
| `hold_01` | `0.3` | `0.1` | `0.4` |
| … | … | … | … |
| `hold_07` | `0.9` | `0.1` | `1.0` |

The intro can occupy `0.0–0.2`. Twelve outro frames at `0.05` seconds each
occupy `1.0–1.6`, so the root length is `1.6`.

Prepare the [compiled particle lifetime](particles-and-materials.md#check-cooked-size-and-lifetime)
for each interval. Timing a `0.1`-second track does not rewrite a particle's
baked lifetime. Check for gaps, overlapping old frames, and a visible jump at
the last-to-first loop boundary.

For separate opaque and glowing layers, give each layer its own particle
track at the same frame times. Use separate material instances; a shared
material cannot give each layer independent blend settings.

## Put a one-shot sound after the loop

Add an `effectTrackItemSound` after the loop end. Set its `eventName` to an
available game audio event, and keep its `positionName` consistent with the
effect's placement setup. `ui_fx_hacking_glitch_fullscreen_low` is an example
of an existing electronic event name; it is not a WEM depot path.

For a loop ending at `1.0`, a sound beginning at `1.005` stays outside the
repeating interval. Give the sound its own RUID and compiled placement row.
Listen in game: a valid event name alone does not establish audibility,
spatialization, or one-time playback. Audio behavior here is **Experimental**.

Next: [Entity spawners and status effects](entity-spawners-and-status-effects.md).
