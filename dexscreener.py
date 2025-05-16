# dexscreener.py
import requests
import time
from config import DEXSCREENER_API_URL

def scan_tokens():
    """Consulta Dexscreener y aplica filtros pro a los tokens"""
    try:
        response = requests.get(DEXSCREENER_API_URL)
        response.raise_for_status()
        return _filter_tokens(response.json())
    except Exception as e:
        print(f"[❌] Error Dexscreener: {e}")
        return []

def _filter_tokens(data):
    """Filtra tokens tipo gema en Solana con lógica avanzada"""
    current_time = int(time.time() * 1000)
    valid_tokens = []

    for pair in data.get('pairs', []):
        if pair.get('chainId') != 'solana':
            continue

        age_ms = current_time - pair.get('pairCreatedAt', 0)
        if age_ms > 60 * 60 * 1000:  # Máximo 60 minutos de creados
            continue

        volume = float(pair.get('volume', {}).get('h24', 0))
        if not (5000 <= volume <= 100000):  # Volumen entre $5K y $100K
            continue

        txns = pair.get('txns', {}).get('h24', {})
        tx_count = txns.get('buys', 0) + txns.get('sells', 0)
        if tx_count < 15:
            continue

        base = pair.get('baseToken', {})
        name = base.get('name', 'Unknown')
        url = pair.get('url', '')
        price = float(pair.get('priceUsd', 0))

        token = {
            'name': name,
            'price': price,
            'volume': volume,
            'tx_count': tx_count,
            'url': url
        }

        valid_tokens.append(token)

    return valid_tokens