from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import math
out=Path('SourceAssets/Industrial');out.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(3018)
n=512
y,x=np.mgrid[:n,:n]
for name,color,metal in [('Concrete',(107,112,109),0),('Steel',(87,99,105),.95),('Asphalt',(40,43,45),0),('Rust',(133,65,29),.15)]:
    fine=rng.random((n,n))
    low=np.array(Image.fromarray((rng.random((32,32))*255).astype('uint8')).resize((n,n),Image.Resampling.BICUBIC))/255
    height=.65*fine+.35*low
    if name=='Steel':height=.2*fine+.25*((x+y)%48<4)+.25*((x-y)%48<4)
    if name=='Concrete':height=.25*fine+.75*low
    if name=='Rust':height=.2*fine+.8*low
    albedo=np.clip(np.array(color)[None,None,:]*(.6+.8*height[:,:,None]),0,255).astype('uint8')
    dx=(np.roll(height,-1,1)-np.roll(height,1,1))*1.5
    dy=(np.roll(height,-1,0)-np.roll(height,1,0))*1.5
    norm=np.stack([-dx,-dy,np.ones_like(dx)],2);norm/=np.linalg.norm(norm,axis=2)[:,:,None]
    normal=np.clip((norm*.5+.5)*255,0,255).astype('uint8')
    rough=np.clip((.35+.35*height if name=='Steel' else .7+.25*height)*255,0,255).astype('uint8')
    metallic=np.full((n,n),int(metal*255),dtype='uint8')
    for suffix,data in [('BaseColor',albedo),('Normal',normal),('Roughness',rough),('Metallic',metallic)]:Image.fromarray(data).save(out/f'T_{name}_{suffix}.png')

class Mesh:
 def __init__(self):self.v=[];self.faces=[]
 def box(self,x,y,z,w,d,h):
  start=len(self.v)
  self.v.extend([(x+a*w/2,y+b*d/2,z+c*h/2) for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]])
  self.faces.extend([tuple(start+i for i in f) for f in [(1,4,3,2),(5,6,7,8),(1,2,6,5),(2,3,7,6),(3,4,8,7),(4,1,5,8)]])
 def cyl(self,x,y,z,r,h,segments=32):
  start=len(self.v)
  for dz in [-h/2,h/2]:
   for i in range(segments):
    a=i*math.tau/segments;self.v.append((x+r*math.cos(a),y+r*math.sin(a),z+dz))
  for i in range(segments):j=(i+1)%segments;self.faces.append((start+i+1,start+j+1,start+j+segments+1,start+i+segments+1))
  self.faces.extend([tuple(start+i+1 for i in reversed(range(segments))),tuple(start+segments+i+1 for i in range(segments))])
 def save(self,name):
  lines=['o '+name]+[f'v {a} {b} {c}' for a,b,c in self.v]
  lines+=['vt 0 0','vt 1 0','vt 1 1','vt 0 1']
  for f in self.faces:
   for i in range(1,len(f)-1):lines.append('f '+' '.join(f'{vi}/{uv}' for vi,uv in zip((f[0],f[i],f[i+1]),(1,2,3))))
  (out/(name+'.obj')).write_text('\n'.join(lines))

m=Mesh();m.box(0,0,0,160,160,160)
for a in [-72,72]:
 for b in [-72,72]:m.box(a,b,0,20,20,180)
for z in [-70,70]:
 for a in [-82,82]:m.box(a,0,z,12,180,22);m.box(0,a,z,180,12,22)
for z in [-45,-15,15,45]:m.box(0,-81,z,135,8,24)
m.save('SM_IndustrialCrate')
m=Mesh();m.cyl(0,0,0,42,125)
for z in [-62,-40,40,62]:m.cyl(0,0,z,45,7)
m.cyl(0,0,65,40,4);m.cyl(20,0,69,7,5);m.save('SM_IndustrialDrum')
for name,w,d,h in [('ServerRack',200,150,340),('Generator',350,450,250),('Terminal',200,120,110),('Door',20,180,300)]:
 m=Mesh();m.box(0,0,0,w,d,h)
 if name=='ServerRack':
  for z in range(-130,150,32):m.box(0,-d/2-5,z,w-24,10,24);m.box(60,-d/2-12,z,25,6,6)
  for x in [-w/2,w/2]:m.box(x,0,0,12,d+12,h+12)
 elif name=='Generator':
  for z in range(-70,90,18):m.box(-w/2-5,0,z,10,d-70,8)
  for x in [-130,130]:m.box(x,0,-h/2-12,30,d+40,24)
  m.cyl(100,140,h/2+60,20,120);m.cyl(100,140,h/2+125,28,14)
 elif name=='Terminal':
  m.box(0,30,85,140,20,90);m.box(0,0,59,45,40,10);m.box(0,-30,60,95,35,8)
 else:
  m.box(-14,65,0,12,14,60)
  for z in [-110,110]:m.box(-12,0,z,8,155,14)
 m.save('SM_'+name)
print('Generated 16 PBR maps and 6 detailed OBJ meshes in',out.resolve())
