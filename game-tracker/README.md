# Simple Game Tracker

A lightweight command-line tool for tracking video games you've played or plan to play.  
You can store each game's title, platform, total hours, and current status.  
All data is saved locally in a JSON file so your library persists between runs.

---

## Features

- **View all games** currently in your library  
- **Add new games** (title, platform, hours played, status)  
- **Update game hours or status**  
- **Delete games**  
- **Search** by:
  - Title  
  - Platform  
  - Status (playing / backlog / finished)  
- **Export basic stats** to a text report:
  - Total number of games  
  - Total hours played  
  - Games by status  
  - Hours by platform  
  - Average hours per finished game  

Data is stored in `games.json`, and exported reports are written to `stats.txt`.

---

## Tech Stack

- **Language:** Python 3  
- **Libraries:** Standard Python library only (`json`, basic file I/O)  
- **Data Format:** JSON for persistent storage  

---

## How to Run

1. Make sure you have **Python 3** installed.

2. Clone this repository:

    ```bash
    git clone https://github.com/Noahlies/Noah-Jones-Portfolio.git
    cd Noah-Jones-Portfolio/game-tracker
    ```

3. Run the program:

    ```bash
    python game_tracker.py
    ```
    or:
    ```bash
    py game_tracker.py
    ```

---

## Project Structure

```text
game-tracker/
│
├── game_tracker.py     # Main application
├── games.json          # Auto-generated data file
├── stats.txt           # Exported stats report
└── README.md
```

`games.json` and `stats.txt` are automatically created the first time you run the app.

---

## Possible Future Improvements

- Increment hours instead of replacing the total  
- Tag games by genre or priority  
- Sort/filter features (e.g., backlog-only, most-played)  
- Export stats as CSV for Excel or Pandas  
- Convert into a simple GUI (Tkinter) or small web app (Flask/FastAPI)  

---

## About the Project

This project is part of my ongoing Python practice and portfolio development.  
The goal was to build something functional using only the standard library while focusing on file I/O, data persistence, and clean code organization.
