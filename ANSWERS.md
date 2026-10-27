# Answers, lab 09

Write each answer **before** you run its check. Then run it, and write your points. Do not change an answer after the check: add a line under it with what was wrong.

**Name: Danil Sobar**
**Group: PO 25-Z**
**Date: 27.10.26**

## A1 · Optional, null, required (3)

| Model | `{}` | `{"text": null}` | `{"txt": "hi"}` |
|---|---|---|---|
| PatchA | OK | OK | 422 |
| PatchB | 422 | OK | 422 |
| PatchC | OK | 422 | 422 |

Points: ___ / 3

## A2 · Two validators on one field (4)

| | Status | text after |
|---|---|---|
| (a) | 200 | "hello" (text was not sent, validators do not run on defaults) |
| (b) | 200 | "hi" (stripped) |
| (c) | 500 | "hi" (unchanged). `not_blank` runs first and calls `None.strip()`: AttributeError, not ValueError, so it is not turned into a 422 |
| (d) | 422 | "hi" (unchanged). "text cannot be only spaces" |

Points: ___ / 4

## A3 · Read the traceback (4)

(a) The error is `IndexError: list index out of range`.

(b) It is raised in `Storage.get`, on the line `return self.messages[message_id]`. The list has one element, so only index 0 exists, and `message_id` is 1.

(c) The client gets `500 Internal Server Error`. The traceback stays on the server.

(d) The id is used as a list index. Search by id instead: `next((m for m in self.messages if m.id == message_id), None)`, and if it is `None`, raise a not-found error (404). This also explains why `/messages/0` gives 200 for a message that has id 1.

Points: ___ / 4

## A4 · Routers and addresses (4)

| | Status | Body |
|---|---|---|
| (a) | 404 | `{"detail": "Not Found"}` |
| (b) | 200 | the room: `{"id": 1, "title": "general"}` (prefix `/rooms` + path `/rooms/{room_id}`) |
| (c) | 404 | `{"detail": "Not Found"}` (the `stats` router is never included) |
| (d) | 404 | `{"detail": "Not Found"}` (no route with path `/rooms` in this router) |

Points: ___ / 4

## A5 · Query parameters inside a room (5)

Message ids are global: room 1 has 1, 2, 4, 5; room 2 has 3.

(a) 200, `[4, 1]`: Aida's messages in room 1, newest first.

(b) 200, `[4, 5]`: room 1 is `[1, 2, 4, 5]`, skip 2, take 2.

(c) 200, `[]`: room 2 has one message, skip 1 leaves nothing.

(d) 404: message 3 exists, but in room 2, not in room 1.

(e) 422: `limit=100` is above the allowed maximum (`less than or equal to ...`).

Points: ___ / 5

## B1 · Find the errors: schema and handler (3)

| Line | Corrected line |
|---|---|
| `raise TypeError("text cannot be only spaces")` | `raise ValueError("text cannot be only spaces")` |
| `class RoomNotFound:` | `class RoomNotFound(Exception):` |
| `f"Room {exc.id} not found"` | `f"Room {exc.room_id} not found"` |

Points: ___ / 3

## B2 · Find the errors: a test file (3)

| Line | Corrected line |
|---|---|
| `app.dependency_overrides[get_storage] = Storage()` | `app.dependency_overrides[get_storage] = lambda: store` |
| `response.json["title"]` | `response.json()["title"]` |
| `def check_unknown_room():` | `def test_unknown_room():` |

Points: ___ / 3

## C1 · Lines in order: one storage (2)

Order:

```python
store = Storage()

def get_storage() -> Storage:
    return store

StorageDep = Annotated[Storage, Depends(get_storage)]

@router.get("/{room_id}", response_model=Room)
def get_room(room_id: int, storage: StorageDep) -> Room:
    return storage.get_room(room_id)
```

Points: ___ / 2

## C2 · Lines in order: a test (2)

Order:

```python
def test_created_room_can_be_read():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store

    client.post("/rooms", json={"title": "general"})
    response = client.get("/rooms/1")

    assert response.status_code == 200
    assert response.json()["title"] == "general"
```

Points: ___ / 2

## D1 · UserIn (3)

```python
class UserIn(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=32)]

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("name")
    @classmethod
    def letters_only(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError("name must contain letters only")
        return v
```

Points: ___ / 3

## D2 · GET /rooms with q (3)

```python
@router.get("", response_model=list[Room])
def list_rooms(
    store: StorageDep,
    q: Annotated[str | None, Query(min_length=1, max_length=50)] = None,
) -> list[Room]:
    rooms = store.get_rooms()
    if q is not None:
        rooms = [room for room in rooms if q.lower() in room.title.lower()]
    return rooms
```

Points: ___ / 3

## R1 · model_dump (3)

```
{'text': 'fixed', 'pinned': None}
{'text': 'fixed'}
{}
```

Points: ___ / 3

## R2 · save_room (3)

```python
def save_room(path: str, messages: list[Message]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for m in messages:
            f.write(f"#{m.id} {m.author}: {m.text}\n")
```

Points: ___ / 3

## R3 · count_by_room (4)

```python
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
```

Points: ___ / 4

## Total

**___ / 46**