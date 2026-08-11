# Cyberpunk 2077 Quest Authoring

*The RED Questbook*

A standalone, first-principles guide to authoring native Cyberpunk 2077 quest
resources with WolvenKit and standard modding frameworks.

The book covers questphases, journals, localization, world integration,
conditions, communities, scenes, characters, devices, combat, vehicles, and
specialized systems. It begins with a one-objective quest and grows through
five downloadable WolvenKit labs, so readers can learn the resource model
without relying on a quest generator or an unexplained template.

The project complements the broader [REDmodding quest and scene
guides](https://wiki.redmodding.org/cyberpunk-2077-modding/modding-guides/quest).
It is maintained separately so the material, examples, and tested tool
boundaries can evolve together as native quest authoring develops.

## Read the book

The published book is available at:

<https://hlky.github.io/cyberpunk-quest-authoring/>

New readers should begin with **Start here** and follow Labs 1–5 in order.
Experienced modders can use the subject chapters, gameplay-pattern cookbook,
troubleshooting guides, and reference indexes directly.

## What is in this repository

- `book/src` — the mdBook source;
- `examples` — incremental start and completed WolvenKit projects;
- `assets/diagrams` — deterministic diagram sources;
- `evidence` — machine-readable research provenance for maintainers;
- `scripts` — validation, diagram, and packaging infrastructure.

Extracted vanilla CR2W resources are not redistributed. The book names depot
paths and teaches readers to extract their own focused references.

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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the editorial, example, evidence,
and validation workflow. Reader-facing procedures must use WolvenKit,
ArchiveXL, the game, and chapter-specific standard tools; repository scripts
and evidence records are maintainer infrastructure.

## License

Prose, diagrams, and example projects are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts are licensed
under the [MIT License](LICENSE-MIT). See [LICENSE.md](LICENSE.md) for scope.
