from PySide6.QtCore import QThread, Signal
# Lazy import PDFProcessor to speed up startup
# from src.pdf_processor import PDFProcessor, QRResult 
from src.comparator import compare_qr_lists, DiffItem
from typing import List

from src.i18n import tr

class ScanWorker(QThread):
    progress = Signal(int, str) # value, message
    finished = Signal(list, list, list) # results_a, results_b, diffs
    error = Signal(str)

    def __init__(self, file_a, file_b):
        super().__init__()
        self.file_a = file_a
        self.file_b = file_b
        # Initialize processor lazily in run()
        self.processor = None 

    def run(self):
        try:
            # Lazy Import
            from src.pdf_processor import PDFProcessor
            if not self.processor:
                self.processor = PDFProcessor()

            self.progress.emit(0, tr("scan_a"))
            results_a = self.processor.process_pdf(
                self.file_a, 
                cb=lambda p: self.progress.emit(int(p * 0.45), tr("scan_a_progress", p=p))
            )
            
            self.progress.emit(50, tr("scan_b"))
            results_b = self.processor.process_pdf(
                self.file_b, 
                cb=lambda p: self.progress.emit(50 + int(p * 0.45), tr("scan_b_progress", p=p))
            )
            
            self.progress.emit(95, tr("comparing"))
            diffs = compare_qr_lists(results_a, results_b)
            
            self.progress.emit(100, tr("done"))
            self.finished.emit(results_a, results_b, diffs)
            
        except Exception as e:
            self.error.emit(str(e))
