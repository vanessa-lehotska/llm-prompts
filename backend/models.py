"""Pydantic models for API requests and responses"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List


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


class AttackResult(BaseModel):
    """Result of a single attack"""
    category: str
    attack: str
    response: str
    success: bool
    reason: str


class PromptConfig(BaseModel):
    """Configuration for a single prompt in comparison mode"""
    name: str
    content: str


class ComparisonRequest(BaseModel):
    """Request model for prompt comparison endpoint"""
    prompts: List[PromptConfig]
    secret: str = "TEST_SECRET"
    mode: str = "prompt_comparison"


class PromptComparisonResult(BaseModel):
    """Result for a single prompt in comparison mode"""
    prompt_name: str
    prompt_content: str
    total_attacks: int
    successful_attacks: int
    failed_attacks: int
    attack_success_rate: float
    category_stats: Dict[str, Dict[str, Any]]
    results: List[AttackResult]


class ComparisonResponse(BaseModel):
    """Response model for prompt comparison endpoint"""
    comparisons: List[PromptComparisonResult]
    best_prompt: str
    summary: Dict[str, Any]
