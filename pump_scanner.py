import asyncio
import websockets
import json
import time
from utils import obtener_score_rugcheck
from db import guardar_token
from telegram_bot import notificar_gema

async def start_scanner():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"method": "subscribeNewToken"}))

        print("[⏳] Esperando nuevos tokens...")

        async for message in websocket:
            data = json.loads(message)

            if data.get("method") != "newToken":
                continue

            token = data.get("data", {})
            name = token.get("name", "Unknown")
            address = token.get("address")
            liquidity = float(token.get("liquidity", 0))
            volume = float(token.get("volume", 0))
            holders = int(token.get("holders", 0))
            timestamp = int(token.get("created_at", 0))
            age_minutes = (int(time.time()) - timestamp) / 60

            print(f"[+] Detectado: {name} | LP: {liquidity} | Vol: {volume} | Holders: {holders} | Edad: {int(age_minutes)} min")

            # Filtros suaves para pruebas
            if liquidity < 500:
                continue
            if volume < 5000:
                continue
            if holders < 15:
                continue
            if age_minutes > 60:
                continue

            # Verificación RugCheck
            score = await obtener_score_rugcheck(address)
            if score < 50:
                print(f"[⚠️] Rechazado por score bajo ({score})")
                continue

            token_info = {
                "name": name,
                "address": address,
                "liquidity": liquidity,
                "volume": volume,
                "holders": holders,
                "score": score
            }

            # Guardar y notificar
            guardar_token(token_info)
            await notificar_gema(token_info)