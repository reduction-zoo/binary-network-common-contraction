# Round 005 — Complete Karp maps by central deletion

## Plan

Use the conditional proof from round 004 and its central-deletion experience.
Construct the published colored formula graph without C, then apply its known
black-vertex gadget to remove colors. Prove completeness by induced deletion
from the published YES construction. The new graph is K4-free, which forces
every component representation to have depth at most three. Implement recovery
by retaining each old black vertex's component that meets its old neighborhood,
then the free-port assignment and occurrence-cycle restriction.
Scope: this single full construction, five prepared source cases and independent
structural/witness checks of its constituent mechanisms; no alternate gadget
search. Completion: maps, general proof, actual harness result or concrete defect.

## Evidence and diagnosis

One complete graph-construction candidate was tested. The final prepared suite
[passed](prepared-final.jsonl): five sources, six recovery calls. The extended
suite [passed](ordered-splits.jsonl): seven sources, ten recovery calls. Five
structural source outputs were also checked. Earlier oracle variants, their
partial or complete coverage, and repairs are documented below. Internal solver
query totals and aggregate time/token totals were not instrumented.

The mathematical graph soundness/completeness argument is complete as a
candidate. Before independent review, a bit-encoding audit found that the
old full-length assignment contract can require exponentially many output bits
when JSON n is large and there are few clauses. The proof's explicit-variable
convention does not cover that transport format. Repair the witness encoding,
not the question: a sparse assignment with default false represents the same
Boolean solution. Thus the complete executable polynomial-bound claim remains
open until round 006; all finite passing tests above retain their original scope.

**Experience extraction:** updated [central deletion](../../../../research/experience/central-interval-deletion.md)
with the full candidate proof and its pending review status. The source-encoding
counterexample will be extracted with its repaired test in round 006.

## Next action

Verify independently and request review only with passing full-rule checks.

Literature audit, 2026-09-15: searches for `"unit 2-interval" "K4"
recognition`, `"unit" "2-interval" "depth 3" recognition`, `"unit 2-interval"
"clique number" NP`, and `"unit 2-interval" "depth" "2026"` found no matching
resolution. The [2025 journal](https://www.sciencedirect.com/science/article/pii/S0166218X24004013)
retains depth three in its concluding questions. The older
[TU Delft thesis](https://repository.tudelft.nl/file/File_3ba7af4e-e732-4041-b792-4205cbc08f89)
lists unrestricted unit recognition as unknown in its table, page 18; the
search engine's recent crawl date is not evidence of a recent research result.
[Jana, Roy and Sandeep 2026](https://arxiv.org/pdf/2607.13517), Section 8,
Proposition 28 and Theorem 5, use the published colored recognition theorem
and replace black vertices by large cliques for a total vertex-splitting budget.
That construction does not preserve depth three or K4-freeness. It does not
establish this candidate theorem. Unindexed manuscripts and an exhaustive
citation graph remain outside coverage; novelty is provisional.

The independent verification oracle identifies the *published* private black
vertex gadgets directly from target adjacency, reduces them to one-interval
vertices by Claims 18–20, and solves the remaining real interval constraints.
It never imports candidate or prepared-checker code or infers target decisions
from the source formula. Its positive certificates are extended with explicit
rational gadget coordinates and checked against the entire actual target graph.
This does not replace the unchanged prepared direct oracle, whose run remains
pending. Oracle comparison evidence is under `work/evidence/oracle-comparison/`.

Oracle repair: comparison with a triangle whose three vertices each have three
private leaves exposed overlapping recognizable black gadgets. The independent
oracle asserted disjointness instead of selecting nonoverlapping inverse
applications. It now skips occurrences intersecting already removed vertices
or already selected roots. The affected graph is rechecked against the unchanged
generic oracle. The failure and original oracle are preserved under
[oracle comparison](../../work/evidence/oracle-comparison/). This is a checker
repair, not a new reduction or research round. Generated target gadgets have
disjoint private sets; verify this scope before reusing the in-progress run.

A second exact verification method uses Z3 on the component-edge split first,
then rational interval constraints separately for each connected split component.
Claw, net and four-cycle clauses are necessary conditions derived directly from
unit interval graphs, independent of the proposed reduction. An infeasible
induced split component yields a sound blocking clause. The declared finite
budget is 64 split candidates per target; exhaustion raises an explicit error.
A positive result must still validate the full target representation exactly.
The initial implementation omitted the optional four-cycle cuts; its in-progress
run is retained separately. Adding these redundant constraints does not alter
the target predicate. Neither method has a wall-clock timeout.

Both the split-plus-unordered-linear check and the split-plus-LBFS check
completed all seven full source instances, including two 1,872-vertex NO
outputs and the 936-vertex YES output. Each completed run made ten successful
recovery calls. [Unordered output](split-cycles.jsonl),
[ordered output](ordered-splits.jsonl). The earlier split run without four-cycle
clauses exhausted its explicit 64-candidate budget on the positive-unit case;
this was an oracle search-budget result, not a reduction counterexample.

The original direct-real prepared run, direct-real peeled verification run,
and CP-SAT run were interrupted after their replacements completed the relevant
full-instance coverage. They are incomplete, not failed mathematical cases or
passing suites. No wall-clock cutoff was installed. Their raw partial logs
remain [here](prepared.jsonl), [here](independent.jsonl), and [here](cp-sat.jsonl).

Prepared target solving now uses the exact split method on the *entire uncolored
output graph*, whereas verification first removes the known private gadgets.
Both use the shared `split_oracle.py` SAT and coordinate routines; their
Fraction witness validators and source checks are separate. This shared solver
is a correlated-risk limitation for independent review, not two independent
proofs. The original real encoding remains for colored probes and comparisons,
with its previous complete implementation preserved in the oracle-comparison
directory. The new self-test passed; the full prepared harness is running again.

The coordinate subproblem now uses Corneil's published three-sweep LBFS
recognition algorithm, Section 2, pages 373–375 of
[the primary paper](https://kam.mff.cuni.cz/~ksemweb/clanky/Corneil-unit-interval-gr-recognition.pdf).
It verifies consecutive closed neighborhoods, then solves ordered difference
constraints with Z3. Its decisions agree with the original real interval
encoding on all 209 unlabeled graphs of order at most six:
[check](../../work/evidence/oracle-comparison/lbfs.py),
[output](../../work/evidence/oracle-comparison/lbfs.jsonl). This is a textbook
oracle component, not a research contribution. Four-component cliques are
forbidden in the split SAT instance to enforce depth three on arbitrary graphs.

The unpeeled full-graph split experiment was also interrupted without a
nonempty-case verdict. The final testing path reuses the completed graph-only
normalization and split solver for both harnesses, retaining their independent
source and exact witness checks. This removes the duplicate target-solver
implementation instead of maintaining multiple engines. Current code is
`work/split_oracle.py`; the complete earlier peeled outputs apply unchanged.
The prepared harness is being rerun through that solver. Direct real-arithmetic
comparisons explicitly request two slots per vertex and remain independent.
All superseded implementations cited above are retained as experiment snapshots.
