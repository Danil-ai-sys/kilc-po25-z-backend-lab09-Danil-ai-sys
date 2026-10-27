# C2 · Put the lines in order: write them below, without the letters.
# One line is extra: leave it out.
from fastapi.testclient import TestClient

from app.deps import get_storage
from app.main import app
from app.storage import Storage

client = TestClient(app)


def teardown_function():
    app.dependency_overrides.clear()


def test_created_room_can_be_read():
    store = Storage()
    app.dependency_overrides[get_storage] = lambda: store

    client.post("/rooms", json={"title": "general"})
    response = client.get("/rooms/1")

    assert response.status_code == 200
    assert response.json()["title"] == "general"
