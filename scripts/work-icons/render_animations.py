import math
import sys
from pathlib import Path

import bpy


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from render_previews import BUILD, build_logo, reset_scene, setup_studio


FRAMES = BUILD / "frames"
FRAME_COUNT = 96
FRAME_SIZE = 168
ALL_LOGOS = ("ellipsis", "selini", "mgnr", "vatic", "mschf")
LOGOS = tuple(name for name in sys.argv if name in ALL_LOGOS) or ALL_LOGOS

for logo_name in LOGOS:
    reset_scene()
    setup_studio()
    root = build_logo(logo_name)
    bpy.context.scene.render.resolution_x = FRAME_SIZE
    bpy.context.scene.render.resolution_y = FRAME_SIZE
    output = FRAMES / logo_name
    output.mkdir(parents=True, exist_ok=True)

    for frame in range(FRAME_COUNT):
        root.rotation_euler[1] = math.radians(frame * 360 / FRAME_COUNT)
        bpy.context.scene.render.filepath = str(output / f"{frame:02d}.png")
        bpy.ops.render.render(write_still=True)

    print(f"rendered {logo_name}")

(BUILD / "animations.done").write_text("ok")
bpy.ops.wm.quit_blender()
