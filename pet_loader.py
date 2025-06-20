# Frame and UI loading script for virtual pet pal

# --- Imports ---
import os
from PIL import Image, ImageTk
from config import FULL_HEALTH

# --- Constants ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# --- Load Movement Frames ---
def load_frames(folder_name, action):
    """
    Load animation frames for a specific action (e.g., Idle, Walk) from a given pet folder.
    Returns both right-facing and flipped left-facing frames.
    """
    path = os.path.join(BASE_DIR, "Assets", "Pets", folder_name, action)
    right_frames, left_frames = [], []

    if not os.path.exists(path):
        print(f"[Warning] Path not found: {path}")
        return right_frames, left_frames

    for file in sorted(os.listdir(path)):
        if file.lower().endswith(".png"):
            try:
                img = Image.open(os.path.join(path, file)).convert("RGBA")
                right_frames.append(ImageTk.PhotoImage(img))
                left_frames.append(ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)))
            except Exception as e:
                print(f"[Error] Failed to load image {file}: {e}")

    return right_frames, left_frames


# --- Load Health Bar Frames ---
def load_health_frames():
    """
    Load images representing the pet's health from 1 to FULL_HEALTH.
    """
    folder = os.path.join(BASE_DIR, "Assets", "Health_Bar")
    health_frames = []

    if not os.path.exists(folder):
        print(f"[Warning] Health bar folder not found: {folder}")
        return health_frames

    for i in range(1, FULL_HEALTH + 1):
        file_path = os.path.join(folder, f"{i}.png")
        if not os.path.exists(file_path):
            print(f"[Warning] Missing health image: {i}.png")
            continue
        try:
            img = Image.open(file_path)
            health_frames.append(ImageTk.PhotoImage(img))
        except Exception as e:
            print(f"[Error] Failed to load health image {i}.png: {e}")

    return health_frames


# --- Load Preview Frames ---
def load_preview_frames(pet_name):
    """
    Load idle and action frames for the selected pet to be shown in the selection popup.
    """
    idle_path = os.path.join(BASE_DIR, "Assets", "Pets", pet_name, "Idle")
    action_path = os.path.join(BASE_DIR, "Assets", "Pets", pet_name, "Action")

    idle_frames, action_frames = [], []

    # Load Idle Frames
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

    # Load Action Frames
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
