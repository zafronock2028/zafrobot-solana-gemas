import sqlite3

def init_db():
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            address TEXT PRIMARY KEY,
            name TEXT,
            timestamp INTEGER
        )
    """)
    conn.commit()
    conn.close()

def guardar_token(address, name, timestamp):
    try:
        conn = sqlite3.connect("tokens.db")
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO tokens (address, name, timestamp) VALUES (?, ?, ?)", (address, name, timestamp))
        conn.commit()
        conn.close()
        print(f"[✅] Guardado en DB: {name} ({address})")
    except Exception as e:
        print(f"[❌] Error guardando token: {e}")

def contar_tokens():
    conn = sqlite3.connect("tokens.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tokens")
    total = c.fetchone()[0]
    conn.close()
    return total