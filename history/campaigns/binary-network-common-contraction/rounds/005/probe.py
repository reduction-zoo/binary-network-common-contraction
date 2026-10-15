import json,sys
from pathlib import Path
import networkx as nx
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work'))
from check import network
from spine import replace_vertex,encode
rows=[]
for d in range(1,5):
 for e in range(1,5):
  g=nx.DiGraph()
  if d==1:g.add_node('f0')
  else:
   for i in range(d-1):
    g.add_edge(f'r{i}',f'f{i}')
    g.add_edge(f'r{i}',f'r{i+1}' if i<d-2 else f'f{d-1}')
  for i in range(d):g.add_edges_from([(f'f{i}','v'),(f'f{i}',f'l{i}')])
  for i in range(e):g.add_edge('v',f'o{i}')
  nx.set_node_attributes(g,'','label')
  for v in g:
   if g.out_degree(v)==0:g.nodes[v]['label']=v
  expected=g.copy();expected.add_node('x',label='x');expected.add_node('y',label='y');expected.add_edges_from([('v','x'),('v','y')])
  nodes=replace_vertex(g,'v','x','y');encoded,ids=encode(g);network(encoded)
  assert all(nx.has_path(g,nodes[0],v) and nx.has_path(g,v,nodes[-1]) for v in nodes)
  mapping={v:'v' if v in nodes else v for v in g}
  arcs={(mapping[u],mapping[v]) for u,v in g.edges if mapping[u]!=mapping[v]}
  assert arcs==set(expected.edges)
  assert nx.is_directed_acyclic_graph(g)
  rows.append({'in':d,'out':e,'vertices':len(g),'spine_vertices':len(nodes),'network':encoded})
print(json.dumps({'templates':len(rows),'rows':rows}))
