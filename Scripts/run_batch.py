from mcp_client import *
from pathlib import Path
connect()
source=Path(sys.argv[1]).read_text(encoding='utf-8')
r=tool('call_tool',{'toolset_name':'editor_toolset.toolsets.programmatic.ProgrammaticToolset','tool_name':'execute_tool_script','arguments':{'script':source}})
for c in r.get('content',[]):
    if c.get('type')=='text':
        try:
            d=json.loads(c['text'])
            if isinstance(d.get('returnValue'),str):
                try:d=json.loads(d['returnValue'])
                except ValueError:pass
            print(json.dumps(d,indent=2,ensure_ascii=True))
        except ValueError: print(c['text'])
if r.get('isError'):sys.exit(1)
