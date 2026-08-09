# Cyberpunk 2077 Quest Authoring

*The RED Questbook*

This book explains how Cyberpunk 2077's native quest resources work together
and how to author new quest content with WolvenKit and standard modding
frameworks.

It starts with a one-shot objective and grows toward scenes, communities,
devices, combat, vehicles, and specialized systems. The goal is not to hide the
engine behind a generator. The goal is to make the resource model
understandable.

The first tutorial builds `cqa001`, a one-shot quest with no world, scene,
actor, or device dependencies. Its resource design, exact graph, manual
WolvenKit walkthrough, and runtime-acceptance record keep structural
claims reviewable without presenting an expected game result as proof.

**Lab 1 runtime evidence:** **Experimental** — pending.

The second tutorial, `cqa002`, adds immediate and waiting conditions, a nested
Boolean tree, parallel monitors, and XOR-shaped signal convergence. It ships as
two structurally validated WolvenKit checkpoints with separate canonical and
source-edited runtime candidates.

**Lab 2 runtime evidence:** **Experimental** — pending.

The third tutorial, `cqa003`, adds a registered streaming block, Quest and
AlwaysLoaded sectors, a quest-prefab/NodeRef chain, concentric reach/leave
triggers, a static marker, and a journal map pin. Its six-resource checkpoints
are structurally validated; the eight-run world/save matrix is still pending.

**Lab 3 runtime evidence:** **Experimental** — pending.

The fourth tutorial, `cqa004`, moves the world activity into an archived
external child and makes the registered-root, root-owned prefab, `In1`/`Out1`,
and normal return contract explicit.

**Lab 4 runtime evidence:** **Experimental** — pending.

The fifth tutorial, `cqa005`, activates a one-entry community, waits for actor
and approach readiness, runs one externally localized spoken line through a
named scene entry/exit, and delays deactivation until V leaves the outer
cleanup area. Both checkpoints are structurally validated; exact in-matrix
runtime claims, including the named pre-scene seed loads in Cases 3, 4, and 7,
follow the synchronized marker below. Active-line
interruption/`CutDestination`, arbitrary/unlisted pre-scene active-child
states, and facial/workspot-animation quality remain **Experimental** outside
that matrix.

**Lab 5 runtime evidence:** **Experimental** — pending.

## What this book will cover

Cyberpunk quests span several resource systems:

- `.questphase` graphs control progression and persistent state;
- `.journal` resources provide quests, objectives, messages, files, and map
  pins;
- localization resources provide UI text, subtitles, spoken dialogue, and
  scene choice text through distinct lookup paths;
- streaming resources provide triggers, markers, communities, AI spots, and
  devices;
- `.scene` resources provide dialogue, choices, events, animations, and named
  exits;
- entity, appearance, and TweakDB resources provide custom characters and
  gameplay records.

The practical guides will explain who owns each responsibility and how to test
the boundaries between them.

## Evidence

Pages distinguish behavior proven in game from structure observed in vanilla
or validated only through serialization. Experimental material is kept visible
without being presented as settled authoring guidance.
