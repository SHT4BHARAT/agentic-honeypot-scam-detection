"""Pydantic models for request/response validation."""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class Message(BaseModel):
    """Individual message in a conversation."""
    sender: Literal["scammer", "user"]
    text: str
    timestamp: int


class Metadata(BaseModel):
    """Optional metadata about the conversation."""
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"


class HoneypotRequest(BaseModel):
    """Incoming request to the honeypot API."""
    sessionId: str = Field(..., description="Unique session identifier")
    message: Message = Field(..., description="Latest incoming message")
    conversationHistory: List[Message] = Field(default_factory=list, description="Previous messages")
    metadata: Optional[Metadata] = None


class HoneypotResponse(BaseModel):
    """Response from the honeypot API."""
    status: Literal["success", "error"]
    reply: Optional[str] = None
    message: Optional[str] = None  # For error messages


class ExtractedIntelligence(BaseModel):
    """Intelligence extracted from scammer conversations."""
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    suspiciousKeywords: List[str] = Field(default_factory=list)


class FinalResultPayload(BaseModel):
    """Payload sent to GUVI evaluation endpoint."""
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str
