import asyncio
import websockets
import json
import time
from config import MIN_LIQUIDITY, MAX_LIQUIDITY, MIN_VOLUME, MIN_HOLDERS, MAX_AGE_MINUTES
from db import save_token
from telegram_bot import send_alert

async def start_scanner():
    uri = "wss://pumpportal.fun/api/data"

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"method": "subscribeNewToken"}))

        print("[LOG] Suscrito a Pump.fun")

        async for message in websocket:
            try:
                data = json.loads(message)

                if data.get("method") != "newToken":
                    continue

                token = data.get("data", {})
                liquidity = token.get("liquidity", 0)
                volume = token.get("volume", 0)
                holders = token.get("holders", 0)
                created_at = token.get("createdAt", int(time.time()))
                age_minutes = (int(time.time()) - int(created_at)) / 60

                if not (MIN_LIQUIDITY <= liquidity <= MAX_LIQUIDITY):
                    continue
                if volume < MIN_VOLUME:
                    continue
                if holders < MIN_HOLDERS:
                    continue
                if age_minutes > MAX_AGE_MINUTES:
                    continue

                token_data = {
                    "name": token.get("name", "Unknown"),
                    "price": token.get("price", 0),
                    "volume": volume,
                    "holders": holders,
                    "url": f"https://pump.fun/{token.get('id')}"
                }

                save_token(token_data)
                send_alert(token_data)

                print(f"[JOYITA] {token_data['name']} - Holders: {holders} - ${token_data['price']}")
            except Exception as e:
                print(f"[ERROR] {e}")