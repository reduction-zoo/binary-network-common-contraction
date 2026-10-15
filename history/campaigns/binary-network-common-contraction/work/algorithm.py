import json
import sys
import networkx as nx

sys.set_int_max_str_digits(0)


def valid_source(x):
    if type(x) is not dict or set(x) != {'elements','sets'}:
        return False
    if type(x['elements']) is not list or any(type(v) is not int or v != i for i,v in enumerate(x['elements'])):
        return False
    if type(x['sets']) is not list:
        return False
    n=len(x['elements'])
    return all(type(s) is list and all(type(i) is int and 0<=i<n for i in s) and len(set(s))==len(s) for s in x['sets'])


def spine(g, v, x, y):
    incoming=sorted(g.predecessors(v));outgoing=sorted(g.successors(v))
    d,e=len(incoming),len(outgoing)
    nodes=[f'{v}~{i}' for i in range(2+max(0,d-1)+e-1)]
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
    return {'n':len(g),'edges':sorted([[ids[u],ids[v]] for u,v in g.edges]),
            'leaves':{g.nodes[v]['label']:ids[v] for v in vertices if g.nodes[v].get('label')}},ids


def leaf(g, parent, label):
    g.add_node(label,label=label);g.add_edge(parent,label)


def constant(yes):
    def tree(order):
        a,b,c,d=order
        g=nx.DiGraph([('r','u'),('r','v'),('u',a),('u',b),('v',c),('v',d)])
        nx.set_node_attributes(g,'','label')
        for v in 'abcd':g.nodes[v]['label']=v
        return encode(g)[0]
    return {'left':tree('abcd'),'right':tree('abcd' if yes else 'acbd'),'k':3}


def build(source):
    if not source['sets']:
        return constant(True),None
    if any(len(s)<2 for s in source['sets']):
        return constant(False),None
    active=sorted({x for s in source['sets'] for x in s})
    length=len(active)+1
    g=nx.DiGraph([('R','A'),('R','B'),('A','B')])
    h=g.copy()
    groups={v:v for v in ['R','A','B']}
    for x in active:
        name=f'X{x}'
        g.add_edges_from([('A',name),(name,'B')]);h.add_edges_from([('A',name),(name,'B')])
    for j,s in enumerate(source['sets']):
        u,v=f'U{j}',f'V{j}'
        groups[u]='A';groups[v]='B';g.add_edge('R',u)
        for x in s:g.add_edges_from([(u,f'X{x}'),(f'X{x}',v)])
        leaf(g,u,f'clause:{j}:u');leaf(g,v,f'clause:{j}:v')
        leaf(h,'A',f'clause:{j}:u');leaf(h,'B',f'clause:{j}:v')
    for graph in [g,h]:
        for start,end in [('R','A'),('A','B')]:
            previous=start
            for i in range(length):
                name=f'P{start}{end}{i}'
                graph.add_edge(previous,name)
                leaf(graph,name,f'path:{start}:{end}:{i}')
                previous=name
            graph.add_edge(previous,end)
    for group in ['R','A','B']:
        c=f'C{group}';g.add_edge(group,c)
        leaf(g,c,f'H:{group}:x');leaf(g,c,f'H:{group}:y')
    for v,group in groups.items():
        leaf(h,group,f'G:{v}:x');leaf(h,group,f'G:{v}:y')
    gs={}
    for v in sorted(groups):gs[v]=spine(g,v,f'G:{v}:x',f'G:{v}:y')
    for x in active:
        v=f'X{x}'
        gs[v]=spine(g,v,f'G:{v}:x',f'G:{v}:y')
        spine(h,v,f'G:{v}:y',f'G:{v}:x')
    for v in ['R','A','B']:spine(h,v,f'H:{v}:x',f'H:{v}:y')
    left,ids=encode(g);right,_=encode(h)
    metadata={'A':ids[gs['A'][0]],'B':ids[gs['B'][0]],
              'variables':{x:ids[gs[f'X{x}'][0]] for x in active}}
    return {'left':left,'right':right,'k':2*length+3},metadata


def extract(source,witness):
    target,metadata=build(source)
    if metadata is None:
        if source['sets']:
            raise ValueError('NO constant has no valid target witness')
        return [0]*len(source['elements'])
    representative=list(range(target['left']['n']))
    for u,v in witness['left']:
        keep,remove=min(u,v),max(u,v)
        representative=[keep if p==remove else p for p in representative]
    color_b=representative[metadata['B']]
    colors=[0]*len(source['elements'])
    for x,v in metadata['variables'].items():colors[x]=int(representative[v]==color_b)
    return colors


if __name__=='__main__':
    try:
        payload=json.load(sys.stdin)
    except ValueError:
        print(json.dumps({'invalid':True}));sys.exit(0)
    extracting=sys.argv[1:]==['--extract']
    if sys.argv[1:] not in ([],['--extract']):
        raise ValueError('unknown command arguments')
    if extracting:
        if type(payload) is not dict or set(payload)!={'source','target_solution'}:
            raise ValueError('invalid extraction input')
        source=payload['source']
    else:source=payload
    if not valid_source(source):print(json.dumps({'invalid':True}))
    elif extracting:print(json.dumps(extract(source,payload['target_solution'])))
    else:print(json.dumps(build(source)[0]))
