import bpy
import numpy as np

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

def get_frame_info():
    scene = bpy.context.scene
    return {
        'current_frame': scene.frame_current,
        'start_frame': scene.frame_start,
        'end_frame': scene.frame_end,
        'fps': scene.render.fps
    }

if __name__ == "__main__":
    # Test the function
    pixels = get_movie_frame_pixels()
    if pixels is not None:
        print(f"Frame shape: {pixels.shape}")
        print(f"Pixel value range: {pixels.min()} to {pixels.max()}")
    else:
        print("No pixels were extracted. Make sure a movie is loaded in Blender.")
    
    frame_info = get_frame_info()
    print(f"Frame info: {frame_info}")