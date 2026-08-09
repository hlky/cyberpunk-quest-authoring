# Start checkpoint

Open `CQA_Lab01_OneShot_Start.cpmodproj` in WolvenKit. This checkpoint contains
no quest resources yet; it is the state immediately before the Lab 1 authoring
steps begin.

Use a distinct test save. Installing the completed checkpoint sets persistent
fact `cqa001_completed`, so a clean replay requires a pre-install save. A fact
reset is a diagnostic convenience, not clean-save proof: journal and
questphase state may already be serialized in the save.
