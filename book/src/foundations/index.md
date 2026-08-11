# Foundations

Native quests are not one file format. A questphase coordinates resources that
have different owners, identifiers, loading rules, and persistence behavior.
The foundations establish those boundaries before a tutorial asks you to edit a
graph.

Read these chapters in order:

1. [Resources and ownership](resource-model.md)
2. [Graph execution](graph-execution.md)
3. [Identifier domains](identifier-domains.md)
4. [Facts, journals, and saves](persistent-state.md)
5. [Root and child questphases](phase-composition.md)
6. [Lifecycle, cleanup, and evidence](lifecycle-and-evidence.md)

Afterward you should be able to answer:

- which resource owns a behavior;
- whether an identifier names an object, a world location, or a lookup key;
- whether a node evaluates now or waits;
- which state survives a save and reload;
- where a parent phase ends and a child phase begins;
- what serialization, packing, and runtime tests each prove.

The chapters use small excerpts from the mod-owned `cqa001` example. They cite
vanilla depot paths where useful but do not redistribute extracted game
resources.
