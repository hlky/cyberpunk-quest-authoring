# Install, test, and reset

Install Lab 1, check that First Signal appears and completes, then test reload
and replay from separate saves. This guide works with either your authored
start project or the supplied completed checkpoint.

| Record | Value |
| --- | --- |
| Target environment | Cyberpunk 2077 `2.31a`, WolvenKit `8.19.0`, ArchiveXL `1.27.0`, RED4ext `1.30.0`, redscript `0.5.31` |
| Supplied resource status | **Structurally validated** |
| In-game result | Record it while following the save matrix below |
| Runtime test date | Not yet recorded |

The expected results below remain **Experimental** until observed in game.
Keep notes of what actually happens, including failures or cases you cannot run.

## Prepare an untouched save

The completion fact, journal state, and active graph state live in the save.
Create or identify a manual save made before any version of `cqa001` was
installed or registered. Keep that save as an immutable baseline and make new
save slots for test cases.

A useful label in your test notes is:

```text
cqa001-clean-baseline — manual save created before first cqa001 install
```

Removing the mod after it has run does not erase state from a save. Setting
`cqa001_completed` back to `0` with an optional console may help diagnose one
branch, but it does not clear journal entries, quest checkpoints, scene state,
communities, or devices. A fact edit is therefore never a clean-save result,
and no console mod is required by this guide.

See [Facts, journals, and saves](../foundations/persistent-state.md) for the
state model behind this rule.

## Install the completed checkpoint

If you just installed your authored start project, keep that installation and
continue with the file and log checks below. Its archive is
`CQA_Lab01_OneShot_Start.archive`; the loose registration file is still
`CQA_Lab01_OneShot.archive.xl`. Use the `_Start` archive name wherever this
guide names the completed archive, including removal.

To test the supplied completed project instead:

1. Exit the game completely.
2. Download and extract the
   [completed Lab 1 checkpoint](../downloads/cqa-lab-01-completed.zip) into a
   writable projects directory outside the game.
3. Open `CQA_Lab01_OneShot.cpmodproj` in WolvenKit.
4. Confirm the project contains the three cooked resources under
   `source\archive\mod\cqa\cqa001` and
   `source\resources\CQA_Lab01_OneShot.archive.xl`.
5. Use the normal **Install** action. Do not choose **Install as REDmod** and do
   not use hot reload for this acceptance run.
6. Read WolvenKit's Log panel. Stop if packing reports an error or an expected
   depot path is missing.

WolvenKit documents normal **Install** as “pack the project, then copy the
generated `packed` hierarchy into the game directory” in its
[menu reference](https://wiki.redmodding.org/wolvenkit/wolvenkit-app/menu).

Verify these installed files exist:

```text
<Cyberpunk 2077>\archive\pc\mod\CQA_Lab01_OneShot.archive
<Cyberpunk 2077>\archive\pc\mod\CQA_Lab01_OneShot.archive.xl
```

Install only one checkpoint at a time. Before switching, close the game and
remove the other checkpoint's archive so it cannot supply the same depot paths.

## Check startup and registration logs

Launch the game and reach the point where a save can be loaded. After each
test, preserve the relevant portions of:

```text
<Cyberpunk 2077>\red4ext\logs\red4ext.log
<Cyberpunk 2077>\red4ext\logs\game.log
<Cyberpunk 2077>\red4ext\plugins\ArchiveXL\ArchiveXL.log
<Cyberpunk 2077>\r6\logs\redscript_rCURRENT.log
```

Check that RED4ext loaded ArchiveXL, redscript compiled without errors, and
ArchiveXL did not report a failure resolving `CQA_Lab01_OneShot.archive.xl` or
these depot paths:

```text
mod\cqa\cqa001\phases\cqa001.questphase
mod\cqa\cqa001\journal\cqa001.journal
mod\cqa\cqa001\localization\en-us\onscreens\cqa001.json
```

Do not require a guessed fixed “success” sentence: log wording can change.
Record the relevant actual lines. An ArchiveXL registration without errors is
framework evidence, not proof that the graph ran or the journal rendered.

## Run the save matrix

Use separate manual save slots for each state. Keep the installed build unchanged.

| Case | Starting state | Expected observation | Required record |
| --- | --- | --- | --- |
| First load | Untouched pre-mod save | Quest and objective activate once; after about ten real-time seconds the objective and quest succeed | Start save identity, visible state/timing, logs |
| Mid-flow reload | New save made while the objective is active | Reload reaches a defined, non-duplicated state rather than silently creating a second run | Save identity, state before/after reload, logs |
| Completed reload | New save made after success | Root guard takes the already-complete route; no reactivation | Completion state before exit and after reload |
| Reinstall same build | Completed save; the same archive and `.archive.xl` reinstalled | Reinstalling bytes does not erase save-backed completion or reactivate the quest | Installed filenames and observed state |
| Clean replay | Original untouched pre-mod save | The same first-run route remains reproducible | Original save identity and observations |

The player-facing oracle for the first and clean-replay cases is:

```text
First Signal
  -> objective: Wait for the signal.
  -> approximately 10 real-time seconds
  -> objective succeeded
  -> quest succeeded
  -> cqa001 does not activate again on the completed save
```

“Approximately” allows UI presentation and load scheduling; the authored
pause value is ten seconds. Record the measured observation rather than
rounding it into a claimed exact runtime duration.

If you cannot create a save during the short active window, record the
mid-flow case as pending. Do not convert an unrun case into a pass and do not
change the delay merely to make this test easier to run.

## Reset safely between runs

There are three different resets:

1. **Project-output reset:** WolvenKit's **Clean All** removes the generated
   project `packed` directory. It does not remove installed game files, source
   resources, or save state.
2. **Installation reset:** with the game closed, remove only
   `CQA_Lab01_OneShot.archive` and `CQA_Lab01_OneShot.archive.xl` from
   `<Cyberpunk 2077>\archive\pc\mod`. Preserve them with the test record first
   if you need to reproduce a problem. Do not delete the whole `mod` directory.
3. **State reset:** load the preserved manual save that predates the first
   `cqa001` installation. Reinstall the intended build before the clean replay.

For a controlled rebuild, close the game, clean project output, install once,
then load the untouched baseline. Changing source files,
framework versions, installed bytes, and starting saves at the same time makes
the result impossible to attribute.

## Diagnose by layer

| Symptom | First boundary to check |
| --- | --- |
| WolvenKit cannot pack | Project source paths and WolvenKit Log panel |
| `.archive` exists but `.archive.xl` does not | `source\resources` staging |
| ArchiveXL log is absent | RED4ext/plugin installation |
| Registration reports a missing phase | Exact archive depot path versus `.archive.xl` `path` |
| Quest appears without text | Journal/localization merge and localization keys |
| Quest works only on one old save | Persistent fact, journal, or checkpoint state |
| Completed quest runs again | Guard fact write, save identity, or duplicate installed builds |

Stop after the first failing boundary. Repacking repeatedly cannot fix a
missing framework, and editing the graph cannot clean an old save.

Lab sequence: [All labs](../reference/labs-at-a-glance.md) · Previous: [Author First Signal in WolvenKit](lab-01-authoring.md) · Next lab: [Lab 2: Signal Race](../gates/lab-02.md).
