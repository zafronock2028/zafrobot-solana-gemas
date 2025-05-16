# pump_scanner.py
import json
import logging
import websockets
import asyncio
import time
from telegram_bot import send_alert
from db import save_token_if_new

PUMP_WS_URL = "wss://pump.fun/ws"

logging.basicConfig(level=logging.INFO)

def token_filter(data):
    try:
        if (
            data.get("liquidity") and 2000 <= data["liquidity"] <= 75000 and
            data.get("volume") and data["volume"] >= 15000 and
            data.get("holders") and data["holders"] >= 50 and
            data.get("created_at_ms") and
            (int(time.time() * 1000) - data["created_at_ms"]) <= 35 * 60 * 1000
        ):
            return True
    except Exception:
        return False
    return False

async def listen():
    async with websockets.connect(PUMP_WS_URL) as ws:
        logging.info("Conectado al WebSocket de Pump.fun")
        async for message in ws:
            try:
                data = json.loads(message)
                if token_filter(data):
                    url = f"https://pump.fun/{data['token_address']}"
                    token_info = {
                        "name": data.get("name", "Unknown"),
                        "price": float(data.get("price", 0)),
                        "volume": float(data.get("volume", 0)),
                        "tx_count": data.get("tx_count", 0),
                        "url": url
                    }
                    if save_token_if_new(token_info):
                        logging.info(f"Token válido detectado: {token_info['name']}")
                        send_alert(token_info)
            except Exception as e:
                logging.warning(f"Error procesando mensaje: {e}")

def start_scanner():
    asyncio.run(listen())
