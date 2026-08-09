# Start checkpoint

**Lab 2 runtime evidence:** **Experimental** — pending.

Open `CQA_Lab02_SignalRace_Start.cpmodproj` in WolvenKit. This checkpoint
already contains the mod-owned journal, localization, and ArchiveXL
registration used throughout the lab. Its questphase contains only an `Input`
node connected to a `Terminating Output` node.

Do not install the start and completed projects together: they register the
same `cqa002` depot paths. Use the start checkpoint as the authoring baseline,
then add the completed graph in WolvenKit.

Use a distinct test save. Loading either registered checkpoint can serialize
questphase or journal state into the save even when no completion fact is set.
