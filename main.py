"""
Entry point for Virtual Pet Pal.
Runs the pet selection popup and launches the main application window
with the selected pet.
"""

from pet_selector import show_popup
from pet_window import run_main_app

def main():

    selected_pet = show_popup()

    # Exit gracefully if no pet was selected
    if not selected_pet:
        print("Pet selection cancelled. Exiting application.")
        return

    run_main_app(selected_pet)

if __name__ == "__main__":
    main()
