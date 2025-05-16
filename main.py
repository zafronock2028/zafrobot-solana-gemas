# main.py
from telegram_bot import start_bot
from pump_scanner import start_scanner
from db import init_db

import threading

if __name__ == '__main__':
    # Crea la base de datos automáticamente si no existe
    init_db()

    # Inicia el bot de Telegram en un hilo separado
    threading.Thread(target=start_bot).start()

    # Inicia el escaneo de tokens desde Pump.fun
    start_scanner()