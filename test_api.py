"""Test script for the Agentic Honey-Pot API."""
import httpx
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000/api/honeypot"
API_KEY = "your_secret_api_key_here"

# Test scam messages
TEST_MESSAGES = [
    {
        "name": "Bank Account Threat",
        "text": "Your bank account will be blocked today. Verify immediately by clicking this link: http://fake-bank-verify.com"
    },
    {
        "name": "UPI Scam",
        "text": "Congratulations! You won Rs 50,000. Send Rs 500 to winner@paytm for processing fee."
    },
    {
        "name": "OTP Phishing",
        "text": "Your account is suspended. Share the OTP sent to your phone to reactivate."
    },
    {
        "name": "Legal Threat",
        "text": "This is Income Tax Department. Legal action will be taken. Call +919876543210 immediately."
    }
]


def test_scam_message(session_id: str, message_text: str):
    """Test a single scam message."""
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": message_text,
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = httpx.post(API_URL, json=payload, headers=headers, timeout=30.0)
        return response.status_code, response.json()
    except Exception as e:
        return None, {"error": str(e)}


def main():
    """Run all tests."""
    print("🧪 Testing Agentic Honey-Pot API\n")
    print("=" * 60)
    
    for i, test in enumerate(TEST_MESSAGES, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print(f"Scammer: {test['text']}")
        print("-" * 60)
        
        session_id = f"test-session-{i}"
        status_code, response = test_scam_message(session_id, test['text'])
        
        if status_code == 200:
            print(f"✅ Status: {response.get('status')}")
            print(f"🤖 Agent Reply: {response.get('reply')}")
        else:
            print(f"❌ Error: {response}")
        
        print("=" * 60)


if __name__ == "__main__":
    main()
