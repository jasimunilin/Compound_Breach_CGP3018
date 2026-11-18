import json
def call(g,n,**k):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(k)).get('returnValue')
def run():
 out=[]
 for a in call('scene.SceneTools','find_actors',name='InteriorLight',tag='',collision_channels=[]):
  c=call('actor.ActorTools','get_components',actor=a,component_type={'refPath':'/Script/Engine.PointLightComponent'})[0]
  out.append({'actor':a,'transform':call('actor.ActorTools','get_actor_transform',actor=a),'values':call('object.ObjectTools','get_properties',instance=c,properties=['intensity','intensityUnits','attenuationRadius','lightColor','bVisible','bAffectsWorld','castShadows'])})
 return {'lights':out}

