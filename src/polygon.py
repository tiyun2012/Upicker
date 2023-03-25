import sys
from math import sin, cos, pi
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem,QGraphicsItem 
from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QPolygonF, QBrush, QColor,QPainter

class StarPolygonItem(QGraphicsPolygonItem):
    def __init__(self, num_points=5, radius=50):
        star_polygon = QPolygonF()
        for i in range(num_points * 2):
            factor = 1.0 if i % 2 == 0 else 0.5
            angle = (2 * pi * i) / (num_points * 2)
            x = radius * factor * cos(angle)
            y = radius * factor * sin(angle)
            star_polygon.append(QPointF(x, y))

        super().__init__(star_polygon)

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            # Zoom in
            self.scale(zoom_factor, zoom_factor)
        else:
            # Zoom out
            self.scale(1 / zoom_factor, 1 / zoom_factor)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    scene = QGraphicsScene(QRectF(0, 0, 2000, 2000))

    star_item = StarPolygonItem()
    star_item.setPos(1000, 1000)
    star_item.setBrush(QBrush(QColor("blue")))
    star_item.setFlag(QGraphicsItem.ItemIsMovable)
    star_item.setFlag(QGraphicsItem.ItemIsSelectable)

    scene.addItem(star_item)

    view = CustomGraphicsView(scene)
    view.setRenderHint(QPainter.Antialiasing)
    view.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
    view.setSceneRect(scene.sceneRect())
    view.setWindowTitle("Star Polygon Example")
    view.show()

    sys.exit(app.exec_())
