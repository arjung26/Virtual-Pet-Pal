"""
Frame and UI loading script for Virtual Pet Pal.
Loads all image assets used throughout the application.
"""

import os
from PIL import Image, ImageTk
from config import FULL_HEALTH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

"""
Load_frames loads all frames for a specific action (e.g., 'Idle', 'Action') 
from the given pet's folder. Returns two lists of frames:
- right-facing frames (original)
- left-facing frames (flipped horizontally)
"""
def load_frames(folder_name, action):

    path = os.path.join(BASE_DIR, "Assets", "Pets", folder_name, action)
    right_frames, left_frames = [], []

    if not os.path.exists(path):
        print(f"[Warning] Path not found: {path}")
        return right_frames, left_frames

    # Load all PNG files sorted by filename to ensure correct frame order
    for file in sorted(os.listdir(path)):
        if file.lower().endswith(".png"):
            try:
                img = Image.open(os.path.join(path, file)).convert("RGBA")
                right_frames.append(ImageTk.PhotoImage(img))
                left_frames.append(ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)))
            except Exception as e:
                print(f"[Error] Failed to load image {file}: {e}")

    return right_frames, left_frames

"""
Load_health_frames loads health bar images representing health values from 1 to FULL_HEALTH.
Note: Sorting is not used here because filenames are numeric and loaded sequentially using a range.
Returns a list of health bar images.
"""
def load_health_frames():

    path = os.path.join(BASE_DIR, "Assets", "Health_Bar")
    health_frames = []

    if not os.path.exists(path):
        print(f"[Warning] Health bar folder not found: {path}")
        return health_frames

    # Load health images sequentially based on numeric filenames (1.png, 2.png, ...)
    for i in range(1, FULL_HEALTH + 1):
        file_path = os.path.join(path, f"{i}.png")
        if not os.path.exists(file_path):
            print(f"[Warning] Missing health image: {i}.png")
            continue
        try:
            img = Image.open(file_path)
            health_frames.append(ImageTk.PhotoImage(img))
        except Exception as e:
            print(f"[Error] Failed to load health image {i}.png: {e}")

    return health_frames

"""
Load_preview_frames loads idle and action frames for the pet preview shown in the selection popup.
Returns two lists:
- idle frames
- action frames
"""
def load_preview_frames(pet_name):

    idle_path = os.path.join(BASE_DIR, "Assets", "Pets", pet_name, "Idle")
    action_path = os.path.join(BASE_DIR, "Assets", "Pets", pet_name, "Action")

    idle_frames, action_frames = [], []

    # Load idle frames sorted by filename to maintain correct order
    if os.path.exists(idle_path):
        for file in sorted(os.listdir(idle_path)):
            if file.lower().endswith(".png"):
                try:
                    img = Image.open(os.path.join(idle_path, file)).convert("RGBA")
                    idle_frames.append(ImageTk.PhotoImage(img))
                except Exception as e:
                    print(f"[Error] Failed to load idle image {file}: {e}")
    else:
        print(f"[Warning] Idle frames path not found: {idle_path}")

    # Load action frames sorted by filename
    if os.path.exists(action_path):
        for file in sorted(os.listdir(action_path)):
            if file.lower().endswith(".png"):
                try:
                    img = Image.open(os.path.join(action_path, file)).convert("RGBA")
                    action_frames.append(ImageTk.PhotoImage(img))
                except Exception as e:
                    print(f"[Error] Failed to load action image {file}: {e}")
    else:
        print(f"[Warning] Action frames path not found: {action_path}")

    return idle_frames, action_frames
