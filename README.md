# Cyberpunk 2077 Quest Authoring

*The RED Questbook*

First-principles documentation for Cyberpunk 2077 questphases, scenes,
journals, world integration, localization, characters, devices, vehicles, and
related gameplay systems.

The project is intentionally separate from Ghostline's manifest-driven quest
creation system. Ghostline supplies research and runtime evidence; this book
teaches the underlying game resources using WolvenKit and standard modding
frameworks.

## Current state

**Lab 1 runtime evidence:** **Experimental** — pending.

**Lab 2 runtime evidence:** **Experimental** — pending.

The repository contains:

- a published mdBook and GitHub Pages workflow;
- the agreed information architecture;
- editorial and diagram standards;
- complete first-pass Foundations chapters;
- zero-assumption setup, project, vanilla-inspection, and install/test guides;
- the complete Lab 1 resource reference and manual WolvenKit walkthrough;
- a substantive journal, UI, and localization section covering typed paths,
  state, mappins, messages and documents, three localization systems, rewards,
  and completion;
- a complete conditions-and-gates section separating predicate trees from
  signal topology, with an observed condition-family catalog;
- Lab 2's start/completed WolvenKit projects, exact 21-node graph, manual
  authoring path, and two-variant runtime protocol;
- an audited [completion roadmap](ROADMAP.md) with staged release gates;
- a detailed implementation handoff in [HANDOFF.md](HANDOFF.md).

Lab 1's downloadable checkpoints, exact graph, artifact hashes, and
runtime-acceptance record live under `examples/lab-01-one-shot`. Its native
resources are structurally validated; the dedicated marker above mirrors the
canonical runtime record.

Lab 2's `cqa002` resources are structurally validated with the exact pinned
WolvenKit 8.19.0 CLI. Its timing, convergence, reload, and re-entry behaviors
remain Experimental until both hash-bound candidates and all six executions
pass the canonical schema-version-3 acceptance record.

## Local preview

Install [mdBook](https://rust-lang.github.io/mdBook/), then run:

```powershell
mdbook serve .\book --open
```

Build without starting a server:

```powershell
mdbook build .\book
```

The generated site is written to `book/site` and is ignored by Git.

## Publishing

`.github/workflows/pages.yml` builds pull requests and deploys `main` through
GitHub Pages.

The repository is hosted at:

`https://github.com/hlky/cyberpunk-quest-authoring`

The published book is available at:

`https://hlky.github.io/cyberpunk-quest-authoring/`

## License

Prose, diagrams, and example projects are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts are licensed
under the [MIT License](LICENSE-MIT). See [LICENSE.md](LICENSE.md) for scope.
