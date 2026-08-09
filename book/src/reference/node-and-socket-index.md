# Node and socket index

This is a search index for the graph nodes and socket names introduced through
Labs 1–5 and the supporting control-flow chapters. It is not a replacement for
the node's complete property contract.

The exact node sets in the completed lab projects are **Structurally
validated** with WolvenKit `8.19.0`. Wider arities and node families explicitly
described as vanilla inventory are **Observed in vanilla**. Runtime scheduling,
cancellation, save restoration, and re-entry remain governed by each lab's
retained evidence record. Start with [Labs at a glance](labs-at-a-glance.md)
when choosing the smallest project that contains a node.

## Read a quest node in four parts

For every quest graph node, record:

1. the graph-local numeric `id` and containing `.questphase`;
2. the concrete RED node type;
3. the decisive typed payload or external reference;
4. every connected socket name, socket type, and destination.

The node's serialized array position and CR2W `HandleId` are not execution
order. One output socket can contain several connections, and reciprocal
references from the source and destination still describe one edge.

## Quest graph boundary and state nodes

Socket sets below are the focused shapes used by the book. WolvenKit can omit
unused ordinary sockets from one serialized instance, and some node types add
dynamic sockets. Confirm the exact resource rather than manufacturing every
name in this table.

| WolvenKit label / RED type | Job | Decisive property or payload | Focused sockets | First complete use |
| --- | --- | --- | --- | --- |
| Input / `questInputNodeDefinition` | Expose one phase entry | `socketName`, such as `In1` | internal `Out`; `CutDestination` | [Lab 1](../start-here/lab-01.md) |
| Output / `questOutputNodeDefinition` | Expose a phase result and optionally terminate | `socketName`, such as `Out1`; output `type` | internal `In`; `CutDestination` | [Lab 1](../start-here/lab-01.md) |
| Condition / `questConditionNodeDefinition` | Evaluate a predicate on entry and branch immediately | `condition` handle | `In`, `True`, `False`, `CutDestination` | [Lab 1](../start-here/lab-01.md) |
| PauseCondition / `questPauseConditionNodeDefinition` | Hold one active route until a predicate is fulfilled | `condition` handle | `In`, `Out`, `CutDestination` | [Lab 1](../start-here/lab-01.md) |
| Journal / `questJournalNodeDefinition` | Request a state change for one typed journal path | `type` handle, including `path` and presentation properties | `Active`, `Inactive`, `Succeeded`, `Failed` inputs; `Out`; `CutDestination` | [Lab 1](../start-here/lab-01.md) |
| FactsDBManager / `questFactsDBManagerNodeDefinition` | Write a fact | `questSetVar_NodeType`, including fact name, value, and exact/add policy | `In`, `Out`, `CutDestination` | [Lab 1](../start-here/lab-01.md) |
| MappinManager / `questMappinManagerNodeDefinition` | Request active/inactive state for a journal quest pin | Typed pin `path`; `disablePreviousMappins` | `Active`, `Inactive`, `Out`, `CutDestination` | [Lab 3](../world/lab-03.md) |
| Phase / `questPhaseNodeDefinition` | Invoke an inline or external child phase | External form: `phaseResource`, null `phaseGraph`, and `phaseInstancePrefabs` | Parent/child interface names such as `In1`, `Out1`; `CutDestination` | [Lab 4](../questphases/lab-04.md) |
| SpawnManager / `questSpawnManagerNodeDefinition` | Issue community/spawner actions | `actions[]`; Lab 5 uses `questCommunityTemplate_NodeType` | `In`, `Out`, `CutDestination` | [Lab 5](../scenes/lab-05.md) |
| Checkpoint / `questCheckpointNodeDefinition` | Establish an explicit quest checkpoint in the supplied lifecycle | Checkpoint flags and containing graph position | `In`, `Out`, `CutDestination` | [Lab 5](../scenes/lab-05.md) |
| Scene / `questSceneNodeDefinition` | Start an archived scene at a world marker and receive named results | `sceneFile`, `sceneLocation`, interruption fields | Named entry inputs and exit outputs; interruption/return outputs; `CutDestination` | [Lab 5](../scenes/lab-05.md) |

### Input and output have two socket layers

In an external child, the parent interface and the child's internal flow are
different layers:

```text
parent phase node In1
  -> child input socketName In1
       -> child input node Out

child work
  -> child output node In
       -> child output socketName Out1
            -> parent phase node Out1
```

`In1` and `Out1` are CName interface values in this arrangement. They are not
universal requirements for every phase node. **Observed in vanilla**, a
focused external phase node also exists with `In1` but no `Out1`. See [Inputs
and outputs](../questphases/inputs-and-outputs.md).

### Journal and mappin state comes from the incoming socket

For `questJournalNodeDefinition`, the same path can receive different
operations:

| Input | Requested journal state |
| --- | --- |
| `Active` | Activate the target entry |
| `Inactive` | Inactivate it |
| `Succeeded` | Mark it succeeded |
| `Failed` | Mark it failed |

For the quest-pin form of `questMappinManagerNodeDefinition`, the focused
inputs are `Active` and `Inactive`. `disablePreviousMappins` is transition
policy; it does not replace the state socket. In either node, `Out` proves
only that graph execution continued after the request, not that the UI was
visibly redrawn.

## Quest control-flow nodes

Graph-level logical nodes combine execution signals. They do not replace a
`questLogicalCondition` tree inside Condition or Pause Condition.

| RED type | Structural role | Socket/property shape | Evidence boundary |
| --- | --- | --- | --- |
| `questLogicalAndNodeDefinition` | Join-shaped convergence | `inputSocketCount`, `outputSocketCount`, numbered ordinary sockets | **Observed in vanilla:** 2–11 inputs and one output in the retained corpus; arrival memory and save restoration are not established by the type name |
| `questLogicalXorNodeDefinition` | Race-shaped convergence | `inputSocketCount`, `outputSocketCount`, numbered ordinary sockets | Lab 2's exact two-input/one-output shape is **Structurally validated**; automatic loser cancellation is not implied |
| `questLogicalHubNodeDefinition` | General structural routing | Counts plus ordinary input/output sockets | **Observed in vanilla:** split, merge, and 1→1 shapes all occur; “fan-out node” is not a complete definition |
| `questSwitchNodeDefinition` | Map conditions to case sockets | `conditions[]`, each `socketId`; `Case<socketId>` and `Otherwise` outputs | **Observed in vanilla** for one retained switch; ordering and `Otherwise` runtime policy remain **Experimental** |
| `questCutControlNodeDefinition` | Emit an explicit cut toward named targets | ordinary `In`/`Out` plus `CutSource` | `CutSource`→`CutDestination` edges are **Observed in vanilla**; rollback, propagation, persistence, and re-arm behavior are not inferred |

Use [Signal flow: joins, races, hubs, and
switches](../gates/signal-flow.md) for the retained counts and [Parallel
monitors and cancellation](../gates/monitors-and-cancellation.md) before
wiring cuts.

## Other quest node families introduced by the book

| RED type | Job | Decisive payload | Evidence route |
| --- | --- | --- | --- |
| `questRewardManagerNodeDefinition` | Grant one or more reward records | `questGiveReward_NodeType.rewards[]` | The focused arrangement is covered in [Rewards and completion](../journal/rewards-and-completion.md); it is not a Labs 1–5 dependency |
| `questPuppetAIManagerNodeDefinition` | Request a puppet AI tier or operation | Target entity reference and operation-specific fields | Lab 5 wraps one Cinematic-tier request inside `scnQuestNode`; see [Entry, exit, and quest handoff](../scenes/entry-exit-and-quest-handoff.md) |
| `questMiscAICommandNode` | Assign or clear a temporary scripted AI role | Typed command params, target actor, follow/path/role data | [AI roles, behavior, and workspots](../communities/ai-roles-behavior-and-workspots.md) |
| `questUseWorkspotNodeDefinition` | Put a selected actor into a world or scene-local workspot contract | Actor reference plus versioned workspot params/instance ID | [Animation events and workspots](../scenes/animation-events-and-workspots.md) |
| `questInteractiveObjectManagerNodeDefinition` | Issue a typed operation to an interactive object/device | `questDeviceManager_NodeType`, controller/action names, target and action properties | [Advanced devices and interactions](../world/advanced-devices-and-interactions.md) |

These manager nodes perform their own operation only. A reward node does not
set a completion fact or succeed the journal, and a PuppetAI request does not
finish a scene.

## Socket vocabulary

| Socket name or type | Local meaning | Common mistake |
| --- | --- | --- |
| `In` / `Out` | Ordinary internal entry and continuation | Treating `Out` as proof that an external system visibly completed |
| `In1` / `Out1` | First named phase interface or numbered logical socket, depending on node type | Assuming the text has one global meaning or that every phase exposes both |
| `True` / `False` | Results of an immediate Condition node | Expecting the `False` route to wait and later become `True` |
| `Active`, `Inactive`, `Succeeded`, `Failed` | State-operation inputs on journal-like manager nodes | Looking only at the node payload and ignoring which input the edge reaches |
| `Case<n>` / `Otherwise` | Switch outputs mapped from condition items | Assuming case evaluation order from array order |
| `CutSource` | Explicit cancellation source on a Cut Control | Wiring it as ordinary success flow |
| `CutDestination` | Target for a cut edge | Assuming an unwired destination provides automatic cleanup |
| Scene entry name, such as `start` | Input on `questSceneNodeDefinition` matching a scene `entryPoint` | Using the scene Start node's numeric ID as the caller interface |
| Scene exit name, such as `contact_done` | Output on `questSceneNodeDefinition` matching a scene `exitPoint` | Inventing an `end` output because the scene contains an End node |
| `<scenario> INT` / `<scenario> RET` | Quest-scene outputs associated with scene interruption and return policy | Treating them as normal completion without a tested interruption design |

The socket `type` remains decisive. A socket named `CutDestination` has the
cut-destination role; it is not an ordinary input merely because another
record also contains the text `In`.

## Lab 5 scene-caller socket contract

The completed First Contact child uses this exact
`questSceneNodeDefinition` interface:

| Socket | Type | Connection |
| --- | --- | --- |
| `CutDestination` | `CutDestination` | Unconnected |
| `start` | `Input` | From the child route after community readiness and broad setup |
| `contact_done` | `Output` | To the meet-success and cleanup route |
| `Default INT` | `Output` | Unconnected |
| `Default RET` | `Output` | Unconnected |

The resource shape is **Structurally validated**. Active-line interruption,
return, and cut behavior remain **Experimental** outside Lab 5's frozen
acceptance cases.

## Scene graph node index

Scene nodes use `scnNodeId` and scene socket stamps. They do not use
`questSocketDefinition` directly, except when `scnQuestNode` wraps a quest
node.

| Scene RED type | Job | Boundary data |
| --- | --- | --- |
| `scnStartNode` | Receive the published `start` entry and fan one `0/0` output to two destinations | Listed in `sceneGraph.startNodes`; targeted by `entryPoints[].nodeId` |
| `scnSectionNode` | Own actor behavior, timed line events, duration, and normal/cancel outputs | Normal `0/0` reaches End; cancel `1/0` is unconnected in the fixture |
| `scnQuestNode` | Wrap a scene-local quest node; First Contact wraps `questPuppetAIManagerNodeDefinition` | Input/output mappings connect scene stamps to the wrapped quest sockets |
| `scnEndNode` | Terminate the normal scene route | Listed in `sceneGraph.endNodes`; targeted by the named `contact_done` exit |
| `scnChoiceNode` | Present scene-local screenplay options and route the selected branch | Option-to-screenplay IDs, choice conditions, output ordinals, and later named exits are separate joins |
| `scnRewindableSectionNode` | Own a seekable/rewindable timed-event collection | Playback strategies, duration, RID/clue/camera events, and side-effect reconstruction policy |

The exact scene topology is:

```text
                         +-> Section 2 -> End 3 [contact_done]
Start 1 -- one fan-out --+
                         +-> scnQuestNode 4 / PuppetAI [fire-and-forget]
```

The PuppetAI branch has no output destination and does not join the line
branch. The section alone reaches End. See [Entry, exit, and quest
handoff](../scenes/entry-exit-and-quest-handoff.md).

## Scene socket stamps are name/ordinal pairs

The First Contact scene supplies this exact stamp table:

| Source | Output stamp | Destination | Input stamp |
| --- | --- | --- | --- |
| Start `1` | name `0`, ordinal `0` | Section `2` | name `0`, ordinal `0` |
| Start `1` | name `0`, ordinal `0` | PuppetAI wrapper `4` | name `0`, ordinal `1` |
| Section `2` normal | name `0`, ordinal `0` | End `3` | name `0`, ordinal `0` |

The two Start connections are one output fan-out, not two differently stamped
outputs. The wrapper's input ordinal `1` selects its mapped internal `In`; its
ordinal `0` is reserved for the `CutDestination` mapping. Treat ordinals as a
node-local contract, not whole-scene execution order.

## Review checklist

Before diagnosing a graph from its labels:

1. Name the containing questphase or scene graph as well as the node ID.
2. Confirm the concrete RED type and every non-null typed payload handle.
3. Trace each edge by source socket and destination socket.
4. Distinguish one socket with several connections from several sockets.
5. Distinguish a quest socket from a scene socket stamp.
6. Confirm every phase input/output and scene entry/exit name on both sides.
7. Inventory parallel waits, delays, scenes, community operations, and cut
   targets before permitting termination.
8. Apply the evidence label of the exact arrangement, not the reputation of
   the node name.
