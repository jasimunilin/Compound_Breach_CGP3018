import json
def call(group,method,**kw):
    return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def run():
    assets=call('asset.AssetTools','find_assets',folder_path='/Engine/Maps',name='Template')
    mats=call('asset.AssetTools','find_assets',folder_path='/Engine',name='BasicShapeMaterial')
    bp=call('blueprint.BlueprintTools','create',folder_path='/Game/CompoundBreach/Blueprints',asset_name='BP_EscapePlayer',asset_type={'refPath':'/Script/Engine.Character'})
    graph=call('blueprint.BlueprintTools','get_graph',blueprint=bp,graph_name='EventGraph')
    nodes={}
    for search in ['InputAxis','Keyboard','AddMovementInput','AddController','GetControlRotation','GetForwardVector','GetRightVector','Jump','GetPlayerController','IsInputKeyDown','WasInputKeyJustPressed','GetInputMouseDelta','EventTick']:
        nodes[search]=call('blueprint.BlueprintTools','find_node_types',graph=graph,type_id_filter=search,context_pins=[])
    return {'maps':assets,'materials':mats,'bp':bp,'graph':graph,'nodes':nodes}
