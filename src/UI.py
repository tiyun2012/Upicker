import sys
from PySide2.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene, QMainWindow, QAction, QColorDialog, QInputDialog,
                               QVBoxLayout, QLabel, QPushButton, QSpinBox, QGroupBox, QWidget, QToolBar)
from PySide2.QtGui import QPainter, QPen, QColor
from PySide2.QtCore import Qt

class GridGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_enabled = True
        self.grid_color = QColor(200, 200, 255, 125)
        self.grid_thickness = 1
        self.pan_enabled = False
        self.last_pos = None

    def drawForeground(self, painter, rect):
        if self.grid_enabled:
            grid_size = 20
            left = int(rect.left()) - (int(rect.left()) % grid_size)
            top = int(rect.top()) - (int(rect.top()) % grid_size)

            lines = []
            for x in range(left, int(rect.right()), grid_size):
                lines.append((x, rect.top(), x, rect.bottom()))
            for y in range(top, int(rect.bottom()), grid_size):
                lines.append((rect.left(), y, rect.right(), y))

            grid_pen = QPen(self.grid_color, self.grid_thickness, Qt.SolidLine)
            painter.setPen(grid_pen)
            for line in lines:
                painter.drawLine(*line)

        super().drawForeground(painter, rect)

    def set_background_color(self, color):
        self.setBackgroundBrush(color)

    def mousePressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.buttons() == Qt.RightButton:
            self.pan_enabled = True
            self.last_pos = event.pos()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.pan_enabled:
            delta = self.last_pos - event.pos()
            self.last_pos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + delta.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.pan_enabled:
            self.pan_enabled = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.view = GridGraphicsView(self)
        self.scene = QGraphicsScene(self)

        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.init_actions()
        self.init_menu()
        self.init_toolbox()
        self.pan_start_pos = None
    def init_actions(self):
        self.toggle_grid_action = QAction("Toggle Grid", self)
        self.toggle_grid_action.triggered.connect(self.toggle_grid)

        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.triggered.connect(self.zoom_in)

        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.bg_color_action = QAction("Background Color", self)
        self.bg_color_action.triggered.connect(self.select_bg_color)

    def init_menu(self):
        view_menu = self.menuBar().addMenu("options")
        view_menu.addAction(self.toggle_grid_action)
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.bg_color_action)

    def init_toolbox(self):
        grid_toolbox = QGroupBox("Grid Options")
        layout = QVBoxLayout()

        grid_color_label = QLabel("Grid Color:")
        layout.addWidget(grid_color_label)

        grid_color_button = QPushButton("Select Grid Color")
        grid_color_button.clicked.connect(self.select_grid_color)
        layout.addWidget(grid_color_button)

        grid_thickness_label = QLabel("Grid Thickness:")
        layout.addWidget(grid_thickness_label)

        grid_thickness_spinbox = QSpinBox()
        grid_thickness_spinbox.setRange(1, 10)
        grid_thickness_spinbox.setValue(self.view.grid_thickness)
        grid_thickness_spinbox.valueChanged.connect(self.set_grid_thickness)
        layout.addWidget(grid_thickness_spinbox)

        grid_toolbox.setLayout(layout)


        # pan

        self.create_tool_bar(grid_toolbox)

    def create_tool_bar(self, widget):
        tool_bar = QToolBar(self)
        tool_bar.addWidget(widget)
        self.addToolBar(Qt.RightToolBarArea, tool_bar)


    def toggle_grid(self):
        self.view.grid_enabled = not self.view.grid_enabled
        self.view.viewport().update()

    def zoom_in(self):
        # self.view.setTransform(self.view.transform().scale(1.2, 1.2))
        self.view.setTransform(self.view.transform().translate(2,0))

    def zoom_out(self):
        self.view.setTransform(self.view.transform().scale(1 / 1.2, 1 / 1.2))

    def select_grid_color(self):
        color = QColorDialog.getColor(initial=self.view.grid_color, parent=self, title="Select Grid Color")
        if color.isValid():
            self.view.grid_color = color
            self.view.viewport().update()

    def set_grid_thickness(self, value):
        self.view.grid_thickness = value
        self.view.viewport().update()

    def select_bg_color(self):
        color = QColorDialog.getColor(initial=self.view.backgroundBrush().color(), parent=self, title="Select Background Color")
        if color.isValid():
            self.view.set_background_color(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())