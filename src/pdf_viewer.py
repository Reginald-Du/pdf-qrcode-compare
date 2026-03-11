from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem
from PySide6.QtGui import QPixmap, QPen, QColor, QBrush, QPainter, QPolygonF
from PySide6.QtCore import Qt, QPointF

class PDFPageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setBackgroundBrush(QBrush(QColor("#e0e0e0")))

    def set_zoom(self, scale_factor):
        """
        Set the zoom level (e.g., 1.0 = 100%, 2.0 = 200%)
        """
        # Reset transform to identity then scale
        self.resetTransform()
        self.scale(scale_factor, scale_factor)

    def set_content(self, pixmap, overlays):
        """
        overlays: list of (polygon_points, color_hex, tooltip_text)
        """
        self.scene.clear()
        if pixmap:
            self.scene.addPixmap(pixmap)
            self.setSceneRect(0, 0, pixmap.width(), pixmap.height())

        for poly_points, color, tooltip in overlays:
            if not poly_points:
                continue
                
            qpoints = [QPointF(float(x), float(y)) for x, y in poly_points]
            polygon = QPolygonF(qpoints)
            
            item = QGraphicsPolygonItem(polygon)
            
            pen = QPen(QColor(color))
            pen.setWidth(3)
            item.setPen(pen)
            
            # Transparent fill
            c = QColor(color)
            c.setAlpha(50)
            item.setBrush(QBrush(c))
            
            item.setToolTip(tooltip)
            self.scene.addItem(item)
