# World integration

Quests refer to a streamed world rather than creating physical locations by
themselves.

This section will cover:

- streaming worlds, blocks, sectors, and inplace resources;
- AlwaysLoaded and Quest sector responsibilities;
- quest prefabs and phase-prefab declarations;
- NodeRefs and full versus local reference paths;
- markers, triggers, outlines, and notifiers;
- scene placement versus journal/map-pin placement;
- navigation endpoints and device slots;
- researching accessible, quest-safe vanilla locations;
- save-backed device state and fresh NodeRef identities.

The first world lab will add one marker and one trigger to the minimal quest.
