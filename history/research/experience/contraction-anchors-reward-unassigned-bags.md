# A lower-bound contraction objective can reward unassigned variable bags

Tags: common contraction, partial assignment, threshold, objective compatibility.

## Claim and applicability

For the private synchronized interval between two distinguished anchors in the
round-3 binary pair, keeping the variable separate yields five internal quotient
vertices; identifying it with either anchor yields at most four. Therefore a
lower-bound size threshold accepting an assigned witness also accepts a free
witness. The claim concerns this interface without assignment-dependent
compensation, not every clause attachment or every reduction.

## Evidence and status

[Round 3](../../campaigns/binary-network-common-contraction/rounds/003/round.md) gives a counting proof and twenty-four Z3
queries on a 15-vertex pair: nine SAT, fifteen UNSAT, with nine replayed
[positive witnesses](../../campaigns/binary-network-common-contraction/rounds/003/result.json). This is an exact local result.

The stronger search premise that every variable must be assigned was superseded
in [round 4](../../campaigns/binary-network-common-contraction/rounds/004/round.md). With distinct R,A,B images, each clause
vertex U in the A bag must connect through an incident A variable, and each V
in the B bag through an incident B variable. Every set therefore has both colors;
remaining variables can receive arbitrary colors. The full composed argument
passed [independent review](../../campaigns/binary-network-common-contraction/reviews/complete-rule/review.md), including
witnesses retaining two free variables. Human expert assessment remains open.

## Consequence for search

Before compensating the extra free bag, test whether clause coverage suffices
for arbitrary-witness extraction. If it does, protect anchor separation and
retain free variables. If it does not, the local score defect remains unresolved;
partial recovery cannot be assumed for unrelated gadgets.

## Use history

[Round 4](../../campaigns/binary-network-common-contraction/rounds/004/round.md) checked 3,456 partial partitions across 128
set families and derived the clause-connectivity argument. This redirected the
construction away from forced full assignment. [Round 6](../../campaigns/binary-network-common-contraction/rounds/006/round.md)
used that argument with synchronized binary interfaces and separation paths.
