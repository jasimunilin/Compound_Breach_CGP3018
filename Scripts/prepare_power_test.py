from pathlib import Path
s=Path('Scripts/test_escape.py').read_text().split('move(-1800,1600);')[0]
s+='''
def lights():
 root='/Game/CompoundBreach/Maps/UEDPIE_0_L_CompoundEscape.L_CompoundEscape:PersistentLevel.'
 names=['PointLight_'+str(i)+'.LightComponent0' for i in range(6)]+['DirectionalLight_0.LightComponent0','SkyLight_0.SkyLightComponent0']
 return [json.loads(call('editor_toolset.toolsets.object.ObjectTools','get_properties',{'instance':{'refPath':root+n},'properties':['intensity']}))['intensity'] for n in names]
before=lights();print('Before:',before,flush=True)
assert before[:6]==[750]*6
move(1600,-200);interact()
after=lights();print('After generator:',after,flush=True)
assert state()['PowerOnline'] and after[:6]==[5000]*6
assert before[6:]==after[6:]
interact();assert lights()==after
call('SlateInspectorToolset.SlateInspectorToolset','PressKey',{'key':'R'});time.sleep(2)
reset=lights();print('Restart:',reset,flush=True)
assert reset==before and not state()['PowerOnline']
print('PASS: all six indoor lights brighten; outdoor lights unchanged; repeated E stable; restart resets.')
'''
Path('Scripts/test_generator_lights.py').write_text(s)
