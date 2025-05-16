import threading
import asyncio
from flask import Flask
from pump_scanner import start_scanner
from telegram_bot import run_bot
from db import init_db

app = Flask(__name__)

@app.route('/')
def home():
    return "ZafroBot Joyas X100 está activo."

if __name__ == '__main__':
    init_db()
    threading.Thread(target=run_bot).start()
    threading.Thread(target=lambda: asyncio.run(start_scanner())).start()
    app.run(host='0.0.0.0', port=10000)