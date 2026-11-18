from pathlib import Path
import json
src='import json\ndef call(group,method,**kw):return execute_tool("editor_toolset.toolsets."+group+"."+method,json.dumps(kw)).get("returnValue")\ndef run():\n'
for name,file in [('BP_EscapePlayer','player_graph.dsl'),('BP_EscapeHUD','hud_graph.dsl')]:
    args={'graph':{'refPath':f'/Game/CompoundBreach/Blueprints/{name}.{name}:EventGraph'},'code':Path('Scripts/'+file).read_text()}
    src+='    call("blueprint.BlueprintTools","write_graph_dsl",**'+repr(args)+')\n'
src+='    return {"saved":call("asset.AssetTools","save_assets",asset_paths=[])}\n'
Path('Scripts/compiled_graph_batch.py').write_text(src)
