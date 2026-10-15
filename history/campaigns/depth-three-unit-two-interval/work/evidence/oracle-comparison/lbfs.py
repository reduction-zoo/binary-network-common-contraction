from pathlib import Path
import sys,json,networkx as nx
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import check,split_oracle
count=0
for g in nx.graph_atlas_g():
    if len(g)>6:break
    expected=all(split_oracle.unit_order(g.subgraph(c)) is not None for c in nx.connected_components(g))
    instance={'n':len(g),'edges':[sorted(e) for e in g.edges()]}
    actual,_=check.target(instance,[1]*len(g),max(1,len(g)))
    assert actual==expected,(count,instance)
    count+=1
print(json.dumps({'unlabeled_graphs':count,'maximum_vertices':6,'all_match':True}))
