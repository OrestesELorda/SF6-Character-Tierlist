import time
from fetch_tournaments import get_player_placements
from db import init_db, get_players_missing_flag, replace_player_placements


if __name__ == "__main__":
    init_db()
    missing = get_players_missing_flag()

    if not missing:
        print("No players missing flag data.")
    else:
        print(f"{len(missing)} players missing flag data: {missing}")

        for name in missing:
            print("Fetching:", name)
            result = get_player_placements(name)

            if result is None:
                print("  failed")
                continue

            replace_player_placements(name, result["result"])
            print("  success")
            time.sleep(2)

        still_missing = get_players_missing_flag()
        print(f"Done. {len(still_missing)} players still missing flag data: {still_missing}")
