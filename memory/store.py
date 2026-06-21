import json
from datetime import datetime
from pathlib import Path


MEMORY_FILE = Path("memory/research_memory.json")


def save_memory(data):
    MEMORY_FILE.parent.mkdir(exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

    if MEMORY_FILE.exists():
        existing = json.loads(MEMORY_FILE.read_text())
    else:
        existing = []

    existing.append(record)

    MEMORY_FILE.write_text(json.dumps(existing, indent=2))


def load_memory():
    if not MEMORY_FILE.exists():
        return []

    return json.loads(MEMORY_FILE.read_text())
