import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def run():
 root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
 out={}
 for name,path in [('cloud','VolumetricCloud_0.VolumetricCloudComponent'),('fog','ExponentialHeightFog_0.HeightFogComponent0'),('sky','SkyLight_0.SkyLightComponent0')]:
  obj=ref(root+path);d=json.loads(call('object.ObjectTools','list_properties',instance=obj))
  keys=[k for k in d if any(s in k.lower() for s in ['material','altitude','height','fogdensity','foginscattering','volumetricfog','intensity','realtime'])]
  out[name]={'props':{k:d[k] for k in keys},'values':call('object.ObjectTools','get_properties',instance=obj,properties=keys)}
 return out
