import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys
import networkx as nx
import z3


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_valid(x):
    require(type(x) is dict and set(x) == {'elements', 'sets'}, 'source fields')
    require(type(x['elements']) is list and all(type(v) is int and v == i for i,v in enumerate(x['elements'])), 'explicit source elements')
    require(type(x['sets']) is list, 'source sets')
    for s in x['sets']:
        require(type(s) is list and all(type(i) is int and 0 <= i < len(x['elements']) for i in s), 'source indices')
        require(len(set(s)) == len(s), 'repeated set member')


def source_witness(x, w):
    require(type(w) is list and len(w) == len(x['elements']) and all(type(c) is int and c in (0, 1) for c in w), 'source witness')
    require(all({w[i] for i in s} == {0, 1} for s in x['sets']), 'unsplit set')


def source_solve(x):
    source_valid(x)
    c = [z3.Bool(f'x{i}') for i in range(len(x['elements']))]
    solver = z3.Solver()
    for s in x['sets']:
        solver.add(z3.Or([c[i] for i in s]), z3.Or([z3.Not(c[i]) for i in s]))
    result = solver.check()
    if result == z3.unsat:
        return None
    require(result == z3.sat, 'source solver unknown')
    w = [int(z3.is_true(solver.model().eval(v, model_completion=True))) for v in c]
    source_witness(x, w)
    return w


def network(data, binary=True):
    require(type(data) is dict and set(data) == {'n', 'edges', 'leaves'}, 'network fields')
    n = data['n']
    require(type(n) is int and n >= 3, 'network n')
    require(type(data['edges']) is list and type(data['leaves']) is dict, 'network containers')
    require(all(type(e) is list and len(e) == 2 and all(type(v) is int and 0 <= v < n for v in e) and e[0] != e[1] for e in data['edges']), 'network arcs')
    require(len(set(map(tuple, data['edges']))) == len(data['edges']), 'duplicate arcs')
    labels = data['leaves']
    require(all(type(l) is str and l and type(v) is int and 0 <= v < n for l, v in labels.items()), 'leaf encoding')
    require(len(set(labels.values())) == len(labels), 'duplicate leaf vertex')
    g = nx.DiGraph()
    g.add_nodes_from(range(n))
    g.add_edges_from(data['edges'])
    require(nx.is_directed_acyclic_graph(g), 'input cycle')
    roots = [v for v in g if g.in_degree(v) == 0]
    require(len(roots) == 1, 'root count')
    require(set(labels.values()) == {v for v in g if g.out_degree(v) == 0}, 'leaf set')
    if binary:
        require(g.out_degree(roots[0]) == 2, 'root degree')
        for v in g:
            if v in labels.values():
                require(g.in_degree(v) == 1, 'leaf degree')
            elif v != roots[0]:
                require((g.in_degree(v), g.out_degree(v)) in ((1, 2), (2, 1)), 'internal degree')
    nx.set_node_attributes(g, '', 'label')
    for label, v in labels.items():
        g.nodes[v]['label'] = label
    return g


def target_valid(x):
    require(type(x) is dict and set(x) == {'left', 'right', 'k'}, 'target fields')
    require(type(x['k']) is int and x['k'] >= 0, 'threshold')
    a, b = network(x['left']), network(x['right'])
    require(set(x['left']['leaves']) == set(x['right']['leaves']), 'different taxa')
    return a, b


def merge(g, u, v):
    require(g.has_edge(u, v) and not g.nodes[u]['label'] and not g.nodes[v]['label'], 'invalid internal contraction')
    keep, remove = min(u, v), max(u, v)
    h = nx.DiGraph()
    h.add_nodes_from((w, dict(d)) for w, d in g.nodes(data=True) if w != remove)
    for x, y in g.edges:
        x = keep if x == remove else x
        y = keep if y == remove else y
        if x != y:
            h.add_edge(x, y)
    require(nx.is_directed_acyclic_graph(h), 'cyclic contraction')
    return h


def target_witness(x, w):
    a, b = target_valid(x)
    require(type(w) is dict and set(w) == {'left', 'right', 'iso'}, 'target witness fields')
    out = []
    for side, g in [('left', a), ('right', b)]:
        require(type(w[side]) is list and len(w[side]) < len(g), 'sequence length')
        for pair in w[side]:
            require(type(pair) is list and len(pair) == 2 and all(type(i) is int for i in pair), 'contraction pair')
            g = merge(g, *pair)
        out.append(g)
    a, b = out
    require(type(w['iso']) is list and all(type(p) is list and len(p) == 2 and all(type(v) is int for v in p) for p in w['iso']), 'iso encoding')
    phi = dict(w['iso'])
    require(len(phi) == len(w['iso']) and set(phi) == set(a) and set(phi.values()) == set(b) and len(a) == len(b), 'nonbijective iso')
    require({(phi[u], phi[v]) for u, v in a.edges} == set(b.edges), 'iso arcs')
    require(all(a.nodes[u]['label'] == b.nodes[phi[u]]['label'] for u in a), 'iso labels')
    require(sum(not a.nodes[v]['label'] for v in a) >= x['k'], 'small quotient')


def bag_encoding(solver, g, k, prefix):
    vertices = sorted(v for v in g if not g.nodes[v]['label'])
    c = {v: z3.Int(f'{prefix}c{v}') for v in vertices}
    distance = {v: z3.Int(f'{prefix}d{v}') for v in vertices}
    for v in vertices:
        solver.add(c[v] >= 0, c[v] < k, distance[v] >= 0, distance[v] < len(vertices))
        earlier = z3.Or([c[u] == c[v] for u in vertices if u < v])
        neighbors = (set(g.predecessors(v)) | set(g.successors(v))) & set(vertices)
        solver.add(z3.If(earlier, z3.And(distance[v] > 0, z3.Or([z3.And(c[u] == c[v], distance[u] < distance[v]) for u in neighbors])), distance[v] == 0))
    arcs = [(u, v) for u, v in g.edges if u in c and v in c]
    for u, v in arcs:
        solver.add(c[u] <= c[v])
    for i in range(k):
        solver.add(z3.Or([c[v] == i for v in vertices]))
    q = {(i, j): z3.Or([z3.And(c[u] == i, c[v] == j) for u, v in arcs]) for i in range(k) for j in range(i+1, k)}
    parents = {g.nodes[v]['label']: c[next(g.predecessors(v))] for v in g if g.nodes[v]['label']}
    return c, q, parents


def realize(g, colors):
    history = []
    while len({colors[v] for v in colors}) < len(colors):
        choice = None
        for u, v in g.edges:
            if u not in colors or v not in colors or colors[u] != colors[v]:
                continue
            # Proposition 1: a shortcut arc is not admissible.
            h = g.copy()
            h.remove_edge(u, v)
            if not nx.has_path(h, u, v):
                choice = (u, v)
                break
        require(choice is not None, 'connected acyclic bags cannot be realized')
        u, v = choice
        g = merge(g, u, v)
        del colors[max(u, v)]
        history.append([u, v])
    keys = {('bag', colors[v]) if v in colors else ('leaf', g.nodes[v]['label']): v for v in g}
    return history, keys


def target_solve(x):
    a, b = target_valid(x)
    k = max(1, x['k'])
    if k > min(sum(not g.nodes[v]['label'] for v in g) for g in [a, b]):
        return None
    solver = z3.Solver()
    ca, qa, pa = bag_encoding(solver, a, k, 'a')
    cb, qb, pb = bag_encoding(solver, b, k, 'b')
    solver.add([qa[e] == qb[e] for e in qa])
    solver.add([pa[label] == pb[label] for label in pa])
    result = solver.check()
    if result == z3.unsat:
        return None
    require(result == z3.sat, 'target solver unknown')
    model = solver.model()
    ha, ka = realize(a, {v: model.eval(ca[v]).as_long() for v in ca})
    hb, kb = realize(b, {v: model.eval(cb[v]).as_long() for v in cb})
    w = {'left': ha, 'right': hb, 'iso': [[v, kb[key]] for key, v in ka.items()]}
    target_witness(x, w)
    return w


def data(edges, labels):
    vertices = sorted(set(itertools.chain.from_iterable(edges)))
    ids = {v: i for i, v in enumerate(vertices)}
    return {'n': len(ids), 'edges': [[ids[u], ids[v]] for u, v in edges], 'leaves': {v: ids[v] for v in labels}}


def tree(order):
    a, b, c, d = order
    return data([('r','u'),('r','v'),('u',a),('u',b),('v',c),('v',d)], 'abcd')


def regressions():
    n = data([('r','u'),('r','v'),('u','s'),('u','b'),('v','h'),('v','d'),('s','a'),('s','h'),('h','c')], 'abcd')
    return [tree('abcd'), tree('acbd'), tree('abdc'), n]


def enumeration(g, minimum):
    stack = [g]
    seen = set()
    out = []
    while stack:
        h = stack.pop()
        key = (tuple(sorted(h.nodes)), tuple(sorted(h.edges)))
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
        if sum(not h.nodes[v]['label'] for v in h) <= minimum:
            continue
        for u, v in h.edges:
            if h.nodes[u]['label'] or h.nodes[v]['label']:
                continue
            trial = nx.contracted_nodes(h, min(u,v), max(u,v), self_loops=False)
            if nx.is_directed_acyclic_graph(trial):
                stack.append(trial)
    return out


def rejected(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('bad fixture accepted')


def invoke(path, payload, extract=False):
    p = subprocess.run([sys.executable, str(path)] + (['--extract'] if extract else []), input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(p.stdout)


def candidate_case(path, source):
    source_valid(source)
    target = invoke(path, source)
    target_valid(target)
    sw, tw = source_solve(source), target_solve(target)
    require((sw is None) == (tw is None), 'decision mismatch')
    if tw is not None:
        source_witness(source, invoke(path, {'source': source, 'target_solution': tw}, True))
    return {'yes': sw is not None, 'recovery_calls': int(tw is not None)}


def self_test():
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    for row in cases:
        s = row['source']
        exhaustive = any(all({w[i] for i in a} == {0,1} for a in s['sets']) for w in itertools.product([0,1], repeat=len(s['elements'])))
        assert exhaustive == row['yes'] == (source_solve(s) is not None)
    nets = regressions()
    enum = [enumeration(network(n), 1) for n in nets]
    checks = 0
    for i, j in itertools.product(range(4), repeat=2):
        for k in [0,1,2,3,4,5,6]:
            truth = any(len(a)==len(b) and sum(not a.nodes[v]['label'] for v in a)>=k and nx.is_isomorphic(a,b,node_match=lambda x,y:x['label']==y['label']) for a in enum[i] for b in enum[j])
            target = {'left':nets[i], 'right':nets[j], 'k':k}
            assert (target_solve(target) is not None) == truth, target
            checks += 1
    assert target_solve({'left':nets[3], 'right':nets[0], 'k':3}) is None
    yes = {'left':nets[0], 'right':nets[0], 'k':3}
    valid = target_solve(yes)
    target_witness(yes, valid)
    bad = dict(valid, iso=[])
    rejected(lambda:target_witness(yes,bad))
    bad = dict(valid, left=[[nets[0]['leaves']['a'],nets[0]['leaves']['b']]])
    rejected(lambda:target_witness(yes,bad))
    rejected(lambda:source_witness({'elements':[0,1],'sets':[[0,1]]},[0,0]))
    rejected(lambda:target_valid({'invalid':True}))
    print(json.dumps({'source_cases':len(cases),'target_comparisons':checks,'network_sizes':[n['n'] for n in nets], 'enumerated_states':[len(x) for x in enum], 'z3':z3.get_version_string(), 'networkx':nx.__version__}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    elif args.candidate:
        for row in json.loads(Path(__file__).with_name('cases.json').read_text()):
            print(json.dumps(candidate_case(args.candidate.resolve(), row['source'])))
    else:
        parser.error('choose --self-test or --candidate')
