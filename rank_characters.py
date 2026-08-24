import json
import statistics
from db import get_placements_by_player, get_player_details

CONSISTENCY_WEIGHT = 0.5  # higher = punish inconsistent players more
MIN_APPEARANCES = 3  # players below this are excluded, too little data to trust
TIERS = ["S", "A", "B", "C", "D", "F"]  # best to worst, players split evenly across these


def assign_tier(index, total):
    tier_index = (index * len(TIERS)) // total
    return TIERS[tier_index]


def main():
    placements_by_player = get_placements_by_player()
    player_details = get_player_details()

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
    total = len(ranked_names)
    ranked = [
        {
            "player": name,
            "score": scores[name],
            "average": stats_by_player[name]["average"],
            "std_dev": stats_by_player[name]["std_dev"],
            "flag": player_details[name]["flag"],
            "characters": player_details[name]["characters"],
            "tier": assign_tier(i, total),
        }
        for i, name in enumerate(ranked_names)
    ]

    with open("data/rankings.json","w") as file:
        json.dump(ranked, file, indent=2)


if __name__ == "__main__":
    main()
