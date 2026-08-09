# Facts, journals, and saves

A quest graph does not start from a blank state every time an archive changes.
Facts, journal state, active quest work, checkpoints, scenes, communities, and
devices can outlive the game session that created them.

That makes the save part of the test input.

## Facts are integer state

Quest facts are signed integer values addressed by name. In the tested quest
fixtures, an unset fact reads as `0`.

Common conventions:

| Value shape | Meaning chosen by the author |
| --- | --- |
| `0` / `1` | false/true, not started/completed, inactive/active |
| increasing integer | stage number, counter, or threshold |
| distinct named facts | independent events that must not overwrite each other |

The engine does not know that `_completed` means completion. The graph gives
the value meaning by deciding when to read and write it.

Prefer event-specific names:

```text
cqa001_completed
cqa002_offer_sent
cqa002_job_accepted
```

One overloaded `quest_state` fact makes re-entry and failure diagnosis harder
because unrelated transitions erase one another.

## Snapshot and wait semantics

The same fact comparison can support two behaviors:

```text
Condition:
    evaluate cqa001_completed == 0 now
    choose True or False

PauseCondition:
    hold this path until cqa001_completed == 0
```

Choose the node according to control semantics, not according to the fact
family.

## One-shot protection

Lab 1 uses:

```text
if cqa001_completed == 0:
    run quest
else:
    terminate
```

The fact is set before the quest reaches its successful terminating output. On
the next root evaluation, the `False` branch terminates without reactivating the
journal.

Runtime testing must still cover interruption between the fact write and quest
completion. A graph that looks one-shot on the happy path can expose partial
state after a save, crash, reload, or cut.

## Journal state is also persistent

Journal entries can retain states such as inactive, active, succeeded, or
failed. Some entry families also retain visited state.

These are separate questions:

- Is the entry active?
- Has the player visited or opened it?
- Has its objective succeeded?
- Is the quest currently tracked?

Do not substitute a visited condition for an objective state or assume that
activating an entry proves the player saw its presentation.

## Other save-backed systems

Research fixtures have demonstrated persistence involving:

- quest facts;
- journal activation and visited state;
- active questphase branches and checkpoints;
- scene state;
- community and actor lifecycle;
- device persistent state associated with a NodeRef.

A newly packed CR2W resource cannot erase the older state already stored in a
save. Device tests may require both a clean save and a fresh NodeRef identity
when deliberately invalidating a previous device instance.

## What “clean save” means

For a focused quest start test, use a manual save created before any version of
that quest mod was installed or registered.

Avoid:

- an autosave created after the quest first activated;
- a save made after a failed graph or scene probe;
- a save where the journal entry was already visited;
- a save that streamed an older version of a persistent device.

Resetting one fact is useful for diagnosis, but it does not clear every journal,
checkpoint, scene, community, or device record. A console reset is therefore
not equivalent to a clean save.

## Minimum save test matrix

For a one-shot quest:

1. **First load:** start from the known pre-mod save and observe activation.
2. **Mid-flow reload:** save while the objective is active, reload, and record
   whether the intended node resumes.
3. **Completed reload:** save after completion, reload, and verify no
   reactivation.
4. **Reinstall same build:** prove that reinstalling does not change the result
   already stored in the save.
5. **Clean replay:** return to the original pre-mod save for another first-run
   pass.

Record which save was used with the archive hash and test result. “Works on my
save” is not enough evidence to reproduce a lifecycle claim.
