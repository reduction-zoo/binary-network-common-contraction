# Round 2: force a binary interval using reversed taxa

## Plan

Action: reconsider. Replace unconstrained degree splitting by cross-network
leaf-parent ancestry. Put leaf x above the variable interval and leaf y below
it in the first network; reverse x and y in the second. The common quotient
must order their parent bags both ways, forcing equality and collapsing every
vertex in the interval. This may synchronize binary input/output halves.

Finite scope: one actual binary pair on eleven vertices per network, thresholds
1 through 6. For each threshold, solve common contraction and separately ask
whether any matched connected-bag witness separates the two variable halves.
Replay all returned witnesses. Prove the ancestry statement for arbitrary
common contractions, independent of the finite checks. Composition with source
clauses and retention of variable choice remain unresolved obligations.

Experience: Round 1's split-variable counterexample motivates synchronization.
The earlier proper-forest reticulation entry still does not apply. Reversed
caterpillar leaf orders appear in the primary paper's diameter examples; the
basic ancestry argument is prior technique, not a novelty claim.

## Evidence and diagnosis

`python3 rounds/002/probe.py > rounds/002/result.json` from the campaign directory.
Both inputs have eleven vertices. Twelve Z3 queries: common quotients exist
exactly at thresholds 1–3, and no connected-bag witness separates the variable
halves at any tested threshold. All three positive sequence witnesses replay.
See [result.json](result.json). The maximum quotient has three internal vertices.

General argument: let P_x,P_y denote the common quotient parents of taxa x,y.
A directed path between their parents in the first input gives P_x <= P_y in
the quotient reachability order. The reversed path in the second gives
P_y <= P_x. Acyclicity forces equality. Every vertex of either directed interval
then belongs to this same bag: otherwise its image lies on a nontrivial directed
closed walk. Thus this also survives arbitrary external attachments preserving
acyclicity and the two ancestry paths. Leaf parents have unique meanings under
any leaf-preserving isomorphism. In this pair, p,i,o,q form that interval.

This repairs the local split-variable defect but uses known ancestry reasoning.
It does not yet encode a source element choosing either truth side. Private
anchor taxa expose the variable's bag in the common quotient, so the second
network must accommodate both choices and must not reward leaving it separate.

Experience extraction: one reusable applicability finding, pending shared write
scope, proposed `research/experience/reversed-taxon-ancestry-synchronization.md`.
This is a documented use of a known mechanism, not a new hardness result.
Original proof and experimental evidence remain here; no shared file written.

## Next action

Test the score of assigned versus unassigned synchronized bags in a complete
binary pair. A lower-bound objective may prefer keeping a variable as its own
bag instead of assigning it to either distinguished side.
