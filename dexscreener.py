# dexscreener.py
import requests
import time
from config import DEXSCREENER_API_URL, SCAN_INTERVAL

def scan_tokens():
    try:
        response = requests.get(DEXSCREENER_API_URL)
        response.raise_for_status()
        return _filter_tokens(response.json())
    except Exception as e:
        print(f"Error Dexscreener: {e}")
        return []

def _filter_tokens(data):
    current_time = int(time.time() * 1000)
    valid_tokens = []
    
    for pair in data.get('pairs', []):
        if pair.get('chainId') != 'solana':
            continue
            
        if (current_time - pair.get('pairCreatedAt', 0)) > 259200000:  # 3 días
            continue
            
        volume = pair.get('volume', {}).get('h24', 0)
        if volume >= 1000000:
            continue
            
        tx_count = pair.get('txns', {}).get('h24', {}).get('buys', 0) + \
                 pair.get('txns', {}).get('h24', {}).get('sells', 0)
        
        if tx_count >= 5000:
            valid_tokens.append({
                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                'price': pair.get('priceUsd', 0),
                'volume': volume,
                'tx_count': tx_count,
                'url': pair.get('url', '')
            })
    
    return valid_tokens