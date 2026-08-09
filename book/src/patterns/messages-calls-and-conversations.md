# Messages, calls, and conversations

Use a journal thread for text, a phone operation for call state, and a scene
for performed dialogue. These systems can appear in the same player-facing
conversation, but they have different resource owners and completion signals.

| Record | Value |
| --- | --- |
| Guide review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Journal and phone resource shapes | **Observed in vanilla** |
| Legacy GQ000 text route | **Runtime-proven** only for the exact retained candidate named below |
| Legacy GQ002 offer/conversation resources | **Structurally validated**; their planned two-route behavior remains **Experimental** |
| A new custom text or call flow on the pinned baseline | **Experimental** until its own clean-save campaign passes |

This page composes the native pieces taught in
[Messages, files, emails, and onscreens](../journal/messages-and-onscreens.md).
It does not require a generator or a manifest compiler, and it does not turn a
voiced holocall into a text-message recipe.

## Choose the presentation owner first

| Player experience | Primary owner | Questphase responsibility | Additional assets |
| --- | --- | --- | --- |
| One-way text | `gameJournalPhoneMessage` beneath a contact conversation | Activate the message in the intended order | Journal contribution and onscreen localization |
| Text offer or reply menu | `gameJournalPhoneChoiceGroup` and `gameJournalPhoneChoiceEntry` | Activate the group, observe the winning entry, and persist the result | Same journal and localization owners |
| Audio call state | `questPhoneManagerNodeDefinition` | Start or end a call for two journal contacts | Both contact paths; phone restrictions must be deliberate |
| Voiced holocall | `.scene` launched by `questSceneNodeDefinition` | Coordinate the call and consume a named scene result | Scene, actor/context bindings, subtitles, VO map, WEMs, and any lipsync resources |
| In-person conversation | `.scene` plus a ready actor/community | Acquire the actor, start the scene, consume its named exit, then clean up | Community, AI spot, placement marker, scene, localization, audio |

A journal contact can own text messages without being a complete callable
contact. Adding a contact, starting a call, playing a scene, and activating a
message are separate operations. Keep those boundaries visible in the graph.

## Shared prerequisites

Before wiring any recipe on this page, create and inspect:

1. a mod-owned `.journal` contribution containing the contact, conversation,
   messages, choice groups, and choice entries used by the route;
2. globally unique onscreen localization keys for every contact name, thread
   title, message, and choice label;
3. ArchiveXL registration for the journal and onscreen localization resources;
4. a mod-owned `.questphase` with explained input, output, and cut sockets;
5. separate facts for presentation sent, player response, and activity
   completion when those meanings differ;
6. an untouched save created before the custom journal identities were
   installed.

For a voiced route, also finish the prerequisites in
[Scene resource anatomy](../scenes/resource-anatomy.md),
[Actors and performers](../scenes/actors-and-performers.md), and
[Entry, exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md).
A `.scene` reference does not synthesize actors, subtitle maps, audio, or phone
state.

## Recipe: send an ordered text sequence

The smallest sequence activates one journal entry at a time:

```text
In1
 -> sent == 0?
      False -> Out1
      True  -> message 1 Active
             -> message 2 Active
             -> set sent = 1
             -> Out1
```

Use `questJournalNodeDefinition` with a
`questJournalEntry_NodeType` for each message. The decisive fields are:

| Field | Required meaning |
| --- | --- |
| `type.path.className` | `gameJournalPhoneMessage` |
| `type.path.realPath` | Full path to exactly one message |
| `type.path.fileEntryIndex` | Index of the containing contact in the path; commonly `1`, but calculate it |
| `type.sendNotification` | Whether this activation should request phone presentation |
| incoming socket | `Active` |
| outgoing socket | `Out` means the activation request continued, not that the message was read |

The message entry's own `delay` participates in phone presentation. A graph
`questRealtimeDelay_ConditionType` is a different owner: it delays execution.
Do not add an arbitrary graph delay and then describe it as proof that the
player saw the earlier message.

Protect a one-shot sequence with a persistent fact and an already-sent bypass.
Write the fact at the boundary whose meaning it names. If it means “the opening
messages were requested,” write it after their activation. If it means “the
player acknowledged the exchange,” write it only after the acknowledgement
gate.

**Observed in vanilla:** the compact thread at
`contacts/dex/q003_flathead_price` inside
`base\journal\cooked_journal.journal` contains a message, a one-choice group,
and a following message with the expected entry properties. It proves the
journal hierarchy, not a new mod-owned questphase.

**Structurally validated:** Ghostline research commit
`5f0e0d5558c35b0fe58b9dd732d4039c91e9c2eb` retains the GQ002 source phases.
The phone-related cooked resources match the retained final-polish build whose
archive SHA-256 is
`E37C3498B0AF0EE01697C4542D579252DE844E4D529F6381EDAF0D0CFCA1BF94`.
Its runtime section is the active next-test checklist, not a retained result.
The serialized source reports WolvenKit `8.17.4`; it is not a pinned
WolvenKit `8.19.0` compatibility result. Ordered presentation for that exact
candidate therefore remains **Experimental**.

## Recipe: make a one-choice text job offer

The retained GQ002 offer uses this native shape:

```text
In1
 -> opening message Active
 -> accept-choice group Active
 -> set offer_sent = 1
 -> wait until the accept choice is visited
 -> set offer_accepted = 1
 -> Out1
```

| Step | Native node and decisive payload |
| ---: | --- |
| 1–2 | `questJournalNodeDefinition` → `questJournalEntry_NodeType`, entered through `Active` |
| 3 and 5 | `questFactsDBManagerNodeDefinition` → `questSetVar_NodeType`, `setExactValue: 1`, `value: 1` |
| 4 | `questPauseConditionNodeDefinition` → `questJournalCondition` → `questJournalEntryVisited_ConditionType` |
| 6 | Normal external child output such as `Out1` |

The wait path must address the individual
`gameJournalPhoneChoiceEntry`, not its group. The exact retained one-choice
offer used a visited condition. The multi-choice conversations below instead
route on each entry's `Succeeded` state. Both shapes exist in the evidence;
do not assume that `Active`, `visited`, and `Succeeded` are interchangeable.

The accepted fact is a handoff, not the whole quest. A following phase should
activate the quest, objective, description, and mappin that the offer promises.
See [Journal state and tracking](../journal/quest-state.md). Keep the quest
inactive if the design intentionally allows a declined offer, and give that
route an explicit output instead of leaving an active listener behind.

The GQ002 candidate named above is **Structurally validated** for the exact
node/path shape. Its checklist asks the tester to confirm that the offer
appears and `On my way.` activates the meeting objective, but it does not
retain that result. Those runtime claims, decline handling, repeatable offers,
and behavior under the pinned versions remain **Experimental**.

## Recipe: route a two-choice text conversation

Use one wait per choice, one reply per branch, and an explicit convergence:

```text
common message(s) Active
 -> choice group Active
    +-> wait choice A Succeeded -> reply A Active -> set outcome_a = 1 --+
    `-> wait choice B Succeeded -> reply B Active -> set outcome_b = 1 --+
                                                                       |
                              two-input XOR-shaped convergence <-------+
                                           -> final message Active
                                           -> acknowledgement gate
                                           -> Out1
```

| Concern | Native representation |
| --- | --- |
| Winning choice | `questJournalEntryState_ConditionType`, `state: Succeeded`, individual `gameJournalPhoneChoiceEntry` path |
| Branch response | One `questJournalNodeDefinition` entered through `Active` |
| Durable outcome | One branch-specific fact writer before convergence |
| Convergence | Two-input `questLogicalXorNodeDefinition`, with both inputs and `Out1` inspected |
| Required acknowledgement | `questJournalEntryVisited_ConditionType`, `visited: 1`, final message path |

The branch facts must be mutually exclusive. The retained XOR-shaped route
does not establish that a logical XOR cancels a losing wait. If both choice
facts can become true, a later signal may reach supposedly finished logic;
that behavior is **Experimental**. Persist the winner at the choice boundary,
and make a late losing signal harmless or explicitly cut it.

The GQ002 candidate above is **Structurally validated** for two selected-state
waits, matching replies, result facts, and convergence. Its checklist planned
both routes; it is not runtime proof for either result. Separately, Ghostline
research commit `97b5c5330acfc259bc1e5b814a83b7902cbd70bf`, archive SHA-256
`1C669335E83C93F714455D24743C7F03E34F2FA381A60ABB9E8F35A85375EDCC`,
is **Runtime-proven** for a complete GQ000 route containing phone choices and
completion presentation after its final-message gate. Combining pieces from
the two fixtures into a new conversation remains **Experimental** until that
exact combined resource passes.

## Text is not a holocall

A performed call adds both phone lifecycle and scene lifecycle. Two vanilla
references make the boundary concrete:

- **Observed in vanilla:**
  `base\quest\side_quests\sq004\phases\sq004_03_raffen_shiv_camp.questphase`
  contains `questPhoneManagerNodeDefinition` operations whose nested
  `questCallContact_NodeType` uses `caller`, `addressee`, `mode: Audio`, and
  distinct `StartCall` or `EndCall` phases.
- **Observed in vanilla:**
  `base\quest\side_quests\sq011\phases\sq011_concert.questphase` launches
  `base\quest\side_quests\sq011\scenes\sq011_09_nancy_call.scene` through a
  `questSceneNodeDefinition`. The retained scene node has a soft `sceneFile`,
  a tagged `scnWorldMarker`, named scene inputs/outputs, `Holocall INT`,
  `Holocall RET`, and `Prefetch`. A nearby `questPhone_ConditionType` records
  caller, addressee, and `callPhase: IncomingCall`.

Those are focused resource observations, not a universal wiring diagram. A
safe planning shape is:

```text
phone availability/restriction gate
 -> StartCall operation
 -> questSceneNodeDefinition named input
 -> consume the intended named scene result
 -> EndCall operation
 -> persist result and continue
```

| Owner | What must be authored and tested |
| --- | --- |
| Phone operation | Correct caller/addressee `gameJournalContact` paths, mode, phase, restriction, rejectability, avatar/visual settings |
| Scene node | Exact `.scene` depot path, location/context, input socket, every completion/rejection/interruption output |
| Scene | Actors, screenplay, sections, events, named exits, and cleanup |
| Localization/audio | Spoken-line IDs, subtitle entries and map, VO map, WEMs, lipsync slot/resource contract |
| Quest | What rejection, interruption, reload, and an already-busy phone do |

No book-owned custom holocall has a retained pinned-baseline acceptance run.
The assembled custom-call recipe is therefore **Experimental**. Start with a
text thread or the one-line in-person scene unless the quest genuinely needs
phone performance. For the scene half, follow
[Author one spoken line](../scenes/one-spoken-line.md) rather than copying a
vanilla call scene.

## Author and inspect in WolvenKit

1. Build the journal tree and localization resource first. Reopen both and
   verify every full path and secondary key.
2. Add the questphase journal nodes. Set concrete entry classes,
   `fileEntryIndex`, notification flags, and incoming state sockets.
3. Wire the sequence by socket identity. Screen position is not execution
   order.
4. Add one persistent sent guard and separate branch/completion facts. Avoid a
   single fact whose meaning changes halfway through the flow.
5. For multiple choices, fan out to individual state waits, write the result
   on each branch, and converge only after the matching reply.
6. For a required acknowledgement, wait on the final message's visited state.
   Do not treat a journal node's `Out` as acknowledgement.
7. Save, reopen, serialize a focused review copy, and resolve every node,
   socket, condition handle, and journal path.
8. Pack and inspect framework logs before beginning runtime diagnosis.

## Clean-save acceptance

Phone entries, visited flags, choice states, facts, scenes, and phone lifecycle
can all be save-backed. Retain separate cases for:

1. first install on an untouched save;
2. save and reload before the opening message;
3. save with the choice group active;
4. one run for every choice from the same untouched baseline;
5. save after the reply but before required final acknowledgement;
6. completed-save reload and re-entry attempt;
7. removal isolation from the original pre-install save;
8. for calls, reject/interruption, save during the call, and phone-busy cases.

Record archive and loose-file hashes, save provenance, selected choice,
journal state, facts, and fresh ArchiveXL/RED4ext/redscript logs. Resetting one
fact does not clear a visited message or an active call.

## Failure routing

| Symptom | Inspect first |
| --- | --- |
| Contact or message never appears | Journal registration, full path, entry class, `fileEntryIndex`, localization registration |
| Message appears twice | Sent guard timing, duplicate root entry, completed-save re-entry |
| Choice group appears but never advances | Wait path points to the group instead of the individual choice, or wrong state dimension |
| Both replies appear | Branch conditions, mutual-exclusion facts, and convergence wiring |
| Final message appears after completion | Completion used activation or a pacing delay instead of the intended visited gate |
| Call UI starts but no dialogue plays | Phone operation succeeded while scene input, actor/context, subtitle, VO, or WEM ownership failed |
| Dialogue ends but phone remains busy | Missing or unreachable `EndCall`, rejected/interrupted output not handled |
| Only one save behaves incorrectly | Saved journal, phone, scene, or fact state; repeat from the untouched baseline |

Keep the evidence terms narrow: the exact GQ000 archive is
**Runtime-proven** for its recorded route, the GQ002 resource/build shape is
**Structurally validated** while its planned behavior remains
**Experimental**, and the named base-game shapes are **Observed in vanilla**.
Every new custom arrangement remains **Experimental** until its own retained
run passes.
