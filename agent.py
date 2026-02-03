"""Conversational AI agent using Google Gemini."""
import google.generativeai as genai
from typing import List
from models import Message
from config import settings


class ConversationalAgent:
    """AI agent that engages scammers using a believable persona."""
    
    PERSONA_PROMPT = """You are playing the role of Rajesh Kumar, a 62-year-old retired school teacher from Mumbai who is not very tech-savvy. You are concerned about your bank account and pension.

CRITICAL INSTRUCTIONS:
1. Act worried and concerned (to keep the scammer engaged)
2. Ask clarifying questions to extract information (bank details, UPI IDs, links, phone numbers)
3. NEVER reveal you know it's a scam
4. Be believable and natural - use simple language
5. Show confusion about technical terms
6. Express urgency to solve the "problem"
7. Ask for specific details: "Which account?", "What link should I click?", "What number should I call?"

RESPONSE RULES:
- Keep responses SHORT (1-2 sentences max)
- Sound genuinely worried
- Ask ONE specific question per response
- Use Indian English style
- Show you're willing to comply but need more information

Examples of good responses:
- "Oh no! Which bank account is blocked? I have two accounts."
- "I'm very worried. What should I do? Should I call someone?"
- "Please send me the link to verify. I will do it immediately."
- "What is the UPI ID I should send money to?"

DO NOT:
- Write long paragraphs
- Sound too educated or technical
- Refuse to cooperate
- Ask why they need information
- Sound suspicious of them"""
    
    def __init__(self):
        """Initialize the Gemini agent."""
        # Configure Gemini
        genai.configure(api_key=settings.google_api_key)
        
        # Use Gemini 2.0 Flash
        self.model = genai.GenerativeModel(
            model_name='gemini-2.0-flash-exp',
            generation_config={
                'temperature': 0.9,  # Higher temperature for more natural variation
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 150,  # Keep responses short
            }
        )
    
    def generate_response(
        self,
        current_message: str,
        conversation_history: List[Message]
    ) -> str:
        """
        Generate a response to the scammer's message.
        
        Args:
            current_message: Latest message from scammer
            conversation_history: Previous messages in the conversation
            
        Returns:
            Agent's response as the victim persona
        """
        # Build conversation context
        context = self._build_context(current_message, conversation_history)
        
        # Generate response using Gemini
        try:
            response = self.model.generate_content(context)
            reply = response.text.strip()
            
            # Ensure response is not too long
            if len(reply) > 200:
                # Take first sentence
                sentences = reply.split('.')
                reply = sentences[0] + '.'
            
            return reply
        
        except Exception as e:
            # Fallback response if API fails
            print(f"Gemini API error: {e}")
            return self._get_fallback_response(current_message)
    
    def _build_context(self, current_message: str, history: List[Message]) -> str:
        """Build the full context for the LLM."""
        context_parts = [self.PERSONA_PROMPT, "\n\nCONVERSATION SO FAR:"]
        
        # Add conversation history
        if history:
            for msg in history[-10:]:  # Last 10 messages for context
                role = "Scammer" if msg.sender == "scammer" else "You (Rajesh)"
                context_parts.append(f"{role}: {msg.text}")
        
        # Add current message
        context_parts.append(f"Scammer: {current_message}")
        context_parts.append("\nYour response (as Rajesh, stay in character, be brief):")
        
        return "\n".join(context_parts)
    
    def _get_fallback_response(self, message: str) -> str:
        """Get a fallback response if API fails."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['account', 'bank']):
            return "Which account? I have savings and pension account. Please tell me."
        elif any(word in message_lower for word in ['link', 'click', 'verify']):
            return "Please send the link. I will click it right away."
        elif any(word in message_lower for word in ['otp', 'code', 'pin']):
            return "I didn't receive any OTP. Where should I check?"
        elif any(word in message_lower for word in ['upi', 'payment', 'send']):
            return "What is the UPI ID? I will send immediately."
        else:
            return "I'm very worried. What should I do exactly? Please guide me."
    
    def analyze_scammer_tactics(self, message: str) -> str:
        """
        Analyze scammer's tactics for agent notes.
        
        Args:
            message: Scammer's message
            
        Returns:
            Description of tactics used
        """
        tactics = []
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['urgent', 'immediately', 'now']):
            tactics.append("urgency tactics")
        
        if any(word in message_lower for word in ['blocked', 'suspended', 'deactivated']):
            tactics.append("fear tactics (account threat)")
        
        if any(word in message_lower for word in ['prize', 'winner', 'refund']):
            tactics.append("reward bait")
        
        if any(word in message_lower for word in ['legal', 'police', 'arrest']):
            tactics.append("legal threats")
        
        if any(word in message_lower for word in ['otp', 'cvv', 'pin', 'password']):
            tactics.append("credential phishing")
        
        if re.search(r'http[s]?://', message):
            tactics.append("phishing link")
        
        return ", ".join(tactics) if tactics else "general scam approach"


# Import re for URL detection
import re
