# Virtual-Pet-Pal

Ever wanted a pet without the mess, feeding schedule, or fur all over your keyboard?
Virtual Pet Pal is your animated desktop companion built with Python and Tkinter.
It floats on your screen, responds to your clicks, and shows emotions — all without needing a litter box.
Whether you're feeding it or just watching it nap, your desktop will never feel lonely again.

---

## 🐾 Features

- **Pet Selection Popup:** Choose your favorite pet from an animated preview dropdown before starting.
- **Multiple Pets:** Select from a variety of pets (Dog, Cat, Minotaur, Werewolf) with unique animations.
- **Animated Behaviors:** Pets cycle through idle, action, play, and sleep animations to bring them to life.
- **Interactive Play:** Click on the pet to make it play — it moves across the screen while health decreases faster.
- **Health & Mood System:** The pet’s health decreases naturally over time; feeding restores health. Mood changes reflect its state (Happy, Energetic, Hungry).
- **Floating Transparent Window:** The pet floats on your desktop with a frameless, always-on-top window and transparent background.
- **Modular, Easy-to-Understand Code:** Clear separation of concerns with well-commented code for maintainability.

---

## 💻 Requirements
Before running the app, make sure the following are installed:

- Python 3.x
- Tkinter (usually bundled with Python — if not, install using your package manager)
- Pillow

---

## 🚀 How to Run
1. **Download the following files** and place them in the **same folder**:
   - `config.py`
   - `main.py`
   - `pet_loader.py`
   - `pet_window.py`
   - `pet_selector.py`
   - `Assets.zip`

2. **Extract the `Assets.zip` file**:
   - Ensure the contents are extracted into a folder named `Assets` in the same directory.
   - Your folder structure should look like this:

     ```
     /YourProjectFolder
     ├── config.py
     ├── main.py
     ├── pet_loader.py
     ├── pet_window.py
     ├── pet_selector.py
     ├── Assets
     │   ├── Pets
     │   │   ├── Dog
     │   │   ├── Cat
     │   │   └── ...
     │   └── Health_Bar
     ```

3. **Install required library (if not already installed)**:
   ```bash
   pip install pillow

4. **Run the application:**:
   ```bash
   python main.py

---

## 🐶 How to Interact With Your Pet

- Click on the pet to enter Play mode. The pet will move back and forth across the screen and lose health more quickly.

- When the pet gets tired (health is low), it will automatically fall asleep.

- Click the Feed button to restore health and wake the pet from sleep.

- Click the Close button to exit the application.

---

## 📂 Project Structure

- **main.py:** Entry point to start the application.

- **pet_selector.py:** Handles the pet selection popup with animated previews.

- **pet_window.py:** Handles the main pet window, animations, interactions, health, mood, and behavior.

- **pet_loader.py:** Loads animation and health bar image assets.

- **config.py:** Stores all global configuration constants.

- **Assets:** Contains pet animation images and health bar graphics.

---

## 📝 Notes

- Ensure that each pet folder includes **complete sets of animation frames** (`Idle`, `Action`, `Play`, `Sleep`).
- The `Assets/Health_Bar/` folder must contain numbered images from `1.png` to `56.png` to reflect different health states.
- If any required frames or health images are missing, the application will exit with a warning.
- All files (`.py` scripts and the `Assets/` folder) must be located **in the same directory** to run correctly.

---

## 📜 License

This project is licensed under the **MIT License** — feel free to use, modify, and share!

---

## 🙌 Final Notes

Virtual Pet Pal is a fun way to liven up your desktop with a tiny animated companion.  
Feel free to experiment with adding your own pets, animations, or new behaviors — and make it truly yours!

Happy coding! 🐾

