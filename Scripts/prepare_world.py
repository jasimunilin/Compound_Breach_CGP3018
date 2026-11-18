import json
def call(group,method,**kw):
    return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def run():
    call('scene.SceneTools','load_level',level_path='/Game/CompoundBreach/Maps/L_CompoundEscape')
    bp=ref('/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer')
    camera=ref('/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer_C:FirstPersonCamera_GEN_VARIABLE')
    assert call('object.ObjectTools','set_properties',instance=camera,values=json.dumps({'relativeLocation':{'x':0,'y':0,'z':64},'bUsePawnControlRotation':True,'fieldOfView':90}))
    assert call('object.ObjectTools','set_properties',instance=bp,values=json.dumps({'bUseControllerRotationYaw':True}))
    gm=ref('/Game/CompoundBreach/Blueprints/BP_EscapeGameMode.BP_EscapeGameMode')
    assert call('object.ObjectTools','set_properties',instance=gm,values=json.dumps({'defaultPawnClass':ref('/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer_C'),'hUDClass':ref('/Game/CompoundBreach/Blueprints/BP_EscapeHUD.BP_EscapeHUD_C')}))
    graph=call('blueprint.BlueprintTools','get_graph',blueprint=bp,graph_name='EventGraph')
    ids=['Transformation|GetActorForwardVector','Transformation|GetActorRightVector','Input|SetInputModeGameOnly','Transformation|GetActorLocation','Math|Vector|VectorLength','Actor|GetAllActorswithTag','Transformation|SetActorLocation','Rendering|SetActorHiddenInGame','Game|OpenLevel(byName)','Variables|Default|SetPrompt','Variables|Default|GetPrompt','Variables|Default|SetObjective','Variables|Default|GetObjective','Variables|Default|SetHasKeycard','Variables|Default|GetHasKeycard','Variables|Default|SetPowerOnline','Variables|Default|GetPowerOnline','Variables|Default|SetGateUnlocked','Variables|Default|GetGateUnlocked','Variables|Default|GetEscaped','Variables|Default|SetEscaped','Variables|Default|SetGateHeight','Variables|Default|GetGateHeight']
    pins={i:call('blueprint.BlueprintTools','get_node_type_pins',graph=graph,type_id=i) for i in ids}
    hg=call('blueprint.BlueprintTools','get_graph',blueprint=ref('/Game/CompoundBreach/Blueprints/BP_EscapeHUD.BP_EscapeHUD'),graph_name='EventGraph')
    searches={s:call('blueprint.BlueprintTools','find_node_types',graph=hg,type_id_filter=s,context_pins=[]) for s in ['DrawText','DrawRect','ReceiveDrawHUD','EventReceiveDraw','GetPlayerCharacter','CastToBP_EscapePlayer','MakeLinearColor','MakeVector']}
    return {'pins':pins,'hudGraph':hg,'hudNodes':searches,'actors':call('scene.SceneTools','find_actors',name='',tag='',collision_channels=[])}
