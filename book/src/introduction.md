# Cyberpunk 2077 Quest Authoring

*The RED Questbook*

Quest modding in Cyberpunk 2077 is powerful, but the public documentation is
still scattered across a small number of focused guides. This book provides a
standalone path from opening your first quest resource to building quests with
journal entries, world interactions, characters, scenes, combat, vehicles,
and cleanup.

You do not need to understand REDengine internals before you begin. The early
chapters introduce one idea at a time, and the downloadable WolvenKit projects
give you something concrete to inspect whenever the resource model feels
abstract.

The book complements the broader [REDmodding quest and scene
guides](https://wiki.redmodding.org/cyberpunk-2077-modding/modding-guides/quest).
It lives separately because native quest authoring is still developing quickly
and benefits from executable examples, coordinated diagrams, and a learning
path that can evolve as the tools improve.

## Start small

Begin with [Start here](start-here/index.md). You will install the tools, learn
the shape of a WolvenKit project, inspect one vanilla questphase, and build
**First Signal**: a quest with one objective, a short wait, and a one-shot
completion fact.

Five incremental labs then add the major systems:

1. **First Signal** — questphase, journal, localization, and a persistent fact.
2. **Signal Race** — conditions, waits, Boolean trees, and parallel signal flow.
3. **Boundary Check** — streaming sectors, NodeRefs, triggers, and a map pin.
4. **Handoff Point** — root and child questphases with explicit input/output
   contracts.
5. **First Contact** — a community actor, readiness, a spoken scene, named
   handoff, and delayed cleanup.

Each lab includes an overview, a manual WolvenKit walkthrough, a completed
project, and an in-game test procedure. You can follow them in order or use the
[lab overview](reference/labs-at-a-glance.md) to find the closest starting
point for your own quest.

## Think in cooperating resources

A Cyberpunk quest is rarely one file:

- `.questphase` graphs coordinate progression and persistent state;
- `.journal` resources define quests, objectives, messages, files, and map
  pins;
- localization resources provide UI text, subtitles, dialogue, and choices;
- streaming resources place triggers, markers, communities, AI spots, and
  devices in the world;
- `.scene` resources provide dialogue, choices, events, animations, and named
  exits;
- entity, appearance, and TweakDB resources provide custom characters and
  gameplay records.

Most difficult bugs occur where two of these owners disagree. The book
therefore explains not only which properties to set, but which resource owns
the behavior, how identities connect across files, and what to inspect when a
graph looks valid but nothing happens in game.

## What the examples prove

The downloadable projects are executable reference material, not magic
templates. Their structure is checked with the version of WolvenKit listed in
[Tested versions](reference/tested-versions.md), and every supplied node and
resource is explained in the book.

Some wider recipes are based on focused vanilla inspection or on bounded
runtime research rather than a complete custom quest tested on every save and
reload path. Those claims are labelled where the distinction affects what you
should build or test. Detailed provenance remains available in the reference
material, but it is never required to follow a reader procedure.
