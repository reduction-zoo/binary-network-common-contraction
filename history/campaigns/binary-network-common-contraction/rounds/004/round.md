# Round 4: use partial assignments instead of penalizing every free variable

## Plan

Action: reconsider recovery. The prior score objection assumed that every
variable must merge with a truth anchor. That may be unnecessarily strong:
Set Splitting admits recovery from a partial coloring whenever every set
already contains an A-colored and a B-colored element. Unassigned elements
can then receive any color. Test connected-bag clause incidence with synchronized
variable nodes and permit unused variable bags.

Finite scope: all 128 families of the seven nonempty subsets of three elements.
For each, compare exact Set Splitting against existence of a connected quotient
partition of a small nonbinary incidence graph, with R,A,B distinct, every U_s
pinned to A and V_s to B, and element vertices allowed A, B or separate free
bags. Enumerate all 27 partial assignments per family and check graph connectivity
and quotient acyclicity directly with NetworkX; compare with the prepared Z3
source oracle (128 calls). Check every accepted partial coloring directly.
This changes the recovery premise, not the source or target. The intermediate
incidence graph is not a binary Karp output; binary enforcement remains required.

Experience: round 3 applies only if full assignment is necessary. Investigate
that premise before searching for compensation gadgets. Existing reservoir
entries concern graph cuts, not contraction bags; no direct transfer is used.

## Evidence and diagnosis

`python3 rounds/004/probe.py > rounds/004/result.json` from the campaign directory.
All 128 source families agree with 3,456 directly checked graph partitions.
Every accepted partial assignment recovers a source coloring. The result file
records family-level counts, including accepted states with unassigned elements.

General reason: U_s has neighbors R and its incident element vertices. Since
R differs from A, its A-bag can connect to the distinguished A only through
an element in A. Similarly, V_s can connect to B only through an element in B.
Thus every set already has both colors; remaining elements may be colored
arbitrarily. Conversely, a valid split connects all pinned clause vertices to
the corresponding anchors, and every resulting quotient is acyclic.

The score defect of round 3 need not be repaired by assigning every variable.
The actual unresolved issue is forcing R,A,B distinct and the clause bags in
binary input pairs. This is a more promising route than compensating all free
variable bags. The nonbinary incidence graph is still only an intermediate model.

Experience extraction: extend the pending unassigned-bag finding with this
applicability correction, not a new generic failure claim. The existing
[partial-assignment entry](../../../../research/experience/central-interval-deletion.md)
suggested checking clause coverage; it helped change the recovery premise,
not supply a proven contraction gadget. Its shared use-history update is pending
under the campaign-only write scope.

## Next action

Binaryize incidence vertices using a directed spine with a taxon at each end.
Synchronized endpoint parents force every port along the spine into one bag.
For fixed-color vertices, the second network can collect the endpoint taxa;
for variables, reversed endpoint order can synchronize without fixing the color.
