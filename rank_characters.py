import json
import statistics

CONSISTENCY_WEIGHT = 0.5  # higher = punish inconsistent players more
MIN_APPEARANCES = 3  # players below this are excluded, too little data to trust


def load_raw_data():
    with open("data/player_placements_raw.json") as f:
        return json.load(f)


def main():
    data = load_raw_data()

    placements_by_player = {
        player: [row["placement_number"] for row in rows]
        for player, rows in data.items()
    }

    scores = {}
    stats_by_player = {}
    for player in placements_by_player:
        placements = placements_by_player[player]

        if len(placements) < MIN_APPEARANCES:
            continue

        ind_avg = 0
        for p in placements:
            ind_avg += p
        avg = ind_avg / len(placements)

        std_dev = statistics.pstdev(placements)

        scores[player] = avg + CONSISTENCY_WEIGHT * std_dev
        stats_by_player[player] = {"average": avg, "std_dev": std_dev}


    ranked_names = sorted(scores, key=scores.get)
    ranked = [
        {
            "player": name,
            "score": scores[name],
            "average": stats_by_player[name]["average"],
            "std_dev": stats_by_player[name]["std_dev"],
        }
        for name in ranked_names
    ]

    with open("data/rankings.json","w") as file:
        json.dump(ranked, file, indent=2)


if __name__ == "__main__":
    main()
