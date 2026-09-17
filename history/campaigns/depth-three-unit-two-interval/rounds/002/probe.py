from pathlib import Path
from itertools import product
import json,sys,z3
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work'))
import check
for leaves in (False,True):
    g={'n':8 if leaves else 5,'edges':[[b,w] for b in range(2) for w in range(2,5)]+[[2,3]]+([[2,5],[3,6],[4,7]] if leaves else [])}
    counts=[1,1,2,2,2]+([1]*3 if leaves else [])
    for mask in product((False,True),repeat=3):
        solver,left=check.encoding(g,counts,3)
        for v,want in zip((2,3,4),mask):
            free=z3.Or(*[z3.And(*[z3.Or(a+1<=b,b+1<=a) for row in left[:2] for b in row]) for a in left[v]])
            solver.add(free==want)
        yes=check.sat_result(solver)
        w=check.model_witness(solver,left) if yes else None
        if yes:assert check.target_witness(g,w,counts,3)
        print(json.dumps({'leaves':leaves,'black_free':mask,'yes':yes,'witness':w}),flush=True)
