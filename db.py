import sqlite3

def init_db():
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens (name TEXT, price REAL, volume REAL, holders INTEGER, url TEXT)''')
    conn.commit()
    conn.close()

def save_token(token):
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute("INSERT INTO tokens VALUES (?, ?, ?, ?, ?)", (
        token['name'],
        token['price'],
        token['volume'],
        token['holders'],
        token['url']
    ))
    conn.commit()
    conn.close()

def get_token_count():
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tokens")
    count = c.fetchone()[0]
    conn.close()
    return count