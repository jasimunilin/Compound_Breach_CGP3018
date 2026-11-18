import json,math
from pathlib import Path
d=json.load(open('Saved/CodexSchemas/alignment.json'))
ops=[]
for flight in ['SouthAccessRamp','EastAccessRamp']:
 top=311.75 if flight.startswith('South') else 311
 r=top/440
 for entry in d[flight]:
  name=entry['label'];t=entry['transform'];z=t['location']['z']
  if z<0:continue
  if '_Tread' in name:t['location']['z']=(z+5)*r-5
  elif '_Nosing' in name:t['location']['z']=(z-1)*r+1
  elif '_Riser' in name:t['location']['z']=z*r;t['scale']['z']*=r
  elif '_Baluster' in name:t['location']['z']=(z-50)*r+50
  elif '_Handrail' in name:
   offset=65 if z<300 else 110;t['location']['z']=220*r+offset
   t['rotation']['pitch']=math.copysign(math.degrees(math.atan2(440*r,1012)),t['rotation']['pitch'])
   t['scale']['x']=math.hypot(1012,440*r)/100
  elif '_Stringer' in name:
   t['location']['z']=220*r;t['rotation']['pitch']=math.copysign(math.degrees(math.atan2(440*r,1012)),t['rotation']['pitch']);t['scale']['x']=math.hypot(1012,440*r)/100
  ops.append({'actor':entry['actor'],'xform':t})
src='import json\ndef run():\n    ops='+repr(ops)+'\n    for op in ops:\n        assert execute_tool("editor_toolset.toolsets.actor.ActorTools.set_actor_transform",json.dumps(op))["returnValue"]\n    return {"adjusted":len(ops),"saved":execute_tool("editor_toolset.toolsets.asset.AssetTools.save_assets",json.dumps({"asset_paths":[]}))["returnValue"]}\n'
Path('Scripts/apply_stair_fix.py').write_text(src)
