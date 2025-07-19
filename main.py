from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": message}]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        result = response.json()

        if "error" in result:
            return {"reply": f"⚠️ OpenRouter Error: {result['error']}"}

        reply = result["choices"][0]["message"]["content"]
        return {"reply": reply}

    except Exception as e:
        return {"reply": f"⚠️ Backend Exception: {str(e)}"}
