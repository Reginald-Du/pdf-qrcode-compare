from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QFrame, 
                               QHBoxLayout, QPushButton, QProgressBar, QFileDialog)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent

from src.i18n import tr

class FileDropZone(QFrame):
    files_dropped = Signal(str) # Emits file path

    def __init__(self, title_key="drop_title"):
        super().__init__()
        self.default_title_key = title_key
        self.setAcceptDrops(True)
        self.setFixedSize(400, 400)
        
        # Initial Style
        self.setStyleSheet("""
            QFrame { 
                border: 2px dashed #aaa; 
                border-radius: 8px; 
                background: #f9f9f9; 
            }
            QLabel {
                color: #555;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        self.layout.addStretch()
        
        # Label
        # If title_key is not in map, it might be raw text, but we assume it's a key or localized text passed in
        # For safety, check if it's a known key, else use as is
        self.label = QLabel(tr(title_key)) 
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)
        
        # Select Button
        self.btn_select = QPushButton(tr("btn_select_file"))
        self.btn_select.setFixedSize(120, 40)
        self.btn_select.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_select.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.btn_select.clicked.connect(self.open_file_dialog)
        
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.btn_select)
        btn_container.addStretch()
        self.layout.addLayout(btn_container)
        
        self.layout.addStretch()
        self.setLayout(self.layout)
        
        self.current_file = None

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, tr("dialog_select_title"), "", tr("dialog_file_filter"))
        if file_path:
            self.set_file(file_path)
            self.files_dropped.emit(file_path)

    def reset(self):
        self.current_file = None
        self.label.setText(tr(self.default_title_key))
        self.btn_select.setText(tr("btn_select_file"))
        self.label.setStyleSheet("") # Reset label style
        self.setStyleSheet("""
            QFrame { 
                border: 2px dashed #aaa; 
                border-radius: 8px; 
                background: #f9f9f9; 
            }
            QLabel {
                color: #555;
                font-size: 16px;
                font-weight: bold;
            }
        """)

    def set_file(self, file_path):
        self.current_file = file_path
        filename = file_path.split('/')[-1]
        
        # Truncate if too long (approx 20 chars)
        display_name = filename
        if len(filename) > 20:
            display_name = filename[:10] + "..." + filename[-7:]
            
        self.label.setText(display_name)
        self.btn_select.setText(tr("btn_change_file"))
        
        # Filename style
        self.label.setStyleSheet("""
            QLabel {
                color: #333333;
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                font-weight: normal;
            }
        """)
        
        # Selected state style
        self.setStyleSheet("""
            QFrame { 
                border: 2px solid #2196F3; 
                border-radius: 8px; 
                background: #e3f2fd; 
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame { 
                    border: 2px solid #2196F3; 
                    border-radius: 8px; 
                    background-color: rgba(33, 150, 243, 0.1);
                }
            """)
            
    def dragLeaveEvent(self, event):
        if not self.current_file:
            self.setStyleSheet("""
                QFrame { 
                    border: 2px dashed #aaa; 
                    border-radius: 8px; 
                    background: #f9f9f9; 
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame { 
                    border: 2px solid #2196F3; 
                    border-radius: 8px; 
                    background: #e3f2fd; 
                }
            """)

    def dropEvent(self, event: QDropEvent):
        files = []
        for url in event.mimeData().urls():
            files.append(url.toLocalFile())
        
        if files:
            # Only take the first pdf
            for f in files:
                if f.lower().endswith('.pdf'):
                    self.set_file(f)
                    self.files_dropped.emit(f)
                    break
        else:
             if not self.current_file:
                self.setStyleSheet("""
                    QFrame { 
                        border: 2px dashed #aaa; 
                        border-radius: 8px; 
                        background: #f9f9f9; 
                    }
                """)

class ProcessingDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel(tr("processing"))
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progress)
        self.setLayout(self.layout)
        
    def update_progress(self, value, text=None):
        self.progress.setValue(value)
        if text:
            self.label.setText(text)
