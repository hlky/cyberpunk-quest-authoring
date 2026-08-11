# Contributing

This book is written for readers who may never have used WolvenKit or authored
a Cyberpunk quest resource.

Before contributing, read:

- [STYLE.md](STYLE.md) for the editorial and visual contract;
- [AGENTS.md](AGENTS.md) for repository guardrails.

## License of contributions

By contributing, you agree that prose, diagrams, and example-project material
may be distributed under CC BY 4.0 and that contributions under `scripts/` may
be distributed under the MIT License. See [LICENSE.md](LICENSE.md).

## Chapter requirements

A hands-on chapter should help a reader reach an observable result without
requiring knowledge of this repository's release process. Include, where
relevant:

1. the outcome the reader will produce;
2. prerequisites, including accounts that must be created;
3. the underlying engine concept;
4. a high-level flow diagram;
5. the exact node/resource representation;
6. step-by-step authoring instructions;
7. a checkpoint with an observable expected result;
8. verification and relevant logs;
9. common failure modes;
10. tested versions and a concise warning for any behavior that remains
    uncertain.

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

Do not add a generic evidence-boundary section to every chapter. Put a label
beside the claim it qualifies, and link to the central provenance only when a
reader is likely to need it. Version tables belong in the tested-versions
reference and in procedures whose tool requirements differ from the normal
baseline.

## Maintainer evidence workflow

Machine-readable acceptance records, archive hashes, save provenance,
publication evidence, status promotion, manifest regeneration, and repository
validators are maintainer infrastructure. Keep their complete instructions in
this file, `scripts/README.md`, example-project metadata, or the `evidence`
directory—not in reader-facing authoring and test procedures.

Reader test chapters should explain:

- which project to install;
- which save state to begin from;
- the route or interaction to perform;
- the visible result and useful logs;
- when a clean save, reload, stream return, or removal test matters.

The example's `runtime-acceptance.json` remains the canonical publication
record. When contributing runtime evidence, preserve its case IDs and expected
results, bind observations to the installed candidate and relevant saves/logs,
then run the lab-specific validator followed by `python -B scripts/validate.py`.
The validator, rather than duplicated prose markers, is responsible for
checking consistency between the record, manifest, diagrams, and packaged
downloads.

## Vanilla assets

Do not commit extracted base-game CR2W resources or complete serialized copies.
Record the original depot path and the reason it is relevant. Small focused
property excerpts and original diagrams are acceptable.
