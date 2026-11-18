import json
def call(group,method,**kw):
    return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def run():
    bp=ref('/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer')
    camera=call('actor.ActorTools','add_component',owner=bp,component_type=ref('/Script/Engine.CameraComponent'),name='FirstPersonCamera')
    for name,typ in [('HasKeycard','bool'),('PowerOnline','bool'),('GateUnlocked','bool'),('Escaped','bool'),('Prompt','string'),('Objective','string'),('GateHeight','float')]:
        call('blueprint.BlueprintTools','add_variable',blueprint=bp,name=name,type_name=typ)
    call('blueprint.BlueprintTools','compile_blueprint',blueprint=bp)
    gm=call('blueprint.BlueprintTools','create',folder_path='/Game/CompoundBreach/Blueprints',asset_name='BP_EscapeGameMode',asset_type=ref('/Script/Engine.GameModeBase'))
    hud=call('blueprint.BlueprintTools','create',folder_path='/Game/CompoundBreach/Blueprints',asset_name='BP_EscapeHUD',asset_type=ref('/Script/Engine.HUD'))
    graph=call('blueprint.BlueprintTools','get_graph',blueprint=bp,graph_name='EventGraph')
    ids=['Pawn|Input|AddMovementInput','Pawn|Input|AddControllerYawInput','Pawn|Input|AddControllerPitchInput','Game|GetPlayerController','Game|Player|IsInputKeyDown','Game|Player|WasInputKeyJustPressed','Game|Player|GetInputMouseDelta','Character|Jump','Character|StopJumping','AddEvent|EventTick']
    pins={i:call('blueprint.BlueprintTools','get_node_type_pins',graph=graph,type_id=i) for i in ids}
    for search in ['GetActorForwardVector','GetActorRightVector','SetInputModeGameOnly','GetActorLocation','VectorLength','GetAllActorswithTag','SetActorLocation','SetActorHidden','OpenLevel','Variables|Default|']:
        pins[search]=call('blueprint.BlueprintTools','find_node_types',graph=graph,type_id_filter=search,context_pins=[])
    return {'camera':camera,'cameraProps':call('object.ObjectTools','list_properties',instance=camera),'playerProps':call('object.ObjectTools','list_properties',instance=bp),'gmProps':call('object.ObjectTools','list_properties',instance=gm),'pins':pins}
