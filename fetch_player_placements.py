import json
import time
from fetch_tournaments import get_player_placements
from db import init_db, replace_player_placements


def load_players_to_fetch():
    with open("data/players_to_fetch.json") as f:
        return json.load(f)


if __name__ == "__main__":
    init_db()
    player_names = load_players_to_fetch()

    for name in player_names:
        print("Fetching placements for:", name)
        result = get_player_placements(name)

        if result is None:
            print("  skipped (request failed)")
            continue

        replace_player_placements(name, result["result"])
        time.sleep(2)

    print(f"Updated placement data for {len(player_names)} players in the database")
