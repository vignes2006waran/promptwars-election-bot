from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are VoteGuide AI — an expert, friendly assistant that helps Indian citizens understand the election process.

You help users with:
- Voter registration (how to register, eligibility, documents needed)
- How to find their polling booth
- How to check their name on the voter list
- What to bring on election day
- How EVMs (Electronic Voting Machines) work
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
- Always end with an encouraging note about the importance of voting."""

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>VoteGuide AI</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"/>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Inter',sans-serif;background:#fff;color:#0d0d0d;display:flex;height:100vh;overflow:hidden}
    .sidebar{width:260px;background:#f9f9f9;border-right:1px solid #e5e5e5;display:flex;flex-direction:column;flex-shrink:0;padding:12px}
    .sidebar-header{display:flex;align-items:center;gap:10px;padding:10px 8px 16px}
    .sidebar-logo{width:32px;height:32px;background:linear-gradient(135deg,#ff9933,#138808);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px}
    .sidebar-title{font-size:15px;font-weight:600;color:#0d0d0d}
    .new-chat-btn{display:flex;align-items:center;gap:8px;padding:10px 12px;border-radius:8px;border:1px solid #e5e5e5;background:#fff;cursor:pointer;font-size:14px;color:#0d0d0d;font-family:'Inter',sans-serif;width:100%;transition:background .15s}
    .new-chat-btn:hover{background:#f0f0f0}
    .sidebar-divider{height:1px;background:#e5e5e5;margin:12px 0}
    .sidebar-label{font-size:11px;color:#8e8ea0;font-weight:500;padding:0 8px;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em}
    .quick-list{display:flex;flex-direction:column;gap:2px}
    .quick-item{padding:8px 12px;border-radius:8px;font-size:13px;color:#444;cursor:pointer;transition:background .15s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;border:none;background:transparent;width:100%;text-align:left;font-family:'Inter',sans-serif}
    .quick-item:hover{background:#ececec;color:#0d0d0d}
    .sidebar-footer{margin-top:auto;padding-top:12px;border-top:1px solid #e5e5e5}
    .lang-section{padding:8px}
    .lang-label{font-size:11px;color:#8e8ea0;margin-bottom:6px;text-transform:uppercase;letter-spacing:.05em;font-weight:500}
    .lang-btns{display:flex;gap:6px}
    .lang-btn{flex:1;padding:6px 4px;border-radius:6px;border:1px solid #e5e5e5;background:#fff;font-size:12px;cursor:pointer;font-family:'Inter',sans-serif;color:#444;transition:all .15s;text-align:center}
    .lang-btn.active{background:#0d0d0d;color:#fff;border-color:#0d0d0d}
    .lang-btn:hover:not(.active){background:#f0f0f0}
    .main{flex:1;display:flex;flex-direction:column;overflow:hidden}
    .topbar{padding:14px 20px;border-bottom:1px solid #e5e5e5;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
    .topbar-title{font-size:15px;font-weight:500;color:#0d0d0d}
    .topbar-badge{display:flex;align-items:center;gap:5px;font-size:12px;color:#22c55e;background:#f0fdf4;border:1px solid #bbf7d0;padding:3px 10px;border-radius:999px}
    .badge-dot{width:6px;height:6px;border-radius:50%;background:#22c55e;animation:pulse 2s infinite}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
    #chat{flex:1;overflow-y:auto;padding:0;display:flex;flex-direction:column;scroll-behavior:smooth}
    #chat::-webkit-scrollbar{width:6px}
    #chat::-webkit-scrollbar-thumb{background:#e5e5e5;border-radius:3px}
    .welcome{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;padding:40px 20px;text-align:center;gap:16px}
    .welcome-icon{font-size:52px}
    .welcome h2{font-size:26px;font-weight:600;color:#0d0d0d}
    .welcome p{font-size:14px;color:#8e8ea0;max-width:400px;line-height:1.6}
    .welcome-chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:8px;max-width:500px}
    .welcome-chip{padding:8px 16px;border-radius:999px;border:1px solid #e5e5e5;background:#fff;font-size:13px;color:#444;cursor:pointer;transition:all .15s;font-family:'Inter',sans-serif}
    .welcome-chip:hover{border-color:#0d0d0d;color:#0d0d0d;background:#f9f9f9}
    .msg-row{padding:16px 20px;display:flex;gap:14px;animation:fadeUp .25s ease}
    @keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
    .msg-row.user{background:#fff}
    .msg-row.bot{background:#f9f9f9}
    .msg-avatar{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0;margin-top:2px}
    .msg-row.user .msg-avatar{background:#0d0d0d;color:#fff;font-size:13px;font-weight:600}
    .msg-row.bot .msg-avatar{background:linear-gradient(135deg,#ff9933,#138808);font-size:15px}
    .msg-content{flex:1;max-width:680px}
    .msg-name{font-size:13px;font-weight:600;margin-bottom:6px;color:#0d0d0d}
    .msg-text{font-size:14px;line-height:1.75;color:#0d0d0d}
    .msg-text strong{font-weight:600}
    .msg-text ul{padding-left:20px;margin:6px 0}
    .msg-text li{margin:3px 0}
    .typing-dots{display:flex;gap:4px;align-items:center;padding:4px 0}
    .typing-dot{width:7px;height:7px;border-radius:50%;background:#c5c5c5;animation:bounce 1.2s infinite}
    .typing-dot:nth-child(2){animation-delay:.2s}
    .typing-dot:nth-child(3){animation-delay:.4s}
    @keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}
    .input-area{padding:16px 20px 20px;flex-shrink:0;border-top:1px solid #e5e5e5;background:#fff}
    .input-box{display:flex;align-items:flex-end;gap:10px;background:#fff;border:1px solid #e5e5e5;border-radius:14px;padding:12px 16px;box-shadow:0 2px 8px rgba(0,0,0,.06);transition:border-color .2s,box-shadow .2s}
    .input-box:focus-within{border-color:#0d0d0d;box-shadow:0 2px 12px rgba(0,0,0,.1)}
    #userInput{flex:1;border:none;outline:none;font-family:'Inter',sans-serif;font-size:14px;color:#0d0d0d;resize:none;max-height:120px;min-height:22px;line-height:1.5;background:transparent}
    #userInput::placeholder{color:#c5c5c5}
    #sendBtn{width:34px;height:34px;border-radius:8px;background:#0d0d0d;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .15s}
    #sendBtn:hover{background:#333;transform:scale(1.05)}
    #sendBtn:disabled{opacity:.3;cursor:not-allowed;transform:none}
    #sendBtn svg{width:16px;height:16px;fill:#fff}
    .input-hint{text-align:center;font-size:11px;color:#c5c5c5;margin-top:8px}
    .tricolor{height:3px;background:linear-gradient(90deg,#ff9933 33%,#fff 33%,#fff 66%,#138808 66%);flex-shrink:0}
    @media(max-width:600px){.sidebar{display:none}.msg-row{padding:12px 16px}}
  </style>
</head>
<body>
<div class="sidebar">
  <div class="sidebar-header">
    <div class="sidebar-logo">🗳️</div>
    <div class="sidebar-title">VoteGuide AI</div>
  </div>
  <button class="new-chat-btn" onclick="newChat()">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
    New Chat
  </button>
  <div class="sidebar-divider"></div>
  <div class="sidebar-label">Quick Topics</div>
  <div class="quick-list">
    <button class="quick-item" type="button" onclick="askQuick('How do I register as a voter in India?')">📝 Voter Registration</button>
    <button class="quick-item" type="button" onclick="askQuick('How to find my polling booth?')">📍 Find Polling Booth</button>
    <button class="quick-item" type="button" onclick="askQuick('What documents do I need on election day?')">📄 Documents Needed</button>
    <button class="quick-item" type="button" onclick="askQuick('How does the EVM machine work?')">🖥️ How EVM Works</button>
    <button class="quick-item" type="button" onclick="askQuick('How to check my name in voter list?')">🔍 Check Voter List</button>
    <button class="quick-item" type="button" onclick="askQuick('What is NOTA and how to use it?')">❓ What is NOTA?</button>
    <button class="quick-item" type="button" onclick="askQuick('What are my rights as a voter?')">⚖️ Voter Rights</button>
  </div>
  <div class="sidebar-footer">
    <div class="lang-section">
      <div class="lang-label">Language</div>
      <div class="lang-btns">
        <button class="lang-btn active" onclick="setLang('en',this)">EN</button>
        <button class="lang-btn" onclick="setLang('ta',this)">தமிழ்</button>
        <button class="lang-btn" onclick="setLang('hi',this)">हिंदी</button>
      </div>
    </div>
  </div>
</div>
<div class="main">
  <div class="tricolor"></div>
  <div class="topbar">
    <div class="topbar-title">Election Process Education</div>
    <div class="topbar-badge"><div class="badge-dot"></div>Gemini Powered</div>
  </div>
  <div id="chat">
    <div class="welcome" id="welcome">
      <div class="welcome-icon" style="font-size:52px;margin-bottom:8px;">🗳️</div>
      <h2>How can I help you today?</h2>
      <p>Ask me anything about the Indian election process — voter registration, polling booths, EVMs, voter rights, and more.</p>
      <div class="welcome-chips">
        <button class="welcome-chip" type="button" onclick="askQuick('How do I register as a voter?')">How do I register as a voter?</button>
        <button class="welcome-chip" type="button" onclick="askQuick('What is the voting age in India?')">What is the voting age?</button>
        <button class="welcome-chip" type="button" onclick="askQuick('How does EVM work?')">How does EVM work?</button>
        <button class="welcome-chip" type="button" onclick="askQuick('What documents do I need on election day?')">Documents needed for voting</button>
      </div>
    </div>
  </div>
  <div class="input-area">
    <div class="input-box">
      <textarea id="userInput" placeholder="Ask about elections, voting process, voter rights..." rows="1"></textarea>
      <button id="sendBtn" onclick="sendMessage()">
        <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
      </button>
    </div>
    <p class="input-hint">VoteGuide AI · Non-partisan election education · Press Enter to send</p>
  </div>
</div>
<script>
  var chatHistory=[];
  var currentLang='en';
  var langPrompts={en:'',ta:'Please respond in Tamil language. ',hi:'Please respond in Hindi language. '};
  function setLang(lang,btn){
    currentLang=lang;
    document.querySelectorAll('.lang-btn').forEach(function(b){b.classList.remove('active')});
    btn.classList.add('active');
  }
  function newChat(){
    chatHistory=[];
    var chat=document.getElementById('chat');
    chat.innerHTML='<div class="welcome" id="welcome"><div class="welcome-icon">🗳️</div><h2>How can I help you today?</h2><p>Ask me anything about the Indian election process.</p><div class="welcome-chips"><button class="welcome-chip" type="button" onclick="askQuick(\x27How do I register as a voter?\x27)">How do I register as a voter?</button><button class="welcome-chip" type="button" onclick="askQuick(\x27How does EVM work?\x27)">How does EVM work?</button></div></div>';
  }
  function askQuick(q){
    document.getElementById('userInput').value=q;
    sendMessage();
  }
  async function sendMessage(){
    var input=document.getElementById('userInput');
    var btn=document.getElementById('sendBtn');
    var text=input.value.trim();
    if(!text)return;
    var langPrefix=langPrompts[currentLang]||'';
    var msgWithLang=langPrefix+text;
    var welcome=document.getElementById('welcome');
    if(welcome)welcome.remove();
    appendMessage('user',text);
    chatHistory.push({role:'user',content:msgWithLang});
    input.value='';
    input.style.height='auto';
    btn.disabled=true;
    var typingId=showTyping();
    try{
      var res=await fetch('/chat',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({message:msgWithLang,history:chatHistory.slice(0,-1)})
      });
      var data=await res.json();
      removeTyping(typingId);
      appendMessage('bot',data.response);
      chatHistory.push({role:'model',content:data.response});
    }catch(e){
      removeTyping(typingId);
      appendMessage('bot','Sorry, connection error. Please try again.');
    }
    btn.disabled=false;
  }
  function appendMessage(role,text){
    var chat=document.getElementById('chat');
    var row=document.createElement('div');
    row.className='msg-row '+role;
    var avatarContent=role==='user'?'V':'🗳️';
    var name=role==='user'?'You':'VoteGuide AI';
    var formatted=text
      .replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>')
      .replace(/\*(.*?)\*/g,'<em>$1</em>')
      .replace(/\n/g,'<br/>');
    row.innerHTML='<div class="msg-avatar">'+avatarContent+'</div><div class="msg-content"><div class="msg-name">'+name+'</div><div class="msg-text">'+formatted+'</div></div>';
    chat.appendChild(row);
    chat.scrollTop=chat.scrollHeight;
  }
  function showTyping(){
    var chat=document.getElementById('chat');
    var id='typing'+Date.now();
    var row=document.createElement('div');
    row.className='msg-row bot';
    row.id=id;
    row.innerHTML='<div class="msg-avatar">🗳️</div><div class="msg-content"><div class="msg-name">VoteGuide AI</div><div class="typing-dots"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div></div>';
    chat.appendChild(row);
    chat.scrollTop=chat.scrollHeight;
    return id;
  }
  function removeTyping(id){var el=document.getElementById(id);if(el)el.remove();}
  document.getElementById('userInput').addEventListener('keydown',function(e){
    if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMessage();}
  });
  document.getElementById('userInput').addEventListener('input',function(){
    this.style.height='auto';
    this.style.height=Math.min(this.scrollHeight,120)+'px';
  });
</script>
</body>
</html>"""

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=HTML_PAGE, status_code=200)

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {req.message}"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt
        )
        return JSONResponse({"response": response.text})
    except Exception as e:
        return JSONResponse({"response": f"Error: {str(e)}"}, status_code=500)

@app.get("/health")
async def health():
    return {"status": "ok"}