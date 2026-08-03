import math
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from render_previews import material, reset_scene, setup_studio


OUTPUT = ROOT.parents[1] / "assets" / "favicon.png"
FONT = Path("/System/Library/Fonts/Supplemental/Georgia Bold.ttf")

reset_scene()
setup_studio()

scene = bpy.context.scene
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.camera.data.ortho_scale = 2.75
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"

root = bpy.data.objects.new("favicon-root", None)
bpy.context.collection.objects.link(root)

bpy.ops.mesh.primitive_cube_add()
backing = bpy.context.object
backing.name = "favicon-backing"
backing.dimensions = (2.35, 2.35, 0.3)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
backing.data.materials.append(material("td-purple"))
bevel = backing.modifiers.new("soft corners", "BEVEL")
bevel.width = 0.2
bevel.segments = 8
backing.parent = root

bpy.ops.object.text_add(location=(0, 0, 0.17))
letters = bpy.context.object
letters.name = "favicon-letters"
letters.data.body = "TD"
letters.data.font = bpy.data.fonts.load(str(FONT))
letters.data.align_x = "CENTER"
letters.data.align_y = "CENTER"
letters.data.extrude = 0.08
letters.data.bevel_depth = 0.018
letters.data.bevel_resolution = 4
letters.data.materials.append(material("td-cream"))
bpy.context.view_layer.update()
letters.scale *= 1.5 / letters.dimensions.x
letters.parent = root

root.rotation_euler[0] = 0
root.rotation_euler[1] = math.radians(18.75)

scene.render.filepath = str(OUTPUT)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.quit_blender()
