# SF6 Player Tierlist

A tierlist of Street Fighter 6 players, ranked by competitive performance across tier-1 tournaments in the 2026 season. Data is pulled from [Liquipedia](https://liquipedia.net/fighters/) and updated automatically roughly twice a month.

**Live site:** https://oresteselorda.github.io/SF6-Character-Tierlist/

## How it works

The project has two parts: a Python data pipeline that fetches and ranks tournament results, and a React site that displays them.

```
Liquipedia API
      |
fetch_tournaments.py          (discovers tier-1 2026 tournaments, finds involved players)
      |
fetch_player_placements.py    (fetches each player's full placement history)
      |
tierlist.db (SQLite)          (stores tournaments + placements, avoids re-fetching known data)
      |
rank_characters.py            (computes average placement, consistency score, tier)
      |
data/rankings.json            (final ranked output)
      |
website/ (React + Vite)       (displays the tierlist, deployed to GitHub Pages)
```

## Ranking method

- **Score** = average placement + a penalty for inconsistency (standard deviation of placements), so a player who's reliably strong ranks above one with a single lucky result.
- Players need at least 3 tournament appearances to be ranked at all — too little data to be meaningful otherwise.
- Players are split evenly into six tiers (S/A/B/C/D/F) based on their sorted rank.

## Project structure

```
fetch_tournaments.py       fetches tier-1 SF6 tournaments, tracks which are complete
fetch_player_placements.py fetches each player's full placement record
rank_characters.py         computes scores and writes data/rankings.json
db.py                      SQLite layer — all database reads/writes go through here
backfill_flags.py          one-off tool to retry players missing flag data
data/tierlist.db           the database (tournaments + placements)
website/                   React + Vite frontend
.github/workflows/         GitHub Actions automation (fetch, rank, build, deploy)
```

## Running it locally

**Data pipeline:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your own Liquipedia API key:
```
LIQUIPEDIA_API_KEY=your_key_here
```

Then run the pipeline in order:
```bash
python fetch_tournaments.py
python fetch_player_placements.py
python rank_characters.py
```

**Website:**
```bash
cd website
npm install
npm run dev
```

## Automation

A GitHub Actions workflow (`.github/workflows/update-tierlist.yml`) runs the full pipeline on the 1st and 15th of each month, commits any updated data, rebuilds the site, and redeploys it to GitHub Pages. It can also be triggered manually from the Actions tab.

## Data source

Tournament and player data is provided by [Liquipedia](https://liquipedia.net/fighters/), licensed under [CC-BY-SA](https://liquipedia.net/fighters/Liquipedia:Copyrights). This project is not affiliated with Liquipedia or Capcom.
