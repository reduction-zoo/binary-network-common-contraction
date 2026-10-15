# Round 002 — Black-free ports with private external neighbors

## Plan

Continue the C-deletion route. Use the paper's actual predicate: at least one
representative avoids both black intervals. Test all eight masks first locally,
then with one private one-interval leaf on each literal port (a necessary
restriction of the full formula graph). Exactly sixteen depth-three QF_LRA
queries, with exact witness checks. Retrieve experience: no applicable stored
interval finding; round 001 supplies the local evidence. If either truth mode
is excluded after leaves, do not claim completeness from local masks.

## Evidence and diagnosis

Command: `python3 campaigns/depth-three-unit-two-interval/rounds/002/probe.py`.
[Output](output.jsonl): sixteen queries, eight validated positive witnesses,
zero source instances or recoveries, no repairs. Both truth modes survive.
Private leaves exclude 010 and 100 but still admit 000. Therefore the old
claim that exactly one sign has a free slot cannot be inherited after C deletion.
This is a soundness obligation, not yet a counterexample to the reduction:
a variable with no free literal might receive an arbitrary assignment if every
clause has another free literal. Check that weaker clause property next.

Primary check, 2026-09-15: [preprint](https://arxiv.org/pdf/2309.11908),
Claims 9–11, pages 9–11: Claim 9 explicitly uses C to exclude the no-free case.
Claims 15–16 must therefore be re-proved without invoking Claim 11.
Time/token totals unavailable.

**Experience extraction:** saved [central-interval-deletion](../../../../research/experience/central-interval-deletion.md).

## Next action

Decide whether clause composition or an interface replacement is justified.
