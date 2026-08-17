import json
import time
from fetch_tournaments import get_player_placements


def load_player_names():
    with open("data/rankings.json") as f:
        ranked = json.load(f)
    return [entry["player"] for entry in ranked]


if __name__ == "__main__":
    player_names = load_player_names()

    all_data = {}

    for name in player_names:
        print("Fetching placements for:", name)
        result = get_player_placements(name)

        if result is None:
            print("  skipped (request failed)")
            continue

        all_data[name] = result["result"]
        time.sleep(2)

    with open("data/player_placements_raw.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"Saved placement data for {len(all_data)} players to data/player_placements_raw.json")
