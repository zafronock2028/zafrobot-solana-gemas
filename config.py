import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN no está configurado")
if not CHAT_ID:
    raise ValueError("❌ CHAT_ID no está configurado")

DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"
SCAN_INTERVAL = 30