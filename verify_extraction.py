
from intelligence_extractor import IntelligenceExtractor
from models import ExtractedIntelligence
import unittest

class TestNewExtractionFields(unittest.TestCase):
    def setUp(self):
        self.extractor = IntelligenceExtractor()

    def test_email_extraction(self):
        text = "Please contact me at scammer@fake.com for more details."
        intel = self.extractor.extract(text)
        self.assertIn("scammer@fake.com", intel.emailAddresses)

    def test_case_id_extraction(self):
        text = "Your Case ID is CASE-12345. Please quote this."
        intel = self.extractor.extract(text)
        self.assertIn("CASE-12345", intel.caseIds)
        
        text2 = "Ref #: REF-9876"
        intel = self.extractor.extract(text2)
        self.assertIn("REF-9876", intel.caseIds)

    def test_policy_number_extraction(self):
        text = "Your Policy Number is POL-55555."
        intel = self.extractor.extract(text)
        self.assertIn("POL-55555", intel.policyNumbers)

    def test_order_number_extraction(self):
        text = "Order # ORD-111222 has been placed."
        intel = self.extractor.extract(text)
        self.assertIn("ORD-111222", intel.orderNumbers)

    def test_combined_extraction(self):
        text = """
        URGENT: Your SBI account is compromised. 
        Case ID: SBI-FAIL-2024
        Policy No: INS-998877
        Contact support@sbi-fraud.com immediately.
        """
        intel = self.extractor.extract(text)
        self.assertIn("SBI-FAIL-2024", intel.caseIds)
        self.assertIn("INS-998877", intel.policyNumbers)
        self.assertIn("support@sbi-fraud.com", intel.emailAddresses)

if __name__ == '__main__':
    unittest.main()
