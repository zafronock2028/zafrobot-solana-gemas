import sqlite3

def init_db():
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            volume REAL,
            tx_count INTEGER,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_token(token):
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tokens (name, price, volume, tx_count, url)
        VALUES (?, ?, ?, ?, ?)
    """, (
        token["name"],
        token["price"],
        token["volume"],
        token["tx_count"],
        token["url"]
    ))
    conn.commit()
    conn.close()

def get_token_count():
    conn = sqlite3.connect("tokens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tokens")
    count = cursor.fetchone()[0]
    conn.close()
    return count