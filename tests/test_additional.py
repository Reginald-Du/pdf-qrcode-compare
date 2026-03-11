import os
import unittest

from src.pdf_processor import PDFProcessor, QRResult
from src.comparator import compare_qr_lists


class TestComparatorEdgeCases(unittest.TestCase):
    def make_qr(self, page, text, x=10, y=20):
        # Minimal quadrilateral polygon
        pts = [(x, y), (x + 10, y), (x + 10, y + 10), (x, y + 10)]
        return QRResult(page_index=page, content=text, polygon=pts)

    def test_only_in_a(self):
        a = [self.make_qr(1, "A1"), self.make_qr(1, "A2")]
        b = [self.make_qr(1, "B1")]
        diffs = compare_qr_lists(a, b, strict_order=True)
        # Expect: index0 compare A1 vs B1 -> mismatch or match, index1 ONLY_IN_A
        self.assertTrue(any(d.type == "ONLY_IN_A" for d in diffs), "Should detect ONLY_IN_A when A has extra element")

    def test_only_in_b(self):
        a = [self.make_qr(1, "A1")]
        b = [self.make_qr(1, "B1"), self.make_qr(1, "B2")]
        diffs = compare_qr_lists(a, b, strict_order=True)
        self.assertTrue(any(d.type == "ONLY_IN_B" for d in diffs), "Should detect ONLY_IN_B when B has extra element")


class TestPDFProcessorErrorHandling(unittest.TestCase):
    def setUp(self):
        self.processor = PDFProcessor()

    def test_nonexistent_path_raises(self):
        with self.assertRaises(Exception):
            self.processor.process_pdf("/nonexistent/path/does_not_exist.pdf")

    def test_invalid_pdf_raises(self):
        # Create an invalid PDF file (actually plain text)
        invalid_path = os.path.abspath("tests/data_invalid.pdf")
        try:
            with open(invalid_path, "w", encoding="utf-8") as f:
                f.write("this is not a pdf")
            with self.assertRaises(Exception):
                self.processor.process_pdf(invalid_path)
        finally:
            try:
                os.remove(invalid_path)
            except Exception:
                pass


class TestPDFProcessorProgressCallback(unittest.TestCase):
    def test_progress_reaches_100(self):
        processor = PDFProcessor()
        last = {"v": 0}
        def cb(p):
            last["v"] = p
        # Use a small local test file to minimize runtime
        pdf_path = os.path.abspath("test/file1.pdf")
        # If path not present, skip to avoid false negatives
        if not os.path.exists(pdf_path):
            self.skipTest("test/file1.pdf not found")
        _ = processor.process_pdf(pdf_path, cb=cb)
        self.assertEqual(last["v"], 100, "Progress callback should end at 100")


class TestGUISmoke(unittest.TestCase):
    def test_main_window_instantiation(self):
        # Minimal GUI smoke test: construct and dispose MainWindow without starting event loop
        try:
            from PySide6.QtWidgets import QApplication
            from src.app_window import MainWindow
        except Exception as e:
            self.skipTest(f"PySide6 not available or import failed: {e}")
            return
        app = QApplication.instance() or QApplication([])
        window = MainWindow()
        # Basic assertions on constructed UI state
        self.assertIsNotNone(window.centralWidget())
        self.assertFalse(window.btn_compare.isEnabled(), "Compare button should be disabled before selecting files")
        # Close and cleanup
        window.close()
        app.quit()


if __name__ == "__main__":
    unittest.main()
