import sys
import multiprocessing
import time

if __name__ == "__main__":
    # macOS specific: multiprocessing needs to be handled before any heavy imports
    multiprocessing.freeze_support()
    
    t0 = time.time()

    # Import Qt modules here (already imported but this marks the start of GUI init)
    from PySide6.QtWidgets import QApplication
    from src.app_window import MainWindow
    
    t_imports = time.time()
    print(f"[Startup] Imports loaded in {t_imports - t0:.4f}s")
    
    app = QApplication(sys.argv)
    t_app = time.time()
    print(f"[Startup] QApplication initialized in {t_app - t_imports:.4f}s")
    
    window = MainWindow()
    t_window = time.time()
    print(f"[Startup] MainWindow initialized in {t_window - t_app:.4f}s")
    print(f"[Startup] Total cold start time: {t_window - t0:.4f}s")
    
    window.show()
    sys.exit(app.exec())
