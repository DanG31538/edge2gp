import bpy
import numpy as np
import bmesh
from mathutils import Vector

def create_image_from_numpy(array, name="NumpyImage"):
    """
    Create a Blender Image from a NumPy array.
    
    :param array: NumPy array (height, width) or (height, width, channels)
    :param name: Name for the new image
    :return: Blender Image object
    """
    if array.ndim == 2:
        height, width = array.shape
        channels = 1
    elif array.ndim == 3:
        height, width, channels = array.shape
    else:
        raise ValueError("Input array must be 2D or 3D")

    if name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[name])

    image = bpy.data.images.new(name, width, height, alpha=channels==4)

    # Ensure array is flattened and in the correct format
    if channels == 1:
        array = np.repeat(array.flatten(), 4)
    elif channels == 3:
        array = np.column_stack((array.reshape(-1, 3), np.ones(height*width)))
    
    image.pixels = array.flatten()
    
    return image

def visualize_numpy_array(array, name="Visualization"):
    """
    Visualize a NumPy array as an image in Blender's Image Editor.
    
    :param array: NumPy array to visualize
    :param name: Name for the visualization
    """
    image = create_image_from_numpy(array, name)
    
    # Find or create an Image Editor area
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            break
    else:
        # If no Image Editor is found, create one by splitting the 3D View
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                # Create a new context override
                override = bpy.context.copy()
                override['area'] = area
                override['region'] = area.regions[-1]  # Use the last region in the area
                
                with bpy.context.temp_override(**override):
                    bpy.ops.screen.area_split(direction='VERTICAL', factor=0.5)
                
                # The new area is the last one in the list
                area = bpy.context.screen.areas[-1]
                area.type = 'IMAGE_EDITOR'
                break

    # Set the image to the Image Editor
    area.spaces.active.image = image

def get_or_create_grease_pencil_object(name="GPObject"):
    """
    Get an existing Grease Pencil object or create a new one.
    
    :param name: Name for the Grease Pencil object
    :return: Grease Pencil object
    """
    gp_obj = bpy.data.objects.get(name)
    if gp_obj is None:
        gp_data = bpy.data.grease_pencils.new(name)
        gp_obj = bpy.data.objects.new(name, gp_data)
        bpy.context.scene.collection.objects.link(gp_obj)
    return gp_obj

def focus_view_on_object(obj):
    """
    Focus the 3D View on a specific object.
    
    :param obj: Blender object to focus on
    """
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = bpy.context.copy()
                    override['area'] = area
                    override['region'] = region
                    bpy.ops.view3d.view_selected(override)
                    break
            break

if __name__ == "__main__":
    # Test functions
    test_array = np.random.rand(100, 100)
    image = create_image_from_numpy(test_array, "TestImage")
    print(f"Created image: {image.name}")

    visualize_numpy_array(test_array, "TestVisualization")
    print("Visualized array in Image Editor")

    gp_obj = get_or_create_grease_pencil_object("TestGP")
    print(f"Got or created Grease Pencil object: {gp_obj.name}")

    focus_view_on_object(gp_obj)
    print("Focused view on Grease Pencil object")