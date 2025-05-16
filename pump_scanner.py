import json
import asyncio
import websockets
from config import PUMPFUN_WS_URL
from telegram_bot import send_alert
from db import save_token

def is_valid_token(data):
    try:
        price = float(data.get("priceUsd", 0))
        volume = float(data.get("volume24h", 0))
        tx_count = int(data.get("txCount", 0))
        age = int(data.get("age", 0))
        holders = int(data.get("holders", 0))
        market_cap = float(data.get("marketCap", 0))
        if (
            2000 <= volume <= 75000 and
            50 <= holders and
            age <= 2100 and
            3000 <= market_cap <= 80000
        ):
            return True
        return False
    except:
        return False

async def scan_tokens():
    async with websockets.connect(PUMPFUN_WS_URL) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)

            if isinstance(data, dict) and data.get("type") == "new_token":
                token = data.get("token", {})
                if is_valid_token(token):
                    save_token(token)
                    send_alert({
                        "name": token.get("name", "Unknown"),
                        "price": float(token.get("priceUsd", 0)),
                        "volume": float(token.get("volume24h", 0)),
                        "tx_count": int(token.get("txCount", 0)),
                        "url": f"https://dexscreener.com/solana/{token.get('address')}"
                    })

def start_scanner():
    asyncio.run(scan_tokens())