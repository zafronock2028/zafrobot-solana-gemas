from telegram_bot import start_bot
from pump_scanner import start_scanner
from db import init_db  # ← Esto es clave

import threading

if __name__ == '__main__':
    init_db()  # ← Esto crea automáticamente tokens.db
    threading.Thread(target=start_bot).start()
    start_scanner()