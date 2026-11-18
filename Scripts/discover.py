from mcp_client import *
from pathlib import Path
connect()
out=Path('Saved/CodexSchemas');out.mkdir(exist_ok=True)
names=['editor_toolset.toolsets.'+x for x in ['blueprint.BlueprintTools','scene.SceneTools','actor.ActorTools','object.ObjectTools','asset.AssetTools','material.MaterialTools','primitive.PrimitiveTools']]+['EditorToolset.EditorAppToolset']
for name in names:
    r=tool('describe_toolset',{'toolset_name':name})
    d=json.loads(r['content'][0]['text'])
    (out/(name.split('.')[-1]+'.json')).write_text(json.dumps(d,indent=2))
    print(name, [t['name'].split('.')[-1] for t in d['tools']])
r=tool('call_tool',{'toolset_name':'ToolsetRegistry.AgentSkillToolset','tool_name':'GetSkills','arguments':{'skillPaths':['/EditorToolset/Python/editor_toolset/skills/blueprint_basics_PY.BlueprintBasicsSkill','/EditorToolset/Python/editor_toolset/skills/default_outdoor_lighting_PY.DefaultOutdoorLightingSkill','/EditorToolset/Python/editor_toolset/skills/material_basics_PY.MaterialBasicsSkill','/PCGToolset/Skills/Skill_InstantLevelOperations.Skill_InstantLevelOperations_C']}})
(out/'skills.json').write_text(json.dumps(r,indent=2))
for c in r['content']: print(c.get('text',''))
r=tool('call_tool',{'toolset_name':'editor_toolset.toolsets.blueprint.BlueprintTools','tool_name':'get_graph_dsl_docs'})
for c in r['content']:
    d=json.loads(c['text']);(out/'dsl.txt').write_text(d['returnValue'],encoding='utf-8')
