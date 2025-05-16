# main.py
import os
import time
import threading
from flask import Flask
from dexscreener import scan_tokens
from db import create_table, insert_token
from telegram_bot import send_alert, start_bot

app = Flask(__name__)

@app.route('/')
def home():
    return '🔍 ZafroBot Joyas X100 está activo!'

def scanner_loop():
    create_table()
    while True:
        try:
            tokens = scan_tokens()
            for token in tokens:
                if insert_token(token):
                    send_alert(token)
        except Exception as e:
            print(f"Error en el escaneo: {e}")
        time.sleep(30)

if __name__ == '__main__':
    threading.Thread(target=scanner_loop, daemon=True).start()
    threading.Thread(target=start_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)