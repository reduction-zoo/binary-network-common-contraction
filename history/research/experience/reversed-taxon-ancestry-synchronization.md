# Reversed taxon ancestry synchronizes every port inside a directed interval

Tags: binary phylogenetic network, common contraction, leaf labels, all-port spine.

## Claim and applicability

If taxon x's parent reaches taxon y's parent in one input, and their order is
reversed in the other, every leaf-preserving common acyclic contraction identifies
these two parent images. Every vertex between the parents on either directed
path shares that image. External attachments are allowed if the ancestry paths,
unique leaf labels and acyclic common-quotient semantics are preserved.

For d incoming and e>=1 outgoing ports, place all ports on a binary spine between
two auxiliary leaf parents: first parent, d-1 reticulations when d>0, e-1 tree
vertices, last parent. The spine has d+e vertices for d>0 and e+1 for d=0.
Forcing endpoint-parent equality synchronizes every port, including incoming
reticulation ports. Synchronization alone does not force a truth assignment.

## Evidence and status

This is an application of known ancestry reasoning: Marchand et al.,
[Proposition 7 and Figure 3](https://doi.org/10.1186/s13015-025-00283-9).
[Round 2](../../campaigns/binary-network-common-contraction/rounds/002/round.md) proves the path statement and checks an
11-vertex pair with twelve queries and three realized positive witnesses.
[Round 5](../../campaigns/binary-network-common-contraction/rounds/005/round.md) proves the port count and checks sixteen
interfaces with d,e in 1..4. The root case is covered by the full construction.
The complete composition's [independent review](../../campaigns/binary-network-common-contraction/reviews/complete-rule/review.md)
advances the general synchronization argument; human expert assessment remains.
The primitive is not claimed as a novel discovery.

## Consequence for search

Bracket all ports, not just outgoing branches. Then separately check the
objective and solution-recovery premise: a synchronized bag may remain free.
Do not infer source-choice enforcement from endpoint equality alone.

## Use history

[Round 3](../../campaigns/binary-network-common-contraction/rounds/003/round.md) used synchronization successfully but exposed
an objective that rewards a free variable bag. [Round 6](../../campaigns/binary-network-common-contraction/rounds/006/round.md)
combined all-port spines with fixed-group cherries, partial recovery and marked
separation paths; the full rule passed independent review.
