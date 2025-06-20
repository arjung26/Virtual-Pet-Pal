# Entry point for the virtual pet pal

# --- Imports ---
from pet_selector import show_popup
from pet_window import run_main_app

# --- Main Execution ---
def main():
    # Show popup to select a pet
    selected_pet = show_popup()

    # Exit if no pet is selected
    if not selected_pet:
        print("Pet selection cancelled. Exiting application.")
        return

    # Run main pet window with selected pet
    run_main_app(selected_pet)

if __name__ == "__main__":
    main()