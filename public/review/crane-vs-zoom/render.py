"""Render the E12 yard study with Blender 5.2.

Usage: blender -b --python-exit-code 1 --python render.py -- OUTPUT full
Use the 'stills' mode to render only the first, middle and final frames.
"""
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

output = Path(sys.argv[sys.argv.index("--") + 1])
mode = sys.argv[sys.argv.index("--") + 2]
output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.fps = 24
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGB"
scene.frame_start = 1
scene.frame_end = 96
shading = scene.display.shading
shading.light = "STUDIO"
shading.color_type = "MATERIAL"
shading.show_shadows = True
shading.show_cavity = True
shading.cavity_type = "BOTH"
shading.background_type = "WORLD"
scene.world = bpy.data.worlds.new("Yard sky")
scene.world.color = (0.20, 0.28, 0.30)
scene.view_settings.view_transform = "Standard"

def swatch(name, rgb):
    material = bpy.data.materials.new(name)
    material.diffuse_color = (*rgb, 1)
    return material

concrete = swatch("Cool concrete", (0.27, 0.33, 0.35))
cap = swatch("Wall cap", (0.51, 0.55, 0.53))
asphalt = swatch("Loading court", (0.16, 0.20, 0.20))
teal = swatch("Warehouse siding", (0.13, 0.29, 0.31))
door = swatch("Loading doors", (0.065, 0.13, 0.14))
trim = swatch("Metal framing", (0.11, 0.17, 0.18))
yellow = swatch("Safety yellow", (0.92, 0.58, 0.11))
orange = swatch("Yard workbench", (0.95, 0.27, 0.08))
wood = swatch("Crate panel", (0.53, 0.32, 0.16))
dark_wood = swatch("Crate straps", (0.32, 0.19, 0.10))
silver = swatch("Bench equipment", (0.58, 0.64, 0.61))
coat = swatch("Scale figure coat", (0.95, 0.71, 0.20))
pants = swatch("Scale figure trousers", (0.08, 0.13, 0.16))

def box(name, center, dimensions, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel:
        edge = obj.modifiers.new("Rounded edges", "BEVEL")
        edge.width = bevel
        edge.segments = 2
    return obj

box("Asphalt yard", (0, 7, -0.10), (29, 35, 0.20), asphalt)
box("Foreground retaining wall", (0, -1.6, 1.0), (20, 0.32, 2.0), concrete)
box("Foreground coping", (0, -1.6, 2.02), (20, 0.45, 0.10), cap, 0.022)
for x in range(-10, 11, 2):
    box("Wall panel seam", (x, -1.768, 1.05), (0.022, 0.014, 1.94), trim)

box("Warehouse", (0, 13.0, 2.25), (19, 4.8, 4.5), teal, 0.03)
box("Roof coping", (0, 13.0, 4.52), (19.4, 5.1, 0.12), trim)
box("Dock slab", (0, 10.4, 0.19), (19, 1.8, 0.38), concrete)
for x in (-5.2, 0, 5.2):
    box("Recessed roller door", (x, 10.55, 1.62), (4.1, 0.13, 2.65), door, 0.02)
    for index in range(10):
        box("Roller door slat", (x, 10.46, 0.47 + index * 0.24), (4.0, 0.045, 0.04), trim)
    box("Dock canopy", (x, 9.8, 3.2), (4.5, 1.6, 0.13), trim)
    box("Canopy fascia", (x, 9.0, 3.2), (4.5, 0.05, 0.13), yellow)
for x in (-8, -2.6, 2.6, 8):
    box("Dock bollard", (x, 9.17, 0.42), (0.16, 0.16, 0.84), yellow, 0.03)
for x in (-4.8, 4.8):
    box("Work lane stripe", (x, 4.85, 0.007), (0.10, 7.9, 0.014), yellow)
for y in (1.5, 8.2):
    box("Work lane cross stripe", (0, y, 0.007), (9.6, 0.10, 0.014), yellow)
for x, y, z in [(-3.5, 5.7, 0.0), (-3.6, 7.1, 0.0), (-3.5, 5.7, 0.85), (3.7, 6.5, 0.0), (3.6, 8.0, 0.0)]:
    box("Cargo crate", (x, y, z + 0.42), (1.2, 1.0, 0.84), wood, 0.032)
    for dx in (-0.40, 0.40):
        box("Crate brace", (x+dx, y-0.51, z+0.42), (0.09, 0.04, 0.84), dark_wood)
for x in (-1.02, 1.02):
    for y in (4.25, 5.12):
        box("Workbench leg", (x, y, 0.44), (0.12, 0.12, 0.88), trim, 0.02)
box("Orange workbench", (0, 4.7, 0.9), (2.5, 1.15, 0.16), orange, 0.035)
box("Orange equipment tray", (-0.50, 4.72, 1.07), (0.65, 0.50, 0.19), door, 0.035)
box("Metal case on workbench", (0.56, 4.81, 1.05), (0.65, 0.46, 0.15), silver, 0.027)
for x in (-7, 7):
    box("Light pole", (x, 4, 2.9), (0.11, 0.11, 5.8), trim)
    box("Pole fixture", (x, 4.25, 5.79), (0.34, 0.68, 0.10), cap, 0.02)
box("Stand-in torso", (1.95, 5.4, 1.12), (0.43, 0.29, 0.59), coat, 0.085)
for x in (1.82, 2.08):
    box("Stand-in leg", (x, 5.4, 0.43), (0.17, 0.20, 0.86), pants, 0.048)
for x in (1.65, 2.25):
    box("Stand-in sleeve", (x, 5.40, 1.1), (0.14, 0.24, 0.55), coat, 0.05)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.145, location=(1.95, 5.40, 1.55))
bpy.context.object.name = "Stand-in head"
bpy.context.object.data.materials.append(pants)

bpy.ops.object.camera_add()
camera = bpy.context.object
camera.name = "Camera with fixed horizontal position"
camera.rotation_mode = "QUATERNION"
camera.data.sensor_width = 36
camera.data.sensor_fit = "HORIZONTAL"
scene.camera = camera
start = Vector((0, -5.8, 1.90))
end = Vector((0, -5.8, 5.80))
start_rotation = (Vector((0, 5.0, 1.90)) - start).to_track_quat("-Z", "Y")
end_rotation = (Vector((0, 5.0, 0.40)) - end).to_track_quat("-Z", "Y")

audit = {}
for variant in ("A", "B"):
    camera.animation_data_clear()
    camera.data.animation_data_clear()
    for frame, progress in ((1, 0), (13, 0), (85, 1), (96, 1)):
        camera.location = start.lerp(end, progress if variant == "B" else 0)
        camera.rotation_quaternion = start_rotation.slerp(end_rotation, progress if variant == "B" else 0)
        camera.data.lens = 38 - (16 * progress if variant == "A" else 0)
        for prop in ("location", "rotation_quaternion"):
            camera.keyframe_insert(data_path=prop, frame=frame)
        camera.data.keyframe_insert(data_path="lens", frame=frame)
    samples = []
    top = Vector((0, 4.7, 0.98))
    for frame in range(1, 97):
        scene.frame_set(frame)
        graph = bpy.context.evaluated_depsgraph_get()
        rendered_camera = camera.evaluated_get(graph)
        origin = rendered_camera.matrix_world.translation
        direction = top - origin
        _, _, _, _, hit, _ = scene.ray_cast(graph, origin, direction.normalized(), distance=direction.length + 0.02)
        projection = world_to_camera_view(scene, rendered_camera, top)
        visible = hit is not None and hit.name == "Orange workbench"
        in_frame = 0 <= projection.x <= 1 and 0 <= projection.y <= 1 and projection.z > 0
        samples.append({
            "frame": frame,
            "time_seconds": round((frame - 1) / 24, 4),
            "height_m": round(origin.z, 4),
            "lens_mm": round(rendered_camera.data.lens, 4),
            "first_hit": hit.name if hit is not None else None,
            "workbench_center_visible": visible and in_frame,
        })
    audit[variant] = {
        "start": samples[0],
        "end": samples[-1],
        "first_workbench_center_visible": next((sample for sample in samples if sample["workbench_center_visible"]), None),
    }
    folder = output / variant
    folder.mkdir(exist_ok=True)
    if mode == "stills":
        for frame in (1, 54, 96):
            scene.frame_set(frame)
            scene.render.filepath = str(folder / f"check-{frame:04}.png")
            bpy.ops.render.render(write_still=True)
    else:
        scene.frame_set(1)
        scene.render.filepath = str(folder / "frame-")
        bpy.ops.render.render(animation=True)

(output / "geometry.json").write_text(json.dumps(audit, indent=2) + "\n")
