# 🗳️ VoteGuide AI — Election Process Education Chatbot

> An AI-powered assistant that helps Indian citizens understand the election process, built for Virtual: PromptWars by Team Nova Coders.

## 🎯 Challenge Vertical
**Election Process Education**

## 🚀 Live Demo
[Deployed on Render](https://your-app.onrender.com) *(replace with your URL)*

---

## 💡 Approach & Logic

VoteGuide AI is a conversational chatbot that educates Indian citizens about the democratic process. The assistant uses Google's Gemini AI to provide accurate, non-partisan information about:

- Voter registration process
- Finding polling booths
- Documents required on election day
- How EVMs (Electronic Voting Machines) work
- Checking name on voter list
- Understanding NOTA
- Voter rights and how to report violations

The bot supports **English, Tamil, and Hindi** to serve a diverse Indian population.

---

## 🛠️ How It Works

1. User types a question about elections in the chat interface
2. FastAPI backend receives the message
3. Gemini 1.5 Flash processes it with a carefully crafted system prompt ensuring non-partisan, accurate responses
4. Response is streamed back to the frontend
5. Full conversation history is maintained for context-aware responses

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript (single file) |
| Backend | FastAPI (Python) |
| AI Model | Google Gemini 1.5 Flash |
| Deployment | Render / Google Cloud Run |

## 🔑 Google Services Used
- **Google Gemini API** — Core AI intelligence via Google AI Studio

---

## 📁 Project Structure

```
promptwars-election-bot/
├── main.py          # FastAPI backend
├── index.html       # Frontend chat UI
├── requirements.txt # Python dependencies
├── Dockerfile       # Container config
└── README.md        # This file
```

---

## ⚙️ Local Setup

```bash
# Clone the repo
git clone https://github.com/vignes2006waran/promptwars-election-bot
cd promptwars-election-bot

# Install dependencies
pip install -r requirements.txt

# Set your Gemini API key
export GEMINI_API_KEY=your_key_here

# Run the app
uvicorn main:app --reload

# Open http://localhost:8000
```

---

## 🧠 Assumptions Made

- Target audience is Indian voters (18+)
- Information is based on Election Commission of India guidelines
- The bot deliberately avoids political bias or party recommendations
- Multilingual support covers the top 3 languages by user base

---

## 👨‍💻 Team
**Code Cracks** — SRM Madurai College for Engineering and Technology

---

## 📊 Evaluation Criteria Coverage

| Criteria | Implementation |
|----------|---------------|
| Code Quality | Clean separation of concerns, typed models, error handling |
| Security | API key via environment variables, input validation |
| Efficiency | Gemini Flash model (fastest), limited history window |
| Testing | /health endpoint, error fallbacks |
| Accessibility | Keyboard navigation, multilingual support, responsive design |
| Google Services | Gemini 1.5 Flash API integration |
