import json
def call(group,method,**kw):return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def run():
    root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
    floor=ref(root+'Floor_0.StaticMeshComponent0')
    text=call('scene.SceneTools','add_to_scene_from_class',actor_type=ref('/Script/Engine.TextRenderActor'),name='Sign_CompoundTitle',xform={'location':{'x':0,'y':0,'z':100}})
    tc=call('actor.ActorTools','get_components',actor=text)
    sun=call('actor.ActorTools','get_components',actor=ref(root+'DirectionalLight_0'))
    player=ref('/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer')
    cdo=call('blueprint.BlueprintTools','get_default_object',blueprint=player)
    comps=call('actor.ActorTools','get_components',actor=cdo)
    return {'params':call('material_instance.MaterialInstanceTools','list_parameters',material=ref('/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial')),'floorProps':call('object.ObjectTools','list_properties',instance=floor),'textActor':text,'textComps':tc,'textProps':call('object.ObjectTools','list_properties',instance=tc[0]),'sun':sun,'playerComponents':comps}
