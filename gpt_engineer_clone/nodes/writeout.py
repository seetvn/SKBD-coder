from pathlib import Path
from ..util.fs import safe_write

def writeout_node(state, _settings,debug: bool = True):
    #TODO: tidy up debug mode
    print(f"[DEBUG] Running writeout_node with state: {state}") if debug else None
    out_dir = Path(state.get("out_dir") or "generated_project").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for draft in state.get("drafts", []):
        #TODO: refactor folder path handling
        folder_path = draft["path"].replace("`","")
        print(f"Path {folder_path} is being handled")
        if folder_path.endswith("/"):
            continue
        else:
            content = draft["content"]
            #TODO: handle other languages
            if content.startswith("```python"):
                print("Found Python code block, stripping it")
                content = content[9:-3].strip()
            safe_write(out_dir.joinpath(folder_path), content)
    return state