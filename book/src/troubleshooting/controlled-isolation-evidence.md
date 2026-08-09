# Controlled isolation and evidence

Controlled isolation answers one question: what smallest changed boundary
explains the different result? It requires a known-good or known-failing
baseline, one intentional delta, the same eligible inputs, and retained
evidence for both sides.

## Evidence and version boundary

Use Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31` for current campaigns.

**Runtime-proven:** the strongest retained legacy scene differential changed
only the meeting scene between archive
`177500B67B2A6B975A597DF5D582797F006643BA6BC975E1D9CFBC66BC498BFD`
and archive
`87956AFFE3C7CD66E16AD8531D0784689B01A24DCA629FAF41C2291C6E70E40D`.
The former reproduced the launch crash; the latter made one addressable
lipsync row and selected slot `0` for both actors, then completed the meeting
route. That supports the bounded legacy cardinality diagnosis.

**Experimental:** facial-animation quality, active-line interruption, and
current-stack equivalence remained outside that differential. A controlled
test never proves untested neighboring behavior.

## Freeze the baseline

Before creating a candidate, record:

| Input | Frozen value |
| --- | --- |
| Game/framework stack | Exact versions and storefront/build |
| Candidate files | Names, sizes, SHA-256 hashes, and install paths |
| Archive contents | Sorted depot-path listing and extracted payload hashes |
| Unrelated mods | Explicit inventory or verified absence |
| Starting save | Capture name, slot directory, pre-install assertion, and hash |
| Route | Exact player actions and activation boundary |
| Oracle | Visible/log result that distinguishes pass from fail |
| Logs | Complete file paths and hashes |

“Same setup” is not evidence unless these values are retained.

## State one falsifiable hypothesis

Write the hypothesis before editing:

```text
If actor slot 1 is the out-of-range lookup, then changing only the scene's
addressable lipsync table/consumer indexes will move the launch result from the
same crash to successful scene entry under the same route and save class.
```

A useful hypothesis names:

- one suspected boundary;
- one controlled change;
- one expected observation if correct;
- one observation that would reject it.

“Make the scene more vanilla” is not falsifiable. “Change actor readiness,
trigger radius, lipsync rows, VO paths, and graph timing” cannot identify a
cause.

## Build a one-delta candidate

1. Copy the known baseline project or restore its exact source commit.
2. Make one semantic change. Generated binary noise does not count as another
   semantic change, but it must still be inspected.
3. Round-trip every changed CR2W and compare decisive properties.
4. Build in a clean staging directory.
5. List/extract the archive and prove the expected payload set.
6. Compare extracted payloads with the baseline and name every changed depot
   path.
7. Stage one canonical candidate; record that earlier labs/copies and unrelated
   mods are absent.
8. Hash installed files after staging.

If more payloads changed than planned, stop. Explain or eliminate the drift
before runtime testing.

## Run paired cases

Use independent full-slot clones from the same eligible capture:

| Run | Installed bytes | Save clone | Purpose |
| --- | --- | --- | --- |
| Baseline reproduction | Baseline hash | Clone A | Prove the original symptom still occurs |
| Candidate test | Candidate hash | Clone B | Test the one-delta hypothesis |
| Baseline return, when practical | Baseline hash restored | Clone C | Reject an unrelated one-time environment change |
| Removal isolation, when defined | Candidate pair deliberately absent | Clone D | Prove mounted candidate dependency without mutating save state |

Close the game before changing files or cloning slots. Run the same route and
collect a fresh full log bundle each time.

## Record observations before explanations

Separate these fields:

| Field | Example |
| --- | --- |
| Expected | Scene reaches its first section without process termination |
| Observed | Crash at setup boundary; no dialogue visualizer; report ID retained |
| Difference | Candidate moved past setup and returned through named exit |
| Interpretation | Result is consistent with the indexed table diagnosis |
| Rejected alternatives | World/trigger path was byte-identical; subtitle/VO resources unchanged |
| Limitations | Shared slot is diagnostic; facial quality and reload not tested |

Do not rewrite “consistent with” into a universal engine law. Runtime evidence
is bounded by the exact bytes, versions, save class, and route.

## Use negative controls

Negative controls prevent false attribution:

- bypass a suspect scene while leaving world/community setup intact;
- invoke a Start-to-End shell before restoring dialogue;
- remove only the candidate pair while keeping framework/unrelated-mod
  inventory frozen;
- restore the baseline hash after a passing candidate;
- test a clean original and an old save with identical installed bytes;
- move an activation boundary without changing the suspected resource, then
  record whether the failure follows launch or world position.

Each control answers a narrow question. A scene bypass proves the preceding
path can continue; it does not prove the full scene is correct.

## Evidence package

Retain or record:

- source commit and focused diff;
- built `.archive`/loose-file hashes;
- archive listing and extracted-payload comparison;
- exact installed inventory;
- game/framework/tool versions;
- save lineage and private save hash;
- full relevant log hashes;
- crash report identifier when applicable;
- privacy-reviewed screenshots, video, log excerpts, save metadata, and notes;
- every expected/observed result, including failed and unexecutable cases;
- the hypotheses rejected during the campaign.

Do not publish private saves or unreviewed logs. Hashes identify retained
private artifacts without redistributing them.

## Promote only the tested claim

| Evidence | Supported statement |
| --- | --- |
| Round trip retains exact intended delta | Candidate is **Structurally validated** |
| Cited vanilla resource contains the comparison shape | Shape is **Observed in vanilla** |
| Paired runtime route changes exactly as predicted | Exact bounded behavior is **Runtime-proven** |
| Reload, interruption, replay, quality, or another version was not tested | Those surfaces remain **Experimental** |

If several changes landed together, preserve the result as a useful candidate
but do not assign causality. Return to the last controlled baseline and split
the changes into separate candidates.

## Handoff checklist

Before another tester receives the candidate, they should be able to answer:

1. Which exact bytes should be installed?
2. Which files and mods must be absent?
3. Which save capture and clone should be used?
4. What actions reach the tested boundary?
5. What observation passes or fails the case?
6. Which logs and evidence must be retained?
7. Which neighboring claims are explicitly outside scope?

If any answer is missing, the next run may be informative, but it is not yet a
reproducible acceptance case.

Previous: [Save state and clean retests](save-state-clean-retests.md). Back to:
[Troubleshooting](index.md).
