# main.py

import os
import time
import threading
from flask import Flask
from config import SCAN_INTERVAL
from dexscreener import scan_tokens
from db import create_table, insert_token
from telegram_bot import send_alert, start_bot  # Importa las funciones correctas

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot de gemas Solana corriendo...'

def scanner_loop():
    create_table()
    while True:
        try:
            tokens = scan_tokens()
            for token in tokens:
                if insert_token(token):
                    send_alert(token)
        except Exception as e:
            print(f"❌ Error en escaneo: {e}")
        time.sleep(SCAN_INTERVAL)

if __name__ == '__main__':
    # Hilo 1: escaneo de tokens
    threading.Thread(target=scanner_loop, daemon=True).start()

    # Hilo 2: comandos de Telegram
    threading.Thread(target=start_bot, daemon=True).start()

    # Hilo 3: servidor web para Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)