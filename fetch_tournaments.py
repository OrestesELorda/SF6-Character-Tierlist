import requests
import os
import json
import time
from dotenv import load_dotenv


load_dotenv()
key = os.getenv('LIQUIPEDIA_API_KEY')

if key is None:
    raise ValueError("LIQUIPEDIA_API_KEY not found — check your .env file")


headers = {"Authorization": "Apikey " + key}



def get_tournaments(year):
    params = {
    "wiki": "fighters",
    "conditions": f"[[game::sf6]] AND [[liquipediatier::1]] AND [[startdate_year::{year}]]",
    "limit": 50
    }
    response = requests.get("https://api.liquipedia.net/api/v3/tournament", headers=headers, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
    else:
        return(response.json())


def placement_to_number(placement_str):
    if placement_str == "":
        return None
    if "-" in placement_str:
        low, high = placement_str.split("-")
        return (int(low) + int(high)) / 2
    return int(placement_str)


def get_top(pagename, top=16):
    params = {
        "wiki" : "fighters",
        "conditions": f"[[pagename::{pagename}]]",
        "order": "weight DESC",
        "limit": top
    }
    response = requests.get("https://api.liquipedia.net/api/v3/placement", headers=headers, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
    else:
        data = response.json()
        for row in data["result"]:
            row["placement_number"] = placement_to_number(row.get("placement", ""))

        real_rows = [
            row for row in data["result"]
            if row["placement_number"] is not None
            and row["placement_number"] <= top
            and row.get("opponentplayers", {}).get("p1chars", "") != ""
        ]
        real_rows.sort(key=lambda row: row["placement_number"])

        data["result"] = real_rows
        return data


def get_player_placements(player_name):
    params = {
        "wiki": "fighters",
        "conditions": f"[[opponentname::{player_name}]] AND [[game::sf6]] AND [[liquipediatier::1]] AND [[startdate_year::2026]]",
        "limit": 50
    }

    response = requests.get("https://api.liquipedia.net/api/v3/placement", headers=headers, params=params)
    for attempt in range(3):
        if response.status_code != 429:
            break
        print(f"  rate limited, waiting before retry ({attempt + 1}/3)...")
        time.sleep(10)
        response = requests.get("https://api.liquipedia.net/api/v3/placement", headers=headers, params=params)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
    else:
        data = response.json()
        for row in data["result"]:
            row["placement_number"] = placement_to_number(row.get("placement", ""))

        real_rows = [
            row for row in data["result"]
            if row["placement_number"] is not None
        ]

        data["result"] = real_rows
        return data


if __name__ == "__main__":
    tournaments = get_tournaments(2026)

    all_data = {}

    for t in tournaments["result"]:
        name = t["name"]
        pagename = t["pagename"]

        if t.get("shortname") == "SFL":
            print("Skipping league-type tournament:", name)
            continue

        print("Fetching top 8 for:", name)
        top_players = get_top(pagename, top=16) #only returns top 8 if tournament does not hold data past top 8

        if top_players is None:
            print("  skipped (request failed)")
            continue

        all_data[name] = top_players["result"]
        time.sleep(1)

    os.makedirs("data", exist_ok=True)
    with open("data/rankings_raw.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"Saved {len(all_data)} tournaments to data/rankings_raw.json")