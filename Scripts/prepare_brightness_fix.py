from pathlib import Path
p=Path('Scripts/player_graph.dsl');s=p.read_text();assert ':NewIntensity 5000.0' in s;p.write_text(s.replace(':NewIntensity 5000.0',':NewIntensity 60000.0'))
h=Path('Scripts/build_compound.py').read_text().split('def run():')[0]
b='''def run():
    for a in call('scene.SceneTools','find_actors',name='InteriorLight',tag='',collision_channels=[]):
        c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent'))[0]
        props(c,{'intensity':750,'attenuationRadius':1800})
'''
b+='    call("blueprint.BlueprintTools","write_graph_dsl",graph=ref("/Game/CompoundBreach/Blueprints/BP_EscapePlayer.BP_EscapePlayer:EventGraph"),code='+repr(p.read_text())+')\n'
b+='    return {"saved":call("asset.AssetTools","save_assets",asset_paths=[])}\n'
Path('Scripts/fix_power_brightness.py').write_text(h+b)
p=Path('Scripts/test_generator_lights.py');p.write_text(p.read_text().replace('[5000]*6','[60000]*6'))
