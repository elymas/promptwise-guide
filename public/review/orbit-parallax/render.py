"""Render the E11 orbit comparison: blender -b --python render.py -- OUTPUT."""
import json
import math
import sys
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

output = Path(sys.argv[sys.argv.index("--") + 1])
output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.fps = 24
scene.render.image_settings.file_format = "PNG"
scene.frame_start = 1
scene.frame_end = 96
shading = scene.display.shading
shading.light = "STUDIO"
shading.color_type = "MATERIAL"
shading.show_shadows = True
shading.show_cavity = True
shading.cavity_type = "BOTH"
shading.background_type = "WORLD"
scene.world = bpy.data.worlds.new("Courtyard sky")
scene.world.color = (0.27, 0.33, 0.35)
scene.view_settings.view_transform = "Standard"


def material(name, rgb):
    swatch = bpy.data.materials.new(name)
    swatch.diffuse_color = (*rgb, 1)
    return swatch


def box(name, center, dimensions, swatch, edge=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(swatch)
    if edge:
        bevel = obj.modifiers.new("Edge bevel", "BEVEL")
        bevel.width = edge
        bevel.segments = 2


concrete = material("Mid-grey concrete", (0.34, 0.38, 0.36))
dark = material("Back wall blue", (0.10, 0.25, 0.29))
inset = material("Blue-green window glass", (0.10, 0.34, 0.41))
metal = material("Graphite metal", (0.07, 0.12, 0.13))
teal = material("Foreground mint cue", (0.07, 0.72, 0.66))
gold = material("Distant ochre cue", (0.91, 0.63, 0.14))
jacket = material("Warm red jacket", (0.82, 0.22, 0.11))
skin = material("Stand-in head", (0.44, 0.33, 0.24))
wood = material("Planter timber", (0.25, 0.16, 0.09))
foliage = material("Potted shrubs", (0.15, 0.34, 0.22))

box("Terrace floor", (0, 3, -0.14), (23, 20, .28), concrete)
for x in range(-9, 10):
    box("Floor joint", (x, 2, 0), (.016, 18, .004), metal)
for y in range(-5, 11):
    box("Floor joint", (0, y, 0), (20, .016, .004), metal)
box("Far façade", (0, 5.95, 2.1), (18, .38, 4.2), dark)
for x in (-6, -3, 0, 3, 6):
    box("Window recess", (x, 5.73, 2.0), (2.35, .08, 1.66), metal, .04)
    for dx in (-.55, .55):
        box("Window glass", (x+dx, 5.67, 1.99), (1.0, .04, 1.46), inset, .023)
    box("Window sill", (x, 5.53, 1.15), (2.58, .34, .12), concrete)
box("Distant ochre mullion", (-.90, 5.55, 1.35), (.22, .28, 2.70), gold, .023)
for x,y in ((-2.3,2.3),(2.8,2.55),(-4.0,4.2),(4.5,4.2)):
    box("Planter", (x,y,.235), (.85,.82,.47), wood, .06)
    for dx,dz in ((-.23,0),(.18,.14),(.03,.24)):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.31,location=(x+dx,y,.61+dz))
        bpy.context.object.data.materials.append(foliage)

for z in (.31,.73):
    box("Near railing bar", (0,-1.65,z), (18,.10,.065), metal, .022)
for x in (-2.68,-1.14,1.94,3.48):
    box("Plain near railing post", (x,-1.65,.53), (.11,.13,1.06), metal, .022)
box("Mint railing post", (.4,-1.65,.52), (.14,.16,1.04), teal, .024)

box("Stand-in coat", (0,0,1.12), (.49,.28,.60), jacket, .10)
for x in (-.13,.13):
    box("Stand-in trousers", (x,0,.425), (.19,.23,.85), metal, .055)
    box("Stand-in shoe", (x,-.09,.08), (.22,.34,.16), metal, .055)
for x in (-.31,.31):
    box("Stand-in sleeve", (x,0,1.04), (.16,.24,.56), jacket, .07)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=.15,location=(0,0,1.59))
bpy.context.object.name = "Stand-in head"
bpy.context.object.data.materials.append(skin)

bpy.ops.object.camera_add()
camera = bpy.context.object
camera.data.sensor_width = 36
camera.data.sensor_fit = "HORIZONTAL"
camera.data.lens = 40
camera.rotation_mode = "QUATERNION"
scene.camera = camera
radius = 4.0
height = 1.42
target = Vector((0,0,.97))
landmarks = {
    "mint_post": Vector((.4,-1.73,.92)),
    "ochre_mullion": Vector((-.9,5.41,1.65)),
    "head_top": Vector((0,0,1.74)),
    "foot": Vector((0,0,0)),
}
audit = {}
for variant in ("A","B"):
    camera.animation_data_clear()
    samples = []
    for frame in range(1,97):
        fraction = min(1,max(0,(frame-10)/76))
        progress = fraction*fraction*(3-2*fraction)
        angle = math.radians(30*progress if variant=="B" else 0)
        camera.location = (radius*math.sin(angle), -radius*math.cos(angle), height)
        camera.rotation_quaternion = (target-camera.location).to_track_quat("-Z","Y")
        camera.keyframe_insert(data_path="location",frame=frame)
        camera.keyframe_insert(data_path="rotation_quaternion",frame=frame)
        scene.frame_set(frame)
        points = {key:world_to_camera_view(scene,camera,point) for key,point in landmarks.items()}
        samples.append({
            "frame": frame,
            "azimuth_degrees": round(math.degrees(angle),3),
            "radius_m": round(math.hypot(camera.location.x,camera.location.y),6),
            "height_m": round(camera.location.z,6),
            "near_x_px": round(points["mint_post"].x*960),
            "far_x_px": round(points["ochre_mullion"].x*960),
            "subject_height_px": round((points["head_top"].y-points["foot"].y)*540,2),
        })
    audit[variant] = {"start":samples[0],"end":samples[-1],
                      "subject_height_px_min":min(s["subject_height_px"] for s in samples),
                      "subject_height_px_max":max(s["subject_height_px"] for s in samples)}
    folder = output/variant
    folder.mkdir(exist_ok=True)
    scene.render.filepath = str(folder/"frame-")
    bpy.ops.render.render(animation=True)

(output/"geometry.json").write_text(json.dumps(
    {"frame_width":960,"frame_height":540,"fps":24,"lens_mm":40,"sensor_width_mm":36,"takes":audit},indent=2)+"\n")
