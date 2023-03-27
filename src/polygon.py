
import sys
from math import sin, cos, pi
from PySide2.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, QGraphicsPolygonItem, QGraphicsItem, QVBoxLayout, QWidget
                                ,QSlider, QMainWindow, QScrollArea,QSpinBox)
from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QPolygonF, QBrush, QColor, QPainter, QPen


class StarPolygonItem(QGraphicsPolygonItem):
    def __init__(self, num_points=5, radius=50):
        self.num_points = num_points
        self.radius = radius
        self.edge_color = QColor("transparent")
        super().__init__()
        self.update_polygon()
        self.setBrush(QBrush(QColor("blue")))
        self.setAcceptHoverEvents(True)  # Enable hover events
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, True)  # Enable position change notifications

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

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.edge_color)
        pen.setWidth(3)
        painter.setPen(pen)
        polyline = self.polygon()
        polyline.append(polyline.at(0))
        painter.drawPolyline(polyline)

    def hoverEnterEvent(self, event):
        self.edge_color = QColor("green")
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.edge_color = QColor("transparent") if not self.isSelected() else QColor("red")
        self.update()
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.edge_color = QColor("red") if value else QColor("transparent")
        elif change == QGraphicsItem.ItemPositionChange:
            print(f"Polygon position: {value}")
        return super().itemChange(change, value)
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print(f"Polygon position: {self.pos()}")   



# The rest of the code remains unchanged.


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
class StarSpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def stepBy(self, steps):
        super().stepBy(steps)
        print("hello")
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = CustomGraphicsScene()
        self.view = CustomGraphicsView(self.scene)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.view)

        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.scroll_area)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Star Polygon Example")
        #  attaching Star SpinBox to MainWindow
        self.init_star_spinbox()
        layout.addWidget(self.Star_spinBox)

    def on_Star_spinBox_value_changed(self, value):
        self.scene.star_item.set_num_points(value)

    def init_star_spinbox(self):
        self.Star_spinBox = QSpinBox()
        self.Star_spinBox.setMinimum(3)
        self.Star_spinBox.setMaximum(20)
        self.Star_spinBox.setValue(5)
        self.Star_spinBox.valueChanged.connect(self.on_Star_spinBox_value_changed)
if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())