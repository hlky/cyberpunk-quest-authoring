# Journal, UI, and localization

The journal is the game's player-facing record of quest state. It owns quest
titles, objectives, descriptions, contacts, messages, documents, and map-pin
entries. It does not decide when those entries change, create their world
targets, resolve every kind of text, or grant rewards by itself.

| Record | Value |
| --- | --- |
| Section review date | 2026-08-09 |
| Practical baseline | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Mod-owned reference | `cqa001` / **First Signal** |
| Reference status | Lab 1 journal and onscreen resources are **Structurally validated** |

> **Scope note:** this section distinguishes the structurally validated
> Lab 1 resources, focused structures **Observed in vanilla**, legacy
> **Runtime-proven** research fixtures whose environment is not identical to
> the pinned book baseline, and untested combinations that remain
> **Experimental**. A legacy run never silently promotes a new tutorial
> resource.

Where a chapter cites a legacy fixture as **Runtime-proven**, the surviving
records variously name WolvenKit `8.17.4` for mod-owned fixture resources,
ArchiveXL `1.27.0`, and, where relevant, TweakXL `1.11.3`. Separate focused
vanilla-extraction notes name WolvenKit `8.17.4-nightly.2026-03-20`. They do
not bind one uniform game and RED4ext environment. Those values are research
provenance, not the reader baseline and not proof that a new tutorial resource
works on the pinned versions.

## Keep the owners separate

A journal entry is data. A quest graph requests a state change. A localization
resource supplies display text. A streamed world resource supplies the object
or marker that a journal mappin can target. A reward node resolves a TweakDB
record. Those responsibilities meet through typed paths and identifiers:

```text
ArchiveXL journal registration
          |
          v
gameJournalResource tree <--- gameJournalPath --- quest journal node
          |                                           |
          | LocalizationString                        | state input socket
          v                                           v
onscreen localization ----------------> player-facing journal presentation

journal mappin -- NodeRef --> streamed world node
reward node ----- TweakDBID -> reward record

scene line RUID --+--> subtitle map ----> subtitle text
                  +--> voiceover map ---> WEM audio
scene option ID --> screenplay option --> locStore --> displayed choice text
```

The arrows are lookup boundaries, not an execution graph. For example, a valid
objective path does not activate itself, and a valid mappin entry cannot make
an unresolved world `NodeRef` exist.

## Read the section in dependency order

| Chapter | Question it answers |
| --- | --- |
| [Trees and paths](trees-and-paths.md) | How is a `.journal` resource built, merged, and addressed? |
| [Quest state](quest-state.md) | Which entry types and graph operations produce active, inactive, succeeded, failed, tracked, and visited state? |
| [Mappins](mappins.md) | Which data belongs to the journal, and where does the streamed-world boundary begin? |
| [Messages and onscreens](messages-and-onscreens.md) | How do contacts, phone choices, files, emails, and readable entries differ? |
| [Localization paths](localization-paths.md) | Why do UI text, spoken lines, and scene choices use three unrelated lookup chains? |
| [Rewards and completion](rewards-and-completion.md) | How do payout, the completion fact, journal success, and phase termination remain independent? |

Read [Trees and paths](trees-and-paths.md) and [Quest state](quest-state.md)
before changing Lab 1. The other chapters introduce dependencies that First
Signal deliberately omits.

## One path has several contracts

Consider Lab 1's objective address:

```text
quests/minor_quest/cqa001/cqa001_01/cqa001_01_obj_wait
```

That string is useful only when all of the surrounding contracts agree:

| Contract | Lab 1 value |
| --- | --- |
| Registered journal resource | `mod\cqa\cqa001\journal\cqa001.journal` |
| Entry chain | primary folder → folder → quest → phase → objective |
| Expected leaf type | `gameJournalQuestObjective` |
| `gameJournalPath.className` | `gameJournalQuestObjective` |
| `gameJournalPath.fileEntryIndex` | `2`, identifying the containing quest file entry in this path family |
| Requested state | The journal node's connected `Active` or `Succeeded` input socket |
| Visible text key | `cqa_cqa001_objective_wait` |
| Registered text resource | `mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json` |

Changing only the path string cannot repair the wrong leaf type, missing merge,
wrong state socket, or unresolved localization key. Diagnose those layers
separately.

## State is save-backed

Journal activation, success, visited flags, tracking, graph checkpoints, and
supporting facts can be serialized in a save. They are not one resettable
variable. This affects every practical experiment in this section:

- start a first acceptance run from a save made before the mod was installed;
- preserve separate slots for active, visited, and completed states;
- return to the original pre-install save when changing journal IDs or tree
  shape;
- treat a console fact edit as diagnosis, never as a clean journal reset;
- use a fresh save or fresh world identity when a test also changes a streamed
  device or mappin target.

The complete procedure is in [Install, test, and reset](../start-here/install-and-test.md).

## How to verify these resources

The chapters cite exact depot paths rather than shipping extracted game files.
Use a disposable inspection project and the procedure in
[Inspect a vanilla questphase](../start-here/inspecting-vanilla.md) to examine
only the focused properties needed for a claim. Principal references include:

- `base\journal\cooked_journal.journal` for journal entry families;
- `base\journal\descriptor.journaldesc` for the standard descriptor contract;
- `base\quest\side_quests\sq021\phases\sq021_randys_room.questphase` for a
  computer-document fact handoff;
- `base\open_world\street_stories\watson\kabuki\sts_wat_kab_05\phases\sts_wat_kab_05_openworld.questphase`
  for a native reward node.

These are **Observed in vanilla** reference paths. Do not add them to a
tutorial archive, publish their cooked binaries, or paste their complete
serializations into a chapter.

## Scope boundary

This section explains journal data, graph operations, lookup chains, and their
immediate consumers. It does not teach complete device packages, streaming
sectors, scene graphs, audio production, or custom TweakDB reward records.
Those systems are named where the boundary matters and developed in their own
sections. Lab 1 remains intentionally small: it needs only a questphase, one
journal tree, one onscreen localization resource, and ArchiveXL registration.
