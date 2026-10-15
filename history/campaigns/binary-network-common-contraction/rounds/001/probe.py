import json
from pathlib import Path
import sys
import z3
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'work'))
from check import data, network, bag_encoding, realize
names = [('r','s'),('r','t'),('s','a'),('s','u'),('t','b'),('t','lr'),('a','i'),('a','la'),('u','i'),('u','lu'),('i','o'),('o','b'),('o','v'),('b','lb'),('v','lv'),('v','lw')]
vertices = sorted({v for edge in names for v in edge})
ids = {v:i for i,v in enumerate(vertices)}
n = data(names, ['la','lu','lr','lb','lv','lw'])
g = network(n)
solver = z3.Solver()
c,q,p = bag_encoding(solver,g,3,'single')
for label,color in [('lr',0),('la',1),('lu',1),('lb',2),('lv',2),('lw',2)]:
    solver.add(p[label] == color)
solver.add(c[ids['r']]==0, c[ids['s']]==0)
assert solver.check()==z3.sat
model=solver.model()
colors={v:model.eval(cv).as_long() for v,cv in c.items()}
assert (colors[ids['i']],colors[ids['o']])==(1,2)
history,keys=realize(g,dict(colors))
solver.add(c[ids['i']]==c[ids['o']])
assert solver.check()==z3.unsat
print(json.dumps({'network':n,'named_colors':{vertices[v]:color for v,color in colors.items()},'contractions':history,'quotient_vertices':len(keys),'split_halves':'SAT','equal_halves':'UNSAT','solver_queries':2}))
