from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .db import get_connection, init_db
from .schemas import CreatePostRequest, PostResponse, VoteRequest

app = FastAPI(title="Post Voting API", version="1.0.0")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/posts", response_model=list[PostResponse])
def list_posts() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, text, score, created_at FROM posts ORDER BY score DESC, id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


@app.post("/api/posts", response_model=PostResponse)
def create_post(payload: CreatePostRequest) -> dict[str, Any]:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Post text cannot be empty")

    with get_connection() as conn:
        cursor = conn.execute("INSERT INTO posts (text) VALUES (?)", (text,))
        post_id = cursor.lastrowid
        conn.commit()
        row = conn.execute(
            "SELECT id, text, score, created_at FROM posts WHERE id = ?", (post_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=500, detail="Failed to create post")

    return dict(row)


@app.post("/api/posts/{post_id}/vote", response_model=PostResponse)
def vote(post_id: int, payload: VoteRequest) -> dict[str, Any]:
    if payload.delta not in (1, -1):
        raise HTTPException(status_code=400, detail="delta must be 1 or -1")

    with get_connection() as conn:
        existing = conn.execute("SELECT id FROM posts WHERE id = ?", (post_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Post not found")

        conn.execute(
            "UPDATE posts SET score = score + ? WHERE id = ?", (payload.delta, post_id)
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, text, score, created_at FROM posts WHERE id = ?", (post_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=500, detail="Failed to update post")

    return dict(row)
