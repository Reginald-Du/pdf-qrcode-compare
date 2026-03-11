# PDF QR Code Comparison Tool

A cross-platform desktop application to compare QR codes between two PDF files.

## Features

-   **Cross-Platform:** Works on macOS and Windows (Python/Qt).
-   **PDF Parsing:** Supports standard PDF files.
-   **QR Detection:** Uses high-performance ZXing-CPP to find QR codes with precision.
-   **Visual Comparison:** Side-by-side view with synchronized scrolling.
-   **Diff Highlighting:**
    -   **Green:** Match.
    -   **Red:** Content Mismatch.
    -   **Blue:** Unique to File A.
    -   **Orange:** Unique to File B.
-   **Export:** Generate CSV reports of differences.

## Installation

1.  Ensure you have Python 3.9+ installed.
2.  Create a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # or
    .\venv\Scripts\activate   # Windows
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the application:
    ```bash
    python main.py
    ```
2.  Drag and drop your "Original" PDF (File A) into the left box.
3.  Drag and drop your "Modified" PDF (File B) into the right box.
4.  Click **Compare QR Codes**.
5.  Wait for processing to complete.
6.  Review differences in the sidebar or visual view.
7.  Click **Export Report** to save a CSV summary.

## Troubleshooting

-   **QR Not Detected:** The tool uses `ZXing-CPP` with 6.0x high-precision rendering. If detection is still poor, check if the PDF pages are valid images.
-   **Performance:** Processing large PDFs with many pages can take time. The interface shows a progress bar.

## Tech Stack

-   **GUI:** PySide6 (Qt)
-   **PDF Engine:** PyMuPDF (fitz)
-   **QR Engine:** ZXing-CPP
-   **Geometry:** Shapely

## Building for Distribution

### 🚀 自动化构建（推荐）

项目已配置 GitHub Actions 自动构建。只需推送代码到 GitHub，系统会自动编译 Windows 和 macOS 两个版本。

**快速开始：**
```bash
# 推送代码
git push origin main

# 或发布正式版本
git tag v1.0.0
git push origin v1.0.0
```

然后在 GitHub 仓库的 **Actions** 标签查看构建进度，在 **Releases** 页面下载安装包。

详细说明请查看：[.github/workflows/README.md](.github/workflows/README.md)

### 🔨 手动构建

**macOS**
```bash
./scripts/build_mac.sh
```

**Windows**
```bat
scripts\build_win.bat
```

输出目录：`dist/`

### Web Distribution
A sample download page is available in `dist_web/index.html`. It automatically detects the user's OS and serves the appropriate link.

## Running Tests

To run the automated test suite (including QR detection verification):

```bash
python -m unittest discover -s tests -v
```
