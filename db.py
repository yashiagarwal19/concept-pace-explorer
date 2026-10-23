"""Tiny SQLite helper: stores anonymous learning interactions."""
import sqlite3

DB = "explorer.db"

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child TEXT, fmt TEXT, concept TEXT,
            correct INTEGER, response_ms INTEGER, hints INTEGER,
            reward REAL, ts TEXT DEFAULT CURRENT_TIMESTAMP)""")

def add_log(child, fmt, concept, correct, ms, hints, reward):
    with conn() as c:
        c.execute("INSERT INTO logs(child,fmt,concept,correct,response_ms,hints,reward) VALUES (?,?,?,?,?,?,?)",
                  (child, fmt, concept, correct, ms, hints, reward))

def stats(child):
    """Per-format summary for one child."""
    with conn() as c:
        return c.execute("""SELECT fmt, COUNT(*) n, AVG(reward) avg_reward,
            100.0*AVG(correct) accuracy, AVG(response_ms) avg_ms
            FROM logs WHERE child=? GROUP BY fmt""", (child,)).fetchall()

def children():
    with conn() as c:
        return [r["child"] for r in c.execute("SELECT DISTINCT child FROM logs ORDER BY child")]
