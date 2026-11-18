import json
def call(group,method,**kw):return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def run():
    gm=ref('/Game/CompoundBreach/Blueprints/BP_EscapeGameMode.BP_EscapeGameMode')
    call('blueprint.BlueprintTools','compile_blueprint',blueprint=gm)
    assert call('object.ObjectTools','set_properties',instance=gm,values=json.dumps({'defaultPawnClass':ref('/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer_C'),'hUDClass':ref('/Game/CompoundBreach/Blueprints/BP_EscapeHUD.BP_EscapeHUD_C')}))
    call('blueprint.BlueprintTools','compile_blueprint',blueprint=gm)
    return {'gm':call('object.ObjectTools','get_properties',instance=gm,properties=['defaultPawnClass','hUDClass']),'saved':call('asset.AssetTools','save_assets',asset_paths=[])}
