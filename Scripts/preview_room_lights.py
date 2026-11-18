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
    changed=[]
    for a in call('scene.SceneTools','find_actors',name='InteriorLight',tag='',collision_channels=[]):
        old=json.loads(call('object.ObjectTools','get_properties',instance=a,properties=['tags']))['tags']
        props(a,{'tags':list(dict.fromkeys(old+['GeneratorRoomLight']))})
        c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent'))[0]
        props(c,{'mobility':'Movable','intensity':5000})
        changed.append(a)
    return {'saved':False,'lights':changed}


