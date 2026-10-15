# Independent complete-rule review

Date: 2026-09-16. Decision: **advance**.

The submitted theorem, construction and arbitrary-witness recovery are supported
by the general argument and executable checks below. I found no material
correctness gap. The binary-input hardness contribution is supported relative
to the inspected primary literature and meets the fixed significance criterion.
This is eligibility for expert review, not publication acceptance or a guarantee
of priority. Literature coverage remains bounded.

## Scope and independence

I read the repository instructions and README, fixed question, contract,
algorithm.py, proof.md, preparation.md, verification.md and literature.md.
The candidate and its two checkers were not modified or imported. My new
[independent_check.py](independent_check.py) invokes both candidate modes in
fresh subprocesses. All reviewer writes are in this review directory. I did
not spawn agents or rerun the author's full suites. The author-reported suites
remain supporting evidence, not independently authored evidence.

## Correctness

**Total map and binary degrees.** The branches in algorithm.py:56–60 cover
empty families and families with a set of size zero or one. Their balanced
four-leaf tree outputs are binary. At k=3, the NO pair cannot contract at all
while retaining three internal vertices, and its leaf splits differ. For every
other legal source, each expanded vertex has at least one outgoing port.
In algorithm.py:19–32 the spine has d+e nodes when d>0, and e+1 at the root.
Its entry and exit nodes are tree nodes, each extra incoming port produces one
reticulation, and each extra outgoing port produces one tree node. All ports
have distinct adjacent endpoints. Sequential replacement changes their names
but not their incidences. Unexpanded path and cherry vertices have degree
(1,2). Thus the entire output, including NO instances, has the stated degrees.
The only zero-indegree node is the first R-spine node, with outdegree two.
Labels and internal identifiers occupy disjoint syntactic namespaces.

**Global forcing.** In proof.md:102–109, each G cherry identifies the two
endpoint-parent images of the corresponding H group spine. A directed path
whose endpoints have equal images in a DAG quotient must have a single image.
The H spine therefore forces the endpoints of every corresponding fixed-group
G spine. This argument does not assume group distinctness. The reversed
variable endpoint parents in proof.md:111–115 likewise imply mutual
reachability, so both variable spines have one common image. Extra incident
ports cannot evade these directed-path arguments.

**Distinctness and the NO direction.** The upper bound in proof.md:117–135
counts every H internal vertex after forced identifications; there are no
unaccounted gadget vertices. R=A loses the whole R–A path and one group,
leaving at most 2+p+L=2p+3<2p+5=k images. A=B also absorbs every variable
and the second path, leaving at most 2+L<k. R=B forces A into the same image.
These are upper bounds for arbitrary witnesses, independent of optimality.

With the group images distinct, each U_j spine is a proper subset of the A
bag because that bag also contains the A spine. Its only possible internal
neighbors outside the spine are R and its incident variables. Hence a
connected A bag must contain an incident variable. The analogous V_j argument
forces an incident B variable. These variables are distinct because their
images differ. This verifies the local cut argument at proof.md:140–147 even
if paths are merged or some variables retain their own images. It establishes
that a target YES cannot arise from a source NO.

**YES direction and admissibility.** The partitions in proof.md:164–179 are
connected: every A-colored variable touches A; each U_j touches at least one
such variable; the B side uses the corresponding V_j incidences. R contains
only its spine and attached cherry. H group connectivity is immediate from
A→X→B. Crossing arcs give exactly the claimed three group arcs and marked
paths, and every label has the same parent image on both sides. This quotient
is a DAG. A connected bag in a DAG quotient can be contracted by repeatedly
choosing a first vertex and its earliest internal successor in a topological
ordering. An alternative path outside the bag would form a quotient cycle;
one inside would contradict earliest choice. Thus admissible sequences exist
globally, not just as isolated gadget contractions.

**Recovery.** algorithm.py:108–114 maintains the image of every original
left vertex. Under the supplied valid-witness premise, u and v are current
identifiers, and replacing every occurrence of max(u,v) by min(u,v) exactly
implements the retained-ID convention. Forced variable synchrony makes its
first spine node sufficient. Comparing it with the B entry node gives the
coloring proved above. Ignoring the right sequence and isomorphism is sound
because their validity is a premise. The explicit ground-set list bounds the
length of the all-zero and general recovered witnesses. Invalid witnesses
are outside the recovery obligation.

**Resources.** The sum of spine port counts is linear in total preliminary
arc count. Both networks therefore have O(p+m+t+1) vertices and arcs; vertex
and taxon names have O(log(n+m+t+2)) bits. Sorting, dictionary operations,
serialization and O(N²) representative updates are polynomial in explicit
source and witness lengths. The stated cubic conservative bounds are adequate.
The decimal digit-cap setting prevents an arbitrary parser cutoff on long
integer tokens. The candidate uses no randomness, oracle, solver or search.
Polynomial sequence lengths, direct acyclicity checks and an explicit
isomorphism certificate establish target membership in NP.

## Independent executable evidence

Command from repository root:

```
python3 campaigns/binary-network-common-contraction/reviews/complete-rule/independent_check.py
```

The [saved run](results.jsonl) passed, exit code 0. It covers eight distinct
sources, five YES and three NO, through nine target solver queries and twelve
fresh-process recovery calls. Largest output orders are 139 and 109. Cases
include empty sources/families, empty and singleton sets, a NO triangle of
two-element sets, overlapping triples, duplicate sets, inactive elements and
multi-digit element identifiers. Two queries on the same four-element source
require two distinct free-variable images. One has at least k+2 quotient
vertices; another also merges two marked-path parents and retains at least
k+1. Both increasing and decreasing admissible-edge orders recover valid splits.

The new solver identifies cross-network leaf parents and collapses strongly
connected components of the combined precedence relation. These are necessary
equalities for every common DAG quotient. It then assigns topologically ordered
bag numbers, imposes the actual >=k condition and exact crossing-arc equality,
and adds connectivity cuts when a proposed bag is disconnected. A cut allows
splitting its component or the other selected member, or adding a boundary
neighbor; therefore it does not exclude a connected bag. The finite assignment
space makes the refinement procedure complete. No source coloring enters the
target solver. SAT partitions are independently realized by direct contraction
and acyclicity checks; final arc and leaf-label isomorphism is checked before
calling recovery. Source decisions are separately enumerated. This is finite
experimental evidence, not a replacement for the preceding proof.

## Novelty and attribution

Primary references inspected on 2026-09-16:

- [Marchand et al., journal article](https://link.springer.com/article/10.1186/s13015-025-00283-9):
  Preliminaries permit unary intermediates. Definition 1 and Proposition 5 match
  the contraction and bag contracts. Theorem 9 gives degree-ten hardness; its
  following paragraph and conclusion leave binary complexity open. Proposition
  7/Figure 3 already uses swapped endpoint leaves to force a star. Theorem 8
  supplies the incidence/connectivity antecedent.
- [WABI predecessor](https://drops.dagstuhl.de/storage/00lipics/lipics-vol312-wabi2024/LIPIcs.WABI.2024.16/LIPIcs.WABI.2024.16.pdf):
  Theorem 16 states the same degree-ten baseline and binary question.
- [Maximum agreement subnetworks](https://www.sciencedirect.com/science/article/pii/S0304397504008102):
  the abstract treats agreement subnetworks, not this contraction relation.

The present all-port synchronization, partial-assignment extraction and
separation-path threshold are not supplied by those statements. I found no
matching later theorem in searches for common/maximum common contraction,
binary phylogenetic networks, Set Splitting, and the authors with 2026. This
supports advancing the specific combination, not claiming endpoint reversal
itself is new. **Nonblocking recommendation:** explicitly cite Proposition
7/Figure 3 alongside proof.md:111–115 and the novelty paragraph. The present
text already claims a new combination rather than sole invention of reversal.

Searches also returned agreement-forest, tree-containment and undirected
contractibility work; none inspected supplies the required same-leaf directed
admissible-contraction theorem. Coverage does not exhaust citation descendants,
unindexed preprints, or every equivalently formulated directed contraction
problem. A neighboring historical tree-agreement-with-contractions article
was found but its full text could not be opened; its exact definitions remain
unresolved here. No inference of priority is drawn from search absence.

## Significance and exact scope

The constructed inputs have strict root degree (0,2), leaf degree (1,0), and
internal degree (1,2)/(2,1), not merely a bound on one type of internal vertex.
They are consequently inside the degree-at-most-three class under discussion.
Unary or higher-degree common quotients are allowed by the fixed question and
are essential to the intended target, so no semibinary reinterpretation is
needed.

The concrete contribution is a polynomial Karp reduction and arbitrary-witness
recovery establishing NP-completeness on strict binary inputs with variable k
and an unbounded taxon set. It closes the specified structural restriction
while retaining linear graph size. This meets the fixed moderate significance
criterion. It establishes neither constant-k hardness on binary inputs nor
hardness at bounded level, fixed leaf count, or for contraction-expansion edit
distance. These stronger claims are unnecessary and should remain absent.

No blocking correction is requested. General mathematical correctness,
supported novelty within recorded coverage, and significance are separate
grounds for the advance decision.
