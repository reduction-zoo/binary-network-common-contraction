import json
from pathlib import Path
import sys
import z3
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work'))
from check import data,network,bag_encoding,realize,target_witness
edges=[('r','a'),('r','u'),('a','p'),('a','la'),('u','i'),('u','lu'),('p','i'),('p','x'),('i','o'),('o','q'),('o','z'),('q','d'),('q','y'),('d','lb'),('d','lc')]
vertices=sorted({v for e in edges for v in e});ids={v:i for i,v in enumerate(vertices)}
a=data(edges,['la','lu','x','z','y','lb','lc']);b=json.loads(json.dumps(a));b['leaves']['x'],b['leaves']['y']=b['leaves']['y'],b['leaves']['x']
results=[];maxima={}
for state in ['upstream','downstream','unassigned']:
    maxima[state]=0
    for k in range(1,9):
        solver=z3.Solver();ga,gb=network(a),network(b)
        ca,qa,pa=bag_encoding(solver,ga,k,'a');cb,qb,pb=bag_encoding(solver,gb,k,'b')
        solver.add([qa[e]==qb[e] for e in qa]);solver.add([pa[l]==pb[l] for l in pa])
        for colors in [ca,cb]:
            v,up,down=[colors[ids[n]] for n in ['i','a','d']]
            solver.add(up!=down)
            if state=='upstream':solver.add(v==up)
            elif state=='downstream':solver.add(v==down)
            else:solver.add(v!=up,v!=down)
        result=solver.check();assert result in (z3.sat,z3.unsat)
        row={'state':state,'k':k,'result':str(result)}
        if result==z3.sat:
            maxima[state]=k
            model=solver.model()
            ac={v:model.eval(c).as_long() for v,c in ca.items()};bc={v:model.eval(c).as_long() for v,c in cb.items()}
            ha,ka=realize(ga,dict(ac));hb,kb=realize(gb,dict(bc))
            w={'left':ha,'right':hb,'iso':[[v,kb[key]] for key,v in ka.items()]}
            target_witness({'left':a,'right':b,'k':k},w)
            row['witness']=w;row['left_colors']={vertices[v]:c for v,c in ac.items()}
        results.append(row)
assert maxima=={'upstream':4,'downstream':4,'unassigned':5},maxima
print(json.dumps({'left':a,'right':b,'maxima':maxima,'solver_queries':24,'results':results}))
