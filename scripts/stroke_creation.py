import bpy
import numpy as np
import bmesh
from mathutils import Vector

def create_grease_pencil_strokes(gpencil_object, edge_image, threshold=0.5, simplify=True, simplify_factor=0.01):
    """
    Create Grease Pencil strokes from an edge image.
    
    :param gpencil_object: The Grease Pencil object to add strokes to
    :param edge_image: A Blender image containing the edge data
    :param threshold: Threshold for edge detection (0.0 to 1.0)
    :param simplify: Whether to simplify the strokes
    :param simplify_factor: Factor for stroke simplification (lower is more detailed)
    """
    print("Creating Grease Pencil strokes")

    # Ensure we're in OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Get pixel data from the edge image
    pixels = np.array(edge_image.pixels)
    width, height = edge_image.size
    pixels = pixels.reshape((height, width, 4))

    # Create a new layer for our strokes
    gp_layer = gpencil_object.data.layers.new("Edge_Layer", set_active=True)
    gp_frame = gp_layer.frames.new(bpy.context.scene.frame_current)

    # Create strokes
    for y in range(height):
        stroke = None
        for x in range(width):
            if pixels[y, x, 0] > threshold:  # Assuming edge is white on black
                if stroke is None:
                    stroke = gp_frame.strokes.new()
                    stroke.display_mode = '3DSPACE'
                    stroke.line_width = 10  # Adjust as needed
                point = stroke.points.add(1)
                point.co = Vector((x / width, 1 - y / height, 0))
            elif stroke is not None:
                stroke = None

    print(f"Created {len(gp_frame.strokes)} strokes")

    # Simplify strokes if requested
    if simplify:
        bpy.context.view_layer.objects.active = gpencil_object
        bpy.ops.object.mode_set(mode='EDIT_GPENCIL')
        bpy.ops.gpencil.select_all(action='SELECT')
        bpy.ops.gpencil.stroke_simplify(factor=simplify_factor)
        bpy.ops.object.mode_set(mode='OBJECT')
        print("Simplified strokes")

    return True

def create_grease_pencil_from_segments(gpencil_object, segmentation_mask, object_data):
    """
    Create Grease Pencil strokes from segmentation data.
    
    :param gpencil_object: The Grease Pencil object to add strokes to
    :param segmentation_mask: NumPy array of the segmentation mask
    :param object_data: List of dictionaries containing object information
    """
    print("Creating Grease Pencil strokes from segmentation data")

    # Ensure we're in OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create a new layer for our strokes
    gp_layer = gpencil_object.data.layers.new("Segmentation_Layer", set_active=True)
    gp_frame = gp_layer.frames.new(bpy.context.scene.frame_current)

    height, width = segmentation_mask.shape[:2]

    # Create strokes for each detected object
    for obj in object_data:
        stroke = gp_frame.strokes.new()
        stroke.display_mode = '3DSPACE'
        stroke.line_width = 10  # Adjust as needed

        # Convert segmentation points to Grease Pencil points
        for point in obj['segmentation']:
            gp_point = stroke.points.add(1)
            x, y = point
            gp_point.co = Vector((x / width, 1 - y / height, 0))

        # Set stroke color based on object class (you can customize this)
        stroke.material_index = hash(obj['class']) % len(gpencil_object.material_slots)

    print(f"Created {len(gp_frame.strokes)} strokes from segmentation data")

    return True

if __name__ == "__main__":
    # Test the functions (this will only work when run in Blender)
    try:
        # Create a new Grease Pencil object
        gp_data = bpy.data.grease_pencils.new("TestGP")
        gp_obj = bpy.data.objects.new("TestGP", gp_data)
        bpy.context.scene.collection.objects.link(gp_obj)

        # Create a test image
        test_image = bpy.data.images.new("TestEdgeImage", width=100, height=100)
        pixels = [1.0 if (i % 10 < 5) ^ (i // 1000 % 10 < 5) else 0.0 for i in range(100 * 100 * 4)]
        test_image.pixels[:] = pixels

        # Test create_grease_pencil_strokes
        result = create_grease_pencil_strokes(gp_obj, test_image)
        print(f"create_grease_pencil_strokes result: {result}")

        # Test create_grease_pencil_from_segments (with dummy data)
        segmentation_mask = np.zeros((100, 100), dtype=np.uint8)
        segmentation_mask[25:75, 25:75] = 255
        object_data = [{
            'class': 'test_object',
            'confidence': 0.95,
            'segmentation': [[25, 25], [75, 25], [75, 75], [25, 75]]
        }]
        result = create_grease_pencil_from_segments(gp_obj, segmentation_mask, object_data)
        print(f"create_grease_pencil_from_segments result: {result}")

    except Exception as e:
        print(f"Error in test: {str(e)}")