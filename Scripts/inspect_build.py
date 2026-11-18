import json
def call(group,method,**kw):return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def run():
    base='/Game/CompoundBreach/Blueprints/'
    hg=ref(base+'BP_EscapeHUD.BP_EscapeHUD:EventGraph')
    pg=ref(base+'BP_EscapePlayer.BP_EscapePlayer:EventGraph')
    ids=['HUD|DrawText','HUD|DrawRect','AddEvent|EventReceiveDrawHUD','Game|GetPlayerCharacter','Utilities|Casting|CastToBP_EscapePlayer','Utilities|Struct|MakeLinearColor','Math|Vector|MakeVector']
    pins={i:call('blueprint.BlueprintTools','get_node_type_pins',graph=hg,type_id=i) for i in ids}
    for s in ['GetPrompt','GetObjective','GetHasKeycard','GetPowerOnline','GetEscaped']:
        ids=call('blueprint.BlueprintTools','find_node_types',graph=hg,type_id_filter=s,context_pins=[])
        for i in ids:pins[i]=call('blueprint.BlueprintTools','get_node_type_pins',graph=hg,type_id=i)
    world=ref('/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.WorldSettings_1')
    comps=call('actor.ActorTools','get_components',actor=ref('/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.Floor_0'))
    mat=call('material.MaterialTools','get_expressions',material_or_function=ref('/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial'))
    return {'pins':{k:{'in':[(p['name'],p['type_id'],p['value']) for p in v['input_pins']],'out':[(p['name'],p['type_id']) for p in v['output_pins']]} for k,v in pins.items()},'worldProps':call('object.ObjectTools','list_properties',instance=world),'floorComponents':comps,'material':mat}

