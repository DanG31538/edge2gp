bl_info = {
    "name": "Edge to Grease Pencil",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Grease Pencil",
    "description": "Detect edges from background image and create Grease Pencil strokes",
    "warning": "",
    "doc_url": "",
    "category": "Grease Pencil",
}

import bpy
import os
import sys

# Add the parent directory to sys.path
parent_dir = os.path.dirname(os.path.abspath(__file__))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from scripts.main import edge_to_grease_pencil

def get_current_frame_image():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.background_images:
                        bg_image = space.background_images[0]
                        if bg_image.image:
                            # Save the current frame as a temporary image
                            temp_path = os.path.join(bpy.app.tempdir, "temp_frame.png")
                            bg_image.image.save_render(temp_path)
                            return temp_path
    return None

class GPENCIL_OT_edge_detect(bpy.types.Operator):
    bl_idname = "gpencil.edge_detect"
    bl_label = "Detect Edges to Grease Pencil"
    bl_options = {'REGISTER', 'UNDO'}

    noise: bpy.props.FloatProperty(name="Noise", default=0.1, min=0.0, max=1.0)
    variation: bpy.props.FloatProperty(name="Variation", default=0.05, min=0.0, max=1.0)

    def execute(self, context):
        frame_path = get_current_frame_image()
        if not frame_path:
            self.report({'ERROR'}, "Could not get current frame image")
            return {'CANCELLED'}

        try:
            gpencil_obj = edge_to_grease_pencil(frame_path, noise_amount=self.noise, variation_amount=self.variation)
            self.report({'INFO'}, f"Added edge strokes to Grease Pencil object: {gpencil_obj.name}")
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(GPENCIL_OT_edge_detect.bl_idname)

def register():
    bpy.utils.register_class(GPENCIL_OT_edge_detect)
    bpy.types.VIEW3D_MT_gpencil_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(GPENCIL_OT_edge_detect)
    bpy.types.VIEW3D_MT_gpencil_add.remove(menu_func)

if __name__ == "__main__":
    register()