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
def run():
    for a in call('scene.SceneTools','find_actors',name='EastAccessRamp_',tag='',collision_channels=[]):
        t=call('actor.ActorTools','get_actor_transform',actor=a)
        t['location']['y']-=122
        call('actor.ActorTools','set_actor_transform',actor=a,xform=t)
    for a in call('scene.SceneTools','find_actors',name='CatwalkSafetyRail',tag='',collision_channels=[]):
        call('actor.ActorTools','set_actor_transform',actor=a,xform={'location':dict(call('actor.ActorTools','get_actor_transform',actor=a)['location'],z=401.75)})
    for a in call('scene.SceneTools','find_actors',name='BridgeSafetyRail',tag='',collision_channels=[]):
        t=call('actor.ActorTools','get_actor_transform',actor=a)
        if t['location']['y']<-500:t['location']['z']=-20000
        else:t['location']['z']=401
        call('actor.ActorTools','set_actor_transform',actor=a,xform=t)
    mesh('BridgeRail_StairOpeningLeft',(35,-638,401),(910,14,150),'Yellow')
    mesh('BridgeRail_StairOpeningRight',(945,-638,401),(190,14,150),'Yellow')
    root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
    props(ref(root+'DirectionalLight_0.LightComponent0'),{'intensity':1000})
    props(ref(root+'SkyLight_0.SkyLightComponent0'),{'intensity':2})
    for a in call('scene.SceneTools','find_actors',name='IndustrialMoodExposure',tag='',collision_channels=[]):
        props(a,{'settings':{'bOverride_AutoExposureMinBrightness':True,'bOverride_AutoExposureMaxBrightness':True,'autoExposureMinBrightness':6.5,'autoExposureMaxBrightness':6.5,'bOverride_AutoExposureBias':True,'autoExposureBias':0}})
    return {'saved':call('asset.AssetTools','save_assets',asset_paths=[])}

