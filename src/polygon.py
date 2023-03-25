import sys
from math import sin, cos, pi
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QGraphicsItem, QVBoxLayout, QWidget, QSlider
from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QPolygonF, QBrush, QColor, QPainter


class StarPolygonItem(QGraphicsPolygonItem):
    def __init__(self, num_points=5, radius=50):
        self.num_points = num_points
        self.radius = radius
        super().__init__()
        self.update_polygon()

    def update_polygon(self):
        star_polygon = QPolygonF()
        for i in range(self.num_points * 2):
            factor = 1.0 if i % 2 == 0 else 0.5
            angle = (2 * pi * i) / (self.num_points * 2)
            x = self.radius * factor * cos(angle)
            y = self.radius * factor * sin(angle)
            star_polygon.append(QPointF(x, y))
        self.setPolygon(star_polygon)

    def set_num_points(self, num_points):
        self.num_points = num_points
        self.update_polygon()

def on_slider_value_changed(value):
    star_item.set_num_points(value)
    star_item.update_polygon()


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

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

    slider = QSlider(Qt.Horizontal)
    slider.setMinimum(3)
    slider.setMaximum(20)
    slider.setValue(5)
    slider.valueChanged.connect(on_slider_value_changed)

    layout = QVBoxLayout()
    layout.addWidget(view)
    layout.addWidget(slider)

    container = QWidget()
    container.setLayout(layout)
    container.setWindowTitle("Star Polygon Example")
    container.show()

    sys.exit(app.exec_())
