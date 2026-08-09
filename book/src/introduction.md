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
