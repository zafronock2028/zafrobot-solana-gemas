# db.py
import json
import os

DB_FILE = "tokens.json"

def load_tokens():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_tokens(tokens):
    with open(DB_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

def get_token_count():
    return len(load_tokens())

def save_token_if_new(token):
    tokens = load_tokens()
    if not any(t["url"] == token["url"] for t in tokens):
        tokens.append(token)
        save_tokens(tokens)
        return True
    return False