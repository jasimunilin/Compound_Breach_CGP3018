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
    root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
    for name,cx,ystart,direction in [('SouthAccessRamp',-600,3400,-1),('EastAccessRamp',650,-1520,1)]:
        for a in call('scene.SceneTools','find_actors',name=name,tag='',collision_channels=[]):
            call('actor.ActorTools','set_actor_transform',actor=a,xform={'location':v(0,0,-20000)})
        for i in range(22):
            cy=ystart+direction*(i+.5)*46
            mesh(name+'_Tread',(cx,cy,(i+1)*20-5),(250,48,10),'Steel')
            mesh(name+'_Riser',(cx,cy+direction*20,(i+.5)*20),(250,6,20),'Steel')
            mesh(name+'_Nosing',(cx,cy-direction*21,(i+1)*20+1),(250,6,3),'Yellow')
        for side in [-1,1]:
            x=cx+side*132
            mesh(name+'_Stringer',(x,ystart+direction*506,220),(1110,14,32),'Steel',yaw=90,pitch=24*direction)
            for i in [0,5,10,15,21]:
                z=(i+1)*20;cy=ystart+direction*(i+.5)*46
                mesh(name+'_Baluster',(x,cy,z+50),(8,8,100),'Yellow')
            for z in [65,110]:
                mesh(name+'_Handrail',(x,ystart+direction*506,220+z),(1110,8,8),'Yellow',yaw=90,pitch=24*direction)
    swaps=[('ShippingCrate','IndustrialCrate'),('ChemicalDrum','IndustrialDrum'),('ServerCabinet','ServerRack'),('GeneratorBody','Generator'),('ControlDesk','Terminal')]
    swapped=[]
    for label,asset in swaps:
        for a in call('scene.SceneTools','find_actors',name=label,tag='',collision_channels=[]):
            c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.StaticMeshComponent'))[0]
            props(c,{'staticMesh':ref('/Game/CompoundBreach/Meshes/SM_'+asset+'.SM_'+asset)})
            call('actor.ActorTools','set_actor_transform',actor=a,xform={'scale':v(1,1,1)})
            swapped.append(a)
    for label in ['Keycard','GeneratorButton','ControlScreen']:
        for a in call('scene.SceneTools','find_actors',name=label,tag='',collision_channels=[]):
            cs=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.StaticMeshComponent'))
            for c in cs:props(c,{'overrideMaterials':[ref('/Game/CompoundBreach/Materials/M_IndicatorGlow.M_IndicatorGlow')]})
    for letter,x,y in [('A',-1800,-1200),('B',1800,-200),('C',-1800,1800)]:
        for offset in [-350,350]:
            a=call('scene.SceneTools','add_to_scene_from_class',actor_type=ref('/Script/Engine.PointLight'),name=letter+'_InteriorLight',xform={'location':v(x,y+offset,720)})
            c=call('actor.ActorTools','get_components',actor=a,component_type=ref('/Script/Engine.PointLightComponent'))[0]
            props(c,{'mobility':'Movable','intensity':3500,'attenuationRadius':1300,'lightColor':{'r':1,'g':.8,'b':.55,'a':1} if letter=='B' else {'r':.65,'g':.85,'b':1,'a':1}})
            mesh(letter+'_Luminaire',(x,y+offset,755),(160,30,20),'Steel')
        # Open door leaves frame the ground-level entrance without blocking the route.
        front=x+(900 if letter!='B' else -750)
        ey=y if letter!='B' else -500
        for side in [-1,1]:
            call('scene.SceneTools','add_to_scene_from_asset',asset_path='/Game/CompoundBreach/Meshes/SM_Door',name=letter+'_OpenIndustrialDoor',xform={'location':v(front,ey+side*210,150),'rotation':{'pitch':0,'yaw':side*75,'roll':0}})
    return {'replacedProps':len(swapped),'saved':call('asset.AssetTools','save_assets',asset_paths=[])}

