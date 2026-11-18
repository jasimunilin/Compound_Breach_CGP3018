from pathlib import Path
import json
p=Path('Scripts/player_graph.dsl')
s=p.read_text()
old='(if use (Variables|Default|SetPowerOnline true))'
new='''(if use
            (Variables|Default|SetPowerOnline true)
            (bind roomLights (Actor|GetAllActorswithTag :Tag "GeneratorRoomLight"))
            (for roomLight roomLights
              (bind pointLight (Utilities|Casting|CastToPointLight :Object roomLight)
                (:then
                  (Rendering|Components|Light|SetIntensity
                    :self (Class|Light|GetLightComponent :self pointLight)
                    :NewIntensity 5000.0))
                (:CastFailed))))'''
assert s.count(old)==1
p.write_text(s.replace(old,new))
helpers=Path('Scripts/build_compound.py').read_text().split('def run():')[0]
body='''def run():
    changed=[]
    for a in call('scene.SceneTools','find_actors',name='InteriorLight',tag='',collision_channels=[]):
        old=json.loads(call('object.ObjectTools','get_properties',instance=a,properties=['tags']))['tags']
        props(a,{'tags':list(dict.fromkeys(old+['GeneratorRoomLight']))})
        c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent'))[0]
        props(c,{'mobility':'Movable','intensity':750})
        changed.append(a)
'''
body+='    call("blueprint.BlueprintTools","write_graph_dsl",graph=ref("/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer:EventGraph"),code='+repr(s.replace(old,new))+')\n'
body+='    return {"lights":changed,"saved":call("asset.AssetTools","save_assets",asset_paths=[])}\n'
Path('Scripts/implement_generator_lights.py').write_text(helpers+body)
