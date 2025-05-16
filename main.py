# main.py
import threading
import time
import os
from flask import Flask
from dexscreener import scan_tokens
from db import create_table, insert_token
from telegram_bot import TelegramBot

app = Flask(__name__)

@app.route('/')
def home():
    return '🔍 Bot Solana Gem Scanner - Online'

def scanner_loop():
    create_table()
    while True:
        try:
            tokens = scan_tokens()
            for token in tokens:
                if insert_token(token):
                    TelegramBot().send_alert(token)
        except Exception as e:
            print(f"Error en scanner: {e}")
        time.sleep(30)

if __name__ == '__main__':
    # Iniciar componentes
    threading.Thread(target=scanner_loop, daemon=True).start()
    threading.Thread(target=TelegramBot().run, daemon=True).start()
    
    # Servidor web
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)