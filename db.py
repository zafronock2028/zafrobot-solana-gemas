# db.py
import sqlite3

def create_table():
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL,
        volume REAL,
        tx_count INTEGER,
        url TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def insert_token(token):
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    try:
        c.execute('''INSERT OR IGNORE INTO tokens 
                  (name, price, volume, tx_count, url)
                  VALUES (?, ?, ?, ?, ?)''',
                  (token['name'], token['price'], 
                   token['volume'], token['tx_count'], token['url']))
        conn.commit()
        return c.rowcount > 0
    finally:
        conn.close()

def get_token_count():
    conn = sqlite3.connect('tokens.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM tokens')
    count = c.fetchone()[0]
    conn.close()
    return count