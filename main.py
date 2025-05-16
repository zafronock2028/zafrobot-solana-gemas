from telegram_bot import start_bot
from pump_scanner import start_scanner
import threading

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    start_scanner()