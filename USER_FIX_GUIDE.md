# ⚠️ Windows DLL 错误修复指南

## 错误信息
```
Failed to load Python DLL 'python311.dll'
LoadLibrary: 内存不足以完成此操作。
```

**注意**：这个"内存不足"不是真的内存不足，而是缺少系统运行库！

---

## ✅ 解决步骤（按顺序执行）

### 步骤 1：安装 Visual C++ Redistributable（必须！）

**这是最关键的步骤，90% 的问题都是因为缺少这个运行库！**

#### 1.1 下载运行库

访问微软官方下载页面，下载以下**所有版本**：

**方式 A：一键下载包（推荐）**
- 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe
- 这是最新的 2015-2022 版本

**方式 B：下载所有版本（更彻底）**
访问：https://learn.microsoft.com/zh-cn/cpp/windows/latest-supported-vc-redist

下载并安装：
- ✅ Visual C++ 2015-2022 Redistributable (x64)
- ✅ Visual C++ 2013 Redistributable (x64)（可选）
- ✅ Visual C++ 2012 Redistributable (x64)（可选）

#### 1.2 安装步骤

1. 双击下载的 `vc_redist.x64.exe`
2. 如果提示"已安装"，选择"修复"
3. 等待安装完成
4. **重启电脑**（重要！）

---

### 步骤 2：移动到纯英文路径

从错误信息看，你的文件路径包含中文：
```
C:\360安全浏览器下载\PDFQRCodeCompare-Windows\
```

**这可能导致问题！** 请按以下步骤操作：

1. 在 C 盘或 D 盘创建纯英文文件夹：
   ```
   C:\Tools\PDFQRCodeCompare\
   ```
   或
   ```
   D:\Software\PDFQRCodeCompare\
   ```

2. 重新解压 ZIP 文件到新位置

3. 从新位置运行程序

---

### 步骤 3：检查杀毒软件

#### 360 安全卫士/360 杀毒

1. 打开 360 安全卫士
2. 点击"木马防火墙"或"实时防护"
3. 找到"隔离区"或"恢复区"
4. 查看是否有 `python311.dll` 或 `PDFQRCodeCompare.exe` 被隔离
5. 如果有，点击"恢复"并"信任"

#### 添加信任

1. 360 安全卫士 → 设置 → 信任与阻止
2. 添加信任文件夹：`C:\Tools\PDFQRCodeCompare\`
3. 添加信任程序：`PDFQRCodeCompare.exe`

#### Windows Defender

1. Windows 设置 → 更新和安全 → Windows 安全中心
2. 病毒和威胁防护 → 管理设置
3. 排除项 → 添加或删除排除项
4. 添加文件夹：`C:\Tools\PDFQRCodeCompare\`

---

### 步骤 4：以管理员身份运行

1. 右键点击 `PDFQRCodeCompare.exe`
2. 选择"以管理员身份运行"
3. 如果弹出 SmartScreen 警告：
   - 点击"更多信息"
   - 点击"仍要运行"

---

### 步骤 5：验证 DLL 文件完整性

打开命令提示符（CMD），执行：

```cmd
cd C:\Tools\PDFQRCodeCompare
dir /s python*.dll
```

应该看到类似输出：
```
_internal\python311.dll
_internal\python3.dll
```

如果没有这些文件，说明解压不完整，需要：
1. 删除当前文件夹
2. 重新下载 ZIP
3. 使用 Windows 自带的"解压缩"功能（不要用第三方工具）
4. 解压到纯英文路径

---

## 🔍 诊断工具

### 检查是否已安装 VC++ 运行库

1. 打开"控制面板" → "程序和功能"
2. 查找以下程序：
   - Microsoft Visual C++ 2015-2022 Redistributable (x64)

   如果没有找到，说明**必须安装**！

### 检查系统是否支持

- ✅ Windows 10 (64位)
- ✅ Windows 11 (64位)
- ❌ Windows 7/8（可能不兼容）
- ❌ 32位系统（不支持）

确认系统版本：
```cmd
systeminfo | findstr /C:"OS 名称" /C:"系统类型"
```

---

## 💡 如果以上步骤都无效

### 方案 A：使用 Python 源码运行（推荐）

1. 安装 Python 3.11：https://www.python.org/downloads/
2. 下载项目源码：https://github.com/Reginald-Du/pdf-qrcode-compare
3. 打开命令提示符，执行：
   ```cmd
   cd C:\path\to\pdf-qrcode-compare
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

### 方案 B：使用依赖检查工具

下载并运行 Dependency Walker：
- 官网：https://www.dependencywalker.com/
- 打开 `PDFQRCodeCompare.exe`
- 查看缺失的 DLL

### 方案 C：详细错误日志

创建批处理文件 `run_debug.bat`：
```batch
@echo off
cd /d "%~dp0"
PDFQRCodeCompare.exe > error.log 2>&1
pause
notepad error.log
```

双击运行，查看 `error.log` 中的详细错误信息。

---

## 📞 仍然需要帮助？

如果以上所有方法都尝试过仍然无法解决，请：

1. 访问项目 Issues：https://github.com/Reginald-Du/pdf-qrcode-compare/issues
2. 创建新 Issue，提供以下信息：

```
### 系统信息
- Windows 版本：[例如 Windows 11 22H2]
- 系统类型：[64位]
- 是否安装 VC++ Redistributable：[是/否]
- 杀毒软件：[例如 360、Windows Defender]

### 文件路径
- 解压位置：[例如 C:\Tools\PDFQRCodeCompare]
- 是否包含中文：[是/否]

### 已尝试的步骤
- [ ] 安装 VC++ Redistributable
- [ ] 重启电脑
- [ ] 移动到纯英文路径
- [ ] 关闭杀毒软件
- [ ] 以管理员身份运行
- [ ] 重新解压文件

### 错误截图
[粘贴完整的错误截图]

### error.log 内容
[如果有的话]
```

---

## 🎯 快速检查清单

安装运行前，确认以下所有项：

- [ ] 已下载并安装 Visual C++ 2015-2022 Redistributable (x64)
- [ ] 已重启电脑
- [ ] 文件解压到纯英文路径（无中文、无空格最佳）
- [ ] 路径不要太长（建议 < 100 字符）
- [ ] 已将程序添加到杀毒软件信任列表
- [ ] Windows 10/11 64位系统
- [ ] 有管理员权限
- [ ] _internal 文件夹完整存在
- [ ] python311.dll 文件存在于 _internal 文件夹中

全部勾选后，程序应该可以正常运行！

---

**最后更新**: 2026-03-11
**适用版本**: v1.0.0 及更高版本
