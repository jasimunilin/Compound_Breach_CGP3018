import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def run():
 out={}
 for name in ['Texture2D','MaterialExpressionTextureSampleParameter2D','MaterialExpressionTextureCoordinate','MaterialExpressionVectorParameter','PointLightComponent','StaticMeshComponent']:
  raw=call('object.ObjectTools','list_properties',instance=ref('/Script/Engine.'+name))
  d=json.loads(raw);out[name]={k:v for k,v in d.items() if k in ['sRGB','compressionSettings','texture','samplerType','parameterName','uTiling','vTiling','defaultValue','intensity','attenuationRadius','lightColor','staticMesh','mobility']}
 return out
