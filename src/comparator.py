from dataclasses import dataclass
from typing import List, Optional
from src.pdf_processor import QRResult

@dataclass
class DiffItem:
    page_index: int
    type: str
    content_a: Optional[str] = None
    content_b: Optional[str] = None
    rect_a: Optional[List] = None
    rect_b: Optional[List] = None
    diff_details: Optional[str] = None

def compare_qr_lists(list_a: List[QRResult], list_b: List[QRResult], strict_order: bool = True) -> List[DiffItem]:
    diffs = []
    pages_a = {}
    for item in list_a: pages_a.setdefault(item.page_index, []).append(item)
    pages_b = {}
    for item in list_b: pages_b.setdefault(item.page_index, []).append(item)
    all_pages = sorted(list(set(pages_a.keys()) | set(pages_b.keys())))
    
    for page in all_pages:
        qrs_a = pages_a.get(page, [])
        qrs_b = pages_b.get(page, [])
        max_len = max(len(qrs_a), len(qrs_b))
        
        for i in range(max_len):
            qr_a = qrs_a[i] if i < len(qrs_a) else None
            qr_b = qrs_b[i] if i < len(qrs_b) else None
            
            if qr_a and qr_b:
                is_match = False
                details = []
                if qr_a.content == qr_b.content: is_match = True
                else: details.append("Content Mismatch")
                    
                if qr_a.content_hash != qr_b.content_hash and "Content Mismatch" not in details:
                    details.append("Hash Mismatch")
                
                if not is_match:
                    diff_keys = []
                    all_keys = set(qr_a.url_params.keys()) | set(qr_b.url_params.keys())
                    for k in all_keys:
                        val_a = qr_a.url_params.get(k)
                        val_b = qr_b.url_params.get(k)
                        if val_a != val_b: diff_keys.append(f"{k}: {val_a} vs {val_b}")
                    if diff_keys: details.append(f"Param Diff: {'; '.join(diff_keys)}")
                
                if is_match:
                    diffs.append(DiffItem(page, "MATCH", qr_a.content, qr_b.content, qr_a.polygon, qr_b.polygon))
                else:
                    diffs.append(DiffItem(page, "CONTENT_MISMATCH", qr_a.content, qr_b.content, qr_a.polygon, qr_b.polygon, " | ".join(details)))
            elif qr_a and not qr_b:
                diffs.append(DiffItem(page, "ONLY_IN_A", content_a=qr_a.content, rect_a=qr_a.polygon, diff_details=f"Missing corresponding element in B at index {i}"))
            elif not qr_a and qr_b:
                diffs.append(DiffItem(page, "ONLY_IN_B", content_b=qr_b.content, rect_b=qr_b.polygon, diff_details=f"Extra element in B at index {i}"))
    return diffs
