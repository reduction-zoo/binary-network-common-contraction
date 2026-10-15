# Binary-network common contraction

Status: `ready_for_expert_review`.
Budget: 23 rounds authorized (3 initial plus 20 additional); 6 completed,
17 unused. This continuation used three new rounds and stopped on a complete
reviewed candidate, not budget exhaustion.

## Result

[Set Splitting reduces to binary-network common contraction](work/manuscript.pdf)
by a deterministic Karp map with linear graph size and polynomial encoding size.
Every accepted target witness yields a source split in polynomial time.
The theorem establishes NP-completeness for strict binary inputs, a variable
threshold and an unbounded leaf-label set. Intermediate and common networks
need not be binary. It does not assert constant-threshold or edit-distance
hardness. The [question](question.md) is unchanged.

[Executable forward map and extractor](work/algorithm.py),
[contract](work/contract.md), [general proof](work/proof.md),
[Typst source](work/manuscript.typ), and [seven-page paper](work/manuscript.pdf).
All-port spines synchronize incident choices. Partial recovery tolerates free
variables; two marked paths force three distinguished images to remain distinct.

## Evidence and remaining obligations

**Correctness:** [verification](work/verification.md) records eight prepared
sources/four recoveries, eleven separate sources/eighteen recoveries, and an
independent reviewer suite of eight sources/nine target queries/twelve recoveries.
The suites overlap. Actual generated targets are solved, contraction sequences
replayed, and returned source witnesses checked. Oracle and input regressions
pass. Finite evidence supplements the general proof and does not replace it.

**Review:** [independent advance](reviews/complete-rule/review.md) and
[manuscript consistency addendum](reviews/complete-rule/manuscript-addendum.md).
No material proof gap was identified. Only attribution, wording and layout
changed after candidate review. The paper compiled successfully; all seven
pages and all three vector figures were inspected. No executable change remains
untested and no substantive proof change remains unreviewed.

**Novelty:** [bounded primary-literature checks](work/literature.md), dated
2026-09-16, support the binary-input gap left after the degree-ten theorem.
Known incidence and reversed-taxon ideas are explicitly attributed. No matching
later result was found within coverage; missing full text and incomplete citation
coverage prevent a certificate of priority.

**Significance:** resolving the binary-input restriction meets this campaign's
moderate contribution criterion. Publication and stronger restrictions are not
claimed. Human mathematical, novelty and significance assessment remains open.

**Next action:** expert review of the theorem and construction. No further search
round is currently justified. Prospects of surviving that review are an
uncalibrated positive judgment, based on the complete argument and independent
checks; a counterexample, proof gap or matching prior theorem would reopen the
relevant obligation. No numerical success probability is asserted.

## Round index

| Round | Observation |
|---|---|
| [1](rounds/001/round.md) | Unprotected mixed-degree splitting loses a single variable choice |
| [2](rounds/002/round.md) | Reversed taxon ancestry synchronizes a binary interval |
| [3](rounds/003/round.md) | Local size threshold prefers an unassigned synchronized bag |
| [4](rounds/004/round.md) | Partial-assignment recovery repairs that premise: 128 families, 3,456 partitions |
| [5](rounds/005/round.md) | All-port binary spines: 16 interface templates |
| [6](rounds/006/round.md) | Complete composition, separation paths, general proof, passing checks, independent advance and inspected paper |


## Experience and scope

Following explicit user authorization, the five pending experience changes were
synchronized: four new shared findings and one existing use-history update.
[Round 6](rounds/006/round.md#shared-experience-synchronization) links all entries.
No pending experience changes remain for this campaign. The synchronization is
record maintenance, not a research round; mathematical status and round counts
are unchanged. No publishing, production integration, board edit, skill edit,
or background job was performed.
