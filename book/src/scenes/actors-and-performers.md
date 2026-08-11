# Actors and performers

Actor IDs, performer IDs, entity references, and lipsync slots are separate
domains. First Contact deliberately uses small values that make those joins
easy to audit, but their proximity does not make them interchangeable.

## Contact: actor 0 from a community

The non-player speaker is `scnActorDef` actor `0`. Its selected acquisition
plan is `community`:

```json
{
  "$type": "scnActorDef",
  "actorId": { "$type": "scnActorId", "id": 0 },
  "actorName": "contact",
  "acquisitionPlan": "community",
  "communityParams": {
    "$type": "scnCommunityParams",
    "reference": "#cqa005_com_contact",
    "entryName": "contact",
    "forceMaxVisibility": 0
  },
  "lipsyncAnimSet": {
    "$type": "scnLipsyncAnimSetSRRefId",
    "id": 0
  }
}
```

The excerpt shortens the typed `NodeRef` and `CName` wrappers for readability.
The full actor definition also retains the typed parameter blocks and empty
animation-set arrays expected by the resource. Do not assume that deleting
inactive acquisition parameter blocks is equivalent to leaving their native
defaults present.

`acquisitionPlan: community` does not activate a community or wait for its
entry to exist. Before the questphase starts the scene, it must:

1. activate the community at `#cqa005_com_contact`;
2. wait on `CharacterSpawned` for the relevant entry or whole-community scope;
3. complete any broad setup needed for visibility and workspot state;
4. only then enter the scene through `start`.

That sequence is the bridge between [Communities and
characters](../communities/index.md) and this section. Starting the scene while
the actor is still materializing can turn an otherwise valid scene into a
timing-dependent failure.

## V: actor 1 from scene context

The player is a separate `scnPlayerActorDef`, actor `1`. Its selected plan is
`findInContext`, and the context lookup is constrained by the player record:

```json
{
  "$type": "scnPlayerActorDef",
  "actorId": { "$type": "scnActorId", "id": 1 },
  "acquisitionPlan": "findInContext",
  "playerName": "V",
  "findActorInContextParams": {
    "$type": "scnFindEntityInContextParams",
    "contextualName": "Player",
    "specRecordId": "Character.Player_Puppet_Base"
  },
  "specCharacterRecordId": "Character.Player_Puppet_Base",
  "lipsyncAnimSet": {
    "$type": "scnLipsyncAnimSetSRRefId",
    "id": 0
  }
}
```

The two shown record values are serialized `TweakDBID` fields in the native
resource, not strings in the final CR2W type system. V is not supplied by the
contact community and should not be given the contact's NodeRef or entry name.

## Performer debug symbols

First Contact's two `scnPerformerSymbol` rows use performer IDs `1` and `257`:

| Scene role | Actor ID | Performer ID | Debug entity reference |
| --- | ---: | ---: | --- |
| Contact | `0` | `1` | `#cqa005_com_contact`, name `contact` |
| V | `1` | `257` | `#player` |

This exact fixture follows the observed `actor ID * 256 + 1` performer-symbol
convention. Treat that as an authoring relationship to preserve in this shape,
not permission to substitute performer `257` anywhere a `scnActorId(1)` is
required. The screenplay line, section actor behavior, community acquisition,
and debug symbol each expect their own typed identity.

## One addressable lipsync slot

Both actor definitions reference `scnLipsyncAnimSetSRRefId` `0`. The scene has
exactly one row, at array slot `0`, under the natively spelled
`resouresReferences.lipsyncAnimSets`:

```text
slot 0
└── base\animations\facial\generic\interactive_scene\
    generic_facial_lipsync_gestures.anims
```

The lipsync ID is an array index, not an actor ID or performer ID. Therefore:

- actor `0` -> lipsync slot `0` is addressable;
- actor `1` -> lipsync slot `0` is addressable;
- actor `1` -> lipsync slot `1` would be invalid when the array has one row.

**Runtime-proven:** a [retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
records a conversation candidate that previously failed during scene startup
completing its full route after both roles were changed to slot `0` and the
duplicate generic row was reduced to one. It played spoken lines, subtitles,
and VO and returned through its quest outcome. That test proves the
cardinality correction for that hash-bound candidate. It does not prove that
sharing one generic resource is the final quality configuration for every pair
of performers.

Use distinct NPC and player lipsync resources later only when every referenced
slot remains separately addressable after cooking and is runtime-tested.
Facial-animation quality is outside the lab's normal playback checks and must
be reviewed visually for the final actor and audio assets.

## Section actor behavior

The completed scene's `scnSectionNode` contains one
`scnSectionInternalsActorBehavior` per actor:

| Actor | `behaviorMode` |
| ---: | --- |
| `0` contact | `OnlyIfAlive` |
| `1` V | `OnlyIfAlive` |

This bounds section participation when an actor is not alive; it is not an
actor-readiness wait and it cannot replace `CharacterSpawned`. Nor does it
define how a dead or missing contact should change the surrounding quest.
Alternative/failure quest routing remains a separate design problem.
