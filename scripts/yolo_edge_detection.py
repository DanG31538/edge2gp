import cv2
import numpy as np
from ultralytics import YOLO
import os

# Path to the YOLO model file
MODEL_PATH = 'yolov8x-seg.pt'

def load_yolo_model():
    if not os.path.exists(MODEL_PATH):
        print(f"Downloading YOLO model: {MODEL_PATH}")
        model = YOLO(MODEL_PATH)
    else:
        print(f"Loading YOLO model from: {MODEL_PATH}")
        model = YOLO(MODEL_PATH)
    return model

def perform_yolo_edge_detection(frame_pixels):
    print("Starting YOLO edge detection")
    
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
        print(f"Error loading YOLO model: {str(e)}")
        return None

    # Perform YOLO segmentation
    try:
        results = model(frame_pixels, task='segment')
    except Exception as e:
        print(f"Error during YOLO segmentation: {str(e)}")
        return None

    # Create edge mask
    edge_mask = np.zeros(frame_pixels.shape[:2], dtype=np.uint8)
    for r in results:
        for seg in r.masks.xy:
            cv2.polylines(edge_mask, [seg.astype(np.int32)], True, 255, 1)

    print(f"Edge detection completed. Mask shape: {edge_mask.shape}")
    return edge_mask

if __name__ == "__main__":
    # Test the function with a sample image
    import matplotlib.pyplot as plt
    
    # Load a sample image (replace with your own test image)
    sample_image = cv2.imread('sample_image.jpg')
    if sample_image is None:
        print("Failed to load sample image. Make sure 'sample_image.jpg' exists.")
    else:
        edge_mask = perform_yolo_edge_detection(sample_image)
        if edge_mask is not None:
            plt.subplot(121), plt.imshow(cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB))
            plt.title('Original Image'), plt.axis('off')
            plt.subplot(122), plt.imshow(edge_mask, cmap='gray')
            plt.title('YOLO Edge Mask'), plt.axis('off')
            plt.show()