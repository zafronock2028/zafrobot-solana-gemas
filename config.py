# config.py (versión corregida)
import os

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('CHAT_ID', '')
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"
SCAN_INTERVAL = 30