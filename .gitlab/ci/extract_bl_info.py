import ast
import sys
import json
from pathlib import Path

INIT_FILE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("__init__.py")

with INIT_FILE.open() as f:
    tree = ast.parse(f.read())

bl_info = None
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "bl_info":
        bl_info = node.value
        break

if not isinstance(bl_info, ast.Dict):
    raise ValueError("bl_info not found or malformed")


def extract_dict(d):
    keys = [k.value for k in d.keys]  # assume all keys are Constant (str)
    values = []
    for v in d.values:
        if isinstance(v, ast.Tuple):
            values.append(tuple(elt.value for elt in v.elts))
        elif isinstance(v, ast.Constant):  # Python 3.8+
            values.append(v.value)
        else:
            values.append(None)
    return dict(zip(keys, values))


bl_dict = extract_dict(bl_info)

version = bl_dict.get("version", ())
warning = bl_dict.get("warning", "")

print(
    json.dumps({"version": ".".join(map(str, version)), "prerelease": warning == "This Addon is still in Development!"})
)
