import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def run():
 out={}
 for label in ['MainCatwalk','Walkway_B','SouthAccessRamp','EastAccessRamp']:
  out[label]=[]
  for a in call('scene.SceneTools','find_actors',name=label,tag='',collision_channels=[]):
   out[label].append({'actor':a,'label':call('actor.ActorTools','get_label',actor=a),'transform':call('actor.ActorTools','get_actor_transform',actor=a)})
 for typ in ['DirectionalLight','SkyLight','VolumetricCloud','ExponentialHeightFog','PostProcessVolume']:
  out[typ]=[]
  for a in call('scene.SceneTools','find_actors',name='',tag='',collision_channels=[],actor_type=ref('/Script/Engine.'+typ)):
   comps=call('actor.ActorTools','get_components',actor=a)
   out[typ].append({'actor':a,'components':comps})
   if comps:
    d=json.loads(call('object.ObjectTools','list_properties',instance=comps[0]));out[typ][-1]['props']={k:v for k,v in d.items() if any(s in k.lower() for s in ['intensity','fog','material','altitude','height','sourceangle','softangle','realtime'])}
    out[typ][-1]['values']=call('object.ObjectTools','get_properties',instance=comps[0],properties=list(out[typ][-1]['props']))
 return out
