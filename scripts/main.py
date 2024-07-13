import bpy
import logging
from frame_extraction import get_movie_frame_pixels, get_frame_info
from yolo_edge_detection import perform_yolo_edge_detection
from yolo_segmentation import perform_yolo_segmentation, draw_segmentation_results
from stroke_creation import create_grease_pencil_strokes, create_grease_pencil_from_segments
from blender_utils import (
    create_image_from_numpy,
    visualize_numpy_array,
    get_or_create_grease_pencil_object,
    focus_view_on_object
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def edge_to_grease_pencil():
    logger.info("Starting Edge2GP process")

    try:
        # Step 1: Extract frame pixels
        frame_pixels = get_movie_frame_pixels()
        if frame_pixels is None:
            raise ValueError("Failed to extract frame pixels")
        
        frame_info = get_frame_info()
        logger.info(f"Processing frame: {frame_info}")
        
        # Visualize frame pixels (optional)
        visualize_numpy_array(frame_pixels, "Frame Pixels")

        # Step 2: Perform YOLO edge detection
        logger.debug("About to perform YOLO edge detection")
        edge_mask = perform_yolo_edge_detection(frame_pixels)
        if edge_mask is None:
            raise ValueError("Failed to perform YOLO edge detection")
        logger.debug("YOLO edge detection completed successfully")
        
        # Visualize edge mask (optional)
        visualize_numpy_array(edge_mask, "YOLO Edge Mask")

        # Step 3: Perform YOLO segmentation
        logger.debug("About to perform YOLO segmentation")
        segmentation_mask, object_data = perform_yolo_segmentation(frame_pixels)
        if segmentation_mask is None:
            raise ValueError("Failed to perform YOLO segmentation")
        logger.debug("YOLO segmentation completed successfully")
        
        # Visualize segmentation mask (optional)
        visualize_numpy_array(segmentation_mask, "YOLO Segmentation Mask")

        # Step 4: Create Blender images from masks
        edge_image = create_image_from_numpy(edge_mask, "YOLO_Edge_Mask")
        seg_image = create_image_from_numpy(segmentation_mask, "YOLO_Segmentation_Mask")

        # Step 5: Create or get Grease Pencil object
        gp_object = get_or_create_grease_pencil_object("Edge2GP_Result")

        # Step 6: Create Grease Pencil strokes from edge detection
        success_edge = create_grease_pencil_strokes(gp_object, edge_image)
        if not success_edge:
            raise ValueError("Failed to create Grease Pencil strokes from edge detection")

        # Step 7: Create Grease Pencil strokes from segmentation
        success_seg = create_grease_pencil_from_segments(gp_object, segmentation_mask, object_data)
        if not success_seg:
            raise ValueError("Failed to create Grease Pencil strokes from segmentation")

        logger.info("Edge2GP process completed successfully")

        # Optional: Focus view on the Grease Pencil object
        focus_view_on_object(gp_object)

    except Exception as e:
        logger.error(f"Error in Edge2GP process: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        edge_to_grease_pencil()
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)