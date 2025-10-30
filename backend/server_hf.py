import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


# ChatRequest model
class ChatRequest(BaseModel):
    user_message: str
    difficulty: int


app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load game configuration
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"levels": {}}

config = load_config()

# Load GPT-2 model locally (124M parameters)
print("🤖 Loading GPT-2 model locally... (will download ~500MB on first run)")
print("📚 This is the smallest GPT-2 with 124M parameters")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")  # Shorter name works too
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Set pad token for generation
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("✅ GPT-2 model loaded successfully!")

# Thread pool for model inference
executor = ThreadPoolExecutor(max_workers=1)

def generate_local_response(prompt: str) -> str:
    """Generate response using local GPT-2 model"""
    try:
        # Tokenize input
        inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=50,
                temperature=0.8,
                do_sample=True,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.eos_token_id,
                eos_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=2
            )
        
        # Decode and clean response
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove original prompt from response
        if prompt in generated_text:
            response = generated_text.replace(prompt, "").strip()
        else:
            response = generated_text.strip()
        
        # Clean up repetitive patterns
        if "Assistant:" in response:
            # Take only the first Assistant response
            parts = response.split("Assistant:")
            if len(parts) > 1:
                response = parts[1].strip()
        
        # Remove repetitive text patterns
        lines = response.split('\n')
        if len(lines) > 1:
            response = lines[0].strip()  # Take only first line
            
        return response if response else "I'm processing your request..."
        
    except Exception as e:
        return f"❌ Model error: {str(e)}"

async def call_local_model(message: str, system_prompt: str = "") -> str:
    """Call local GPT-2 model with async wrapper"""
    
    # Combine system prompt with user message
    if system_prompt:
        full_prompt = f"{system_prompt}\n\nHuman: {message}\nAssistant:"
    else:
        full_prompt = f"Human: {message}\nAssistant:"
    
    # Run model in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(executor, generate_local_response, full_prompt)
    
    return response

@app.get("/")
async def root():
    return {"message": "Echoes of Astra API with LOCAL GPT-2 model! 🚀"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Handle chat requests with game level system prompts"""
    
    try:
        # Get system prompt for the current difficulty level
        level_config = config.get("levels", {}).get(str(request.difficulty), {})
        system_prompt = level_config.get("systemPrompt", "")
        
        print(f"Processing request for level {request.difficulty}")
        print(f"System prompt: {system_prompt[:100]}..." if system_prompt else "No system prompt")
        print(f"User message: {request.user_message}")
        
        # Call local GPT-2 model
        response = await call_local_model(request.user_message, system_prompt)
        
        return {
            "response": response,
            "level": request.difficulty,
            "success": True
        }
        
    except Exception as e:
        print(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/levels")
async def get_levels():
    """Get available game levels"""
    levels = []
    for level_id, level_data in config.get("levels", {}).items():
        levels.append({
            "id": int(level_id),
            "secret": level_data.get("secret", "Unknown"),
            "hasPrompt": bool(level_data.get("systemPrompt", ""))
        })
    
    return {"levels": levels}

if __name__ == "__main__":
    print("🚀 Starting Echoes of Astra with LOCAL GPT-2!")
    print("🔄 No internet required after model download")
    print("� Model runs completely offline")
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
