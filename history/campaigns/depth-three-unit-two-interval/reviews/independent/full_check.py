"""A hand-designed full target witness, independent of both campaign solvers."""
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import z3

candidate = Path(__file__).resolve().parents[2] / 'work' / 'algorithm.py'
source = {'n': 10**100, 'clauses': [[1, -2, 10**100]]}

def call(data, extract=False):
    cmd = [sys.executable, str(candidate)] + (['--extract'] if extract else [])
    return json.loads(subprocess.run(cmd, input=json.dumps(data), text=True,
                                    capture_output=True, check=True).stdout)

graph = call(source)
assert graph['n'] == 234 and len(graph['edges']) == 288
left = []
black = []
for i in range(6):
    t = F(10*i)
    other = (i+3) % 6
    left.extend([[t], [t+F(3,2)], [t+F(3,4), F(1000+10*(i//3))],
                 [t+F(3,4), F(10*other)-F(11,10)],
                 [t-F(1,2), t+2]])
    black.extend([5*i, 5*i+1])
for i in (0, 3, 1, 4, 2, 5):
    anchor = (i+3) % 6 if i in (1, 4) else i
    t = F(10*anchor)
    black.extend([len(left), len(left)+1])
    left.extend([[t-F(13,10)], [t-F(22,10)]])

# Solve only the fixed, published nine-vertex attachment, independently.
edges = {(0,1), (0,5), (1,5)} | {(1,i) for i in (2,3,4)} | {(5,i) for i in (6,7,8)}
x = [[z3.Real(f'b_{v}_{i}') for i in range(1 if v==0 else 2)] for v in range(9)]
s = z3.Solver()
s.add(x[0][0] == 0)
for row in x[1:]:
    s.add(row[0]+1 <= row[1])
for u, v in combinations(range(9), 2):
    hit = z3.Or([z3.And(a < b+1, b < a+1) for a in x[u] for b in x[v]])
    s.add(hit if (u,v) in edges else z3.Not(hit))
assert s.check() == z3.sat
m = s.model()
template = [[F(str(m.eval(a))) for a in row] for row in x]
lo = min(a for row in template for a in row)
hi = max(a for row in template for a in row)
for j, v in enumerate(black):
    shift = F(2000) + j*(hi-lo+10)-lo
    left[v].append(shift)
    left.extend([[a+shift for a in row] for row in template[1:]])

def validate(rows):
    assert len(rows) == graph['n'] and all(len(row)==2 for row in rows)
    assert all(abs(row[0]-row[1]) >= 1 for row in rows)
    actual = [[u,v] for u,v in combinations(range(len(rows)),2)
              if any(abs(a-b)<1 for a in rows[u] for b in rows[v])]
    assert actual == graph['edges']
    starts = [a for row in rows for a in row]
    assert max(sum(b <= a < b+1 for b in starts) for a in starts) <= 3

for name, rows in [('hand-designed', left),
                   ('reflected-permuted-translated',
                    [[-a-1+F(10**80, 97) for a in row[::-1 if i%2 else 1]]
                     for i,row in enumerate(left)])]:
    validate(rows)
    witness = {'left': [[str(a) for a in row] for row in rows]}
    result = call({'source': source, 'target_solution': witness}, True)['assignment']
    assert all(type(v) is bool for v in result.values())
    assert all(k == str(int(k)) and 1 <= int(k) <= source['n'] for k in result)
    assert all(any(result.get(str(abs(l)), False) == (l>0) for l in clause)
               for clause in source['clauses'])
    print(json.dumps({'check': name, 'vertices': len(rows), 'valid_target': True,
                      'valid_recovery': True, 'assignment': result}), flush=True)
