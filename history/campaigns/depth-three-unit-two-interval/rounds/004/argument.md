# Conditional soundness of central deletion

This is a local proof audit, not a complete or independently reviewed reduction.
All intervals are open and have length one. A component graph is an interval
graph and contains neither an induced claw, an induced four-cycle, nor an
induced net (a triangle with three pairwise nonadjacent private leaves).
For a net, the three independent leaf intervals have a left-to-right order;
the central leaf separates the outer two, while the triangle intervals have
a common point. The two outer triangle vertices cannot both reach their
leaves past the middle leaf without creating a forbidden extra adjacency.

## Variable structure

A and B are nonadjacent black vertices, p,q,n white, with all six black-white
edges, pq, and no other internal edges. In the full construction p has its
positive-three-clause neighbors and q has its private two-clause black L.

Each black interval meets exactly one component of each white port: meeting
both components of a positive port and one of n would form a claw; for n,
use a positive port. The p and q components meeting a common black interval
must meet each other, again by the claw with n. A port is **free** if a
component meets neither A nor B. It is then a bridge plus a free component;
otherwise its two components meet A and B separately. A bridge of n and a
bridge of either positive port would induce a four-cycle with A,B. Hence
positive and negative free ports cannot coexist.

If p is not free but q is free, q's bridge meets A and B, p splits across
A and B, and n also splits (by the four-cycle obstruction). If a component
of p meeting A has an external neighbor E, the triangle A,p_A,q_bridge with
leaves n_A,E,B is an induced net. Each missing edge follows from the graph
construction and unique incidence at a black vertex. The B case is symmetric.
Since p has external neighbors, this is impossible. Thus p not free implies
q not free. The symmetric claim holds when q has an external neighbor.
This proves that any represented full variable has free mask 000,001, or 110,
without using C. It deliberately retains 000.

## Three-clauses

Suppose all three incident p ports are not free. By the preceding argument
their q companions split across A,B too. If a p uses both components for
clause edges, choose a component of q incident to its private black L. It
meets one of A,B, say A. Then A,p_A,q_A with leaves n_A,a clause neighbor
of p_A,L is a net. The two external leaves are nonadjacent: L only meets
its two q/n ports and its private leaf, never a p vertex. All other absent
edges follow from the construction. Thus each p uses only one component
for all its clause edges. These three components form a triangle; one black
neighbor of each is a private leaf. This is another induced net. Therefore
every three-clause has a free positive port.

## Two-clauses

Let u,v be its incident ports and L its black vertex, with private black
leaf P. L cannot meet two components of u: together with P they are claw
leaves; likewise for v. The components u*,v* meeting L must intersect, or
u*,v*,P would be claw leaves. If neither u nor v is free, each of u*,v*
meets a black A/B interval from its own variable. Those two intervals and
P are private independent leaves on the triangle u*,v*,L, a net. Thus at
least one incident literal port is free. This proof does not require a
claim that every variable has a free port.

## Recovery

Set a variable true if p or q is free; otherwise set it false. The exclusive
sign lemma makes every free literal true under this assignment, including
n. The two coverage lemmas therefore satisfy every clause. The neutral
mask can safely receive false. These statements assume distinct variables
in each clause and the exact port-specific edges of the construction.

## Occurrence cycle

First eliminate tautological clauses and deduplicate literals within each
clause. Expand a unit literal l into all four (l or +/-a or +/-b) clauses
with fresh a,b; expand a two-literal clause into (l1 or l2 or a) and
(l1 or l2 or not a). These operations preserve satisfiability and allow
restriction of any satisfying assignment to the original variables.
Duplicate each resulting three-clause once, so every used variable has at
least two occurrences. Every clause now has three distinct variables.

Give each occurrence its own y, positive in its three-clause. If occurrence
i has sign s_i, write b_i=y_i when positive and b_i=not y_i otherwise.
For each original variable's cyclic occurrence list, add (not b_i or b_next).
All b_i must be equal: if one is true, implications propagate around the
cycle; otherwise all are false. Each y occurs once positive and once
negative in its two cycle clauses, and once positive in its three-clause.
The two variables in each cycle clause are distinct. Recovery takes one
b_i per used variable; unused original variables receive false.
The finite check in cycle.py independently enumerates lengths 2–5; the
cycle argument above holds for every length at least two.
