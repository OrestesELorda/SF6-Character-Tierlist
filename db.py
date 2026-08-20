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
        conn.execute("""
            INSERT INTO placements (player_name, pagename, placement, placement_number, main_character)
            VALUES (?, ?, ?, ?, ?)
        """, (player_name, row["pagename"], row["placement"], row["placement_number"], main_character))
    conn.commit()
    conn.close()


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
