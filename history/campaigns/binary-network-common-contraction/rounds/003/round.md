# Round 3: does synchronization reward an unassigned variable?

## Plan

Action: investigate the composition premise. Extend the round-2 interval with
an upstream anchor a and downstream anchor d, keeping both input networks binary.
The synchronized variable bag V can potentially merge with a or d. Test whether
keeping V separate yields a larger common contraction, defeating a lower-bound
size threshold intended to select assignments.

Finite scope: one 15-vertex input pair, swapping the two bracket taxa between
networks. For thresholds 1 through 8 and each of three states V=a, V=d, and
V distinct from both, solve exact connected quotient bags with a and d distinct.
Twenty-four declared Z3 queries. Realize and directly validate every positive
witness. Derive only the scoring consequence for this explicit interface.
No complete source construction or universal impossibility claim is intended.

Experience: use the synchronized interval from round 2; do not repeat round 1.
The new uncertainty is global objective compatibility, not local equality.

## Evidence and diagnosis

`python3 rounds/003/probe.py > rounds/003/result.json` from the campaign directory.
Twenty-four Z3 queries: nine SAT and fifteen UNSAT; nine concrete witnesses
realized and directly checked. Both inputs have fifteen vertices. Exact maxima:
unassigned V has five internal quotient vertices, whereas either assigned
state has four. The [output](result.json) contains every query result and
positive witness, not just the maxima.

General size argument: four forced interval vertices consume three of the eight
internal vertices, leaving at most five. An assignment merges one further
vertex into that interval, leaving at most four. Positive witnesses attain
both bounds. Every lower-bound threshold accepting an assigned witness also
accepts the larger unassigned witness. This is an objective-compatibility defect
of the explicit interface, not an impossibility result for clause attachments.
See the current [partial proof](../../work/proof.md).

Experience extraction: a third reusable finding, pending shared write scope,
proposed `research/experience/contraction-anchors-reward-unassigned-bags.md`.
Premises: private synchronized interval, >=k quotient-size objective, no
additional assignment-dependent compensation. No shared file written.

## Next action

The initial three-round allocation is exhausted. This is not an evidence-based
rejection of the topic: one compositional mechanism has just become testable.
A next allocation should attach a clause module and compare its maximum common
quotient score for assigned and unassigned variable bags. It must produce an
assignment-dependent gain sufficient to offset the extra unassigned bag.
Do not rerun the unprotected split or the unchanged synchronized pair.
