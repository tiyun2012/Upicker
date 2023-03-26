import sys
from math import sin, cos, pi
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QGraphicsItem, QVBoxLayout, QWidget, QSlider, QMainWindow, QScrollArea
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


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(QRectF(0, 0, 2000, 2000))

        self.star_item = StarPolygonItem()
        self.star_item.setPos(1000, 1000)
        self.star_item.setBrush(QBrush(QColor("blue")))
        self.star_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.star_item.setFlag(QGraphicsItem.ItemIsSelectable)

        self.addItem(self.star_item)


class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = CustomGraphicsScene()
        self.view = CustomGraphicsView(self.scene)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.view)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(3)
        self.slider.setMaximum(20)
        self.slider.setValue(5)
        self.slider.valueChanged.connect(self.on_slider_value_changed)

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.slider)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("Star Polygon Example")

    def on_slider_value_changed(self, value):
        self.scene.star_item.set_num_points(value)
        self.scene.star_item.update_polygon()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
