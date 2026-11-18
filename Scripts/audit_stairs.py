import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def run():
 out={}
 for name in ['EastAccessRamp_','SouthAccessRamp_','Mezzanine']:
  out[name]=[]
  for a in call('scene.SceneTools','find_actors',name=name,tag='',collision_channels=[]):
   e={'actor':a,'label':call('actor.ActorTools','get_label',actor=a),'transform':call('actor.ActorTools','get_actor_transform',actor=a)}
   if name=='InteriorLight':
    e['components']=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent'))
    e['values']=call('object.ObjectTools','get_properties',instance=e['components'][0],properties=['intensity','intensityUnits','attenuationRadius','bUseInverseSquaredFalloff','castShadows'])
   out[name].append(e)
 return out

