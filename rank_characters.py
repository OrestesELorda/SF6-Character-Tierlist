import json

def placement_to_number(placement_str):
    if placement_str == "":
        return None
    if "-" in placement_str:
        low, high = placement_str.split("-")
        return (int(low) + int(high)) / 2
    return int(placement_str)


def load_raw_data():
    with open("data/rankings_raw.json") as f:
        return json.load(f)


def main():
    data = load_raw_data()
    count = 0
   
    placements_by_character = {"Ryu": [], "Ken": [], "Chun-Li": [], "Guile": [], "E. Honda": [], "Blanka": [], "Zangief": [], "Dhalsim": [], "Cammy": [], "Dee Jay": [], "Juri": [], "Luke": [], "Jamie": [], "Kimberly": [], "Manon": [], "Marisa": [], "Lily": [], "JP": [], "Rashid": [], "A.K.I.": [], "Ed": [], "Akuma": [], "M. Bison": [], "Terry": [], "Mai": [], "Elena": [], "C. Viper": [], "Alex": [], "Sagat": [], "Ingrid": [], "Yasmine" : []}

    for tournament_name, rows in data.items():
        count = count+1
        for row in rows:
            
            main_character = row['opponentplayers']["p1chars"]
            if "," in main_character:
                main_character = main_character.split(",")[0]

            
            placement_number = placement_to_number(row["placement"])
            
            placements_by_character [main_character].append(placement_number)
            pass

    averages = {}
    for char in placements_by_character:
        if len(placements_by_character[char]) == 0:
            averages[char] = 0
            continue
        ind_avg = 0
        for placements in placements_by_character[char]:
            ind_avg += placements
        averages[char] = ind_avg / len(placements_by_character[char])


    ranked_names = sorted(averages, key=averages.get)
    ranked = [{"character": name, "average": averages[name]} for name in ranked_names]

    with open("data/rankings.json","w") as file:
        json.dump(ranked, file, indent=2)


if __name__ == "__main__":
    main()
