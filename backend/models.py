"""Pydantic models for API requests and responses"""

from typing import List, Optional

from pydantic import BaseModel, model_validator


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for single-turn and multi-turn chat."""

    difficulty: int
    user_message: Optional[str] = None
    messages: Optional[List[Message]] = None

    @model_validator(mode="after")
    def validate_payload(self):
        if not self.user_message and not self.messages:
            raise ValueError("Either 'user_message' or 'messages' must be provided.")
        return self


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str
    level_up: bool = False
    current_level: int
    next_level: Optional[int] = None
    game_completed: bool = False
    defense: Optional[str] = None