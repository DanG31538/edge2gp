import bpy
import os
import sys
import importlib

print("Script is running")

# Add the correct directory to sys.path
script_dir = r"C:\Users\DanTh\Documents\Blender\edge2gp\scripts"
if script_dir not in sys.path:
    sys.path.append(script_dir)
    print(f"Added {script_dir} to sys.path")

print(f"Current sys.path: {sys.path}")

try:
    import main
    importlib.reload(main)  # This will reload the module even if it was previously imported
    from main import edge_to_grease_pencil
    print("Successfully imported edge_to_grease_pencil")
except ImportError as e:
    print(f"Failed to import edge_to_grease_pencil: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Content of script directory: {os.listdir(script_dir)}")

def main():
    print("Starting main function")
    
    # Get the active Grease Pencil object
    gpencil = bpy.context.active_object
    if not gpencil or gpencil.type != 'GPENCIL':
        print("Error: No active Grease Pencil object")
        return

    # Add edge strokes to current Grease Pencil layer
    try:
        edge_to_grease_pencil(gpencil, noise_amount=0.1, variation_amount=0.05)
        print(f"Added edge strokes to Grease Pencil object: {gpencil.name}")
    except Exception as e:
        print(f"Error in edge_to_grease_pencil: {str(e)}")
        import traceback
        traceback.print_exc()
        return

    print("Edge to Grease Pencil conversion completed for the current frame!")

if __name__ == "__main__":
    main()

print("Script finished")