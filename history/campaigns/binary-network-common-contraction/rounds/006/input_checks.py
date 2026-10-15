import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'work'))
from check import candidate_case
fixture=root/'work/evidence/preparation/faulty_candidate.py'
for s,expected in [({'elements':[],'sets':[[]]},'decision mismatch'),({'elements':[0],'sets':[[0]]},'target fields'),({'elements':[0,1],'sets':[[0,1]]},'unsplit set')]:
 try:candidate_case(fixture,s)
 except ValueError as e:assert str(e)==expected
 else:raise AssertionError('fixture accepted')
raws=['null','[]','{}','{','{"elements":[true],"sets":[]}', '{"elements":[0],"sets":[[0,0]]}', '{"elements":[0],"sets":[['+'9'*5001+']]}']
for raw in raws:
 p=subprocess.run([sys.executable,str(root/'work/algorithm.py')],input=raw,text=True,capture_output=True,check=True)
 assert json.loads(p.stdout)=={'invalid':True}
print(json.dumps({'faulty_harness_fixtures':3,'malformed_inputs':len(raws),'largest_integer_digits':5001}))
