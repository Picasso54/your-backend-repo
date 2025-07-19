from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/api-key")
def check_api_key():
    return {"api_key_present": bool(OPENROUTER_API_KEY)}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    if not OPENROUTER_API_KEY:
        return JSONResponse(status_code=500, content={"error": "API key not configured."})

    # Example API call to OpenRouter (modify as per your usage)
    response = requests.post(
        "https://api.openrouter.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": user_message}]
        }
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": reply}
    else:
        return JSONResponse(status_code=500, content={"error": "Failed to fetch from OpenRouter API."})
