import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def props(o,p):assert call('object.ObjectTools','set_properties',instance=o,values=json.dumps(p))
def run():
 root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
 old='/Engine/EngineSky/VolumetricClouds/m_SimpleVolumetricCloud_Inst'
 new='/Game/CompoundBreach/Materials/MI_IndustrialOvercast'
 assert call('asset.AssetTools','duplicate',path=old,new_path=new)
 mi=ref(new+'.MI_IndustrialOvercast')
 for n,v in [('Cloud_GlobalCoverage',.72),('Cloud_GlobalDensity',.035),('Layout_CloudGlobalScale',190),('StormClouds',0)]:
  call('material_instance.MaterialInstanceTools','set_scalar_parameter',instance=mi,name=n,value=v)
 call('material_instance.MaterialInstanceTools','set_vector_parameter',instance=mi,name='Cloud_AlbedoColor',value={'r':.68,'g':.70,'b':.74,'a':.5})
 props(ref(root+'VolumetricCloud_0.VolumetricCloudComponent'),{'material':mi,'layerBottomAltitude':.5,'layerHeight':10})
 props(ref(root+'DirectionalLight_0.LightComponent0'),{'intensity':5000,'lightSourceAngle':20,'lightSourceSoftAngle':50})
 props(ref(root+'ExponentialHeightFog_0.HeightFogComponent0'),{'fogDensity':.045,'fogHeightFalloff':.08,'fogInscatteringLuminance':{'r':.18,'g':.23,'b':.27,'a':1},'bEnableVolumetricFog':True,'volumetricFogAlbedo':{'r':.65,'g':.70,'b':.74,'a':1},'volumetricFogExtinctionScale':2,'volumetricFogDistance':10000})
 props(ref(root+'SkyLight_0.SkyLightComponent0'),{'intensity':.7,'bRealTimeCapture':True})
 pp=call('scene.SceneTools','add_to_scene_from_class',actor_type=ref('/Script/Engine.PostProcessVolume'),name='IndustrialMoodExposure',xform={})
 schema=json.loads(call('object.ObjectTools','list_properties',instance=pp))
 assert 'bUnbound' in schema and 'settings' in schema
 before=call('object.ObjectTools','get_properties',instance=pp,properties=['settings'])
 props(pp,{'bUnbound':True,'settings':{'bOverride_AutoExposureMinBrightness':True,'bOverride_AutoExposureMaxBrightness':True,'autoExposureMinBrightness':8,'autoExposureMaxBrightness':8,'bOverride_AutoExposureBias':True,'autoExposureBias':0}})
 return {'exposureBefore':before,'saved':call('asset.AssetTools','save_assets',asset_paths=[])}
