# Contributing

This book is written for readers who may never have used WolvenKit or authored
a Cyberpunk quest resource.

Before contributing, read:

- [HANDOFF.md](HANDOFF.md) for scope and delivery order;
- [STYLE.md](STYLE.md) for the editorial and visual contract;
- [AGENTS.md](AGENTS.md) for repository guardrails.

## Chapter requirements

A hands-on chapter should contain:

1. the outcome the reader will produce;
2. prerequisites, including accounts that must be created;
3. the underlying engine concept;
4. a high-level flow diagram;
5. the exact node/resource representation;
6. step-by-step authoring instructions;
7. a checkpoint with an observable expected result;
8. verification and relevant logs;
9. common failure modes;
10. evidence status and tested versions.

Avoid instructions whose only explanation is “copy this resource.” If starter
resources are supplied, explain their structure and why each part exists.

## Evidence labels

Use one of these labels for non-obvious behavioral claims:

- **Runtime-proven:** exercised successfully in the game.
- **Structurally validated:** serialized, round-tripped, and inspected, but not
  yet proven in game in the documented custom arrangement.
- **Observed in vanilla:** present in one or more extracted game resources.
- **Experimental:** research is incomplete or runtime acceptance is pending.

Do not generalize one scene- or quest-specific observation into a universal
rule without broader vanilla or runtime evidence.

## Vanilla assets

Do not commit extracted base-game CR2W resources or complete serialized copies.
Record the original depot path and the reason it is relevant. Small focused
property excerpts and original diagrams are acceptable.
