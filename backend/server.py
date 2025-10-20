from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True) 

app = FastAPI()

# OpenAI configuration
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Default to gpt-4o-mini

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Load prompts/config from config.json (levels -> systemPrompt)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
else:
    config = {"level": {}}

# Basic startup logs (sanitized)
print("[startup] OpenAI model:", openai_model)
print("[startup] API key length:", len(openai_api_key) if openai_api_key else 0)

# Minimal request model for chat
class ChatRequest(BaseModel):
    user_message: str
    difficulty: int

def call_openai_api(messages):
    """Call OpenAI API using the official SDK"""
    try:
        response = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "error": "OpenAI API error",
            "message": str(e)
        })
@app.post("/api/chat")
async def chat(request: ChatRequest):
    print("[chat] difficulty=", request.difficulty, "user_message_len=", len(request.user_message or ""))
    
    # Get system prompt from config based on difficulty
    level_key = str(request.difficulty)
    if level_key not in config.get("level", {}):
        raise HTTPException(status_code=400, detail=f"Invalid difficulty level: {request.difficulty}")
    
    level_config = config["level"][level_key]
    system_prompt = level_config.get("systemPrompt", "")
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.user_message},
    ]

    response = call_openai_api(messages)
    try:
        content = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid response from model: {str(e)}")

    return {"response": content}

# Start the server via `python server.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
 
