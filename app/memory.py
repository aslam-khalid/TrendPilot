import json
import os

MEMORY_FILE = "outputs/memory.json"

def save_to_memory(data: dict):
    os.makedirs("outputs", exist_ok=True)
    history = get_memory()
    history.append(data)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

def get_memory() -> list:
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []