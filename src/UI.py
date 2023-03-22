import sys
from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem, QMainWindow, QAction, QGridLayout
from PySide2.QtGui import QPainter, QPen, QColor,QIcon
from PySide2.QtCore import Qt

class GridGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_enabled = True

    def drawBackground(self, painter, rect):
        # Draw grid lines if grid is enabled
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

        # Call parent's drawBackground method to ensure other background elements are drawn correctly
        super().drawBackground(painter, rect)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window icon
        self.setWindowIcon(QIcon('./pictures/upicker.png'))
        # Create custom QGraphicsView and QGraphicsScene instances
        self.view = GridGraphicsView(self)
        self.scene = QGraphicsScene(self)

        # Set the QGraphicsScene as the scene for the QGraphicsView
        self.view.setScene(self.scene)
        # Set the QGraphicsView as the central widget of the QMainWindow
        self.setCentralWidget(self.view)

        # Initialize QAction objects for toggling grid and zooming in/out
        self.init_actions()
        # Initialize the menu bar with the QAction objects
        self.init_menu()

    def init_actions(self):
        # QAction for toggling the grid
        self.toggle_grid_action = QAction("Toggle Grid", self)
        self.toggle_grid_action.triggered.connect(self.toggle_grid)

        # QAction for zooming in
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.triggered.connect(self.zoom_in)

        # QAction for zooming out
        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.triggered.connect(self.zoom_out)

    def init_menu(self):
        # Create a 'View' menu in the menu bar
        view_menu = self.menuBar().addMenu("View")
        # Add QAction objects for toggling grid and zooming in/out to the 'View' menu
        view_menu.addAction(self.toggle_grid_action)
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)

    def toggle_grid(self):
        # Toggle the grid_enabled attribute of the QGraphicsView and update the viewport
        self.view.grid_enabled = not self.view.grid_enabled
        self.view.viewport().update()

    def zoom_in(self):
        # Scale the QGraphicsView's transform to zoom in
        self.view.setTransform(self.view.transform().scale(1.2, 1.2))

    def zoom_out(self):
        # Scale the QGraphicsView's transform to zoom out
        self.view.setTransform(self.view.transform().scale(1 / 1.2, 1 / 1.2))

if __name__ == "__main__":
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Create and show the MainWindow instance
    window = MainWindow()
    window.show()

    # Execute the QApplication event loop and exit with the return code
    sys.exit(app.exec_())

