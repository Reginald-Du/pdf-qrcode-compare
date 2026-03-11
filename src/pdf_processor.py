import fitz, numpy as np, multiprocessing, hashlib, zxingcpp
from urllib.parse import urlparse, parse_qs
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
from shapely.geometry import Polygon

@dataclass
class QRResult:
    page_index: int
    content: str
    polygon: List[Tuple[int, int]]
    content_hash: str = ""
    url_params: Dict[str, Any] = field(default_factory=dict)

def process_single_page(args):
    f_path, p_idx = args
    results = []
    try:
        doc = fitz.open(f_path)
        page = doc.load_page(p_idx)
        zoom = 6.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY, alpha=False)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        doc.close()

        try:
            raw_res = zxingcpp.read_barcodes(img)
        except:
            raw_res = []

        found_polys = []
        for r in raw_res:
            txt = r.text
            if not txt: continue
            
            pos = r.position
            pts = [
                (pos.top_left.x, pos.top_left.y),
                (pos.top_right.x, pos.top_right.y),
                (pos.bottom_right.x, pos.bottom_right.y),
                (pos.bottom_left.x, pos.bottom_left.y)
            ]
            
            curr_poly = Polygon(pts) if len(pts) >= 3 else None
            is_dup = False
            
            if curr_poly and curr_poly.is_valid:
                for exist_poly in found_polys:
                    try:
                        inter = curr_poly.intersection(exist_poly).area
                        union = curr_poly.union(exist_poly).area
                        if union > 0 and (inter / union) > 0.5:
                            is_dup = True
                            break
                    except: pass
            
            if not is_dup:
                if curr_poly and curr_poly.is_valid: found_polys.append(curr_poly)
                
                h_val = hashlib.sha256(txt.encode('utf-8')).hexdigest()
                params = {}
                try:
                    p = urlparse(txt)
                    for k, v in parse_qs(p.query).items(): params[k] = v[0] if v else ""
                    if '?' in p.fragment:
                        for k, v in parse_qs(p.fragment.split('?', 1)[1]).items(): params[k] = v[0] if v else ""
                except: pass

                results.append(QRResult(p_idx + 1, txt, pts, h_val, params))
    except Exception as e:
        print(f"Error p{p_idx+1}: {e}")
    return results

class PDFProcessor:
    def process_pdf(self, path: str, cb=None) -> List[QRResult]:
        try:
            doc = fitz.open(path)
            total = len(doc)
            doc.close()
            all_res = []
            args = [(path, i) for i in range(total)]
            with multiprocessing.Pool() as pool:
                for i, res in enumerate(pool.imap_unordered(process_single_page, args)):
                    all_res.extend(res)
                    if cb: cb(int(((i + 1) / total) * 100))
            
            all_res.sort(key=lambda x: (x.page_index, min(p[1] for p in x.polygon) if x.polygon else 0, min(p[0] for p in x.polygon) if x.polygon else 0))
            if cb: cb(100)
            return all_res
        except Exception as e:
            print(f"Fatal: {e}")
            raise e
