import json
def run():
 r=execute_tool('editor_toolset.toolsets.object.ObjectTools.list_properties',json.dumps({'instance':{'refPath':'/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.DirectionalLight_0.LightComponent0'}})).get('returnValue')
 return {k:v for k,v in json.loads(r).items() if 'cloud' in k.lower() or 'shadow' in k.lower()}
