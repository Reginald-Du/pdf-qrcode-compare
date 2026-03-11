import unittest
import os
from src.pdf_processor import PDFProcessor
from src.comparator import compare_qr_lists, DiffItem

class TestThreeQRs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file3 = os.path.abspath("test/file3.pdf")
        cls.file4 = os.path.abspath("test/file4.pdf")
        
        processor = PDFProcessor()
        print("\nScanning files with ZXing-CPP...")
        cls.res3 = processor.process_pdf(cls.file3)
        cls.res4 = processor.process_pdf(cls.file4)
        
        print(f"File 3: {len(cls.res3)} QRs")
        print(f"File 4: {len(cls.res4)} QRs")

    def test_01_qr_count(self):
        """Verify that 3 QRs are detected in both files."""
        self.assertEqual(len(self.res3), 3, "File 3 should have 3 QRs")
        self.assertEqual(len(self.res4), 3, "File 4 should have 3 QRs")

    def test_02_first_qr_mismatch(self):
        """Verify the First QR (Top-Right) is DIFFERENT."""
        # Index 0 is Top-Right (Y~338)
        qr3 = self.res3[0]
        qr4 = self.res4[0]
        
        # Verify position is roughly same (Top Right)
        # Y should be around 338-340
        y3 = min(p[1] for p in qr3.polygon)
        y4 = min(p[1] for p in qr4.polygon)
        print(f"QR #1 Y-coords: {y3} vs {y4}")
        self.assertAlmostEqual(y3, y4, delta=50)
        
        # Verify Content Mismatch
        print(f"QR #1 Content: {qr3.content[:20]}... vs {qr4.content[:20]}...")
        self.assertNotEqual(qr3.content, qr4.content, "First QR (Top-Right) should be different")

    def test_03_second_qr_match(self):
        """Verify the Second QR (Top-Left) is SAME."""
        # Index 1 is Top-Left (Y~650)
        qr3 = self.res3[1]
        qr4 = self.res4[1]
        
        y3 = min(p[1] for p in qr3.polygon)
        y4 = min(p[1] for p in qr4.polygon)
        print(f"QR #2 Y-coords: {y3} vs {y4}")
        self.assertAlmostEqual(y3, y4, delta=50)
        
        # Verify Content Match
        print(f"QR #2 Content: {qr3.content[:20]}... vs {qr4.content[:20]}...")
        self.assertEqual(qr3.content, qr4.content, "Second QR (Top-Left) should be same")

    def test_04_third_qr_match(self):
        """Verify the Third QR (Bottom-Right) is SAME."""
        # Index 2 is Bottom-Right (Y~1633)
        qr3 = self.res3[2]
        qr4 = self.res4[2]
        
        y3 = min(p[1] for p in qr3.polygon)
        y4 = min(p[1] for p in qr4.polygon)
        print(f"QR #3 Y-coords: {y3} vs {y4}")
        self.assertAlmostEqual(y3, y4, delta=50)
        
        # Verify Content Match
        print(f"QR #3 Content: {qr3.content[:20]}... vs {qr4.content[:20]}...")
        self.assertEqual(qr3.content, qr4.content, "Third QR (Bottom-Right) should be same")

    def test_05_comparator_output(self):
        """Verify comparator produces correct DiffItems."""
        diffs = compare_qr_lists(self.res3, self.res4, strict_order=True)
        
        # We expect:
        # Index 0: CONTENT_MISMATCH
        # Index 1: MATCH
        # Index 2: MATCH
        
        self.assertEqual(len(diffs), 3)
        self.assertEqual(diffs[0].type, "CONTENT_MISMATCH")
        self.assertEqual(diffs[1].type, "MATCH")
        self.assertEqual(diffs[2].type, "MATCH")

if __name__ == "__main__":
    unittest.main()
