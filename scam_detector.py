"""Scam detection module using pattern matching and ML."""
import re
from typing import Tuple


class ScamDetector:
    """Detects scam intent in messages using multiple methods."""
    
    # Common scam keywords and patterns
    SCAM_KEYWORDS = [
        # Urgency tactics
        "urgent", "immediately", "right now", "within 24 hours", "expire",
        "suspended", "blocked", "deactivated", "locked",
        
        # Financial terms
        "bank account", "verify account", "update details", "confirm identity",
        "otp", "cvv", "pin", "password", "card number", "account number",
        "upi", "paytm", "phonepe", "gpay", "payment",
        
        # Authority impersonation
        "bank manager", "customer care", "support team", "security team",
        "rbi", "income tax", "police", "government",
        
        # Reward/threat tactics
        "prize", "winner", "congratulations", "refund", "cashback",
        "legal action", "arrest", "penalty", "fine",
        
        # Action requests
        "click here", "verify now", "update now", "share details",
        "send otp", "provide", "confirm", "validate"
    ]
    
    # Suspicious patterns (regex)
    SUSPICIOUS_PATTERNS = [
        r'\b\d{10,18}\b',  # Long number sequences (account numbers)
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs
        r'\b\d{4}\b',  # 4-digit numbers (OTP, PIN)
        r'@[a-zA-Z]+',  # UPI handles
    ]
    
    def __init__(self):
        """Initialize the scam detector."""
        self.keyword_weight = 0.6
        self.pattern_weight = 0.4
    
    def detect(self, text: str) -> Tuple[bool, float, str]:
        """
        Detect if a message is a scam.
        
        Args:
            text: Message text to analyze
            
        Returns:
            Tuple of (is_scam, confidence_score, explanation)
        """
        text_lower = text.lower()
        
        # Keyword matching
        keyword_matches = sum(1 for keyword in self.SCAM_KEYWORDS if keyword in text_lower)
        keyword_score = min(keyword_matches / 3, 1.0)  # Normalize to 0-1
        
        # Pattern matching
        pattern_matches = sum(1 for pattern in self.SUSPICIOUS_PATTERNS 
                            if re.search(pattern, text, re.IGNORECASE))
        pattern_score = min(pattern_matches / 2, 1.0)  # Normalize to 0-1
        
        # Combined confidence score
        confidence = (keyword_score * self.keyword_weight + 
                     pattern_score * self.pattern_weight)
        
        # Generate explanation
        explanation_parts = []
        if keyword_matches > 0:
            explanation_parts.append(f"{keyword_matches} scam keywords detected")
        if pattern_matches > 0:
            explanation_parts.append(f"{pattern_matches} suspicious patterns found")
        
        explanation = "; ".join(explanation_parts) if explanation_parts else "No scam indicators"
        
        # Determine if it's a scam (threshold from config)
        from config import settings
        is_scam = confidence >= settings.scam_threshold
        
        return is_scam, confidence, explanation
    
    def get_scam_indicators(self, text: str) -> dict:
        """
        Get detailed scam indicators from text.
        
        Args:
            text: Message text to analyze
            
        Returns:
            Dictionary with detected indicators
        """
        indicators = {
            "keywords": [],
            "patterns": [],
            "urgency_level": "low"
        }
        
        text_lower = text.lower()
        
        # Find matching keywords
        for keyword in self.SCAM_KEYWORDS:
            if keyword in text_lower:
                indicators["keywords"].append(keyword)
        
        # Find matching patterns
        for pattern in self.SUSPICIOUS_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                indicators["patterns"].extend(matches)
        
        # Determine urgency level
        urgency_words = ["urgent", "immediately", "right now", "expire", "suspended", "blocked"]
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        if urgency_count >= 2:
            indicators["urgency_level"] = "high"
        elif urgency_count == 1:
            indicators["urgency_level"] = "medium"
        
        return indicators
