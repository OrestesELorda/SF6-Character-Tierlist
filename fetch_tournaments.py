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


def get_top(pagename, top=8):
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
        return(response.json())


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
        top8 = get_top(pagename, top=8)

        if top8 is None:
            print("  skipped (request failed)")
            continue

        all_data[name] = top8["result"]
        time.sleep(1)

    os.makedirs("data", exist_ok=True)
    with open("data/rankings_raw.json", "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"Saved {len(all_data)} tournaments to data/rankings_raw.json")