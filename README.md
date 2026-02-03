# Agentic Honey-Pot for Scam Detection

AI-powered honeypot system that detects scam messages and autonomously engages scammers to extract intelligence.

## 🚀 Features

- **Scam Detection**: Multi-layered detection using keyword matching and pattern analysis
- **AI Agent**: Gemini 2.0 Flash-powered conversational agent with believable victim persona
- **Intelligence Extraction**: Automatically extracts UPI IDs, bank accounts, phone numbers, and phishing links
- **GUVI Integration**: Submits final results to evaluation endpoint

## 📋 Prerequisites

- Python 3.10 or higher
- Google Gemini API key (free tier available)

## 🛠️ Setup Instructions

### 1. Clone/Navigate to Project
```bash
cd d:\IndiaAIImpactBuildathon
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file by copying the example:
```bash
copy .env.example .env
```

Edit `.env` and add your API keys:
```env
API_KEY=your_custom_secret_key_123
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**Get Google Gemini API Key:**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Get API Key"
3. Copy and paste into `.env` file

### 5. Run the Application
```bash
python app.py
```

Or using uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at: `http://localhost:8000`

## 📡 API Usage

### Health Check
```bash
curl http://localhost:8000/
```

### Send Message to Honeypot
```bash
curl -X POST http://localhost:8000/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_custom_secret_key_123" \
  -d '{
    "sessionId": "test-session-123",
    "message": {
      "sender": "scammer",
      "text": "Your bank account will be blocked. Verify immediately.",
      "timestamp": 1770005528731
    },
    "conversationHistory": [],
    "metadata": {
      "channel": "SMS",
      "language": "English",
      "locale": "IN"
    }
  }'
```

### Response Format
```json
{
  "status": "success",
  "reply": "Oh no! Which account? I have two accounts. Please tell me."
}
```

## 🧪 Testing

Test with sample scam messages:

```bash
# Test 1: Bank account threat
curl -X POST http://localhost:8000/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key" \
  -d '{"sessionId":"test1","message":{"sender":"scammer","text":"Your account is suspended. Click http://fake-bank.com to verify","timestamp":1770005528731},"conversationHistory":[]}'

# Test 2: UPI scam
curl -X POST http://localhost:8000/api/honeypot \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key" \
  -d '{"sessionId":"test2","message":{"sender":"scammer","text":"Send refund to scammer@paytm immediately","timestamp":1770005528731},"conversationHistory":[]}'
```

## 📁 Project Structure

```
IndiaAIImpactBuildathon/
├── app.py                      # Main FastAPI application
├── config.py                   # Configuration management
├── models.py                   # Pydantic models
├── scam_detector.py           # Scam detection module
├── agent.py                   # Conversational AI agent
├── intelligence_extractor.py  # Entity extraction
├── session_manager.py         # Session state management
├── guvi_callback.py          # GUVI endpoint integration
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your actual config (not in git)
└── .gitignore               # Git ignore rules
```

## 🔧 Configuration

Edit `.env` to customize:

- `API_KEY`: Your custom API key for authentication
- `LLM_PROVIDER`: Choose `gemini`, `anthropic`, or `openai`
- `GOOGLE_API_KEY`: Your Gemini API key
- `MAX_CONVERSATION_TURNS`: Maximum turns before ending (default: 20)
- `SCAM_THRESHOLD`: Confidence threshold for scam detection (default: 0.7)

## 📊 How It Works

1. **Message Received**: API receives incoming message
2. **Scam Detection**: First message analyzed for scam indicators
3. **Agent Activation**: If scam detected, AI agent engages with victim persona
4. **Intelligence Extraction**: Extracts UPI IDs, bank accounts, URLs, phone numbers
5. **Multi-turn Conversation**: Agent asks strategic questions to extract more info
6. **GUVI Submission**: Final results submitted to evaluation endpoint

## 🎭 Agent Persona

The AI agent plays "Rajesh Kumar", a 62-year-old retired teacher who:
- Is not tech-savvy
- Sounds worried and concerned
- Asks clarifying questions
- Never reveals scam detection
- Uses simple Indian English

## 🔒 Security

- API key authentication required
- Environment variables for sensitive data
- `.env` file excluded from git
- Input validation with Pydantic

## 📝 License

Built for GUVI India AI Impact Buildathon 2026

## 🤝 Support

For issues or questions, check the logs in the console output.
