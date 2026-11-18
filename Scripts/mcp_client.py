import json, sys, urllib.request
URL = 'http://127.0.0.1:8000/mcp'
session = None
def rpc(method, params, request_id=1):
    global session
    headers = {'Content-Type':'application/json','Accept':'application/json, text/event-stream'}
    if session: headers['Mcp-Session-Id'] = session
    payload = {'jsonrpc':'2.0','method':method,'params':params}
    if request_id is not None: payload['id'] = request_id
    req = urllib.request.Request(URL,json.dumps(payload).encode(),headers)
    with urllib.request.urlopen(req, timeout=180) as response:
        session = response.headers.get('Mcp-Session-Id',session)
        data = response.read().decode()
    if not data: return {}
    if data.startswith('event:') or data.startswith('data:'):
        data = next(line[5:].strip() for line in data.splitlines() if line.startswith('data:'))
    result = json.loads(data)
    if 'error' in result: raise RuntimeError(result['error'])
    return result.get('result',result)
def connect():
    rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'Codex','version':'1'}})
    rpc('notifications/initialized',{},None)
def tool(name, arguments): return rpc('tools/call',{'name':name,'arguments':arguments})
if __name__ == '__main__':
    connect()
    if len(sys.argv)>1:
        result = tool(sys.argv[1],json.loads(sys.argv[2]) if len(sys.argv)>2 else {})
        for c in result.get('content',[]):
            if c.get('type')=='text':
                try: print(json.dumps(json.loads(c['text']),indent=2))
                except ValueError: print(c['text'])
    else: print(json.dumps(rpc('tools/list',{}),indent=2))
