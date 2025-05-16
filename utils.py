import requests

async def obtener_score_rugcheck(address):
    try:
        url = f"https://api.rugcheck.xyz/api/token/{address}"
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            score = data.get("score", 0)
            return score if isinstance(score, (int, float)) else 0
        else:
            print(f"[⚠️] Error en RugCheck: {response.status_code}")
            return 0
    except Exception as e:
        print(f"[❌] Error en obtener_score_rugcheck: {e}")
        return 0