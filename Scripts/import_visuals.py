import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def setp(o,p):assert call('object.ObjectTools','set_properties',instance=o,values=json.dumps(p))
def run():
 root='C:/Users/nabid/OneDrive/Documents/Unreal Projects/Compound_Breach/SourceAssets/Industrial/'
 for name in ['Concrete','Steel','Asphalt','Rust']:
  mat=call('material.MaterialTools','create_material',folder_path='/Game/CompoundBreach/Materials',asset_name='M_PBR_'+name)
  uv=call('material.MaterialTools','add_expression',material_or_function=mat,expression_class=ref('/Script/Engine.MaterialExpressionTextureCoordinate'))
  setp(uv,{'uTiling':8,'vTiling':8})
  for suffix,prop in [('BaseColor','MP_BaseColor'),('Normal','MP_Normal'),('Roughness','MP_Roughness'),('Metallic','MP_Metallic')]:
   tn='T_'+name+'_'+suffix
   tx=call('texture.TextureTools','import_file',folder_path='/Game/CompoundBreach/Textures',asset_name=tn,source_file=root+tn+'.png')
   setp(tx,{'sRGB':suffix=='BaseColor','compressionSettings':'TC_Normalmap' if suffix=='Normal' else ('TC_Default' if suffix=='BaseColor' else 'TC_Masks')})
   ex=call('material.MaterialTools','add_expression',material_or_function=mat,expression_class=ref('/Script/Engine.MaterialExpressionTextureSampleParameter2D'))
   setp(ex,{'parameterName':suffix,'texture':tx,'samplerType':'SAMPLERTYPE_Normal' if suffix=='Normal' else ('SAMPLERTYPE_Color' if suffix=='BaseColor' else 'SAMPLERTYPE_Masks')})
   inputs=call('material.MaterialTools','get_expression_input_names',expression=ex)
   call('material.MaterialTools','connect_expressions',from_expression=uv,from_output_name='',to_expression=ex,to_input_name='UVs')
   call('material.MaterialTools','connect_to_output',expression=ex,output_name='' if suffix in ['BaseColor','Normal'] else 'R',material_property=prop)
  call('material.MaterialTools','recompile',material_or_function=mat)
  call('material_instance.MaterialInstanceTools','set_parent',instance=ref('/Game/CompoundBreach/Materials/MI_'+name+'.MI_'+name),parent=mat)
 for name in ['IndustrialCrate','IndustrialDrum','ServerRack','Generator','Terminal','Door']:
  call('static_mesh.StaticMeshTools','import_file',folder_path='/Game/CompoundBreach/Meshes',asset_name='SM_'+name,source_file=root+'SM_'+name+'.obj')
 mat=call('material.MaterialTools','create_material',folder_path='/Game/CompoundBreach/Materials',asset_name='M_IndicatorGlow')
 ex=call('material.MaterialTools','add_expression',material_or_function=mat,expression_class=ref('/Script/Engine.MaterialExpressionVectorParameter'))
 setp(ex,{'parameterName':'GlowColor','defaultValue':{'r':.1,'g':4,'b':2,'a':1}})
 call('material.MaterialTools','connect_to_output',expression=ex,output_name='',material_property='MP_EmissiveColor')
 call('material.MaterialTools','recompile',material_or_function=mat)
 return {'saved':call('asset.AssetTools','save_assets',asset_paths=[])}
