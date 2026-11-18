import json
def c(n,**k):return execute_tool('editor_toolset.toolsets.blueprint.BlueprintTools.'+n,json.dumps(k)).get('returnValue')
def run():
 g={'refPath':'/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer:EventGraph'}
 return {s:c('find_node_types',graph=g,type_id_filter=s,context_pins=[]) for s in ['SetIntensity','GetLightComponent','CastToPointLight']}

