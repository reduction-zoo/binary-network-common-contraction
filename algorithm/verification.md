# Verification of the complete candidate

The fixed target remains binary-network common contraction with >=k internal
vertices. Both executable maps are in algorithm.py. No solver is used by the
candidate. The source explicitly lists its ground set.

## Commands and final evidence

From this campaign directory:

```
python3 work/check.py --self-test
python3 work/check.py --candidate work/algorithm.py
python3 work/verify.py --candidate work/algorithm.py
python3 rounds/006/input_checks.py
```

- [Prepared final run](../history/campaigns/binary-network-common-contraction/rounds/006/prepared-final.jsonl): eight sources,
  four YES and four NO, with four actual target-witness recovery calls.
- [Separate final run](../history/campaigns/binary-network-common-contraction/rounds/006/independent-final.jsonl): eleven sources,
  eight YES and three NO, with eighteen recovery calls. Target orders reach 117.
  A three-element positive case additionally forces one synchronized variable
  to remain separate from both A and B, then checks recovery from that target.
- [Input regressions](../history/campaigns/binary-network-common-contraction/rounds/006/encoding-repair/harness-final.json): three
  faulty subprocess fixtures rejected and seven malformed raw inputs handled.
- [Repaired oracle self-test](../history/campaigns/binary-network-common-contraction/rounds/006/encoding-repair/self-test.json):
  eight source comparisons against enumeration, 112 target comparisons against
  direct contraction enumeration, and direct witness-validator regressions.

The two source suites overlap and are not nineteen distinct inputs. Earlier
runs before the decimal-parser repair are retained as prepared.jsonl and
independent-verification.jsonl in round 6; they are not additional coverage.
The graph construction and extraction rule did not change during that repair.

## Independence and coverage

The prepared checker uses Z3 with distance-ranked connected bags. The separate
verifier imports neither check.py nor algorithm.py. It uses OR-Tools CP-SAT
9.15.6755 with integer flows from a selected root in each bag. Unit demand at
every bag member, conserved flow, and zero capacity through other bags enforce
connectivity. Conversely a rooted spanning tree provides feasible flow for
every connected bag. Both models impose an acyclic quotient ordering, exact
cross-bag arc equality, and matching leaf-parent images. Exact-k suffices for
>=k because a larger common quotient can be contracted further.

The CP-SAT verifier derives source answers by exhaustive colorings. It solves
the actual subprocess-produced target, realizes its bags as contraction
sequences in both increasing and decreasing eligible-edge order, checks the
final arc and leaf-label isomorphism, and invokes the executable extractor on
both witnesses. Unknown statuses fail explicitly; they never count as NO.
There are no solver, subprocess or shell timeouts.

Cases include empty families and sets, singletons, duplicate sets, inactive
source elements, two- and three-element sets, overlapping clauses, a NO odd
cycle, and the explicit unassigned-variable witness. This is finite evidence,
not a proof for arbitrary instances or exhaustive target-witness enumeration.
Both checkers were written by the main researcher. The independent native review below supplies a separate assessment; solver
agreement alone is not a correctness proof.


## Independent review and manuscript

The [review](../history/campaigns/binary-network-common-contraction/reviews/complete-rule/review.md) returned **advance**. Its
[independent checker](../history/campaigns/binary-network-common-contraction/reviews/complete-rule/independent_check.py) imports
neither candidate nor author checkers. Its [results](../history/campaigns/binary-network-common-contraction/reviews/complete-rule/results.jsonl)
cover eight distinct sources (five YES, three NO), nine target queries, and
twelve successful recovery calls. Largest left/right input orders are 139/109.
The cases include two free variables with quotient size k+2 and merged
marked-path parents with size k+1, with both contraction orders replayed.
These finite checks supplement the general proof; suite counts overlap.

The [manuscript addendum](../history/campaigns/binary-network-common-contraction/reviews/complete-rule/manuscript-addendum.md)
retains advance and finds no theorem/construction mismatch. Its three optional
wording clarifications were applied. Only attribution, wording and layout
changed after candidate review; executable checks were therefore reused.

The [native Typst manuscript](../paper/manuscript.typ) compiles to [seven pages](../paper/manuscript.pdf).
All seven rendered pages and three vector figures were visually inspected.
Formula/setup page breaks and a duplicated figure-reference prefix were repaired.
The final language pass used how-to-technical-writing. Human expert assessment
of correctness, priority and significance remains outstanding.
