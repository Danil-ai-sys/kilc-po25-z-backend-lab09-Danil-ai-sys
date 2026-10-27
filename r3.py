# R3 · Read a folder of JSON files, from control work 1. See the slide.
import json
import os


def count_by_room(folder: str) -> dict[int, int]:
    counts: dict[int, int] = {}
    for name in os.listdir(folder):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            rows = json.load(f)
        for row in rows:
            room = row["room_id"]
            counts[room] = counts.get(room, 0) + 1
    return counts
