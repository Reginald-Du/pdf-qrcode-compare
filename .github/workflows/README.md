# GitHub Actions 自动构建说明

## 功能

此工作流会自动编译 Windows 和 macOS 两个平台的应用程序包。

## 触发条件

1. **推送到 main 分支** - 自动构建最新版本
2. **创建 Pull Request** - 在合并前测试构建
3. **创建版本标签** - 例如 `v1.0.0`，会自动创建 GitHub Release
4. **手动触发** - 在 GitHub Actions 页面手动运行

## 使用步骤

### 1. 推送代码到 GitHub

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 2. 查看构建进度

1. 访问你的 GitHub 仓库
2. 点击 **Actions** 标签
3. 查看正在运行的工作流

### 3. 下载构建产物

**方法 A：从 Actions 下载**
1. 进入完成的工作流
2. 滚动到底部 **Artifacts** 部分
3. 下载 `PDFQRCodeCompare-Windows.zip` 和 `PDFQRCodeCompare-macOS.zip`

**方法 B：发布正式版本**
```bash
# 创建版本标签
git tag v1.0.0
git push origin v1.0.0
```

然后访问仓库的 **Releases** 页面，会自动创建一个新的 Release，包含两个平台的安装包。

## 注意事项

1. **首次使用**需要确保 GitHub 仓库有 Actions 权限
2. 构建时间约 **5-10 分钟**（取决于 GitHub 服务器负载）
3. Artifacts 会保留 **30 天**
4. Release 文件永久保留

## 本地测试

如果想在本地测试构建脚本是否正确：

**Windows:**
```cmd
scripts\build_win.bat
```

**macOS:**
```bash
./scripts/build_mac.sh
```

## 常见问题

**Q: 构建失败怎么办？**
A: 查看 Actions 日志，通常是依赖安装问题。检查 requirements.txt 是否完整。

**Q: 如何修改 Python 版本？**
A: 编辑 `.github/workflows/build.yml` 中的 `python-version` 字段。

**Q: 如何只构建 Windows 版本？**
A: 修改 `matrix.os` 为 `[windows-latest]`。
