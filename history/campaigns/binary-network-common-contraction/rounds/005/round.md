# Round 5: bracket every port of a binary spine

## Plan

Action: construct. Replace a vertex with d incoming and e outgoing arcs by a
spine: first an x-leaf parent, then d-1 binary reticulations taking the remaining
incoming ports, then e-1 binary tree nodes exposing outgoing ports, then a
last y-leaf parent exposing the final outgoing port. Every internal spine node
lies between the two taxon parents; reversal or fixed-color leaf constraints
therefore synchronize all ports, including incoming reticulations omitted by
ordinary split trees.

Finite scope: d,e in 1..4 (16 templates), with binary feeder trees and leaf
outputs providing legal network contexts. Check every vertex degree and all
paths, contract the whole spine, and compare the incidence interface against
one mixed-degree vertex. No full second network or source reduction yet.
The explicit construction and arbitrary-degree proof matter; the sixteen
instances check implementation. No synthesis or parameter optimization.

Experience: round 4 permits free variable bags; rounds 1–2 require all ports,
not merely outgoing branches, in the synchronized interval.

## Evidence and diagnosis

`python3 rounds/005/probe.py > rounds/005/result.json` from the campaign directory.
All sixteen templates are binary, acyclic, preserve the intended port incidence
after collapsing their spines, and place every spine node between the endpoint
taxon parents. The [result](result.json) saves the sixteen explicit networks.

For d>=1 incoming and e>=1 outgoing arcs, the spine uses d+e internal vertices:
one first taxon parent, d-1 reticulations, e-1 outgoing tree nodes and one last
taxon parent. All nonroot internal degrees are (1,2) or (2,1). For d=0, the first
node is the root and has outdegree two. Every external edge remains incident to
a spine vertex, and collapsing the spine recovers the original vertex with the
two additional taxon leaves. Thus forced equality of endpoint parents forces
all port choices to agree, unlike round 1. The root case is used by the upcoming
composition and must be checked there; this finite probe covers d>=1 only.

Experience extraction: extend pending reversed-taxon synchronization with the
all-port spine construction and its d+e size. No separate generic entry needed.
No shared file was written. The local interface is not a complete reduction.

## Next action

Compose binary pairs. Force each reference anchor spine to collapse using a
cherry in the incidence network. Place all clause endpoint taxa on the matching
reference anchor. Use reversed variable endpoint taxa for synchronization.
Finally protect distinct anchors with long, taxon-marked paths: merging anchor
endpoints must collapse the entire path, overpowering free variable bags.
