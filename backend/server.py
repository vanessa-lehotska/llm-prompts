"""Main FastAPI application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import load_config
from handlers import prompt_injection
from models import ChatRequest
from utils.openai_client import get_model_name

config = load_config()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("LLM Security Lab API starting...")
print(f"OpenAI model: {get_model_name()}")

levels_count = len(
    config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
)
print(f"Levels loaded: {levels_count}")


def _get_last_user_message(request: ChatRequest) -> str:
    if request.messages:
        for message in reversed(request.messages):
            if message.role == "user":
                return message.content
        return ""
    return request.user_message or ""


@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint."""

    last_user_msg = _get_last_user_message(request)
    preview = (last_user_msg[:50] + "...") if last_user_msg else ""

    print(f"Level {request.difficulty} | User: {preview}")

    return await prompt_injection.handle_prompt_injection(request, config)


@app.get("/api/levels")
async def get_levels():
    """Return available levels without secrets."""

    levels_data = config.get("modes", {}).get("prompt_injection", {}).get("levels", {})
    levels = []

    for level_id, level_data in levels_data.items():
        levels.append(
            {
                "id": int(level_id),
                "defense": level_data.get("defense", "none"),
            }
        )

    return {"levels": sorted(levels, key=lambda x: x["id"])}


@app.get("/")
async def root():
    return {"message": "LLM Security Lab API is running."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)