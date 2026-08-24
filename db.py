import sqlite3
import os

DB_PATH = "data/tierlist.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tournaments (
            pagename TEXT PRIMARY KEY,
            name TEXT,
            startdate TEXT,
            is_complete INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS placements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            pagename TEXT,
            placement TEXT,
            placement_number REAL,
            main_character TEXT
        )
    """)

    existing_columns = {row[1] for row in conn.execute("PRAGMA table_info(placements)")}
    if "flag" not in existing_columns:
        conn.execute("ALTER TABLE placements ADD COLUMN flag TEXT")

    conn.commit()
    conn.close()


def get_complete_tournament_pagenames():
    conn = get_connection()
    rows = conn.execute("SELECT pagename FROM tournaments WHERE is_complete = 1").fetchall()
    conn.close()
    return {row[0] for row in rows}


def upsert_tournament(pagename, name, startdate, is_complete):
    conn = get_connection()
    conn.execute("""
        INSERT INTO tournaments (pagename, name, startdate, is_complete)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(pagename) DO UPDATE SET
            name=excluded.name,
            startdate=excluded.startdate,
            is_complete=excluded.is_complete
    """, (pagename, name, startdate, int(is_complete)))
    conn.commit()
    conn.close()


def replace_player_placements(player_name, rows):
    conn = get_connection()
    conn.execute("DELETE FROM placements WHERE player_name = ?", (player_name,))
    for row in rows:
        main_character = row["opponentplayers"].get("p1chars", "").split(",")[0]
        flag = row["opponentplayers"].get("p1flag", "")
        conn.execute("""
            INSERT INTO placements (player_name, pagename, placement, placement_number, main_character, flag)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (player_name, row["pagename"], row["placement"], row["placement_number"], main_character, flag))
    conn.commit()
    conn.close()


def get_players_with_no_data(player_names):
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT player_name FROM placements").fetchall()
    conn.close()
    have_data = {row[0] for row in rows}
    return [name for name in player_names if name not in have_data]


def get_players_missing_flag():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT player_name FROM placements WHERE flag IS NULL OR flag = ''").fetchall()
    conn.close()
    return [row[0] for row in rows]


def get_player_details():
    conn = get_connection()
    rows = conn.execute("SELECT player_name, flag, main_character FROM placements").fetchall()
    conn.close()

    details = {}
    for player_name, flag, main_character in rows:
        if player_name not in details:
            details[player_name] = {"flag": "", "characters": set()}
        if flag:
            details[player_name]["flag"] = flag
        if main_character:
            details[player_name]["characters"].add(main_character)

    for player_name in details:
        details[player_name]["characters"] = sorted(details[player_name]["characters"])

    return details


def get_placements_by_player():
    conn = get_connection()
    rows = conn.execute("SELECT player_name, placement_number FROM placements").fetchall()
    conn.close()

    placements_by_player = {}
    for player_name, placement_number in rows:
        if player_name not in placements_by_player:
            placements_by_player[player_name] = []
        placements_by_player[player_name].append(placement_number)
    return placements_by_player
