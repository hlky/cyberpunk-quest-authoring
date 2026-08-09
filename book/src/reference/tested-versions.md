# Tested versions

The first release pins one exact baseline instead of promising compatibility
with older tools.

| Component | Pinned version | Role |
| --- | --- | --- |
| Cyberpunk 2077 for Windows | `2.31a` | Exact GOG Windows build; CD Projekt RED calls the underlying public patch `2.31` |
| WolvenKit | `8.19.0` | Project editing, CR2W inspection, conversion, packing, and deployment |
| ArchiveXL | `1.27.0` | Root questphase, journal, and localization registration |
| RED4ext | `1.30.0` | Runtime required by ArchiveXL |
| mdBook | `0.5.4` | Documentation build only; not a reader authoring prerequisite |

Version check date: **2026-07-27**. The WolvenKit, ArchiveXL, and RED4ext pins
were their latest stable GitHub releases on that date. Cyberpunk 2077 `2.31a`
was the current Windows GOG build supplied for testing.

These are the initial tested versions, not universal minimums. A practical
chapter may name a newer baseline after its example has been repeated against
that combination. Older versions are unsupported unless the chapter says
otherwise.

The `2.31a` suffix is visible in the Windows GOG distribution. CD Projekt RED's
public notes are titled [Patch
2.31](https://www.cyberpunk.net/en/news/51794/patch-2-31); this book records the
exact installed build so results are reproducible.

Release sources:

- [WolvenKit 8.19.0](https://github.com/WolvenKit/WolvenKit/releases/tag/8.19.0)
- [ArchiveXL 1.27.0](https://github.com/psiberx/cp2077-archive-xl/releases/tag/v1.27.0)
- [RED4ext 1.30.0](https://github.com/WopsS/RED4ext/releases/tag/v1.30.0)

Every practical guide must also state its own test date, evidence status, and
clean-save requirements. A repository-wide pin does not turn an untested
resource arrangement into a runtime-proven one.
