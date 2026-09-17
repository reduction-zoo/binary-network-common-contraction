# Partial arguments: synchronizing a binary replacement

No complete Set Splitting reduction has been obtained. The lemmas here concern
local interfaces and do not establish hardness, source-witness recovery or a
polynomial candidate algorithm. They have main-researcher arguments and finite
checks, but no independent review or novelty claim.

## Unprotected degree splitting permits inconsistent choices

Replacing a vertex of indegree/outdegree (2,2) by a reticulation i followed by
a tree vertex o admits a partition with i in bag A and o in bag B. The edge
between them simply becomes A->B. The complete binary network in
[round 1](../rounds/001/result.json) demonstrates this under pinned boundary
colors: a,u can connect in A through i, and b,v in B through o. Collapsing each
connected bag gives an acyclic three-internal-vertex quotient. The saved
admissible contraction sequence independently witnesses feasibility.

The required equality i=o fails here, so this replacement does not preserve
the intended single-choice interface. This is a counterexample to that local
replacement, not a counterexample to every degree-reduction construction.

## Reversed leaf ancestry forces a common bag

Let N1,N2 have common contraction M, with leaf-preserving quotient maps h1,h2.
For a taxon x, the image of its input parent is its unique parent P_x in M.
This uses the prohibition on contracting leaf edges and uniqueness of leaf
parents. Suppose N1 has a directed path from the parent of x to that of y,
and N2 has a directed path in the opposite order. Quotient maps send each
input arc either within a bag or to an arc of M. Hence P_x reaches P_y and
P_y reaches P_x, allowing length-zero paths. Since M is acyclic, P_x=P_y.
Every vertex along either path has this same image; a different image would
give a directed cycle in M. The argument survives additional structure provided
the two ancestry paths, acyclicity and leaf-parent premises remain true.

In round 2 the path p->i->o->q brackets the variable halves. Swapping only
leaf labels x and y between two binary inputs forces these four internal
vertices together in every common contraction. There are six internal vertices
per input, so at most three remain. The saved three-internal-vertex witness
attains the bound. This applies the known leaf-ancestry method from the primary
paper's contraction arguments; it is not presented as an original theorem.

## A synchronized free bag can dominate assigned states

The round-3 pair has eight internal vertices per input. Reversed taxa force
four of them, p,i,o,q, into a bag V, so every common contraction has at most
five internal vertices. If V is identified with either distinguished vertex a
or d, at least one further identification occurs, giving an upper bound four.
The saved witnesses attain five with V distinct from both, and four with V=a
or V=d while a and d remain distinct. Thus the maxima are exactly 5,4,4.
These bounds hold without relying on solver UNSAT for a growing domain.

Consequently no threshold of the form 'at least k internal vertices' accepts
one of the assigned states while excluding the unassigned state of this pair:
for k<=4, the five-vertex unassigned witness is also accepted; for k>=5, no
assigned witness meets the bound. The paired anchors repair synchronization
but do not implement a truth choice selected by this objective. External
clause attachments may change the tradeoff; this is not an impossibility
claim for such compositions.

## Remaining construction obligations

A full construction needs a mechanism under which every sufficiently large
common quotient determines a valid source split. In particular, simply assigning
private synchronized bags to variables leaves an extra unassigned state.
An attachment may require assigning a variable to unlock common clause
structure, but it must work for both colors, preserve binary degrees, avoid
unintended cross-clause contractions, and support recovery from every accepted
quotient. No proof or implementation currently meets these obligations.

The next useful experiment is a small clause attachment that changes the size
advantage of unassigned states. Test the complete quotient score under each
boundary assignment, including unassigned and merged-anchor states, before
replicating the gadget or growing its search range.
