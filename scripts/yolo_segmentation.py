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

def perform_yolo_segmentation(frame_pixels, confidence_threshold=0.3):
    print("Starting YOLO segmentation")
    
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
        results = model(frame_pixels, task='segment', conf=confidence_threshold)
    except Exception as e:
        print(f"Error during YOLO segmentation: {str(e)}")
        return None

    # Process segmentation results
    segmentation_mask = np.zeros(frame_pixels.shape[:2], dtype=np.uint8)
    object_data = []

    for r in results:
        for seg, box, cls, conf in zip(r.masks.xy, r.boxes.xyxy, r.boxes.cls, r.boxes.conf):
            if conf > confidence_threshold:
                # Add segmentation to mask
                cv2.fillPoly(segmentation_mask, [seg.astype(np.int32)], 255)
                
                # Store object data
                object_data.append({
                    'class': model.names[int(cls)],
                    'confidence': float(conf),
                    'bbox': box.tolist(),
                    'segmentation': seg.tolist()
                })

    print(f"Segmentation completed. Found {len(object_data)} objects.")
    return segmentation_mask, object_data

def draw_segmentation_results(image, segmentation_mask, object_data):
    result_image = image.copy()
    
    # Draw segmentation mask
    result_image = cv2.addWeighted(result_image, 1, cv2.cvtColor(segmentation_mask, cv2.COLOR_GRAY2BGR), 0.5, 0)
    
    # Draw bounding boxes and labels
    for obj in object_data:
        bbox = obj['bbox']
        cv2.rectangle(result_image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
        cv2.putText(result_image, f"{obj['class']} {obj['confidence']:.2f}", (int(bbox[0]), int(bbox[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return result_image

if __name__ == "__main__":
    # Test the function with a sample image
    import matplotlib.pyplot as plt
    
    # Load a sample image (replace with your own test image)
    sample_image = cv2.imread('sample_image.jpg')
    if sample_image is None:
        print("Failed to load sample image. Make sure 'sample_image.jpg' exists.")
    else:
        segmentation_mask, object_data = perform_yolo_segmentation(sample_image)
        if segmentation_mask is not None:
            result_image = draw_segmentation_results(sample_image, segmentation_mask, object_data)
            
            plt.figure(figsize=(15, 5))
            plt.subplot(131), plt.imshow(cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB))
            plt.title('Original Image'), plt.axis('off')
            plt.subplot(132), plt.imshow(segmentation_mask, cmap='gray')
            plt.title('Segmentation Mask'), plt.axis('off')
            plt.subplot(133), plt.imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
            plt.title('Segmentation Results'), plt.axis('off')
            plt.tight_layout()
            plt.show()
            
            print("Detected Objects:")
            for obj in object_data:
                print(f"- {obj['class']} (Confidence: {obj['confidence']:.2f})")