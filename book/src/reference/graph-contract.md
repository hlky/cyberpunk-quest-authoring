# Reading graph diagrams

Graph diagrams show node IDs, concrete RED types, socket names, and
connections. Match these to your WolvenKit resource; editor positions and
CR2W handle numbers can differ.

## Follow execution

- Follow solid arrows for normal execution.
- Read the source and destination socket names beside each connection.
- Follow dashed red arrows for cut or interruption routes.
- Treat dotted links as resource lookups rather than execution edges.
- Check node-detail tables for conditions and properties too large to fit in
  the figure.

## Distinguish the views

| View | Use it to understand |
| --- | --- |
| Story flow | What the player does and sees |
| Exact node graph | Which node types and sockets implement the route |
| Resource map | Which files own the graph, world objects, text, or actors |

A graph node ID identifies the node. A CR2W handle connects objects inside one
resource, while a NodeRef locates a world object. See
[Identifier domains](../foundations/identifier-domains.md) before comparing
numbers across these views.
