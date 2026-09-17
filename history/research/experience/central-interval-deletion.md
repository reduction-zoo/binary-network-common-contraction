# Deleting a central interval changes the truth interface

Tags: unit 2-interval, depth three, black-free ports, partial assignment.

## Claim and applicability

Consider black one-interval A,B and white two-interval p,q,n, with all six
black-white edges and pq. With one private black leaf on each white vertex,
depth-three representations allow exactly black-free masks 000,001,110.
A port is black-free if one of its components avoids both A and B. In
particular, deleting C from the published variable gadget does not preserve
its two-state classification. This claim is only for this colored graph.

## Evidence and status

Exact QF_LRA finite-family classification with independently fraction-checked
positive witnesses in [round 002](../../campaigns/depth-three-unit-two-interval/rounds/002/round.md).
The local classification and its full composition were subsequently
[independently reviewed](../../campaigns/depth-three-unit-two-interval/reviews/independent/review.md).
The published exclusion of 000 uses C in
Claim 9 of [the preprint](https://arxiv.org/pdf/2309.11908).

## Consequence for search

Do not reuse the published full-assignment extraction after deleting C.
Either forbid 000 or prove every clause has a free port, so partial assignments
suffice. Local availability alone does not settle formula soundness.

## Use history

[Round 003](../../campaigns/depth-three-unit-two-interval/rounds/003/round.md)
used the neutral-state observation to test partial-assignment clause coverage.
Four local counterexample queries were UNSAT and seven positive assignments
were representable. This supports continuation but does not prove coverage in
the formula graph: the probes use mutually nonadjacent private leaf vertices.

[Round 004](../../campaigns/depth-three-unit-two-interval/rounds/004/round.md)
derived a conditional general clause-coverage proof: choose the positive
companion's private black L as the external leaf in the net argument. This
removes the need to force a free sign at every variable. At that round the derivation was conditional; subsequent composition and
independent review are recorded below.

[Round 005](../../campaigns/depth-three-unit-two-interval/rounds/005/round.md)
completed the graph construction and conditional full proof. The final prepared
suite passed five sources and six recoveries; extended verification passed seven
sources and ten recoveries. That round exposed a sparse-source encoding repair, completed in round 006.
The subsequent independent review advances the general central-deletion proof
and both maps without required repairs. Its own direct-real checks and hand-built
full witness passed. Expert human assessment and the stated literature coverage
limits remain; finite local tests alone are not the proof.


[Binary-network round 4](../../campaigns/binary-network-common-contraction/rounds/004/round.md) reused the question of whether
clause coverage permits partial recovery. It helped replace the unnecessary
full-assignment premise by a connected-bag argument; no interval-graph lemma was
transferred to contractions. The round checked 128 set families and 3,456 partial
partitions. [Round 6](../../campaigns/binary-network-common-contraction/rounds/006/round.md) completed that contraction-specific
argument, subsequently independently reviewed. This is a useful cross-problem
search analogy, not evidence that the original geometric assumptions apply.
