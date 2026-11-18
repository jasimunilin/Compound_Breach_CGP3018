from mcp_client import *
from pathlib import Path
import base64
connect()
if len(sys.argv)>2:
    args=json.loads(sys.argv[2])
else:args={}
args.setdefault('annotations',{'gridSpacing':0,'gridExtent':0,'gridHeight':0,'maxLabelDistance':0,'classFilter':{'refPath':'/Script/Engine.Actor'},'maxLabels':0})
args.setdefault('bShowUI',False)
r=tool('call_tool',{'toolset_name':'EditorToolset.EditorAppToolset','tool_name':'CaptureViewport','arguments':args})
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
for c in r.get('content',[]):
    if c['type']=='image':out.write_bytes(base64.b64decode(c['data']));print(str(out.resolve()))
    elif c['type']=='text':
        try:d=json.loads(c['text']).get('returnValue',{})
        except ValueError:
            print(c['text'][:500]);continue
        if isinstance(d,dict) and d.get('image',{}).get('data'):
            out.write_bytes(base64.b64decode(d['image']['data']));print(str(out.resolve()))
        else:print(c['text'][:500])
