# Unsynchronized binary splitting can divide one variable choice

Tags: directed contraction, binary phylogenetic network, degree reduction, connected bags.

## Claim and applicability

Replacing a mixed-degree (2,2) vertex by a reticulation followed by a tree
vertex can let its incoming half join one truth bag and its outgoing half join
the other. This claim concerns the pinned local interface below, with connected
bags and an acyclic quotient. It does not exclude all binary replacements or
constitute a counterexample to a complete Karp reduction.

## Evidence and status

[Round 1](../../campaigns/binary-network-common-contraction/rounds/001/round.md) gives a 15-vertex binary network and
[explicit counterexample](../../campaigns/binary-network-common-contraction/rounds/001/result.json). Two Z3 queries find the
split partition feasible and equality of the halves infeasible under the same
pins. Six admissible contractions realize the counterexample. This is a local
counterexample, not a universal impossibility theorem. The later complete rule
was independently reviewed; no separate independent rerun of this local probe
is claimed.

## Consequence for search

Binary degree reduction must synchronize both incoming and outgoing ports when
the original vertex represents one choice. Check actual contraction bags rather
than transferring a coloring or proper-forest argument with different premises.
The [all-port spine](reversed-taxon-ancestry-synchronization.md) supplies one
applicable repair when labeled ancestry can force endpoint equality.

## Use history

[Round 2](../../campaigns/binary-network-common-contraction/rounds/002/round.md) replaced unprotected splitting by reversed
leaf-parent ancestry; the general path argument removed the split-halves
freedom. [Round 5](../../campaigns/binary-network-common-contraction/rounds/005/round.md) extended the synchronized interval
to every port. This helped construct the complete rule in round 6; it does not
measure discovery efficiency against a control.
