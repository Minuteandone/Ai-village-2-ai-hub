from pydantic import BaseModel, Field


class CreatePostRequest(BaseModel):
    text: str = Field(min_length=1, max_length=500)


class VoteRequest(BaseModel):
    delta: int


class PostResponse(BaseModel):
    id: int
    text: str
    score: int
    created_at: str
