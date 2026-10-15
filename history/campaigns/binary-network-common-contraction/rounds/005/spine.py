import networkx as nx


def replace_vertex(g, v, x, y):
    incoming=sorted(g.predecessors(v));outgoing=sorted(g.successors(v))
    assert outgoing and x not in g and y not in g
    d,e=len(incoming),len(outgoing)
    nodes=[f'{v}~{i}' for i in range(2+max(0,d-1)+e-1)]
    assert not (set(nodes)&set(g))
    g.remove_node(v)
    g.add_nodes_from((u,{'label':''}) for u in nodes)
    g.add_edges_from(zip(nodes,nodes[1:]))
    g.add_node(x,label=x);g.add_node(y,label=y)
    g.add_edges_from([(nodes[0],x),(nodes[-1],y)])
    if incoming:g.add_edge(incoming[0],nodes[0])
    for i,parent in enumerate(incoming[1:],1):g.add_edge(parent,nodes[i])
    start=1+max(0,d-1)
    for i,child in enumerate(outgoing[:-1]):g.add_edge(nodes[start+i],child)
    g.add_edge(nodes[-1],outgoing[-1])
    return nodes


def encode(g):
    vertices=sorted(g);ids={v:i for i,v in enumerate(vertices)}
    return {'n':len(g),'edges':[[ids[u],ids[v]] for u,v in g.edges],
            'leaves':{g.nodes[v]['label']:ids[v] for v in g if g.nodes[v].get('label')}},ids
