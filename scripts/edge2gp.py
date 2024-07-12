import bpy
import os
import sys
import importlib

# Add the script directory to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Import other modules
import main
import blender_utils

# Ensure modules are reloaded in case of changes
importlib.reload(main)
importlib.reload(blender_utils)

def run_edge2gp():
    try:
        main.edge_to_grease_pencil()
        print("Edge2GP process completed successfully")
    except Exception as e:
        print(f"Error in Edge2GP process: {str(e)}")

# Addon Classes (for future use)
class EDGE2GP_OT_run(bpy.types.Operator):
    bl_idname = "edge2gp.run"
    bl_label = "Run Edge2GP"
    bl_description = "Run the Edge2GP process"

    def execute(self, context):
        run_edge2gp()
        return {'FINISHED'}

class EDGE2GP_PT_panel(bpy.types.Panel):
    bl_label = "Edge2GP"
    bl_idname = "EDGE2GP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Edge2GP'

    def draw(self, context):
        layout = self.layout
        layout.operator("edge2gp.run")

# Registration functions (for future addon use)
def register():
    bpy.utils.register_class(EDGE2GP_OT_run)
    bpy.utils.register_class(EDGE2GP_PT_panel)
    blender_utils.register_image_viewer()

def unregister():
    bpy.utils.unregister_class(EDGE2GP_OT_run)
    bpy.utils.unregister_class(EDGE2GP_PT_panel)
    blender_utils.unregister_image_viewer()

if __name__ == "__main__":
    # For development, just run the main function
    run_edge2gp()
    
    # Uncomment the following line to test addon functionality
    # register()