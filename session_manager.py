"""Session management for tracking conversations."""
from typing import Dict, Optional
from models import Message, ExtractedIntelligence
from datetime import datetime


class SessionData:
    """Data stored for each conversation session."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messages: list[Message] = []
        self.intelligence = ExtractedIntelligence()
        self.scam_detected = False
        self.scam_confidence = 0.0
        self.created_at = datetime.now()
        self.turn_count = 0
        self.agent_notes: list[str] = []
    
    def add_message(self, message: Message):
        """Add a message to the session history."""
        self.messages.append(message)
        if message.sender == "scammer" or message.sender == "user":
            self.turn_count += 1
    
    def add_note(self, note: str):
        """Add an observation note about scammer behavior."""
        self.agent_notes.append(note)
    
    def get_agent_notes_summary(self) -> str:
        """Get a summary of all agent notes."""
        if not self.agent_notes:
            return "No specific tactics observed"
        return "; ".join(self.agent_notes)
    
    def should_end_conversation(self, max_turns: int) -> bool:
        """Determine if conversation should end."""
        # End if max turns reached
        if self.turn_count >= max_turns:
            return True
        
        # End if we have sufficient intelligence
        has_financial_info = (
            len(self.intelligence.upiIds) > 0 or
            len(self.intelligence.bankAccounts) > 0 or
            len(self.intelligence.phishingLinks) > 0
        )
        
        if has_financial_info and self.turn_count >= 5:
            return True
        
        return False


class SessionManager:
    """Manages conversation sessions."""
    
    def __init__(self):
        self._sessions: Dict[str, SessionData] = {}
    
    def get_session(self, session_id: str) -> SessionData:
        """Get or create a session."""
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionData(session_id)
        return self._sessions[session_id]
    
    def session_exists(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self._sessions
    
    def delete_session(self, session_id: str):
        """Delete a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions."""
        return len(self._sessions)


# Global session manager instance
session_manager = SessionManager()
