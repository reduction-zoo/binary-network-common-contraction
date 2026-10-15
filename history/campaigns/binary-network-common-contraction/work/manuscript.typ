#import "report.typ": research-report
#show: research-report.with(
  title: "Maximum Common Contraction of Binary Phylogenetic Networks Is NP-complete",
  date: "September 16, 2026",
  status: "Research manuscript · awaiting human expert assessment",
)

#heading(numbering: none)[Abstract]
A common contraction records structure shared by two rooted phylogenetic networks under acyclic internal-edge contractions. The complexity of finding a largest common contraction was known for bounded-degree networks, but the binary-input case remained open in the published classification. We give a deterministic polynomial-time reduction from Set Splitting to this binary case. The construction replaces every incidence vertex by a binary directed path whose auxiliary taxa force all its ports into one contraction bag. Marked paths separate three distinguished bags even when some variables remain unassigned. Every accepted target witness yields a source split in polynomial time. The reduction has linear graph size and proves NP-completeness for a variable threshold and an unbounded taxon set.

= Introduction

Phylogenetic networks represent ancestry that may include reticulation. Comparing two such networks requires a notion of shared structure that respects both direction and leaf labels. Marchand et al. [1] study common contractions obtained by identifying the endpoints of internal arcs while preserving acyclicity. Their Theorem 9 proves NP-hardness for networks of maximum degree ten. The paragraph following that theorem and the conclusion leave the binary restriction open.

Binary inputs have a root of outdegree two, leaves of indegree one, and other vertices of indegree/outdegree $(1,2)$ or $(2,1)$. A direct degree reduction is insufficient: replacing a variable by a sequence of merging and branching vertices can let different occurrences enter different contraction bags. Moreover, forcing a variable into a single bag need not force it into one of two designated truth bags. A larger common contraction can retain that variable separately.

We combine binary paths with labeled endpoint constraints and two long marked paths. The endpoint constraints synchronize every occurrence of an element. The marked paths force three distinguished bag images to remain distinct. We then recover a _partial_ assignment: connectivity guarantees both colors in every source set, so unconstrained elements can be assigned arbitrarily.

#block[
  *Theorem 1.* Maximum Common Network Contraction is NP-complete for simple binary rooted phylogenetic input networks with the same uniquely labeled leaves. There is a deterministic Karp reduction from Set Splitting with linear output graph size. From every accepted target witness of an output, a source split can be recovered in polynomial time.
]

The threshold is part of the input. The theorem does not assert hardness for a constant threshold, a fixed number of taxa, bounded reticulation level, or contraction-expansion edit distance. The incidence encoding and leaf-based forcing build on [1]. In particular, reversed endpoint ancestry already appears in its Proposition 7 and Figure 3. The contribution is the binary realization of all ports and its composition with partial recovery and a separation threshold.

= Contractions and source witnesses

A network is a finite simple directed acyclic graph with a unique root and uniquely labeled leaves. An _admissible contraction_ identifies the endpoints of an internal arc, removes loops and duplicate arcs, and preserves acyclicity. Leaf edges cannot be contracted. The two input networks must be binary; intermediate networks and their common contraction need not be binary. A common contraction must preserve every leaf label.

#block(width: 100%, breakable: false)[
Let $I(N)$ denote the internal vertices of a network $N$. Our decision convention is
$ exists M: M " is a common contraction of " N_1,N_2 quad "and" quad |I(M)| >= k. $
]
The strict-threshold convention satisfies $|I(M)| > q$ if and only if $|I(M)| >= q+1$.

A contraction partitions the original internal vertices into nonempty _bags_, one for each quotient vertex. We use the following characterization from Definition 5 and Proposition 5 of [1]: bags induce weakly connected subgraphs, the quotient arcs are exactly the arcs crossing distinct bags, leaf-parent images agree, and the quotient is acyclic. Conversely, these conditions suffice for a sequence of admissible contractions. In particular, a path whose endpoints have the same quotient image must lie entirely in one bag; otherwise its image contains a directed cycle.

Set Splitting supplies an explicitly listed ground set $X$ and a family $cal(S) = (S_1, dots, S_m)$ of subsets. A witness is a coloring $c: X -> {0,1}$ such that every set contains both colors. This problem is NP-complete [2, SP12]; it is also the source used in [1]. Write $n=|X|$, $t=sum_(j=1)^m |S_j|$, and let $p$ count elements appearing in at least one set. Inactive elements have no constraints and will receive color zero.

If the family is empty, the reduction emits two identical balanced four-leaf trees with threshold three. If some set has size at most one, it emits the balanced trees with splits $a b | c d$ and $a c | b d$, again with threshold three. This is a NO pair because each tree has only three internal vertices and they are not leaf-preservingly isomorphic. We therefore assume every set has at least two elements.

= Construction

== Incidence and reference networks

Start two preliminary networks $G,H$ with distinct vertices $R,A,B$ and arcs
$ R -> A, quad R -> B, quad A -> B. $
For each active element $x$, add a vertex $X_x$ and arcs $A -> X_x -> B$ in both networks. For each set $S_j$, add $U_j,V_j$ in $G$, together with
$ R -> U_j, quad U_j -> X_x, quad X_x -> V_j quad (x in S_j). $
Attach private labeled leaves $u_j,v_j$ to $U_j,V_j$ in $G$. Attach leaves with those same labels to $A,B$ in $H$. The incidence pattern is shown in @incidence.

#figure(
  image("figures/incidence-reference.svg", width: 100%),
  caption: [Preliminary incidence and reference networks for one three-element set. Leaf labels, later synchronization taxa, and separation paths are omitted. Blue vertices are intended for one bag and orange vertices for the other; these colors are explanatory, not part of the target input. A variable can retain a separate image. The connectivity requirement at $U$ and $V$ must still be met.],
) <incidence>

Choose
$ L=p+1, quad k=2L+3. $
In both networks add an $R$–$A$ path and an $A$–$B$ path, each with $L$ new internal vertices. Retain the direct arcs. Every new path vertex has a private labeled leaf, with the same labels and order in the two networks. These vertices already have degrees $(1,2)$ and are not expanded. The paths are illustrated in @separation.

#figure(
  image("figures/separation-paths.svg", width: 94%),
  caption: [The three distinguished vertices and the two marked separation paths, shown schematically with three internal vertices per path. Each pendant circle is a uniquely labeled leaf. In the actual construction each path has $L=p+1$ internal vertices. Identifying either path's endpoints in an acyclic quotient identifies its entire path. The figure omits variables and clause incidences.],
) <separation>

For each $g in {R,A,B}$, attach to $g$ in $G$ a cherry $C_g$ with leaf labels $h_g^-$ and $h_g^+$. Designate $R,A,B,U_j,V_j$ as fixed-group vertices of $G$, belonging respectively to groups $R,A,B,A,B$. For each such vertex $v$, reserve two labels $g_v^-,g_v^+$ and attach leaves with these labels to its group vertex in $H$. Their counterparts in $G$ are added by the expansion below. Each variable $X_x$ reserves its own pair $g_(X_x)^-,g_(X_x)^+$. All labels are distinct unless explicitly shared between the two inputs.

== A binary path carrying all ports

Suppose a vertex has $d$ incoming and $e>=1$ outgoing arcs. Choose deterministic orders for these ports. Its replacement is a directed path with an auxiliary leaf at the first vertex and another at the last vertex. The first incoming arc, when present, enters the first vertex. The other $d-1$ incoming arcs enter successive reticulation vertices. The first $e-1$ outgoing arcs leave successive tree vertices after those reticulations. The last outgoing arc leaves the final vertex. @spine gives the two-input, two-output instance.

#figure(
  image("figures/binary-spine.svg", width: 100%),
  caption: [Exact local replacement for two incoming and two outgoing ports. The internal path has degree pairs $(1,2),(2,1),(1,2),(1,2)$. The displayed external port vertices have their surrounding edges omitted. If the two leaf-parent images coincide, every internal path vertex has that image; thus both incoming and outgoing ports share one choice.],
) <spine>

#block(width: 100%, breakable: false)[
The replacement has
$ 2 + max(0,d-1) + e-1 $
internal vertices.
]
For $d>0$ this is $d+e$. Every nonroot internal vertex has degrees $(1,2)$ or $(2,1)$. When $d=0$, its first vertex is the unique root and has outdegree two. Every replacement vertex lies between the two auxiliary leaf parents on a directed path.

Expand every fixed-group vertex $v$ in $G$ with endpoint taxa $g_v^-,g_v^+$. Expand $X_x$ in $G$ in the order $g_(X_x)^-,g_(X_x)^+$, and expand $X_x$ in $H$ in the opposite order. Finally, expand each group vertex $g$ in $H$ with endpoints $h_g^-,h_g^+$. Cherry parents and marked-path vertices are left unchanged. These operations produce the output networks $N_G,N_H$.

*Lemma 1 (legal binary outputs).* For every source in the nontrivial case, $N_G,N_H$ are simple binary rooted networks with the same leaf labels.

_Proof._ All preliminary vertices are reachable from $R$. Every $V_j$ has a parent because $S_j$ is nonempty. The preliminary graphs are acyclic: clause vertices precede their incident variables, which precede the corresponding $V_j$ and $B$; the two added paths follow the order $R,A,B$. Replacing a vertex by a directed path cannot create a cycle, since any such cycle would project to a closed directed walk in the preliminary graph. The port construction gives the claimed degrees. Unexpanded cherries and marked-path vertices have degrees $(1,2)$. Distinct ports and disjoint name classes prevent loops, parallel arcs, and label collisions. The reserved labels occur once on each side after expansion. $square$

= Correctness

== Forced images

Let $M$ be any common contraction, without assuming that its size meets the threshold. Use its leaf-preserving isomorphism to identify images across the two networks.

*Lemma 2 (synchronization).* Each fixed group has a common image in $M$, denoted $rho,alpha,beta$ for $R,A,B$. Every variable replacement has one image $z_x$ shared between the two inputs. The group images are not assumed distinct in this lemma.

_Proof._ The two leaves $h_g^-,h_g^+$ share their parent $C_g$ in $N_G$. Their parent images in $N_H$ therefore agree. Acyclicity forces the entire group replacement path between these two parents into one image. All endpoint taxa of every corresponding fixed-group vertex in $N_G$ consequently have that same parent image. The same directed-path argument collapses the whole replacement of each such vertex and identifies $C_g$ with the group.

For a variable, write $P,Q$ for the common parents of $g_(X_x)^-,g_(X_x)^+$. One network has a directed path from the first parent to the second, while the other reverses this order. Hence $P$ reaches $Q$ and $Q$ reaches $P$, allowing paths of length zero. Acyclicity gives $P=Q$. Every vertex between these parents in either variable path has this same image. This is the reversed-ancestry argument used in [1, Proposition 7 and Figure 3], applied to a path carrying all incidence ports. $square$

*Lemma 3 (separation).* If $|I(M)|>=2L+3$, then $rho,alpha,beta$ are pairwise distinct.

_Proof._ After Lemma 2, every internal vertex of $N_H$ belongs to a group image, a variable image, or one of the $2L$ marked-path vertices. If $rho=alpha$, the whole first path has that image, so
$ |I(M)| <= 2+p+L = 2p+3 < 2L+3. $
If $alpha=beta$, the second path and every variable image lie on directed paths whose endpoints agree. All of them collapse, giving
$ |I(M)| <= 2+L < 2L+3. $
Finally, $rho=beta$ forces $alpha$ to have that same image along $R -> A -> B$. Each case contradicts the threshold. These bounds cover every quotient, including those with separate variable bags. $square$

== Recovery and the NO direction

*Lemma 4 (partial recovery).* Every common contraction meeting the threshold yields a valid source split by coloring $x$ with one exactly when $z_x=beta$, and coloring every other element with zero.

_Proof._ The $alpha$ bag in $N_G$ contains the $A$ replacement and each $U_j$ replacement. The latter's only internal neighbors outside its own path are the $R$ replacement and the replacements of $X_x$ for $x in S_j$. Its auxiliary and clause leaves cannot join an internal bag. By Lemma 3, $rho != alpha$. Connectivity therefore requires an incident variable with $z_x=alpha$; otherwise the entire $U_j$ path is separated from the $A$ path within their common bag.

The $beta$ bag contains the $B$ replacement and each $V_j$ replacement. The only internal neighbors outside a $V_j$ path are its incident variables. Thus some $y in S_j$ has $z_y=beta$. Since $alpha != beta$, the prescribed colors give zero to $x$ and one to $y$. Every source set is split. Variables with other images are harmless because each set already has both colors. $square$

The executable recovery algorithm rebuilds $N_G$ and tracks every original vertex's current identifier through the supplied left contraction sequence. The implementation retains the smaller identifier at each contraction. It compares the image of the first vertex of each variable path with that of the first $B$-path vertex, then returns the resulting coloring. The right sequence and isomorphism need not be inspected by this algorithm: their validity is part of the accepted-witness premise used in the proof. Recovery performs no source search.

== Completeness

Suppose a source split is given. In $N_G$, put each fixed-group replacement into its designated group bag, and each cherry parent $C_g$ into group $g$. Put each variable replacement in $A$ or $B$ according to the split. Leave every marked-path vertex as a singleton bag. Use the analogous partition in $N_H$.

The $R$ bag is connected. In $N_G$, all $A$-colored variable paths attach directly to the $A$ path. Every $U_j$ path attaches to at least one of them because $S_j$ has both colors. This makes the entire $A$ bag connected. The $B$ argument uses $V_j$ and the $B$-colored variables. In $N_H$, the variable paths join their designated group through the arcs $A -> X_x -> B$. Singleton marked-path bags are connected.

The exact quotient arcs are $R -> A$, $R -> B$, $A -> B$, and the two marked paths. Every clause incidence is either internal to a group or maps to $A -> B$. Each leaf label has the same parent in both quotients: fixed taxa and cherry taxa use their group, variable taxa use their color, and path taxa use their singleton. The quotients are acyclic and leaf-preservingly isomorphic, with $2L+3$ internal vertices. The connected-bag characterization supplies admissible contraction sequences. Together with Lemma 4, this proves the Karp equivalence and the recovery claim of Theorem 1.

= Complexity and scope

The preliminary networks have $O(p+m+t+1)$ vertices and arcs. Summed over all replacements, the number of ports is linear in their arc count. The binary expansion therefore preserves this asymptotic bound. Taxon labels and identifiers use $O(log(n+m+t+2))$ bits, so the explicit output length is
$ O((p+m+t+1) log(n+m+t+2)). $
The construction uses only deterministic ordering, graph insertion, and serialization. A conservative bit-time bound for the implementation is $O(s^3)$, where $s$ is the source encoding length.

If $N$ is the order of the left output, recovery processes at most $N-1$ contractions and updates at most $N$ representatives per contraction. Its output has $n$ bits; the explicitly listed ground set makes this polynomial in $s$. Including reconstruction and witness parsing, a conservative bit-time bound is $O((s+w)^3)$ for witness length $w$.

The target lies in NP. Each contraction reduces the internal-vertex count, so both sequences have polynomial length. One can replay them, check acyclicity after every step, and verify the supplied final leaf-preserving isomorphism in polynomial time. This completes the NP-completeness statement.

The construction closes the binary-input restriction within the recorded literature coverage. The quotient itself may be nonbinary, and the number of taxa and the threshold grow with the source. Restricting any of these quantities further requires another argument.

#heading(numbering: none)[References]

[1] Bertrand Marchand, Nadia Tahiri, Shohreh Golpaigani Fard, Olivier Tremblay-Savard, and Manuel Lafond. Finding maximum common contractions between phylogenetic networks. _Algorithms for Molecular Biology_ 20, Article 18, 2025. #link("https://doi.org/10.1186/s13015-025-00283-9")[doi:10.1186/s13015-025-00283-9].

[2] Michael R. Garey and David S. Johnson. _Computers and Intractability: A Guide to the Theory of NP-Completeness._ W. H. Freeman, 1979. Problem SP12: Set Splitting.

#pagebreak()
#set heading(numbering: "A.")
#counter(heading).update(0)
= Verification and reproducibility

The theorem rests on the preceding general proof. Finite experiments check the implementation and witness handling; they do not establish correctness for all inputs. The artifact includes the forward map and extractor in `algorithm.py`, a Z3 checker in `check.py`, and a separately implemented CP-SAT verifier in `verify.py`. Neither checker imports the candidate. The source JSON lists `elements` explicitly and gives `sets` as lists of their indices. Target JSON contains both networks and the threshold. The accompanying contract defines contraction sequences and the final isomorphism.

The prepared suite contains eight source instances and four recovery calls. The separate suite contains eleven sources and eighteen recovery calls, including an explicitly unassigned variable. These suites overlap. The Z3 oracle uses distance-ranked connected bags; CP-SAT uses conserved flows. Both solve the actual generated targets and replay returned contraction witnesses. Initial oracle checks compare 112 small target decisions against direct contraction enumeration. Seven malformed raw inputs, including a 5,001-digit out-of-domain index, test the parser.

An independently authored reviewer checker tested eight distinct sources with nine target queries and twelve recovery calls. It uses forced ancestor equalities and lazy connectivity constraints, then realizes each positive partition by direct contractions. Its cases include two free variables with quotient size $k+2$, and free variables with merged marked-path parents at size $k+1$. Both increasing and decreasing admissible-edge orders recover valid source splits. Its largest left and right input orders are 139 and 109. Agent review found no material proof gap; human mathematical and priority assessment remains outstanding.

Prerequisites are Python 3, NetworkX 3.6.1, Z3 5.1.0, OR-Tools 9.15.6755, and Typst. From the campaign directory, reproduce the checks with:

```sh
python3 work/check.py --self-test
python3 work/check.py --candidate work/algorithm.py
python3 work/verify.py --candidate work/algorithm.py
python3 reviews/complete-rule/independent_check.py
```

The candidate's normal mode reads one source JSON object from standard input. Recovery runs in a fresh process:

```sh
python3 work/algorithm.py < source.json
python3 work/algorithm.py --extract < recovery-input.json
```

Here `recovery-input.json` contains `source` and `target_solution`. No solver is used by either candidate mode. Experiments use finite scopes and no wall-clock timeouts. Raw outputs, source instances, review findings, and exact commands remain in the campaign artifacts. Literature checks on September 16, 2026 found no matching later resolution; incomplete citation coverage is not a certificate of priority.
