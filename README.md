# Edge2GP: YOLO-based Object Segmentation for Blender's Grease Pencil Tracing

## Project Overview

Edge2GP is a Python-based tool that integrates YOLOv8 object segmentation with Blender's Grease Pencil to enhance its tracing functionality. This project combines computer vision, deep learning, and Blender's Python API to provide an alternative approach to edge detection and tracing in 3D animation workflows.

## Technologies Used

- Python 3.x
- Blender 4.1 Python API
- OpenCV (cv2)
- NumPy
- PyTorch
- YOLOv8
- Git & GitHub
- Git LFS

## Core Functionalities

- YOLOv8 integration for object segmentation
- Frame extraction from Blender's video sequences
- Conversion of YOLO segmentation output to Grease Pencil strokes
- Custom Blender operator and panel for user interaction

## Project Structure

```
edge2gp/
├── scripts/
│   ├── main.py                 # Main execution script
│   ├── edge2gp.py              # Blender operator and panel definitions
│   ├── yolo_edge_detection.py  # YOLO model interface for edge detection
│   ├── yolo_segmentation.py    # YOLO model interface for segmentation
│   ├── frame_extraction.py     # Video frame extraction utilities
│   ├── stroke_creation.py      # Grease Pencil stroke generation
│   ├── blender_utils.py        # Blender-specific utility functions
│   └── utils.py                # General utility functions
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/YourUsername/edge2gp.git
   ```
2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Download the YOLOv8 model file (`yolov8x-seg.pt`) and place it in the project directory.

## Usage

1. Open Blender and navigate to the scripting workspace.
2. Load `edge2gp.py` into Blender's Text Editor.
3. Execute the script to add the Edge2GP operator and panel.
4. Use the Edge2GP panel in the 3D Viewport to process the current frame and generate Grease Pencil strokes.

## Technical Implementation Details

- **YOLO Integration**: Utilizes YOLOv8 for object segmentation, providing input for edge detection.
- **Blender API Utilization**: Implements custom operators and UI elements using Blender's Python API.
- **Image Processing**: Uses OpenCV and NumPy for efficient frame manipulation and analysis.
- **Grease Pencil Interaction**: Generates and modifies Grease Pencil strokes programmatically based on YOLO output.
- **Version Control**: Implements Git workflows, including large file handling with Git LFS for the YOLO model.

## Current Limitations and Future Work

- Limited to processing single frames; future work includes multi-frame support.
- Potential for GPU acceleration to improve processing speed.
- Opportunity for developing a more comprehensive Blender add-on interface.

## Contributing

Contributions are welcome. Please submit pull requests for any enhancements, bug fixes, or documentation improvements.

## License

This project is open source and available under the [MIT License](LICENSE).

