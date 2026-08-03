import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
VECTORS = ROOT / "vectors"
PREVIEWS = BUILD / "previews"
PREVIEWS.mkdir(parents=True, exist_ok=True)


PALETTES = {
    "ellipsis": ((0.035, 0.045, 0.065, 1), 0.92, 0.16),
    "selini": ((0.72, 0.82, 0.92, 1), 0.65, 0.16),
    "mgnr": ((0.025, 0.03, 0.04, 1), 0.95, 0.14),
    "vatic-dark": ((0.075, 0.055, 0.32, 1), 0.78, 0.17),
    "vatic-light": ((0.45, 0.67, 0.86, 1), 0.52, 0.15),
    "mschf": ((1.0, 0.018, 0.0, 1), 0.52, 0.16),
    "mschf-yellow": ((1.0, 0.53, 0.0, 1), 0.4, 0.2),
}


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.curves, bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for item in list(block):
            if item.users == 0:
                block.remove(item)


def material(name):
    color, metallic, roughness = PALETTES[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.use_backface_culling = False
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    coat = shader.inputs.get("Coat Weight") or shader.inputs.get("Clearcoat")
    if coat:
        coat.default_value = 0.45
    emission = shader.inputs.get("Emission Color") or shader.inputs.get("Emission")
    if emission:
        emission.default_value = color
    emission_strength = shader.inputs.get("Emission Strength")
    if emission_strength:
        emission_strength.default_value = 0.06
    return mat


def import_mark(svg_name, mat_name):
    before = set(bpy.data.objects)
    bpy.ops.import_curve.svg(filepath=str(VECTORS / f"{svg_name}.svg"))
    objects = [obj for obj in bpy.data.objects if obj not in before and obj.type == "CURVE"]
    mat = material(mat_name)
    for obj in objects:
        curve = obj.data
        curve.dimensions = "2D"
        curve.fill_mode = "BOTH"
        curve.extrude = 0
        curve.bevel_depth = 0
        curve.resolution_u = 8
        curve.materials.clear()
        curve.materials.append(mat)
    bpy.context.view_layer.update()
    return objects


def normalize(objects, target=2.15):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.join()
    joined = bpy.context.object
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    joined.location = (0, 0, 0)
    factor = target / max(joined.dimensions.x, joined.dimensions.y)
    joined.scale *= factor
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    solidify = joined.modifiers.new("depth", "SOLIDIFY")
    solidify.thickness = 0.22
    solidify.offset = 0
    bpy.context.view_layer.objects.active = joined
    bpy.ops.object.modifier_apply(modifier=solidify.name)
    bevel = joined.modifiers.new("edge highlights", "BEVEL")
    bevel.width = 0.035
    bevel.segments = 4
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.context.view_layer.update()
    return [joined]


def parent_to_root(objects, name):
    root = bpy.data.objects.new(f"{name}-root", None)
    bpy.context.collection.objects.link(root)
    for obj in objects:
        obj.parent = root
    return root


def add_backing(root):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, -0.09))
    backing = bpy.context.object
    backing.name = "mschf-backing"
    backing.dimensions = (2.28, 2.28, 0.24)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    backing.data.materials.append(material("mschf-yellow"))
    bevel = backing.modifiers.new("soft corners", "BEVEL")
    bevel.width = 0.2
    bevel.segments = 8
    backing.parent = root


def look_at(obj, target=(0, 0, 0)):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def add_light(name, location, energy, size, color):
    bpy.ops.object.light_add(type="AREA", location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = energy
    light.data.shape = "DISK"
    light.data.size = size
    light.data.color = color
    look_at(light)


def setup_studio():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 224
    scene.render.resolution_y = 224
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True
    scene.render.image_settings.color_depth = "8"
    scene.render.image_settings.compression = 25
    scene.world.color = (0.015, 0.02, 0.03)
    scene.view_settings.look = "AgX - Medium High Contrast"

    bpy.ops.object.camera_add(location=(0, 0, 6.5))
    camera = bpy.context.object
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = 3.1
    look_at(camera)
    scene.camera = camera

    add_light("key", (4.5, -3.5, 5.5), 820, 4.0, (1.0, 0.86, 0.72))
    add_light("fill", (-4.0, 2.0, 4.0), 620, 3.5, (0.55, 0.72, 1.0))
    add_light("rim", (1.0, 5.0, 2.5), 900, 3.0, (0.72, 0.82, 1.0))


def build_logo(name):
    if name == "vatic":
        objects = import_mark("vatic-dark", "vatic-dark") + import_mark("vatic-light", "vatic-light")
        objects = normalize(objects, 2.05)
    else:
        objects = import_mark(name, name)
        objects = normalize(objects, 1.45 if name == "mschf" else 2.12)

    root = parent_to_root(objects, name)
    if name == "mschf":
        for obj in objects:
            obj.location.z = 0.16
            back = obj.copy()
            back.data = obj.data.copy()
            back.name = "mschf-logo-back"
            back.location.z = -0.34
            back.parent = root
            bpy.context.collection.objects.link(back)
        add_backing(root)
    root.rotation_euler[1] = math.radians(24)
    root.rotation_euler[0] = math.radians(-4)
    return root


if __name__ == "__main__":
    for logo_name in ("ellipsis", "selini", "mgnr", "vatic", "mschf"):
        reset_scene()
        setup_studio()
        build_logo(logo_name)
        bpy.context.scene.render.filepath = str(PREVIEWS / f"{logo_name}.png")
        bpy.ops.render.render(write_still=True)

    (BUILD / "previews.done").write_text("ok")
    bpy.ops.wm.quit_blender()
