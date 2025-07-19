from fastapi import FastAPI
import os

app = FastAPI()

# Fetching the API Key from environment variables
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.get("/api-key")
def get_api_key():
    if OPENROUTER_API_KEY:
        return {"api_key_present": True}
    return {"api_key_present": False}
