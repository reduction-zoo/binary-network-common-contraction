import json
from pathlib import Path
import sys
import z3
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work'))
from check import data,network,bag_encoding,target_solve
edges=[('r','p'),('r','u'),('p','x'),('p','i'),('u','i'),('u','w'),('i','o'),('o','q'),('o','z'),('q','y'),('q','t')]
vertices=sorted({v for e in edges for v in e});ids={v:i for i,v in enumerate(vertices)}
a=data(edges,'xwyzt')
b=json.loads(json.dumps(a));b['leaves']['x'],b['leaves']['y']=b['leaves']['y'],b['leaves']['x']
results=[]
for k in range(1,7):
 x={'left':a,'right':b,'k':k};w=target_solve(x)
 solver=z3.Solver();ca,qa,pa=bag_encoding(solver,network(a),k,'a');cb,qb,pb=bag_encoding(solver,network(b),k,'b')
 solver.add([qa[e]==qb[e] for e in qa]);solver.add([pa[l]==pb[l] for l in pa])
 solver.add(z3.Or(ca[ids['i']]!=ca[ids['o']],cb[ids['i']]!=cb[ids['o']]))
 result=solver.check();assert result==z3.unsat
 assert (w is not None)==(k<=3)
 results.append({'k':k,'common':w is not None,'separated_halves':str(result),'witness':w})
print(json.dumps({'left':a,'right':b,'results':results,'solver_queries':12}))
