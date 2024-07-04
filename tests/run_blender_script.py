import subprocess
import sys
import os

# Use the Blender executable, not the Python executable
blender_path = r"C:\Program Files\Blender Foundation\Blender 4.1\blender.exe"
script_path = os.path.join(os.path.dirname(__file__), "test_blender.py")

# Remove the --background flag to see the Blender GUI
command = [blender_path, "--python", script_path]

print(f"Running command: {' '.join(command)}")

result = subprocess.run(command, capture_output=True, text=True)

print("STDOUT:")
print(result.stdout)

print("STDERR:")
print(result.stderr)

if result.returncode != 0:
    print(f"Script failed with return code {result.returncode}")
else:
    print("Script completed successfully")