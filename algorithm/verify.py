import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
import networkx as nx
from ortools.sat.python import cp_model


def run_candidate(path,payload,extract=False):
    p=subprocess.run([sys.executable,str(path)]+(['--extract'] if extract else []),input=json.dumps(payload),text=True,capture_output=True,check=True)
    return json.loads(p.stdout)


def graph(d):
    assert type(d['n']) is int and d['n']>=3
    assert len(d['edges'])==len(set(map(tuple,d['edges'])))
    assert all(type(i) is int and 0<=i<d['n'] for e in d['edges'] for i in e)
    assert all(len(e)==2 and e[0]!=e[1] for e in d['edges'])
    g=nx.DiGraph();g.add_nodes_from(range(d['n']));g.add_edges_from(d['edges'])
    assert nx.is_directed_acyclic_graph(g)
    roots=[u for u in g if g.in_degree(u)==0];assert len(roots)==1
    assert g.out_degree(roots[0])==2
    leaves=set(d['leaves'].values());assert len(leaves)==len(d['leaves'])
    assert leaves=={u for u in g if g.out_degree(u)==0}
    for u in g:
        if u in leaves:assert g.in_degree(u)==1
        elif u!=roots[0]:assert (g.in_degree(u),g.out_degree(u)) in ((1,2),(2,1))
    return g,leaves


def quotient_model(model,g,leaves,k,prefix):
    nodes=sorted(set(g)-leaves);n=len(nodes)
    c={u:model.new_int_var(0,k-1,f'{prefix}c{u}') for u in nodes}
    x={(u,b):model.new_bool_var(f'{prefix}x{u}_{b}') for u in nodes for b in range(k)}
    for (u,b),v in x.items():
        model.add(c[u]==b).only_enforce_if(v);model.add(c[u]!=b).only_enforce_if(v.negated())
    internal=[(u,v) for u,v in g.edges if u in c and v in c]
    undirected=set(internal)|{(v,u) for u,v in internal}
    for u,v in internal:model.add(c[u]<=c[v])
    for b in range(k):
        root={u:model.new_bool_var(f'{prefix}root{u}_{b}') for u in nodes}
        model.add(sum(root.values())==1)
        flow={(u,v):model.new_int_var(0,n,f'{prefix}flow{u}_{v}_{b}') for u,v in undirected}
        for (u,v),f in flow.items():model.add(f<=n*x[u,b]);model.add(f<=n*x[v,b])
        for u in nodes:
            model.add(root[u]<=x[u,b])
            injection=model.new_int_var(0,n,f'{prefix}supply{u}_{b}')
            model.add(injection<=n*root[u])
            incoming=sum(f for (v,w),f in flow.items() if w==u)
            outgoing=sum(f for (v,w),f in flow.items() if v==u)
            model.add(injection+incoming-outgoing==x[u,b])
    q={}
    for a in range(k):
        for b in range(a+1,k):
            witnesses=[]
            for u,v in internal:
                w=model.new_bool_var(f'{prefix}edge{u}_{v}_{a}_{b}')
                model.add(w<=x[u,a]);model.add(w<=x[v,b]);model.add(w>=x[u,a]+x[v,b]-1)
                witnesses.append(w)
            q[a,b]=model.new_bool_var(f'{prefix}quot{a}_{b}')
            model.add_max_equality(q[a,b],witnesses)
    return c,q


def sequence(g,colors,leaves,reverse):
    g=g.copy();seq=[]
    while len(colors)>len(set(colors.values())):
        eligible=[]
        for u,v in g.edges:
            if u in leaves or v in leaves or colors[u]!=colors[v]:continue
            temp=g.copy();temp.remove_edge(u,v)
            if not nx.has_path(temp,u,v):eligible.append((u,v))
        assert eligible
        u,v=sorted(eligible,reverse=reverse)[0];keep,drop=min(u,v),max(u,v)
        seq.append([u,v]);g=nx.contracted_nodes(g,keep,drop,self_loops=False);del colors[drop]
        assert nx.is_directed_acyclic_graph(g)
    return seq,{v:c for v,c in colors.items()},g


def witness(target,ga,gb,leaves_a,leaves_b,ca,cb,reverse):
    sa,da,fa=sequence(ga,dict(ca),leaves_a,reverse)
    sb,db,fb=sequence(gb,dict(cb),leaves_b,reverse)
    inverse={c:v for v,c in db.items()};iso={v:inverse[c] for v,c in da.items()}
    iso.update({u:target['right']['leaves'][label] for label,u in target['left']['leaves'].items()})
    assert len(iso)==len(fa)==len(fb) and set(iso.values())==set(fb)
    assert {(iso[u],iso[v]) for u,v in fa.edges}==set(fb.edges)
    assert len(da)>=target['k']
    return {'left':sa,'right':sb,'iso':[list(pair) for pair in iso.items()]}


def solve(target,free_label=None):
    ga,la=graph(target['left']);gb,lb=graph(target['right'])
    assert set(target['left']['leaves'])==set(target['right']['leaves'])
    k=max(1,target['k'])
    if k>min(len(ga)-len(la),len(gb)-len(lb)):return []
    model=cp_model.CpModel()
    ca,qa=quotient_model(model,ga,la,k,'left');cb,qb=quotient_model(model,gb,lb,k,'right')
    for e in qa:model.add(qa[e]==qb[e])
    for label,u in target['left']['leaves'].items():
        v=target['right']['leaves'][label]
        model.add(ca[next(ga.predecessors(u))]==cb[next(gb.predecessors(v))])
    if free_label:
        parent=lambda label:next(ga.predecessors(target['left']['leaves'][label]))
        for side in ['A','B']:model.add(ca[parent(free_label)]!=ca[parent(f'G:{side}:x')])
    solver=cp_model.CpSolver();solver.parameters.num_search_workers=1
    status=solver.solve(model)
    if status==cp_model.INFEASIBLE:return []
    assert status in (cp_model.OPTIMAL,cp_model.FEASIBLE),solver.status_name(status)
    a={u:solver.value(v) for u,v in ca.items()};b={u:solver.value(v) for u,v in cb.items()}
    return [witness(target,ga,gb,la,lb,a,b,reverse) for reverse in [False,True]]


def valid_coloring(s,w):
    assert type(w) is list and len(w)==len(s['elements']) and all(type(v) is int and v in (0,1) for v in w)
    assert all(len({w[x] for x in clause})==2 for clause in s['sets'])


def main(path):
    cases=[(0,[]),(0,[[]]),(1,[[0]]),(2,[[0,1]]),(3,[[0,1,2]]),
           (3,[[0,1],[1,2],[0,2]]),(3,[[0,1],[1,2]]),(3,[[0,1,2],[0,1]]),
           (4,[[0,1],[0,1]]),(4,[[1,3]]),(4,[[0,1,2],[1,2,3]])]
    for index,(n,sets) in enumerate(cases):
        s={'elements':list(range(n)),'sets':sets}
        truth=any(all(len({w[x] for x in c})==2 for c in sets) for w in itertools.product([0,1],repeat=n))
        target=run_candidate(path,s);ws=solve(target)
        assert bool(ws)==truth,(s,target)
        for w in ws:valid_coloring(s,run_candidate(path,{'source':s,'target_solution':w},True))
        if index==4:
            alt=solve(target,'G:X2:x');assert alt
            for w in alt:valid_coloring(s,run_candidate(path,{'source':s,'target_solution':w},True))
            ws+=alt
        print(json.dumps({'source':s,'yes':truth,'target_orders':[target['left']['n'],target['right']['n']], 'k':target['k'],'recovery_calls':len(ws),'witnesses':ws}),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',type=Path,required=True)
    main(parser.parse_args().candidate.resolve())
