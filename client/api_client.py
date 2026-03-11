from __future__ import annotations

import requests


class ApiClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def list_posts(self) -> list[dict]:
        response = requests.get(f"{self.base_url}/api/posts", timeout=10)
        response.raise_for_status()
        return response.json()

    def create_post(self, text: str) -> dict:
        response = requests.post(
            f"{self.base_url}/api/posts", json={"text": text}, timeout=10
        )
        response.raise_for_status()
        return response.json()

    def vote(self, post_id: int, delta: int) -> dict:
        response = requests.post(
            f"{self.base_url}/api/posts/{post_id}/vote", json={"delta": delta}, timeout=10
        )
        response.raise_for_status()
        return response.json()
