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
    palette={'Steel':(.075,.11,.14),'Concrete':(.27,.30,.30),'Asphalt':(.055,.065,.075),'Yellow':(.95,.48,.035),'Teal':(.025,.35,.33),'Rust':(.42,.12,.045),'White':(.72,.78,.79),'Dark':(.012,.022,.028),'Green':(.06,.62,.32),'Blue':(.035,.15,.38)}
    for name,rgb in palette.items():
        m=call('material_instance.MaterialInstanceTools','create',folder_path='/Game/CompoundBreach/Materials',asset_name='MI_'+name,parent=ref('/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial'))
        call('material_instance.MaterialInstanceTools','set_vector_parameter',instance=m,name='Color',value={'r':rgb[0],'g':rgb[1],'b':rgb[2],'a':1})
        call('material_instance.MaterialInstanceTools','set_scalar_parameter',instance=m,name='Roughness',value=.72)
    root='/Game/CompoundBreach/Maps/L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
    props(ref(root+'WorldSettings_1'),{'defaultGameMode':ref('/Game/CompoundBreach/Blueprints/BP_EscapeGameMode.BP_EscapeGameMode_C')})
    for original in ['Floor_0','StaticMeshActor_0','TextRenderActor_0']:
        call('actor.ActorTools','set_actor_transform',actor=ref(root+original),xform={'location':v(0,0,-10000)})
    call('actor.ActorTools','set_actor_transform',actor=ref(root+'PlayerStart_0'),xform={'location':v(-600,-2500,555),'rotation':{'pitch':0,'yaw':90,'roll':0}})
    mesh('Compound_Foundation',(0,0,-60),(6600,7000,120),'Asphalt')
    mesh('ExitRoad',(1200,4200,-40),(1200,1800,80),'Asphalt')
    mesh('NorthSecurityWall',(0,-3400,450),(6400,80,900),'Concrete')
    mesh('WestSecurityWall',(-3200,0,450),(80,6800,900),'Concrete')
    mesh('EastSecurityWall',(3200,0,450),(80,6800,900),'Concrete')
    mesh('SouthWallWest',(-1200,3400,450),(4000,80,900),'Concrete')
    mesh('SouthWallEast',(2400,3400,450),(1600,80,900),'Concrete')
    mesh('ExitGate',(1200,3400,250),(800,70,500),'Teal',movable=True,tag='ExitGate')
    mesh('GateHeader',(1200,3400,850),(1000,160,160),'Steel')
    sign('ExitSign','EXIT / 01',(1200,3308,850),-90,75)
    # Each building has a tall courtyard entrance and a mezzanine landing.
    for letter,cx,cy,w,d,accent,face in [('A',-1800,-1200,1800,1500,'Rust',1),('B',1800,-200,1500,2000,'Yellow',-1),('C',-1800,1800,1800,1600,'Teal',1)]:
        mesh(letter+'_Floor',(cx,cy,10),(w,d,20),'Concrete')
        mesh(letter+'_Roof',(cx,cy,910),(w+100,d+100,40),'Steel')
        mesh(letter+'_Rear',(cx-face*w/2,cy,450),(40,d,900),'Concrete')
        mesh(letter+'_North',(cx,cy-d/2,450),(w,40,900),'Concrete')
        mesh(letter+'_South',(cx,cy+d/2,450),(w,40,900),'Concrete')
        entrance_y=cy if letter!='B' else -500
        lo=cy-d/2;hi=cy+d/2;gap=220
        for suffix,a,b in [('N',lo,entrance_y-gap),('S',entrance_y+gap,hi)]:
            mesh(letter+'_Front_'+suffix,(cx+face*w/2,(a+b)/2,450),(40,b-a,900),accent)
        mesh(letter+'_DoorHeader',(cx+face*w/2,entrance_y,810),(55,gap*2,180),accent)
        mesh(letter+'_Mezzanine',(cx+face*(w/2-220),cy,440),(440,d-80,20),'Steel')
        mesh(letter+'_FoundationBand',(cx,cy-d/2-24,100),(w+30,20,100),accent)
        sign(letter+'_BuildingLabel',{'A':'A / PROCESSING','B':'B / GENERATOR','C':'C / CONTROL'}[letter],(cx+face*(w/2+28),cy,820),0 if face==1 else 180,65)
    # Elevated route from the breach point to each building.
    mesh('MainCatwalk',(-600,-150,440),(260,5100,20),'Steel')
    mesh('Walkway_A',(-850,-1200,440),(500,260,20),'Steel')
    mesh('Walkway_B',(250,-500,440),(1700,260,20),'Steel')
    mesh('Walkway_C',(-850,1800,440),(500,260,20),'Steel')
    # Ramps have a 24 degree slope and connect the catwalk to ground.
    mesh('SouthAccessRamp',(-600,2895,225),(1130,260,24),'Steel',yaw=90,pitch=-24)
    mesh('EastAccessRamp',(650,-1010,225),(1130,260,24),'Steel',yaw=90,pitch=24)
    # Landmarks: three chemical tanks, raised above concrete bunds.
    for x in [200,1300,2400]:
        mesh('TankBund',(x,-2600,30),(1000,1000,60),'Concrete')
        mesh('ChemicalTank',(x,-2600,450),(760,760,800),'White','Cylinder')
        mesh('TankTop',(x,-2600,865),(790,790,35),'Teal','Cylinder')
        mesh('TankBaseBand',(x,-2600,110),(790,790,50),'Steel','Cylinder')
        sign('TankID','CHEMICAL / 0'+str(int(x/1100)+1),(x,-2180,500),90,48)
    # Objective props at coordinates used by the player Blueprint.
    mesh('SecurityDesk',(-1800,-1200,50),(180,110,100),'Steel')
    mesh('Keycard',(-1800,-1200,108),(36,22,6),'Yellow',tag='Keycard')
    sign('KeycardLabel','SECURITY ACCESS',(-1800,-1270,170),90,26)
    mesh('GeneratorBody',(2050,-200,125),(350,450,250),'Yellow')
    mesh('GeneratorConsole',(1800,-200,80),(90,120,160),'Steel')
    mesh('GeneratorButton',(1748,-200,130),(8,38,38),'Green')
    sign('GeneratorLabel','POWER / START',(1740,-200,210),180,30)
    mesh('ControlDesk',(-1800,1800,55),(200,120,110),'Steel')
    mesh('ControlMonitor',(-1800,1835,160),(140,18,90),'Dark')
    mesh('ControlScreen',(-1800,1823,160),(120,4,70),'Green')
    sign('TerminalLabel','GATE CONTROL',(-1800,1818,165),-90,19)
    sign('BreachSign','COMPOUND / BREACH<br>Find access. Restore power. Escape.',(-600,-2850,670),90,40)
    return {'saved':call('asset.AssetTools','save_assets',asset_paths=[]),'status':'Core compound built'}
