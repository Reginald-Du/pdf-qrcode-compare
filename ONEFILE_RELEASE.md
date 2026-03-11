# 🎉 OneFile 版本已发布！

## ✅ 新版本说明

为了解决 Windows DLL 加载问题，我们现在提供**两个 Windows 版本**：

### 版本 1：OneDir（原版，74 MB）
- 文件：`PDFQRCodeCompare-Windows.zip`
- 结构：文件夹 + 多个 DLL 文件
- 优点：启动较快
- 缺点：需要安装 VC++ Redistributable

### 版本 2：OneFile（新版，73 MB）⭐ **推荐**
- 文件：`PDFQRCodeCompare-Windows-OneFile.zip`
- 结构：单个 exe 文件（77 MB）
- 优点：**更好的兼容性**，减少 DLL 问题
- 缺点：首次运行稍慢（解压临时文件）

---

## 📥 下载地址

### OneFile 版本（推荐给遇到问题的用户）

**从 Actions 下载**：
```
https://github.com/Reginald-Du/pdf-qrcode-compare/actions/runs/22937071960
```

滚动到底部 **Artifacts** 区域，下载：
- `PDFQRCodeCompare-Windows` → 包含两个版本

**本地位置**：
```
downloads-onefile/PDFQRCodeCompare-Windows/PDFQRCodeCompare-Windows-OneFile.zip
```

---

## 🚀 使用 OneFile 版本

### 步骤 1：解压

解压 `PDFQRCodeCompare-Windows-OneFile.zip`，得到：
```
PDFQRCodeCompare-OneFile/
├── PDFQRCodeCompare.exe  (77 MB) ← 这是主程序
└── README.txt
```

### 步骤 2：移动到纯英文路径

将 `PDFQRCodeCompare.exe` 移动到：
```
✅ C:\Tools\PDFQRCodeCompare.exe
❌ C:\360安全浏览器下载\
```

### 步骤 3：首次运行

1. **仍然建议安装 VC++ Redistributable**（虽然 OneFile 版本不太需要）：
   https://aka.ms/vs/17/release/vc_redist.x64.exe

2. 右键 `PDFQRCodeCompare.exe` → **以管理员身份运行**

3. 如果 Windows SmartScreen 阻止：
   - 点击"更多信息"
   - 点击"仍要运行"

4. **首次运行会较慢**（10-30秒）
   - 程序正在解压临时文件到系统临时目录
   - 后续运行会更快

### 步骤 4：添加杀毒软件信任

**360 用户**：
- 设置 → 信任与阻止 → 添加信任文件：`C:\Tools\PDFQRCodeCompare.exe`

**Windows Defender**：
- Windows 安全中心 → 排除项 → 添加文件

---

## 🔧 OneFile vs OneDir 对比

| 特性 | OneFile (新) | OneDir (原) |
|------|-------------|------------|
| 文件结构 | 单文件 | 文件夹 |
| 大小 | 77 MB | 74 MB（含 _internal） |
| 兼容性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 首次启动 | 较慢 (10-30秒) | 快 |
| 后续启动 | 正常 | 快 |
| DLL 问题 | 极少 | 可能出现 |
| 临时空间 | 需要 ~150MB | 不需要 |
| 推荐场景 | 有 DLL 问题的用户 | 系统环境完整的用户 |

---

## 💡 技术说明

### OneFile 工作原理

1. **打包时**：PyInstaller 将所有依赖打包进单个 exe
2. **运行时**：
   - 首次运行：解压到 `%TEMP%\_MEI*` 临时目录
   - 加载所有依赖
   - 运行主程序
3. **关闭后**：临时文件保留在系统临时目录
4. **再次运行**：直接使用已解压的临时文件（更快）

### 为什么更兼容？

- ✅ 所有 DLL 打包在 exe 内部
- ✅ 不依赖外部文件
- ✅ 减少路径相关问题
- ✅ 避免杀毒软件隔离个别 DLL

### 为什么首次慢？

- 需要解压 ~150MB 的文件到临时目录
- 验证文件完整性
- 创建运行环境

---

## 🎯 推荐使用场景

### 使用 OneFile 版本（单文件）

- ✅ 遇到 "python311.dll" 错误
- ✅ 遇到 "内存不足" 错误
- ✅ 没有安装 VC++ Redistributable
- ✅ Windows 7/8 系统（不推荐，但可尝试）
- ✅ 便携使用（U盘）
- ✅ 简单分发

### 使用 OneDir 版本（文件夹）

- ✅ 系统已安装 VC++ Redistributable
- ✅ 需要频繁启动（启动更快）
- ✅ 磁盘空间紧张（不占用临时空间）
- ✅ Windows 10/11 完整系统

---

## 📊 构建信息

- **构建 ID**: 22937071960
- **构建时间**: 2026-03-11 12:40
- **Windows 构建时长**: 3分45秒
- **macOS 构建时长**: 1分49秒
- **Python 版本**: 3.11.9
- **PyInstaller**: 最新版本

---

## 🆕 未来计划

### v1.1.0（计划中）

- [ ] 创建新的 Release v1.1.0
- [ ] 包含 OneFile 版本
- [ ] 更新安装文档
- [ ] 添加版本选择指南

### v1.2.0（未来）

- [ ] 优化 OneFile 启动速度
- [ ] 添加数字签名（消除 SmartScreen 警告）
- [ ] 创建 MSI 安装程序
- [ ] 自动检测系统环境并推荐版本

---

## 📞 反馈

如果 OneFile 版本解决了你的问题，请反馈：
https://github.com/Reginald-Du/pdf-qrcode-compare/issues

---

**发布时间**: 2026-03-11 12:48
**状态**: ✅ 可用
**推荐**: ⭐⭐⭐⭐⭐ 强烈推荐给遇到 DLL 问题的用户
