import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide2.QtGui import QPainter, QPolygon, QColor, QPen
from PySide2.QtCore import QPoint, Qt

class TriangleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.draw_triangle = False
        self.triangle_pos = QPoint(0, 0)
        self.dragging = False
        self.mouse_offset = QPoint(0, 0)

    def paintEvent(self, event):
        if self.draw_triangle:
            painter = QPainter(self)
            painter.setBrush(QColor(255, 0, 0))
            painter.setPen(QPen(Qt.black, 2))

            triangle = QPolygon([
                QPoint(self.width() // 2, self.height() // 4),
                QPoint(self.width() // 4, 3 * self.height() // 4),
                QPoint(3 * self.width() // 4, 3 * self.height() // 4)
            ])

            triangle.translate(self.triangle_pos)

            painter.drawPolygon(triangle)
            painter.end()

    def display_triangle(self):
        self.draw_triangle = True
        self.update()

    def mousePressEvent(self, event):
        if not self.draw_triangle:
            return

        triangle = QPolygon([
            QPoint(self.width() // 2, self.height() // 4),
            QPoint(self.width() // 4, 3 * self.height() // 4),
            QPoint(3 * self.width() // 4, 3 * self.height() // 4)
        ])

        triangle.translate(self.triangle_pos)

        if triangle.containsPoint(event.pos(), Qt.WindingFill):
            self.dragging = True
            self.mouse_offset = self.triangle_pos - event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.triangle_pos = event.pos() + self.mouse_offset
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = False

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.triangle_widget = TriangleWidget()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        button = QPushButton('Draw Triangle')
        button.clicked.connect(self.triangle_widget.display_triangle)

        layout.addWidget(button)
        layout.addWidget(self.triangle_widget)

        self.setLayout(layout)
        self.setWindowTitle('Draw Triangle Example')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
