import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    import bpy
    print("bpy imported successfully")
except ImportError as e:
    print(f"Failed to import bpy: {e}")

def main():
    print("Script execution started")
    
    # Remove default cube
    print("Removing default cube...")
    bpy.ops.object.select_all(action='DESELECT')
    if 'Cube' in bpy.data.objects:
        bpy.data.objects['Cube'].select_set(True)
        bpy.ops.object.delete()
        print("Default cube removed")
    else:
        print("No cube found to remove")

    # Add UV sphere
    print("Adding UV sphere...")
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    print("UV sphere added")
    
    # Add a subsurf modifier
    print("Adding subdivision surface modifier...")
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 2
    print("Subdivision surface modifier added")
    
    # Add a simple material
    print("Creating and applying material...")
    mat = bpy.data.materials.new(name="BlueMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.2, 0.8, 1)  # Blue color
    bpy.context.active_object.data.materials.append(mat)
    print("Material created and applied")

    print("Script execution completed successfully!")

if __name__ == "__main__":
    main()