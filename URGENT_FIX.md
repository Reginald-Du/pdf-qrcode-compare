# ⚠️ 紧急修复通知

## 问题现状

部分 Windows 用户遇到错误：
```
Failed to load Python DLL 'python311.dll'
LoadLibrary: 内存不足以完成此操作。
```

**这不是真的内存不足，而是缺少系统运行库！**

---

## ✅ 立即解决方案（5 分钟）

### 步骤 1：安装 Visual C++ Redistributable（必须）

**点击下载并安装**：
```
https://aka.ms/vs/17/release/vc_redist.x64.exe
```

安装步骤：
1. 双击下载的文件
2. 如果提示"已安装"，选择"修复"
3. 等待完成
4. **重启电脑**

### 步骤 2：移动到纯英文路径

如果你的文件在这样的路径：
```
❌ C:\360安全浏览器下载\PDFQRCodeCompare-Windows\
```

请移动到：
```
✅ C:\Tools\PDFQRCodeCompare\
```

### 步骤 3：添加杀毒软件信任

**360 用户**：
1. 打开 360 安全卫士
2. 设置 → 信任与阻止
3. 添加信任文件夹：`C:\Tools\PDFQRCodeCompare\`

**Windows Defender 用户**：
1. Windows 设置 → 更新和安全 → Windows 安全中心
2. 病毒和威胁防护 → 排除项
3. 添加文件夹：`C:\Tools\PDFQRCodeCompare\`

### 步骤 4：以管理员身份运行

右键 `PDFQRCodeCompare.exe` → 以管理员身份运行

---

## 📖 详细修复指南

完整的分步指南请查看：
```
https://github.com/Reginald-Du/pdf-qrcode-compare/blob/main/USER_FIX_GUIDE.md
```

---

## 🚀 备用方案：单文件版本（即将发布）

如果上述方法仍然无法解决，我们正在构建**单文件版本**（OneFile），兼容性更好。

**预计发布时间**：1 小时内

**下载地址**（稍后更新）：
```
https://github.com/Reginald-Du/pdf-qrcode-compare/releases
```

---

## 💡 为什么会出现这个问题？

1. **Windows 系统差异**：不同 Windows 系统预装的运行库版本不同
2. **打包方式限制**：当前使用的 OneDir 模式依赖系统运行库
3. **杀毒软件干扰**：部分杀毒软件可能隔离 DLL 文件

---

## 🔧 开发者正在做什么？

1. ✅ 创建详细的修复指南（已完成）
2. 🔄 构建单文件版本（进行中）
3. 📋 优化打包配置（进行中）
4. 📝 更新安装文档（已完成）

---

## 📞 仍需帮助？

如果以上方法都尝试过仍然无法解决：

### 方案 A：使用 Python 源码运行

1. 安装 Python 3.11：https://www.python.org/downloads/
2. 下载源码：https://github.com/Reginald-Du/pdf-qrcode-compare/archive/refs/heads/main.zip
3. 解压后，在文件夹中打开命令提示符：
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

### 方案 B：提交 Issue

访问：https://github.com/Reginald-Du/pdf-qrcode-compare/issues/new

提供信息：
- Windows 版本
- 文件路径
- 是否安装了 VC++ Redistributable
- 杀毒软件类型
- 错误截图

---

## 📊 受影响范围

根据初步反馈：
- ✅ 大部分用户可通过安装 VC++ 解决
- ⚠️ 少数用户可能需要单文件版本
- 📌 路径包含中文的用户需要特别注意

---

## 🎯 快速检查清单

解决问题前，请确认：

- [ ] 已下载并安装 VC++ Redistributable (2015-2022)
- [ ] 已重启电脑
- [ ] 文件在纯英文路径（如 `C:\Tools\`）
- [ ] 已添加到杀毒软件信任列表
- [ ] Windows 10/11 64位系统
- [ ] 有管理员权限

全部勾选后，90% 的问题都能解决！

---

**更新时间**：2026-03-11 12:30
**紧急程度**：🔴 高
**预计解决**：安装 VC++ Redistributable（5 分钟）
**备用方案**：单文件版本（1 小时内）
