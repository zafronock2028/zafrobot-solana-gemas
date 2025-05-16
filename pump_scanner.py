# pump_scanner.py
import asyncio
import websockets
import json
import time
from telegram_bot import send_alert
from db import save_token

# Filtros de validación
MIN_LIQUIDITY = 2000
MAX_LIQUIDITY = 75000
MIN_VOLUME = 15000
MIN_HOLDERS = 50
MAX_AGE_MINUTES = 35

def is_valid_token(token):
    try:
        liquidity = float(token.get("liquidity", 0))
        volume = float(token.get("volume", 0))
        holders = int(token.get("holders", 0))
        created_at = int(token.get("created_at", time.time() * 1000))
        age_minutes = (int(time.time() * 1000) - created_at) / 60000

        if (
            MIN_LIQUIDITY <= liquidity <= MAX_LIQUIDITY and
            volume >= MIN_VOLUME and
            holders >= MIN_HOLDERS and
            age_minutes <= MAX_AGE_MINUTES
        ):
            return True
    except Exception as e:
        print(f"[❌] Error al validar token: {e}")
    return False

async def start_scanner():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({ "method": "subscribeNewToken" }))
        print("[✅] Conectado al WebSocket de Pump.fun")

        async for message in websocket:
            data = json.loads(message)
            if data.get("method") == "newToken":
                token = data.get("data", {})
                if is_valid_token(token):
                    print(f"[🚀] Joya detectada: {token.get('name')}")
                    save_token(token)
                    send_alert({
                        "name": token.get("name", "Unknown"),
                        "price": token.get("price", 0),
                        "volume": token.get("volume", 0),
                        "tx_count": token.get("txCount", 0),
                        "url": token.get("url", "https://pump.fun")
                    })
                else:
                    print(f"[⛔] Token descartado: {token.get('name')}")