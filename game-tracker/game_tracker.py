# Simple Game Tracker - Phase 1
import json

FILENAME = "games.json"
STATS_FILENAME = "stats.txt"

# A list of games, each game is a dictionary
games = [
    {
        "title": "Fellowship",
        "platform": "PC",
        "hours": 120,
        "status": "playing"
    },
    {
        "title": "World of Warcraft",
        "platform": "PC",
        "hours": 500,
        "status": "backlog"
    },
    {
        "title": "Marvel Rivals",
        "platform": "PC",
        "hours": 40,
        "status": "finished"
    }
]


# -------------------------------------------------
# Helper functions (MOVED UP so they exist early)
# -------------------------------------------------

def save_games():
    with open(FILENAME, "w") as f:
        json.dump(games, f, indent=2)
    print("\nGames saved.\n")


def load_games():
    global games
    try:
        with open(FILENAME, "r") as f:
            games = json.load(f)
        print("Loaded games from file.\n")
    except FileNotFoundError:
        print("No save file found, starting with defaults.\n")


# -------------------------------------------------
# Display a single game
# -------------------------------------------------
def print_game(game):
    print("Title:", game["title"])
    print("Platform:", game["platform"])
    print("Hours:", game["hours"])
    print("Status:", game["status"])
    print("-" * 20)


# -------------------------------------------------
# Add a game
# -------------------------------------------------
def add_game():
    title = input("Enter game title: ")
    platform = input("Enter platform (PC, Xbox, Playstation, etc): ")
    hours = int(input("Hours played: "))
    status = input("Status (playing / backlog / finished): ")

    new_game = {
        "title": title,
        "platform": platform,
        "hours": hours,
        "status": status,
    }

    games.append(new_game)
    print("\nGame added successfully!\n")
    save_games()


# -------------------------------------------------
# Delete a game
# -------------------------------------------------
def delete_game():
    title = input("Enter the title of the game to delete: ")

    for index, game in enumerate(games):
        if game["title"].lower() == title.lower():
            print("\nFound this game:")
            print_game(game)

            confirm = input("Delete this game? (y/n): ").lower()
            if confirm == "y":
                games.pop(index)
                print("Game deleted.\n")
                save_games()
            else:
                print("Delete cancelled.\n")
            break
    else:
        print(f"No game found with title '{title}'.")


# -------------------------------------------------
# Update a game
# -------------------------------------------------
def update_game():
    title = input("\nEnter the title of the game to update: ").strip()

    for game in games:
        if game["title"].lower() == title.lower():
            print("\nFound this game:")
            print_game(game)

            print("\nWhat would you like to update?")
            print("1. Hours played")
            print("2. Status")
            choice = input("Choose 1 or 2: ")

            if choice == "1":
                new_hours_str = input("Enter new TOTAL hours: ")
                try:
                    new_hours = int(new_hours_str)
                    game["hours"] = new_hours
                    print("\nHours updated!")
                    save_games()
                except ValueError:
                    print("Invalid number, hours not changed.")

            elif choice == "2":
                new_status = input("Enter new status (playing / backlog / finished): ")
                game["status"] = new_status
                print("\nStatus updated.")
                save_games()

            return

    print(f"\nNo game found with title '{title}'.")

# =================================================
# Search feature
# =================================================
def search_games():
    while True:
        print("\n=== Search Games ===")
        print("1. Search by title")
        print("2. Search by platform")
        print("3. Search by status")
        print("4. Back to main menu")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "4":
            # Go back to main menu
            print()
            return
        
        if choice not in ("1", "2", "3"):
            print("Invalid choice, try again.")
            continue

    
        query = input("Enter search text: ").strip().lower()
        if not query:
            print("Empty search, try again.")
            continue

        if choice == "1":
            field = "title"
        elif choice == "2":
            field = "platform"
        else:
            field = "status"

        matches = []
        for game in games:
            value = str(game.get(field, "")).lower()
            if query in value:     # partial, case insensitive match
                matches.append(game)
            
        if not matches:
            print("\nNo games matched your search. \n")
        else:
            print(f"\nFound {len(matches)} matching game(s):\n")
            for game in matches:
                print_game(game)

# =================================================
# Stats + export
# =================================================
def export_stats():
    if not games:
        print("\nNo games to analyze. \n")
        return
    
    # total count + hours
    total_games = len(games)
    total_hours = sum(g["hours"] for g in games)

    # count by status
    status_counts = {"playing": 0, "backlog": 0, "finished": 0}
    for g in games:
        status = g["status"].lower()
        if status in status_counts:
            status_counts[status] += 1
        else:
            # just for adding new statuses
            status_counts[status] = status_counts.get(status, 0) + 1
    
    # hours per platform
    hours_by_platform = {}
    for g in games:
        platform = g["platform"]
        hours_by_platform[platform] = hours_by_platform.get(platform, 0) + g["hours"]

    # average hours per finished game
    finished_games = [g for g in games if g["status"].lower() == "finished"]
    if finished_games:
        avg_finished_hours = sum(g["hours"] for g in finished_games) / len(finished_games)
    else:
        avg_finished_hours = 0

    # build a text report
    lines = []
    lines.append("=== Game Tracker Stats ===")
    lines.append(f"Total games: {total_games}")
    lines.append(f"Total hours played (all games): {total_hours}")
    lines.append("")
    lines.append("Games by status:")
    for s, count in status_counts.items():
        lines.append(f" {s}: {count}")
    lines.append("")
    lines.append("Hours by platform:")
    for platform, hours in hours_by_platform.items():
        lines.append(f" {platform}: {hours} hours")
    lines.append("")
    lines.append(f"Average hours per finished game: {avg_finished_hours:.2f}")
    lines.append("")

    report_text = "\n".join(lines)

    # print to screen
    print("\n" + report_text)

    # save to file
    with open(STATS_FILENAME, "w") as f:
        f.write(report_text)

    print(f"Stats exported to {STATS_FILENAME}\n")

# -------------------------------------------------
# Main Menu Loop
# -------------------------------------------------
def menu():
    while True:
        print("\n=== Game Tracker Menu ===")
        print("1. View all games")
        print("2. Add a new game")
        print("3. Delete a game")
        print("4. Update hours/status")
        print("5. Search games")
        print("6. Export stats")
        print("7. Quit")
    

        choice = input("Choose an option (1-7): ")

        if choice == "1":
            print("\nCurrent games:")
            for game in games:
                print_game(game)

        elif choice == "2":
            add_game()

        elif choice == "3":
            delete_game()

        elif choice == "4":
            update_game()

        elif choice == "5":
            search_games()

        elif choice == "6":
            export_stats()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


# -------------------------------------------------
# Load saved games + start menu + a main guard
# -------------------------------------------------

def main():
    load_games()
    save_games()
    menu()

if __name__ == "__main__":
    main()
