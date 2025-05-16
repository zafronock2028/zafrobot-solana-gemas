# config.py
import os

def get_env_var(var_name: str, required: bool = True, default=None):
    """Obtiene una variable de entorno y lanza error si no está definida (si es requerida)."""
    value = os.environ.get(var_name, default)
    if required and value is None:
        raise RuntimeError(f"❌ La variable de entorno '{var_name}' no está configurada.")
    return value

# Variables críticas del bot
TELEGRAM_TOKEN = get_env_var("TELEGRAM_TOKEN")
CHAT_ID = get_env_var("CHAT_ID")

# Configuraciones de Dexscreener
DEXSCREENER_API_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"
SCAN_INTERVAL = int(get_env_var("SCAN_INTERVAL", required=False, default=30))  # segundos