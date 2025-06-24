"""
Main application window for the Virtual Pet Pal.
Initializes and runs the pet animation, health, and interaction logic.
"""

import tkinter as tk
from PIL import ImageTk
import os
import sys

from config import (
    PET_PLAY_SPEED, ANIMATION_DELAY, HEALTH_DECREASE_INTERVAL, ACTION_INTERVAL,
    ACTION_DURATION, SLEEP_HEALTH_THRESHOLD, FULL_HEALTH, PET_FRAME_WIDTH, PET_FRAME_HEIGHT
)
from pet_loader import load_frames, load_health_frames

selected_pet = None  

"""
Initializes and runs the main application window.
Loads animations and health frames, sets up UI, and manages pet state and behavior.
"""
def run_main_app(pet_name):

    global selected_pet
    selected_pet = pet_name

    root_window = tk.Tk()
    root_window.overrideredirect(True)  # Makes the window borderless
    root_window.attributes("-topmost", True)  # Ensures the application always stays on top

    screen_width = root_window.winfo_screenwidth()
    screen_height = root_window.winfo_screenheight()
    transparent_color = "magenta"  

    root_window.config(bg=transparent_color)
    root_window.wm_attributes("-transparentcolor", transparent_color)

    window_width, window_height = 400, 400
    window_x = screen_width - window_width - 10
    window_y = screen_height - window_height - 40
    root_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # All the available animations
    animations = {
        "Idle": load_frames(selected_pet, "Idle"),
        "Action": load_frames(selected_pet, "Action"),
        "Sleep": load_frames(selected_pet, "Sleep"),
        "Play": load_frames(selected_pet, "Play")
    }

    for action, frames in animations.items():
        if not frames or not all(frames):
            print(f"[Warning] Animation frames missing or incomplete for '{action}' action.")
            sys.exit(1)

    health_images = load_health_frames()

    if not health_images:
        print("[Error] Health frames failed to load. Health bar will not display.")
        sys.exit(1)

    canvas = tk.Canvas(
        root_window,
        width=window_width,
        height=window_height,
        bg=transparent_color,
        highlightthickness=0
    )
    canvas.place(x=0, y=0)

    # The location of the pet sprite on the screen
    frame_w = animations["Idle"][0][0].width() if animations["Idle"] else 100  
    frame_h = animations["Idle"][0][0].height() if animations["Idle"] else 100
    x = window_width - frame_w - 10
    y = window_height - frame_h - 10

    direction = "left"  
    current_action = ["Idle"]  
    is_playing = [False]  
    is_sleeping = [False]  
    current_health = [FULL_HEALTH]  
    mood = ["Happy"]  
    running_health_job = [None]  
    sleep_animation_done = [False]

    right_frames, left_frames = animations[current_action[0]]
    frame_index = [0]

    pet_sprite = canvas.create_image(x, y, anchor="nw", image=left_frames[0] if left_frames else None)

    # The mood text setup
    mood_text = canvas.create_text(
        x + frame_w // 2,
        y - 20,
        text=f"Mood: {mood[0]}",
        font=("Arial", 10, "bold"),
        fill="white"
    )
    canvas.tag_raise(mood_text)

    # UI Frame with buttons and health bar 
    ui_frame = tk.Frame(canvas, bg=transparent_color)
    feed_btn = tk.Button(ui_frame, text="Feed", command=lambda: feed_pet())
    close_btn = tk.Button(ui_frame, text="Close", command=root_window.destroy)
    feed_btn.grid(row=0, column=0, padx=10)
    close_btn.grid(row=0, column=1, padx=10)

    health_label = tk.Label(ui_frame, image=health_images[current_health[0] - 1] if health_images else None,
                            bg=transparent_color)
    health_label.grid(row=1, column=0, columnspan=2)
    canvas.create_window(window_width - 120, y - 135, anchor="nw", window=ui_frame)

    """
    Updates the health bar image to reflect the pet's current health.
    Called periodically whenever health changes.
    """
    def update_health_bar():

        current_health_index = max(current_health[0], 1) - 1
        if health_images and 0 <= current_health_index < len(health_images):
            health_label.config(image=health_images[current_health_index])

    """
    Updates the pet's mood text based on its current action and health level.
    """
    def update_mood():

        if current_action[0] in ["Play", "Action"]:
            mood[0] = "Energetic"
        elif current_action[0] == "Sleep" or current_health[0] <= SLEEP_HEALTH_THRESHOLD:
            mood[0] = "Hungry"
        else:
            mood[0] = "Happy"

    """
    Changes the pet's current animation action if allowed,
    updates frames accordingly, and refreshes the pet's mood.
    """
    def switch_action(action):

        if is_playing[0] and action not in ["Sleep", "Play"]:
            return
        if current_action[0] == "Sleep" and action not in ["Sleep", "Idle"]:
            return
        if action not in animations:
            return

        frames = animations.get(action)

        if isinstance(frames, tuple) and len(frames) == 2:
            nonlocal right_frames, left_frames
            right_frames, left_frames = frames
        else:
            right_frames, left_frames = ([], [])

        current_action[0] = action
        frame_index[0] = 0
        sleep_animation_done[0] = False if action == "Sleep" else sleep_animation_done[0]
        update_mood()

    """
    Resets the pet's health to full, cancels any ongoing health decrease,
    and switches the pet to the idle animation.
    """
    def feed_pet():

        current_health[0] = FULL_HEALTH
        is_sleeping[0] = False
        sleep_animation_done[0] = False
        update_health_bar()

        if running_health_job[0]:
            root_window.after_cancel(running_health_job[0])
            running_health_job[0] = None
            is_playing[0] = False

        switch_action("Idle")

    """
    Stops the play action, cancels health decrease timers,
    and switches the pet to idle unless it's sleeping.
    """
    def stop_play():

        is_playing[0] = False
        if running_health_job[0]:
            root_window.after_cancel(running_health_job[0])
            running_health_job[0] = None

        if current_action[0] != "Sleep":
            switch_action("Idle")

    """
    Decreases health faster while the pet is playing.
    If health falls below the threshold, switches pet to sleep.
    """
    def play_health_decrease():

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

    """
    Starts the play action when the pet sprite is clicked,
    initiating faster health decrease and play animation.
    """
    def on_click(event):

        mouse_x, mouse_y = event.x, event.y
        if x < mouse_x < x + frame_w and y < mouse_y < y + frame_h:
            if current_action[0] != "Sleep" and not is_playing[0]:
                is_playing[0] = True
                switch_action("Play")
                play_health_decrease()
                root_window.after(3000, stop_play)

    """
    Periodically switches pet actions between idle and action animations,
    to simulate natural pet behavior.
    """
    def action_cycle():

        if not is_playing[0] and not is_sleeping[0] and current_action[0] != "Sleep":
            switch_action("Action")
            root_window.after(ACTION_DURATION, lambda: switch_action("Idle"))

        root_window.after(ACTION_INTERVAL, action_cycle)

    """
    Gradually decreases the pet's health over time when not playing or sleeping.
    Triggers sleep action if health falls below threshold.
    """
    def decrease_health():
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

    """
    Animates the pet by updating its animation frames and position.
    Handles pet movement during play, updates mood text position,
    and schedules itself to run periodically for smooth animation.
    """
    def animate():
        if current_action[0] == "Sleep" and not sleep_animation_done[0]:
            if frame_index[0] < len(right_frames) - 1:
                frame_index[0] += 1
            else:
                sleep_animation_done[0] = True
        elif current_action[0] != "Sleep":
            frame_index[0] = (frame_index[0] + 1) % len(right_frames) if right_frames else 0

        nonlocal x, direction

        if current_action[0] == "Play":
            if direction == "right":
                x += PET_PLAY_SPEED
                if x >= window_width - frame_w:
                    direction = "left"
            else:
                x -= PET_PLAY_SPEED
                if x <= 0:
                    direction = "right"

        text_x = max(60, min(window_width - 60, x + frame_w // 2))

        canvas.coords(pet_sprite, x, y)
        canvas.coords(mood_text, text_x, y - 20)
        canvas.itemconfig(mood_text, text=f"Mood: {mood[0]}", fill="white")

        if right_frames and left_frames:
            canvas.itemconfig(pet_sprite, image=(right_frames if direction == "right" else left_frames)[frame_index[0]])

        root_window.after(ANIMATION_DELAY, animate)

    canvas.tag_bind(pet_sprite, "<Button-1>", on_click)

    action_cycle()
    decrease_health()
    animate()

    root_window.mainloop()
