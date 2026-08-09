# Handles, sockets, and resource references

Three kinds of connection often look alike in WolvenKit: an internal CR2W
handle, a graph socket edge, and a path to another resource. They fail at
different times and need different tests.

## Evidence and version boundary

Use Cyberpunk 2077 Windows GOG `2.31a`, WolvenKit `8.19.0`, ArchiveXL
`1.27.0`, RED4ext `1.30.0`, and redscript `0.5.31` for the practical checks.

**Structurally validated:** the lab validators resolve internal handles,
freeze semantic graph edges and socket contracts, and verify decisive external
resource paths after WolvenKit `8.19.0` round trips.

**Observed in vanilla:** the node/socket and handled-object shapes taught in
the foundations and scene chapters occur in the cited extracted vanilla
resources. Incidental `HandleId` allocation is not treated as a stable engine
meaning.

**Experimental:** any changed runtime route remains experimental until its
exact packed bytes pass the relevant clean-save cases. Structural repair does
not prove lifecycle behavior.

## Identify the connection domain

| Connection | Typical form | Scope | Question |
| --- | --- | --- | --- |
| CR2W handle | `HandleId` / `HandleRefId` | One serialized CR2W object graph | Which object does this field own or reference? |
| Quest graph edge | Source socket to destination socket | One questphase graph | Which output causes execution to enter which input? |
| Scene graph stamp | Named/ordinal socket stamps and destinations | One scene graph | Which stamped route joins these nodes? |
| External resource | `ResourcePath`, often hard or soft | Virtual depot | Does the packed/registered resource exist at this exact path? |
| World identity | `NodeRef` | Streaming/world namespace | Is a loaded world resource registering this identity? |

A graph node ID is not its CR2W `HandleId`. A NodeRef is not either one. See
[Identifier domains](../foundations/identifier-domains.md) before editing a
number merely because it resembles another identifier.

## Diagnose an internal handle failure

Symptoms include conversion errors, a missing nested object after round trip,
an edge whose destination disappears, or a crash when a handled payload is
first used.

1. Serialize the binary back to an isolated review file.
2. Inventory every `HandleId` and every `HandleRefId` in the affected CR2W.
3. Require each reference to resolve to exactly one compatible object.
4. Check ownership: two fields may intentionally reference one object, but a
   copied node must not accidentally alias the old node's sockets or payload.
5. Inspect the target object's RED type, not only the matching number.
6. Reopen the binary in WolvenKit and verify the nested object is still owned
   by the intended field.

Let WolvenKit maintain handle identities through normal editor operations.
When comparing round trips, compare the resulting object relationships rather
than requiring the same incidental numbers.

> A legacy research tool once required referenced objects to have already
> appeared in its serialized traversal. Treat that as a tool-specific
> constraint, not a universal authoring rule. The portable requirement is
> that the final CR2W object graph resolves every reference correctly.

## Diagnose a socket failure

Start with the source and destination nodes and write the intended edge in one
line:

```text
node 12 / Out  ->  node 13 / Active
```

Then verify:

1. the source socket is an output or the node type's corresponding source
   role;
2. the destination socket is an input with the intended operation semantics;
3. spelling and case match the concrete socket contract;
4. both socket handles still belong to their intended nodes after round trip;
5. the source connection targets the destination socket, not merely the
   destination node;
6. a parallel fan-out is deliberate and does not masquerade as an ordered
   sequence;
7. a `CutDestination` route is not connected to normal success by accident.

Journal nodes are a common example: entering `Active`, `Succeeded`, or
`Inactive` on the same node can produce three different state changes. A
visible edge is not correct merely because it reaches the right box.

For a child questphase, compare both sides of its public interface:

```text
parent phase-node input  In1  -> child questInputNodeDefinition In1
child questOutputNodeDefinition Out1 -> parent phase-node output Out1
```

The parent can resolve the child resource and still stall if the socket names
or terminating output contract do not match.

## Diagnose a resource-reference failure

An internal handle can be valid while the object it owns contains a missing
external path. Trace the external edge separately:

1. copy the exact `ResourcePath` from WolvenKit;
2. identify whether the reference is hard, soft, or reached through a
   registered map/block;
3. list the archive and confirm the target path exists;
4. inspect any intermediary owner, such as a subtitle map's entries path or a
   streaming block descriptor's sector path;
5. check ArchiveXL logs for registration/merge errors;
6. confirm the target resource's root type is compatible with the referring
   property.

Do not repair a missing `ResourcePath` by changing a `HandleRefId`; the handle
may correctly point at the soft-reference object whose path is wrong.

## Address indexed resource tables

Some scene fields select a row in a resource table. The actor's index and the
table cardinality form one contract:

```text
maximum referenced index < number of addressable cooked rows
```

Duplicate source rows do not guarantee duplicate runtime rows. If two entries
resolve to one cooked import while an actor requests index `1`, conversion can
succeed and runtime can still perform an out-of-range lookup. Inspect the
round-tripped resource-reference array and every consumer index. The dedicated
[Actors, scenes, and lipsync](actors-scenes-lipsync.md) guide applies this to
lipsync slots.

## Minimal repair loop

| Failure | Smallest safe correction |
| --- | --- |
| Dangling handle | Recreate the referenced nested object through WolvenKit and reselect it from the owning property |
| Wrong shared ownership | Duplicate through an editor operation that creates an independent object, then rewire its fields |
| Missing graph edge | Connect the exact named source and destination sockets |
| Wrong operation socket | Reconnect to the intended semantic input, such as `Succeeded` rather than `Active` |
| Missing external path | Correct the ResourcePath or pack/register its target; do not alter internal handles |
| Indexed table too short | Supply addressable distinct resources or reduce consumers only as an explicit diagnostic |

Round-trip after each correction. If several edges are repaired at once, a
passing result cannot identify which defect caused the original symptom.

Previous: [Registration and depot paths](registration-and-depot-paths.md).
Next: [NodeRefs, streaming, and
placement](noderefs-streaming-placement.md).
