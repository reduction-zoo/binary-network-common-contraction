# Round 004 — General clause proof and occurrence preprocessing

## Plan

Continue C deletion using the central-deletion experience: local clause coverage
is promising but its external-neighbor premises must hold globally. Derive a
signed occurrence-cycle transformation from 3SAT with distinct variables in
each clause; audit clause soundness without the discarded two-state claim.
Scope: this single construction and proof strategy, exact symbolic local
arguments plus finite enumeration of cycle assignments for lengths 2–5 and
all occurrence signs. Completion: either a complete conditional soundness
proof or a concrete gap/counterexample. No full target candidate yet.

## Evidence and diagnosis

[Argument](argument.md) gives the missing partial-assignment soundness proof.
The positive companion's private black L is automatically nonadjacent to
three-clause p neighbors, resolving the external-leaf issue. A bridge of one
positive port itself replaces C when excluding an asymmetric free mask.
Command `python3 campaigns/depth-three-unit-two-interval/rounds/004/cycle.py`:
[output](output.jsonl), 1,360 Boolean assignment checks across 60 sign patterns,
no solver queries, target instances or recoveries. No repairs. The general
cycle proof is independent of these finite enumerations. Time/token unavailable.

**Experience extraction:** updated central-deletion finding with the conditional
proof. Not independently reviewed. Next: complete the maps and depth bound.

## Next action

If soundness survives, prove depth-three completeness and remove colors.
