# config.py
import os

# Configuración esencial desde variables de entorno
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
CHAT_ID = os.environ.get('CHAT_ID', '')

# Configuración de Dexscreener
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"

# Intervalo de escaneo en segundos
SCAN_INTERVAL = 30

# Validación básica de configuración
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN no está configurado en las variables de entorno")

if not CHAT_ID:
    raise ValueError("❌ CHAT_ID no está configurado en las variables de entorno")