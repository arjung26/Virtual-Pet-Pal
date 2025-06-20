# Main application window for virtual pet pal

# --- Imports ---
import tkinter as tk
from PIL import ImageTk
import os

from config import (
    PET_SPEED, ANIMATION_DELAY, HEALTH_DECREASE_INTERVAL, ACTION_INTERVAL,
    ACTION_DURATION, SLEEP_HEALTH_THRESHOLD, FULL_HEALTH, CANVAS_WIDTH, CANVAS_HEIGHT
)
from pet_loader import load_frames, load_health_frames

# --- Global variable ---
selected_pet = None  


# --- Run Main App ---
def run_main_app(pet_name):
    """
    Initializes the main pet window with animations and health logic,
    handling user interaction and pet behavior.
    """

    global selected_pet
    selected_pet = pet_name

    # Initialize root window with transparent background and no decorations
    root_window = tk.Tk()
    root_window.overrideredirect(True)  # Remove title bar
    root_window.attributes("-topmost", True)  # Keep window on top

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    transparent_color = "magenta"  # Color used for transparency

    root_window.config(bg=transparent_color)
    root_window.wm_attributes("-transparentcolor", transparent_color)

    # Set window size and position at bottom-right corner of screen
    window_width, window_height = 400, 400
    window_x = screen_width - window_width - 10
    window_y = screen_height - window_height - 40
    root_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # --- Load Animations ---
    animations = {
        "Idle": load_frames(selected_pet, "Idle"),
        "Action": load_frames(selected_pet, "Action"),
        "Sleep": load_frames(selected_pet, "Sleep"),
        "Play": load_frames(selected_pet, "Play")
    }

    # Edge case: Ensure all animations loaded properly
    for action, frames in animations.items():
        if not frames or not all(frames):
            print(f"[Warning] Animation frames missing or incomplete for '{action}' action.")

    health_images = load_health_frames()
    if not health_images:
        print("[Error] Health frames failed to load. Health bar will not display.")

    # --- Setup Canvas ---
    canvas = tk.Canvas(
        root_window,
        width=window_width,
        height=window_height,
        bg=transparent_color,
        highlightthickness=0
    )
    canvas.place(x=0, y=0)

    # Initial position for the pet sprite within the window
    frame_w = animations["Idle"][0][0].width() if animations["Idle"] else 100  
    frame_h = animations["Idle"][0][0].height() if animations["Idle"] else 100
    x = window_width - frame_w - 10
    y = window_height - frame_h - 10

    # --- State Variables ---
    direction = "left"  
    current_action = ["Idle"]  
    is_playing = [False]  
    is_sleeping = [False]  
    current_health = [FULL_HEALTH]  
    mood = ["Happy"]  
    running_health_job = [None]  

    # Frames for current animation direction
    right_frames, left_frames = animations[current_action[0]]
    frame_index = [0]

    # Create pet sprite image on canvas (initial frame)
    pet_sprite = canvas.create_image(x, y, anchor="nw", image=left_frames[0] if left_frames else None)

    # Floating text above pet to display mood
    mood_text = canvas.create_text(
        x + frame_w // 2,
        y - 20,
        text=f"Mood: {mood[0]}",
        font=("Arial", 10, "bold"),
        fill="white"
    )
    canvas.tag_raise(mood_text)

    # --- UI Frame with buttons and health bar ---
    ui_frame = tk.Frame(canvas, bg=transparent_color)
    feed_btn = tk.Button(ui_frame, text="Feed", command=lambda: feed_pet())
    close_btn = tk.Button(ui_frame, text="Close", command=root_window.destroy)
    feed_btn.grid(row=0, column=0, padx=10)
    close_btn.grid(row=0, column=1, padx=10)

    health_label = tk.Label(ui_frame, image=health_images[current_health[0] - 1] if health_images else None,
                            bg=transparent_color)
    health_label.grid(row=1, column=0, columnspan=2)
    canvas.create_window(window_width - 120, y - 135, anchor="nw", window=ui_frame)

    # --- Helper functions ---

    def update_health_bar():
        """Update health bar image based on current health index."""
        current_health_index = max(current_health[0], 1) - 1
        if health_images and 0 <= current_health_index < len(health_images):
            health_label.config(image=health_images[current_health_index])
        else:
            print("[Warning] Cannot update health bar: health image index out of range or images missing.")

    def update_mood():
        """Update pet's mood string based on current action and health."""
        if current_action[0] in ["Play", "Action"]:
            mood[0] = "Energetic"
        elif current_action[0] == "Sleep" or current_health[0] <= SLEEP_HEALTH_THRESHOLD:
            mood[0] = "Hungry"
        else:
            mood[0] = "Happy"

    def switch_action(action):
        """
        Switch pet's current action and reset animation frames.
        Handles restrictions if pet is playing or sleeping.
        """

        if is_playing[0] and action not in ["Sleep", "Play"]:
            return
        
        if current_action[0] == "Sleep" and action not in ["Sleep","Idle"]:
            return

        if action not in animations:
            print(f"[Warning] Animation for action '{action}' not found.")
            return

        frames = animations.get(action)
        if isinstance(frames, tuple) and len(frames) == 2:
            nonlocal right_frames, left_frames
            right_frames, left_frames = frames
        else:
            right_frames, left_frames = ([], [])
            print(f"[Warning] Animation frames for '{action}' are invalid.")

        current_action[0] = action
        frame_index[0] = 0
        update_mood()

    def feed_pet():
        """Reset health to full and revive pet. """
        current_health[0] = FULL_HEALTH
        is_sleeping[0] = False
        update_health_bar()

        if running_health_job[0]:
            root_window.after_cancel(running_health_job[0])
            running_health_job[0] = None
            is_playing[0] = False

        switch_action("Idle")

    def stop_play():
        """Stop playing action and reset states."""
        is_playing[0] = False
        if running_health_job[0]:
            root_window.after_cancel(running_health_job[0])
            running_health_job[0] = None

        if current_action[0] != "Sleep":
            switch_action("Idle")

    def play_health_decrease():
        """
        Decrease health periodically while playing.
        If health drops below threshold, put pet to sleep.
        If health too low, pet 'sleeps' and stops playing.
        """
        if current_action[0] != "Play":
            return

        if current_health[0] > 2:
            current_health[0] -= 1
            update_health_bar()
            update_mood()

            if current_health[0] <= SLEEP_HEALTH_THRESHOLD and current_action[0] != "Sleep":
                switch_action("Sleep")
                stop_play()
                return

            running_health_job[0] = root_window.after(500, play_health_decrease)
        else:
            current_health[0] = 2
            is_sleeping[0] = True
            update_health_bar()
            update_mood()

            if current_action[0] != "Sleep":
                switch_action("Sleep")
            stop_play()

    def on_click(event):
        """
        Handle clicks on the pet sprite to trigger play action if possible.
        """
        mouse_x, mouse_y = event.x, event.y

        if x < mouse_x < x + frame_w and y < mouse_y < y + frame_h:
            if current_action[0] != "Sleep" and not is_playing[0]:
                is_playing[0] = True
                switch_action("Play")
                play_health_decrease()
                root_window.after(3000, stop_play)

    def action_cycle():
        """
        Cycle between action and idle animations at regular intervals.
        Only act if not acting or sleeping.
        """
        if not is_playing[0] and current_action[0] != "Sleep":
            switch_action("Action")
            root_window.after(ACTION_DURATION, lambda: switch_action("Idle"))

        root_window.after(ACTION_INTERVAL, action_cycle)

    def decrease_health():
        """
        Gradually decrease pet health over time when idle.
        Switch pet to sleep state if health falls below threshold.
        """
        if not is_sleeping[0] and not is_playing[0]:
            if current_health[0] > 2:
                current_health[0] -= 1
                update_health_bar()
                update_mood()

                if current_health[0] <= SLEEP_HEALTH_THRESHOLD and current_action[0] != "Sleep":
                    switch_action("Sleep")
            else:
                current_health[0] = 2
                is_sleeping[0] = True
                update_health_bar()
                update_mood()

        root_window.after(HEALTH_DECREASE_INTERVAL, decrease_health)

    def animate():
        """
        Main animation loop for cycling frames and moving pet when playing.
        Also updates mood text position and image based on direction.
        """
        frame_index[0] = (frame_index[0] + 1) % len(right_frames) if right_frames else 0

        # If sleeping, show last frame only
        if current_action[0] == "Sleep" and right_frames:
            frame_index[0] = len(right_frames) - 1

        nonlocal x, direction

        # Move pet left and right when running
        if current_action[0] == "Play":
            if direction == "right":
                x += PET_SPEED
                if x >= window_width - frame_w:
                    direction = "left"
            else:
                x -= PET_SPEED
                if x <= 0:
                    direction = "right"

        # Clamp mood text position within window bounds
        text_x = max(60, min(window_width - 60, x + frame_w // 2))

        # Update sprite and text positions and images
        canvas.coords(pet_sprite, x, y)
        canvas.coords(mood_text, text_x, y - 20)
        canvas.itemconfig(mood_text, text=f"Mood: {mood[0]}", fill="white")

        # Set sprite image based on direction and current frame
        if right_frames and left_frames:
            canvas.itemconfig(pet_sprite, image=(right_frames if direction == "right" else left_frames)[frame_index[0]])

        # Schedule next animation frame
        root_window.after(ANIMATION_DELAY, animate)

    # --- Bind click event to pet sprite ---
    canvas.tag_bind(pet_sprite, "<Button-1>", on_click)

    # --- Start cycles and main loop ---
    action_cycle()
    decrease_health()
    animate()

    root_window.mainloop()