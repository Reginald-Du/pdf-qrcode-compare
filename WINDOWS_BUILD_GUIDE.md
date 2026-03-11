# Windows 编译指南

## 🎯 方法选择

### 方法 1：GitHub Actions 自动编译（最简单）⭐

**优点**：
- ✅ 无需 Windows 电脑
- ✅ 全自动，5-10 分钟完成
- ✅ 同时生成 Windows + macOS 版本
- ✅ 免费使用 GitHub 云服务器

**步骤**：

1. **推送项目到 GitHub**
   ```bash
   # 初始化仓库（如果还没有）
   git init
   git add .
   git commit -m "Initial commit"

   # 创建 GitHub 仓库并推送
   # 在 GitHub 网站创建新仓库后：
   git remote add origin https://github.com/你的用户名/pdf_qrcode_compare.git
   git branch -M main
   git push -u origin main
   ```

2. **等待自动构建**
   - 访问：`https://github.com/你的用户名/pdf_qrcode_compare/actions`
   - 等待构建完成（约 5-10 分钟）

3. **下载安装包**
   - 点击完成的工作流
   - 滚动到底部 **Artifacts** 区域
   - 下载 `PDFQRCodeCompare-Windows.zip`

4. **（可选）发布正式版本**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   然后在 Releases 页面会自动发布

---

### 方法 2：在 Windows 电脑上手动编译

**前提条件**：
- Windows 10/11
- Python 3.9+ ([下载地址](https://www.python.org/downloads/))

**步骤**：

#### 1. 安装 Python

下载并安装 Python，**勾选 "Add Python to PATH"**

#### 2. 打开命令提示符（CMD）

```cmd
Win + R → 输入 cmd → 回车
```

#### 3. 进入项目目录

```cmd
cd C:\path\to\pdf_qrcode_compare
```

#### 4. 创建虚拟环境

```cmd
python -m venv venv
```

#### 5. 激活虚拟环境

```cmd
venv\Scripts\activate
```

激活后，命令行前面会显示 `(venv)`

#### 6. 安装依赖

```cmd
pip install -r requirements.txt
pip install pyinstaller
```

#### 7. 运行构建脚本

```cmd
scripts\build_win.bat
```

#### 8. 查看输出

编译完成后，可执行文件位于：
```
dist\PDFQRCodeCompare\PDFQRCodeCompare.exe
```

---

### 方法 3：使用虚拟机

如果你只有 macOS/Linux 电脑：

**选项 A：Parallels Desktop（macOS）**
1. 安装 Parallels Desktop
2. 创建 Windows 11 虚拟机
3. 按照"方法 2"操作

**选项 B：VirtualBox（免费）**
1. 下载 VirtualBox
2. 下载 Windows 11 开发环境镜像（微软官方免费提供）
3. 按照"方法 2"操作

**选项 C：云服务器**
1. 租用 Windows 云服务器（如 AWS、Azure）
2. 远程桌面连接
3. 按照"方法 2"操作

---

## 📦 预期输出

### Windows 版本结构

```
dist/
└── PDFQRCodeCompare/
    ├── PDFQRCodeCompare.exe     # 主程序
    ├── Qt6Core.dll               # Qt 核心库
    ├── Qt6Gui.dll
    ├── Qt6Widgets.dll
    ├── python311.dll             # Python 运行时
    ├── _internal/                # 依赖库
    └── ...
```

### 文件大小

预计 **150-250 MB**（包含所有依赖）

### 分发方式

将整个 `PDFQRCodeCompare` 文件夹打包成 ZIP：
```cmd
cd dist
powershell Compress-Archive -Path PDFQRCodeCompare -DestinationPath PDFQRCodeCompare-Windows.zip
```

---

## 🔍 常见问题

### Q1: Python 命令不存在

**解决**：重新安装 Python，勾选 "Add Python to PATH"，或手动添加到环境变量。

### Q2: pip 安装依赖失败

**解决**：
```cmd
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: PyInstaller 构建失败

**解决**：
```cmd
# 清理缓存
rmdir /s /q build dist
pyinstaller --clean --noconfirm main.spec
```

### Q4: 缺少 MSVCP140.dll

**解决**：安装 [Visual C++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)

### Q5: 程序运行报错

**解决**：
```cmd
# 以控制台模式运行查看错误信息
# 修改 main.spec 中 console=True，重新构建
```

---

## 💡 推荐方案

| 场景 | 推荐方法 | 理由 |
|------|----------|------|
| 只有 macOS 电脑 | 方法 1（GitHub Actions） | 无需虚拟机，最简单 |
| 有 Windows 电脑 | 方法 2（手动编译） | 编译速度快，调试方便 |
| 团队协作 | 方法 1（GitHub Actions） | 自动化 CI/CD |
| 学习目的 | 方法 2（手动编译） | 理解构建过程 |

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 GitHub Actions 构建日志
2. 在项目仓库提交 Issue
3. 附上完整的错误信息和系统环境
