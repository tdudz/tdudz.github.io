from pathlib import Path
import bpy

root = Path(__file__).resolve().parent
(root / "build").mkdir(exist_ok=True)
result = {
    "wm": [name for name in dir(bpy.ops.wm) if "svg" in name.lower()],
    "import_curve": [name for name in dir(bpy.ops.import_curve) if "svg" in name.lower()],
}
(root / "build" / "blender-probe.txt").write_text(repr(result))
bpy.ops.wm.quit_blender()
