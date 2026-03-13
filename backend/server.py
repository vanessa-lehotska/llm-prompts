"""Main FastAPI application - routing and middleware only"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ChatRequest, ComparisonRequest
from config import load_config
from utils.openai_client import get_model_name
from handlers import prompt_injection, promptfoo_integration

# Load configuration
config = load_config()

# Initialize FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup logs
print("LLM Security Lab API starting...")
print(f"OpenAI model: {get_model_name()}")
prompt_injection_levels = len(
    config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
)
print(f"Prompt Injection levels loaded: {prompt_injection_levels}")


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint - routes to appropriate mode handler"""
    print(
        f"Mode: {request.mode} | Level {request.difficulty} | "
        f"User: {request.user_message[:50]}..."
    )
    
    if request.mode == "prompt_injection":
        return await prompt_injection.handle_prompt_injection(request, config)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown mode: {request.mode}"
        )


@app.post("/api/promptfoo")
async def run_promptfoo_tests(request: ComparisonRequest):
    """Run Promptfoo red team tests to compare multiple prompts"""
    print(f"Running Promptfoo tests for {len(request.prompts)} prompts...")
    return await promptfoo_integration.handle_promptfoo_testing(request, config)


@app.get("/api/levels")
async def get_levels():
    """Get available game levels (without exposing secrets)"""
    mode_config = config.get("modes", {}).get("prompt_injection", {})
    levels_data = mode_config.get("levels", {})
    
    levels = []
    for level_id, level_data in levels_data.items():
        levels.append({
            "id": int(level_id),
            "has_system_prompt": bool(level_data.get("systemPrompt", "")),
            "defense": level_data.get("defense", "none")
        })
    
    return {"levels": sorted(levels, key=lambda x: x["id"])}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "LLM Security Lab API is running! Ready for AI security testing."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)