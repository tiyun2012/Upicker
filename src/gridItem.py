# import sys
# from PySide2.QtCore import Qt, QPointF,QPoint
# from PySide2.QtGui import QPen, QColor, QPainterPath, QPainter
# from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPathItem


import sys
from PySide2.QtCore import Qt, QPointF, QPoint
from PySide2.QtGui import QPen, QColor, QPainterPath, QPainter
from PySide2.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPathItem, QMainWindow, QVBoxLayout, QWidget


class Grid(QGraphicsPathItem):
    def __init__(self, width, height, spacing, grid_color=QColor(230, 230, 230)):
        super().__init__()
        self.width = width
        self.height = height
        self.spacing = spacing
        self.grid_color = grid_color
        self.create_grid()

    def create_grid(self):
        pen = QPen(self.grid_color)
        pen.setWidth(1)
        self.setPen(pen)

        path = QPainterPath()

        for x in range(0, self.width + 1, self.spacing):
            path.moveTo(x, 0)
            path.lineTo(x, self.height)

        for y in range(0, self.height + 1, self.spacing):
            path.moveTo(0, y)
            path.lineTo(self.width, y)

        self.setPath(path)


class CustomGraphicsView(QGraphicsView):
    def __init__(self, background_color=Qt.white, grid_color=QColor(230, 230, 230)):
        super().__init__()

        self.background_color = background_color
        self.grid_color = grid_color

        # Set up the scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 2000, 2000)
        self.grid_item = Grid(1000, 1000, 50, grid_color=self.grid_color)
        self.grid_item.setPos(QPoint(500,500))
        self.scene.addItem(self.grid_item)

        # Remove the alignment line
        # self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setBackgroundBrush(QColor(self.background_color))

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        # Enable mouse tracking
        self.setMouseTracking(True)
        self.setInteractive(True)

        # Enable pan and zoom
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self._pan = False
        self.pan_start = QPoint(100, 100)

    def wheelEvent(self, event):
        zoom_factor = 1.15
        if event.angleDelta().y() < 0:
            zoom_factor = 1 / zoom_factor

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._pan = True
            self.pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)
    def mouseMoveEvent(self, event):
        if self._pan:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self.pan_start)
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.translate(delta.x(), delta.y())
            self.pan_start = event.pos()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self._pan = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = True
        elif event.key() == Qt.Key_F:
            self.f_pressed = True

        if self.shift_pressed and self.f_pressed:
            self.resetTransform()
            event.accept()
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication([])
    view = CustomGraphicsView(background_color=QColor(0, 0, 0), grid_color=QColor(230, 230, 230))
    view.show()
    sys.exit(app.exec_())


