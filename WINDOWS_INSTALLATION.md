# Windows 安装指南

## ⚠️ 首次运行前必读

### 系统要求

- ✅ Windows 10 或 Windows 11（64位）
- ✅ **Visual C++ Redistributable**（必须安装）

## 🔧 安装步骤

### 步骤 1：安装 Visual C++ Redistributable（必需）

**为什么需要？**
Windows 版本依赖 Microsoft Visual C++ 运行库。大多数 Windows 系统已预装，但如果缺失会导致程序无法启动。

**下载安装**：

1. 访问微软官方下载页：
   https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

2. 或直接下载（推荐）：
   https://aka.ms/vs/17/release/vc_redist.x64.exe

3. 双击运行 `vc_redist.x64.exe`
4. 点击"安装"或"修复"
5. 等待安装完成
6. **重启电脑**（重要）

### 步骤 2：下载并解压程序

1. **下载** `PDFQRCodeCompare-Windows.zip`

2. **解压到合适位置**
   - ✅ 推荐：`C:\Program Files\PDFQRCodeCompare\`
   - ✅ 推荐：`C:\Tools\PDFQRCodeCompare\`
   - ✅ 推荐：`D:\Software\PDFQRCodeCompare\`
   - ❌ 避免：含有中文的路径（如 `C:\Users\陈睿民\`）
   - ❌ 避免：太深的路径（超过 200 字符）

3. **右键 ZIP 文件** → 选择"全部提取..."

### 步骤 3：首次运行

1. 进入解压后的文件夹：
   ```
   PDFQRCodeCompare/
   ├── PDFQRCodeCompare.exe   ← 双击运行
   └── _internal/             ← 依赖文件
   ```

2. 双击 `PDFQRCodeCompare.exe`

3. 如果 Windows SmartScreen 弹出警告：
   - 点击"更多信息"
   - 点击"仍要运行"

## 🐛 常见问题

### 问题 1：提示 "找不到 python311.dll"

**错误信息**：
```
Failed to load Python DLL 'python311.dll'
LoadLibrary: 找不到指定的模块。
```

**解决方案**：
1. ✅ 安装 Visual C++ Redistributable（见步骤 1）
2. ✅ 重启电脑
3. ✅ 检查杀毒软件是否隔离了文件

### 问题 2：Windows Defender 报毒

**原因**：
PyInstaller 打包的程序有时会被误报为病毒。这是误报，程序完全安全。

**解决方案**：
1. 打开 Windows 安全中心
2. 点击"病毒和威胁防护"
3. 点击"保护历史记录"
4. 找到被隔离的文件
5. 选择"允许"或"恢复"
6. 或将程序文件夹添加到排除项：
   - 设置 → 更新和安全 → Windows 安全中心
   - 病毒和威胁防护 → 管理设置
   - 排除项 → 添加或删除排除项
   - 添加文件夹：选择 `PDFQRCodeCompare` 文件夹

### 问题 3：双击没反应

**可能原因**：
- 缺少 VC++ 运行库
- 杀毒软件阻止
- 文件损坏

**解决方案**：
1. 以管理员身份运行：
   - 右键 `PDFQRCodeCompare.exe`
   - 选择"以管理员身份运行"

2. 查看错误信息（控制台模式）：
   - 打开命令提示符（CMD）
   - 进入程序目录：`cd C:\path\to\PDFQRCodeCompare`
   - 运行：`PDFQRCodeCompare.exe`
   - 查看输出的错误信息

3. 检查防火墙和杀毒软件

### 问题 4：路径包含中文导致问题

**错误现象**：
程序无法正常读取文件或启动失败

**解决方案**：
将程序解压到纯英文路径，例如：
- ✅ `C:\Tools\PDFQRCodeCompare\`
- ❌ `C:\Users\陈睿民\Downloads\PDF比对工具\`

## 📦 文件说明

```
PDFQRCodeCompare/
├── PDFQRCodeCompare.exe         # 主程序（双击运行）
└── _internal/                   # 程序依赖文件（不要删除）
    ├── python311.dll            # Python 运行时
    ├── Qt6Core.dll              # Qt 框架
    ├── Qt6Gui.dll
    ├── Qt6Widgets.dll
    └── ... (其他依赖库)
```

**重要**：不要删除 `_internal` 文件夹或其中的任何文件！

## 🚀 创建桌面快捷方式

1. 右键 `PDFQRCodeCompare.exe`
2. 选择"发送到" → "桌面快捷方式"
3. （可选）重命名快捷方式为 "PDF QR 比对工具"

## 🔒 安全性说明

### 为什么 Windows Defender 报警？

1. **PyInstaller 打包特征**：使用 PyInstaller 打包的程序会被部分杀毒软件误报
2. **未签名**：程序没有数字签名证书（需要付费购买）
3. **压缩和加密**：PyInstaller 对代码进行了压缩，某些杀软误认为是恶意行为

### 程序是否安全？

✅ **完全安全**：
- 开源项目，代码公开在 GitHub
- 不联网，不收集任何信息
- 仅在本地处理 PDF 文件
- 可通过源码验证安全性

### 如何验证？

1. 查看源代码：https://github.com/Reginald-Du/pdf-qrcode-compare
2. 本地从源码构建（见 WINDOWS_BUILD_GUIDE.md）
3. 使用 VirusTotal 扫描：https://www.virustotal.com

## 💡 性能优化

### 首次启动较慢？

首次运行时，Windows 会扫描和验证程序文件，需要 10-30 秒。

**加速方法**：
1. 将程序文件夹添加到 Windows Defender 排除项
2. 安装到 SSD 硬盘
3. 关闭不必要的杀毒软件实时监控

### 处理大文件卡顿？

如果 PDF 文件很大（>100MB）或页数很多（>100页）：
1. 关闭其他占用内存的程序
2. 耐心等待，程序会显示进度条
3. 考虑升级电脑内存

## 📞 获取帮助

如果以上方法都无法解决问题：

1. **查看详细错误**：
   ```cmd
   cd C:\path\to\PDFQRCodeCompare
   PDFQRCodeCompare.exe > error.log 2>&1
   notepad error.log
   ```

2. **在 GitHub 提交 Issue**：
   https://github.com/Reginald-Du/pdf-qrcode-compare/issues

   提供以下信息：
   - Windows 版本（Win10/Win11）
   - 完整的错误信息
   - 是否安装了 VC++ Redistributable
   - 杀毒软件信息

3. **尝试从源码运行**（开发者）：
   参考 WINDOWS_BUILD_GUIDE.md

## ✅ 安装检查清单

安装前请确认：

- [ ] Windows 10/11 64位系统
- [ ] 已安装 Visual C++ Redistributable
- [ ] 已重启电脑
- [ ] 解压到纯英文路径
- [ ] 杀毒软件已添加排除项
- [ ] 有足够的磁盘空间（至少 500MB）

全部勾选后，程序应该可以正常运行！

---

**版本**: 1.0.0
**更新日期**: 2026-03-11
**项目主页**: https://github.com/Reginald-Du/pdf-qrcode-compare
