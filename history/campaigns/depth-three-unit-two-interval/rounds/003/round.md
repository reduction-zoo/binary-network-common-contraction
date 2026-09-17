# Round 003 — Clause coverage under partial truth states

## Plan

Use [central deletion](../../../../research/experience/central-interval-deletion.md):
000 survives, so replace the two-state obligation with clause coverage.
Three variable copies with a triangle on p and private one-interval leaves
on q,n: ask whether all three p can be black-bound, then whether each of the
seven nonzero truth assignments has a representation with its designated
black-free mask (110 for true,001 for false). Also test three two-clause types
qq,qn,nn using L and its private leaf, private leaves on unused ports, and
both incident ports black-bound. Exactly eleven queries. No full formula
construction or general proof yet. Failure of coverage rejects this extraction;
success justifies a general local proof audit.

## Evidence and diagnosis

[Output](output.jsonl), command `python3 campaigns/depth-three-unit-two-interval/rounds/003/probe.py`:
eleven queries; seven positive witnesses fraction-checked. All four coverage
counterexample queries UNSAT. Seven satisfying three-clause truth modes SAT.
No full source instance or extraction, no repairs; time/token totals unavailable.
The neutral state did not break these local clauses. However private leaves
are a restriction, not arbitrary external graph vertices: the induced-net
argument needs their mutual nonadjacency. Audit the occurrence-copy reduction
before generalizing. Prospects medium, uncalibrated.

**Experience extraction:** updated the central-deletion finding with the local
coverage results and the unverified external-neighbor premise.

## Next action

Resolve the local proof, or retain the counterexample before changing gadgets.
