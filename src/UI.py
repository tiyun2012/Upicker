import sys
from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMainWindow, QAction, QGridLayout
from PySide2.QtGui import QPainter, QPen, QColor
from PySide2.QtCore import Qt

class GridGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_enabled = True

    def drawBackground(self, painter, rect):
        if self.grid_enabled:
            grid_size = 20
            left = int(rect.left()) - (int(rect.left()) % grid_size)
            top = int(rect.top()) - (int(rect.top()) % grid_size)

            lines = []
            for x in range(left, int(rect.right()), grid_size):
                lines.append((x, rect.top(), x, rect.bottom()))
            for y in range(top, int(rect.bottom()), grid_size):
                lines.append((rect.left(), y, rect.right(), y))

            grid_pen = QPen(QColor(200, 200, 255, 125))
            painter.setPen(grid_pen)
            for line in lines:
                painter.drawLine(*line)

        super().drawBackground(painter, rect)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = GridGraphicsView(self)
        self.scene = QGraphicsScene(self)

        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.init_actions()
        self.init_menu()

    def init_actions(self):
        self.toggle_grid_action = QAction("Toggle Grid", self)
        self.toggle_grid_action.triggered.connect(self.toggle_grid)

        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.triggered.connect(self.zoom_in)

        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.triggered.connect(self.zoom_out)

    def init_menu(self):
        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.toggle_grid_action)
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)

    def toggle_grid(self):
        self.view.grid_enabled = not self.view.grid_enabled
        self.view.viewport().update()

    def zoom_in(self):
        self.view.setTransform(self.view.transform().scale(1.2, 1.2))

    def zoom_out(self):
        self.view.setTransform(self.view.transform().scale(1 / 1.2, 1 / 1.2))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())