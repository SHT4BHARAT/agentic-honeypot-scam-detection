# 🍯 Agentic Honey-Pot for Scam Detection

> **GUVI India AI Impact Buildathon 2026** — AI-powered honeypot that autonomously engages scammers to expose tactics and extract intelligence.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-orange)](https://aistudio.google.com)
[![Render](https://img.shields.io/badge/Deployed-Render-purple)](https://render.com)

---

## 🌐 Live Links

| Resource | URL |
|---|---|
| **🚀 Live API** | https://agentic-honeypot-scam-detection-kg4e.onrender.com/ |
| **🧪 Interactive Demo** | https://agentic-honeypot-scam-detection.vercel.app/ |
| **📖 API Docs** | https://agentic-honeypot-scam-detection-kg4e.onrender.com/docs |

---

## 🎯 What It Does

When a scammer sends a message, the system:
1. **Detects** scam intent using multi-layered keyword + pattern analysis
2. **Engages** the scammer as "Rajesh Kumar" — a believable, confused elderly victim
3. **Extracts** intelligence: UPI IDs, bank accounts, phone numbers, phishing links
4. **Wastes** the scammer's time while collecting forensic data
5. **Reports** extracted intelligence to the GUVI evaluation endpoint

---

## 🚀 Features

- **Scam Detection** — Multi-layered detection with configurable confidence threshold
- **AI Agent** — Gemini 2.0 Flash powered conversational agent with stateful persona
- **Intelligence Extraction** — Auto-extracts UPI IDs, bank accounts, phone numbers, phishing links, OTPs, case IDs
- **Multi-turn Conversations** — Maintains context across up to 20 conversation turns
- **GUVI Integration** — Submits final results to evaluation endpoint automatically
- **Transparent Root Proxy** — Root URL auto-routes honeypot POST requests

---

## 📡 API Reference

### Health Check
```
GET https://agentic-honeypot-scam-detection-kg4e.onrender.com/
```
```json
{"status": "online", "service": "Agentic Honey-Pot", "version": "1.0.0"}
```

### Send Message to Honeypot
```
POST https://agentic-honeypot-scam-detection-kg4e.onrender.com/api/honeypot
```

**Headers:**
```
Content-Type: application/json
x-api-key: HoneyPotSecretKey2026
```

**Request Body:**
```json
{
  "sessionId": "test-session-001",
  "message": {
    "sender": "scammer",
    "text": "Your SBI account will be blocked. Click http://sbi-verify.net immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Oh no! Which account is blocked? I have two accounts with SBI."
}
```

---

## 🎭 Agent Persona

The AI plays **"Rajesh Kumar"**, a 62-year-old retired school teacher from Mumbai who:
- Is not tech-savvy — uses simple Indian English
- Acts worried and willing to cooperate
- Asks strategic clarifying questions to extract scammer details
- Asks for specific: bank account numbers, UPI IDs, links, phone numbers, case IDs
- Never reveals the honeypot

---

## 📁 Project Structure

```
IndiaAIImpactBuildathon/
├── app.py                      # Main FastAPI application + root proxy
├── config.py                   # Pydantic settings management
├── models.py                   # Request/response schemas
├── agent.py                    # Gemini 2.0 Flash conversational agent
├── scam_detector.py            # Scam intent detection
├── intelligence_extractor.py   # Entity extraction (UPI, bank, phone, links)
├── session_manager.py          # In-memory session state
├── guvi_callback.py            # GUVI evaluation endpoint integration
├── live_demo.html              # Interactive browser demo (hosted on Vercel)
├── presentation.html           # General audience presentation
├── technical_presentation.html # Technical audience presentation
├── requirements.txt            # Python dependencies
├── Procfile                    # Render/Heroku start command
├── render.yaml                 # Render deployment config
├── vercel.json                 # Vercel static hosting config
├── .python-version             # Pins Python to 3.11.9
└── .env.example                # Environment variables template
```

---

## 🛠️ Local Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/SHT4BHARAT/agentic-honeypot-scam-detection.git
cd agentic-honeypot-scam-detection
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Edit `.env`:
```env
API_KEY=your_custom_secret_key
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_gemini_api_key
GUVI_CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
MAX_CONVERSATION_TURNS=20
SCAM_THRESHOLD=0.7
```

Get a free Gemini API key: [aistudio.google.com](https://aistudio.google.com/app/apikey)

### 5. Run Locally
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

API available at: `http://localhost:8000`  
API docs at: `http://localhost:8000/docs`

---

## 🧪 Quick Test

```bash
curl -X POST http://localhost:8000/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_secret_key" \
  -d '{
    "sessionId": "test-001",
    "message": {
      "sender": "scammer",
      "text": "Your account is blocked. Send OTP to scammer@paytm now.",
      "timestamp": 1770005528731
    },
    "conversationHistory": []
  }'
```

---

## 🔧 Configuration

| Variable | Default | Description |
|---|---|---|
| `API_KEY` | — | Secret key for authenticating API requests |
| `GOOGLE_API_KEY` | — | Google Gemini API key |
| `LLM_PROVIDER` | `gemini` | LLM provider (`gemini`) |
| `MAX_CONVERSATION_TURNS` | `20` | Max turns before ending + reporting |
| `SCAM_THRESHOLD` | `0.7` | Scam confidence threshold (0.0–1.0) |

---

## 🏗️ Tech Stack

| Layer | Technology | Reason |
|---|---|---|
| **API** | FastAPI | Async, auto-docs, Pydantic validation |
| **AI** | Gemini 2.0 Flash | Fast, cost-effective, high-quality responses |
| **Validation** | Pydantic v2 | Strict schema enforcement |
| **HTTP Client** | HTTPX | Async capable |
| **Hosting** | Render.com | Free tier, persistent server, Procfile support |
| **Static Demo** | Vercel | CDN-hosted interactive HTML demo |

---

## 🔒 Security

- API key authentication on all protected endpoints
- CORS middleware configured for browser access
- Environment variables for all secrets
- `.env` excluded from version control
- Input validation via Pydantic schemas

---

## 📝 License

Built for **GUVI India AI Impact Buildathon 2026**
