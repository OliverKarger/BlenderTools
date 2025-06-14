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

bl_dict = dict(zip([k.s for k in bl_info.keys], bl_info.values))

version = bl_dict.get("version")
warning = bl_dict.get("warning")

version_str = ""
if isinstance(version, ast.Tuple):
    version_str = ".".join(str(n.n) for n in version.elts)

is_prerelease = (
    isinstance(warning, ast.Str)
    and warning.s == "This Addon is still in Development!"
)

print(json.dumps({
    "version": version_str,
    "prerelease": is_prerelease
}))