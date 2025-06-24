"""
Pet selection popup script for Virtual Pet Pal.
Displays a popup window with a dropdown to select a pet.
Includes an animated preview of the selected pet.
Disables the Save button if necessary frames are missing.
"""

import tkinter as tk
from tkinter import messagebox
from pet_loader import load_preview_frames
from config import PET_LIST, DEFAULT_PET, PET_FRAME_WIDTH, PET_FRAME_HEIGHT

"""
Displays a popup window allowing the user to select a pet from a dropdown.
Shows animated preview for each pet.
Disables the Save button if the selected pet is missing idle or action frames.
"""
def show_popup():

    popup = tk.Tk()
    popup.title("Select Pet")
    popup.geometry("250x280")
    popup.resizable(False, False)
    popup.configure(bg="lightblue")

    dropdown_selected_pet = tk.StringVar(value=DEFAULT_PET)
    idle_frames, action_frames = load_preview_frames(DEFAULT_PET)
    frame_index = [0]  
    is_acting = [False]  
    result = {"pet": None}

    """
    Animate() cycles through idle and action frames to animate the pet preview.
    Uses modulo (%) to loop back to the first frame after reaching the last.
    """
    def animate():

        if not idle_frames:
            print("[Warning] No idle frames loaded for selected pet.")
            return

        frames = action_frames if is_acting[0] and action_frames else idle_frames
        current_frame = frames[frame_index[0] % len(frames)]  
        canvas.itemconfig(sprite, image=current_frame)
        frame_index[0] = (frame_index[0] + 1) % len(frames)

        if frame_index[0] == 0 and action_frames:
            is_acting[0] = not is_acting[0]

        popup.after(150, animate)

    """
    Enables or disables the Save button based on availability of idle and action frames.
    Prevents starting the app without essential frames.
    """
    def update_save_button_state():

        if idle_frames and action_frames:
            save_btn.config(state=tk.NORMAL)
        else:
            save_btn.config(state=tk.DISABLED)

    """
    Triggered when the selected pet changes.
    Reloads frames, resets animation state, and updates Save button status.
    """
    def on_pet_change(*_):

        nonlocal idle_frames, action_frames
        new_pet = dropdown_selected_pet.get()
        idle_frames, action_frames = load_preview_frames(new_pet)

        frame_index[0] = 0
        is_acting[0] = False

        update_save_button_state()

        if not idle_frames or not action_frames:
            print(f"[Warning] Pet '{new_pet}' missing frames - Save disabled.")

        if idle_frames:
            canvas.itemconfig(sprite, image=idle_frames[0])
        else:
            canvas.itemconfig(sprite, image='')

    """
    Saves the currently selected pet and closes the popup.
    """
    def save_and_start():
        selected = dropdown_selected_pet.get()
        result["pet"] = selected
        popup.destroy()

    """
    Handles popup close event without selection.
    Logs info and closes the popup.
    """
    def on_close():
        print("[Info] Popup closed. No pet selected.")
        popup.destroy()

    canvas = tk.Canvas(
        popup,
        width=PET_FRAME_WIDTH,
        height=PET_FRAME_HEIGHT,
        highlightthickness=0,
        bg="lightblue"
    )
    canvas.pack(pady=10)

    label = tk.Label(
        popup,
        text="Choose Your Pet",
        font=("Arial", 12, "bold"),
        bg="lightblue"
    )
    label.pack(pady=(5, 0))

    dropdown = tk.OptionMenu(popup, dropdown_selected_pet, *PET_LIST)
    max_len = max(len(name) for name in PET_LIST)
    dropdown.config(width=max_len)
    dropdown.pack(pady=5)

    initial_image = idle_frames[0] if idle_frames else None
    sprite = canvas.create_image(PET_FRAME_WIDTH // 2, PET_FRAME_HEIGHT // 2, image=initial_image)

    save_btn = tk.Button(
        popup,
        text="Save",
        command=save_and_start,
        bg="green",
        fg="white",
        font=("Arial", 16, "bold"),
        width=10,
        height=2,
        relief="raised",
        bd=4,
        activebackground="#006400",
        activeforeground="white"
    )
    save_btn.pack(pady=10)

    dropdown_selected_pet.trace_add("write", on_pet_change)
    popup.protocol("WM_DELETE_WINDOW", on_close)

    update_save_button_state()

    animate()
    popup.mainloop()

    return result["pet"]
