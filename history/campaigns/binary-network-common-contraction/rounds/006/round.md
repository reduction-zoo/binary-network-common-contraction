# Round 6: compose anchored binary networks with separation paths

## Plan

Action: construct a full candidate. Build the connected-bag incidence graph of
round 4 and a reference with anchors R,A,B and independent paths A->x->B.
Binaryize all fixed-color vertices using round 5's spines. In the incidence
network, cherries with the two reference-spine taxa force those reference
spines to collapse; their other taxa in turn synchronize clause and anchor
spines. Reverse each variable's endpoint taxa in the reference network.

Insert identical leaf-marked paths of L=n_active+1 internal vertices between
R,A and A,B in both networks, retaining the direct arcs. Set k=2L+3.
If R=A, its path collapses, giving at most L+n_active+2 vertices; if A=B,
that path and all variable spines collapse. Thus an accepted quotient must
keep all three anchors distinct. A source split realizes a quotient retaining
all path nodes and the three anchors. Extract variable colors from its actual
contraction bags; default unused/unassigned elements to zero.

Finite scope: first build the full maps and check the eight prepared source
cases with the prepared solver, including a nonempty NO triangle. Verify every
output is binary even on NO sources. Correct source encoding to explicitly list
the ground set before testing: the question specifies an explicit set, whereas
the original numeric n-only contract accidentally permitted a succinct unused
universe with an exponentially long n-bit witness. Preserve the old artifacts
and record this oracle/contract repair separately; it is not a new mechanism.

A full proof and external verification remain obligations even if these pass.
No change of mathematical source language or target restrictions is intended.


## Result and diagnosis

The complete rule passed both author suites and independent native review.
The [proof](../../work/proof.md) establishes legal strict binary outputs,
synchronization of all ports, distinct anchor images, completeness and recovery
from every accepted target witness, including larger quotients with free variables.
The deterministic [implementation](../../work/algorithm.py) has both map and
extract modes and uses no solver. Output graph size is linear in the explicit
incidence input; encoding and both executable modes have polynomial bounds.

The crucial repair to the earlier route is to allow unassigned variable bags.
Connectivity already certifies both colors in each set. Only anchor collapse
needs to be excluded by the size threshold. With L=p+1, merging R and A leaves
at most 2+p+L=2p+3 internal images, below k=2p+5; merging A and B collapses
its path and all variables. This closes the obstacle identified in rounds 4–5.
The result is variable-threshold binary-input NP-completeness, not fixed-k
hardness or contraction-expansion distance hardness.

The source-interface repair was required by the fixed explicit-set definition:
the former n-only representation allowed a succinct unused universe and an
exponentially long recovery output. The current interface lists all elements.
A separate malformed-input check exposed Python's decimal digit parsing limit;
the candidate now handles the tested oversized out-of-domain integer explicitly.
Saved pre-repair files and regression evidence are in [encoding-repair](encoding-repair/).
Neither repair creates a new research route or changes the accepted source problem.
The round-4 partition probe was replayed after the source-format repair and
matched its earlier result; it is not additional mathematical coverage.

## Verification and review

[Verification](../../work/verification.md) records commands and raw evidence.
Final author runs: eight prepared sources/four recoveries, eleven separate
sources/eighteen recoveries. The independent reviewer checked eight distinct
sources, nine target queries and twelve recoveries, including two free-variable
and merged-path witnesses. The suites overlap. Source/target oracle self-tests,
malformed-input regressions and actual contraction replay passed. Finite tests
support implementation behavior; the general proof supplies the all-input claim.

The [independent review](../../reviews/complete-rule/review.md) returned advance;
its [manuscript addendum](../../reviews/complete-rule/manuscript-addendum.md)
retained that decision. No material proof gap was identified. The reviewed rule
is written in [native Typst](../../work/manuscript.typ) with three vector figures
and a compiled, visually inspected [PDF](../../work/manuscript.pdf).
`typst compile work/manuscript.typ work/manuscript.pdf` completed with exit 0
and no diagnostics (Typst 0.15.1); the final PDF has seven pages. The final
wording pass applied how-to-technical-writing. No candidate code changed during
or after review.

[Literature coverage](../../work/literature.md) distinguishes the new composition
from the reversed-taxon principle already in Marchand et al., Proposition 7 and
Figure 3, and the incidence construction in Theorem 8. Their Theorem 9 and
following paragraph supply the degree-ten baseline and binary gap. The bounded
search found no matching later resolution; inaccessible neighboring text and
incomplete citation coverage remain limitations, not evidence of priority.

## Experience extraction

New reusable finding, pending shared destination:
`research/experience/binary-contraction-separation-paths.md`.
When p optional variable images could mask identification of distinguished
images, two leaf-marked paths of length L=p+1 force their separation at k=2L+3.
This relies on directed acyclic quotients, synchronized spine interfaces, and
the reference-side image count. It does not establish a generic forcing gadget
for other contraction models or constant thresholds. Evidence: the separation
lemma and reviewer witnesses above. Partial recovery avoids the stronger and
unnecessary requirement that every variable select a designated truth bag.

Campaign-wide extraction has four proposed new shared entries and one update
to an existing entry, all pending because writes are restricted to this campaign.
The earlier three proposed entries remain in rounds 1–3, with applicability
corrections in rounds 4–5; round 4 records the existing entry's use-history update.
Actual shared writes: zero new, zero updated. No duplicate reflection file was
created and no unrecorded experience is claimed to have been integrated.

## Recommendation and exit

Stop exploration with `ready_for_expert_review`: both maps, a general proof,
passing relevant tests, independent advance, and the inspected paper exist.
This continuation used three of twenty authorized rounds; six of twenty-three
total rounds are complete and seventeen remain unused. Testing, repair, review
and writing of this same construction are not extra rounds or independent routes.

Next is human mathematical and novelty review, not another speculative gadget.
There is no known remaining construction obstacle. Prospects for surviving that
review are an uncalibrated positive assessment based on the explicit proof and
independent checks, not a probability or publication forecast. A counterexample,
proof gap, or matching prior theorem would change this recommendation and reopen
the relevant obligation. No production integration or publication was performed.


## Shared experience synchronization

After campaign completion, the user explicitly authorized synchronization.
Four new shared entries and one existing entry update are now saved:

- [Unsynchronized variable splitting](../../../../research/experience/binary-contraction-split-variable.md).
- [Reversed ancestry and all-port spines](../../../../research/experience/reversed-taxon-ancestry-synchronization.md).
- [Free-bag scoring and partial recovery](../../../../research/experience/contraction-anchors-reward-unassigned-bags.md).
- [Marked separation paths](../../../../research/experience/binary-contraction-separation-paths.md).
- [Existing partial-assignment entry: use history](../../../../research/experience/central-interval-deletion.md#use-history).

This resolves the earlier pending-write notes without rewriting their historical
scope. No pending synchronization remains. No new research round, experiment,
independent review or novelty claim is implied by extracting these findings.
