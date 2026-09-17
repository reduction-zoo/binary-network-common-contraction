from pathlib import Path
from itertools import product,combinations
import json,sys,z3
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work'))
import check

def build(ports):
    n=len(ports);edges=[];counts=[1,1,2,2,2]*n
    for i in range(n):edges += [(5*i+b,5*i+w) for b in range(2) for w in range(2,5)]+[(5*i+2,5*i+3)]
    ends=[5*i+p for i,p in enumerate(ports)]
    edges+=list(combinations(ends,2))
    if n==2:
        l=len(counts);counts += [1,1];edges += [(v,l) for v in ends]+[(l,l+1)]
    for i,p in enumerate(ports):
        for q in (2,3,4):
            if q!=p:edges.append((5*i+q,len(counts)));counts.append(1)
    g={'n':len(counts),'edges':sorted([sorted(e) for e in edges])}
    return g,counts

def free(left,i,p):
    return z3.Or(*[z3.And(*[z3.Or(a+1<=b,b+1<=a) for row in left[5*i:5*i+2] for b in row]) for a in left[5*i+p]])

def run(ports,truth=None):
    g,counts=build(ports);s,left=check.encoding(g,counts,3)
    if truth is None:
        s.add(*[z3.Not(free(left,i,p)) for i,p in enumerate(ports)])
    else:
        for i,t in enumerate(truth):
            for p,want in zip((2,3,4),(t,t,not t)):s.add(free(left,i,p)==want)
    yes=check.sat_result(s);w=check.model_witness(s,left) if yes else None
    if yes:assert check.target_witness(g,w,counts,3)
    print(json.dumps({'ports':ports,'truth':truth,'yes':yes,'witness':w}),flush=True)
run([2,2,2])
for truth in product((False,True),repeat=3):
    if any(truth):run([2,2,2],truth)
for ports in ([3,3],[3,4],[4,4]):run(ports)
