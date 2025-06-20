# Pet selection popup UI for virtual pet pal

# --- Imports ---
import tkinter as tk
from tkinter import messagebox
from pet_loader import load_preview_frames
from config import PET_LIST, DEFAULT_PET, CANVAS_WIDTH, CANVAS_HEIGHT

# --- Show Popup ---
def show_popup():
    """
    Displays a popup window allowing the user to select a pet from a dropdown.
    Includes animated preview for each pet.
    The Save button is disabled if the selected pet is missing idle or action frames.
    """

    # Initialize popup window
    popup = tk.Tk()
    popup.title("Select Pet")
    popup.geometry("250x280")
    popup.resizable(False, False)
    popup.configure(bg="lightblue")

    # --- Variables ---
    dropdown_selected_pet = tk.StringVar(value=DEFAULT_PET)
    idle_frames, action_frames = load_preview_frames(DEFAULT_PET)
    frame_index = [0]
    is_acting = [False]
    result = {"pet": None}

    # --- Animate Preview ---
    def animate():
        # Stop animation if no idle frames at all
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

    # --- Enable/Disable Save Button Based on Frames ---
    def update_save_button_state():
        if idle_frames and action_frames:
            save_btn.config(state=tk.NORMAL)
        else:
            save_btn.config(state=tk.DISABLED)

    # --- Handle Pet Selection Change ---
    def on_pet_change(*_):
        nonlocal idle_frames, action_frames
        new_pet = dropdown_selected_pet.get()
        idle_frames, action_frames = load_preview_frames(new_pet)

        # Reset animation variables
        frame_index[0] = 0
        is_acting[0] = False

        # Update Save button enabled/disabled state
        update_save_button_state()

        # Debug warning if frames missing
        if not idle_frames or not action_frames:
            print(f"[Warning] Pet '{new_pet}' missing frames - Save disabled.")

        # Update sprite image or clear if no idle frames
        if idle_frames:
            canvas.itemconfig(sprite, image=idle_frames[0])
        else:
            canvas.itemconfig(sprite, image='')  # Clear image if none

    # --- Save Pet and Close Popup ---
    def save_and_start():
        selected = dropdown_selected_pet.get()
        result["pet"] = selected
        popup.destroy()

    # --- Handle Window Close ---
    def on_close():
        print("[Info] Popup closed. No pet selected.")
        popup.destroy()

    # --- UI Elements ---
    canvas = tk.Canvas(
        popup,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
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

    # Use a placeholder frame if idle_frames is empty
    initial_image = idle_frames[0] if idle_frames else None
    sprite = canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=initial_image)

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

    # --- Bind Events ---
    dropdown_selected_pet.trace_add("write", on_pet_change)
    popup.protocol("WM_DELETE_WINDOW", on_close)

    # --- Initial Save Button State Setup ---
    update_save_button_state()

    # --- Start Animation & Mainloop ---
    animate()
    popup.mainloop()

    return result["pet"]
