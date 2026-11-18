import json
def call(g,n,**kw):return execute_tool('editor_toolset.toolsets.'+g+'.'+n,json.dumps(kw)).get('returnValue')
def ref(p):return {'refPath':p}
def props(o,p):assert call('object.ObjectTools','set_properties',instance=o,values=json.dumps(p))
def run():
    for name in ['IndustrialCrate','IndustrialDrum','ServerRack','Generator','Terminal','Door']:
        assert call('static_mesh.StaticMeshTools','generate_convex_collisions',mesh=ref('/Game/CompoundBreach/Meshes/SM_'+name+'.SM_'+name),hull_count=4,max_hull_verts=16,hull_precision=10000)
    for a in call('scene.SceneTools','find_actors',name='OpenIndustrialDoor',tag='',collision_channels=[]):
        for c in call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.StaticMeshComponent')):
            props(c,{'overrideMaterials':[ref('/Game/CompoundBreach/Materials/MI_Steel.MI_Steel')]})
    for a in call('scene.SceneTools','find_actors',name='InteriorLight',tag='',collision_channels=[]):
        for c in call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent')):
            props(c,{'intensity':200})
    return {'saved':call('asset.AssetTools','save_assets',asset_paths=[])}
