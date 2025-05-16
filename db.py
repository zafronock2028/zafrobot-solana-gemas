# db.py
import sqlite3

DB_NAME = 'tokens.db'

def create_table():
    """Crea la tabla de tokens si no existe."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    volume REAL,
                    tx_count INTEGER,
                    url TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    except Exception as e:
        print(f"[❌] Error al crear la tabla: {e}")

def insert_token(token: dict) -> bool:
    """Intenta insertar un token. Retorna True si fue insertado, False si ya existía."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO tokens (name, price, volume, tx_count, url)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                token['name'],
                token['price'],
                token['volume'],
                token['tx_count'],
                token['url']
            ))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"[❌] Error al insertar token: {e}")
        return False

def get_token_count() -> int:
    """Retorna la cantidad total de tokens almacenados."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM tokens')
            count = cursor.fetchone()[0]
            return count
    except Exception as e:
        print(f"[❌] Error al contar tokens: {e}")
        return 0