import json
import time
from fetch_tournaments import get_player_placements
from db import init_db, replace_player_placements, get_players_with_no_data


def load_players_to_fetch():
    with open("data/players_to_fetch.json") as f:
        return json.load(f)


def fetch_players(player_names):
    for name in player_names:
        print("Fetching placements for:", name)
        result = get_player_placements(name)

        if result is None:
            print("  skipped (request failed)")
            continue

        replace_player_placements(name, result["result"])
        time.sleep(2)


if __name__ == "__main__":
    init_db()
    player_names = load_players_to_fetch()

    fetch_players(player_names)
    print(f"Finished main pass for {len(player_names)} players")

    never_fetched = get_players_with_no_data(player_names)
    if never_fetched:
        print(f"Retrying {len(never_fetched)} players with zero data: {never_fetched}")
        fetch_players(never_fetched)

    still_missing = get_players_with_no_data(player_names)
    print(f"Done. {len(still_missing)} players still have no data: {still_missing}")
