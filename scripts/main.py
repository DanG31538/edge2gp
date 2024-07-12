import bpy
import os
import importlib

# Import other modules
from frame_extraction import get_movie_frame_pixels
from yolo_edge_detection import perform_yolo_edge_detection
from stroke_creation import create_grease_pencil_strokes
import blender_utils

# Ensure modules are reloaded in case of changes
importlib.reload(frame_extraction)
importlib.reload(yolo_edge_detection)
importlib.reload(stroke_creation)
importlib.reload(blender_utils)

def edge_to_grease_pencil():
    print("Starting Edge2GP process")

    # Step 1: Extract frame pixels
    frame_pixels = get_movie_frame_pixels()
    if frame_pixels is None:
        raise ValueError("Failed to extract frame pixels")
    
    # Visualize frame pixels (optional)
    blender_utils.visualize_numpy_array(frame_pixels, "Frame Pixels")

    # Step 2: Perform YOLO edge detection
    edge_mask = perform_yolo_edge_detection(frame_pixels)
    if edge_mask is None:
        raise ValueError("Failed to perform YOLO edge detection")
    
    # Visualize edge mask (optional)
    blender_utils.visualize_numpy_array(edge_mask, "YOLO Edge Mask")

    # Step 3: Create Blender image from edge mask
    edge_image = blender_utils.create_image_from_numpy(edge_mask, "YOLO_Edge_Mask")
    if edge_image is None:
        raise ValueError("Failed to create Blender image from edge mask")

    # Step 4: Create or get Grease Pencil object
    gp_object = blender_utils.get_or_create_grease_pencil_object("Edge2GP_Result")

    # Step 5: Create Grease Pencil strokes
    success = create_grease_pencil_strokes(gp_object, edge_image)
    if not success:
        raise ValueError("Failed to create Grease Pencil strokes")

    print("Edge2GP process completed successfully")

    # Optional: Focus view on the Grease Pencil object
    blender_utils.focus_view_on_object(gp_object)

if __name__ == "__main__":
    try:
        edge_to_grease_pencil()
    except Exception as e:
        print(f"Error in Edge2GP process: {str(e)}")