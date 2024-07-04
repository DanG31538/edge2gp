import bpy
import cv2
import numpy as np
from .utils import add_noise_to_points, vary_points_from_edges

def edge_to_grease_pencil(image_path, noise_amount=0.1, variation_amount=0.05):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect edges
    edges = cv2.Canny(gray, 100, 200)
    
    # Get active Grease Pencil object and layer
    gpencil = bpy.context.active_object
    if not gpencil or gpencil.type != 'GPENCIL':
        raise ValueError("No active Grease Pencil object")
    
    gp_layer = gpencil.data.layers.active
    if not gp_layer:
        raise ValueError("No active Grease Pencil layer")
    
    # Create a new frame or get the current frame
    frame = gp_layer.frames.new(bpy.context.scene.frame_current)
    
    # Create a new stroke
    stroke = frame.strokes.new()
    stroke.display_mode = '3DSPACE'
    
    # Convert edge pixels to 3D points
    points = np.column_stack(np.where(edges > 0))
    
    # Add noise and variation
    points = add_noise_to_points(points, noise_amount)
    points = vary_points_from_edges(points, variation_amount)
    
    # Add points to the stroke
    stroke.points.add(len(points))
    for i, point in enumerate(points):
        stroke.points[i].co = (point[1], -point[0], 0)  # Negating y to match Blender's coordinate system
    
    return gpencil