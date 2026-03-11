# Windows 版本错误修复

## 问题描述

错误信息：
```
Failed to load Python DLL
'C:\Users\chenruimin\Downloads\PDFQRCodeCompare-Windows\PDFQRCodeCompare\_internal\python311.dll'
LoadLibrary: 找不到指定的模块。
```

## 原因分析

这个问题通常由以下原因引起：
1. ❌ 缺少 **Visual C++ Redistributable** 运行库
2. ❌ Windows Defender 或杀毒软件隔离了文件
3. ❌ PyInstaller 打包配置问题

## 🔧 立即修复（用户端）

### 方案 1：安装 Visual C++ Redistributable（推荐）

**下载并安装**：
- [Microsoft Visual C++ Redistributable (最新版本)](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)
- 或直接下载：https://aka.ms/vs/17/release/vc_redist.x64.exe

**安装步骤**：
1. 下载 `vc_redist.x64.exe`
2. 双击运行
3. 点击"安装"
4. 重启电脑
5. 重新运行 PDFQRCodeCompare.exe

### 方案 2：检查杀毒软件

1. 打开 Windows Defender 安全中心
2. 检查"病毒和威胁防护" → "保护历史记录"
3. 如果 python311.dll 被隔离，添加为信任文件
4. 或者将整个 PDFQRCodeCompare 文件夹添加到排除项

### 方案 3：重新解压

1. 将 ZIP 文件解压到 **不含中文** 的路径
   - ❌ 错误：`C:\Users\陈睿民\Downloads\`
   - ✅ 正确：`C:\Tools\PDFQRCodeCompare\`
2. 右键 ZIP 文件 → "全部提取"
3. 选择英文路径解压

## 🛠️ 开发者修复（改进打包）

我们需要修改 PyInstaller 配置来避免这个问题。
