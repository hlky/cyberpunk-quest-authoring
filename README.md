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

The repository contains:

- a published mdBook and GitHub Pages workflow;
- the agreed information architecture;
- editorial and diagram standards;
- complete first-pass Foundations chapters;
- the pinned first-release toolchain and Lab 1 resource design;
- a detailed implementation handoff in [HANDOFF.md](HANDOFF.md).

Lab 1 implementation is in progress under `examples/lab-01-one-shot`.

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
