# Items, shards, files, and scans

An item objective crosses several identifier domains. The inventory contains a
TweakDB item record; a readable entry lives in the journal; a pickup or scan
target has a world identity; and the questphase observes or changes those
systems. Reusing one string across fields does not make those owners equivalent.

```text
TweakDB item ID ---------> inventory count
                              ^
world loot or quest grant ----|

journal path -----------> shard / file / email presentation
                              ^
item Read action or computer --|

world object NodeRef ----> scan event ----> quest condition
```

This page teaches bounded native patterns for acquisition, readable shards,
computer files, terminal documents, and ordered clue scans. It does not create
a universal loot container, computer controller, scanner component, or custom
item record.

## Vanilla references

These focused base-game resources are useful comparisons. Extract them from
your own installation; they are references, not files to copy into the project.

```text
base\open_world\minor_activities\watson\northside\ma_wat_nid_15\ma_wat_nid_15_phase.questphase
base\open_world\minor_activities\watson\little_china\ma_wat_lch_03\ma_wat_lch_03_phase.questphase
base\open_world\minor_activities\watson\little_china\ma_wat_lch_05\ma_wat_lch_05_phase.questphase
base\open_world\minor_activities\watson\little_china\ma_wat_lch_15\phases\ma_wat_lch_15.questphase
base\open_world\street_stories\heywood\vista_del_rey\sts_hey_rey_09\phases\sts_hey_rey_09_openworld.questphase
base\quest\side_quests\sq021\phases\sq021_randys_room.questphase
base\worlds\03_night_city\_compiled\default\exterior_19_-8_0_0.streamingsector
base\gameplay\devices\masters\computers\laptop_1.ent
base\journal\cooked_journal.journal
```

## Resource and asset checklist

| Concern | Owner | Required decision |
| --- | --- | --- |
| Inventory identity | TweakDB item record | Exact `TweakDBID`, quantity, stack behavior, tags, and whether a readable action exists |
| Acquisition producer | World loot, device, scene, or quest item-manager node | Who actually adds the item and whether a notification is expected |
| Acquisition observer | `questInventory_ConditionType` or an explicit fact | Quantity comparison, player/object selection, and already-owned behavior |
| Readable content | Mod-owned journal tree | Leaf type, full path, localization, registration, and containing-group `fileEntryIndex` |
| Shard bridge | Item's secondary `Read` action | Exact journal entry target and presentation behavior |
| Computer content | Entity template plus bound instance `RedPackage` | Controller chunks, component CRUIDs, non-empty file/email structures, menus, and per-element fact |
| Scan target | Streamed entity/device | Full/local NodeRef, scanner component, highlight owner, placement, and streaming range |
| Scan observer | `questScan_ConditionType` | Event type, object reference, activation order, and whether every clue is required |
| Objective presentation | Journal objective, description, optional clue entries, and mappins | Explicit Active/Succeeded/Inactive edges and registered localization |
| Persistence | Save plus world/device/journal state | Clean control, reload points, fresh device identity where needed, and replay policy |

The item ID, journal path, and world NodeRef are different identifier domains.
Review [Identifier domains](../foundations/identifier-domains.md) before
binding them.

## Acquire an item

### Choose the producer first

There are two useful small stories:

```text
world pickup or other system adds item
  -> quest waits until inventory quantity is sufficient
```

```text
quest grants item
  -> quest waits until inventory quantity is sufficient
```

The first pattern does not need an add node. The second does. In either case,
the wait is a separate assertion; the item-manager node's `Out` means its
command was dispatched, not that every downstream inventory/UI effect has been
accepted.

### Focused native properties

**Structurally validated:** the retained generated grant uses a
`questItemManagerNodeDefinition` with a handled
`questAddRemoveItem_NodeType`. Its parameter object contains:

| `questAddRemoveItem_NodeTypeParams` property | Retained grant value |
| --- | --- |
| `entityRef` | Local-player `questUniversalRef` |
| `itemID` | Bound item `TweakDBID` |
| `nodeType` | `AddItem` |
| `quantity` | Bound positive quantity |
| `sendNotification` | `1` |
| `flagItemAddedCallbackAsSilent` | `0` |

The corresponding wait is:

```text
questPauseConditionNodeDefinition
  condition -> questObjectCondition
    type -> questInventory_ConditionType
      comparisonType: GreaterOrEqual
      isPlayer: 1
      itemID: Items.YourRecord
      quantity: N
```

**Observed in vanilla:** inventory conditions occur in the retained vanilla
corpus, including the cited Heywood street-story phase. The table above is a
mod-owned reduced shape; its notification and player-reference choices are not
universal vanilla rules.

### Already-owned and repeatable cases

An inventory state wait can be true at activation if the player already owns
the item. That is appropriate for “have the package” but wrong for “pick up
this newly spawned package now.” Use a separate acquisition fact or resettable
counter only when its producer is explicit.

**Experimental:** merely changing `GreaterOrEqual` to another enum or using an
object reference instead of `isPlayer` creates a new behavior claim. Inspect a
matching vanilla payload and test it rather than inferring semantics from the
name.

## Remove, consume, or hand off an item

The retained plant template uses the same item-manager family with
`nodeType: RemoveAll`, silent callback, and no notification. The generated
outcome-device shape can also remove branch-specific items before adding an
outcome item or fact.

| Design question | Why it must be explicit |
| --- | --- |
| Remove one or every matching item | `RemoveAll` is not a quantity-one promise |
| Show a notification | Silent callback and `sendNotification` are separate fields |
| Consume before or after success | Graph order determines whether a failed interaction loses the item |
| Retry after reload | Inventory and completion facts may restore from different save-backed owners |
| Deliver to a kiosk | The drop point owns deposit UI and removal; do not also remove the item early unless the design proves that sequence |

**Runtime-proven:** a
[retained candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
consumed one exact keylogger as part of its completed personal-link install
route. It does not establish a generic
`RemoveAll` policy for quest items. See
[Areas, devices, and hacking](areas-devices-and-hacking.md) for the complete
plant and drop-point contracts.

## Readable shards

A readable shard combines at least two assets:

```text
TweakDB readable item
  -> secondary Read action
     -> full gameJournalOnscreen path

mod-owned journal
  -> gameJournalOnscreenGroup
     -> gameJournalOnscreen leaf
        -> title / description localization
```

Activating a `gameJournalOnscreen` makes journal content available. It does
not by itself award an inventory item or guarantee a pickup overlay. Likewise,
owning or consuming a readable item does not establish a universal “the player
read every word” signal.

### Choose what completion means

| Intended contract | Suitable observed signal | Evidence boundary |
| --- | --- | --- |
| Player acquired the readable | Inventory ownership while it remains stacked | **Structurally validated** reduced inventory wait; reload and consumption still need testing |
| The award step occurred | Dedicated acquisition fact set by the known producer | **Runtime-proven** only for the exact `82C221...` route |
| Player opened a full Journal reader | A matching visited condition, if the exact UI path emits it | **Experimental** for a generic inventory shard |
| Player opened the pickup-notification preview | No generic visited signal is established | **Experimental**; do not equate it with the full Journal reader |

**Observed in vanilla:** the retained phases associated with the
`ma_wat_lch_03`, `ma_wat_lch_05`, and `ma_wat_lch_15` objectives named
`read_shard` do not contain `questJournalEntryVisited_ConditionType`. Their
progression is tied to inventory, loot, or interaction state instead. This is
evidence against a universal visited recipe, not proof that no quest anywhere
uses visited state.

**Runtime-proven:** the readable item in archive `82C221...` was consumed into
the Journal, so inventory ceased to be a dependable completion wait. Its graph
instead observed the final scan's acquisition fact, allowed a three-second
presentation window, succeeded the objective, and continued. It deliberately
did not prove that the pickup preview had been read.

### Focused shard graph

The structurally validated reduced shape is:

```text
optional objective Active
  -> optional description Active
  -> optional gameJournalOnscreen Active
  -> wait acquisition fact OR inventory ownership
  -> optional presentation delay
  -> objective Succeeded
  -> optional completion fact
```

Do not activate the same journal entry twice merely to force a notification.
Keep acquisition, availability, notification, and proof-of-reading as separate
claims.

## Files, emails, and terminal documents

### Journal leaves are presentation data

The onscreen journal branch contains distinct leaf families:

| Group | Leaf | Principal player-facing fields |
| --- | --- | --- |
| `gameJournalOnscreenGroup` | `gameJournalOnscreen` | `title.value`, `description.value`, `tag`, `iconID` |
| `gameJournalFileGroup` | `gameJournalFile` | `title.value`, `content.value`, `pictureTweak`, `videoResource` |
| `gameJournalEmailGroup` | `gameJournalEmail` | `sender.value`, `addressee.value`, `title.value`, `content.value`, optional media |

**Observed in vanilla:** these types and fields occur in
`base\journal\cooked_journal.journal`. A journal leaf does not create a
terminal menu or decide which device displays it.

For a path such as:

```text
onscreens/emails/quests/minor_quest/your_quest/files/diagnostic
```

the containing `files` group is the path component used by
`gameJournalPath.fileEntryIndex`. Count the real path components from zero;
do not use the document's array position or copy an index from another path.

### The computer owns the clickable content

**Observed in vanilla:** SQ021's laptop separates four owners:

```text
world sector node
  -> laptop_1.ent
  -> node-local instanceData RedPackage
     -> ComputerControllerPS
        -> computerSetup.filesStructure[].content[]
           -> journalPath
           -> gamedeviceDataElement.questInfo.factName

questphase
  -> wait for that fact
```

The inspected SQ021 resource joins its active controller package to the
controller component in `laptop_1.ent` through matching component CRUIDs. That
join is **Observed in vanilla**. The runtime behavior of a mismatched custom
package remains **Experimental**. Independently, `filesMenu: 1` cannot name
clickable content when `filesStructure` itself is empty.

Do not copy SQ021's full RedPackage. Inspect its three relevant chunks and
construct a mod-owned minimal package whose controller/scanner component IDs
match the exact selected template. Remove inherited mail, web, newsfeed,
scanner, and quest content unless the new design owns it.

### Terminal read graph

The structurally validated reduced graph is:

| Order | Node | Binding |
| ---: | --- | --- |
| 1 | Optional `questJournalNodeDefinition` | `gameJournalFile` path `Active` |
| 2 | `questJournalNodeDefinition` | Objective `Active` |
| 3 | `questPauseConditionNodeDefinition` | Dedicated document fact greater than zero |
| 4 | `questJournalNodeDefinition` | Objective `Succeeded` |

The phase does not infer a read from generic journal state. The computer
element, computer scene output, or another explicitly authored UI owner must
set the completion fact.

**Runtime-proven:** a
[retained laptop candidate](../reference/evidence-version-matrix.md#retained-legacy-runtime-evidence)
used a fresh mod-owned laptop identity, exposed only its authored Files tab,
and advanced when opening
`SIGNAL DELAY` set the named document fact. That result is bounded to the
retained component mapping and device package. Its later quest-complete
presentation was a separate, initially unresolved acceptance item.

**Experimental:** a generic email-click completion signal is not established
by the file result. Files, emails, internet pages, and onscreens can use
different device/UI owners.

## Investigate clue scans

### The scan target and the scan wait have different owners

The target must already be a streamed object with whatever scanner component
and presentation behavior its template requires. The quest condition only
observes it:

```text
questPauseConditionNodeDefinition
  condition -> questObjectCondition
    type -> questScan_ConditionType
      eventType: Finished
      objectRef: gameEntityReference to clue NodeRef
```

**Structurally validated:** the current variable-length reduced shape uses
`eventType: Finished`, not `Started`. For each clue it can activate a mappin,
wait for the finished scan, hide that mappin, activate an optional
`gameJournalOnscreen`, set a clue fact, and grant one or more items.

The retained generated topology is ordered:

```text
objective and description Active
  -> clue 1 marker -> clue 1 Finished -> clue 1 outputs
  -> clue 2 marker -> clue 2 Finished -> clue 2 outputs
  -> ...
  -> objective Succeeded -> optional completion fact
```

**Observed in vanilla:** `ma_wat_nid_15_phase.questphase` provides a broader
investigation comparison, and the retained Little China phases provide scan
condition shapes. Extract and inspect the exact target reference and event
payload; do not reuse their quest-local NodeRefs or facts.

The only **Runtime-proven** claim here is the narrow `82C221...` result: its
final clue acquisition fact advanced the readable-shard stage after the item
had already been consumed into the Journal. Ordered three-clue completion,
reveal/conceal cleanup, and scanner-outline policy are **Experimental** because
no archive in this book's ledger binds those broader results.

**Experimental:** requiring any `N` of `M` clues, unordered scans, scan reset,
repeated scans, evidence-board presentation, or a custom highlight layer needs
a different graph and acceptance campaign.

## Author in WolvenKit

1. Create or clone the mod-owned journal branch first. Add the precise
   `gameJournalOnscreen`, `gameJournalFile`, or `gameJournalEmail` leaf and its
   localization, then register both resources through ArchiveXL.
2. For an inventory item, create or select a mod-owned TweakDB item record.
   Bind a readable action to the intended journal path only if the item should
   open that content.
3. In the questphase, add explicit objective activation before the inventory,
   fact, or scan pause condition. Add a separate Succeeded state after it.
4. For a quest grant or removal, add a `questItemManagerNodeDefinition` and
   inspect every parameter rather than copying a whole node blindly.
5. For each scan, bind `questScan_ConditionType.objectRef` to the exact local
   target NodeRef made available by the phase's prefab ownership. Confirm the
   corresponding full world registration and concrete target.
6. For a terminal, inspect the exact `.ent` component IDs and author the
   smallest node-local package with non-empty content. Bind the device
   element's `journalPath` and `questInfo.factName` to mod-owned values.
7. Add marker cleanup, clue journal activation, fact writes, item grants, and
   presentation delay only on explicit post-condition edges.
8. Save and reopen every CR2W. Serialize it and review concrete nested types,
   handle references, item IDs, journal class names, `fileEntryIndex`, scan
   `eventType`, target refs, and graph sockets.
9. Pack, extract, and compare the archive payload inventory before runtime
   testing. Serialization is **Structurally validated**, not
   **Runtime-proven**.

No existing lab download contains all of these systems. Lab 1 supplies the
journal/localization foundation; Lab 3 supplies world NodeRef ownership. Copy
their completed projects into a new experiment rather than treating this page
as a hidden template.

## Clean-save acceptance matrix

| Case | What it distinguishes |
| --- | --- |
| Start with zero items | Negative control for an inventory wait |
| Start already owning the required quantity | Intended state semantics versus a new-acquisition requirement |
| Acquire from the real world source | Producer, notification, inventory update, and quest wait |
| Save while waiting, then acquire after reload | Condition restoration and duplicate-grant prevention |
| Open the pickup preview and the full Journal separately | Preview behavior versus visited state |
| Consume the readable item | Whether the chosen completion signal survives item removal |
| Open the terminal before its objective | Pre-set fact and save-backed device/journal behavior |
| Open the terminal during the objective | Exact content element, fact, and single completion |
| Scan clues in intended order | Marker handoff, target identity, `Finished`, and outputs |
| Attempt a later clue early | Ordered topology and inactive-target presentation |
| Stream away and return mid-investigation | Target, marker, condition, and highlight reacquisition |
| Reload after completion | Duplicate item, journal entry, fact, objective, and marker prevention |
| Reuse an old device save after changing content | Persistent controller contamination; repeat with a fresh NodeRef or pre-stream save |

Retain the exact archive and resource hashes, TweakDB item records, full
journal paths, scan target NodeRefs, inventory counts, facts, journal states,
starting save provenance, and framework/game logs.

## Troubleshooting

| Symptom | Inspect first |
| --- | --- |
| Item objective completes immediately | Already-owned quantity, comparison type, and whether acquisition rather than ownership was intended |
| Grant node runs but no expected item appears | Item record existence, exact `TweakDBID`, local-player reference, quantity, and TweakXL load |
| Plant or handoff leaves the item | Remove mode, item ID, branch route, and whether the device/drop point owns removal instead |
| Shard appears but the quest stalls after opening it | Inventory consumption, preview versus full-reader state, and the actual acquisition/read signal |
| Journal entry is blank | Leaf type, full path, containing-group `fileEntryIndex`, ArchiveXL journal registration, and localization |
| Computer has no Files tab | Empty `filesStructure`, wrong controller chunk, component CRUID mismatch, content assignment, or stale saved device state |
| File opens but fact stays zero | `gamedeviceDataElement.questInfo.factName`, bound controller, or scene/UI output owner |
| Scan never completes | Target NodeRef, streaming, scanner component, `eventType`, object-reference form, and whether the condition was active |
| Scan completes on the wrong object | Local/full identity collision, prefab root, or copied target reference |
| Highlight remains after scanner exit | Determine whether the template or quest owns it; remove the custom layer before adding more cleanup events |
| Later clue appears too soon | Graph order, marker activation edges, and accidental parallel wiring |

See [Messages, files, emails, and onscreens](../journal/messages-and-onscreens.md)
for complete journal leaf fields, [Condition payloads](../gates/condition-payloads.md)
for pause-condition anatomy, and
[Areas, devices, and hacking](areas-devices-and-hacking.md) for the world and
device sides of these patterns.
