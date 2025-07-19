from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message", "")
    reply = f"Echo: {message}"
    return {"reply": reply}
