# 🚨 关键修复：OneFile 版本仍报错

## 问题现状

即使使用 OneFile 版本，仍然出现：
```
Failed to load Python DLL 'python311.dll'
LoadLibrary: 内存不足以完成此操作。
```

**重要**：这不是内存问题，是缺少 Microsoft Visual C++ 运行库！

---

## ✅ 必须执行的步骤

### 步骤 1：安装所有版本的 VC++ Redistributable（必须！）

**下载并安装以下所有版本**：

#### Visual C++ 2015-2022 Redistributable (x64) - 最重要！
```
https://aka.ms/vs/17/release/vc_redist.x64.exe
```

#### Visual C++ 2013 Redistributable (x64)
```
https://aka.ms/highdpimfc2013x64enu
```

#### 或者使用一键安装包
下载 "All in One Runtimes" 安装包：
```
https://www.computerbase.de/downloads/systemtools/all-in-one-runtimes/
```

**安装步骤**：
1. 双击每个安装包
2. 如果提示"已安装"，选择**"修复"**
3. 安装完所有版本后，**必须重启电脑**
4. 重启后再运行程序

---

### 步骤 2：清理临时目录

PyInstaller OneFile 会解压到临时目录，可能有残留文件导致问题。

**清理步骤**：
1. 按 `Win + R`
2. 输入：`%TEMP%`
3. 删除所有 `_MEI*` 开头的文件夹
4. 如果无法删除，重启后再删除

---

### 步骤 3：检查 Windows 版本

**查看系统版本**：
1. 按 `Win + R`
2. 输入：`winver`
3. 查看版本信息

**最低要求**：
- ✅ Windows 10 (1809 或更高)
- ✅ Windows 11
- ⚠️ Windows 8.1（可能不兼容）
- ❌ Windows 7（不支持）

**如果是 Windows 7/8**：
- 升级到 Windows 10/11
- 或使用 Python 源码运行（见方案 4）

---

### 步骤 4：禁用杀毒软件（临时）

**360 安全卫士用户**：
1. 打开 360 安全卫士
2. 右上角设置 → 实时防护
3. 临时关闭"文件实时防护"
4. 运行程序测试
5. 如果成功，将程序添加到白名单

**Windows Defender**：
1. Windows 设置 → 更新和安全
2. Windows 安全中心 → 病毒和威胁防护
3. 管理设置 → 关闭"实时保护"（临时）
4. 运行程序测试

---

### 步骤 5：以管理员身份运行

1. 右键 `PDFQRCodeCompare.exe`
2. 选择"以管理员身份运行"
3. 如果弹出 UAC，点击"是"

---

## 🛠️ 高级诊断工具

### 检查缺失的 DLL

下载 Dependency Walker：
```
https://www.dependencywalker.com/
```

1. 打开 Dependency Walker
2. 拖入 `PDFQRCodeCompare.exe`
3. 查看红色标记的缺失 DLL
4. 根据缺失的 DLL 安装对应的运行库

### 使用 dumpbin 检查依赖

在命令提示符中：
```cmd
cd C:\path\to\PDFQRCodeCompare
dumpbin /dependents PDFQRCodeCompare.exe
```

---

## 🎯 终极解决方案：从源码运行

如果以上方法都无效，使用源码运行是最可靠的方式：

### 步骤 1：安装 Python

下载 Python 3.11：
```
https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
```

安装时**必须勾选**：
- ✅ Add Python to PATH

### 步骤 2：下载项目源码

访问：
```
https://github.com/Reginald-Du/pdf-qrcode-compare
```

点击绿色的 "Code" 按钮 → Download ZIP

### 步骤 3：安装依赖

解压源码后，打开命令提示符（CMD）：
```cmd
cd C:\path\to\pdf-qrcode-compare
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 步骤 4：运行程序

```cmd
python main.py
```

**优点**：
- ✅ 100% 兼容性
- ✅ 不依赖 VC++ 打包
- ✅ 可以调试错误
- ✅ 更新方便

---

## 🔍 问题排查清单

在提交 Issue 前，请确认以下所有项：

- [ ] 已安装 Visual C++ 2015-2022 Redistributable (x64)
- [ ] 已重启电脑
- [ ] Windows 10/11 64位系统
- [ ] 已清理 %TEMP%\_MEI* 文件夹
- [ ] 文件路径为纯英文（如 C:\Tools\）
- [ ] 已以管理员身份运行
- [ ] 已关闭杀毒软件实时防护（临时）
- [ ] 已将程序添加到杀毒软件白名单
- [ ] 检查了 Dependency Walker 的结果

---

## 📞 如果仍然无法解决

### 收集诊断信息

在命令提示符中运行：
```cmd
systeminfo > system_info.txt
wmic os get Caption,Version,BuildNumber,OSArchitecture > os_info.txt
```

### 提交 Issue

访问：https://github.com/Reginald-Du/pdf-qrcode-compare/issues/new

提供以下信息：
1. Windows 版本（从 `winver` 获取）
2. 是否安装了 VC++ Redistributable
3. 是否以管理员身份运行
4. 杀毒软件类型
5. 文件路径
6. Dependency Walker 截图（如果有）
7. system_info.txt 和 os_info.txt 内容

---

## 🎓 为什么会这样？

### OneFile 不是万能的

OneFile 模式虽然打包了所有 Python 依赖，但仍然需要：
1. **Microsoft Visual C++ Runtime** - 系统级 DLL
2. **Windows API** - 操作系统接口
3. **内核库** - kernel32.dll, ntdll.dll 等

这些是**无法打包进 exe 的**，必须由操作系统提供。

### python311.dll 的依赖链

```
PDFQRCodeCompare.exe
└── python311.dll
    ├── VCRUNTIME140.dll (需要 VC++ 2015-2022)
    ├── MSVCP140.dll (需要 VC++ 2015-2022)
    ├── api-ms-win-crt-runtime-l1-1-0.dll (需要 Universal CRT)
    └── kernel32.dll (系统自带)
```

如果缺少任何一个，就会报"内存不足"错误。

---

## 💡 最佳实践

### 对于开发者

1. 文档中明确说明系统要求
2. 提供安装脚本自动安装 VC++ Runtime
3. 考虑创建 MSI 安装程序（自动安装依赖）
4. 提供源码运行选项

### 对于用户

1. 优先尝试源码运行（最可靠）
2. 确保系统运行库完整
3. 使用 Windows 10/11
4. 保持系统更新

---

**创建时间**: 2026-03-11 13:00
**严重程度**: 🔴 Critical
**影响范围**: Windows 用户
**推荐方案**: 安装 VC++ Runtime + 从源码运行
