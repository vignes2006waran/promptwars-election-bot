from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are VoteGuide AI — an expert, friendly assistant that helps Indian citizens understand the election process.

You help users with:
- Voter registration (how to register, eligibility, documents needed)
- How to find their polling booth
- How to check their name on the voter list
- What to bring on election day
- How EVMs (Electronic Voting Machines) work
- Understanding candidates and how to research them
- Postal ballot and overseas voting
- Election Commission rules and guidelines
- Rights of voters
- How to report election violations

Rules:
- Always be helpful, clear, and non-partisan
- Never recommend any specific political party or candidate
- Provide accurate information about Indian elections
- If asked in Tamil or Hindi, respond in that language
- Keep responses concise and easy to understand
- Use bullet points and emojis where helpful

Always end responses with an encouraging note about the importance of voting."""

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Build conversation history for Gemini
        chat_history = []
        for msg in req.history[-10:]:  # Last 10 messages for context
            chat_history.append({
                "role": msg["role"],
                "parts": [msg["content"]]
            })

        # Start chat with history
        chat = model.start_chat(history=chat_history)

        # Send message with system context
        full_message = f"{SYSTEM_PROMPT}\n\nUser question: {req.message}"
        if req.history:
            full_message = req.message  # System prompt already set context

        response = chat.send_message(
            req.message if req.history else full_message
        )

        return JSONResponse({"response": response.text})
    except Exception as e:
        return JSONResponse({"response": f"Sorry, I encountered an error. Please try again. ({str(e)})"}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "VoteGuide AI"}
