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

def lights():
 root='/Game/CompoundBreach/Maps/UEDPIE_0_L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
 names=['PointLight_'+str(i)+'.LightComponent0' for i in range(6)]+['DirectionalLight_0.LightComponent0','SkyLight_0.SkyLightComponent0']
 return [json.loads(call('editor_toolset.toolsets.object.ObjectTools','get_properties',{'instance':{'refPath':root+n},'properties':['intensity']}))['intensity'] for n in names]
before=lights();print('Before:',before,flush=True)
assert before[:6]==[750]*6
move(1600,-200);interact()
after=lights();print('After generator:',after,flush=True)
assert state()['PowerOnline'] and after[:6]==[60000]*6
assert before[6:]==after[6:]
interact();assert lights()==after
call('SlateInspectorToolset.SlateInspectorToolset','PressKey',{'key':'R'});time.sleep(2)
reset=lights();print('Restart:',reset,flush=True)
assert reset==before and not state()['PowerOnline']
print('PASS: all six indoor lights brighten; outdoor lights unchanged; repeated E stable; restart resets.')
