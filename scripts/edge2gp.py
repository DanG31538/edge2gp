import bpy
import os
import sys
import importlib
import logging
import traceback

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the direct path to your edge2gp directory
EDGE2GP_DIR = r"C:\Users\DanTh\Documents\Blender\edge2gp"

# Add the scripts directory to sys.path
scripts_dir = os.path.join(EDGE2GP_DIR, 'scripts')
if os.path.exists(scripts_dir) and scripts_dir not in sys.path:
    sys.path.append(scripts_dir)
    logger.info(f"Added scripts directory to sys.path: {scripts_dir}")
else:
    logger.error(f"Scripts directory not found: {scripts_dir}")

logger.info(f"Current sys.path: {sys.path}")
logger.info(f"Current working directory: {os.getcwd()}")
if os.path.exists(scripts_dir):
    logger.info(f"Files in scripts directory: {os.listdir(scripts_dir)}")

# Import other modules
main = None
blender_utils = None

def import_modules():
    global main, blender_utils
    try:
        logger.info("Attempting to import main")
        import main
        logger.info("Successfully imported main module")
    except ImportError as e:
        logger.error(f"Error importing main module: {str(e)}")
        logger.error(traceback.format_exc())

    try:
        logger.info("Attempting to import blender_utils")
        import blender_utils
        logger.info("Successfully imported blender_utils module")
    except ImportError as e:
        logger.error(f"Error importing blender_utils module: {str(e)}")
        logger.error(traceback.format_exc())

    # Ensure modules are reloaded in case of changes
    if 'main' in sys.modules:
        importlib.reload(main)
    if 'blender_utils' in sys.modules:
        importlib.reload(blender_utils)

def run_edge2gp():
    import_modules()
    try:
        logger.info("Starting Edge2GP process")
        if main is not None:
            main.edge_to_grease_pencil()
            logger.info("Edge2GP process completed successfully")
        else:
            logger.error("Cannot run edge_to_grease_pencil: main module not imported")
    except Exception as e:
        logger.error(f"Error in Edge2GP process: {str(e)}")
        logger.error(traceback.format_exc())

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
    logger.info("Registering Edge2GP classes")
    bpy.utils.register_class(EDGE2GP_OT_run)
    bpy.utils.register_class(EDGE2GP_PT_panel)
    import_modules()
    if blender_utils is not None:
        blender_utils.register_image_viewer()

def unregister():
    logger.info("Unregistering Edge2GP classes")
    bpy.utils.unregister_class(EDGE2GP_OT_run)
    bpy.utils.unregister_class(EDGE2GP_PT_panel)
    if blender_utils is not None:
        blender_utils.unregister_image_viewer()

if __name__ == "__main__":
    logger.info("Running edge2gp.py as main")
    # For development, just run the main function
    run_edge2gp()
    
    # Uncomment the following line to test addon functionality
    # register()