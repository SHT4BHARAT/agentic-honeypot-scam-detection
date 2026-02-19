"""Test scam detection scoring"""
from scam_detector import ScamDetector

detector = ScamDetector()

# Test the official bank fraud scenario
test_message = "URGENT: Your SBI account has been compromised. Your account will be blocked in 2 hours. Share your account number and OTP immediately to verify your identity."

is_scam, confidence, explanation = detector.detect(test_message)

print(f"Is Scam: {is_scam}")
print(f"Confidence: {confidence:.4f}")
print(f"Explanation: {explanation}")
print(f"\nKeyword matches:")
indicators = detector.get_scam_indicators(test_message)
print(f"Keywords found: {indicators['keywords']}")
print(f"Patterns found: {indicators['patterns']}")
print(f"Urgency level: {indicators['urgency_level']}")
