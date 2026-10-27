# R2 · Write a text file, from control work 1. See the slide.
from app.models import Message


def save_room(path: str, messages: list[Message]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for m in messages:
            f.write(f"#{m.id} {m.author}: {m.text}\n")
