import itertools,json,sys
from pathlib import Path
import networkx as nx
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work'))
from check import source_solve,source_witness
subsets=[list(s) for k in range(1,4) for s in itertools.combinations(range(3),k)]
rows=[];accepted=0
for mask in range(128):
 sets=[s for i,s in enumerate(subsets) if mask>>i&1]
 g=nx.DiGraph([('R','A'),('R','B'),('A','B')])
 for x in range(3):g.add_edges_from([('A',f'x{x}'),(f'x{x}','B')])
 pins={'R':0,'A':1,'B':5}
 for j,s in enumerate(sets):
  u,v=f'u{j}',f'v{j}';pins[u]=1;pins[v]=5
  g.add_edge('R',u)
  for x in s:g.add_edges_from([(u,f'x{x}'),(f'x{x}',v)])
 count=0;free=0
 for choices in itertools.product(range(3),repeat=3):
  colors=dict(pins)
  for x,ch in enumerate(choices):colors[f'x{x}']=[1,5,2+x][ch]
  bags={c:[v for v in g if colors[v]==c] for c in set(colors.values())}
  if not all(nx.is_connected(g.subgraph(b).to_undirected()) for b in bags.values()):continue
  q=nx.DiGraph();q.add_nodes_from(bags);q.add_edges_from((colors[u],colors[v]) for u,v in g.edges if colors[u]!=colors[v])
  if not nx.is_directed_acyclic_graph(q):continue
  w=[int(ch==1) for ch in choices];source_witness({'elements':[0,1,2],'sets':sets},w)
  count+=1;free+=int(2 in choices)
 truth=source_solve({'elements':[0,1,2],'sets':sets}) is not None
 assert bool(count)==truth,(sets,count,truth)
 accepted+=count;rows.append({'sets':sets,'yes':truth,'valid_partial_assignments':count,'with_unassigned':free})
print(json.dumps({'families':128,'partition_checks':128*27,'source_queries':128,'accepted_partial_assignments':accepted,'rows':rows}))
