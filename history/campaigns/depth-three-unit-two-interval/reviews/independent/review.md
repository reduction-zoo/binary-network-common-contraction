# Independent review

Date: 2026-09-15. Decision: **advance** to manuscript preparation and expert review.
This is a native independent-agent review, not human validation or publication acceptance.
No blocking correctness gap or matching prior theorem was found. Novelty is supported
within the explicit literature coverage below, not certified against all unpublished work.

## Scope and evidence

Reviewed the fixed question, current `work/algorithm.py`, `work/contract.md`,
`work/proof.md`, the linked `rounds/004/argument.md`, preparation and verification
reports, round 005 development/literature record, round 006 encoding record and
completed logs, and the central-deletion and compressed-variable experience entries.
The central-deletion entry's local experiments are not used as a general theorem:
the full composition premises are checked below.

The reported current complete-rule counts agree with the logs: five prepared
sources and six recoveries; nine extended sources and fourteen recoveries.
The two harnesses share their target solver and are correlated evidence.
I did not rerun them or import their implementations.

Reviewer-owned checks, run from the repository root:

```
python3 campaigns/depth-three-unit-two-interval/reviews/independent/check.py
python3 campaigns/depth-three-unit-two-interval/reviews/independent/full_check.py
```

`check.jsonl` records ten exact QF_LRA checks. Eight local variable masks admit
exactly the neutral, both-positive-free, and negative-free states. The printed
binary mask orders bits as n,q,p, whereas the proof writes p,q,n. The remaining
checks exclude a two-clause with neither incident port free and a three-clause
with no free positive port. This encoding uses real endpoints directly, own-slot
disjointness, and all adjacency/nonadjacency constraints. It imposes neither
depth cuts nor forbidden-subgraph clauses. External q neighbors in the
three-clause query are private black leaves; any restriction of a full
counterexample would satisfy this weaker local instance. These are finite
solver results, not proof certificates for arbitrary formula sizes.

`full-check.jsonl` records two successful actual extractor calls on a separately
constructed 234-vertex witness for source `[1,-2,10^100]`, with declared n=10^100.
Its formula-core coordinates were hand designed; only the constant-size published
black attachment was solved with a reviewer-owned real model. Every edge,
nonedge, own-component disjointness constraint, and the depth bound was checked
with exact fractions against the actual candidate output. Reflection, selected
row reversals, and translation by 10^80/97 also passed. Both recovered sparse
assignments satisfy the source and respect its declared variable indices.
This independently exercises graph construction, attachment, and backward
execution without either campaign target solver.

## Correctness: supported

**Normalization and composition.** `algorithm.py:12–28` implements the argument
at `rounds/004/argument.md:71–85`. Removing tautologies and expanding a deduplicated
unit or two-literal clause preserves satisfiability in both directions. The
fresh indices exceed n and therefore cannot collide with an original variable.
Duplication ensures each occurrence cycle has length at least two. Even at
length two, the two directed cycle clauses use different q/n ports, so no loop
or duplicate edge appears. Each occurrence variable has exactly one positive
triple incidence and one incidence of each sign in the cycle clauses.

The signs in `algorithm.py:37–38` are correct: the outgoing port represents
not b_i and the incoming port represents b_j. A satisfying cycle forces all
b_i equal. Conversely, a satisfying normalized assignment sets y_i to the
truth value of its signed occurrence and satisfies all triples and implications.
Distinctness within clauses holds after occurrence splitting, including when
source clauses repeat literals. Empty or entirely tautological formulas map
to the empty graph and recover the valid default-false assignment.

**Color removal and arbitrary witnesses.** The private attachment is exactly
the published graph. The cited coverage premise applies to the restriction
of any target representation to that attachment. An interval covered by private
center intervals cannot intersect any component of an old neighbor, because
that neighbor is nonadjacent to both private centers. Every constructed black
vertex has positive old degree. Thus exactly one component is active, as
required by `algorithm.py:58–61`. This also covers black-black edges: neither
endpoint's discarded component can participate in an old edge. Consequently
simultaneous deletion produces the claimed colored representation.

**Variable lemma.** `rounds/004/argument.md:18–25` correctly obtains unique
black-to-port component incidence from a unit-interval claw obstruction.
A component free from A and B forces its other component to bridge them.
Opposite-sign bridges yield an induced four-cycle. In the asymmetric-positive
case at lines 27–33, n must split; the proposed net really is induced:
n_A meets only A among its triangle vertices, the external neighbor E only
p_A, and B only the q bridge. The symmetric argument is legitimate because
q's L is external and nonadjacent to the other internal vertices. All full
p and q ports have the required external neighbor. Thus neutral states are
allowed but unequal positive-port freeness is impossible.

**Clause coverage.** At `rounds/004/argument.md:39–48`, when p uses both
components externally, the q component meeting its own L selects an A/B side
where p has a clause neighbor. The six named components form the claimed net.
In particular, that L is not adjacent to any p vertex; this is a port-specific
premise preserved by the occurrence construction. The n component may bridge
A and B when n is free, but this causes no extra edge within the six chosen
vertices, because B is absent from this net. If every p uses only one component
externally, those three components realize all three triangle edges and their
three variable-specific black neighbors are independent private leaves.
No assumption of a unique component representative for every graph edge is
being smuggled into either argument.

At lines 52–58, P and unit length force L to meet exactly one component of
each port and force those two components to meet each other. When neither is
free, its own variable supplies an A/B leaf. The two variables are distinct,
and neither selected black leaf has an edge into the other variable. Hence
the two-clause net is also induced. Every clause therefore has a free literal.

**Recovery.** `algorithm.py:65` tests precisely whether either positive port
has a component disjoint from both retained black intervals. By the variable
lemma this equals the stated y_i assignment. Sign exclusivity makes every
free negative literal true when y_i is false, including neutral variables
assigned false. Clause coverage satisfies the entire occurrence formula.
Line 70 reads the signed cycle value and discards fresh normalization variables;
this yields a source assignment. Exact absolute differences make the reasoning
independent of reflection, slot order, coordinates, or how an edge is duplicated
among component intersections. The extractor need not validate arbitrary
invalid graph representations: its theorem has a valid-witness premise.

**Completeness, graph restrictions, and size.** The occurrence formula meets
all four premises of the published normalized SAT lemma. Adding C back to
each candidate variable produces the published colored formula graph, with
the same port-specific clauses. Its YES representation can therefore be
restricted and then extended by private attachments. No reverse implication
is inherited from induced deletion; the new soundness argument supplies it.

The K4-free argument at `work/proof.md:104–115` holds. In particular, white
cliques cannot extend a p triple through a q edge, and different attachments
meet only their respective roots. Four simultaneously overlapping components
would belong to four different vertices and force K4. Thus every target
representation already has depth at most three. Degrees are A/B=5, p=q=5,
n=4, L=5, P=3, private centers=5, private leaves=1. Counts 39N vertices and
48N edges follow directly, with N at most 24m.

**Encoding and bit complexity.** The maps never iterate to the declared n.
Their integer labels have input-polynomial bit length. Sparse recovery writes
each mentioned original index at most once and omits all unused variables;
the O(ell) witness-size claim is justified by indices already present in the
source. Fraction parsing and bounded-degree comparisons on explicit rational
strings have polynomial bit cost; the conservative bounds at
`work/proof.md:119–138` suffice. Scientific notation is excluded consistently.
The difference-constraint argument at lines 142–156 is sound: a feasible
simple cycle containing a strict edge has positive integer constant sum, so
the specified uniform slack preserves feasibility and the whole component
intersection graph. For compressed isolated target vertices, the NP assertion
at lines 157–161 uses a compressed core certificate plus an implicit placement;
it should not be read as promising polynomial length for a fully enumerated
`left` array on every such target. This distinction does not affect either map
or the candidate hardness theorem.

## Novelty: supported within recorded coverage

Primary sources checked on 2026-09-15:

- [Ardévol Martínez, Rizzi, Sikora, Vialette, DAM 360 (2025)](https://www.sciencedirect.com/science/article/pii/S0166218X24004013),
  Theorem 18, Corollary 24, and Section 4: the baseline is degree-seven
  unrestricted recognition hardness, depth-four hardness, and an explicit
  remaining depth-three question. In the
  [arXiv preprint](https://arxiv.org/pdf/2309.11908), I checked Lemma 1
  (page 5), Lemma 12 (pages 11–13), and Claims 18–20 (pages 17–18).
  These supply the inherited normalization premises, YES construction,
  and color-removal mechanism, not central-deletion soundness.
- [Ardévol Martínez et al., MFCS 2024](https://drops.dagstuhl.de/storage/00lipics/lipics-vol306-mfcs2024/LIPIcs.MFCS.2024.12/LIPIcs.MFCS.2024.12.pdf),
  Section 4 and Theorem 8: disjoint and non-disjoint unit representations
  differ. Its interval-graph characterization does not settle this target.
- [Jana, Roy, Sandeep, arXiv:2607.13517](https://arxiv.org/pdf/2607.13517),
  Section 8, Proposition 28 and Theorem 5 (pages 20–23): the vertex-splitting
  reduction replaces black vertices by growing cliques and uses a total split
  budget. It provides no depth-three or K4-free consequence of the required form.

Independent queries included `"unit 2-interval" "depth" recognition 2026`,
`"unit 2-interval" "depth three"`, `"unit 2-interval" "depth 3"`,
`"K4-free" "2-interval"`, `"unit 2-interval" "K_4" recognition`,
`"unit 2-interval" recognition degree five`, and
`"unit interval number" recognition two depth`, as well as the baseline title
and 2025/2026 follow-ups. No matching theorem was located. Searches of equivalent
formulations were evaluated mathematically: K4-freeness is a sufficient condition
for the depth bound, not an equivalence on arbitrary graphs; vertex splitting
must preserve the per-vertex two-component bound and disjointness; hardness of
a larger representation class alone does not imply this recognition result.

Coverage is not an exhaustive citation graph or a search of all theses and
unindexed manuscripts. Those limits remain unresolved. Within the inspected
literature, the new content is the general soundness of central deletion with
neutral states retained, yielding the depth-three restriction. It is more than
an implementation of the published construction.

## Significance: supported

The result answers the fixed d=2 depth-three question and strengthens hardness
to K4-free graphs of maximum degree five. The new argument explains why clause
coverage survives loss of the old two-state truth interface, rather than merely
reducing a gadget's size. This meets the campaign's requirement for an original
deterministic Karp reduction with universal witness recovery and a general proof.
No higher-dimension theorem follows automatically. The manuscript should keep
that scope and the inherited ingredients explicit.

There are no required mathematical or implementation repairs from this review.
Advance denotes eligibility for careful expert assessment, with the literature
coverage limitation preserved.
