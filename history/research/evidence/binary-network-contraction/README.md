# Tree display versus admissible contraction

Scope declared before execution on 2026-09-16: one binary network N on nine
vertices and one binary tree T on seven vertices, both with leaves a,b,c,d.
Check that deleting s->h and suppressing s,h displays T. Then enumerate every
two-step sequence of internal-edge contractions, rejecting cycles and merging
parallel arcs. Test each resulting graph for leaf-preserving directed
isomorphism to T. Exactly two contractions are necessary by vertex counts.

This is a screening check of the proposed direct Tree Containment mapping
(N,T) -> (N,T,k=3) for Maximum Common Network Contraction. A positive display
with no contraction would refute that mapping; it would not exclude other
reductions or solve the open binary-network problem. No campaign is admitted.
Repository search found no applicable prior contraction experience.

Run from the repository root with installed NetworkX 3.6.1:

```sh
python3 research/evidence/binary-network-contraction/probe.py > research/evidence/binary-network-contraction/probe.json
```

The definitions follow Marchand et al.,
[Finding maximum common contractions between phylogenetic networks](https://link.springer.com/article/10.1186/s13015-025-00283-9),
Preliminaries, admissible contractions and Proposition 5. Input networks are
binary; intermediate contractions need not remain binary. Leaves cannot be
contracted. T has three internal vertices, so a common contraction of size
at least three must be T itself.

## Result

The [raw output](probe.json) confirms display but no contraction. All five
first contractions were admissible; of the twenty second-step candidates,
eighteen were admissible. None yielded T. The instance therefore refutes the
direct mapping, already with one reticulation and four leaves. It does not
refute a transformed-instance reduction. No repairs or reruns were needed.
This is finite exhaustive evidence for a counterexample, not a universal
impossibility theorem or an independent review. Experience extraction: none;
the exact counterexample is retained here for future contraction work.
