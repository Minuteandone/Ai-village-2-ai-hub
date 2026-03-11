from pathlib import Path

from fastapi.testclient import TestClient

from app import db
from app.main import app


def setup_test_db(tmp_path: Path) -> None:
    db.DB_PATH = tmp_path / "posts.db"
    db.init_db()


def test_create_list_and_vote_posts(tmp_path: Path) -> None:
    setup_test_db(tmp_path)
    client = TestClient(app)

    response = client.post("/api/posts", json={"text": "First post"})
    assert response.status_code == 200
    post = response.json()
    assert post["text"] == "First post"
    assert post["score"] == 0

    vote_response = client.post(f"/api/posts/{post['id']}/vote", json={"delta": 1})
    assert vote_response.status_code == 200
    assert vote_response.json()["score"] == 1

    list_response = client.get("/api/posts")
    assert list_response.status_code == 200
    posts = list_response.json()
    assert len(posts) == 1
    assert posts[0]["score"] == 1


def test_invalid_vote_rejected(tmp_path: Path) -> None:
    setup_test_db(tmp_path)
    client = TestClient(app)

    response = client.post("/api/posts", json={"text": "Hello"})
    post_id = response.json()["id"]

    bad_vote = client.post(f"/api/posts/{post_id}/vote", json={"delta": 3})
    assert bad_vote.status_code == 400
