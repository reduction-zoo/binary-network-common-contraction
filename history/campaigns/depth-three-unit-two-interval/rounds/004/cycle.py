from itertools import product
import json
queries=0
for k in range(2,6):
    for signs in product((False,True),repeat=k):
        accepted=[]
        for y in product((False,True),repeat=k):
            b=[v==s for v,s in zip(y,signs)]
            cycle=all(not b[i] or b[(i+1)%k] for i in range(k))
            assert cycle==(len(set(b))==1)
            queries+=1
            if cycle:accepted.append(y)
        assert len(accepted)==2
print(json.dumps({'cycle_lengths':[2,3,4,5],'sign_patterns':60,'assignment_checks':queries,'passed':True}))
