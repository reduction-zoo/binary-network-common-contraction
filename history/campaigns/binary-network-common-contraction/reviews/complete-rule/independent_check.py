"""Independent target solver with lazy connectivity cuts; no candidate imports."""
import itertools
import json
from pathlib import Path
import subprocess
import sys

import networkx as nx
import z3

CANDIDATE = Path(__file__).parents[2] / 'work' / 'algorithm.py'


def invoke(payload, extract=False):
    command = [sys.executable, str(CANDIDATE)] + (['--extract'] if extract else [])
    return json.loads(subprocess.run(command, input=json.dumps(payload), text=True,
                                    capture_output=True, check=True).stdout)


def graph(n):
    g = nx.DiGraph()
    g.add_nodes_from(range(n['n']))
    g.add_edges_from(n['edges'])
    assert len(g.edges) == len(n['edges']) and nx.is_directed_acyclic_graph(g)
    leaves = set(n['leaves'].values())
    assert len(leaves) == len(n['leaves'])
    roots = [v for v in g if g.in_degree(v) == 0]
    assert len(roots) == 1 and g.out_degree(roots[0]) == 2
    for v in g:
        if v in leaves:
            assert (g.in_degree(v), g.out_degree(v)) == (1, 0)
        elif v != roots[0]:
            assert (g.in_degree(v), g.out_degree(v)) in [(1, 2), (2, 1)]
    assert nx.descendants(g, roots[0]) == set(g) - set(roots)
    return g


def solve(target, extra=()):
    graphs = [graph(target[side]) for side in ['left', 'right']]
    leaves = [target[s]['leaves'] for s in ['left', 'right']]
    assert set(leaves[0]) == set(leaves[1])
    internal = [set(g) - set(ls.values()) for g, ls in zip(graphs, leaves)]
    # Equal leaf-parent images are necessary in any common contraction. SCCs
    # of their combined precedence relation force further equalities.
    nodes = [(s, v) for s in range(2) for v in internal[s]]
    uf = nx.utils.UnionFind(nodes)
    for label in leaves[0]:
        uf.union(*[(s, next(graphs[s].predecessors(leaves[s][label]))) for s in range(2)])
    for _ in range(len(nodes)):
        combined = nx.DiGraph()
        combined.add_nodes_from(uf[v] for v in nodes)
        combined.add_edges_from((uf[s, u], uf[s, v]) for s in range(2)
                                for u, v in graphs[s].edges if v in internal[s])
        components = [c for c in nx.strongly_connected_components(combined) if len(c) > 1]
        if not components:
            break
        for c in components:
            uf.union(*c)
    atoms = sorted({uf[v] for v in nodes})
    variables = {a: z3.Int(f'b{i}') for i, a in enumerate(atoms)}
    b = {v: variables[uf[v]] for v in nodes}
    solver = z3.Solver()
    vals = list(variables.values())
    solver.add(*[z3.And(v >= 0, v < len(atoms)) for v in vals])
    solver.add(z3.Sum([z3.If(z3.And(*[v != old for old in vals[:i]]), 1, 0)
                      for i, v in enumerate(vals)]) >= target['k'])
    arcs = [[(b[s, u], b[s, v]) for u, v in graphs[s].edges if v in internal[s]]
            for s in range(2)]
    for s in range(2):
        for a, c in arcs[s]:
            solver.add(a <= c)
            solver.add(z3.Or(a == c, *[z3.And(a == x, c == y) for x, y in arcs[1-s]]))
    def parent(side, label):
        return b[side, next(graphs[side].predecessors(leaves[side][label]))]
    for kind, labels in extra:
        if kind == 'different':
            solver.add(z3.Distinct(*[parent(0, label) for label in labels]))
        elif kind == 'same':
            solver.add(parent(0, labels[0]) == parent(0, labels[1]))
        else:
            raise ValueError(kind)
    cuts = 0
    while True:
        status = solver.check()
        if status == z3.unsat:
            return None, {'atoms': len(atoms), 'cuts': cuts}
        assert status == z3.sat
        model = solver.model()
        assigned = {v: model.eval(x).as_long() for v, x in b.items()}
        new_cuts = []
        for s in range(2):
            for bag in set(assigned[s, v] for v in internal[s]):
                members = {v for v in internal[s] if assigned[s, v] == bag}
                components = list(nx.connected_components(graphs[s].subgraph(members).to_undirected()))
                if len(components) > 1:
                    c = components[0]
                    root = min(c)
                    other = min(members - c)
                    boundary = {w for v in c for w in set(graphs[s].predecessors(v)) |
                                set(graphs[s].successors(v)) if w in internal[s] - c}
                    new_cuts.append(z3.Or(b[s, other] != b[s, root],
                                         *[b[s, v] != b[s, root] for v in c],
                                         *[b[s, w] == b[s, root] for w in boundary]))
        if not new_cuts:
            return assigned, {'atoms': len(atoms), 'cuts': cuts}
        solver.add(*new_cuts)
        cuts += len(new_cuts)


def realize(target, assigned, reverse):
    finals = []
    sequences = []
    representatives = []
    for side, name in enumerate(['left', 'right']):
        n = target[name]
        g = graph(n)
        bag = {v: assigned[side, v] for v in g if (side, v) in assigned}
        sequence = []
        while len(bag) > len(set(bag.values())):
            for u, v in sorted(g.edges, reverse=reverse):
                if u not in bag or v not in bag or bag[u] != bag[v]:
                    continue
                keep, remove = sorted((u, v))
                h = nx.relabel_nodes(g, {remove: keep}, copy=True)
                h.remove_edges_from(nx.selfloop_edges(h))
                if nx.is_directed_acyclic_graph(h):
                    g = h
                    del bag[remove]
                    sequence.append([u, v])
                    break
            else:
                raise AssertionError('No admissible contraction realizes connected DAG quotient')
        assert len(bag) >= target['k']
        finals.append(g)
        sequences.append(sequence)
        representatives.append({('bag', a): v for v, a in bag.items()} |
                               {('leaf', label): v for label, v in n['leaves'].items()})
    assert set(representatives[0]) == set(representatives[1])
    iso = {v: representatives[1][key] for key, v in representatives[0].items()}
    assert {(iso[u], iso[v]) for u, v in finals[0].edges} == set(finals[1].edges)
    return {'left': sequences[0], 'right': sequences[1], 'iso': list(map(list, iso.items()))}


def run():
    cases = [(0, []), (3, []), (0, [[]]), (2, [[0]]),
             (3, [[0, 1], [1, 2], [0, 2]]),
             (4, [[0, 1, 2], [1, 2, 3]]),
             (12, [[0, 2, 10], [0, 2, 10], [2, 10, 11]])]
    for n, sets in cases:
        source = {'elements': list(range(n)), 'sets': sets}
        expected = any(all(len({bits[v] for v in s}) == 2 for s in sets)
                       for bits in itertools.product(range(2), repeat=n))
        target = invoke(source)
        assigned, evidence = solve(target)
        assert (assigned is not None) == expected
        for reverse in (False, True) if assigned is not None else ():
            witness = realize(target, assigned, reverse)
            colors = invoke({'source': source, 'target_solution': witness}, True)
            assert len(colors) == n and all(c in [0, 1] for c in colors)
            assert all({colors[v] for v in s} == {0, 1} for s in sets)
        print(json.dumps({'source': source, 'yes': expected, 'orders':
                          [target[s]['n'] for s in ['left', 'right']], **evidence}), flush=True)
    source = {'elements': [0, 1, 2, 3], 'sets': [[0, 1, 2, 3]]}
    target = invoke(source)
    target['k'] += 2
    assigned, evidence = solve(target, [('different', ['G:A:x', 'G:B:x', 'G:X2:x', 'G:X3:x'])])
    assert assigned is not None
    # Original candidate threshold is smaller: both are accepted witnesses.
    for reverse in (False, True):
        witness = realize(target, assigned, reverse)
        colors = invoke({'source': source, 'target_solution': witness}, True)
        assert {colors[v] for v in source['sets'][0]} == {0, 1}
    print(json.dumps({'case': 'two_free_variables_above_threshold', 'threshold': target['k'],
                      'recovery_calls': 2, **evidence}), flush=True)
    target['k'] -= 1
    assigned, evidence = solve(target, [
        ('different', ['G:A:x', 'G:B:x', 'G:X2:x', 'G:X3:x']),
        ('same', ['path:R:A:0', 'path:R:A:1'])])
    assert assigned is not None
    for reverse in (False, True):
        witness = realize(target, assigned, reverse)
        colors = invoke({'source': source, 'target_solution': witness}, True)
        assert {colors[v] for v in source['sets'][0]} == {0, 1}
    print(json.dumps({'case': 'free_variables_and_merged_path', 'threshold': target['k'],
                      'recovery_calls': 2, **evidence}), flush=True)


if __name__ == '__main__':
    run()
