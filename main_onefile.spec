# -*- mode: python ; coding: utf-8 -*-
# OneFile mode - 单文件可执行版本（更好的兼容性）
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
excludes = [
    'tkinter', 'unittest', 'email', 'http', 'xml', 'pydoc',
    'matplotlib', 'scipy', 'pandas', 'PIL', 'IPython', 'jupyter', 'notebook',
    'curses', 'distutils', 'setuptools', 'pkg_resources',
    'cv2', 'opencv-python', 'opencv-python-headless', 'ultralytics', 'torch', 'torchvision', 'qrdet', 'yolo', 'tesseract', 'pytesseract',

    # Exclude unused PySide6 modules
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
        'shapely.geometry',
        'numpy.core._multiarray_umath',
        'numpy.random.common',
        'numpy.random.bounded_integers',
        'numpy.random.entropy',
        'fitz',
        'multiprocessing',
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

# OneFile mode: Everything in a single executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDFQRCodeCompare',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,  # UPX can cause issues with some antivirus
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file
)

# For macOS .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='PDFQRCodeCompare.app',
        icon=icon_file,
        bundle_identifier='com.example.pdfqrcodecompare',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'LSBackgroundOnly': 'False'
        }
    )
