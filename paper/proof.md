# Set Splitting to binary-network common contraction

This complete candidate proof received an independent agent advance review.
Human expert validation and publication acceptance are not claimed. The construction implements
[algorithm.py](../algorithm/algorithm.py); the exact encodings are in [contract.md](../algorithm/contract.md).

## Theorem and source

There is a deterministic polynomial-time many-one reduction from Set Splitting
to the following problem: given two simple binary rooted phylogenetic networks
on the same uniquely labeled leaves and an integer k, decide whether they have
a common admissible contraction with at least k internal vertices. From every
valid pair of contraction sequences and final leaf-preserving isomorphism of
an output, a source split is recoverable in polynomial time. Consequently the
target is NP-complete, using the standard NP-completeness of Set Splitting.

An admissible contraction identifies the ends of an internal arc, removes
loops and repeated arcs, and must preserve acyclicity. Internal vertices with
indegree/outdegree (1,1) may occur after contractions. Input roots have outdegree
two; leaves have indegree one; other input vertices have degrees (1,2) or (2,1).
The two input networks, not necessarily their common quotient, must be binary.

We use the connected-bag characterization in Definition 5 and Proposition 5
of [Marchand et al.](https://link.springer.com/article/10.1186/s13015-025-00283-9).
A quotient is obtainable by admissible contractions exactly when its internal
vertices correspond to nonempty weakly connected bags, its arcs are precisely
the input arcs crossing distinct bags, its leaf parents match, and it is a DAG.
This is a cited ingredient, not a new characterization.

The source explicitly lists its ground set [0,n) and its subsets. If the family
is empty, emit a fixed YES pair: two identical balanced four-leaf trees at k=3.
If some set has fewer than two elements, emit a fixed NO pair: balanced trees
with leaf splits ab|cd and ac|bd, also at k=3. They have three internal vertices,
so a common contraction of that size would require leaf-preserving isomorphism,
which fails. The empty-family extractor returns the all-zero coloring. No valid
target witness exists in the second case. Malformed sources map outside the
target language. Thus assume all sets have at least two elements. Use only the
p active elements appearing in a set, retaining their original indices.

## The two preliminary networks

Create distinct vertices R,A,B and arcs R->A, R->B, A->B in both G and H.
For every active element x, create X_x and arcs A->X_x and X_x->B in both.
For each set S_j create U_j,V_j in G, arcs R->U_j and, for every x in S_j,
U_j->X_x and X_x->V_j. Attach distinct leaves u_j,v_j to U_j,V_j respectively.
In H attach leaves with these same labels to A,B. These leaves are distinct
from every auxiliary taxon introduced below.

Put L=p+1. In each preliminary network, add a path with L new internal vertices
from R to A, and another from A to B, retaining the direct arcs. Each new path
vertex has its own private leaf, with the same labels and order in G and H.
These path vertices have indegree one and outdegree two and are not expanded.

For each g in {R,A,B}, attach a new cherry C_g to g in G. Its two leaf labels
are h_g^x,h_g^y. The three cherry parents are not expanded. Distinct namespaces
separate all vertex names and all leaf labels in the implementation.

Designate each of R,A,B,U_j,V_j in G as a fixed-group vertex, with group R,A,B,A,B
respectively. For each such vertex v reserve two labels g_v^x,g_v^y, and attach
leaves with these labels to its group vertex in H. The corresponding leaves in
G will be supplied by the binary expansion. Each variable X_x reserves its own
two labels g_x^x,g_x^y; neither is attached until the expansion.

Both preliminary digraphs are acyclic. One topological arrangement puts R and
the R-A path before A and all U_j, then variables, then V_j and B. The A-B path
can lie between A and B. Cherry vertices and leaves are placed after parents.
Every vertex is reachable from R, since all sets are nonempty and each V_j has
an incident variable parent. Every internal vertex has an outgoing edge.

## Binary expansion with two taxon endpoints

For a vertex v with d incoming and e outgoing arcs, choose deterministic orders
of these ports. Replace v by a directed spine. Its first node has a new leaf x;
its last node has a new leaf y. The first incoming arc, if present, enters the
first node. The remaining d-1 incoming arcs enter consecutive reticulation nodes
along the spine. The first e-1 outgoing arcs leave consecutive tree nodes after
the reticulations. The final outgoing arc leaves the last node. Consecutive
spine nodes are linked. There are 2+max(0,d-1)+e-1 spine nodes.

If d>0, the first and last nodes and all outgoing nodes have degrees (1,2),
and incoming nodes have degrees (2,1). If d=0, the first node is the root and
has outdegree two. Distinct port endpoints stay distinct. The spine is acyclic,
and replacing a vertex by such a spine cannot create a directed cycle: a cycle
would project to a closed directed walk in the original DAG. Every spine node
is between the parents of x and y in the directed reachability order. Collapsing
the whole spine recovers v and adds the two labeled leaves.

Expand each fixed-group v in G with endpoints g_v^x,g_v^y. Expand X_x in G with
endpoints g_x^x,g_x^y, and X_x in H with endpoints in reversed order g_x^y,g_x^x.
Expand each group g in H with endpoints h_g^x,h_g^y. Expand no other vertices.
Sequential expansion just redirects ports of adjacent spines; it does not change
the specified incidence. All labels now occur exactly once in each input.
The output networks are simple, rooted and binary, on YES and NO sources alike.
Set the target threshold to k=2L+3.

## Forced bags in every common contraction

Let M be any common contraction and use its common leaf labels to identify
parent images. A path in either input maps to a directed walk with possible
zero-length portions inside bags.

For each group g, the leaves h_g^x,h_g^y share parent C_g in G. Their parents in
H therefore have the same image. Acyclicity forces every node on the H group
spine between those parents to have that same image; call it g*. All leaves
attached along that spine consequently have parent g* in M. In particular, both
endpoint taxa of every G fixed-group vertex have parent g*. This forces its
whole G spine to have image g*. It also places C_g in g*. Thus the original
R,A,B,U_j,V_j spines have the intended respective images, without presupposing
that the three group images are distinct.

The reversed-ancestry principle is already used by Marchand et al.,
Proposition 7 and Figure 3; the contribution here is its all-port binary
implementation and composition with the separation bound.

For an element x, its endpoint taxa appear in opposite ancestry orders in G
and H. If their common parents are P,Q, one network implies P reaches Q, while
the other implies Q reaches P. Acyclicity gives P=Q and forces every node on
both variable spines into that image, denoted X_x*. These images may coincide
with group images or with other images; no full assignment is assumed.

In H all internal vertices therefore belong to the three forced group images,
the p variable images and the 2L path vertices. Its common quotient has at most
3+p+2L internal vertices before any further identifications are considered.

## The threshold keeps R*, A*, B* distinct

If R*=A*, the entire R-A path also has this image. Therefore

    |I(M)| <= 2+p+L = 2p+3 < 2L+3.

If A*=B*, the A-B path and every variable spine have this image, because each
variable lies on a directed path from A to B. Consequently

    |I(M)| <= 2+L < 2L+3.

If R*=B*, the path R->A->B forces all three images equal, reducing to the cases
above. Thus every accepted witness has pairwise distinct R*,A*,B*. This uses an
upper bound on all possible quotient vertices, not an optimality assumption
or a preferred witness. Private variable images cannot compensate for a collapsed
separation path.

## Soundness and recovery from every accepted witness

Consider the A* bag in G. It contains the A spine and every U_j spine. The only
external internal neighbors of a U_j spine are the R spine and variable spines
X_x for x in S_j. Its attached leaves cannot be contracted. As R* differs from
A*, weak connectivity of the A* bag requires at least one of these variable
spines to have image A*. Otherwise the entire U_j spine would be a component
of that bag disjoint from its A spine. The B* bag similarly contains the B
spine and every V_j spine. The only external internal neighbors of V_j are its
incident variable spines, so some x in S_j has X_x*=B*.

Color an active element 1 exactly when its variable spine has image B*, and
color all other elements 0. Every set has a B* element of color 1 and an A*
element of color 0, since A* and B* differ. This includes witnesses with free
variable images, merged path nodes, and additional allowed contractions.

The executable extractor rebuilds the deterministic left network and tracks
the image of each original vertex through the supplied left contraction sequence,
using the contract's smaller-identifier representative convention. It compares
the image of the first variable-spine node to that of the first B-spine node.
It need not inspect the final isomorphism: validity of the given witness provides
the existence of the common quotient used in the argument. Extraction never
solves Set Splitting or invokes a solver.

## Completeness

Given a source split, put every fixed-group spine and its cherry parent into
its corresponding R,A,B bag. Put X_x into A or B according to the split. Keep
every separation-path vertex as its own bag. Use the analogous partition in H.
The R bag in G is connected. The A bag is connected through its A spine and
all A-colored variables, each adjacent to A. Each U_j is joined to at least one
such variable because S_j has both colors. The B bag is connected by the symmetric
argument using V_j and B-colored variables. Group bags in H are connected by
its A->X_x->B incidences. Path bags are singletons.

In both inputs the exact quotient arcs are R->A, R->B, A->B and the two marked
paths. No additional arc type occurs: every incidence U_j->X_x or X_x->V_j is
either internal to a group bag or maps to A->B. The quotients are acyclic and
have the same parent for every leaf label: fixed tags and cherry tags use their
group, variable tags use the source color, and path tags use their singleton.
They are therefore leaf-preservingly isomorphic and have exactly 2L+3 internal
vertices. The connected-bag characterization supplies admissible sequences.
This proves YES/NO equivalence together with the soundness argument.

## Size, determinism and membership in NP

Let n be the explicitly listed source universe size, m the number of sets and
t their total incidence count. Active p<=n and p<=t. Preliminary networks and
all added taxa have O(p+m+t+1) vertices and arcs. The sum of incoming and outgoing
degrees is linear in the arc count; expanding each vertex increases size by its
port count plus a constant. Both output graphs therefore still have
O(p+m+t+1) vertices and arcs. Labels and identifiers require
O(log(n+m+t+2)) bits. Explicit output length is polynomial in source bit length s,
and is O((p+m+t+1) log(n+m+t+2)).

All orders, labels, paths and special cases are deterministic. Sorting finite
adjacency lists, inserting spines and serializing integers take polynomial bit
time; O(s^3) is a conservative bound for this implementation. Recovery rebuilds
the construction, then updates at most N vertex representatives for each of at
most N-1 left contractions, where N is the output order. It outputs n bits.
A conservative bit-time bound is O((s+w)^3) for witness encoding length w; both
output and recovered-witness sizes are polynomial. Explicitly listing the ground
set is necessary for the n-bit output bound and is enforced by the JSON contract.

The target is in NP: each contraction decreases internal-vertex count by one,
so both sequences are linear in input vertex count. Replaying them, checking
acyclicity, and checking the supplied final bijection and leaf labels is
polynomial. This proves NP-completeness if the construction and cited source
hardness are confirmed. The general argument is separate from finite tests.
