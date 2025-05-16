# main.py
import threading
import logging
from telegram_bot import start_bot
from pump_scanner import start_scanner

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    threading.Thread(target=start_scanner).start()