# dexscreener.py
import requests
import time
from config import DEXSCREENER_API_URL

def scan_tokens():
    """Consulta Dexscreener y aplica filtros a los tokens"""
    try:
        response = requests.get(DEXSCREENER_API_URL)
        response.raise_for_status()
        return _filter_tokens(response.json())
    except Exception as e:
        print(f"[❌] Error Dexscreener: {e}")
        return []

def _filter_tokens(data):
    """Filtra los tokens según criterios predefinidos"""
    current_time = int(time.time() * 1000)
    valid_tokens = []

    for pair in data.get('pairs', []):
        if pair.get('chainId') != 'solana':
            continue

        pair_created_at = pair.get('pairCreatedAt', 0)
        if (current_time - pair_created_at) > 3 * 24 * 60 * 60 * 1000:  # 3 días en ms
            continue

        volume = float(pair.get('volume', {}).get('h24', 0))
        if volume >= 1_000_000:
            continue

        txns = pair.get('txns', {}).get('h24', {})
        tx_count = txns.get('buys', 0) + txns.get('sells', 0)
        if tx_count < 5000:
            continue

        token = {
            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
            'price': float(pair.get('priceUsd', 0)),
            'volume': volume,
            'tx_count': tx_count,
            'url': pair.get('url', '')
        }

        valid_tokens.append(token)

    return valid_tokens