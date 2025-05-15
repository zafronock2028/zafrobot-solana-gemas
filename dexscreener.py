# dexscreener.py
import requests
import time

def get_filtered_tokens():
    current_time_ms = int(time.time() * 1000)
    max_age_ms = 3 * 24 * 60 * 60 * 1000  # 3 días en milisegundos
    max_volume = 1000000
    min_tx_count = 5000

    try:
        response = requests.get(DEXSCREENER_API_URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    filtered_tokens = []
    for pair in data.get('pairs', []):
        if pair.get('chainId') != 'solana':
            continue

        created_at = pair.get('pairCreatedAt', 0)
        if (current_time_ms - created_at) > max_age_ms:
            continue

        volume = float(pair.get('volume', {}).get('h24', 0))
        if volume >= max_volume:
            continue

        tx_data = pair.get('txns', {}).get('h24', {})
        tx_count = tx_data.get('buys', 0) + tx_data.get('sells', 0)
        if tx_count < min_tx_count:
            continue

        filtered_tokens.append({
            'name': pair.get('baseToken', {}).get('name', 'Unknown'),
            'price': pair.get('priceUsd', 0),
            'volume': volume,
            'tx_count': tx_count,
            'url': pair.get('url', '')
        })

    return filtered_tokens