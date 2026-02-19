"""Intelligence extraction from scammer messages."""
import re
from typing import Set
from models import ExtractedIntelligence


class IntelligenceExtractor:
    """Extracts actionable intelligence from scammer conversations."""
    
    # Regex patterns for entity extraction
    UPI_PATTERN = r'\b[a-zA-Z0-9._-]+@[a-zA-Z]+\b'
    BANK_ACCOUNT_PATTERN = r'\b\d{9,18}\b'
    PHONE_PATTERN = r'(?:\+91|0)?[6-9]\d{9}\b'
    URL_PATTERN = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Generic ID patterns
    CASE_ID_PATTERN = r'(?i)\b(?:case|ref|ticket)\s*(?:id|no|num|number|#)?\s*(?:[:#-]|\bis\b)?\s*([a-z0-9-]{4,})\b'
    POLICY_NO_PATTERN = r'(?i)\b(?:policy|pol)\s*(?:id|no|num|number|#)?\s*(?:[:#-]|\bis\b)?\s*([a-z0-9-]{4,})\b'
    ORDER_NO_PATTERN = r'(?i)\b(?:order|ord)\s*(?:id|no|num|number|#)?\s*(?:[:#-]|\bis\b)?\s*([a-z0-9-]{4,})\b'
    
    # Suspicious keywords to track
    SUSPICIOUS_KEYWORDS = [
        "urgent", "verify", "blocked", "suspended", "otp", "cvv", "pin",
        "password", "account", "bank", "payment", "refund", "prize",
        "winner", "legal action", "arrest", "penalty"
    ]
    
    def __init__(self):
        """Initialize the intelligence extractor."""
        pass
    
    def extract(self, text: str, existing_intel: ExtractedIntelligence = None) -> ExtractedIntelligence:
        """
        Extract intelligence from a message.
        
        Args:
            text: Message text to analyze
            existing_intel: Previously extracted intelligence to merge with
            
        Returns:
            ExtractedIntelligence object with all findings
        """
        if existing_intel is None:
            intel = ExtractedIntelligence()
        else:
            intel = existing_intel
        
        if intel.emailAddresses is None:
            intel.emailAddresses = []
        if intel.caseIds is None:
            intel.caseIds = []
        if intel.policyNumbers is None:
            intel.policyNumbers = []
        if intel.orderNumbers is None:
            intel.orderNumbers = []
            
        # Extract UPI IDs
        upi_matches = re.findall(self.UPI_PATTERN, text, re.IGNORECASE)
        for upi in upi_matches:
            if upi not in intel.upiIds and self._is_valid_upi(upi):
                intel.upiIds.append(upi)
        
        # Extract bank account numbers
        bank_matches = re.findall(self.BANK_ACCOUNT_PATTERN, text)
        for account in bank_matches:
            if account not in intel.bankAccounts and self._is_valid_bank_account(account):
                intel.bankAccounts.append(account)
        
        # Extract phone numbers
        phone_matches = re.findall(self.PHONE_PATTERN, text)
        for phone in phone_matches:
            normalized_phone = self._normalize_phone(phone)
            if normalized_phone and normalized_phone not in intel.phoneNumbers:
                intel.phoneNumbers.append(normalized_phone)
        
        # Extract URLs
        url_matches = re.findall(self.URL_PATTERN, text, re.IGNORECASE)
        for url in url_matches:
            if url not in intel.phishingLinks:
                intel.phishingLinks.append(url)
                
        # Extract Email Addresses
        email_matches = re.findall(self.EMAIL_PATTERN, text)
        for email in email_matches:
            if email not in intel.emailAddresses:
                intel.emailAddresses.append(email)
                
        # Extract Case IDs
        case_matches = re.findall(self.CASE_ID_PATTERN, text)
        for case_id in case_matches:
            if case_id not in intel.caseIds:
                intel.caseIds.append(case_id)
                
        # Extract Policy Numbers
        policy_matches = re.findall(self.POLICY_NO_PATTERN, text)
        for policy_no in policy_matches:
            if policy_no not in intel.policyNumbers:
                intel.policyNumbers.append(policy_no)
                
        # Extract Order Numbers
        order_matches = re.findall(self.ORDER_NO_PATTERN, text)
        for order_no in order_matches:
            if order_no not in intel.orderNumbers:
                intel.orderNumbers.append(order_no)
        
        # Extract suspicious keywords
        text_lower = text.lower()
        for keyword in self.SUSPICIOUS_KEYWORDS:
            if keyword in text_lower and keyword not in intel.suspiciousKeywords:
                intel.suspiciousKeywords.append(keyword)
        
        return intel
    
    def _is_valid_upi(self, upi: str) -> bool:
        """Validate UPI ID format."""
        # Must have @ symbol and valid provider
        if '@' not in upi:
            return False
        
        username, provider = upi.split('@', 1)
        
        # Username should be at least 3 characters
        if len(username) < 3:
            return False
        
        # Common UPI providers
        valid_providers = ['paytm', 'phonepe', 'gpay', 'ybl', 'okaxis', 'okicici', 'oksbi', 'upi']
        return provider.lower() in valid_providers or len(provider) >= 3
    
    def _is_valid_bank_account(self, account: str) -> bool:
        """Validate bank account number."""
        # Should be between 9-18 digits
        if not (9 <= len(account) <= 18):
            return False
        
        # Exclude common false positives (like timestamps, phone numbers)
        # Avoid numbers that look like timestamps (starts with 17, 16, 20)
        if account.startswith(('17', '16', '20')):
            return False
        
        return True
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number to standard format."""
        # Remove all non-digits
        digits = re.sub(r'\D', '', phone)
        
        # Handle Indian phone numbers
        if len(digits) == 10 and digits[0] in '6789':
            return f"+91{digits}"
        elif len(digits) == 12 and digits.startswith('91'):
            return f"+{digits}"
        elif len(digits) == 13 and digits.startswith('91'):
            return f"+{digits[1:]}"
        
        return None
    
    def get_extraction_summary(self, intel: ExtractedIntelligence) -> str:
        """
        Generate a summary of extracted intelligence.
        
        Args:
            intel: ExtractedIntelligence object
            
        Returns:
            Human-readable summary string
        """
        parts = []
        
        if intel.upiIds:
            parts.append(f"{len(intel.upiIds)} UPI ID(s)")
        if intel.bankAccounts:
            parts.append(f"{len(intel.bankAccounts)} bank account(s)")
        if intel.phoneNumbers:
            parts.append(f"{len(intel.phoneNumbers)} phone number(s)")
        if intel.phishingLinks:
            parts.append(f"{len(intel.phishingLinks)} phishing link(s)")
        
        if not parts:
            return "No intelligence extracted yet"
        
        return "Extracted: " + ", ".join(parts)
