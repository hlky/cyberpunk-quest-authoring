# Install the pinned toolchain

This procedure establishes one reproducible Windows authoring environment. At
the end, WolvenKit can browse your installed game and the framework logs can
prove which runtime components loaded.

| Record | Value |
| --- | --- |
| Procedure review date | 2026-08-09 |
| Game baseline | Cyberpunk 2077 `2.31a`, Windows GOG build |
| Authoring tool | WolvenKit `8.19.0` |
| Resource framework | ArchiveXL `1.27.0` |
| Runtime loader | RED4ext `1.30.0` |
| ArchiveXL script requirement | redscript `0.5.31` |
| Runtime test date | Not yet recorded |

> **Evidence boundary:** the version selection and file layouts below are
> supported by the linked upstream releases and project documentation. The Lab
> 1 resources are **Structurally validated**; installing the prerequisites does
> not make Lab 1 **Runtime-proven**.

The repository-wide baseline is recorded in [Tested versions](../reference/tested-versions.md).
ArchiveXL's upstream documentation also lists redscript `0.5.31+` as a
requirement, so this guide fixes the first compatible stable version,
`0.5.31`, rather than leaving a clean-install reader with a hidden dependency.

## Start from a known game installation

You need:

- 64-bit Windows 10 or 11;
- a legally owned Windows copy of Cyberpunk 2077 and the store or launcher
  account that owns it;
- enough writable storage for WolvenKit, its asset cache, and projects outside
  the game directory;
- permission to copy the framework and built mod files into the game
  directory.

No GitHub account is needed to download public release assets. No Nexus Mods,
WolvenKit, Discord, or other service account is required for this book.

Launch the unmodded game once and confirm the version shown by the game is the
expected build. Then exit completely. If the installation may be damaged, use
your storefront's verification function; CD Projekt RED documents
[Verify/Repair for GOG and equivalent Steam/Epic checks](https://support.cdprojektred.com/en/cyberpunk%20/pc/sp-technical/issue/1562/verify-integrity-of-game-files-1).

Store verification repairs official files but may leave extra mod files in
place. An installation is a controlled baseline only when you also know what
is present under locations such as `archive\pc\mod`, `red4ext`, and
`r6\scripts`. Preserve an inventory or use a dedicated test installation.
Never delete the whole game directory as a troubleshooting shortcut.

This release was checked against the exact GOG suffix `2.31a`. The public patch
name and the labels shown by other storefronts may be `2.31`; treat those as a
separate environment until the example is repeated there.

## Install WolvenKit 8.19.0

1. Install Microsoft's .NET 8 runtime. The
   [WolvenKit 8.19.0 release](https://github.com/WolvenKit/WolvenKit/releases/tag/8.19.0)
   names .NET 8 as its prerequisite.
2. From that release, download `WolvenKit-8.19.0.zip` or
   `WolvenKitSetup-8.19.0.exe`. Do not download GitHub's automatically
   generated “Source code” archives.
3. If you chose the ZIP, extract it into a dedicated, user-writable tools
   directory. WolvenKit's project documentation treats the ZIP build as a
   portable application; it does not belong inside the Cyberpunk directory.
4. Start `WolvenKit.exe`. On first launch, set **Game Executable Path** to the
   actual `Cyberpunk2077.exe`:

   ```text
   <Cyberpunk 2077>\bin\x64\Cyberpunk2077.exe
   ```

5. Set **Depot Path** to a writable cache directory outside both the game and
   your projects, for example `C:\CyberpunkModding\WolvenKitDepot`.
6. Confirm the status bar reports `8.19.0`, then close WolvenKit before
   installing the runtime frameworks.

The upstream [download and setup guide](https://wiki.redmodding.org/wolvenkit/getting-started/download)
and [settings reference](https://wiki.redmodding.org/wolvenkit/wolvenkit-app/settings)
explain these two paths. The setting called **Depot Path** is WolvenKit's local
asset cache. It is not a resource's virtual depot path; that distinction is
covered in [Project and resource structure](project-structure.md).

The separate WolvenKit Console download is not a reader prerequisite for these
chapters.

## Install the runtime dependencies

All release archives in this section are laid out relative to the Cyberpunk
2077 directory. Extract each archive so that its `bin`, `red4ext`, or `r6`
directory merges with the directory of the same name in the game installation.
Do not create an extra wrapper such as
`Cyberpunk 2077\red4ext-1.30.0\red4ext`.

1. Install the Microsoft Visual C++ 2015–2022 x64 Redistributable required by
   RED4ext.
2. Download `red4ext-1.30.0.zip` from the
   [RED4ext 1.30.0 release](https://github.com/WopsS/RED4ext/releases/tag/v1.30.0)
   and extract it into the Cyberpunk 2077 directory. Do not use the separate
   symbols archive.
3. Download `redscript-v0.5.31-windows.zip` from the
   [redscript 0.5.31 release](https://github.com/jac3km4/redscript/releases/tag/v0.5.31)
   and extract it into the same directory.
4. Download `ArchiveXL-1.27.0.zip` from the
   [ArchiveXL 1.27.0 release](https://github.com/psiberx/cp2077-archive-xl/releases/tag/v1.27.0)
   and extract it into the same directory.

The [RED4ext installation guide](https://docs.red4ext.com/getting-started/installing-red4ext)
and [ArchiveXL repository](https://github.com/psiberx/cp2077-archive-xl)
are the authoritative upstream installation references.

At minimum, the merge should leave these files at these relative locations:

```text
bin\x64\winmm.dll
red4ext\RED4ext.dll
red4ext\plugins\ArchiveXL\ArchiveXL.dll
```

ArchiveXL also supplies files below `r6\config` and its plugin directory.
Their presence is expected; do not cherry-pick only the DLL.

## Prove the frameworks start

Launch the game once, reach the main menu, and exit. Check for:

```text
<Cyberpunk 2077>\red4ext\logs\red4ext.log
<Cyberpunk 2077>\red4ext\logs\game.log
<Cyberpunk 2077>\red4ext\plugins\ArchiveXL\ArchiveXL.log
<Cyberpunk 2077>\r6\logs\redscript_rCURRENT.log
```

The RED4ext documentation identifies `red4ext.log` and `game.log` as the
loader/plugin checks, while the
[redscript repository](https://github.com/jac3km4/redscript) identifies its
`r6\logs` output. ArchiveXL writes its own plugin log after it loads.

Record the version banners and resolve errors before creating a quest. A file
existing on disk proves only that it was copied; a clean framework log proves
only that the loader reached that component. Neither proves a quest resource
was registered or executed.

## Setup checkpoint

Before continuing, you should be able to answer yes to all of these:

- Does the unmodded game reach the main menu on the target build?
- Does WolvenKit 8.19.0 point to the real game executable?
- Is the WolvenKit cache outside the game and project directories?
- Do RED4ext, redscript, and ArchiveXL create their expected logs without an
  unresolved dependency or compilation error?
- Have you recorded any unrelated mods still present in the test installation?

If not, stop here. Quest edits cannot repair a broken authoring or runtime
baseline.
