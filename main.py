# main.py
import threading
import time
import os
from flask import Flask
from dexscreener import get_filtered_tokens
from db import create_table, insert_token
from telegram_bot import send_alert

app = Flask(__name__)

@app.route('/')
def home():
    return '🔍 Bot de detección de gemas Solana en funcionamiento'

def scanner_loop():
    create_table()
    while True:
        try:
            tokens = get_filtered_tokens()
            for token in tokens:
                if insert_token(token):
                    send_alert(token)
        except Exception as e:
            print(f"Error en el escaneo: {e}")
        time.sleep(SCAN_INTERVAL)

if __name__ == '__main__':
    # Iniciar hilos
    threading.Thread(target=scanner_loop, daemon=True).start()
    
    from telegram_bot import start_bot
    threading.Thread(target=start_bot, daemon=True).start()

    # Iniciar servidor web
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)