import bpy
import numpy as np
import cv2

print("main.py is being executed")

def get_movie_frame_pixels():
    print("Attempting to get movie frame pixels")
    for image in bpy.data.images:
        if image.source == 'MOVIE':
            print(f"Found movie: {image.name}")
            frame = bpy.context.scene.frame_current
            image.update()
            print(f"Processing frame {frame} of movie {image.name}")
            
            if image.has_data:
                pixels = np.array(image.pixels[:])
                width, height = image.size
                print(f"Successfully got movie frame pixels: {width}x{height}")
                return pixels.reshape((height, width, 4))  # RGBA format
    print("Failed to get movie frame pixels")
    return None

def create_outline_stroke(edges, frame):
    # Find contours using OpenCV
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found {len(contours)} contours")

    # Create a single stroke for the outline
    stroke = frame.strokes.new()
    stroke.display_mode = '3DSPACE'
    
    all_points = []
    for contour in contours:
        # Include all contours, no minimum area threshold
        epsilon = 0.001 * cv2.arcLength(contour, True)  # Reduced epsilon for more detail
        approx = cv2.approxPolyDP(contour, epsilon, True)
        all_points.extend(approx.reshape(-1, 2))

    print(f"Total points: {len(all_points)}")

    # Add points to the stroke
    stroke.points.add(len(all_points))
    for i, point in enumerate(all_points):
        # Swap x and y, and invert y to correct orientation
        x = 1 - (point[1] / edges.shape[0])
        y = point[0] / edges.shape[1]
        stroke.points[i].co = (x, y, 0)
    
    print(f"Added stroke with {len(all_points)} points")

def edge_to_grease_pencil(gpencil, noise_amount=0.1, variation_amount=0.05):
    print("Starting edge_to_grease_pencil")
    
    # Get the current frame pixels
    frame_pixels = get_movie_frame_pixels()
    if frame_pixels is None:
        raise ValueError("Could not get movie frame pixels")
    print(f"Frame pixels shape: {frame_pixels.shape}")
    
    # Convert to grayscale
    gray = (np.dot(frame_pixels[...,:3], [0.299, 0.587, 0.114]) * 255).astype(np.uint8)
    
    # Edge detection with lower thresholds for more edges
    edges = cv2.Canny(gray, 30, 100)  # Lowered thresholds
    
    gp_layer = gpencil.data.layers.active
    if not gp_layer:
        raise ValueError("No active Grease Pencil layer")
    print(f"Using Grease Pencil object: {gpencil.name}, Layer: {gp_layer.info}")
    
    # Get or create a new frame
    current_frame = bpy.context.scene.frame_current
    frame = None
    for f in gp_layer.frames:
        if f.frame_number == current_frame:
            frame = f
            break
    
    if frame is None:
        frame = gp_layer.frames.new(current_frame)
        print(f"Created new frame at {current_frame}")
    else:
        print(f"Using existing frame at {current_frame}")
        frame.clear()
    
    # Create outline stroke
    create_outline_stroke(edges, frame)
    
    print(f"Created outline stroke for frame {current_frame}")

    # Adjust Grease Pencil object scale and rotation
    gpencil.scale = (1, 1, 1)  # Reset scale
    gpencil.rotation_euler = (0, 0, 0)  # Reset rotation

print("main.py finished loading")