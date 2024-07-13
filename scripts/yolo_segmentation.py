import cv2
import numpy as np
import torch
import os
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Path to the YOLO model file
MODEL_NAME = 'yolov8x-seg.pt'
EDGE2GP_DIR = r"C:\Users\DanTh\Documents\Blender\edge2gp"  # Update this path if necessary
MODEL_PATH = os.path.join(EDGE2GP_DIR, MODEL_NAME)

def load_yolo_model():
    logger.debug(f"Attempting to load YOLO model from: {MODEL_PATH}")
    if not os.path.exists(MODEL_PATH):
        logger.error(f"YOLO model not found at: {MODEL_PATH}")
        raise FileNotFoundError(f"YOLO model not found at: {MODEL_PATH}")
    
    logger.info(f"Loading YOLO model from: {MODEL_PATH}")
    try:
        # Load the model weights directly using PyTorch
        model = torch.load(MODEL_PATH, map_location='cpu')
        logger.info("YOLO model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading YOLO model: {str(e)}")
        raise

def perform_yolo_segmentation(frame_pixels, confidence_threshold=0.3):
    logger.info("Starting YOLO segmentation")
    
    # Ensure frame_pixels is in the correct format (uint8, BGR)
    if frame_pixels.dtype != np.uint8:
        frame_pixels = (frame_pixels * 255).astype(np.uint8)
    if frame_pixels.shape[2] == 4:  # RGBA
        frame_pixels = cv2.cvtColor(frame_pixels, cv2.COLOR_RGBA2BGR)
    elif frame_pixels.shape[2] == 3:  # RGB
        frame_pixels = cv2.cvtColor(frame_pixels, cv2.COLOR_RGB2BGR)

    # Load YOLO model
    try:
        model = load_yolo_model()
    except Exception as e:
        logger.error(f"Error loading YOLO model: {str(e)}")
        return None, None

    # Perform YOLO segmentation
    try:
        logger.debug("Performing YOLO segmentation")
        # Convert frame to tensor
        frame_tensor = torch.from_numpy(frame_pixels).float().permute(2, 0, 1).unsqueeze(0) / 255.0
        
        # Run inference
        with torch.no_grad():
            output = model(frame_tensor)
        
        # Process output to create segmentation mask and object data
        segmentation_mask = np.zeros(frame_pixels.shape[:2], dtype=np.uint8)
        object_data = []
        
        for detection in output[0]:
            if detection[4] > confidence_threshold:
                x1, y1, x2, y2 = detection[:4].int().cpu().numpy()
                cv2.rectangle(segmentation_mask, (x1, y1), (x2, y2), 255, -1)
                
                object_data.append({
                    'class': 'object',  # We don't have class names in this simplified version
                    'confidence': float(detection[4]),
                    'bbox': [x1, y1, x2, y2],
                    'segmentation': [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                })
        
        logger.debug("YOLO segmentation completed")
    except Exception as e:
        logger.error(f"Error during YOLO segmentation: {str(e)}")
        return None, None

    logger.info(f"Segmentation completed. Found {len(object_data)} objects.")
    return segmentation_mask, object_data

def draw_segmentation_results(image, segmentation_mask, object_data):
    result_image = image.copy()
    
    # Draw segmentation mask
    result_image = cv2.addWeighted(result_image, 1, cv2.cvtColor(segmentation_mask, cv2.COLOR_GRAY2BGR), 0.5, 0)
    
    # Draw bounding boxes and labels
    for obj in object_data:
        bbox = obj['bbox']
        cv2.rectangle(result_image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
        cv2.putText(result_image, f"Object {obj['confidence']:.2f}", (int(bbox[0]), int(bbox[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return result_image

if __name__ == "__main__":
    logger.debug("YOLO segmentation module loaded")