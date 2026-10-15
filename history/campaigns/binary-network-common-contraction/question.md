---
status: proof-route-hold
openness: explicit-2025-question-no-later-resolution-found
difficulty: uncertain
importance: moderate
tags: phylogenetics, binary-networks, contractions, NP-hardness
last-literature-check: 2026-09-16
---

# Set Splitting to binary-network common contraction

Not admitted. The primary source leaves the binary case open, but neither a
degree-reduction construction nor an alternative source transformation has
been established. An initial direct tree-display route has a counterexample.

## Fixed prospective target

Input: two finite simple rooted DAGs on the same uniquely labeled leaves and
a binary integer k. Each root has outdegree two; each leaf has indegree one;
every other vertex has indegree/outdegree (1,2) or (2,1). Accept if both networks
can be contracted into leaf-preservingly isomorphic networks with at least k
internal vertices. A contraction merges the endpoints of an internal edge,
removes loops and duplicate arcs, and is allowed only if the resulting graph
is acyclic. Intermediate networks and the common contraction may be nonbinary.

The source is Set Splitting: an explicitly listed finite set and family of
subsets, asking for a two-coloring under which every listed subset has both
colors. Seek a total deterministic polynomial Karp map into the target and
polynomial recovery of such a coloring from every valid target witness.
Malformed sources may map outside the target language. Well-formed sources
must always produce binary input networks, including on NO instances.

A target witness consists of both contraction sequences and their final
leaf-preserving isomorphism. Each sequence has at most the initial number of
internal vertices minus one steps. With explicit vertex identifiers, witnesses
have polynomial length and can be verified by direct graph operations.
The intended local-gadget approach needs polynomially many output vertices,
edges and label bits in the explicit source length. No forward or recovery
algorithm meeting these bounds is yet available.

## Literature and significance

Marchand et al.,
[Finding maximum common contractions between phylogenetic networks](https://link.springer.com/article/10.1186/s13015-025-00283-9),
October 1, 2025, Theorem 9 proves hardness at degree at most ten. The paragraph
following it and the conclusion leave binary networks open. Theorem 11 uses
five leaves and one tree but permits high degree in the other network.
The source appeared earlier at
[WABI 2024](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.WABI.2024.16)
and has [arXiv record 2405.16713](https://arxiv.org/abs/2405.16713).

One introductory sentence in the construction calls its networks binary, but
the actual degree calculation in Theorem 9 has vertices of degree ten and
explicitly leaves the binary restriction open. That sentence cannot justify
claiming an existing binary hardness result. The precise binary input contract
above also avoids applying degree three to roots and leaves.

Importance is provisionally moderate: success would classify common-structure
comparison on the standard binary network class. It does not automatically
classify the different contraction-expansion edit distance, which the paper
distinguishes from maximum common contraction.

## Initial investigation

The [nine-vertex counterexample](../evidence/binary-network-contraction/README.md)
has a displayed balanced four-leaf tree that cannot be obtained by admissible
contractions. All eighteen admissible two-contraction histories fail the
required leaf-preserving isomorphism. Thus passing Tree Containment inputs
unchanged to common contraction does not preserve YES instances. Deleting
reticulation edges must be simulated by a new construction; it cannot be
silently replaced by contractions. No such simulation is established.

## Search and admission

Searches on 2026-09-16 included `"maximum common" "contraction" "binary" phylogenetic 2026`,
`"directed" "contraction" "binary" phylogenetic`, and
`"Finding maximum common contractions" arxiv`. No matching later resolution
was located. The journal definitions, degree calculation and conclusion were
inspected; the full later citation trail remains incomplete. Separate searches
for P4 contractibility did not establish a matching directed, leaf-labeled
binary-network theorem. Undirected contractibility is not interchangeable.

Gate 1 passes for the prospective Karp contract. Gate 2 passes within the
inspected restrictions. Gate 3 passes provisionally within the stated coverage.
Gate 4 passes at moderate importance. Gate 5 is on hold: a degree-three gadget
that keeps the contraction choices consistent is missing. Gate 6 is not passed;
the alternative identity map failed the finite check. Difficulty is uncertain,
and the present evidence does not support a moderate-difficulty admission.

Resume only after specifying a binary replacement gadget with a checkable
converse, or a transformed tree-containment route that avoids the saved
counterexample. No campaign or round allocation has started. No shared
experience entry was created; the counterexample remains in its evidence file.
