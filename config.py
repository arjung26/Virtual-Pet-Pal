"""
Configuration settings for Virtual Pet Pal.
Defines constant values used throughout the application.
"""

# --- Pet Settings ---
PET_LIST = ["Dog", "Cat", "Minotaur", "Werewolf"]
DEFAULT_PET = "Dog"
PET_PLAY_SPEED = 10
PET_FRAME_WIDTH = 130  
PET_FRAME_HEIGHT = 130  

# --- Animation Settings ---
ANIMATION_DELAY = 120  # milliseconds

# --- Health Settings ---
FULL_HEALTH = 56
HEALTH_DECREASE_INTERVAL = 5000  # milliseconds
SLEEP_HEALTH_THRESHOLD = 20

# --- Action Timings ---
ACTION_INTERVAL = 15000  # milliseconds
ACTION_DURATION = 3000   # milliseconds
