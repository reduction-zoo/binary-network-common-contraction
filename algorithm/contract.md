# Input and witness contract

Source: {"elements": [0,...,n-1], "sets": [[i,...],...]}, n>=0.
The explicit elements list defines the ground set; indices lie in [0,n).
Each listed set has distinct indices. A witness is an n-entry list of bits;
every listed set must contain both bits. Empty and singleton sets make NO.

Target: {"left": N, "right": N, "k": k}. A network N has
{"n": n, "edges": [[u,v],...], "leaves": {label: vertex,...}}.
Vertices are [0,n), arcs are distinct, and labels are nonempty strings.
Input networks are simple DAGs with a unique root of outdegree two, labeled
leaves of indegree one, and all other vertices of degrees (1,2) or (2,1).
Both networks have exactly the same label set. k is a nonnegative binary integer.
Intermediate graphs may have degree-two or higher-degree internal vertices.

A witness is {"left": [[u,v],...], "right": [[u,v],...],
"iso": [[u,v],...]}. Each pair contracts a currently present internal arc,
retaining the smaller numeric identifier. Remove loops and duplicate arcs;
the quotient must remain acyclic after every step. The final isomorphism must
be bijective, preserve every arc and leaf label, and leave at least k internal
vertices. There are at most n-1 contractions per side. Renaming to fresh
identifiers, as in the paper, is equivalent to this deterministic retained-ID
encoding. Verification is polynomial in the instance and witness length.

The paper's problem box uses >k, while its hardness construction uses >=3.
This campaign fixes >=k as its card states; >k is translated as >=k+1.

Candidate command: python3 algorithm.py reads one source JSON from stdin and
writes one target JSON. With --extract, it reads {"source": source,
"target_solution": witness} and returns a source coloring. Each invocation
is a fresh process; neither map may call a solver. Malformed sources may emit
{"invalid": true}, which lies outside the target language. Well-formed sources
must always produce structurally legal binary network pairs, including NO cases.
