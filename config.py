"""
Configuration settings for the virtual pet pal.

Includes pet options, animation parameters, health mechanics, and action timings.
"""

# --- Pet Settings ---
PET_LIST = ["Dog", "Cat", "Minotaur", "Werewolf"]
DEFAULT_PET = "Dog"
PET_SPEED = 10

# --- Animation Settings ---
ANIMATION_DELAY = 120  # milliseconds

# --- UI Settings ---
CANVAS_WIDTH = 130  
CANVAS_HEIGHT = 130  

# --- Health Settings ---
FULL_HEALTH = 56
HEALTH_DECREASE_INTERVAL = 5000  # milliseconds
SLEEP_HEALTH_THRESHOLD = 20

# --- Action Timings ---
ACTION_INTERVAL = 15000  # milliseconds
ACTION_DURATION = 3000   # milliseconds
