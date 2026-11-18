import json
def call(group,method,**kw):return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def run():
    out={}
    for name in ['BP_EscapePlayer','BP_EscapeHUD','BP_EscapeGameMode']:
        bp=ref('/Game/CompoundBreach/Blueprints/'+name+'.'+name)
        out[name]=call('blueprint.BlueprintTools','list_events',blueprint=bp)
        if name=='BP_EscapeGameMode':out['gm']=call('object.ObjectTools','get_properties',instance=bp,properties=['defaultPawnClass','hUDClass'])
    out['actors']=call('scene.SceneTools','find_actors',name='Escape',tag='',collision_channels=[])
    return out
