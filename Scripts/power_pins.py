import json
def run():
 g={'refPath':'/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer:EventGraph'}
 return {s:execute_tool('editor_toolset.toolsets.blueprint.BlueprintTools.get_node_type_pins',json.dumps({'graph':g,'type_id':s})).get('returnValue') for s in ['Rendering|Components|Light|SetIntensity','Class|Light|GetLightComponent','Utilities|Casting|CastToPointLight']}
