from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import load_config
from handlers.prompt_injection import get_last_user_message, handle_prompt_injection
from llm.openai_client import get_model_name
from models import ChatRequest

load_dotenv()

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


@app.post("/api/chat")
async def chat(request: ChatRequest):
    last_user_msg = get_last_user_message(request)
    preview = (last_user_msg[:50] + "...") if last_user_msg else ""

    print(f"Level {request.difficulty} | User: {preview}")

    return await handle_prompt_injection(request, config)


@app.get("/api/levels")
async def get_levels():
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