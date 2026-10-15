# Round 1: split a mixed-degree variable

## Plan

Action: construct and test. First formal attempt; the older tree-display probe
is not counted. Try replacing a (2,2) incidence vertex by an incoming binary
reticulation followed by an outgoing binary tree vertex. In a three-bag quotient
R -> A -> B with R -> B, the replacement must behave as one choice, not allow
its input half to join A while its output half joins B. Such a split would let
one source element satisfy both sides of a singleton set.

Finite scope: construct one complete binary network around this replacement,
with a supplied leaf-parent coloring, and test whether connected acyclic bags
can split its two halves. Compare against forcing both halves into one bag.
Use the prepared bag encoding, then realize and replay the partition.
This is a local interface investigation, not a Set Splitting Karp candidate;
a binary second network forcing the intended quotient is still missing.

Experience: reticulation-stack NAE is inapplicable because contraction bags
lack the proper-forest same-parent condition. Test actual bag connectivity.

## Evidence and diagnosis

`python3 rounds/001/probe.py > rounds/001/result.json` from the campaign directory.
One legal 15-vertex binary network; two Z3 queries. The split-halves partition
is SAT, and six admissible contractions realize it. Enforcing equality of the
two halves is UNSAT under the same pins. The [output](result.json) saves the
complete network, named colors and sequence.

The A-colored vertices a and u connect only through the incoming half i when
the root scaffold stays R. Similarly b and v connect only through the outgoing
half o on the B side. The i->o edge may cross between bags without a cycle.
Thus ordinary fan-in/fan-out binaryization creates two independent sides where
the original vertex represented one source choice. This exact local example
excludes this replacement under the declared boundary conditions; it does not
refute all binary encodings or exhibit a complete bad Karp output.

Experience extraction: one reusable finding identified, pending shared write
scope, destination `research/experience/binary-contraction-split-variable.md`.
Applicability: mixed-degree vertex replaced by a reticulation/tree pair without
synchronization. Evidence: this round. No shared file was written.

## Next action

Change mechanism: use reversed leaf-parent ancestry across the two input
networks to force the variable halves into one bag. Test an actual binary
network pair and whether every valid witness respects that equality.
