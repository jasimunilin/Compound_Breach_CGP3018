import json
def call(group,method,**kw):return execute_tool('editor_toolset.toolsets.'+group+'.'+method,json.dumps(kw)).get('returnValue')
def ref(s):return {'refPath':s}
def v(x,y,z):return {'x':x,'y':y,'z':z}
def props(obj,values):
    assert call('object.ObjectTools','set_properties',instance=obj,values=json.dumps(values))
def mesh(name,loc,size,mat='Steel',shape='Cube',yaw=0,pitch=0,movable=False,tag=None):
    a=call('scene.SceneTools','add_to_scene_from_asset',asset_path='/Engine/BasicShapes/'+shape,name=name,xform={'location':v(*loc),'scale':v(*[s/100 for s in size]),'rotation':{'pitch':pitch,'yaw':yaw,'roll':0}})
    c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.StaticMeshComponent'))[0]
    vals={'overrideMaterials':[ref('/Game/CompoundBreach/Materials/MI_'+mat+'.MI_'+mat)]}
    if movable:vals['mobility']='Movable'
    props(c,vals)
    if tag:props(a,{'tags':[tag]})
    return a
def sign(name,text,loc,yaw=0,size=45):
    a=call('scene.SceneTools','add_to_scene_from_class',actor_type=ref('/Script/Engine.TextRenderActor'),name=name,xform={'location':v(*loc),'rotation':{'pitch':0,'yaw':yaw,'roll':0}})
    c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.TextRenderComponent'))[0]
    props(c,{'text':text,'worldSize':size,'horizontalAlignment':'EHTA_Center','textRenderColor':{'r':0.85,'g':0.95,'b':1,'a':1}})
    return a
import math
def find(n):return call('scene.SceneTools','find_actors',name=n,tag='',collision_channels=[])
def rail(n,x1,y1,x2,y2,z):
    length=math.hypot(x2-x1,y2-y1); yaw=math.degrees(math.atan2(y2-y1,x2-x1))
    for h in [55,105]:mesh('RepairRail_'+n,( (x1+x2)/2,(y1+y2)/2,z+h),(length,6,6),'Yellow',yaw=yaw)
    count=int(math.ceil(length/180))
    for i in range(count+1):mesh('RepairPost_'+n,(x1+(x2-x1)*i/count,y1+(y2-y1)*i/count,z+51),(7,7,102),'Steel')
def run():
    for label in ['SafetyRail','BridgeRail_']:
        for a in find(label):
            t=call('actor.ActorTools','get_actor_transform',actor=a);t['location']['z']=-20000
            call('actor.ActorTools','set_actor_transform',actor=a,xform=t)
    for a,b in [(-3350,-1330),(-1070,1670),(1930,2388)]:rail('MainWest',-728,a,-728,b,311.75)
    for a,b in [(-3350,-630),(-370,2388)]:rail('MainEast',-472,a,-472,b,311.75)
    rail('NorthEnd',-728,-3350,-472,-3350,311.75)
    for cy in [-1200,1800]:
        for side in [-1,1]:rail('Branch',-900,cy+side*127,-728,cy+side*127,311)
    rail('BridgeNorth',-472,-373,1050,-373,311)
    rail('BridgeSouthLeft',-472,-627,558,-627,311)
    rail('BridgeSouthRight',822,-627,1050,-627,311)
    # Lower the ceiling lights to illuminate both the floor and access platform.
    for a in find('InteriorLight'):
        t=call('actor.ActorTools','get_actor_transform',actor=a);t['location']['z']=570
        call('actor.ActorTools','set_actor_transform',actor=a,xform=t)
        c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent'))[0]
        props(c,{'mobility':'Movable','intensityUnits':'Lumens','intensity':5000,'attenuationRadius':1150,'castShadows':True,'lightColor':{'r':220,'g':231,'b':240,'a':255}})
    for a in find('Luminaire'):
        t=call('actor.ActorTools','get_actor_transform',actor=a);t['location']['z']=610
        call('actor.ActorTools','set_actor_transform',actor=a,xform=t)
    root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
    props(ref(root+'DirectionalLight_0.LightComponent0'),{'intensity':1000,'castShadows':False})
    props(ref(root+'SkyLight_0.SkyLightComponent0'),{'intensity':1.2,'bRealTimeCapture':True})
    props(ref(root+'ExponentialHeightFog_0.HeightFogComponent0'),{'fogDensity':.065,'volumetricFogExtinctionScale':3})
    return {'saved':call('asset.AssetTools','save_assets',asset_paths=[])}

