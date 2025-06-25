# Slug Dungeon

A Python turn-based dungeon escape game!  
Escape from a dungeon filled with different types of slugs, collect weapons, and survive turn-by-turn. This game is built with object-oriented programming (OOP) using the Model-View-Controller (MVC) pattern and features a Tkinter graphical interface.

---

## Game Overview

- **Goal:** Defeat all slugs and reach the goal tile (`G`) to win.
- **Controls:**
    - `W`: Move up
    - `A`: Move left
    - `S`: Move down
    - `D`: Move right
    - `Space`: Stay and attack from your current position
- Each turn, both you and the slugs take actions in order.

---

## Included Files

- `a2.py` – Main game file. All logic and GUI are here.
- `support.py` – Helper classes/constants (do not modify).
- `level1.txt`, `level2.txt` – Example levels/maps.
- `surround.txt` – Special level: you are surrounded by slugs for a survival challenge.

---

## How to Play

1. **Requirements**
    - Python 3.12 or later (with `tkinter` installed—usually included by default)
2. **Setup**
    - Download or clone this repository.
    - Make sure all `.py` and `.txt` files are in the same directory.
3. **Run the game**
    ```bash
    python a2.py
    ```
4. **Select a map** (e.g., `level1.txt`) when prompted.

---

## Level Descriptions

- **level1.txt / level2.txt:**  
  Standard levels with different enemy placements and map layouts.
    - `A`: AngrySlug (chases the player)
    - `N`: NiceSlug (never moves)
    - `L`: ScaredSlug (runs away from the player)
    - `P`: Player's starting position
    - `G`: Goal tile
- **surround.txt:**  
  A special "trapped" scenario where the player is surrounded by slugs at the start—designed to test how you handle tight situations!

---

## Key Features

- OOP & MVC code structure
- Multiple enemy types (each with unique AI: chase, run, or stay)
- Weapon system: PoisonDart, PoisonSword, HealingRock
- Turn-based mechanics with poison and health stats
- Tkinter-based GUI for map, stats, and controls
- Easily load and play custom level files

---

## File Guide

- **a2.py** – Edit and run this file to play.
- **support.py** – Do not change; contains constants and UI helpers.
- **level1.txt / level2.txt / surround.txt** – Level files (plain text, see these as templates for new maps).
- **README.md** – This help file.

---

## Creating Your Own Levels

- Level files are simple text files.
- The **first line** = player's max health (e.g., `30`)
- The following lines = map layout (`#` = wall, spaces = floor, see example files for all symbols)
- Add enemies and weapons using their symbols.

---

## License

This project is for educational/demo use only.

---

## Tips

- Try `surround.txt` for a real challenge!
- If stuck or the GUI does not launch, double-check your Python version and ensure Tkinter is installed.

---

Enjoy playing Slug Dungeon!  
Feel free to fork or adapt this project for your own experiments.
