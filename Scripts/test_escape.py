from mcp_client import *
import time
connect()
def call(ts,n,a={}):
 r=tool('call_tool',{'toolset_name':ts,'tool_name':n,'arguments':a})
 if r.get('isError'):raise RuntimeError(r)
 for c in r.get('content',[]):
  if c['type']=='text':
   try:return json.loads(c['text']).get('returnValue')
   except ValueError:print(c['text'])
player={'refPath':'/Game/CompoundBreach/Maps/UEDPIE_0_L_CompoundEscape.L_CompoundEscape:PersistentLevel.BP_EscapePlayer_C_0'}
def state():return json.loads(call('editor_toolset.toolsets.object.ObjectTools','get_properties',{'instance':player,'properties':['HasKeycard','PowerOnline','GateUnlocked','Escaped','Prompt','GateHeight']}))
def move(x,y,z=110):
 call('editor_toolset.toolsets.actor.ActorTools','set_actor_transform',{'actor':player,'xform':{'location':{'x':x,'y':y,'z':z}}});time.sleep(.5)
def interact():
 call('SlateInspectorToolset.SlateInspectorToolset','PressKey',{'key':'E'});time.sleep(.5)
move(-1800,1600);print('Locked terminal:',state(),flush=True)
move(-1800,-1400);interact();print('Keycard:',state(),flush=True)
move(1600,-200);interact();print('Generator:',state(),flush=True)
move(-1800,1600);interact();time.sleep(5);print('Gate:',state(),flush=True)
move(1200,3750);print('Escape:',state(),flush=True)
