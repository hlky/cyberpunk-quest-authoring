# Start here

This section takes you from a verified Windows game installation and no
WolvenKit project to an installed, observable quest mod. It assumes no previous
REDengine knowledge and no GitHub, Nexus Mods, or WolvenKit account.

The first result is deliberately small: **First Signal** activates one quest
and one objective, waits ten real-time seconds, completes them, records a
one-shot fact, and terminates. It has no world, scene, NPC, device, or audio
dependency.

The supplied start and completed projects let you compare your work at each
stage. The completed resources pass the book's structural checks; the test
guide shows you how to verify the player-facing result in your own game.

## What a quest consists of

A `.questphase` is the coordinator, not the entire quest. Even this minimal
example crosses four ownership boundaries:

| Responsibility | Owner in Lab 1 |
| --- | --- |
| Execution, wait, fact guard, and termination | `cqa001.questphase` |
| Quest and objective definitions | `cqa001.journal` |
| English player-facing text | `cqa001` onscreen localization resource |
| Attaching those mod-owned resources to game roots | `CQA_Lab01_OneShot.archive.xl` |

The first three are native CR2W resources packed into a game archive. The last
is a loose ArchiveXL framework file. Installing only one layer cannot produce
the complete behavior.

## Use this reading path

1. [Install the pinned toolchain](setup.md) from a known starting state.
2. [Create a project and understand its layers](project-structure.md).
3. [Extract and inspect one named vanilla questphase](inspecting-vanilla.md)
   in a separate research project.
4. Read [Foundations](../foundations/index.md) for ownership, graph execution,
   identifiers, save-backed state, composition, and lifecycle.
5. Build [Lab 1: First Signal](lab-01.md).
6. [Install, observe, record, and reset](install-and-test.md) without confusing
   an old save with a clean test.

Use the [tested version set](../reference/tested-versions.md) throughout. Newer
versions may work, but editor labels, serialization, or framework registration
can change; note the versions you actually use when reporting a problem.

## What you do not need

You do not need a quest generator, a manifest compiler, a pre-extracted copy of
the game, or access to the research repository used to develop this book. You
will author and inspect the game resource model with WolvenKit, package native
resources in an archive, register them with ArchiveXL, and test them in the
game.

You also do not need to edit raw CR2W-JSON. The serialized files supplied with
the completed checkpoint exist for review, deterministic diagrams, and
structural comparison; the beginner workflow stays in WolvenKit.
