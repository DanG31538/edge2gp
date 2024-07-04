# File: scripts/main.py

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

# File: edge2gp.py

import bpy
import os
import sys
import argparse

# Add the scripts directory to sys.path
scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.append(scripts_dir)

from scripts.main import edge_to_grease_pencil

def get_current_frame_image():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    if space.background_images:
                        bg_image = space.background_images[0]
                        if bg_image.image:
                            # Save the current frame as a temporary image
                            temp_path = os.path.join(bpy.app.tempdir, "temp_frame.png")
                            bg_image.image.save_render(temp_path)
                            return temp_path
    return None

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Add edge strokes to current Grease Pencil layer")
    parser.add_argument("--noise", type=float, default=0.1, help="Amount of noise to add")
    parser.add_argument("--variation", type=float, default=0.05, help="Amount of variation from edges")
    args = parser.parse_args()

    # Get the current frame image
    frame_path = get_current_frame_image()
    if not frame_path:
        print("Error: Could not get current frame image")
        return

    # Add edge strokes to current Grease Pencil layer
    try:
        gpencil_obj = edge_to_grease_pencil(frame_path, noise_amount=args.noise, variation_amount=args.variation)
        print(f"Added edge strokes to Grease Pencil object: {gpencil_obj.name}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return

    print("Edge to Grease Pencil conversion completed for the current frame!")

if __name__ == "__main__":
    main()