import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from check import tree
x = json.load(sys.stdin)
if '--extract' in sys.argv:
    print(json.dumps([0] * len(x['source']['elements'])))
elif len(x['elements']) == 1:
    print(json.dumps({'invalid': True}))
else:
    print(json.dumps({'left': tree('abcd'), 'right': tree('abcd'), 'k': 3}))
