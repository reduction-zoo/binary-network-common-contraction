"""Reviewer-owned direct real-endpoint checks; imports no campaign code."""
import json
from itertools import combinations
import z3


def model(slots, edges):
    x = [[z3.Real(f'x_{v}_{i}') for i in range(s)] for v, s in enumerate(slots)]
    s = z3.Solver()
    s.add(x[0][0] == 0)
    def hit(a, b):
        return z3.And(a < b + 1, b < a + 1)
    for row in x:
        if len(row) == 2:
            s.add(row[0] + 1 <= row[1])
    for u, v in combinations(range(len(slots)), 2):
        overlap = z3.Or([hit(a, b) for a in x[u] for b in x[v]])
        s.add(overlap if (u, v) in edges else z3.Not(overlap))
    return s, x, hit


def variable(base, edges):
    edges.update((base+b, base+w) for b in (0, 1) for w in (2, 3, 4))
    edges.add((base+2, base+3))


def run(name, solver, expected):
    result = solver.check()
    print(json.dumps({'check': name, 'result': str(result), 'expected': expected}), flush=True)
    assert str(result) == expected


# A private outside neighbor on p and q supplies exactly the full proof's
# external-neighbor premise. No depth or forbidden-subgraph cuts are imposed.
e = set()
variable(0, e)
e.update({(2, 5), (3, 6)})
s, x, hit = model([1, 1, 2, 2, 2, 1, 1], e)
free = [z3.Or([z3.And([z3.Not(hit(a, x[b][0])) for b in (0, 1)]) for a in x[v]]) for v in (2, 3, 4)]
for mask in range(8):
    s.push()
    s.add([f == bool(mask & (1 << i)) for i, f in enumerate(free)])
    run(f'variable-free-mask-{mask:03b}', s, 'sat' if mask in (0, 3, 4) else 'unsat')
    s.pop()

# Two-clause obstruction with distinct variables, one negative and one positive
# port. Removing other external edges enlarges the feasible family.
e = set()
variable(0, e)
variable(5, e)
e.update({(4, 8), (4, 10), (8, 10), (10, 11)})
s, x, hit = model([1, 1, 2, 2, 2]*2 + [1, 1], e)
for port, blacks in ((4, (0, 1)), (8, (5, 6))):
    s.add([z3.Or([hit(a, x[b][0]) for b in blacks]) for a in x[port]])
run('two-clause-no-free-port', s, 'unsat')

# Three-clause obstruction. Each q retains its private L only, a superfamily
# of restrictions of full representations. Components may duplicate edges.
e = set()
for base in (0, 5, 10):
    variable(base, e)
e.update(combinations((2, 7, 12), 2))
e.update({(3, 15), (8, 16), (13, 17)})
s, x, hit = model([1, 1, 2, 2, 2]*3 + [1]*3, e)
for base in (0, 5, 10):
    s.add([z3.Or(hit(a, x[base][0]), hit(a, x[base+1][0])) for a in x[base+2]])
run('three-clause-no-free-positive-port', s, 'unsat')
