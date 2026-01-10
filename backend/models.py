"""Pydantic models for API requests and responses"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    user_message: str
    difficulty: int
    mode: str = "prompt_injection"


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    level_up: bool = False
    current_level: int
    next_level: Optional[int] = None
    game_completed: bool = False
    defense: Optional[str] = None
    learning: Optional[Dict[str, Any]] = None
