import json
import os

PERSISTENT_MEMORY_FILE = os.path.join(os.path.dirname(__file__), "persistent_memory.json")


def load_persistent_history(path: str = PERSISTENT_MEMORY_FILE) -> list:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_persistent_history(history: list, path: str = PERSISTENT_MEMORY_FILE) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def append_turn(user_input: str, ai_output: str, path: str = PERSISTENT_MEMORY_FILE) -> None:
    history = load_persistent_history(path)
    history.append({"input": user_input, "output": ai_output})
    save_persistent_history(history, path)