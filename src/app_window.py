import sys
import fitz
import numpy as np
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QStackedWidget, QLabel, QSplitter, 
                               QListWidget, QListWidgetItem, QFileDialog, QMessageBox,
                               QFrame, QSpinBox, QComboBox)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QImage, QAction, QKeySequence, QShortcut

from src.ui_components import FileDropZone, ProcessingDialog
from src.worker import ScanWorker
from src.pdf_viewer import PDFPageViewer
from src.i18n import tr

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("app_title"))
        self.resize(1200, 800)

        # State
        self.file_a_path = None
        self.file_b_path = None
        self.doc_a = None
        self.doc_b = None
        self.scan_results_a = []
        self.scan_results_b = []
        self.diffs = []
        self.current_scale = 1.0 # 100%
        
        # Central Widget & Stack
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # -- Page 1: Input --
        self.page_input = QWidget()
        self.setup_input_page()
        self.stack.addWidget(self.page_input)

        # -- Page 2: Processing --
        self.page_processing = ProcessingDialog()
        self.stack.addWidget(self.page_processing)

        # -- Page 3: Results --
        self.page_results = QWidget()
        self.setup_results_page()
        self.stack.addWidget(self.page_results)

    def setup_input_page(self):
        layout = QVBoxLayout(self.page_input)
        
        title = QLabel(tr("select_title"))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        drop_layout = QHBoxLayout()
        drop_layout.setSpacing(40) # Add spacing between drop zones
        
        self.drop_a = FileDropZone(tr("drop_file_a"))
        self.drop_a.files_dropped.connect(self.set_file_a)
        
        self.drop_b = FileDropZone(tr("drop_file_b"))
        self.drop_b.files_dropped.connect(self.set_file_b)
        
        drop_layout.addStretch()
        drop_layout.addWidget(self.drop_a)
        drop_layout.addWidget(self.drop_b)
        drop_layout.addStretch()
        
        layout.addLayout(drop_layout)

        self.btn_compare = QPushButton(tr("btn_compare"))
        self.btn_compare.setEnabled(False)
        self.btn_compare.setFixedSize(200, 50)
        self.btn_compare.setStyleSheet("font-size: 18px; background-color: #2196F3; color: white; border-radius: 5px;")
        self.btn_compare.clicked.connect(self.start_comparison)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.btn_compare)
        btn_container.addStretch()
        layout.addLayout(btn_container)
        layout.addStretch()

    def setup_results_page(self):
        layout = QHBoxLayout(self.page_results)
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        
        sidebar_layout.addWidget(QLabel(tr("diff_found")))
        self.diff_list = QListWidget()
        self.diff_list.itemClicked.connect(self.on_diff_clicked)
        sidebar_layout.addWidget(self.diff_list)
        
        self.btn_export = QPushButton(tr("btn_export"))
        self.btn_export.clicked.connect(self.export_report)
        sidebar_layout.addWidget(self.btn_export)
        
        self.btn_new = QPushButton(tr("btn_new"))
        self.btn_new.clicked.connect(self.reset_app)
        sidebar_layout.addWidget(self.btn_new)
        
        layout.addWidget(sidebar)
        
        # Main Viewers
        viewer_container = QWidget()
        v_layout = QVBoxLayout(viewer_container)
        
        # Navigation
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton(tr("btn_prev"))
        self.btn_prev.clicked.connect(lambda _: self.change_page(-1))
        self.btn_next = QPushButton(tr("btn_next"))
        self.btn_next.clicked.connect(lambda _: self.change_page(1))
        self.lbl_page = QLabel(tr("page_label", current=1, total="?"))
        
        # Zoom Controls
        self.btn_zoom_out = QPushButton("-")
        self.btn_zoom_out.setFixedSize(30, 30)
        self.btn_zoom_out.clicked.connect(self.zoom_out)
        
        self.combo_zoom = QComboBox()
        self.combo_zoom.setEditable(True)
        self.combo_zoom.setFixedWidth(80)
        self.combo_zoom.addItems(["25%", "50%", "75%", "100%", "125%", "150%", "200%", "300%", "400%"])
        self.combo_zoom.setCurrentText("100%")
        self.combo_zoom.currentTextChanged.connect(self.on_zoom_text_changed)
        
        self.btn_zoom_in = QPushButton("+")
        self.btn_zoom_in.setFixedSize(30, 30)
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        
        self.btn_fit_width = QPushButton(tr("btn_fit_width"))
        self.btn_fit_width.clicked.connect(self.zoom_fit_width)
        
        # Shortcuts
        QShortcut(QKeySequence("Ctrl+="), self).activated.connect(self.zoom_in)
        QShortcut(QKeySequence("Ctrl+-"), self).activated.connect(self.zoom_out)
        QShortcut(QKeySequence("Cmd+="), self).activated.connect(self.zoom_in) # Mac
        QShortcut(QKeySequence("Cmd+-"), self).activated.connect(self.zoom_out) # Mac

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.lbl_page)
        nav_layout.addWidget(self.btn_next)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_zoom_out)
        nav_layout.addWidget(self.combo_zoom)
        nav_layout.addWidget(self.btn_zoom_in)
        nav_layout.addWidget(self.btn_fit_width)
        
        v_layout.addLayout(nav_layout)
        
        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        self.viewer_a = PDFPageViewer()
        self.viewer_b = PDFPageViewer()
        
        # Sync scrolling (basic)
        self.viewer_a.verticalScrollBar().valueChanged.connect(self.viewer_b.verticalScrollBar().setValue)
        self.viewer_b.verticalScrollBar().valueChanged.connect(self.viewer_a.verticalScrollBar().setValue)
        self.viewer_a.horizontalScrollBar().valueChanged.connect(self.viewer_b.horizontalScrollBar().setValue)
        self.viewer_b.horizontalScrollBar().valueChanged.connect(self.viewer_a.horizontalScrollBar().setValue)

        splitter.addWidget(self.viewer_a)
        splitter.addWidget(self.viewer_b)
        
        v_layout.addWidget(splitter)
        layout.addWidget(viewer_container)

    def set_file_a(self, path):
        self.file_a_path = path
        self.check_ready()

    def set_file_b(self, path):
        self.file_b_path = path
        self.check_ready()

    def check_ready(self):
        if self.file_a_path and self.file_b_path:
            self.btn_compare.setEnabled(True)

    def start_comparison(self):
        self.stack.setCurrentIndex(1)
        self.worker = ScanWorker(self.file_a_path, self.file_b_path)
        self.worker.progress.connect(self.page_processing.update_progress)
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.error.connect(self.on_scan_error)
        self.worker.start()

    def on_scan_error(self, msg):
        QMessageBox.critical(self, tr("error_title"), msg)
        self.stack.setCurrentIndex(0)

    def on_scan_finished(self, res_a, res_b, diffs):
        self.scan_results_a = res_a
        self.scan_results_b = res_b
        self.diffs = diffs
        
        try:
            self.doc_a = fitz.open(self.file_a_path)
            self.doc_b = fitz.open(self.file_b_path)
            self.total_pages = max(len(self.doc_a), len(self.doc_b))
        except Exception as e:
            self.on_scan_error(tr("open_error", e=e))
            return

        self.populate_diff_list()
        self.load_page(1) # 1-based
        self.stack.setCurrentIndex(2)

    def populate_diff_list(self):
        self.diff_list.clear()
        
        # Group by page for summary
        diff_count = 0
        for diff in self.diffs:
            if diff.type != "MATCH":
                diff_count += 1
                
                # Localize Diff Type
                type_str = diff.type
                if diff.type == "CONTENT_MISMATCH":
                    type_str = tr("diff_mismatch")
                elif diff.type == "ONLY_IN_A":
                    type_str = tr("diff_only_a")
                elif diff.type == "ONLY_IN_B":
                    type_str = tr("diff_only_b")
                    
                item = QListWidgetItem(f"Page {diff.page_index}: {type_str}")
                item.setData(Qt.ItemDataRole.UserRole, diff.page_index)
                if diff.type == "CONTENT_MISMATCH":
                    item.setForeground(Qt.GlobalColor.red)
                elif diff.type == "ONLY_IN_A":
                    item.setForeground(Qt.GlobalColor.blue)
                elif diff.type == "ONLY_IN_B":
                    item.setForeground(Qt.GlobalColor.darkYellow)
                self.diff_list.addItem(item)
        
        if diff_count == 0:
            self.diff_list.addItem(tr("no_diff"))

    def on_diff_clicked(self, item):
        page = item.data(Qt.ItemDataRole.UserRole)
        if page:
            self.load_page(page)

    def zoom_in(self, _=None):
        self.set_scale(self.current_scale + 0.25)

    def zoom_out(self, _=None):
        self.set_scale(self.current_scale - 0.25)

    def on_zoom_text_changed(self, text):
        # Only process if it ends with % or is a number
        clean_text = text.replace("%", "").strip()
        try:
            val = float(clean_text)
            self.set_scale(val / 100.0)
        except ValueError:
            pass

    def zoom_fit_width(self, _=None):
        # Calculate scale to fit width
        # Viewport width / Page width
        if not self.doc_a: return
        
        try:
            page = self.doc_a.load_page(0)
            # Default PDF point size
            rect = page.rect
            
            # Viewport width (approximate, taking half of splitter width)
            # A better way is to use the actual viewer width if visible
            viewer_width = self.viewer_a.viewport().width()
            
            # 2.0 is the base render scale we use in get_page_pixmap
            base_scale = 2.0 
            image_width = rect.width * base_scale
            
            if image_width > 0:
                # Scale needed to fit image into viewer
                # We want scale_factor * image_width = viewer_width
                scale = viewer_width / image_width
                self.set_scale(scale)
        except Exception as e:
            print(f"Fit width error: {e}")

    def set_scale(self, scale):
        # Clamp 25% - 400%
        scale = max(0.25, min(4.0, scale))
        self.current_scale = scale
        
        # Update UI
        self.combo_zoom.blockSignals(True)
        self.combo_zoom.setCurrentText(f"{int(scale * 100)}%")
        self.combo_zoom.blockSignals(False)
        
        # Apply to viewers
        self.viewer_a.set_zoom(scale)
        self.viewer_b.set_zoom(scale)

    def change_page(self, delta):
        new_page = self.current_page + delta
        if 1 <= new_page <= self.total_pages:
            self.load_page(new_page)

    def load_page(self, page_num):
        self.current_page = page_num
        self.lbl_page.setText(f"Page: {page_num} / {self.total_pages}")
        
        # Render Page A
        pix_a = self.get_page_pixmap(self.doc_a, page_num - 1)
        overlays_a = self.get_overlays(page_num, is_a=True)
        self.viewer_a.set_content(pix_a, overlays_a)
        
        # Render Page B
        pix_b = self.get_page_pixmap(self.doc_b, page_num - 1)
        overlays_b = self.get_overlays(page_num, is_a=False)
        self.viewer_b.set_content(pix_b, overlays_b)
        
        # Re-apply current scale to ensure new page respects it
        self.set_scale(self.current_scale)

    def get_page_pixmap(self, doc, page_idx):
        if not doc or page_idx >= len(doc):
            return None
        page = doc.load_page(page_idx)
        # 2.0 zoom for display quality
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to QPixmap
        img_format = QImage.Format.Format_RGB888
        if pix.n == 4:
            img_format = QImage.Format.Format_RGBA8888
            
        img = QImage(pix.samples, pix.w, pix.h, pix.stride, img_format)
        return QPixmap.fromImage(img)

    def get_overlays(self, page_num, is_a=True):
        overlays = []
        
        # Filter diffs for this page
        page_diffs = [d for d in self.diffs if d.page_index == page_num]
        
        for diff in page_diffs:
            if diff.type == "MATCH":
                # Green
                if is_a and diff.rect_a:
                    overlays.append((diff.rect_a, "#00FF00", tr("diff_tooltip_match", content=diff.content_a)))
                elif not is_a and diff.rect_b:
                    overlays.append((diff.rect_b, "#00FF00", tr("diff_tooltip_match", content=diff.content_b)))
                    
            elif diff.type == "CONTENT_MISMATCH":
                # Red
                if is_a and diff.rect_a:
                    overlays.append((diff.rect_a, "#FF0000", tr("diff_tooltip_mismatch", content=diff.content_a)))
                elif not is_a and diff.rect_b:
                    overlays.append((diff.rect_b, "#FF0000", tr("diff_tooltip_mismatch", content=diff.content_b)))
                    
            elif diff.type == "ONLY_IN_A":
                # Blue (only in A)
                if is_a and diff.rect_a:
                    overlays.append((diff.rect_a, "#0000FF", tr("diff_tooltip_unique_a", content=diff.content_a)))
                    
            elif diff.type == "ONLY_IN_B":
                # Yellow/Orange (only in B)
                if not is_a and diff.rect_b:
                    overlays.append((diff.rect_b, "#FFA500", tr("diff_tooltip_unique_b", content=diff.content_b)))
                    
        return overlays

    def export_report(self, _=None):
        path, _ = QFileDialog.getSaveFileName(self, tr("btn_export"), "report.csv", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, 'w') as f:
                    f.write(tr("csv_header"))
                    for diff in self.diffs:
                        if diff.type == "MATCH": continue
                        c_a = diff.content_a.replace('"', '""') if diff.content_a else ""
                        c_b = diff.content_b.replace('"', '""') if diff.content_b else ""
                        f.write(f'{diff.page_index},{diff.type},"{c_a}","{c_b}"\n')
                QMessageBox.information(self, tr("success_title"), tr("report_saved"))
            except Exception as e:
                QMessageBox.critical(self, tr("error_title"), tr("save_error", e=e))

    def reset_app(self, _=None):
        self.doc_a = None
        self.doc_b = None
        self.file_a_path = None
        self.file_b_path = None
        self.scan_results_a = []
        self.scan_results_b = []
        self.diffs = []
        self.drop_a.reset()
        self.drop_b.reset()
        
        self.btn_compare.setEnabled(False)
        self.stack.setCurrentIndex(0)
