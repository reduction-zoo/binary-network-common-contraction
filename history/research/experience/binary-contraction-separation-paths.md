# Marked paths separate anchors despite optional variable images

Tags: binary network, directed acyclic contraction, threshold amplification, partial recovery.

## Claim and applicability

In the reviewed binary common-contraction construction, the reference network's
internal images consist of three synchronized groups R,A,B, at most p variable
images on A-to-B paths, and two shared leaf-marked paths, R-to-A and A-to-B,
with L=p+1 new internal vertices each. Set k=2L+3. Any common quotient with at
least k internal vertices keeps R,A,B distinct.

If R=A, acyclicity collapses the first path, leaving at most 2+p+L=2p+3<k
images. If A=B, the second path and all variable images collapse, leaving at
most 2+L<k. If R=B, the R-to-A-to-B path also forces A into that image.
A satisfying source split retains the three groups and all 2L marked vertices.

This relies on the stated exhaustive reference-side image count, synchronized
interfaces, acyclic contractions and matching private leaf labels. It is not a
generic separation gadget for undirected contractions or constant thresholds.

## Evidence and status

[Round 6](../../campaigns/binary-network-common-contraction/rounds/006/round.md) records the construction and tests.
The [general proof](../../campaigns/binary-network-common-contraction/work/proof.md) supplies separation and completeness;
the [independent review](../../campaigns/binary-network-common-contraction/reviews/complete-rule/review.md) advances both.
Its tests include free-variable quotients of size k+2 and merged marked-path
parents at size k+1. These finite witnesses supplement the proof. The
[paper](../../campaigns/binary-network-common-contraction/work/manuscript.pdf) states the complete variable-threshold result;
human correctness and priority assessment remains outstanding.

## Consequence for search

Count all optional quotient images before choosing a path length. A forced
anchor identification must lose more marked vertices than those optional images
can retain. Pair separation with clause-coverage recovery rather than requiring
every synchronized variable to join a truth bag.

## Use history

Originated in round 6 of this campaign. No subsequent independent application
is recorded.
