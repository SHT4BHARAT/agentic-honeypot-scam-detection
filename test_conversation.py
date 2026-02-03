"""Multi-turn conversation test to validate intelligence extraction."""
import httpx
import json
import time
from datetime import datetime

API_URL = "http://localhost:8000/api/honeypot"
API_KEY = "honeypot_secret_key_2026"


def send_message(session_id: str, sender: str, text: str, history: list):
    """Send a message and get response."""
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": sender,
            "text": text,
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "conversationHistory": history,
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


def run_conversation():
    """Run a multi-turn conversation."""
    session_id = "demo-session-001"
    conversation_history = []
    
    print("🎭 Multi-Turn Conversation Test")
    print("=" * 80)
    print()
    
    # Turn 1: Scammer initiates
    scammer_msg_1 = "Your bank account will be blocked in 2 hours. Verify immediately to avoid suspension."
    print(f"💀 Scammer: {scammer_msg_1}")
    
    status, response = send_message(session_id, "scammer", scammer_msg_1, conversation_history)
    agent_reply_1 = response.get('reply', '')
    print(f"🤖 Agent: {agent_reply_1}")
    print()
    
    # Update history
    conversation_history.append({
        "sender": "scammer",
        "text": scammer_msg_1,
        "timestamp": int(datetime.now().timestamp() * 1000)
    })
    conversation_history.append({
        "sender": "user",
        "text": agent_reply_1,
        "timestamp": int(datetime.now().timestamp() * 1000)
    })
    
    time.sleep(2)
    
    # Turn 2: Scammer provides link
    scammer_msg_2 = "Click this link to verify: http://fake-bank-verify.com/urgent and enter your account details."
    print(f"💀 Scammer: {scammer_msg_2}")
    
    status, response = send_message(session_id, "scammer", scammer_msg_2, conversation_history)
    agent_reply_2 = response.get('reply', '')
    print(f"🤖 Agent: {agent_reply_2}")
    print()
    
    conversation_history.append({
        "sender": "scammer",
        "text": scammer_msg_2,
        "timestamp": int(datetime.now().timestamp() * 1000)
    })
    conversation_history.append({
        "sender": "user",
        "text": agent_reply_2,
        "timestamp": int(datetime.now().timestamp() * 1000)
    })
    
    time.sleep(2)
    
    # Turn 3: Scammer asks for UPI
    scammer_msg_3 = "For faster verification, send Rs 100 to verify-account@paytm. This will confirm your identity."
    print(f"💀 Scammer: {scammer_msg_3}")
    
    status, response = send_message(session_id, "scammer", scammer_msg_3, conversation_history)
    agent_reply_3 = response.get('reply', '')
    print(f"🤖 Agent: {agent_reply_3}")
    print()
    
    conversation_history.append({
        "sender": "scammer",
        "text": scammer_msg_3,
        "timestamp": int(datetime.now().timestamp() * 1000)
    })
    conversation_history.append({
        "sender": "user",
        "text": agent_reply_3,
        "timestamp": int(datetime.now().timestamp() * 1000)
    })
    
    time.sleep(2)
    
    # Turn 4: Scammer provides phone number
    scammer_msg_4 = "If you have any issues, call our support at +919876543210. Transfer to account 1234567890123."
    print(f"💀 Scammer: {scammer_msg_4}")
    
    status, response = send_message(session_id, "scammer", scammer_msg_4, conversation_history)
    agent_reply_4 = response.get('reply', '')
    print(f"🤖 Agent: {agent_reply_4}")
    print()
    
    print("=" * 80)
    print("\n✅ Multi-turn conversation completed!")
    print("\n📊 Expected Intelligence Extracted:")
    print("   - UPI ID: verify-account@paytm")
    print("   - Phone: +919876543210")
    print("   - Bank Account: 1234567890123")
    print("   - Phishing Link: http://fake-bank-verify.com/urgent")
    print("   - Keywords: urgent, verify, blocked, account, etc.")
    print("\n💡 Check server logs for GUVI callback submission!")


if __name__ == "__main__":
    run_conversation()
