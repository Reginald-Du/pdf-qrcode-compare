# Localization Dictionary
# Using simple dictionary for easy maintenance and key lookup

TRANSLATIONS = {
    # Main Window
    "app_title": "PDF 二维码对比工具",
    "select_title": "请选择两个 PDF 文件进行对比",
    "btn_compare": "开始对比二维码",
    "btn_export": "导出报告",
    "btn_new": "新对比",
    "diff_found": "发现的差异:",
    "no_diff": "未发现差异！",
    "page_label": "第 {current} 页 / 共 {total} 页",
    "btn_prev": "上一页",
    "btn_next": "下一页",
    "btn_fit_width": "适应宽度",
    
    # Drop Zone
    "drop_title": "拖拽 PDF 到此处",
    "drop_file_a": "拖拽文件 A (原版)",
    "drop_file_b": "拖拽文件 B (修改版)",
    "btn_select_file": "选择文件",
    "btn_change_file": "更换文件",
    "dialog_select_title": "选择 PDF",
    "dialog_file_filter": "PDF 文件 (*.pdf)",
    
    # Progress
    "processing": "正在处理...",
    "scan_a": "正在扫描文件 A...",
    "scan_a_progress": "正在扫描文件 A ({p}%)...",
    "scan_b": "正在扫描文件 B...",
    "scan_b_progress": "正在扫描文件 B ({p}%)...",
    "comparing": "正在对比...",
    "done": "完成！",
    
    # Dialogs & Messages
    "success_title": "成功",
    "report_saved": "报告已成功保存！",
    "error_title": "错误",
    "save_error": "保存报告失败: {e}",
    "open_error": "无法打开 PDF: {e}",
    
    # Diff Types
    "diff_match": "匹配",
    "diff_mismatch": "内容不一致",
    "diff_only_a": "仅在 A 中",
    "diff_only_b": "仅在 B 中",
    "diff_tooltip_match": "匹配: {content}",
    "diff_tooltip_mismatch": "不一致: {content}",
    "diff_tooltip_unique_a": "A 独有: {content}",
    "diff_tooltip_unique_b": "B 独有: {content}",
    
    # Report CSV Header
    "csv_header": "页码,类型,内容_A,内容_B\n"
}

def tr(key, **kwargs):
    """Translate key to Chinese, supporting format arguments."""
    text = TRANSLATIONS.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
