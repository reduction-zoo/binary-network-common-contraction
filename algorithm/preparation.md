# Preparation

Z3 5.1.0 decides Set Splitting directly by requiring both Boolean values in
every listed set. The target solver assigns each internal vertex to one of k
nonempty bags. Each bag is connected using a distance-to-minimum-vertex encoding
on the undirected induced graph. Every nonminimum bag member has a same-bag
neighbor of smaller distance. Distinct bag indices follow a topological order.
Both sides have exactly the same quotient arcs and leaf-parent bags.

Definition 5 and Proposition 5 of the primary paper justify this representation.
For a common quotient larger than k, admissible contractions of that quotient
reduce it to k (Proposition 2); thus exact-k feasibility decides >=k. k=0 is
handled as k=1. A threshold above either internal vertex count is immediately NO.
A SAT model is converted to concrete admissible contractions by selecting a
same-bag internal arc with no alternative directed path; failure is explicit.
The resulting sequences and complete isomorphism are checked independently.
Only solver UNSAT means NO; other statuses fail explicitly. These are exponential
experimental oracles, never candidate runtime algorithms. No timeouts are used.

Commands from repository root:

- `python3 campaigns/binary-network-common-contraction/work/check.py --self-test`
- The [harness check](../history/campaigns/binary-network-common-contraction/work/evidence/preparation/harness.json) executes the deliberately
  [faulty subprocess](../history/campaigns/binary-network-common-contraction/work/evidence/preparation/faulty_candidate.py), detecting a
  decision mismatch, malformed target and incorrect recovered assignment.

The [self-test](../history/campaigns/binary-network-common-contraction/work/evidence/preparation/self-test.json) covers eight source cases,
cross-checked by exhaustive colorings, and 112 target comparisons on four
networks of orders 7 and 9 and thresholds 0 through 6. Target comparisons use
separate direct contraction enumeration with leaf-preserving graph isomorphism.
Returned SAT witnesses are replayed. Invalid sequence, isomorphism, target and
source-witness fixtures are rejected. The inherited display/contraction
counterexample is a negative target regression, not a new discovery round.

The encodings are separate from future candidates but authored by the main
researcher; this is not independent agent review. Finite agreement does not
establish general solver implementation correctness. Candidate testing has not
occurred: no candidate reduction exists yet. The harness currently requests one
solver witness per YES target; broader witness coverage is required when a full
candidate becomes available.

## Explicit ground-set repair in round 6

The source now uses `elements: [0,...,n-1]` instead of a numeric n with an
implicitly listed universe. This aligns with the fixed question and bounds the
n-bit recovered witness by explicit input length. No mathematical decision
problem changed. The original checker, contract, cases and partial-assignment
probe were [preserved](../history/campaigns/binary-network-common-contraction/rounds/006/encoding-repair).
The unchanged eight mathematical source cases and 112 target comparisons pass
under the repaired encoding; see [self-test](../history/campaigns/binary-network-common-contraction/rounds/006/encoding-repair/self-test.json).
The round-4 reproducer now supplies the explicit elements list when calling
source predicates; its mathematical graphs and recorded experiment remain unchanged.

[Input checks](../history/campaigns/binary-network-common-contraction/rounds/006/input_checks.py) rerun all three faulty subprocess
fixtures and seven malformed raw inputs against the final parser, including a
5,001-digit out-of-domain index. [Results](../history/campaigns/binary-network-common-contraction/rounds/006/encoding-repair/harness-final.json).
The candidate disables Python's decimal conversion digit cap. This parser-only
repair does not change the graph construction. Both candidate suites were rerun.
