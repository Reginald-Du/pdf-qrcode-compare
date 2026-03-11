# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

# Determine platform-specific icon
icon_file = None
if sys.platform == 'darwin':
    icon_file = 'resources/icon.icns'
elif sys.platform == 'win32':
    icon_file = 'resources/icon.ico'

# Extra datas
datas = []

# Exclude unused modules to save space
# We exclude heavy data science libraries and unused Qt modules
excludes = [
    'tkinter', 'unittest', 'email', 'http', 'xml', 'pydoc',
    'matplotlib', 'scipy', 'pandas', 'PIL', 'IPython', 'jupyter', 'notebook',
    'curses', 'distutils', 'setuptools', 'pkg_resources',
    'cv2', 'opencv-python', 'opencv-python-headless', 'ultralytics', 'torch', 'torchvision', 'qrdet', 'yolo', 'tesseract', 'pytesseract',
    
    # Exclude unused PySide6 modules to save ~50-100MB
    'PySide6.QtNetwork', 'PySide6.QtQml', 'PySide6.QtQuick', 
    'PySide6.QtWebEngine', 'PySide6.QtWebEngineWidgets', 'PySide6.QtWebEngineCore',
    'PySide6.QtSql', 'PySide6.QtTest', 'PySide6.QtMultimedia', 'PySide6.QtSensors',
    'PySide6.QtSerialPort', 'PySide6.QtXml', 'PySide6.QtSvg', 'PySide6.QtBluetooth',
    'PySide6.QtDesigner', 'PySide6.QtHelp', 'PySide6.QtLocation', 'PySide6.QtNfc',
    'PySide6.QtPositioning', 'PySide6.QtPrintSupport', 'PySide6.QtRemoteObjects',
    'PySide6.QtScxml', 'PySide6.QtStateMachine', 'PySide6.QtTextToSpeech',
    'PySide6.QtWebChannel', 'PySide6.QtWebSockets', 'PySide6.Qt3DCore',
    'PySide6.Qt3DInput', 'PySide6.Qt3DLogic', 'PySide6.Qt3DRender', 'PySide6.Qt3DExtras',
    'PySide6.Qt3DAnimation', 'PySide6.QtCharts', 'PySide6.QtDataVisualization'
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'numpy',
        'zxingcpp',
        'shapely',
        'numpy.core._multiarray_umath',
        'numpy.random.common',
        'numpy.random.bounded_integers',
        'numpy.random.entropy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDFQRCodeCompare',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file
)

# OneDir mode: Bundle everything into a directory (faster startup)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=False,
    upx_exclude=[],
    name='PDFQRCodeCompare',
)

# For macOS .app bundle
# Wraps the folder into a valid .app structure
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='PDFQRCodeCompare.app',
        icon=icon_file,
        bundle_identifier='com.example.pdfqrcodecompare',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False'
        }
    )
