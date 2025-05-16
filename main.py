# main.py

import os
import time
import threading
from flask import Flask
from config import SCAN_INTERVAL
from dexscreener import scan_tokens
from db import create_table, insert_token
from telegram_bot import telegram_bot  # este importa tu clase actual

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Bot de gemas Solana está corriendo'

def scanner_loop():
    create_table()
    while True:
        try:
            tokens = scan_tokens()
            for token in tokens:
                if insert_token(token):
                    telegram_bot.send_alert(token)
        except Exception as e:
            print(f"❌ Error en escaneo: {e}")
        time.sleep(SCAN_INTERVAL)

if __name__ == '__main__':
    threading.Thread(target=scanner_loop, daemon=True).start()
    threading.Thread(target=telegram_bot.run, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)