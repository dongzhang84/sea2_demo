# João Opening Topology v1

This is the first João-opening topology export that includes candidate control-flow edges.

## Summary

- nodes: 142
- sequence_edges: 141
- candidate_control_edges: 63
- near_control_edges: 4
- high_confidence_control_edges: 13
- medium_confidence_control_edges: 50
- low_confidence_control_edges: 4

## Interpretation

The graph is still a candidate execution topology, not a fully runtime-confirmed VM trace. The important shift is that João opening now has explicit non-sequence edges derived from `ad/ac/8c/fe` operands.

High confidence means the operand lands exactly on a known timeline start/end. Medium means it lands inside a known timeline item. Low means it is within four bytes of a known boundary.

## Files

- `output/sndt_topology/joao_opening_topology_v1.json`
- `output/sndt_topology/joao_opening_topology_v1.dot`
- `output/sndt_analysis/joao_control_edges.json`
